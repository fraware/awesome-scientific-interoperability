#!/usr/bin/env python3
"""Verify that MANIFEST.json exactly covers every tracked release file.

Compares against git index blob contents so verification matches CI checkouts
regardless of local working-tree line endings.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"


def tracked_paths() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    paths = [item.decode("utf-8") for item in result.stdout.split(b"\0") if item]
    return sorted(path for path in paths if path != "MANIFEST.json")


def index_blob(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f":{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return result.stdout


def main() -> int:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = payload.get("files", [])
    recorded = [entry.get("path") for entry in entries]
    expected = tracked_paths()
    errors: list[str] = []

    if payload.get("file_count") != len(entries):
        errors.append("file_count does not match the number of manifest entries")
    if recorded != expected:
        missing = sorted(set(expected) - set(recorded))
        extra = sorted(set(recorded) - set(expected))
        if missing:
            errors.append(f"tracked files missing from manifest: {missing}")
        if extra:
            errors.append(f"manifest entries are not tracked files: {extra}")
        if not missing and not extra:
            errors.append("manifest entries are not deterministically sorted")

    for entry in entries:
        relative = entry.get("path", "")
        try:
            data = index_blob(relative)
        except subprocess.CalledProcessError:
            errors.append(f"missing indexed file: {relative}")
            continue
        digest = hashlib.sha256(data).hexdigest()
        if entry.get("sha256") != digest:
            errors.append(f"SHA-256 mismatch: {relative}")
        if entry.get("bytes") != len(data):
            errors.append(f"byte-count mismatch: {relative}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Verified {len(entries)} tracked release files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
