#!/usr/bin/env python3
"""Adversarial checks for fail-closed book sweep tooling and gates."""
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
    hide = load("hide_sophia", ROOT / "tools" / "hide_sophia_book_promo.py")
    hide_gate = load("hide_sophia_gate", ROOT / "tests" / "verify_no_sophia_book_promo.py")
    keywords = load("book_keywords", ROOT / "tools" / "add_missing_book_keywords.py")

    page_path = ROOT / "books" / "week-95-contar" / "index.html"
    current = page_path.read_text(encoding="utf-8")
    variant = current.replace(
        "</body>",
        '<a href="https://tutti-sophia.onrender.com/">Try Sophia, our AI teacher</a>\n</body>',
    )
    require_raises("changed Sophia URL/copy transformer", lambda: hide.transform(variant, page_path))
    errors, _ = hide_gate.validate_page(variant, page_path.relative_to(ROOT))
    if not any("Sophia" in error for error in errors):
        raise SystemExit("FAIL — changed Sophia URL/copy gate mutation was accepted")

    reversed_variant = current.replace(
        "</body>",
        '<a href="https://example.com/try">Meet our AI teacher Sofia</a>\n</body>',
    )
    require_raises(
        "changed domain/reversed Sophia copy transformer",
        lambda: hide.transform(reversed_variant, page_path),
    )
    errors, _ = hide_gate.validate_page(reversed_variant, page_path.relative_to(ROOT))
    if not any("Sophia" in error for error in errors):
        raise SystemExit("FAIL — changed domain/reversed Sophia copy gate mutation was accepted")

    for label, marker in hide_gate.SOCIAL_MARKERS.items():
        mutated = current.replace(marker, f"REMOVED-{label}", 1)
        require_raises(
            f"deleted {label} transformer",
            lambda mutated=mutated: hide.transform(mutated, page_path),
        )
        errors, _ = hide_gate.validate_page(mutated, page_path.relative_to(ROOT))
        if not errors:
            raise SystemExit(f"FAIL — deleted {label} gate mutation was accepted")

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

    print(
        "PASS — adversarial Sophia variants/social deletions and keyword attribute/preflight "
        "mutations fail closed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
