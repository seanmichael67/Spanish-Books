#!/usr/bin/env python3
"""Adversarial checks for fail-closed book metadata tooling."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require_raises(label: str, function) -> None:
    try:
        function()
    except RuntimeError:
        return
    raise SystemExit(f"FAIL — {label} did not fail closed")


def main() -> int:
    keywords = load("book_metadata", ROOT / "tools" / "complete_book_metadata.py")

    reversed_tag = '<html><head><title>X</title><meta data-extra="yes" content="a, b, c" name="keywords"></head></html>'
    updated, changed = keywords.add_keywords(
        reversed_tag,
        "week-25-la-cocina-de-abuela",
        Path("reversed.html"),
    )
    if changed or updated != reversed_tag:
        raise SystemExit("FAIL — reordered keyword attributes were not preserved")

    duplicate_tags = reversed_tag.replace("</head>", '<meta name="keywords" content="d, e, f"></head>')
    require_raises(
        "duplicate reordered keyword tags",
        lambda: keywords.add_keywords(
            duplicate_tags,
            "week-25-la-cocina-de-abuela",
            Path("duplicate.html"),
        ),
    )

    reordered_description = (
        '<html><head><title>X</title><meta data-extra="yes" '
        'content="Una descripción válida y existente." name="description"></head></html>'
    )
    updated, changed = keywords.add_description(
        reordered_description,
        "week-39-las-frutas",
        Path("description.html"),
    )
    if changed or updated != reordered_description:
        raise SystemExit("FAIL — reordered description attributes were not preserved")

    blank_description = '<html><head><title>X</title><meta name="description" content=""></head></html>'
    require_raises(
        "blank description",
        lambda: keywords.add_description(
            blank_description,
            "week-39-las-frutas",
            Path("blank-description.html"),
        ),
    )
    duplicate_descriptions = reordered_description.replace(
        "</head>", '<meta name="description" content="Otra descripción"></head>'
    )
    require_raises(
        "duplicate description tags",
        lambda: keywords.add_description(
            duplicate_descriptions,
            "week-39-las-frutas",
            Path("duplicate-description.html"),
        ),
    )

    with tempfile.TemporaryDirectory(prefix="book-keyword-preflight-") as temp:
        temp_root = Path(temp)
        first = temp_root / "week-25-la-cocina-de-abuela" / "index.html"
        last = temp_root / "week-unmapped" / "index.html"
        first.parent.mkdir(parents=True)
        last.parent.mkdir(parents=True)
        first.write_text("<html><head><title>First</title></head></html>", encoding="utf-8")
        last.write_text("<html><head><title>Last</title></head></html>", encoding="utf-8")
        before = first.read_text(encoding="utf-8")
        require_raises("late keyword preflight failure", lambda: keywords.plan_changes([first, last]))
        if first.read_text(encoding="utf-8") != before:
            raise SystemExit("FAIL — keyword preflight wrote an earlier page before later validation failed")

    print("PASS — adversarial metadata attributes, duplicates, blanks, and preflight fail closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
