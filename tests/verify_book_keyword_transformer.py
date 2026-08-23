#!/usr/bin/env python3
"""Regression checks for the curated keyword transformer contract."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "add_missing_book_keywords.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("book_keywords", TOOL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {TOOL_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    tool = load_tool()
    if len(tool.KEYWORDS) != 29:
        raise SystemExit(f"FAIL — expected 29 curated mappings, found {len(tool.KEYWORDS)}")

    slug = "week-25-la-cocina-de-abuela"
    source = "<html>\n<head>\n<title>La cocina de abuela</title>\n</head>\n<body></body>\n</html>\n"
    updated, changed = tool.add_keywords(source, slug, Path("fixture.html"))
    if not changed or updated.count('<meta name="keywords"') != 1:
        raise SystemExit("FAIL — mapped page did not receive exactly one keyword tag")

    rerun, changed_again = tool.add_keywords(updated, slug, Path("fixture.html"))
    if changed_again or rerun != updated:
        raise SystemExit("FAIL — transformer is not idempotent")

    try:
        tool.add_keywords(source, "week-unmapped", Path("unmapped.html"))
    except RuntimeError:
        pass
    else:
        raise SystemExit("FAIL — missing curated mapping did not fail closed")

    print("PASS — 29 mappings; insertion, idempotence, and fail-closed behavior verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
