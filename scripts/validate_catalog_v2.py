#!/usr/bin/env python3
"""Validate catalog records against the v2 schema and migration rules.

Coexists with the live v1 validator until PR-07 cutover. This command does not
modify live shards. Pass fixture catalogs or migrated shards explicitly.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "catalog.schema.v2.json"
DEFAULT_INDEX = ROOT / "catalog" / "resources.yaml"

EMERGING_SHORT_SECTIONS = {
    "Instruments and Laboratories",
    "Agents, Access, and Policy",
}


def load_schema() -> dict[str, Any]:
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


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


def load_all_live_ids() -> set[str]:
    if not DEFAULT_INDEX.exists():
        return set()
    catalog = load_catalog_from_index(DEFAULT_INDEX)
    return {resource_id for resource in catalog["resources"] if (resource_id := resource.get("id"))}


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


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def is_v2_resource(resource: dict[str, Any]) -> bool:
    return "summary" in resource


def semantic_errors(
    catalog: dict[str, Any],
    *,
    known_ids: set[str] | None = None,
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

        forbidden_legacy = {"evidence_level", "maintenance_signal", "north_star_utility", "description"}
        present_legacy = sorted(forbidden_legacy & set(resource))
        if present_legacy:
            errors.append(f"{resource_id}: legacy fields present: {present_legacy}")

    return errors


def validate_catalog(
    catalog: dict[str, Any],
    *,
    known_ids: set[str] | None = None,
) -> list[str]:
    schema = load_schema()
    errors: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(catalog), key=lambda item: list(item.absolute_path)):
        path = ".".join(str(part) for part in error.absolute_path) or "catalog"
        errors.append(f"schema:{path}: {error.message}")
    errors.extend(semantic_errors(catalog, known_ids=known_ids))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog",
        type=Path,
        action="append",
        default=None,
        help="Catalog document or shard to validate (repeatable). Defaults to no live-data check.",
    )
    parser.add_argument(
        "--fixtures-dir",
        type=Path,
        default=ROOT / "tests" / "fixtures" / "v2",
        help="Directory of *.valid.yaml / *.invalid.yaml fixtures",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Also validate the live catalog index (expected to fail until migration completes)",
    )
    args = parser.parse_args()

    failures = 0
    live_ids = load_all_live_ids()

    if args.fixtures_dir.is_dir():
        for path in sorted(args.fixtures_dir.glob("*.yaml")):
            catalog = load_catalog_document(path)
            catalog_ids = {resource_id for resource in catalog["resources"] if (resource_id := resource.get("id"))}
            errors = validate_catalog(catalog, known_ids=live_ids | catalog_ids)
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

    catalogs: list[Path] = list(args.catalog or [])
    if args.live:
        catalogs.append(DEFAULT_INDEX)

    for path in catalogs:
        catalog = load_catalog_from_index(path) if path.name == "resources.yaml" else load_catalog_document(path)
        catalog_ids = {resource_id for resource in catalog["resources"] if (resource_id := resource.get("id"))}
        errors = validate_catalog(catalog, known_ids=live_ids | catalog_ids)
        if errors:
            print(f"ERROR: {path}:", file=sys.stderr)
            for error in errors:
                print(f"  {error}", file=sys.stderr)
            failures += 1
        else:
            print(f"Validated v2 catalog {path} with {len(catalog['resources'])} resource(s).")

    if failures:
        print(f"v2 validation failed with {failures} failure group(s).", file=sys.stderr)
        return 1
    print("Catalog v2 validation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
