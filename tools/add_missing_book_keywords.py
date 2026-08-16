#!/usr/bin/env python3
"""Add curated meta-keywords to book pages that lack them."""
from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYWORDS = {
    "week-25-la-cocina-de-abuela": "Spanish books for kids, learn Spanish preschool, cooking vocabulary Spanish, kitchen words for children, bilingual preschool books",
    "week-28-la-orquesta": "Spanish books for kids, learn Spanish preschool, musical instruments Spanish, animal orchestra for children, bilingual preschool books",
    "week-29-las-partes-del-cuerpo": "Spanish books for kids, learn Spanish preschool, body parts Spanish, human body vocabulary for children, bilingual preschool books",
    "week-30-los-colores": "Spanish books for kids, learn Spanish preschool, colors in Spanish, color vocabulary for children, bilingual preschool books",
    "week-32-los-numeros": "Spanish books for kids, learn Spanish preschool, numbers in Spanish, Spanish counting for children, bilingual preschool books",
    "week-33-las-emociones": "Spanish books for kids, learn Spanish preschool, emotions in Spanish, feelings vocabulary for children, bilingual preschool books",
    "week-36-las-estaciones": "Spanish books for kids, learn Spanish preschool, seasons in Spanish, weather vocabulary for children, bilingual preschool books",
    "week-39-las-frutas": "Spanish books for kids, learn Spanish preschool, fruits in Spanish, food vocabulary for children, bilingual preschool books",
    "week-41-la-familia": "Spanish books for kids, learn Spanish preschool, family vocabulary Spanish, family members for children, bilingual preschool books",
    "week-42-el-salon-de-clase": "Spanish books for kids, learn Spanish preschool, classroom vocabulary Spanish, school words for children, bilingual preschool books",
    "week-43-los-deportes": "Spanish books for kids, learn Spanish preschool, sports in Spanish, sports vocabulary for children, bilingual preschool books",
    "week-45-las-profesiones": "Spanish books for kids, learn Spanish preschool, professions in Spanish, community jobs for children, bilingual preschool books",
    "week-50-los-insectos": "Spanish books for kids, learn Spanish preschool, insects in Spanish, bug vocabulary for children, bilingual preschool books",
    "week-51-las-maravillas-del-mar": "Spanish books for kids, learn Spanish preschool, ocean animals Spanish, sea life for children, bilingual preschool books",
    "week-52-el-viaje-de-los-pajaros": "Spanish books for kids, learn Spanish preschool, birds in Spanish, bird migration for children, bilingual preschool books",
    "week-54-los-amigos-de-la-comunidad": "Spanish books for kids, learn Spanish preschool, community helpers Spanish, neighborhood jobs for children, bilingual preschool books",
    "week-56-las-formas-geometricas": "Spanish books for kids, learn Spanish preschool, shapes in Spanish, geometry vocabulary for children, bilingual preschool books",
    "week-57-la-primavera-y-las-flores": "Spanish books for kids, learn Spanish preschool, spring vocabulary Spanish, flowers in Spanish for children, bilingual preschool books",
    "week-58-el-dia-y-la-noche": "Spanish books for kids, learn Spanish preschool, day and night Spanish, time vocabulary for children, bilingual preschool books",
    "week-59-los-sentidos": "Spanish books for kids, learn Spanish preschool, five senses Spanish, senses vocabulary for children, bilingual preschool books",
    "week-60-el-ciclo-del-agua": "Spanish books for kids, learn Spanish preschool, water cycle Spanish, science vocabulary for children, bilingual preschool books",
    "week-61-las-emociones": "Spanish books for kids, learn Spanish preschool, emotions in Spanish, social emotional vocabulary, bilingual preschool books",
    "week-62-los-instrumentos-musicales": "Spanish books for kids, learn Spanish preschool, musical instruments Spanish, music vocabulary for children, bilingual preschool books",
    "week-63-la-granja-y-sus-animales": "Spanish books for kids, learn Spanish preschool, farm animals Spanish, farm vocabulary for children, bilingual preschool books",
    "week-64-el-parque-de-juegos": "Spanish books for kids, learn Spanish preschool, playground vocabulary Spanish, outdoor play for children, bilingual preschool books",
    "week-68-las-abejas-y-el-jardin": "Spanish books for kids, learn Spanish preschool, bees in Spanish, garden vocabulary for children, bilingual preschool books",
    "week-70-el-reino-submarino": "Spanish books for kids, learn Spanish preschool, underwater animals Spanish, ocean vocabulary for children, bilingual preschool books",
    "week-71-el-viaje-espacial": "Spanish books for kids, learn Spanish preschool, space vocabulary Spanish, planets and rockets for children, bilingual preschool books",
    "week-73-el-clima": "Spanish books for kids, learn Spanish preschool, weather in Spanish, climate vocabulary for children, bilingual preschool books",
}
TITLE_RE = re.compile(r'^(?P<indent>\s*)<title>.*?</title>\s*$', re.I | re.M)
DESCRIPTION_RE = re.compile(r'^(?P<indent>\s*)<meta\s+name=["\']description["\'][^>]*>\s*$', re.I | re.M)


class KeywordMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.values: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "meta" and values.get("name", "").lower() == "keywords":
            self.values.append(values.get("content", ""))


def keyword_values(text: str) -> list[str]:
    parser = KeywordMetaParser()
    parser.feed(text)
    return parser.values


def add_keywords(text: str, slug: str, path: Path) -> tuple[str, bool]:
    matches = keyword_values(text)
    if matches:
        if len(matches) != 1 or not matches[0].strip():
            raise RuntimeError(f"{path}: malformed or duplicate keyword metadata")
        return text, False
    if slug not in KEYWORDS:
        raise RuntimeError(f"{path}: missing curated keyword mapping")

    anchors = list(DESCRIPTION_RE.finditer(text)) or list(TITLE_RE.finditer(text))
    if len(anchors) != 1:
        raise RuntimeError(f"{path}: expected one title/description insertion anchor, found {len(anchors)}")
    anchor = anchors[0]
    indent = anchor.group("indent")
    tag = f'{indent}<meta name="keywords" content="{KEYWORDS[slug]}">'
    return text[: anchor.end()] + "\n" + tag + text[anchor.end() :], True


def plan_changes(pages: list[Path]) -> list[tuple[Path, str]]:
    """Preflight every page before writing any page."""
    planned: list[tuple[Path, str]] = []
    for path in pages:
        original = path.read_text(encoding="utf-8")
        updated, needed = add_keywords(original, path.parent.name, path)
        if needed:
            planned.append((path, updated))
    return planned


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if any book page lacks keywords")
    args = parser.parse_args()

    pages = sorted(ROOT.glob("books/week-*/index.html"))
    if not pages:
        raise SystemExit("No book pages found")

    planned = plan_changes(pages)

    if args.check and planned:
        print(f"FAIL — {len(planned)} of {len(pages)} book pages still lack keyword metadata")
        return 1
    if not args.check:
        for path, updated in planned:
            path.write_text(updated, encoding="utf-8")

    action = "would change" if args.check else "changed"
    print(f"PASS — {action} {len(planned)} of {len(pages)} book pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
