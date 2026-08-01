from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_catalog.py"
spec = importlib.util.spec_from_file_location("validate_catalog", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class CatalogTests(unittest.TestCase):
    def test_repository_invariants(self) -> None:
        self.assertEqual(module.validate(), [])

    def test_seed_size(self) -> None:
        catalog, _, readme = module.load()
        self.assertEqual(len(catalog["resources"]), 75)
        self.assertEqual(len(module.readme_entries(readme)), 75)

    def test_every_section_has_resources(self) -> None:
        catalog, _, _ = module.load()
        sections = {resource["section"] for resource in catalog["resources"]}
        expected = {
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
        self.assertEqual(sections, expected)

    def test_catalog_index_is_complete(self) -> None:
        import yaml

        index_path = ROOT / "catalog" / "resources.yaml"
        index = yaml.safe_load(index_path.read_text(encoding="utf-8"))
        self.assertEqual(len(index["resource_files"]), 11)
        for relative_path in index["resource_files"]:
            self.assertTrue((index_path.parent / relative_path).is_file())


if __name__ == "__main__":
    unittest.main()
