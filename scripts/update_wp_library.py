#!/usr/bin/env python3
"""Compatibility wrapper for the shared Beibei Spanish-book sync.

Dry-run is the default. Pass ``--apply`` to use the same transactional,
fail-closed publisher used by future weekly books.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--skip-previews", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    command = [
        sys.executable,
        str(root / "scripts" / "sync_wordpress_books.py"),
        "--root", str(root),
    ]
    if args.apply:
        command.append("--apply")
    if args.skip_previews:
        command.append("--skip-previews")
    return subprocess.run(command, cwd=root, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
