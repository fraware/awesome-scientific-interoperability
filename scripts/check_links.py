#!/usr/bin/env python3
"""Check canonical resource URLs with conservative HTTP semantics."""

from __future__ import annotations

import argparse
import concurrent.futures
import socket
import urllib.error
import urllib.request
from pathlib import Path

from validate_catalog import load

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "awesome-scientific-interoperability-link-check/1.0"


def check(url: str, timeout: float) -> tuple[str, int | str, str]:
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8"}
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return url, response.status, response.geturl()
        except urllib.error.HTTPError as exc:
            if exc.code in {401, 403, 405, 406, 429}:
                if method == "HEAD" and exc.code == 405:
                    continue
                return url, exc.code, url
            if method == "HEAD":
                continue
            return url, exc.code, str(exc)
        except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
            if method == "HEAD":
                continue
            return url, "ERROR", str(exc)
    return url, "ERROR", "unreachable"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--offline", action="store_true", help="Validate URL syntax without network access")
    args = parser.parse_args()

    catalog, _, _ = load()
    urls = sorted(resource["url"] for resource in catalog["resources"])
    if args.offline:
        invalid = [url for url in urls if not url.startswith("https://") or " " in url]
        if invalid:
            for url in invalid:
                print(f"INVALID {url}")
            return 1
        print(f"Validated syntax for {len(urls)} HTTPS URLs.")
        return 0

    failed = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(check, url, args.timeout) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            url, status, detail = future.result()
            print(f"{status!s:>5} {url} -> {detail}")
            if status == "ERROR" or (isinstance(status, int) and status >= 500):
                failed.append((url, status, detail))
    if failed:
        print(f"{len(failed)} link(s) require review.")
        return 1
    print(f"Checked {len(urls)} links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
