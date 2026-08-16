#!/usr/bin/env python3
"""Regression gate: individual books must not expose Sophia before launch."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PAGES = 172
EXPECTED_MODERN_TEMPLATES = 136
GRID_BEFORE = "grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6"
GRID_AFTER = "grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6"
SOCIAL_MARKERS = {
    "sharing prompt": "Share this book with other parents!",
    "Facebook share action": "facebook.com/sharer/sharer.php",
    "WhatsApp share action": "https://wa.me/",
    "email share action": "mailto:?subject=Free Spanish Book for Kids",
}
SOPHIA_PATTERNS = {
    "Tutti-Sophia destination": re.compile(r"tutti[-_.]?sophia", re.I),
    "Sophia fullscreen destination": re.compile(r"sofia-fullscreen", re.I),
    "AI Spanish teacher promotion": re.compile(r"\bAI\s+Spanish\s+Teacher\b", re.I),
    "AI tutor readiness claim": re.compile(r"\breal\s+AI\s+tutor\b", re.I),
    "Sophia AI promotion": re.compile(
        r"(?:\b(?:Sophia|Sofia|Sofía)\b.{0,80}\bAI\b|\bAI\b.{0,80}\b(?:Sophia|Sofia|Sofía)\b)",
        re.I | re.S,
    ),
}


def validate_page(text: str, path: Path) -> tuple[list[str], bool]:
    errors: list[str] = []
    for label, pattern in SOPHIA_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"{path}: contains {label}")
    if GRID_BEFORE in text:
        errors.append(f"{path}: contains stale three-card grid")

    modern_template = GRID_AFTER in text
    social_counts = {label: text.count(marker) for label, marker in SOCIAL_MARKERS.items()}
    if modern_template:
        for label, count in social_counts.items():
            if count != 1:
                errors.append(f"{path}: expected one {label}, found {count}")
    elif any(social_counts.values()):
        errors.append(f"{path}: social block exists without the expected two-card promo grid")

    if not text.rstrip().endswith("</html>"):
        errors.append(f"{path}: incomplete HTML document")
    return errors, modern_template


def main() -> int:
    pages = sorted(ROOT.glob("books/week-*/index.html"))
    if len(pages) != EXPECTED_PAGES:
        print(f"FAIL — expected {EXPECTED_PAGES} book pages, found {len(pages)}")
        return 1

    errors: list[str] = []
    modern_templates = 0
    for path in pages:
        page_errors, modern = validate_page(path.read_text(encoding="utf-8"), path.relative_to(ROOT))
        errors.extend(page_errors)
        modern_templates += int(modern)

    if modern_templates != EXPECTED_MODERN_TEMPLATES:
        errors.append(
            f"expected {EXPECTED_MODERN_TEMPLATES} modern book templates, found {modern_templates}"
        )

    if errors:
        print("FAIL — Sophia book-promo verifier")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"PASS — Sophia hidden on {len(pages)} book pages; "
        f"all {modern_templates} social blocks preserved and grids rebalanced"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
