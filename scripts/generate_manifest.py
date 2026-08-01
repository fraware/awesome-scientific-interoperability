#!/usr/bin/env python3
"""Generate a deterministic SHA-256 manifest for every tracked release file.

Hashes git index blob contents so results are independent of working-tree
line-ending conversion (for example core.autocrlf on Windows).
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import date
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


def build_manifest() -> dict:
    files = []
    for path in tracked_paths():
        data = index_blob(path)
        files.append(
            {
                "path": path,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
            }
        )
    return {
        "generated_on": date.today().isoformat(),
        "file_count": len(files),
        "files": files,
    }


def main() -> int:
    MANIFEST.write_text(json.dumps(build_manifest(), indent=2) + "\n", encoding="utf-8")
    print(f"Generated {MANIFEST.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
