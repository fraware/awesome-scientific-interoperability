#!/usr/bin/env python3
"""Validate watchlist schema, editorial invariants, and docs/watchlist.md parity."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
WATCHLIST_PATH = ROOT / "catalog" / "watchlist.yaml"
SCHEMA_PATH = ROOT / "schema" / "watchlist.schema.json"
PROSE_PATH = ROOT / "docs" / "watchlist.md"
CATALOG_INDEX_PATH = ROOT / "catalog" / "resources.yaml"
ENTRY_RE = re.compile(r"^- \[([^\]]+)\]\((https://[^)]+)\) - (.+)$")
CANDIDATE_SECTIONS = {
    "Foundations",
    "Identifiers and Discovery",
    "Metadata and Semantics",
    "Data and Digital Objects",
    "Research Software and Environments",
    "Workflows and Execution",
    "Provenance and Evidence",
    "Knowledge Systems and Publications",
    "Instruments and Laboratories",
    "Agents, Access, and Policy",
    "Validation and Conformance",
}


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def load_watchlist(path: Path = WATCHLIST_PATH) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_schema() -> dict[str, Any]:
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_catalog_ids() -> set[str]:
    if not CATALOG_INDEX_PATH.exists():
        return set()
    with CATALOG_INDEX_PATH.open(encoding="utf-8") as handle:
        index = yaml.safe_load(handle)
    ids: set[str] = set()
    for relative_path in index.get("resource_files", []):
        path = CATALOG_INDEX_PATH.parent / relative_path
        with path.open(encoding="utf-8") as handle:
            shard = yaml.safe_load(handle)
        for resource in shard.get("resources", []):
            resource_id = resource.get("id")
            if isinstance(resource_id, str):
                ids.add(resource_id)
    return ids


def prose_entries(prose: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for raw in prose.splitlines():
        match = ENTRY_RE.match(raw)
        if match:
            name, url, description = match.groups()
            entries.append({"name": name, "url": url, "description": description})
    return entries


def semantic_errors(
    watchlist: dict[str, Any],
    *,
    as_of: date | None = None,
    catalog_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    items = watchlist.get("items", [])
    reference_date = as_of or date.today()

    for field in ("id", "name", "url"):
        values = [item.get(field) for item in items]
        duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
        if duplicates:
            errors.append(f"duplicate {field}: {duplicates}")

    if catalog_ids is None:
        catalog_ids = load_catalog_ids()

    for item in items:
        item_id = item.get("id", "<missing>")
        candidate_section = item.get("candidate_section")
        if candidate_section not in CANDIDATE_SECTIONS:
            errors.append(f"{item_id}: unknown candidate_section {candidate_section!r}")

        reviewed_on = item.get("reviewed_on")
        review_due_on = item.get("review_due_on")
        if isinstance(reviewed_on, str) and isinstance(review_due_on, str):
            try:
                start = parse_date(reviewed_on)
                due = parse_date(review_due_on)
            except ValueError as exc:
                errors.append(f"{item_id}: invalid review date: {exc}")
            else:
                if due <= start:
                    errors.append(f"{item_id}: review_due_on must be later than reviewed_on")
                if due < reference_date:
                    errors.append(
                        f"{item_id}: review_due_on {review_due_on} precedes as-of date "
                        f"{reference_date.isoformat()}"
                    )

        if item_id in catalog_ids:
            errors.append(f"{item_id}: watchlist id conflicts with main-list catalog id")

    return errors


def validate_watchlist(
    watchlist: dict[str, Any],
    schema: dict[str, Any],
    *,
    as_of: date | None = None,
    catalog_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(watchlist), key=lambda item: list(item.absolute_path)):
        path = ".".join(str(part) for part in error.absolute_path) or "watchlist"
        errors.append(f"schema:{path}: {error.message}")
    errors.extend(semantic_errors(watchlist, as_of=as_of, catalog_ids=catalog_ids))
    return errors


def parity_errors(watchlist: dict[str, Any], prose: str) -> list[str]:
    errors: list[str] = []
    items = watchlist.get("items", [])
    watchlist_keyed = {(item["name"], item["url"]): item for item in items}
    prose_items = prose_entries(prose)
    prose_keyed = {(item["name"], item["url"]): item for item in prose_items}

    missing_prose = sorted(set(watchlist_keyed) - set(prose_keyed))
    missing_yaml = sorted(set(prose_keyed) - set(watchlist_keyed))
    if missing_prose:
        errors.append(f"watchlist items missing from docs/watchlist.md: {missing_prose}")
    if missing_yaml:
        errors.append(f"docs/watchlist.md entries missing from watchlist.yaml: {missing_yaml}")

    for key in sorted(set(watchlist_keyed) & set(prose_keyed)):
        item = watchlist_keyed[key]
        prose_item = prose_keyed[key]
        reason = item.get("reason", "")
        if reason != prose_item["description"]:
            errors.append(
                f"{item['id']}: docs/watchlist.md reason mismatch: "
                f"{prose_item['description']!r} != {reason!r}"
            )
    return errors


def validate(*, as_of: date | None = None) -> list[str]:
    watchlist = load_watchlist()
    schema = load_schema()
    prose = PROSE_PATH.read_text(encoding="utf-8")
    errors = validate_watchlist(watchlist, schema, as_of=as_of)
    errors.extend(parity_errors(watchlist, prose))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--as-of",
        type=str,
        default=None,
        help="Reference date YYYY-MM-DD for review freshness (default: today)",
    )
    parser.add_argument(
        "--watchlist",
        type=Path,
        default=WATCHLIST_PATH,
        help="Watchlist YAML path (default: live watchlist)",
    )
    args = parser.parse_args()

    as_of: date | None
    try:
        as_of = parse_date(args.as_of) if args.as_of else None
    except ValueError as exc:
        print(f"ERROR: invalid --as-of date: {exc}", file=sys.stderr)
        return 1

    if args.watchlist == WATCHLIST_PATH:
        errors = validate(as_of=as_of)
    else:
        watchlist = load_watchlist(args.watchlist)
        schema = load_schema()
        errors = validate_watchlist(watchlist, schema, as_of=as_of)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Watchlist validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    watchlist = load_watchlist(args.watchlist)
    prose_count = len(prose_entries(PROSE_PATH.read_text(encoding="utf-8")))
    print(
        f"Validated {len(watchlist.get('items', []))} watchlist item(s) "
        f"and {prose_count} prose entr{'y' if prose_count == 1 else 'ies'}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
