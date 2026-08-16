#!/usr/bin/env python3
"""Verify one useful meta-keywords tag on every Spanish book page."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.keywords: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "meta" and values.get("name", "").lower() == "keywords":
            self.keywords.append(values.get("content", ""))


def main() -> int:
    pages = sorted(ROOT.glob("books/week-*/index.html"))
    if not pages:
        raise SystemExit("FAIL — no book pages found")

    errors: list[str] = []
    counts: list[int] = []
    for path in pages:
        parser = MetaParser()
        parser.feed(path.read_text(encoding="utf-8"))
        if len(parser.keywords) != 1:
            errors.append(f"{path.relative_to(ROOT)}: expected one keyword tag, found {len(parser.keywords)}")
            continue
        phrases = [phrase.strip() for phrase in parser.keywords[0].split(",") if phrase.strip()]
        counts.append(len(phrases))
        if not 3 <= len(phrases) <= 8:
            errors.append(f"{path.relative_to(ROOT)}: expected 3–8 keyword phrases, found {len(phrases)}")
        normalized = [phrase.casefold() for phrase in phrases]
        if len(normalized) != len(set(normalized)):
            errors.append(f"{path.relative_to(ROOT)}: duplicate keyword phrase")

    if errors:
        print("FAIL — book keyword metadata verifier")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"PASS — {len(pages)} book pages each have one populated keyword tag "
        f"({min(counts)}–{max(counts)} phrases)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
