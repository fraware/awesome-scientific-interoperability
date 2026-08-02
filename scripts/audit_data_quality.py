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
    load_implementation_list,
    load_references,
    load_stewards,
)
from lib.independence import independent_operator_stewards  # noqa: E402
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
    implementations = load_implementation_list()

    mi_queue: list[dict[str, Any]] = []
    dt_queue: list[dict[str, Any]] = []
    for resource in sorted(resources, key=lambda item: item["id"]):
        if resource.get("implementation_status") == "multiple-independent":
            operators = independent_operator_stewards(resource, implementations)
            typed_refs = implementation_evidence_count(resource, references)
            if len(operators) < 2:
                mi_queue.append(
                    {
                        "id": resource["id"],
                        "section": resource["section"],
                        "implementation_status": resource["implementation_status"],
                        "independent_operators": operators,
                        "direct_implementation_refs": typed_refs,
                        "reason": (
                            "fewer than two distinct independent-implementation operators "
                            "outside the resource steward"
                        ),
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
            "implementations": len(implementations),
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


def section_counts(queue: list[dict[str, Any]]) -> list[tuple[str, int]]:
    tallies: dict[str, int] = {}
    for item in queue:
        section = item.get("section") or "—"
        tallies[section] = tallies.get(section, 0) + 1
    return sorted(tallies.items(), key=lambda pair: (-pair[1], pair[0]))


def baseline_snapshot(report: dict[str, Any]) -> dict[str, Any]:
    """Machine-checkable subset compared by --check-baseline / CI."""
    return {
        "as_of": report["as_of"],
        "catalog_version": report.get("catalog_version"),
        "counts": {
            "resources": report["counts"]["resources"],
            "references": report["counts"]["references"],
            "stewards": report["counts"]["stewards"],
            "implementations": report["counts"].get("implementations", 0),
            "integrity_errors": report["counts"]["integrity_errors"],
            "multiple_independent_queue": report["counts"]["multiple_independent_queue"],
            "documented_tests_queue": report["counts"]["documented_tests_queue"],
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
        f"- Implementations: {counts.get('implementations', 0)}",
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
            operators = item.get("independent_operators") or []
            lines.append(
                f"- `{item['id']}` ({item['section']}): {len(operators)} independent operators "
                f"{operators} — {item['reason']}"
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


def _render_section_table(queue: list[dict[str, Any]]) -> list[str]:
    lines = ["| Section | Count |", "|---|---:|"]
    rows = section_counts(queue)
    if not rows:
        lines.append("| — | 0 |")
    else:
        for section, count in rows:
            lines.append(f"| {section} | {count} |")
    return lines


def render_baseline_markdown(report: dict[str, Any]) -> str:
    """Human-readable checked-in baseline; counts must match baseline_snapshot()."""
    counts = report["counts"]
    version = report.get("catalog_version") or "unknown"
    as_of = report["as_of"]
    integrity_ok = counts["integrity_errors"] == 0
    lines = [
        f"# Data quality baseline (catalog v{version})",
        "",
        f"**As of:** {as_of}",
        f"**Generated by:** `python scripts/audit_data_quality.py --as-of {as_of} --write-baseline docs/data-quality-baseline.json`",
        "",
        "## Integrity",
        "",
        "| Check | Result |",
        "|---|---|",
        f"| Catalog resources | {counts['resources']} |",
        f"| Unresolved integrity errors | {counts['integrity_errors']} |",
        f"| Registry sizes | {counts['references']} references, {counts['stewards']} stewards, {counts.get('implementations', 0)} implementations |",
        "",
    ]
    if integrity_ok:
        lines.append(
            "Blocking integrity is green. Remaining work is evidence depth semantics, not structural validity."
        )
    else:
        lines.append(
            "Blocking integrity is red. Fix integrity errors before treating queue counts as authoritative."
        )
    lines.extend(
        [
            "",
            "## Evidence-depth queues",
            "",
            "| Queue | Count | Disposition rule |",
            "|---|---:|---|",
            f"| Unsupported `multiple-independent` | {counts['multiple_independent_queue']} | Enrich with ≥2 distinct independent-implementation operators outside the resource steward, or downgrade status |",
            f"| Unsupported `documented-tests` | {counts['documented_tests_queue']} | Enrich with a direct validator/suite/interop-result ref, or downgrade status |",
            "",
            "Exact resource IDs are exported by:",
            "",
            "```bash",
            f"python scripts/audit_data_quality.py --as-of {as_of} --json-report data-quality-audit.json",
            "```",
            "",
            "### Queue concentration by section",
            "",
            "**Multiple-independent**",
            "",
        ]
    )
    lines.extend(_render_section_table(report["queues"]["multiple_independent"]))
    lines.extend(["", "**Documented-tests**", ""])
    lines.extend(_render_section_table(report["queues"]["documented_tests"]))
    lines.extend(
        [
            "",
            "## Machine snapshot",
            "",
            "CI compares `docs/data-quality-baseline.json` to a fresh `build_report()` via",
            "`python scripts/audit_data_quality.py --as-of <date> --check-baseline docs/data-quality-baseline.json`.",
            "Do not hand-edit counts in this markdown or the JSON sidecar; regenerate both with `--write-baseline`.",
            "",
            "## Refresh protocol",
            "",
            "After each evidence or model batch merges:",
            "",
            "1. Re-run the audit with the batch review date.",
            "2. Regenerate the baseline pair:",
            "",
            "```bash",
            f"python scripts/audit_data_quality.py --as-of {as_of} --write-baseline docs/data-quality-baseline.json",
            "```",
            "",
            "3. Keep Quality CI artifacts for the JSON/Markdown audit reports.",
            "",
            "## Post-queue hardening (tracked)",
            "",
            "After both queues remain at zero for a maintenance quarter:",
            "",
            "1. Consider promoting selected depth rules from audit warning to validator fail-closed checks, only with fixtures and an explicit decision record.",
            "2. Keep any domain hierarchy work as a separate taxonomy PR.",
            "3. Continue the quarterly full-scope offline reference audit cadence in [maintenance-protocol.md](maintenance-protocol.md).",
            "",
        ]
    )
    return "\n".join(lines)


def write_baseline(report: dict[str, Any], json_path: Path, markdown_path: Path | None = None) -> None:
    snapshot = baseline_snapshot(report)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    md_path = markdown_path or json_path.with_suffix(".md")
    md_path.write_text(render_baseline_markdown(report), encoding="utf-8")


def check_baseline(report: dict[str, Any], baseline_path: Path) -> list[str]:
    if not baseline_path.is_file():
        return [f"baseline file missing: {baseline_path}"]
    try:
        checked_in = json.loads(baseline_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"baseline JSON invalid: {exc}"]
    live = baseline_snapshot(report)
    mismatches: list[str] = []
    for key in ("as_of", "catalog_version"):
        if checked_in.get(key) != live.get(key):
            mismatches.append(f"{key}: baseline={checked_in.get(key)!r} live={live.get(key)!r}")
    baseline_counts = checked_in.get("counts") or {}
    live_counts = live["counts"]
    for key, live_value in live_counts.items():
        baseline_value = baseline_counts.get(key)
        if baseline_value != live_value:
            mismatches.append(f"counts.{key}: baseline={baseline_value!r} live={live_value!r}")
    return mismatches


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
    parser.add_argument(
        "--write-baseline",
        type=Path,
        help="Write machine snapshot JSON and matching markdown (same stem .md)",
    )
    parser.add_argument(
        "--check-baseline",
        type=Path,
        help="Fail if checked-in baseline JSON diverges from live build_report()",
    )
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
    if args.write_baseline:
        write_baseline(report, args.write_baseline)
        print(f"Wrote baseline snapshot: {args.write_baseline}")
        print(f"Wrote baseline markdown: {args.write_baseline.with_suffix('.md')}")

    if args.check_baseline:
        mismatches = check_baseline(report, args.check_baseline)
        if mismatches:
            print("ERROR: data-quality baseline drift:", file=sys.stderr)
            for item in mismatches:
                print(f"  - {item}", file=sys.stderr)
            print(
                "Regenerate with: python scripts/audit_data_quality.py "
                f"--as-of {args.as_of} --write-baseline {args.check_baseline}",
                file=sys.stderr,
            )
            return 1

    has_errors = bool(report["integrity_errors"])
    has_warnings = bool(report["warnings"])
    if args.fail_on == "error" and has_errors:
        return 1
    if args.fail_on == "warning" and (has_errors or has_warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
