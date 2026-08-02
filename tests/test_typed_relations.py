"""Typed relation validation coverage (PR #40)."""

from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

validate_spec = importlib.util.spec_from_file_location(
    "validate_catalog", SCRIPTS / "validate_catalog.py"
)
validate_module = importlib.util.module_from_spec(validate_spec)
assert validate_spec and validate_spec.loader
validate_spec.loader.exec_module(validate_module)


class TypedRelationsTests(unittest.TestCase):
    def test_unknown_relation_type_fails(self) -> None:
        catalog, schema, _ = validate_module.load()
        resource = copy.deepcopy(catalog["resources"][0])
        resource["relations"] = [{"type": "not-a-relation", "resource_id": "bagit"}]
        catalog["resources"] = [resource]
        errors = validate_module.validate_catalog(catalog, schema, as_of=date(2026, 8, 1))
        self.assertTrue(any("unknown relation type" in error for error in errors), errors)

    def test_self_edge_fails(self) -> None:
        catalog, schema, _ = validate_module.load()
        resource = copy.deepcopy(catalog["resources"][0])
        resource["relations"] = [{"type": "complements", "resource_id": resource["id"]}]
        catalog["resources"] = [resource]
        errors = validate_module.validate_catalog(catalog, schema, as_of=date(2026, 8, 1))
        self.assertTrue(any("must not self-reference" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
