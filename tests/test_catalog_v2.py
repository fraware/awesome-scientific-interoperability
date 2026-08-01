from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

MODULE_PATH = SCRIPTS / "validate_catalog_v2.py"
spec = importlib.util.spec_from_file_location("validate_catalog_v2", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules["validate_catalog_v2"] = module
spec.loader.exec_module(module)

FIXTURES = ROOT / "tests" / "fixtures" / "v2"


class CatalogV2Tests(unittest.TestCase):
    def test_fixture_directory_has_at_least_twelve_cases(self) -> None:
        fixtures = list(FIXTURES.glob("*.yaml"))
        self.assertGreaterEqual(len(fixtures), 12)

    def test_valid_fixtures_pass(self) -> None:
        for path in sorted(FIXTURES.glob("*.valid.yaml")):
            with self.subTest(path=path.name):
                catalog = module.load_catalog_document(path)
                self.assertEqual(module.validate_catalog(catalog), [])

    def test_invalid_fixtures_fail(self) -> None:
        for path in sorted(FIXTURES.glob("*.invalid.yaml")):
            with self.subTest(path=path.name):
                catalog = module.load_catalog_document(path)
                self.assertTrue(module.validate_catalog(catalog))

    def test_live_v1_catalog_is_not_required_to_pass_v2(self) -> None:
        catalog = module.load_catalog_from_index(ROOT / "catalog" / "resources.yaml")
        errors = module.validate_catalog(catalog)
        self.assertTrue(errors, "live v1 records must still fail v2 until migration")


if __name__ == "__main__":
    unittest.main()
