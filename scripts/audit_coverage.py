#!/usr/bin/env python3
"""Measure catalog coverage and concentration without automating editorial decisions."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "resources.yaml"
POLICY_PATH = ROOT / "config" / "coverage-policy.yaml"

EVIDENCE_REQUIRING_SOURCE = frozenset(
    {
        "conformance-suite",
        "public-validator",
        "reference-implementation",
        "independent-implementation",
    }
)
CONFORMANCE_REQUIRING_SOURCE = frozenset({"public-suite", "public-validator"})


@dataclass
class Warning:
    code: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class IntegrityFailure:
    code: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def load_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"coverage policy must be a mapping: {path}")
    required = {"version", "thresholds", "general_purpose_substrate_ids", "standard_families"}
    missing = sorted(required - set(payload))
    if missing:
        raise ValueError(f"coverage policy missing fields: {missing}")
    return payload


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


def count_by(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items(), key=lambda item: (-item[1], item[0])))


def domains_per_entry(resources: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(len(resource.get("domains", [])) for resource in resources)
    return {str(key): value for key, value in sorted(counts.items())}


def entries_per_domain(resources: list[dict[str, Any]]) -> dict[str, int]:
    domain_counts: Counter[str] = Counter()
    for resource in resources:
        for domain in resource.get("domains", []):
            domain_counts[str(domain)] += 1
    return dict(sorted(domain_counts.items(), key=lambda item: (-item[1], item[0])))


def flatten_values(resources: list[dict[str, Any]], field_name: str) -> dict[str, int]:
    values: list[str] = []
    for resource in resources:
        payload = resource.get(field_name)
        if isinstance(payload, list):
            values.extend(str(item) for item in payload)
        elif payload is not None:
            values.append(str(payload))
    return count_by(values)


def stewardship_types(resources: list[dict[str, Any]]) -> dict[str, int]:
    stewards: dict[str, dict[str, Any]] = {}
    stewards_path = ROOT / "catalog" / "stewards.yaml"
    if stewards_path.exists():
        payload = yaml.safe_load(stewards_path.read_text(encoding="utf-8")) or {}
        for item in payload.get("stewards", []):
            if item.get("id"):
                stewards[item["id"]] = item
    values: list[str] = []
    for resource in resources:
        if resource.get("steward_type"):
            values.append(str(resource["steward_type"]))
            continue
        if resource.get("stewardship", {}).get("type"):
            values.append(str(resource["stewardship"]["type"]))
            continue
        steward_id = resource.get("steward_id")
        if steward_id in stewards:
            values.append(str(stewards[steward_id].get("type", "unknown")))
        else:
            values.append("unknown")
    return count_by(values)


def review_schedule(resources: list[dict[str, Any]], *, as_of: date) -> dict[str, Any]:
    overdue = [
        {
            "review_due_on": resource["review_due_on"],
            "id": resource["id"],
            "name": resource["name"],
            "section": resource["section"],
        }
        for resource in resources
        if parse_date(resource["review_due_on"]) < as_of
    ]
    upcoming = [
        {
            "review_due_on": resource["review_due_on"],
            "id": resource["id"],
            "name": resource["name"],
            "section": resource["section"],
        }
        for resource in sorted(resources, key=lambda item: (item["review_due_on"], item["id"]))
        if parse_date(resource["review_due_on"]) >= as_of
    ]
    return {
        "reviewed_on": count_by(resource["reviewed_on"] for resource in resources),
        "review_due_on_values": sorted({resource["review_due_on"] for resource in resources}),
        "upcoming_deadlines": upcoming[:20],
        "overdue_count": len(overdue),
        "overdue_entries": overdue,
    }


def implementations_per_family(
    resources: list[dict[str, Any]], policy: dict[str, Any]
) -> dict[str, Any]:
    by_id = {resource["id"]: resource for resource in resources}
    implementation_kinds = set(policy.get("implementation_resource_kinds", []))
    if not implementation_kinds:
        # Backward-compatible alias used by older fixture policies.
        implementation_kinds = set(policy.get("implementation_resource_types", []))
    families: dict[str, Any] = {}
    for family_name, member_ids in sorted(policy.get("standard_families", {}).items()):
        members: list[str] = []
        implementations: list[dict[str, str]] = []
        for member_id in member_ids:
            resource = by_id.get(member_id)
            if resource is None:
                continue
            members.append(member_id)
            kind = resource.get("resource_kind") or resource.get("resource_type")
            if kind in implementation_kinds:
                implementations.append(
                    {
                        "id": member_id,
                        "name": resource["name"],
                        "resource_kind": str(kind),
                    }
                )
        families[family_name] = {
            "member_count": len(members),
            "member_ids": members,
            "implementation_count": len(implementations),
            "implementations": implementations,
            "unknown_member_ids": sorted(set(member_ids) - set(members)),
        }
    return families


def substrate_metrics(resources: list[dict[str, Any]], policy: dict[str, Any]) -> dict[str, Any]:
    substrate_ids = set(policy.get("general_purpose_substrate_ids", []))
    by_id = {resource["id"] for resource in resources}
    present = sorted(substrate_ids & by_id)
    total = len(resources)
    share = len(present) / total if total else 0.0
    return {
        "configured_substrate_ids": sorted(substrate_ids),
        "present_substrate_ids": present,
        "missing_configured_ids": sorted(substrate_ids - by_id),
        "count": len(present),
        "total_entries": total,
        "share": round(share, 4),
        "share_percent": round(share * 100, 2),
    }


def domain_concentration(
    resources: list[dict[str, Any]], *, exclude_domains: frozenset[str]
) -> dict[str, Any]:
    total = len(resources)
    counts = entries_per_domain(resources)
    scientific_counts = {
        domain: count for domain, count in counts.items() if domain not in exclude_domains
    }
    top_domain = max(scientific_counts.items(), key=lambda item: item[1], default=(None, 0))
    top_share = top_domain[1] / total if total and top_domain[0] else 0.0
    return {
        "entries_per_domain": counts,
        "scientific_domain_counts": scientific_counts,
        "cross_domain_tagged_entries": counts.get("cross-domain", 0),
        "largest_scientific_domain": top_domain[0],
        "largest_scientific_domain_count": top_domain[1],
        "largest_scientific_domain_share": round(top_share, 4),
        "largest_scientific_domain_share_percent": round(top_share * 100, 2),
    }


def evidence_without_source(resources: list[dict[str, Any]]) -> list[dict[str, str]]:
    flagged: list[dict[str, str]] = []
    for resource in resources:
        evidence_types = set(resource.get("evidence_types", []))
        source_refs = resource.get("source_refs") or resource.get("source_urls") or []
        conformance = resource.get("conformance_status")
        needs_source = bool(evidence_types & EVIDENCE_REQUIRING_SOURCE) or (
            conformance in CONFORMANCE_REQUIRING_SOURCE
        )
        if needs_source and not source_refs:
            flagged.append(
                {
                    "id": resource["id"],
                    "name": resource["name"],
                    "section": resource["section"],
                }
            )
    return flagged


def isolated_entries(resources: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {"id": resource["id"], "name": resource["name"], "section": resource["section"]}
        for resource in resources
        if not resource.get("relations")
    ]


def check_integrity(
    resources: list[dict[str, Any]], policy: dict[str, Any], *, as_of: date
) -> list[IntegrityFailure]:
    failures: list[IntegrityFailure] = []
    if not resources:
        return [
            IntegrityFailure(
                code="empty-catalog",
                message="catalog contains no main-list resources",
            )
        ]

    known_ids = {resource["id"] for resource in resources}
    for family_name, member_ids in policy.get("standard_families", {}).items():
        unknown = sorted(set(member_ids) - known_ids)
        if unknown:
            failures.append(
                IntegrityFailure(
                    code="unknown-standard-family-member",
                    message=f"standard family {family_name!r} references unknown catalog IDs",
                    details={"unknown_ids": unknown, "family": family_name},
                )
            )

    unknown_substrates = sorted(set(policy.get("general_purpose_substrate_ids", [])) - known_ids)
    if unknown_substrates:
        failures.append(
            IntegrityFailure(
                code="unknown-substrate-id",
                message="coverage policy lists substrate IDs that are not in the catalog",
                details={"unknown_ids": unknown_substrates},
            )
        )

    for resource in resources:
        resource_id = resource["id"]
        try:
            reviewed_on = parse_date(resource["reviewed_on"])
            review_due_on = parse_date(resource["review_due_on"])
        except (KeyError, ValueError, TypeError) as exc:
            failures.append(
                IntegrityFailure(
                    code="invalid-review-date",
                    message=f"resource {resource_id!r} has invalid review dates",
                    details={"error": str(exc), "id": resource_id},
                )
            )
            continue
        if review_due_on <= reviewed_on:
            failures.append(
                IntegrityFailure(
                    code="review-window-invalid",
                    message=f"resource {resource_id!r} has review_due_on on or before reviewed_on",
                    details={
                        "id": resource_id,
                        "reviewed_on": resource["reviewed_on"],
                        "review_due_on": resource["review_due_on"],
                    },
                )
            )

    if not failures:
        _ = review_schedule(resources, as_of=as_of)
    return failures


def build_warnings(
    resources: list[dict[str, Any]], policy: dict[str, Any], metrics: dict[str, Any]
) -> list[Warning]:
    warnings: list[Warning] = []
    thresholds = policy["thresholds"]
    total = len(resources)

    for section, count in metrics["entries_per_section"].items():
        if count < thresholds["min_entries_per_section"]:
            warnings.append(
                Warning(
                    code="section-underrepresented",
                    message=(
                        f"section {section!r} has {count} entries "
                        f"(threshold {thresholds['min_entries_per_section']})"
                    ),
                    details={"section": section, "count": count},
                )
            )

    domain_info = metrics["domain_concentration"]
    if domain_info["largest_scientific_domain_share"] > thresholds["max_single_domain_share"]:
        warnings.append(
            Warning(
                code="domain-concentration",
                message=(
                    f"domain {domain_info['largest_scientific_domain']!r} appears on "
                    f"{domain_info['largest_scientific_domain_count']} of {total} entries "
                    f"({domain_info['largest_scientific_domain_share_percent']}%)"
                ),
                details=domain_info,
            )
        )

    substrate = metrics["general_purpose_substrates"]
    if substrate["share"] > thresholds["max_general_purpose_substrate_share"]:
        warnings.append(
            Warning(
                code="substrate-concentration",
                message=(
                    f"general-purpose substrates account for {substrate['count']} of {total} "
                    f"entries ({substrate['share_percent']}%)"
                ),
                details=substrate,
            )
        )

    for family_name, family_info in metrics["implementations_per_family"].items():
        if family_info["implementation_count"] > thresholds["max_implementations_per_family"]:
            warnings.append(
                Warning(
                    code="implementation-family-concentration",
                    message=(
                        f"standard family {family_name!r} has "
                        f"{family_info['implementation_count']} implementation entries "
                        f"(threshold {thresholds['max_implementations_per_family']})"
                    ),
                    details={"family": family_name, **family_info},
                )
            )

    isolated = metrics["isolated_entries"]
    if isolated:
        warnings.append(
            Warning(
                code="isolated-entries",
                message=(
                    f"{len(isolated)} entries have no typed relations"
                ),
                details={"entries": isolated},
            )
        )

    evidence_gaps = metrics["evidence_without_source"]
    if evidence_gaps:
        warnings.append(
            Warning(
                code="evidence-without-source",
                message=(
                    f"{len(evidence_gaps)} entries claim implementation or conformance "
                    "evidence but record no source_refs"
                ),
                details={"entries": evidence_gaps},
            )
        )

    return warnings


def compute_metrics(
    resources: list[dict[str, Any]], policy: dict[str, Any], *, as_of: date
) -> dict[str, Any]:
    return {
        "generated_on": as_of.isoformat(),
        "total_entries": len(resources),
        "entries_per_section": count_by(resource["section"] for resource in resources),
        "domains_per_entry": domains_per_entry(resources),
        "entries_per_domain": entries_per_domain(resources),
        "domain_concentration": domain_concentration(
            resources, exclude_domains=frozenset({"cross-domain"})
        ),
        "interoperability_layers": flatten_values(resources, "interoperability_layers"),
        "resource_kinds": count_by(
            resource.get("resource_kind") or resource.get("resource_type") for resource in resources
        ),
        "maturity_states": count_by(resource["maturity"] for resource in resources),
        "evidence_types": flatten_values(resources, "evidence_types"),
        "implementation_status": count_by(
            resource["implementation_status"] for resource in resources
        ),
        "conformance_status": count_by(resource["conformance_status"] for resource in resources),
        "stewardship_types": stewardship_types(resources),
        "review_schedule": review_schedule(resources, as_of=as_of),
        "implementations_per_family": implementations_per_family(resources, policy),
        "general_purpose_substrates": substrate_metrics(resources, policy),
        "isolated_entries": isolated_entries(resources),
        "evidence_without_source": evidence_without_source(resources),
    }


def format_markdown(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    lines = [
        "# Coverage Audit Report",
        "",
        f"**Generated on:** {metrics['generated_on']}",
        f"**Total main-list entries:** {metrics['total_entries']}",
        "",
        "This report measures corpus balance and editorial concentration. "
        "It does not assign quality scores or recommend inclusion or exclusion.",
        "",
        "## Concentration and gap warnings",
        "",
    ]
    if report["warnings"]:
        for warning in report["warnings"]:
            lines.append(f"- **{warning['code']}:** {warning['message']}")
    else:
        lines.append("- None")
    lines.extend(["", "## Data-integrity failures", ""])
    if report["integrity_failures"]:
        for failure in report["integrity_failures"]:
            lines.append(f"- **{failure['code']}:** {failure['message']}")
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def build_report(*, as_of: date, policy_path: Path = POLICY_PATH) -> dict[str, Any]:
    policy = load_policy(policy_path)
    resources = load_resources()
    integrity_failures = check_integrity(resources, policy, as_of=as_of)
    metrics = compute_metrics(resources, policy, as_of=as_of)
    warnings = [] if integrity_failures else build_warnings(resources, policy, metrics)
    return {
        "metrics": metrics,
        "warnings": [
            {"code": warning.code, "message": warning.message, "details": warning.details}
            for warning in warnings
        ],
        "integrity_failures": [
            {
                "code": failure.code,
                "message": failure.message,
                "details": failure.details,
            }
            for failure in integrity_failures
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default=date.today().isoformat())
    parser.add_argument("--json-report", type=Path)
    parser.add_argument("--markdown-report", type=Path)
    parser.add_argument("--policy", type=Path, default=POLICY_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        as_of = parse_date(args.as_of)
    except ValueError:
        print(f"ERROR: invalid --as-of date: {args.as_of!r}", file=sys.stderr)
        return 2

    try:
        report = build_report(as_of=as_of, policy_path=args.policy)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json_report:
        args.json_report.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    if args.markdown_report:
        args.markdown_report.write_text(format_markdown(report), encoding="utf-8")

    for warning in report["warnings"]:
        print(f"WARNING: {warning['message']}", file=sys.stderr)

    if report["integrity_failures"]:
        for failure in report["integrity_failures"]:
            print(f"ERROR: {failure['message']}", file=sys.stderr)
        return 1

    if not args.json_report and not args.markdown_report:
        sys.stdout.write(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
