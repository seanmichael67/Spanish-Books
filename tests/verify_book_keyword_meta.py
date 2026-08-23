#!/usr/bin/env python3
"""Verify one useful meta-keywords tag on every Spanish book page."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESCRIPTION_TARGETS = {
    "week-39-las-frutas",
    "week-45-las-profesiones",
    "week-50-los-insectos",
    "week-51-las-maravillas-del-mar",
    "week-52-el-viaje-de-los-pajaros",
    "week-54-los-amigos-de-la-comunidad",
    "week-56-las-formas-geometricas",
    "week-57-la-primavera-y-las-flores",
    "week-58-el-dia-y-la-noche",
    "week-59-los-sentidos",
    "week-60-el-ciclo-del-agua",
    "week-61-las-emociones",
    "week-62-los-instrumentos-musicales",
    "week-63-la-granja-y-sus-animales",
    "week-64-el-parque-de-juegos",
    "week-68-las-abejas-y-el-jardin",
    "week-70-el-reino-submarino",
    "week-71-el-viaje-espacial",
    "week-73-el-clima",
}


class MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.values: dict[str, list[str]] = {"keywords": [], "description": []}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        name = values.get("name", "").lower()
        if tag.lower() == "meta" and name in self.values:
            self.values[name].append(values.get("content", ""))


def main() -> int:
    pages = sorted(ROOT.glob("books/week-*/index.html"))
    if not pages:
        raise SystemExit("FAIL — no book pages found")

    errors: list[str] = []
    counts: list[int] = []
    for path in pages:
        parser = MetaParser()
        parser.feed(path.read_text(encoding="utf-8"))
        keywords = parser.values["keywords"]
        if len(keywords) != 1:
            errors.append(f"{path.relative_to(ROOT)}: expected one keyword tag, found {len(keywords)}")
            continue
        phrases = [phrase.strip() for phrase in keywords[0].split(",") if phrase.strip()]
        counts.append(len(phrases))
        if not 3 <= len(phrases) <= 8:
            errors.append(f"{path.relative_to(ROOT)}: expected 3–8 keyword phrases, found {len(phrases)}")
        normalized = [phrase.casefold() for phrase in phrases]
        if len(normalized) != len(set(normalized)):
            errors.append(f"{path.relative_to(ROOT)}: duplicate keyword phrase")

        if path.parent.name in DESCRIPTION_TARGETS:
            descriptions = parser.values["description"]
            if len(descriptions) != 1:
                errors.append(
                    f"{path.relative_to(ROOT)}: expected one description tag, found {len(descriptions)}"
                )
            elif not 120 <= len(descriptions[0].strip()) <= 160:
                errors.append(
                    f"{path.relative_to(ROOT)}: expected 120–160 description characters, "
                    f"found {len(descriptions[0].strip())}"
                )

    if errors:
        print("FAIL — book keyword metadata verifier")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"PASS — {len(pages)} book pages each have one populated keyword tag "
        f"({min(counts)}–{max(counts)} phrases); {len(DESCRIPTION_TARGETS)} curated descriptions pass"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
