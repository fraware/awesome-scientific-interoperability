#!/usr/bin/env python3
"""Export deterministic catalog dumps under dist/ for CI and release assets.

Read-only over catalog sources: never modifies README or catalog YAML and
performs no network I/O. Inclusion remains editorial (README/catalog); this
script only projects already-admitted records into downloadable shapes.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import date
from io import StringIO
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.catalog_model import (  # noqa: E402
    clear_caches,
    load_catalog_resources,
    load_implementations,
    load_stewards,
)
from query_catalog import sort_resources  # noqa: E402

CATALOG_INDEX_PATH = ROOT / "catalog" / "resources.yaml"
PROBLEMS_DOC_PATH = ROOT / "docs" / "integration-problems.md"
GUIDES_DIR = ROOT / "docs" / "decision-guides"
GUIDES_README_PATH = GUIDES_DIR / "README.md"
DEFAULT_OUT_DIR = ROOT / "dist"

PROBLEM_LINE_RE = re.compile(r"^\[problem:([a-z0-9-]+)\]\s*$", re.MULTILINE)
RESOURCE_MARKER_RE = re.compile(r"\[resource:([a-z0-9-]+)\]")
GUIDE_TABLE_ROW_RE = re.compile(
    r"^\|\s*\[([^\]]+)\]\(([^)]+\.md)\)\s*\|\s*(.+?)\s*\|\s*$",
    re.MULTILINE,
)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

ARTIFACT_NAMES = (
    "catalog.json",
    "catalog.csv",
    "relations.json",
    "catalog.jsonld",
    "problems.json",
    "guides-index.json",
)

CSV_COLUMNS = (
    "id",
    "name",
    "url",
    "section",
    "resource_kind",
    "interoperability_layers",
    "connects",
    "mechanism",
    "summary",
    "maturity",
    "evidence_types",
    "implementation_status",
    "conformance_status",
    "steward_id",
    "steward_name",
    "steward_type",
    "steward_url",
    "implementation_ids",
    "scientific_domains",
    "integration_functions",
    "infrastructure_contexts",
    "artifact_classes",
    "review_type",
    "boundary_note",
    "relations",
)


def load_catalog_index() -> dict[str, Any]:
    with CATALOG_INDEX_PATH.open(encoding="utf-8") as handle:
        index = yaml.safe_load(handle)
    if not isinstance(index, dict):
        raise ValueError("catalog index must be a mapping")
    return index


def steward_summary(steward_id: str | None, stewards: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    if not steward_id:
        return None
    steward = stewards.get(steward_id)
    if not steward:
        return {"id": steward_id, "name": None, "type": None, "url": None}
    return {
        "id": steward["id"],
        "name": steward["name"],
        "type": steward["type"],
        "url": steward["url"],
    }


def implementation_summary(impl: dict[str, Any]) -> dict[str, Any]:
    record = {
        "id": impl["id"],
        "name": impl["name"],
        "url": impl["url"],
        "relationship": impl["relationship"],
        "operator_steward_id": impl["operator_steward_id"],
    }
    if impl.get("supported_versions"):
        record["supported_versions"] = list(impl["supported_versions"])
    return record


def implementations_for_resource(
    resource_id: str,
    implementations: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    matched = [
        implementation_summary(impl)
        for impl in implementations.values()
        if impl.get("implements_resource_id") == resource_id
    ]
    return sorted(matched, key=lambda item: item["id"])


def join_resource(
    resource: dict[str, Any],
    *,
    stewards: dict[str, dict[str, Any]],
    implementations: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    relations = sorted(
        [
            {"type": item["type"], "resource_id": item["resource_id"]}
            for item in (resource.get("relations") or [])
        ],
        key=lambda item: (item["type"], item["resource_id"]),
    )
    steward_id = resource.get("steward_id")
    impls = implementations_for_resource(resource["id"], implementations)
    review = resource.get("review") or {}

    return {
        "id": resource["id"],
        "name": resource["name"],
        "url": resource["url"],
        "section": resource["section"],
        "resource_kind": resource["resource_kind"],
        "interoperability_layers": list(resource.get("interoperability_layers") or []),
        "connects": list(resource.get("connects") or []),
        "mechanism": resource["mechanism"],
        "summary": resource["summary"],
        "maturity": resource.get("maturity"),
        "evidence_types": list(resource.get("evidence_types") or []),
        "implementation_status": resource.get("implementation_status"),
        "conformance_status": resource.get("conformance_status"),
        "steward_id": steward_id,
        "steward": steward_summary(steward_id, stewards),
        "implementations": impls,
        "scientific_domains": list(resource.get("scientific_domains") or []),
        "integration_functions": list(resource.get("integration_functions") or []),
        "infrastructure_contexts": list(resource.get("infrastructure_contexts") or []),
        "artifact_classes": list(resource.get("artifact_classes") or []),
        "relations": relations,
        "review_type": review.get("review_type"),
        "boundary_note": resource.get("boundary_note"),
        "reviewed_on": resource.get("reviewed_on"),
        "review_due_on": resource.get("review_due_on"),
    }


def build_meta(
    index: dict[str, Any],
    *,
    generated_on: str,
    resource_count: int,
) -> dict[str, Any]:
    return {
        "catalog_version": index["catalog_version"],
        "catalog_reviewed_on": index["reviewed_on"],
        "export_generated_on": generated_on,
        "resource_count": resource_count,
        "north_star": index["north_star"],
    }


def build_catalog_payload(
    resources: list[dict[str, Any]],
    index: dict[str, Any],
    *,
    generated_on: str,
) -> dict[str, Any]:
    clear_caches()
    stewards = load_stewards()
    implementations = load_implementations()
    joined = [
        join_resource(resource, stewards=stewards, implementations=implementations)
        for resource in sort_resources(resources)
    ]
    return {
        "meta": build_meta(index, generated_on=generated_on, resource_count=len(joined)),
        "resources": joined,
    }


def build_relations_payload(
    resources: list[dict[str, Any]],
    index: dict[str, Any],
    *,
    generated_on: str,
) -> dict[str, Any]:
    edges: list[dict[str, str]] = []
    for resource in sort_resources(resources):
        for relation in resource.get("relations") or []:
            edges.append(
                {
                    "source": resource["id"],
                    "type": relation["type"],
                    "target": relation["resource_id"],
                }
            )
    edges.sort(key=lambda edge: (edge["source"], edge["type"], edge["target"]))
    return {
        "meta": build_meta(index, generated_on=generated_on, resource_count=len(resources)),
        "edges": edges,
    }


def build_jsonld_payload(
    catalog: dict[str, Any],
    relations: dict[str, Any],
) -> dict[str, Any]:
    return {
        "@context": {
            "asi": (
                "https://github.com/fraware/awesome-scientific-interoperability/"
                "blob/main/docs/catalog-model.md#"
            ),
            "schema": "https://schema.org/",
            "id": "@id",
            "name": "schema:name",
            "url": "schema:url",
            "section": "asi:section",
            "resource_kind": "asi:resourceKind",
            "interoperability_layers": "asi:interoperabilityLayer",
            "evidence_types": "asi:evidenceType",
            "steward": "asi:steward",
            "implementations": "asi:implementation",
            "relations": "asi:relation",
            "type": "asi:relationType",
            "resource_id": "asi:targetResource",
            "source": "asi:sourceResource",
            "target": "asi:targetResource",
            "edges": "asi:edge",
            "resources": "asi:resource",
        },
        "meta": catalog["meta"],
        "resources": catalog["resources"],
        "edges": relations["edges"],
    }


def join_list(values: list[Any] | None) -> str:
    return ";".join(str(item) for item in (values or []))


def build_catalog_csv(catalog: dict[str, Any]) -> str:
    buffer = StringIO()
    writer = csv.DictWriter(
        buffer,
        fieldnames=list(CSV_COLUMNS),
        lineterminator="\n",
        extrasaction="ignore",
    )
    writer.writeheader()
    for resource in catalog["resources"]:
        steward = resource.get("steward") or {}
        relations = resource.get("relations") or []
        writer.writerow(
            {
                "id": resource["id"],
                "name": resource["name"],
                "url": resource["url"],
                "section": resource["section"],
                "resource_kind": resource["resource_kind"],
                "interoperability_layers": join_list(resource.get("interoperability_layers")),
                "connects": join_list(resource.get("connects")),
                "mechanism": resource.get("mechanism") or "",
                "summary": resource.get("summary") or "",
                "maturity": resource.get("maturity") or "",
                "evidence_types": join_list(resource.get("evidence_types")),
                "implementation_status": resource.get("implementation_status") or "",
                "conformance_status": resource.get("conformance_status") or "",
                "steward_id": resource.get("steward_id") or "",
                "steward_name": steward.get("name") or "",
                "steward_type": steward.get("type") or "",
                "steward_url": steward.get("url") or "",
                "implementation_ids": join_list(
                    [item["id"] for item in resource.get("implementations") or []]
                ),
                "scientific_domains": join_list(resource.get("scientific_domains")),
                "integration_functions": join_list(resource.get("integration_functions")),
                "infrastructure_contexts": join_list(resource.get("infrastructure_contexts")),
                "artifact_classes": join_list(resource.get("artifact_classes")),
                "review_type": resource.get("review_type") or "",
                "boundary_note": resource.get("boundary_note") or "",
                "relations": join_list(
                    [f"{item['type']}->{item['resource_id']}" for item in relations]
                ),
            }
        )
    return buffer.getvalue()


def parse_problems(doc_path: Path = PROBLEMS_DOC_PATH) -> list[dict[str, Any]]:
    text = doc_path.read_text(encoding="utf-8")
    headings = list(HEADING_RE.finditer(text))
    problems: list[dict[str, Any]] = []

    for match in PROBLEM_LINE_RE.finditer(text):
        problem_id = match.group(1)
        title = None
        for heading in headings:
            if heading.start() < match.start():
                title = heading.group(1).strip()
            else:
                break
        if title is None:
            title = problem_id

        section_start = match.end()
        section_end = len(text)
        for heading in headings:
            if heading.start() > match.start():
                section_end = heading.start()
                break

        section_text = text[section_start:section_end]
        resource_ids = sorted(set(RESOURCE_MARKER_RE.findall(section_text)))
        problems.append(
            {
                "id": problem_id,
                "title": title,
                "resource_ids": resource_ids,
            }
        )

    problems.sort(key=lambda item: item["id"])
    return problems


def parse_guides(
    guides_dir: Path = GUIDES_DIR,
    readme_path: Path = GUIDES_README_PATH,
) -> list[dict[str, Any]]:
    table_rows: dict[str, dict[str, str]] = {}
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        for match in GUIDE_TABLE_ROW_RE.finditer(readme):
            title, filename, scope = match.group(1), match.group(2), match.group(3)
            slug = Path(filename).stem
            table_rows[slug] = {
                "title": title.strip(),
                "scope": scope.strip(),
                "filename": filename.strip(),
            }

    guides: list[dict[str, Any]] = []
    for path in sorted(guides_dir.glob("*.md")):
        if path.name.casefold() == "readme.md":
            continue
        slug = path.stem
        text = path.read_text(encoding="utf-8")
        first_heading = None
        for line in text.splitlines():
            if line.startswith("# "):
                first_heading = line[2:].strip()
                break
        table = table_rows.get(slug, {})
        guides.append(
            {
                "id": slug,
                "title": table.get("title") or first_heading or slug,
                "path": f"docs/decision-guides/{path.name}",
                "scope": table.get("scope") or "",
                "resource_ids": sorted(set(RESOURCE_MARKER_RE.findall(text))),
            }
        )

    guides.sort(key=lambda item: item["id"])
    return guides


def dumps_json(payload: Any) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def export_all(
    out_dir: Path,
    *,
    generated_on: str | None = None,
) -> dict[str, Path]:
    clear_caches()
    index = load_catalog_index()
    resources = load_catalog_resources(CATALOG_INDEX_PATH)
    generated = generated_on or date.today().isoformat()

    catalog = build_catalog_payload(resources, index, generated_on=generated)
    relations = build_relations_payload(resources, index, generated_on=generated)
    jsonld = build_jsonld_payload(catalog, relations)
    problems = {
        "meta": {
            "export_generated_on": generated,
            "source": "docs/integration-problems.md",
            "problem_count": None,
        },
        "problems": parse_problems(),
    }
    problems["meta"]["problem_count"] = len(problems["problems"])
    guides = {
        "meta": {
            "export_generated_on": generated,
            "source": "docs/decision-guides/",
            "guide_count": None,
        },
        "guides": parse_guides(),
    }
    guides["meta"]["guide_count"] = len(guides["guides"])

    out_dir.mkdir(parents=True, exist_ok=True)
    written = {
        "catalog.json": out_dir / "catalog.json",
        "catalog.csv": out_dir / "catalog.csv",
        "relations.json": out_dir / "relations.json",
        "catalog.jsonld": out_dir / "catalog.jsonld",
        "problems.json": out_dir / "problems.json",
        "guides-index.json": out_dir / "guides-index.json",
    }
    write_text(written["catalog.json"], dumps_json(catalog))
    write_text(written["catalog.csv"], build_catalog_csv(catalog))
    write_text(written["relations.json"], dumps_json(relations))
    write_text(written["catalog.jsonld"], dumps_json(jsonld))
    write_text(written["problems.json"], dumps_json(problems))
    write_text(written["guides-index.json"], dumps_json(guides))
    return written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Output directory (default: dist/)",
    )
    parser.add_argument(
        "--generated-on",
        help="Override export_generated_on date (YYYY-MM-DD) for deterministic tests",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.generated_on:
        try:
            date.fromisoformat(args.generated_on)
        except ValueError:
            print(f"ERROR: invalid --generated-on date: {args.generated_on!r}", file=sys.stderr)
            return 2

    written = export_all(args.out_dir, generated_on=args.generated_on)
    for name in ARTIFACT_NAMES:
        path = written[name]
        print(f"wrote {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
