#!/usr/bin/env python3
"""Validate catalog schema, editorial invariants, and README/catalog parity."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

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


def load() -> tuple[dict, dict, str]:
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        index = yaml.safe_load(handle)

    resource_files = index.get("resource_files", [])
    if not isinstance(resource_files, list) or not resource_files:
        raise ValueError("catalog index must define a non-empty resource_files list")

    resources = []
    seen_files = set()
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


def is_v2_resource(resource: dict) -> bool:
    return "summary" in resource


def resource_description(resource: dict) -> str:
    if is_v2_resource(resource):
        return resource.get("summary", "")
    return resource.get("description", "")


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


def validate() -> list[str]:
    catalog, schema, readme = load()
    errors: list[str] = []

    v1_resource_schema = schema["properties"]["resources"]["items"]
    v1_validator = Draft202012Validator(v1_resource_schema, format_checker=FormatChecker())

    for field in ("catalog_version", "reviewed_on", "north_star"):
        if field not in catalog:
            errors.append(f"schema:catalog: missing required field {field!r}")

    resources = catalog.get("resources", [])
    if len(resources) < schema["properties"]["resources"].get("minItems", 1):
        errors.append(
            f"schema:resources: array is too short ({len(resources)} < "
            f"{schema['properties']['resources']['minItems']})"
        )

    for field in ("id", "name", "url"):
        values = [resource.get(field) for resource in resources]
        duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
        if duplicates:
            errors.append(f"duplicate {field}: {duplicates}")

    all_ids = {resource.get("id") for resource in resources if resource.get("id")}
    v2_resources = [resource for resource in resources if is_v2_resource(resource)]

    if v2_resources:
        import validate_catalog_v2

        v2_catalog = {
            "catalog_version": catalog["catalog_version"],
            "reviewed_on": catalog["reviewed_on"],
            "north_star": catalog["north_star"],
            "resources": v2_resources,
        }
        errors.extend(validate_catalog_v2.validate_catalog(v2_catalog, known_ids=all_ids))

    for resource in resources:
        if is_v2_resource(resource):
            continue
        resource_id = resource.get("id", "<missing>")
        for error in sorted(v1_validator.iter_errors(resource), key=lambda item: list(item.absolute_path)):
            path = ".".join(str(part) for part in error.absolute_path) or resource_id
            errors.append(f"schema:{resource_id}.{path}: {error.message}")

    for resource in resources:
        description = resource_description(resource)
        if description and description[0].isalpha() and not description[0].isupper():
            errors.append(f"{resource.get('id')}: description must start with an uppercase character")
        if description and not description.endswith("."):
            errors.append(f"{resource.get('id')}: description must end with a period")
        lower = description.casefold()
        for phrase in BANNED_MARKETING:
            if phrase in lower:
                errors.append(f"{resource.get('id')}: promotional phrase: {phrase}")
        if len(description) > 260:
            errors.append(f"{resource.get('id')}: description exceeds 260 characters")
        if len(resource.get("connects", [])) < 2:
            errors.append(f"{resource.get('id')}: must identify at least two connected objects or systems")

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
        catalog_description = resource_description(catalog_item)
        if catalog_description != readme_item["description"]:
            errors.append(
                f"{catalog_item['id']}: README/catalog description mismatch: "
                f"{readme_item['description']!r} != {catalog_description!r}"
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--schema-version",
        choices=("1", "2"),
        default="1",
        help="Schema major version. Version 2 validates fixtures via validate_catalog_v2 and does not require live v1 shards to pass v2.",
    )
    args = parser.parse_args()
    if args.schema_version == "2":
        # Preserve argv for callers, but run the v2 CLI entry with fixture defaults only.
        import validate_catalog_v2

        argv_backup = sys.argv[:]
        try:
            sys.argv = [str(ROOT / "scripts" / "validate_catalog_v2.py")]
            return validate_catalog_v2.main()
        finally:
            sys.argv = argv_backup

    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    catalog, _, readme = load()
    print(f"Validated {len(catalog['resources'])} catalog entries and {len(readme_entries(readme))} README entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
