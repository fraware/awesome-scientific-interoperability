#!/usr/bin/env python3
"""Validate decision-guide resource-ID markers against the catalog."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "resources.yaml"
GUIDES_DIR = ROOT / "docs" / "decision-guides"

RESOURCE_MARKER_RE = re.compile(r"\[resource:([a-z0-9-]+)\]")


def load_catalog_ids() -> set[str]:
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        index = yaml.safe_load(handle)

    ids: set[str] = set()
    for relative_path in index.get("resource_files", []):
        path = CATALOG_PATH.parent / relative_path
        with path.open(encoding="utf-8") as handle:
            shard = yaml.safe_load(handle)
        for resource in shard.get("resources", []):
            resource_id = resource.get("id")
            if resource_id:
                ids.add(resource_id)
    return ids


def collect_markers(path: Path) -> list[tuple[int, str]]:
    markers: list[tuple[int, str]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for match in RESOURCE_MARKER_RE.finditer(line):
            markers.append((line_no, match.group(1)))
    return markers


def validate_guides(guides_dir: Path = GUIDES_DIR) -> list[str]:
    if not guides_dir.is_dir():
        return [f"missing decision-guides directory: {guides_dir.relative_to(ROOT)}"]

    catalog_ids = load_catalog_ids()
    errors: list[str] = []

    guide_files = sorted(guides_dir.glob("*.md"))
    if not guide_files:
        errors.append(f"no markdown files found in {guides_dir.relative_to(ROOT)}")
        return errors

    for guide_path in guide_files:
        for line_no, resource_id in collect_markers(guide_path):
            if resource_id not in catalog_ids:
                try:
                    rel = guide_path.relative_to(ROOT)
                except ValueError:
                    rel = guide_path
                errors.append(f"{rel}:{line_no}: unknown catalog id [resource:{resource_id}]")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--guides-dir",
        type=Path,
        default=GUIDES_DIR,
        help="Directory containing decision-guide markdown files",
    )
    args = parser.parse_args()

    errors = validate_guides(args.guides_dir)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Decision guides validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
