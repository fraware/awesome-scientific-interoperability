#!/usr/bin/env python3
"""Validate catalog schema, editorial invariants, and README/catalog parity."""

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
CATALOG_PATH = ROOT / "catalog" / "resources.yaml"
SCHEMA_PATH = ROOT / "schema" / "catalog.schema.json"
README_PATH = ROOT / "README.md"
ENTRY_RE = re.compile(r"^- \[([^\]]+)\]\((https://[^)]+)\) - (.+)$")
BANNED_MARKETING = (
    "powerful platform",
    "innovative solution",
    "comprehensive solution",
    "industry-leading",
    "best-in-class",
    "revolutionary",
)
EMERGING_SHORT_SECTIONS = {
    "Instruments and Laboratories",
    "Agents, Access, and Policy",
}
FORBIDDEN_LEGACY_FIELDS = frozenset(
    {"evidence_level", "maintenance_signal", "north_star_utility", "description"}
)


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def load() -> tuple[dict[str, Any], dict[str, Any], str]:
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        index = yaml.safe_load(handle)

    resource_files = index.get("resource_files", [])
    if not isinstance(resource_files, list) or not resource_files:
        raise ValueError("catalog index must define a non-empty resource_files list")

    resources: list[dict[str, Any]] = []
    seen_files: set[str] = set()
    for relative_path in resource_files:
        if relative_path in seen_files:
            raise ValueError(f"duplicate resource file in catalog index: {relative_path}")
        seen_files.add(relative_path)
        path = CATALOG_PATH.parent / relative_path
        with path.open(encoding="utf-8") as handle:
            shard = yaml.safe_load(handle)
        shard_resources = shard.get("resources", [])
        section = shard.get("section")
        if not section or not isinstance(shard_resources, list):
            raise ValueError(f"invalid catalog shard: {relative_path}")
        for resource in shard_resources:
            if resource.get("section") != section:
                raise ValueError(
                    f"{relative_path}: resource {resource.get('id')} section does not match shard section"
                )
        resources.extend(shard_resources)

    catalog = {
        "catalog_version": index["catalog_version"],
        "reviewed_on": index["reviewed_on"],
        "north_star": index["north_star"],
        "resources": resources,
    }
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        schema = json.load(handle)
    readme = README_PATH.read_text(encoding="utf-8")
    return catalog, schema, readme


def load_catalog_from_index(index_path: Path) -> dict[str, Any]:
    with index_path.open(encoding="utf-8") as handle:
        index = yaml.safe_load(handle)
    resources: list[dict[str, Any]] = []
    for relative_path in index.get("resource_files", []):
        path = index_path.parent / relative_path
        with path.open(encoding="utf-8") as handle:
            shard = yaml.safe_load(handle)
        resources.extend(shard.get("resources", []))
    return {
        "catalog_version": index["catalog_version"],
        "reviewed_on": index["reviewed_on"],
        "north_star": index["north_star"],
        "resources": resources,
    }


