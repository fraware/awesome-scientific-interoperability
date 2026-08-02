#!/usr/bin/env python3
"""Minimal downstream consumer for published catalog.json dumps.

Usage:
  python examples/catalog_json_consumer.py path/to/catalog.json
  python examples/catalog_json_consumer.py path/to/catalog.json --evidence public-validator

This script is intentionally tiny: it proves a third party can consume joined
steward/implementation fields without cloning YAML shards. It never modifies
the catalog or README.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_catalog(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "resources" not in payload:
        raise ValueError("catalog.json must contain a top-level resources array")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog_json", type=Path, help="Path to catalog.json")
    parser.add_argument(
        "--evidence",
        help="Optional evidence_types filter (for example public-validator)",
    )
    args = parser.parse_args(argv)

    catalog = load_catalog(args.catalog_json)
    resources = catalog["resources"]
    if args.evidence:
        resources = [
            item for item in resources if args.evidence in (item.get("evidence_types") or [])
        ]

    print(f"catalog_version={catalog.get('meta', {}).get('catalog_version')}")
    print(f"resource_count={len(resources)}")
    for item in resources[:10]:
        steward = (item.get("steward") or {}).get("name") or item.get("steward_id")
        impl_count = len(item.get("implementations") or [])
        print(
            f"- {item['id']}: steward={steward!s}; "
            f"implementations={impl_count}; "
            f"relations={len(item.get('relations') or [])}"
        )
    if len(resources) > 10:
        print(f"... {len(resources) - 10} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
