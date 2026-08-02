#!/usr/bin/env python3
"""Validate the evidence-backed corpus expansion candidate registry."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "catalog" / "expansion-candidates.yaml"
SCHEMA_PATH = ROOT / "schema" / "expansion-candidates.schema.json"
CATALOG_INDEX = ROOT / "catalog" / "resources.yaml"
WATCHLIST_PATH = ROOT / "catalog" / "watchlist.yaml"

TERMINAL_DISPOSITIONS = frozenset(
    {
        "rejected-out-of-scope",
        "rejected-represented-by",
        "deferred-family-review",
    }
)
ACTIVE_DISPOSITIONS = frozenset({"admission-pr", "boundary-review", "watchlist"})


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def live_resource_keys() -> tuple[set[str], set[str], set[str]]:
    index = load_yaml(CATALOG_INDEX)
    ids: set[str] = set()
    names: set[str] = set()
    urls: set[str] = set()
    for relative in index.get("resource_files", []):
        shard = load_yaml(CATALOG_INDEX.parent / relative)
        for item in shard.get("resources", []):
            ids.add(item["id"])
            names.add(item["name"])
            urls.add(item["url"])
    return ids, names, urls


def watchlist_keys() -> tuple[set[str], set[str], set[str]]:
    payload = load_yaml(WATCHLIST_PATH)
    items = payload.get("items", [])
    return (
        {item["id"] for item in items},
        {item["name"] for item in items},
        {item["url"] for item in items},
    )


def load_registry() -> dict[str, Any]:
    index = load_yaml(DATA_PATH)
    if not isinstance(index, dict):
        raise ValueError("expansion candidate index must be a mapping")
    payload = {key: value for key, value in index.items() if key != "candidate_files"}
    candidates: list[dict[str, Any]] = []
    seen_files: set[str] = set()
    for relative in index.get("candidate_files", []):
        if relative in seen_files:
            raise ValueError(f"duplicate candidate shard: {relative}")
        seen_files.add(relative)
        shard_path = DATA_PATH.parent / relative
        shard = load_yaml(shard_path)
        if not isinstance(shard, dict) or not isinstance(shard.get("candidates"), list):
            raise ValueError(f"invalid candidate shard: {relative}")
        candidates.extend(shard["candidates"])
    payload["candidates"] = candidates
    return payload


def validate() -> list[str]:
    errors: list[str] = []
    try:
        payload = load_registry()
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [str(exc)]
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(payload), key=lambda item: list(item.absolute_path)):
        loc = ".".join(str(part) for part in error.absolute_path) or DATA_PATH.name
        errors.append(f"schema:{loc}: {error.message}")

    candidates = payload.get("candidates", []) if isinstance(payload, dict) else []
    for field in ("id", "name", "official_url"):
        values = [item.get(field) for item in candidates]
        duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
        if duplicates:
            errors.append(f"duplicate {field}: {duplicates}")

    live_ids, live_names, live_urls = live_resource_keys()
    watch_ids, watch_names, watch_urls = watchlist_keys()

    active: list[dict[str, Any]] = []
    terminal: list[dict[str, Any]] = []

    for item in candidates:
        cid = item.get("id", "<missing>")
        disposition = item.get("disposition")
        if item.get("official_url") not in item.get("primary_sources", []):
            errors.append(f"{cid}: official_url must appear in primary_sources")
        if disposition in TERMINAL_DISPOSITIONS:
            terminal.append(item)
            if item.get("priority") == "P0":
                errors.append(f"{cid}: terminal dispositions must not use priority P0")
            if disposition == "rejected-represented-by":
                represented = item.get("represented_by_resource_ids") or []
                if not represented:
                    errors.append(f"{cid}: rejected-represented-by requires represented_by_resource_ids")
                missing = sorted(set(represented) - live_ids)
                if missing:
                    errors.append(
                        f"{cid}: represented_by_resource_ids missing from main catalog: {missing}"
                    )
            if disposition == "deferred-family-review":
                if not item.get("scheduled_review") and not item.get("deferred_family_id"):
                    errors.append(
                        f"{cid}: deferred-family-review requires scheduled_review or deferred_family_id"
                    )
        elif disposition in ACTIVE_DISPOSITIONS:
            active.append(item)
            if item.get("priority") == "P0" and disposition != "admission-pr":
                errors.append(f"{cid}: P0 candidates must use disposition admission-pr")
            if disposition == "admission-pr" and len(item.get("primary_sources", [])) < 3:
                errors.append(f"{cid}: admission-pr requires at least three primary sources")
            next_step = (item.get("next_step") or "").strip()
            if not next_step:
                errors.append(f"{cid}: active dispositions require a non-empty next_step")
            if not item.get("review_due_on"):
                errors.append(
                    f"{cid}: active disposition {disposition} requires review_due_on"
                )
        else:
            errors.append(f"{cid}: unknown disposition {disposition!r}")

        if cid in live_ids or item.get("name") in live_names or item.get("official_url") in live_urls:
            errors.append(f"{cid}: candidate already exists in the main catalog")

        watch_overlap = (
            cid in watch_ids
            or item.get("name") in watch_names
            or item.get("official_url") in watch_urls
        )
        if watch_overlap and item.get("current_repository_state") != "watchlist":
            errors.append(f"{cid}: watchlist overlap requires current_repository_state: watchlist")
        if not watch_overlap and "current_repository_state" in item:
            errors.append(f"{cid}: current_repository_state is set but no watchlist overlap exists")

    completed = payload.get("completed_candidate_ids", [])
    completed_set = set(completed)
    candidate_ids = {item.get("id") for item in candidates}
    overlap = sorted(completed_set & candidate_ids)
    if overlap:
        errors.append(f"completed candidates still present in registry: {overlap}")
    unknown_completed = sorted(completed_set - live_ids)
    if unknown_completed:
        errors.append(f"completed candidate IDs missing from main catalog: {unknown_completed}")

    program_size = payload.get("research_program_size")
    unresolved_active = len(active)
    completed_admitted = len(completed)
    completed_negative = len(terminal)
    if isinstance(program_size, int):
        if unresolved_active + completed_admitted + completed_negative != program_size:
            errors.append(
                "conservation failed: unresolved_active + completed_admitted + "
                "completed_negative must equal research_program_size "
                f"({unresolved_active} + {completed_admitted} + {completed_negative} "
                f"!= {program_size})"
            )
    if not isinstance(program_size, int) or program_size < 60:
        errors.append("research_program_size must preserve the comprehensive landscape baseline (>=60)")

    families = {item.get("coverage_family") for item in active}
    minimum_family_count = max(1, (4 * len(active) + 4) // 5) if active else 0
    if len(families) < minimum_family_count:
        errors.append(
            "unresolved active candidate families must cover at least 80% of unresolved active records"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Expansion-candidate validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    payload = load_registry()
    candidates = payload["candidates"]
    active = [item for item in candidates if item["disposition"] in ACTIVE_DISPOSITIONS]
    terminal = [item for item in candidates if item["disposition"] in TERMINAL_DISPOSITIONS]
    counts = Counter(item["priority"] for item in active)
    dispositions = Counter(item["disposition"] for item in candidates)
    print(
        f"Validated {len(candidates)} expansion candidates "
        f"({len(active)} active, {len(terminal)} terminal) across "
        f"{len({item['coverage_family'] for item in active})} active families; "
        f"active_priorities={dict(sorted(counts.items()))}; "
        f"dispositions={dict(sorted(dispositions.items()))}; "
        f"completed_admitted={len(payload['completed_candidate_ids'])}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
