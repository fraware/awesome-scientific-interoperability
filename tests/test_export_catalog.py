from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

MODULE_PATH = SCRIPTS / "export_catalog.py"
spec = importlib.util.spec_from_file_location("export_catalog", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

FIXED_DATE = "2026-08-02"


class ExportCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmpdir = tempfile.TemporaryDirectory()
        cls.out_dir = Path(cls._tmpdir.name) / "dist"
        code_buffer = io.StringIO()
        with redirect_stdout(code_buffer):
            code = module.main(["--out-dir", str(cls.out_dir), "--generated-on", FIXED_DATE])
        if code != 0:
            raise AssertionError(f"export_catalog failed with code {code}")
        cls.catalog = json.loads((cls.out_dir / "catalog.json").read_text(encoding="utf-8"))
        cls.relations = json.loads((cls.out_dir / "relations.json").read_text(encoding="utf-8"))
        cls.jsonld = json.loads((cls.out_dir / "catalog.jsonld").read_text(encoding="utf-8"))
        cls.problems = json.loads((cls.out_dir / "problems.json").read_text(encoding="utf-8"))
        cls.guides = json.loads((cls.out_dir / "guides-index.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmpdir.cleanup()

    def test_all_artifacts_written(self) -> None:
        for name in module.ARTIFACT_NAMES:
            path = self.out_dir / name
            self.assertTrue(path.is_file(), name)
            self.assertGreater(path.stat().st_size, 0, name)

    def test_catalog_schema_shape(self) -> None:
        self.assertIn("meta", self.catalog)
        self.assertIn("resources", self.catalog)
        meta = self.catalog["meta"]
        self.assertEqual(meta["export_generated_on"], FIXED_DATE)
        self.assertEqual(meta["resource_count"], len(self.catalog["resources"]))
        self.assertGreaterEqual(meta["resource_count"], 87)

        required = {
            "id",
            "name",
            "url",
            "section",
            "resource_kind",
            "steward_id",
            "steward",
            "implementations",
            "relations",
            "evidence_types",
            "boundary_note",
        }
        for resource in self.catalog["resources"]:
            self.assertTrue(required.issubset(resource.keys()), resource.get("id"))
            self.assertIsInstance(resource["implementations"], list)
            self.assertIsInstance(resource["relations"], list)
            if resource["steward"] is not None:
                self.assertEqual(
                    set(resource["steward"].keys()),
                    {"id", "name", "type", "url"},
                )

    def test_resources_sorted_by_section_then_name(self) -> None:
        ids = [item["id"] for item in self.catalog["resources"]]
        sorted_ids = [
            item["id"]
            for item in module.sort_resources(
                [{"id": r["id"], "name": r["name"], "section": r["section"]} for r in self.catalog["resources"]]
            )
        ]
        self.assertEqual(ids, sorted_ids)

    def test_joined_steward_and_implementations(self) -> None:
        bagit = next(item for item in self.catalog["resources"] if item["id"] == "bagit")
        self.assertIsNotNone(bagit["steward"])
        self.assertEqual(bagit["steward"]["id"], bagit["steward_id"])
        self.assertTrue(bagit["steward"]["name"])
        impl_ids = [item["id"] for item in bagit["implementations"]]
        self.assertEqual(impl_ids, sorted(impl_ids))
        self.assertTrue(impl_ids)

    def test_relations_edge_list_shape(self) -> None:
        self.assertIn("edges", self.relations)
        for edge in self.relations["edges"]:
            self.assertEqual(set(edge.keys()), {"source", "type", "target"})
        keys = [(e["source"], e["type"], e["target"]) for e in self.relations["edges"]]
        self.assertEqual(keys, sorted(keys))

    def test_jsonld_has_context_and_graph_fields(self) -> None:
        self.assertIn("@context", self.jsonld)
        self.assertIn("resources", self.jsonld)
        self.assertIn("edges", self.jsonld)
        self.assertEqual(self.jsonld["resources"], self.catalog["resources"])
        self.assertEqual(self.jsonld["edges"], self.relations["edges"])

    def test_csv_header_and_row_count(self) -> None:
        text = (self.out_dir / "catalog.csv").read_text(encoding="utf-8")
        rows = list(csv.DictReader(io.StringIO(text)))
        self.assertEqual(len(rows), self.catalog["meta"]["resource_count"])
        self.assertEqual(tuple(rows[0].keys()), module.CSV_COLUMNS)
        self.assertTrue(any(row["id"] == "ro-crate" for row in rows))

    def test_problems_index_shape(self) -> None:
        self.assertGreaterEqual(self.problems["meta"]["problem_count"], 8)
        ids = [item["id"] for item in self.problems["problems"]]
        self.assertEqual(ids, sorted(ids))
        self.assertIn("identify-research-objects", ids)
        for problem in self.problems["problems"]:
            self.assertIn("title", problem)
            self.assertIsInstance(problem["resource_ids"], list)
            self.assertEqual(problem["resource_ids"], sorted(problem["resource_ids"]))
            self.assertTrue(problem["resource_ids"])

    def test_guides_index_shape(self) -> None:
        self.assertGreaterEqual(self.guides["meta"]["guide_count"], 1)
        ids = [item["id"] for item in self.guides["guides"]]
        self.assertEqual(ids, sorted(ids))
        self.assertIn("research-object-packaging", ids)
        for guide in self.guides["guides"]:
            self.assertTrue(guide["path"].startswith("docs/decision-guides/"))
            self.assertEqual(guide["resource_ids"], sorted(guide["resource_ids"]))

    def test_export_is_byte_deterministic(self) -> None:
        second_dir = Path(self._tmpdir.name) / "dist-2"
        module.export_all(second_dir, generated_on=FIXED_DATE)
        for name in module.ARTIFACT_NAMES:
            first = (self.out_dir / name).read_bytes()
            second = (second_dir / name).read_bytes()
            self.assertEqual(
                hashlib.sha256(first).hexdigest(),
                hashlib.sha256(second).hexdigest(),
                name,
            )
            self.assertEqual(first, second, name)

    def test_invalid_generated_on_exits_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code = module.main(["--out-dir", tmp, "--generated-on", "not-a-date"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
