from __future__ import annotations

import importlib.util
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_expansion_candidates.py"
SPEC = importlib.util.spec_from_file_location("validate_expansion_candidates", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class ExpansionCandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = module.load_registry()
        self.candidates = self.payload["candidates"]

    def test_registry_validates(self) -> None:
        self.assertEqual(module.validate(), [])

    def test_research_breadth(self) -> None:
        self.assertGreaterEqual(len(self.candidates), 50)
        self.assertGreaterEqual(
            len({item["coverage_family"] for item in self.candidates}), 35
        )

    def test_admission_queue_is_substantive(self) -> None:
        counts = Counter(item["priority"] for item in self.candidates)
        self.assertGreaterEqual(counts["P0"], 15)
        for item in self.candidates:
            if item["priority"] == "P0":
                self.assertEqual(item["disposition"], "admission-pr")
                self.assertGreaterEqual(len(item["primary_sources"]), 3)

    def test_no_duplicate_candidate_identity(self) -> None:
        for field in ("id", "name", "official_url"):
            values = [item[field] for item in self.candidates]
            self.assertEqual(len(values), len(set(values)), field)


if __name__ == "__main__":
    unittest.main()
