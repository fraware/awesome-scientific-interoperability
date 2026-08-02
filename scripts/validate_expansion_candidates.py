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

    for item in candidates:
        cid = item.get("id", "<missing>")
        if item.get("official_url") not in item.get("primary_sources", []):
            errors.append(f"{cid}: official_url must appear in primary_sources")
        if item.get("priority") == "P0" and item.get("disposition") != "admission-pr":
            errors.append(f"{cid}: P0 candidates must use disposition admission-pr")
        if item.get("disposition") == "admission-pr" and len(item.get("primary_sources", [])) < 3:
            errors.append(f"{cid}: admission-pr requires at least three primary sources")
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
    if isinstance(program_size, int) and len(candidates) + len(completed) != program_size:
        errors.append(
            "candidate registry plus completed outcomes must equal research_program_size"
        )
    if len(candidates) < 40:
        errors.append("candidate registry must retain at least 40 unresolved researched candidates")
    families = {item.get("coverage_family") for item in candidates}
    if len(families) < 35:
        errors.append("candidate registry must cover at least 35 distinct unresolved interoperability families")

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
    counts = Counter(item["priority"] for item in candidates)
    dispositions = Counter(item["disposition"] for item in candidates)
    print(
        f"Validated {len(candidates)} expansion candidates across "
        f"{len({item['coverage_family'] for item in candidates})} families; "
        f"priorities={dict(sorted(counts.items()))}; "
        f"dispositions={dict(sorted(dispositions.items()))}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
