#!/usr/bin/env python3
"""Deterministic data-quality audit for catalog provenance depth.

Blocking integrity errors exit non-zero under --fail-on error.
Evidence-depth queues (multiple-independent / documented-tests) are warnings by default.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.catalog_model import (  # noqa: E402
    clear_caches,
    conformance_artifact_types,
    load_catalog_resources,
    load_references,
    load_stewards,
)
from validate_catalog import validate as validate_catalog_live  # noqa: E402

IMPLEMENTATION_REF_TYPES = frozenset(
    {
        "implementation-repository",
        "adoption-evidence",
        "registry-record",
        "interoperability-result",
    }
)
IMPLEMENTATION_ROLES = frozenset({"implementation", "adoption", "interoperability-testing"})


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def implementation_evidence_count(resource: dict[str, Any], references: dict[str, dict[str, Any]]) -> int:
    count = 0
    seen: set[str] = set()
    for item in resource.get("source_refs") or []:
        ref_id = item.get("ref_id")
        role = item.get("role")
        ref = references.get(ref_id or "")
        if not ref:
            continue
        if role in IMPLEMENTATION_ROLES and ref.get("type") in IMPLEMENTATION_REF_TYPES:
            if ref_id not in seen:
                seen.add(ref_id)
                count += 1
    return count


def has_conformance_artifact(resource: dict[str, Any], references: dict[str, dict[str, Any]]) -> bool:
    artifacts = conformance_artifact_types()
    for item in resource.get("source_refs") or []:
        ref = references.get(item.get("ref_id") or "")
        if not ref:
            continue
        if (
            ref.get("type") in artifacts
            and item.get("role") in {"conformance", "interoperability-testing"}
        ):
            return True
    return False


def build_report(*, as_of: date) -> dict[str, Any]:
    clear_caches()
    integrity_errors = validate_catalog_live(as_of=as_of)
    resources = load_catalog_resources()
    references = load_references()
    stewards = load_stewards()

    mi_queue: list[dict[str, Any]] = []
    dt_queue: list[dict[str, Any]] = []
    for resource in sorted(resources, key=lambda item: item["id"]):
        if resource.get("implementation_status") == "multiple-independent":
            count = implementation_evidence_count(resource, references)
            if count < 2:
                mi_queue.append(
                    {
                        "id": resource["id"],
                        "section": resource["section"],
                        "implementation_status": resource["implementation_status"],
                        "direct_implementation_refs": count,
                        "reason": "fewer than two direct implementation/adoption/registry/interop references",
                    }
                )
        if resource.get("conformance_status") == "documented-tests":
            if not has_conformance_artifact(resource, references):
                dt_queue.append(
                    {
                        "id": resource["id"],
                        "section": resource["section"],
                        "conformance_status": resource["conformance_status"],
                        "reason": "documented-tests without a direct conformance artifact reference",
                    }
                )

    warnings = [
        f"unsupported multiple-independent: {item['id']}" for item in mi_queue
    ] + [f"unsupported documented-tests: {item['id']}" for item in dt_queue]

    return {
        "as_of": as_of.isoformat(),
        "catalog_version": yaml.safe_load(
            (ROOT / "catalog" / "resources.yaml").read_text(encoding="utf-8")
        ).get("catalog_version"),
        "counts": {
            "resources": len(resources),
            "references": len(references),
            "stewards": len(stewards),
            "integrity_errors": len(integrity_errors),
            "multiple_independent_queue": len(mi_queue),
            "documented_tests_queue": len(dt_queue),
        },
        "integrity_errors": integrity_errors,
        "warnings": warnings,
        "queues": {
            "multiple_independent": mi_queue,
            "documented_tests": dt_queue,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    counts = report["counts"]
    lines = [
        "# Data quality audit",
        "",
        f"As of: `{report['as_of']}`",
        f"Catalog version: `{report.get('catalog_version')}`",
        "",
        "## Counts",
        "",
        f"- Resources: {counts['resources']}",
        f"- References: {counts['references']}",
        f"- Stewards: {counts['stewards']}",
        f"- Integrity errors: {counts['integrity_errors']}",
        f"- Unsupported `multiple-independent` queue: {counts['multiple_independent_queue']}",
        f"- Unsupported `documented-tests` queue: {counts['documented_tests_queue']}",
        "",
        "## Integrity errors",
        "",
    ]
    if report["integrity_errors"]:
        for error in report["integrity_errors"]:
            lines.append(f"- {error}")
    else:
        lines.append("- none")
    lines.extend(["", "## Multiple-independent queue", ""])
    if report["queues"]["multiple_independent"]:
        for item in report["queues"]["multiple_independent"]:
            lines.append(
                f"- `{item['id']}` ({item['section']}): {item['direct_implementation_refs']} direct refs — {item['reason']}"
            )
    else:
        lines.append("- none")
    lines.extend(["", "## Documented-tests queue", ""])
    if report["queues"]["documented_tests"]:
        for item in report["queues"]["documented_tests"]:
            lines.append(f"- `{item['id']}` ({item['section']}): {item['reason']}")
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", required=True, help="Reference date YYYY-MM-DD")
    parser.add_argument(
        "--fail-on",
        choices=("error", "warning", "never"),
        default="error",
        help="Exit non-zero on integrity errors (error), also on queues (warning), or never",
    )
    parser.add_argument("--json-report", type=Path, help="Write machine-readable queue export")
    parser.add_argument("--markdown-report", type=Path, help="Write human-readable audit report")
    args = parser.parse_args(argv)

    try:
        as_of = parse_date(args.as_of)
    except ValueError as exc:
        print(f"ERROR: invalid --as-of date: {exc}", file=sys.stderr)
        return 1

    report = build_report(as_of=as_of)
    markdown = render_markdown(report)
    print(markdown)

    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.markdown_report:
        args.markdown_report.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_report.write_text(markdown, encoding="utf-8")

    has_errors = bool(report["integrity_errors"])
    has_warnings = bool(report["warnings"])
    if args.fail_on == "error" and has_errors:
        return 1
    if args.fail_on == "warning" and (has_errors or has_warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