def load_catalog_document(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    if "resources" in payload and "catalog_version" in payload:
        return payload
    if "resources" in payload and "section" in payload:
        return {
            "catalog_version": "2.0.0",
            "reviewed_on": date.today().isoformat(),
            "north_star": "A technically competent user should identify the strongest interoperability mechanism.",
            "resources": payload["resources"],
        }
    raise ValueError(f"unsupported catalog document: {path}")


def load_all_live_ids() -> set[str]:
    if not CATALOG_PATH.exists():
        return set()
    catalog = load_catalog_from_index(CATALOG_PATH)
    return {resource_id for resource in catalog["resources"] if (resource_id := resource.get("id"))}


def readme_entries(readme: str) -> list[dict[str, str]]:
    entries = []
    section = None
    for raw in readme.splitlines():
        if raw.startswith("## "):
            section = raw[3:].strip()
            continue
        match = ENTRY_RE.match(raw)
        if match and section not in {"Contents", "Related Lists"}:
            name, url, description = match.groups()
            entries.append({"name": name, "url": url, "description": description, "section": section or ""})
    return entries


def semantic_errors(
    catalog: dict[str, Any],
    *,
    known_ids: set[str] | None = None,
    as_of: date | None = None,
) -> list[str]:
    errors: list[str] = []
    resources = catalog.get("resources", [])
    ids = [resource.get("id") for resource in resources]
    for field in ("id", "name", "url"):
        values = [resource.get(field) for resource in resources]
        duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
        if duplicates:
            errors.append(f"duplicate {field}: {duplicates}")

    if known_ids is None:
        known_ids = {resource_id for resource_id in ids if isinstance(resource_id, str)}

    reference_date = as_of or date.today()
    for resource in resources:
        resource_id = resource.get("id", "<missing>")
        reviewed_on = resource.get("reviewed_on")
        review_due_on = resource.get("review_due_on")
        if isinstance(reviewed_on, str) and isinstance(review_due_on, str):
            try:
                start = parse_date(reviewed_on)
                due = parse_date(review_due_on)
            except ValueError as exc:
                errors.append(f"{resource_id}: invalid review date: {exc}")
            else:
                if due <= start:
                    errors.append(f"{resource_id}: review_due_on must be later than reviewed_on")
                interval = (due - start).days
                maturity = resource.get("maturity")
                section = resource.get("section")
                max_interval = 183 if maturity == "emerging" and section in EMERGING_SHORT_SECTIONS else 365
                if interval > max_interval:
                    errors.append(
                        f"{resource_id}: review interval {interval}d exceeds maximum {max_interval}d"
                    )
                if due < reference_date:
                    errors.append(
                        f"{resource_id}: review_due_on {review_due_on} precedes as-of date "
                        f"{reference_date.isoformat()}"
                    )

        for field in ("alternatives", "related_resource_ids"):
            for ref in resource.get(field, []):
                if ref == resource_id:
                    errors.append(f"{resource_id}: {field} must not self-reference")
                elif ref not in known_ids:
                    errors.append(f"{resource_id}: {field} unknown id {ref!r}")

        if resource.get("implementation_status") == "multiple-independent":
            if len(resource.get("source_urls", [])) < 2:
                errors.append(
                    f"{resource_id}: multiple-independent requires at least two source_urls"
                )

        if resource.get("conformance_status") in {"public-suite", "public-validator"}:
            if not resource.get("source_urls"):
                errors.append(
                    f"{resource_id}: public conformance evidence requires source_urls"
                )

        present_legacy = sorted(FORBIDDEN_LEGACY_FIELDS & set(resource))
        if present_legacy:
            errors.append(f"{resource_id}: legacy fields present: {present_legacy}")

    return errors


def validate_catalog(
    catalog: dict[str, Any],
    schema: dict[str, Any],
    *,
    known_ids: set[str] | None = None,
    as_of: date | None = None,
) -> list[str]:
    errors: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(catalog), key=lambda item: list(item.absolute_path)):
        path = ".".join(str(part) for part in error.absolute_path) or "catalog"
        errors.append(f"schema:{path}: {error.message}")
    errors.extend(semantic_errors(catalog, known_ids=known_ids, as_of=as_of))
    return errors


