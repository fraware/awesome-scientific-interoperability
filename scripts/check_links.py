#!/usr/bin/env python3
"""Classify canonical resource URLs with auditable HTTP semantics."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import ssl
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

from validate_catalog import load

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "link-policy.yaml"

CLASSIFICATIONS = (
    "ok",
    "redirected",
    "access-policy",
    "transient-failure",
    "permanent-failure",
    "tls-or-dns-failure",
    "invalid-url",
)

BLOCKING = frozenset({"invalid-url", "permanent-failure", "tls-or-dns-failure"})


@dataclass
class LinkResult:
    url: str
    classification: str
    status: int | None = None
    final_url: str | None = None
    redirect_chain: list[str] = field(default_factory=list)
    error: str | None = None
    attempts: int = 0


def load_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"link policy must be a mapping: {path}")
    required = {
        "accepted_redirect_hops",
        "transient_statuses",
        "access_policy_statuses",
        "permanent_failure_statuses",
        "user_agent",
        "retries",
        "backoff_seconds",
    }
    missing = sorted(required - set(payload))
    if missing:
        raise ValueError(f"link policy missing fields: {missing}")
    return payload


def offline_validate(url: str) -> LinkResult | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc or " " in url:
        return LinkResult(url=url, classification="invalid-url", error="URL must be a valid https URL")
    return None


class RedirectTracker(urllib.request.HTTPRedirectHandler):
    def __init__(self, max_hops: int) -> None:
        self.max_hops = max_hops
        self.chain: list[str] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        self.chain.append(newurl)
        if len(self.chain) > self.max_hops:
            raise urllib.error.HTTPError(req.full_url, code, f"too many redirects (>{self.max_hops})", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _transport_classification(exc: BaseException) -> str:
    text = str(exc).lower()
    if isinstance(exc, ssl.SSLError) or "ssl" in text or "certificate" in text:
        return "tls-or-dns-failure"
    if isinstance(exc, socket_error_types()) or "name or service not known" in text or "getaddrinfo" in text:
        return "tls-or-dns-failure"
    if "timed out" in text or "timeout" in text or "temporarily" in text:
        return "transient-failure"
    return "tls-or-dns-failure"


def socket_error_types() -> tuple[type[BaseException], ...]:
    import socket

    return (socket.gaierror, socket.herror, TimeoutError, socket.timeout)


def classify_status(status: int, policy: dict[str, Any], redirected: bool) -> str:
    if status in policy["access_policy_statuses"]:
        return "access-policy"
    if status in policy["permanent_failure_statuses"]:
        return "permanent-failure"
    if status in policy["transient_statuses"]:
        return "transient-failure"
    if 200 <= status < 300:
        return "redirected" if redirected else "ok"
    if 300 <= status < 400:
        return "redirected"
    if status >= 500:
        return "transient-failure"
    return "permanent-failure"


def probe_once(url: str, policy: dict[str, Any], timeout: float) -> LinkResult:
    headers = {
        "User-Agent": policy["user_agent"],
        "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
    }
    max_hops = int(policy["accepted_redirect_hops"])
    last_error: str | None = None
    for method in ("HEAD", "GET"):
        tracker = RedirectTracker(max_hops)
        opener = urllib.request.build_opener(tracker)
        request = urllib.request.Request(url, headers=headers, method=method)
        try:
            with opener.open(request, timeout=timeout) as response:
                status = int(response.status)
                final_url = response.geturl()
                redirected = bool(tracker.chain) or final_url.rstrip("/") != url.rstrip("/")
                return LinkResult(
                    url=url,
                    classification=classify_status(status, policy, redirected),
                    status=status,
                    final_url=final_url,
                    redirect_chain=list(tracker.chain),
                    attempts=1,
                )
        except urllib.error.HTTPError as exc:
            status = int(exc.code)
            if method == "HEAD" and status == 405:
                last_error = str(exc)
                continue
            redirected = bool(tracker.chain)
            return LinkResult(
                url=url,
                classification=classify_status(status, policy, redirected),
                status=status,
                final_url=getattr(exc, "url", None) or url,
                redirect_chain=list(tracker.chain),
                error=str(exc.reason) if exc.reason else str(exc),
                attempts=1,
            )
        except (urllib.error.URLError, TimeoutError, ssl.SSLError, OSError) as exc:
            cause: BaseException = exc.reason if isinstance(exc, urllib.error.URLError) and exc.reason else exc
            last_error = str(cause)
            if method == "HEAD":
                continue
            return LinkResult(
                url=url,
                classification=_transport_classification(cause),
                error=last_error,
                attempts=1,
            )
    return LinkResult(
        url=url,
        classification="transient-failure",
        error=last_error or "unreachable",
        attempts=1,
    )


def check_url(url: str, policy: dict[str, Any], timeout: float) -> LinkResult:
    invalid = offline_validate(url)
    if invalid is not None:
        return invalid

    retries = int(policy["retries"])
    backoff = float(policy["backoff_seconds"])
    attempts = 0
    result = LinkResult(url=url, classification="transient-failure", error="not attempted")
    while attempts <= retries:
        attempts += 1
        result = probe_once(url, policy, timeout)
        result.attempts = attempts
        if result.classification != "transient-failure":
            return result
        if attempts <= retries:
            time.sleep(backoff * attempts)
    return result


def write_json_report(path: Path, results: list[LinkResult], policy: dict[str, Any]) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy_version": policy.get("version"),
        "counts": _counts(results),
        "results": [asdict(item) for item in sorted(results, key=lambda item: item.url)],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_markdown_report(path: Path, results: list[LinkResult], policy: dict[str, Any]) -> None:
    counts = _counts(results)
    lines = [
        "# Link Audit Report",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        f"Policy version: {policy.get('version')}",
        "",
        "## Counts",
        "",
    ]
    for key in CLASSIFICATIONS:
        lines.append(f"- `{key}`: {counts.get(key, 0)}")
    lines.extend(["", "## Results", ""])
    for item in sorted(results, key=lambda result: (result.classification, result.url)):
        status = item.status if item.status is not None else "-"
        detail = item.error or item.final_url or ""
        lines.append(f"- `{item.classification}` `{status}` {item.url} — {detail}".rstrip(" —"))
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _counts(results: list[LinkResult]) -> dict[str, int]:
    counts = {key: 0 for key in CLASSIFICATIONS}
    for item in results:
        counts[item.classification] = counts.get(item.classification, 0) + 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--offline", action="store_true", help="Validate URL syntax without network access")
    parser.add_argument(
        "--scope",
        choices=("canonical", "all"),
        default="canonical",
        help="canonical: main-list resource URLs; all: canonical + watchlist + steward + reference URLs",
    )
    parser.add_argument("--policy", type=Path, default=POLICY_PATH)
    parser.add_argument("--json-report", type=Path)
    parser.add_argument("--markdown-report", type=Path)
    args = parser.parse_args()

    policy = load_policy(args.policy)
    catalog, _, _ = load()
    urls = {resource["url"] for resource in catalog["resources"]}
    if args.scope == "all":
        watchlist_path = ROOT / "catalog" / "watchlist.yaml"
        if watchlist_path.exists():
            watchlist = yaml.safe_load(watchlist_path.read_text(encoding="utf-8"))
            for item in watchlist.get("items", []):
                urls.add(item["url"])
                for source_ref in item.get("source_refs") or []:
                    pass
        references_path = ROOT / "catalog" / "references.yaml"
        if references_path.exists():
            references = yaml.safe_load(references_path.read_text(encoding="utf-8"))
            for item in references.get("references", []):
                urls.add(item["url"])
        stewards_path = ROOT / "catalog" / "stewards.yaml"
        if stewards_path.exists():
            stewards = yaml.safe_load(stewards_path.read_text(encoding="utf-8"))
            for item in stewards.get("stewards", []):
                urls.add(item["url"])
    urls_list = sorted(urls)

    if args.offline:
        results = [offline_validate(url) or LinkResult(url=url, classification="ok") for url in urls_list]
        invalid = [item for item in results if item.classification == "invalid-url"]
        if args.json_report:
            write_json_report(args.json_report, results, policy)
        if args.markdown_report:
            write_markdown_report(args.markdown_report, results, policy)
        if invalid:
            for item in invalid:
                print(f"INVALID {item.url}")
            return 1
        print(f"Validated syntax for {len(urls_list)} HTTPS URLs (scope={args.scope}).")
        return 0

    results: list[LinkResult] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check_url, url, policy, args.timeout): url for url in urls_list}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            status = result.status if result.status is not None else "ERR"
            detail = result.final_url or result.error or ""
            print(f"{result.classification:20} {status!s:>5} {result.url} -> {detail}")

    results.sort(key=lambda item: item.url)
    if args.json_report:
        write_json_report(args.json_report, results, policy)
    if args.markdown_report:
        write_markdown_report(args.markdown_report, results, policy)

    blocking = [item for item in results if item.classification in BLOCKING]
    counts = _counts(results)
    print("Classification counts: " + ", ".join(f"{key}={counts[key]}" for key in CLASSIFICATIONS))
    if blocking:
        print(f"{len(blocking)} unresolved blocking failure(s).")
        return 1
    print(
        f"Checked {len(urls_list)} links (scope={args.scope}) with no unresolved permanent, "
        "invalid, or TLS/DNS failures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
