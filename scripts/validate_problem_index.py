#!/usr/bin/env python3
"""Validate integration-problems.md problem identifiers and catalog cross-references."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "resources.yaml"
DEFAULT_DOC_PATH = ROOT / "docs" / "integration-problems.md"

PROBLEM_LINE_RE = re.compile(r"^\[problem:([a-z0-9-]+)\]\s*$", re.MULTILINE)
RESOURCE_MARKER_RE = re.compile(r"\[resource:([a-z0-9-]+)\]")

REQUIRED_PROBLEMS = frozenset(
    {
        "identify-research-objects",
        "discover-resources",
        "align-metadata-semantics",
        "package-research-objects",
        "describe-cite-software",
        "execute-workflows",
        "capture-provenance",
        "exchange-publications-claims",
        "integrate-laboratory-systems",
        "expose-tools-to-agents",
        "controlled-data-access",
        "validate-conformance",
        "exchange-computational-models",
        "exchange-neuroscience-data",
        "exchange-astronomy-data",
        "exchange-bioimaging-data",
    }
)

MAIN_SECTIONS = frozenset(
    {
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
)


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


def validate(doc_path: Path, catalog_ids: set[str]) -> list[str]:
    text = doc_path.read_text(encoding="utf-8")
    errors: list[str] = []

    problem_ids = PROBLEM_LINE_RE.findall(text)
    if not problem_ids:
        errors.append("no [problem:...] identifiers found")
        return errors

    seen_problems: set[str] = set()
    for problem_id in problem_ids:
        if problem_id in seen_problems:
            errors.append(f"duplicate problem identifier: {problem_id}")
        seen_problems.add(problem_id)

    missing_problems = sorted(REQUIRED_PROBLEMS - seen_problems)
    if missing_problems:
        errors.append(f"missing required problem identifiers: {', '.join(missing_problems)}")

    extra_problems = sorted(seen_problems - REQUIRED_PROBLEMS)
    if extra_problems:
        errors.append(f"unexpected problem identifiers: {', '.join(extra_problems)}")

    resource_ids = RESOURCE_MARKER_RE.findall(text)
    if not resource_ids:
        errors.append("no [resource:...] markers found")

    for resource_id in sorted(set(resource_ids)):
        if resource_id not in catalog_ids:
            errors.append(f"unknown catalog resource ID: {resource_id}")

    covered_sections = {section for section in MAIN_SECTIONS if section in text}
    missing_sections = sorted(MAIN_SECTIONS - covered_sections)
    if missing_sections:
        errors.append(
            "main README sections not referenced in problem index: "
            + ", ".join(missing_sections)
        )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--doc",
        type=Path,
        default=DEFAULT_DOC_PATH,
        help="path to integration-problems.md (default: docs/integration-problems.md)",
    )
    args = parser.parse_args(argv)

    if not args.doc.is_file():
        print(f"problem index not found: {args.doc}", file=sys.stderr)
        return 1

    catalog_ids = load_catalog_ids()
    errors = validate(args.doc, catalog_ids)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"problem index valid: {args.doc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
