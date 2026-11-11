#!/usr/bin/env python3
"""Repair branding, canonical URLs, and accessibility in generated site files.

This script never talks to WordPress or GitHub. Use ``--write`` to update the
checked-out source tree; without it, the script is an idempotence check and
exits non-zero when repairs are still required.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY_URL = "https://www.beibeiamigos.com/spanish-books/"
BROKEN_FOOTER = (
    "&copy; 2025 Beibei Amigos Language Preschool — Visit Our School →"
    "copy; 2026 Beibei Amigos Language Preschool — Spanish Immersion · "
    "Mandarin Preschool · Bilingual Books — Visit Our School →"
)
FIXED_FOOTER = (
    "&copy; 2026 Beibei Amigos Language Preschool — Spanish Immersion · "
    "Mandarin Preschool · Bilingual Books — Visit Our School →"
)


def page_slug(book_slug: str) -> str:
    return re.sub(r"^week-\d+-", "", book_slug)


def canonical_url(book_slug: str) -> str:
    return f"{LIBRARY_URL}{page_slug(book_slug)}/"


def replace_meta_url(html: str, property_name: str, url: str) -> str:
    pattern = re.compile(
        rf'(<meta\s+property="{re.escape(property_name)}"\s+content=")[^"]*(">)'
    )
    return pattern.sub(rf"\g<1>{url}\g<2>", html, count=1)


def repair_book_app(html: str, book_slug: str) -> str:
    canonical = canonical_url(book_slug)
    old_render = f"https://spanish-books.onrender.com/books/{book_slug}/"

    html = html.replace(old_render, canonical)
    html = html.replace("Sofia", "Sophia")
    html = replace_meta_url(html, "og:url", canonical)
    html = re.sub(
        r'(<link\s+rel="canonical"\s+href=")[^"]*(">)',
        rf"\g<1>{canonical}\g<2>",
        html,
        count=1,
    )

    for before, after in (
        ("Meet Sofia", "Meet Sophia"),
        ("Try Sofia", "Try Sophia"),
        ("with Sofia", "with Sophia"),
        (BROKEN_FOOTER, FIXED_FOOTER),
        (
            "52 weeks of Spanish reading adventures",
            "A growing library of Spanish reading adventures",
        ),
        (
            '<a href="/" className="bg-white rounded-xl',
            f'<a href="{LIBRARY_URL}" target="_top" className="bg-white rounded-xl',
        ),
        (
            '<button onClick={() => readPage(true)} className=',
            '<button aria-label="Stop reading" onClick={() => readPage(true)} className=',
        ),
        (
            '<button onClick={() => nav(currentPage - 1, \'prev\')}',
            '<button aria-label="Previous page" onClick={() => nav(currentPage - 1, \'prev\')}',
        ),
        (
            '<button onClick={() => nav(currentPage + 1, \'next\')}',
            '<button aria-label="Next page" onClick={() => nav(currentPage + 1, \'next\')}',
        ),
        (
            '<img src={BOOK_CONFIG.logoUrl} className=',
            '<img src={BOOK_CONFIG.logoUrl} alt={BOOK_CONFIG.schoolName} className=',
        ),
        (
            '<img src={images[idx]} className=',
            '<img src={images[idx]} alt={BOOK_CONFIG.title} className=',
        ),
        (
            '<span className="text-8xl" role="img">📖</span>',
            '<span className="text-8xl" role="img" aria-label="Book illustration loading">📖</span>',
        ),
    ):
        if after not in html:
            html = html.replace(before, after)

    html = re.sub(
        r'target="_blank"(?!\s+rel=)',
        'target="_blank" rel="noopener noreferrer"',
        html,
    )
    return html


def repair_book_embed(html: str) -> str:
    html = html.replace("Sofia", "Sophia")
    html = html.replace(
        "Explore 100+ free interactive books in our growing themed library!",
        "Explore our growing library of free interactive Spanish books!",
    )
    return re.sub(
        r"We have \d+\+ free interactive books across \d+ themes!",
        "Explore our growing library of free interactive Spanish books!",
        html,
    )


def repair_library_embed(html: str) -> str:
    html = repair_book_embed(html)
    html = html.replace("Sofia", "Sophia")
    html = html.replace(
        '"url": "https://seanmichael67.github.io/Spanish-Books/",',
        f'"url": "{LIBRARY_URL}",',
    )
    return html


def candidate_repairs() -> list[tuple[Path, str]]:
    repairs: list[tuple[Path, str]] = []
    for path in sorted((ROOT / "books").glob("week-*/index.html")):
        html = path.read_text(encoding="utf-8")
        if "const Icons" in html:
            repairs.append((path, repair_book_app(html, path.parent.name)))

    template = ROOT / "templates" / "TEMPLATE-BOOK.html"
    if template.exists():
        html = template.read_text(encoding="utf-8")
        repairs.append((template, repair_book_app(html, "week-00-frutas-y-verduras")))

    for path in sorted((ROOT / "divi-embeds" / "books").glob("week-*.html")):
        repairs.append((path, repair_book_embed(path.read_text(encoding="utf-8"))))

    library = ROOT / "divi-embeds" / "library-divi.html"
    repairs.append((library, repair_library_embed(library.read_text(encoding="utf-8"))))
    return repairs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="write repairs; default is a read-only idempotence check",
    )
    args = parser.parse_args()

    changed: list[Path] = []
    for path, repaired in candidate_repairs():
        original = path.read_text(encoding="utf-8")
        if original == repaired:
            continue
        changed.append(path)
        if args.write:
            path.write_text(repaired, encoding="utf-8")

    action = "repaired" if args.write else "need repair"
    print(f"{len(changed)} files {action}")
    if changed:
        for path in changed[:12]:
            print(f"  {path.relative_to(ROOT)}")
        if len(changed) > 12:
            print(f"  … and {len(changed) - 12} more")
    return 0 if args.write or not changed else 1


if __name__ == "__main__":
    raise SystemExit(main())
