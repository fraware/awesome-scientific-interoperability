"""Shared catalog model loaders for v2.1 provenance registries."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
TAXONOMY_PATH = ROOT / "config" / "catalog-taxonomy.yaml"
REFERENCES_PATH = ROOT / "catalog" / "references.yaml"
STEWARDS_PATH = ROOT / "catalog" / "stewards.yaml"
CATALOG_INDEX_PATH = ROOT / "catalog" / "resources.yaml"


def _load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


@lru_cache(maxsize=1)
def load_taxonomy() -> dict[str, Any]:
    payload = _load_yaml(TAXONOMY_PATH)
    if not isinstance(payload, dict):
        raise ValueError(f"taxonomy must be a mapping: {TAXONOMY_PATH}")
    return payload


@lru_cache(maxsize=1)
def load_references() -> dict[str, dict[str, Any]]:
    payload = _load_yaml(REFERENCES_PATH)
    items = payload.get("references", []) if isinstance(payload, dict) else []
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        ref_id = item.get("id")
        if isinstance(ref_id, str):
            result[ref_id] = item
    return result


@lru_cache(maxsize=1)
def load_stewards() -> dict[str, dict[str, Any]]:
    payload = _load_yaml(STEWARDS_PATH)
    items = payload.get("stewards", []) if isinstance(payload, dict) else []
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        steward_id = item.get("id")
        if isinstance(steward_id, str):
            result[steward_id] = item
    return result


def resource_kind_ids() -> set[str]:
    return {item["id"] for item in load_taxonomy()["resource_kinds"]}


def domain_ids() -> set[str]:
    return set(load_taxonomy()["domains"])


def claim_role_ids() -> set[str]:
    return set(load_taxonomy()["claim_roles"])


def reference_type_ids() -> set[str]:
    return set(load_taxonomy()["reference_types"])


def conformance_artifact_types() -> set[str]:
    return set(load_taxonomy()["conformance_artifact_types"])


def clear_caches() -> None:
    load_taxonomy.cache_clear()
    load_references.cache_clear()
    load_stewards.cache_clear()


def load_catalog_resources(index_path: Path = CATALOG_INDEX_PATH) -> list[dict[str, Any]]:
    index = _load_yaml(index_path)
    resources: list[dict[str, Any]] = []
    for relative_path in index.get("resource_files", []):
        path = index_path.parent / relative_path
        shard = _load_yaml(path)
        resources.extend(shard.get("resources", []))
    return resources
