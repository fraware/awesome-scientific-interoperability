from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "build_site.py"
spec = importlib.util.spec_from_file_location("build_site", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class BuildSiteTests(unittest.TestCase):
    def test_site_build_emits_core_routes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "dist"
            module.build_site(out, generated_on="2026-08-02")
            expected = [
                "index.html",
                "problems/index.html",
                "guides/index.html",
                "explore/index.html",
                "compare/index.html",
                "graph/index.html",
                "downloads/index.html",
                "about/index.html",
                "data/catalog.json",
                "data/relations.json",
                "resource/ro-crate.html",
                "guides/research-object-packaging.html",
                "problems/identify-research-objects.html",
                "assets/app.js",
                "assets/styles.css",
                ".nojekyll",
            ]
            for relative in expected:
                self.assertTrue((out / relative).is_file(), relative)
            home = (out / "index.html").read_text(encoding="utf-8")
            self.assertIn("Start from a problem", home)
            self.assertIn("Browse the Awesome list", home)
            about = (out / "about" / "index.html").read_text(encoding="utf-8")
            self.assertIn("single-maintainer limitation", about)


if __name__ == "__main__":
    unittest.main()
