from __future__ import annotations

import importlib.util
import io
import ssl
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

MODULE_PATH = SCRIPTS / "check_links.py"
spec = importlib.util.spec_from_file_location("check_links", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules["check_links"] = module
spec.loader.exec_module(module)


class FakeResponse:
    def __init__(self, status: int, url: str) -> None:
        self.status = status
        self._url = url

    def geturl(self) -> str:
        return self._url

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *args: object) -> None:
        return None


class LinkClassificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = module.load_policy()

    def test_offline_rejects_malformed_urls(self) -> None:
        result = module.offline_validate("http://example.com/x")
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.classification, "invalid-url")

    def test_redirect_classified(self) -> None:
        opener = mock.Mock()
        opener.open.return_value = FakeResponse(200, "https://example.com/final")

        with mock.patch.object(module.urllib.request, "build_opener", return_value=opener):
            with mock.patch.object(module, "RedirectTracker") as tracker_cls:
                tracker = tracker_cls.return_value
                tracker.chain = ["https://example.com/final"]
                result = module.probe_once("https://example.com/start", self.policy, timeout=1.0)

        self.assertEqual(result.classification, "redirected")
        self.assertEqual(result.status, 200)
        self.assertEqual(result.redirect_chain, ["https://example.com/final"])

    def test_access_policy_403(self) -> None:
        opener = mock.Mock()
        opener.open.side_effect = urllib.error.HTTPError(
            "https://example.com/paywall",
            403,
            "Forbidden",
            hdrs=None,  # type: ignore[arg-type]
            fp=io.BytesIO(),
        )
        with mock.patch.object(module.urllib.request, "build_opener", return_value=opener):
            result = module.probe_once("https://example.com/paywall", self.policy, timeout=1.0)
        self.assertEqual(result.classification, "access-policy")
        self.assertEqual(result.status, 403)

    def test_transient_429_retries_then_exhausts(self) -> None:
        opener = mock.Mock()
        opener.open.side_effect = urllib.error.HTTPError(
            "https://example.com/rate",
            429,
            "Too Many Requests",
            hdrs=None,  # type: ignore[arg-type]
            fp=io.BytesIO(),
        )
        with mock.patch.object(module.urllib.request, "build_opener", return_value=opener):
            with mock.patch.object(module.time, "sleep"):
                result = module.check_url("https://example.com/rate", self.policy, timeout=1.0)
        self.assertEqual(result.classification, "transient-failure")
        self.assertEqual(result.status, 429)
        self.assertEqual(result.attempts, self.policy["retries"] + 1)

    def test_permanent_404(self) -> None:
        opener = mock.Mock()
        opener.open.side_effect = urllib.error.HTTPError(
            "https://example.com/missing",
            404,
            "Not Found",
            hdrs=None,  # type: ignore[arg-type]
            fp=io.BytesIO(),
        )
        with mock.patch.object(module.urllib.request, "build_opener", return_value=opener):
            result = module.probe_once("https://example.com/missing", self.policy, timeout=1.0)
        self.assertEqual(result.classification, "permanent-failure")
        self.assertEqual(result.status, 404)

    def test_tls_failure(self) -> None:
        opener = mock.Mock()
        opener.open.side_effect = urllib.error.URLError(ssl.SSLError("certificate verify failed"))
        with mock.patch.object(module.urllib.request, "build_opener", return_value=opener):
            result = module.probe_once("https://example.com/tls", self.policy, timeout=1.0)
        self.assertEqual(result.classification, "tls-or-dns-failure")

    def test_blocking_set(self) -> None:
        self.assertIn("permanent-failure", module.BLOCKING)
        self.assertIn("tls-or-dns-failure", module.BLOCKING)
        self.assertIn("invalid-url", module.BLOCKING)
        self.assertNotIn("access-policy", module.BLOCKING)
        self.assertNotIn("transient-failure", module.BLOCKING)


if __name__ == "__main__":
    unittest.main()
