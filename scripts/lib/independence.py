"""Shared independence helpers for catalog implementations registry."""

from __future__ import annotations

from typing import Any


INDEPENDENT_RELATIONSHIP = "independent-implementation"


def independent_operator_stewards(
    resource: dict[str, Any],
    implementations: list[dict[str, Any]],
) -> list[str]:
    """Return distinct independent operator steward IDs that count toward MI."""
    resource_id = resource.get("id")
    resource_steward = resource.get("steward_id")
    operators: list[str] = []
    seen: set[str] = set()
    for item in implementations:
        if item.get("implements_resource_id") != resource_id:
            continue
        if item.get("relationship") != INDEPENDENT_RELATIONSHIP:
            continue
        operator = item.get("operator_steward_id")
        if not isinstance(operator, str) or not operator:
            continue
        if operator == resource_steward and not item.get("multi_org_steward_exception"):
            continue
        if operator in seen:
            continue
        seen.add(operator)
        operators.append(operator)
    return operators


def multiple_independent_satisfied(
    resource: dict[str, Any],
    implementations: list[dict[str, Any]],
) -> bool:
    return len(independent_operator_stewards(resource, implementations)) >= 2