def validate(*, as_of: date | None = None) -> list[str]:
    catalog, schema, readme = load()
    errors = validate_catalog(catalog, schema, as_of=as_of)

    resources = catalog.get("resources", [])
    for resource in resources:
        resource_id = resource.get("id", "<missing>")
        summary = resource.get("summary", "")
        if summary and summary[0].isalpha() and not summary[0].isupper():
            errors.append(f"{resource_id}: summary must start with an uppercase character")
        if summary and not summary.endswith("."):
            errors.append(f"{resource_id}: summary must end with a period")
        lower = summary.casefold()
        for phrase in BANNED_MARKETING:
            if phrase in lower:
                errors.append(f"{resource_id}: promotional phrase: {phrase}")
        if len(summary) > 260:
            errors.append(f"{resource_id}: summary exceeds 260 characters")
        if len(resource.get("connects", [])) < 2:
            errors.append(f"{resource_id}: must identify at least two connected objects or systems")

    readme_items = readme_entries(readme)
    catalog_keyed = {(r["name"], r["url"]): r for r in resources}
    readme_keyed = {(r["name"], r["url"]): r for r in readme_items}

    missing_readme = sorted(set(catalog_keyed) - set(readme_keyed))
    missing_catalog = sorted(set(readme_keyed) - set(catalog_keyed))
    if missing_readme:
        errors.append(f"catalog entries missing from README: {missing_readme}")
    if missing_catalog:
        errors.append(f"README entries missing from catalog: {missing_catalog}")

    for key in sorted(set(catalog_keyed) & set(readme_keyed)):
        catalog_item = catalog_keyed[key]
        readme_item = readme_keyed[key]
        if catalog_item["section"] != readme_item["section"]:
            errors.append(
                f"{catalog_item['id']}: README/catalog section mismatch: "
                f"{readme_item['section']!r} != {catalog_item['section']!r}"
            )
        catalog_summary = catalog_item.get("summary", "")
        if catalog_summary != readme_item["description"]:
            errors.append(
                f"{catalog_item['id']}: README/catalog summary mismatch: "
                f"{readme_item['description']!r} != {catalog_summary!r}"
            )

    contents_index = readme.find("## Contents")
    first_section = re.search(r"^## .+$", readme, re.MULTILINE)
    if not first_section or first_section.group(0) != "## Contents":
        errors.append("Contents must be the first level-two section")
    if "## Contributing" in readme[contents_index: readme.find("## Selection Standard")]:
        errors.append("Contributing must not appear in Contents")
    if "## Footnotes" in readme[contents_index: readme.find("## Selection Standard")]:
        errors.append("Footnotes must not appear in Contents")

    return errors


def run_fixture_suite(fixtures_dir: Path, *, as_of: date | None = None) -> int:
    live_ids = load_all_live_ids()
    failures = 0
    for path in sorted(fixtures_dir.glob("*.yaml")):
        catalog = load_catalog_document(path)
        catalog_ids = {resource_id for resource in catalog["resources"] if (resource_id := resource.get("id"))}
        with SCHEMA_PATH.open(encoding="utf-8") as handle:
            schema = json.load(handle)
        errors = validate_catalog(catalog, schema, known_ids=live_ids | catalog_ids, as_of=as_of)
        expect_invalid = path.name.endswith(".invalid.yaml")
        if expect_invalid and not errors:
            print(f"ERROR: fixture {path.name} expected to be invalid but passed", file=sys.stderr)
            failures += 1
        elif not expect_invalid and errors:
            print(f"ERROR: fixture {path.name} expected to be valid:", file=sys.stderr)
            for error in errors:
                print(f"  {error}", file=sys.stderr)
            failures += 1
        else:
            state = "invalid" if expect_invalid else "valid"
            print(f"Fixture {path.name}: {state} as expected ({len(errors)} error(s)).")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--as-of",
        type=str,
        default=None,
        help="Reference date YYYY-MM-DD for review freshness (default: today)",
    )
    parser.add_argument(
        "--fixtures-dir",
        type=Path,
        default=None,
        help="Validate v2 fixture YAML files in this directory",
    )
    args = parser.parse_args()

    as_of: date | None
    try:
        as_of = parse_date(args.as_of) if args.as_of else None
    except ValueError as exc:
        print(f"ERROR: invalid --as-of date: {exc}", file=sys.stderr)
        return 1

    failures = 0
    if args.fixtures_dir is not None:
        if not args.fixtures_dir.is_dir():
            print(f"ERROR: fixtures directory not found: {args.fixtures_dir}", file=sys.stderr)
            return 1
        failures += run_fixture_suite(args.fixtures_dir, as_of=as_of)

    errors = validate(as_of=as_of)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1 if failures == 0 else 1

    if failures:
        print(f"Fixture validation failed with {failures} failure group(s).", file=sys.stderr)
        return 1

    catalog, _, readme = load()
    print(f"Validated {len(catalog['resources'])} catalog entries and {len(readme_entries(readme))} README entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
