#!/usr/bin/env python3
"""Query the structured catalog with conjunctive filters.

Read-only: never modifies catalog or README files and performs no network I/O.
Results are ordered by section then canonical name; no automatic ranking is applied.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "resources.yaml"

SECTION_ORDER = [
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
]

TOKEN_SPLIT_RE = re.compile(r"[^a-z0-9]+")


def load_resources() -> list[dict[str, Any]]:
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        index = yaml.safe_load(handle)

    resources: list[dict[str, Any]] = []
    for relative_path in index.get("resource_files", []):
        path = CATALOG_PATH.parent / relative_path
        with path.open(encoding="utf-8") as handle:
            shard = yaml.safe_load(handle)
        resources.extend(shard.get("resources", []))
    return resources


def normalize_tokens(text: str) -> set[str]:
    return {token for token in TOKEN_SPLIT_RE.split(text.casefold()) if token}


def connects_haystack(resource: dict[str, Any]) -> str:
    parts = list(resource.get("connects", []))
    parts.append(resource.get("mechanism", ""))
    parts.append(resource.get("summary", ""))
    return " ".join(str(part) for part in parts)


def matches_connects(resource: dict[str, Any], query: str) -> bool:
    query_tokens = normalize_tokens(query)
    if not query_tokens:
        return False
    haystack_tokens = normalize_tokens(connects_haystack(resource))
    return query_tokens.issubset(haystack_tokens)


def apply_filters(
    resources: list[dict[str, Any]],
    *,
    section: str | None,
    layer: str | None,
    domain: str | None,
    connects: str | None,
    evidence: str | None,
    resource_id: str | None,
) -> list[dict[str, Any]]:
    results = resources

    if section is not None:
        results = [resource for resource in results if resource.get("section") == section]
    if layer is not None:
        results = [
            resource
            for resource in results
            if layer in resource.get("interoperability_layers", [])
        ]
    if domain is not None:
        normalized_domain = domain.casefold()
        results = [
            resource
            for resource in results
            if normalized_domain in {item.casefold() for item in resource.get("domains", [])}
        ]
    if connects is not None:
        results = [resource for resource in results if matches_connects(resource, connects)]
    if evidence is not None:
        results = [
            resource
            for resource in results
            if evidence in resource.get("evidence_types", [])
        ]
    if resource_id is not None:
        results = [resource for resource in results if resource.get("id") == resource_id]

    return sort_resources(results)


def sort_resources(resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    section_rank = {name: index for index, name in enumerate(SECTION_ORDER)}

    def sort_key(resource: dict[str, Any]) -> tuple[int, str, str]:
        section = resource.get("section", "")
        return (section_rank.get(section, len(SECTION_ORDER)), section, resource.get("name", ""))

    return sorted(resources, key=sort_key)


def resource_record(resource: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": resource["id"],
        "name": resource["name"],
        "url": resource["url"],
        "section": resource["section"],
        "resource_type": resource["resource_type"],
        "interoperability_layers": list(resource.get("interoperability_layers", [])),
        "connects": list(resource.get("connects", [])),
        "mechanism": resource["mechanism"],
        "summary": resource["summary"],
        "evidence_types": list(resource.get("evidence_types", [])),
        "domains": list(resource.get("domains", [])),
        "alternatives": list(resource.get("alternatives", [])),
        "boundary_note": resource["boundary_note"],
    }


def format_json(resources: list[dict[str, Any]]) -> str:
    payload = [resource_record(resource) for resource in resources]
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def format_markdown(resources: list[dict[str, Any]]) -> str:
    if not resources:
        return "No catalog resources matched the query.\n"

    lines: list[str] = []
    current_section: str | None = None
    for resource in resources:
        section = resource.get("section", "")
        if section != current_section:
            current_section = section
            lines.append(f"## {section}")
            lines.append("")

        resource_id = resource["id"]
        lines.append(f"### {resource['name']} (`{resource_id}`)")
        lines.append("")
        lines.append(f"- **URL:** {resource['url']}")
        lines.append(f"- **Summary:** {resource['summary']}")
        lines.append(f"- **Mechanism:** {resource['mechanism']}")
        connects = ", ".join(resource.get("connects", []))
        lines.append(f"- **Connects:** {connects}")
        alternatives = resource.get("alternatives") or []
        if alternatives:
            lines.append(f"- **Alternatives:** {', '.join(alternatives)}")
        else:
            lines.append("- **Alternatives:** none recorded")
        lines.append(f"- **Boundary note:** {resource['boundary_note']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--section", help="Exact catalog section name")
    parser.add_argument(
        "--layer",
        choices=("Syntactic", "Semantic", "Operational", "Evidentiary", "Organizational"),
        help="Interoperability layer",
    )
    parser.add_argument("--domain", help="Domain tag (case-insensitive)")
    parser.add_argument(
        "--connects",
        help="Token match over connects, mechanism, and summary (all tokens required)",
    )
    parser.add_argument(
        "--evidence",
        help="Evidence type enum value (for example conformance-suite)",
    )
    parser.add_argument("--id", dest="resource_id", help="Exact resource identifier")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.evidence and args.evidence not in {
        "normative-specification",
        "reference-implementation",
        "independent-implementation",
        "institutional-adoption",
        "conformance-suite",
        "public-validator",
        "interoperability-demonstration",
    }:
        print(f"ERROR: unknown evidence type: {args.evidence!r}", file=sys.stderr)
        return 2

    if args.section and args.section not in SECTION_ORDER:
        print(f"ERROR: unknown section: {args.section!r}", file=sys.stderr)
        return 2

    resources = load_resources()
    matched = apply_filters(
        resources,
        section=args.section,
        layer=args.layer,
        domain=args.domain,
        connects=args.connects,
        evidence=args.evidence,
        resource_id=args.resource_id,
    )

    if args.format == "json":
        sys.stdout.write(format_json(matched))
    else:
        sys.stdout.write(format_markdown(matched))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
