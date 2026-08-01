#!/usr/bin/env python3
"""Generate a deterministic SHA-256 manifest for every tracked release file."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    paths = [ROOT / item.decode("utf-8") for item in result.stdout.split(b"\0") if item]
    return sorted((path for path in paths if path != MANIFEST), key=lambda path: path.relative_to(ROOT).as_posix())


def build_manifest() -> dict:
    files = []
    for path in tracked_files():
        data = path.read_bytes()
        files.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
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
