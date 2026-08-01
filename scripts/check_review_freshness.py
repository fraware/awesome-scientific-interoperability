#!/usr/bin/env python3
"""Fail when catalog resources have expired review_due_on dates."""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "catalog" / "resources.yaml"


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


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


def review_freshness_errors(
    resources: list[dict[str, Any]],
    *,
    as_of: date,
) -> list[str]:
    errors: list[str] = []
    for resource in resources:
        resource_id = resource.get("id", "<missing>")
        review_due_on = resource.get("review_due_on")
        if not isinstance(review_due_on, str):
            continue
        try:
            due = parse_date(review_due_on)
        except ValueError as exc:
            errors.append(f"{resource_id}: invalid review_due_on: {exc}")
            continue
        if due < as_of:
            errors.append(
                f"{resource_id}: review_due_on {review_due_on} precedes as-of date {as_of.isoformat()}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog",
        type=Path,
        default=DEFAULT_INDEX,
        help="Catalog index path (default: live catalog)",
    )
    parser.add_argument(
        "--as-of",
        type=str,
        default=None,
        help="Reference date YYYY-MM-DD (default: today)",
    )
    args = parser.parse_args()

    try:
        as_of = parse_date(args.as_of) if args.as_of else date.today()
    except ValueError as exc:
        print(f"ERROR: invalid --as-of date: {exc}", file=sys.stderr)
        return 1

    catalog = load_catalog_from_index(args.catalog)
    errors = review_freshness_errors(catalog["resources"], as_of=as_of)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Review freshness failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(
        f"Review freshness OK for {len(catalog['resources'])} resource(s) as of {as_of.isoformat()}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
