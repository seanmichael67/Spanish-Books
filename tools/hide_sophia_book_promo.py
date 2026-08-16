#!/usr/bin/env python3
"""Remove the standard visible Sophia promo card from book pages."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK_GLOB = "books/week-*/index.html"
EXPECTED_BOOK_PAGES = 172
EXPECTED_MODERN_TEMPLATES = 136
SOPHIA_URL = "https://tutti-sophia.onrender.com/sofia-fullscreen.html"
SOPHIA_TITLE = "Meet Sofia — AI Spanish Teacher"
SOPHIA_CLAIM = "Your child speaks with a real AI tutor!"
GRID_BEFORE = "grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6"
GRID_AFTER = "grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6"
SOCIAL_MARKERS = (
    "Share this book with other parents!",
    "facebook.com/sharer/sharer.php",
    "https://wa.me/",
    "mailto:?subject=Free Spanish Book for Kids",
)
SOPHIA_RESIDUE = {
    "Tutti-Sophia destination": re.compile(r"tutti[-_.]?sophia", re.I),
    "Sophia fullscreen destination": re.compile(r"sofia-fullscreen", re.I),
    "AI Spanish teacher promotion": re.compile(r"\bAI\s+Spanish\s+Teacher\b", re.I),
    "AI tutor readiness claim": re.compile(r"\breal\s+AI\s+tutor\b", re.I),
    "Sophia AI promotion": re.compile(
        r"(?:\b(?:Sophia|Sofia|Sofía)\b.{0,80}\bAI\b|\bAI\b.{0,80}\b(?:Sophia|Sofia|Sofía)\b)",
        re.I | re.S,
    ),
}


def residue_labels(text: str) -> list[str]:
    return [label for label, pattern in SOPHIA_RESIDUE.items() if pattern.search(text)]


def validate_social(text: str, path: Path) -> None:
    modern_template = GRID_BEFORE in text or GRID_AFTER in text
    if not modern_template:
        return
    counts = {marker: text.count(marker) for marker in SOCIAL_MARKERS}
    if any(count != 1 for count in counts.values()):
        raise RuntimeError(f"{path}: social-sharing block changed unexpectedly {counts}")


def transform(text: str, path: Path) -> tuple[str, bool]:
    validate_social(text, path)
    marker_counts = {
        SOPHIA_URL: text.count(SOPHIA_URL),
        SOPHIA_TITLE: text.count(SOPHIA_TITLE),
        SOPHIA_CLAIM: text.count(SOPHIA_CLAIM),
        GRID_BEFORE: text.count(GRID_BEFORE),
    }
    if not any(marker_counts.values()):
        residue = residue_labels(text)
        if residue:
            raise RuntimeError(f"{path}: unrecognized Sophia promotion remains: {residue}")
        return text, False
    if any(count != 1 for count in marker_counts.values()):
        raise RuntimeError(f"{path}: unexpected Sophia promo shape {marker_counts}")

    lines = text.splitlines(keepends=True)
    starts = [index for index, line in enumerate(lines) if SOPHIA_URL in line]
    if len(starts) != 1:
        raise RuntimeError(f"{path}: expected one Sophia card, found {len(starts)}")

    start = starts[0]
    end = start + 5
    block = "".join(lines[start:end])
    if not all(marker in block for marker in (SOPHIA_URL, SOPHIA_TITLE, SOPHIA_CLAIM)):
        raise RuntimeError(f"{path}: Sophia card is truncated or unrecognized")
    if block.count("<a ") != 1 or block.count("</a>") != 1:
        raise RuntimeError(f"{path}: refusing to remove a malformed Sophia card")

    updated = "".join(lines[:start] + lines[end:])
    updated = updated.replace(GRID_BEFORE, GRID_AFTER, 1)
    validate_social(updated, path)
    residue = residue_labels(updated)
    if residue:
        raise RuntimeError(f"{path}: Sophia promotion survived removal: {residue}")
    return updated, True


def plan_changes(pages: list[Path]) -> list[tuple[Path, str]]:
    """Preflight every page before writing any page."""
    planned: list[tuple[Path, str]] = []
    for path in pages:
        original = path.read_text(encoding="utf-8")
        updated, has_promo = transform(original, path)
        if has_promo:
            planned.append((path, updated))
    return planned


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if any visible Sophia promo remains")
    args = parser.parse_args()

    pages = sorted(ROOT.glob(BOOK_GLOB))
    if len(pages) != EXPECTED_BOOK_PAGES:
        raise SystemExit(f"Expected {EXPECTED_BOOK_PAGES} book pages, found {len(pages)}")
    modern_templates = sum(
        GRID_BEFORE in path.read_text(encoding="utf-8")
        or GRID_AFTER in path.read_text(encoding="utf-8")
        for path in pages
    )
    if modern_templates != EXPECTED_MODERN_TEMPLATES:
        raise SystemExit(
            f"Expected {EXPECTED_MODERN_TEMPLATES} modern templates, found {modern_templates}"
        )

    planned = plan_changes(pages)
    if args.check and planned:
        print(f"FAIL — Sophia promo remains on {len(planned)} of {len(pages)} book pages")
        return 1
    if not args.check:
        for path, updated in planned:
            path.write_text(updated, encoding="utf-8")

    action = "would change" if args.check else "changed"
    print(f"PASS — {action} {len(planned)} of {len(pages)} book pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
