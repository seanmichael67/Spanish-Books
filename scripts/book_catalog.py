#!/usr/bin/env python3
"""Canonical ready-book catalog and WordPress renderers for Beibei.

The catalog is intentionally fail-closed:
- modern readers must be explicitly marked ``ready: true`` in server.js;
- the older self-contained readers must match an exact reviewed allowlist;
- source-folder counts and draft counts must match the audited repository.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

EXPECTED_SOURCE_COUNT = 172
BASELINE_MODERN_READY_COUNT = 106
EXPECTED_MODERN_SOURCE_COUNT = 136
ASSET_INCOMPLETE_COUNT = 30

LEGACY_READY_FOLDERS = (
    "week-25-la-cocina-de-abuela",
    "week-26-la-granja",
    "week-27-el-viaje-de-pepito",
    "week-28-la-orquesta",
    "week-29-las-partes-del-cuerpo",
    "week-30-los-colores",
    "week-31-la-ropa",
    "week-32-los-numeros",
    "week-33-las-emociones",
    "week-34-los-vehiculos",
    "week-35-los-animales-del-zoologico",
    "week-36-las-estaciones",
    "week-38-el-jardin",
    "week-39-las-frutas",
    "week-40-la-musica",
    "week-41-la-familia",
    "week-42-el-salon-de-clase",
    "week-43-los-deportes",
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
)

SIMPLE_SLUG_OWNER_OVERRIDES = {
    # The current live /las-emociones/ page already represents week 61.
    "las-emociones": "week-61-las-emociones",
}

READER_URL_OVERRIDES = {
    # The reviewed promo-free commit is mirrored first-party because the
    # GitHub Pages main reader still contains a not-parent-ready tutor card.
    # The mirror is noindex and canonicalizes to the WordPress wrapper.
    "week-71-la-familia": "https://www.beibeiamigos.com/wp-content/uploads/spanish-books/week-71-la-familia/",
}

SERVER_BOOK_RE = re.compile(
    r"\{\s*slug:\s*'(?P<slug>[^']+)',\s*"
    r"emoji:\s*'(?P<emoji>[^']*)',\s*"
    r"week:\s*(?P<week>\d+),\s*"
    r"title:\s*'(?P<title>[^']*)',\s*"
    r"subtitle:\s*'(?P<subtitle>[^']*)',\s*"
    r"theme:\s*'(?P<theme>[^']*)',\s*"
    r"ready:\s*(?P<ready>true|false)\s*\}"
)
SOURCE_RE = re.compile(r"week-\d+-[a-z0-9-]+")
SOURCE_MARKER_RE = re.compile(r"spanish-book-source:(week-\d+-[a-z0-9-]+)")


@dataclass(frozen=True)
class Book:
    source_slug: str
    wp_slug: str
    week: int
    title: str
    subtitle: str
    emoji: str
    theme: str
    description: str
    keywords: tuple[str, ...]
    learning_points: tuple[str, ...]
    vocabulary: tuple[tuple[str, str], ...]
    kind: str

    @property
    def reader_url(self) -> str:
        return READER_URL_OVERRIDES.get(
            self.source_slug,
            f"https://seanmichael67.github.io/Spanish-Books/books/{self.source_slug}/",
        )

    @property
    def wordpress_url(self) -> str:
        return f"https://www.beibeiamigos.com/spanish-books/{self.wp_slug}/"

    @property
    def wordpress_title(self) -> str:
        title = self.title
        if self.subtitle and self.subtitle.casefold() != self.title.casefold():
            title = f"{title} — {self.subtitle}"
        if self.wp_slug.endswith(f"-semana-{self.week}"):
            title += f" (Semana {self.week})"
        return f"{self.emoji} {title}".strip()


@dataclass(frozen=True)
class Catalog:
    ready: tuple[Book, ...]
    modern_ready: tuple[Book, ...]
    legacy_ready: tuple[Book, ...]
    all_source_folders: tuple[str, ...]
    asset_incomplete: tuple[str, ...]

    @property
    def ready_slugs(self) -> tuple[str, ...]:
        return tuple(book.source_slug for book in self.ready)


@dataclass(frozen=True)
class Reconciliation:
    represented: tuple[Book, ...]
    missing: tuple[Book, ...]
    unexpected_pages: list[dict[str, object]]
    source_to_page: dict[str, dict[str, object]]


def _strip_tags(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return " ".join(html.unescape(value).split())


def _first(raw: str, patterns: Sequence[str], default: str = "") -> str:
    for pattern in patterns:
        match = re.search(pattern, raw, flags=re.I | re.S)
        if match:
            value = _strip_tags(match.group(1))
            if value:
                return value
    return default


def _meta(raw: str, name: str) -> str:
    escaped = re.escape(name)
    patterns = (
        rf'<meta\s+[^>]*name=["\']{escaped}["\'][^>]*content=["\']([^"\']*)["\'][^>]*>',
        rf'<meta\s+[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']{escaped}["\'][^>]*>',
    )
    return _first(raw, patterns)


def _source_week(source_slug: str) -> int:
    match = re.fullmatch(r"week-(\d+)-[a-z0-9-]+", source_slug)
    if not match:
        raise ValueError(f"invalid source folder: {source_slug}")
    return int(match.group(1))


def tail_slug(source_slug: str) -> str:
    return re.sub(r"^week-\d+-", "", source_slug)


def _theme_for(source_slug: str) -> str:
    slug = tail_slug(source_slug)
    rules = (
        (("familia", "emocion", "amigos", "comunidad"), "familia"),
        (("granja", "animales", "pajaros", "insectos", "abejas", "mar"), "animales"),
        (("cocina", "frutas"), "comida"),
        (("musica", "orquesta", "instrumentos"), "musica"),
        (("cuerpo", "sentidos"), "cuerpo"),
        (("colores", "formas"), "colores"),
        (("numeros",), "numeros"),
        (("vehiculos", "viaje-espacial"), "transporte"),
        (("estaciones", "jardin", "primavera", "clima", "agua", "dia-y-la-noche"), "naturaleza"),
        (("ropa", "salon-de-clase", "deportes", "profesiones", "parque"), "mundo"),
    )
    for needles, theme in rules:
        if any(needle in slug for needle in needles):
            return theme
    return "mundo"


def _legacy_metadata(source_slug: str, raw: str) -> dict[str, object]:
    title = _first(
        raw,
        (
            r'<div\s+class=["\'][^"\']*title-page[^"\']*["\'][^>]*>.*?<h1[^>]*>(.*?)</h1>',
            r"<h1[^>]*>(.*?)</h1>",
            r"<title[^>]*>(.*?)</title>",
        ),
        tail_slug(source_slug).replace("-", " ").title(),
    )
    title = re.sub(r"\s*[-|]\s*(Spanish Book.*|Learn Spanish.*|Beibei Amigos.*)$", "", title, flags=re.I)
    subtitle = _first(
        raw,
        (
            r'<(?:div|p)\s+class=["\'][^"\']*subtitle[^"\']*["\'][^>]*>(.*?)</(?:div|p)>',
            r'<p\s+class=["\'][^"\']*translation[^"\']*["\'][^>]*>(.*?)</p>',
        ),
        "Interactive Spanish Book",
    )
    emoji = _first(
        raw,
        (r'<(?:div|span)\s+class=["\'][^"\']*emoji[^"\']*["\'][^>]*>(.*?)</(?:div|span)>',),
        "📚",
    )
    if len(emoji) > 16 or re.search(r"[A-Za-z]", emoji):
        emoji = "📚"
    description = _meta(raw, "description") or f"Free interactive Spanish book about {title} for preschool learners."
    keyword_text = _meta(raw, "keywords")
    keywords = tuple(item.strip() for item in keyword_text.split(",") if item.strip())

    spanish = [_strip_tags(v) for v in re.findall(r'<p\s+class=["\'][^"\']*story-text[^"\']*["\'][^>]*>(.*?)</p>', raw, flags=re.I | re.S)]
    english = [_strip_tags(v) for v in re.findall(r'<p\s+class=["\'][^"\']*translation[^"\']*["\'][^>]*>(.*?)</p>', raw, flags=re.I | re.S)]
    points: list[str] = []
    vocabulary: list[tuple[str, str]] = []
    for index, text in enumerate(spanish):
        if text and text not in points:
            points.append(text)
        if index < len(english) and text and english[index]:
            vocabulary.append((text, english[index]))
    return {
        "title": title,
        "subtitle": subtitle,
        "emoji": emoji,
        "theme": _theme_for(source_slug),
        "description": description,
        "keywords": keywords,
        "learning_points": tuple(points[:6]),
        "vocabulary": tuple(vocabulary[:8]),
    }


def _modern_metadata(raw: str, server: dict[str, object]) -> dict[str, object]:
    description = _meta(raw, "description") or (
        f"Free interactive Spanish book about {server['title']} for preschool learners ages 2–5."
    )
    keyword_text = _meta(raw, "keywords")
    keywords = tuple(item.strip() for item in keyword_text.split(",") if item.strip())
    pairs = re.findall(
        r'"title"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"\s*,\s*"footer"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"',
        raw,
        flags=re.S,
    )
    learning: list[str] = []
    for title, footer in pairs:
        title = bytes(title, "utf-8").decode("unicode_escape") if "\\" in title else title
        footer = bytes(footer, "utf-8").decode("unicode_escape") if "\\" in footer else footer
        if title not in {server["title"], "Mis Palabras", "¡Ganaste tu insignia!"}:
            learning.append(f"{title} — {footer}")
    vocab = [
        (es, en)
        for es, en in re.findall(
            r'"es"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"\s*,\s*"en"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"',
            raw,
        )
    ]
    return {
        "title": str(server["title"]),
        "subtitle": str(server["subtitle"]),
        "emoji": str(server["emoji"]),
        "theme": str(server["theme"]),
        "description": description,
        "keywords": keywords,
        "learning_points": tuple(learning[:6]),
        "vocabulary": tuple(vocab[:10]),
    }


def _wp_slug_map(source_slugs: Iterable[str]) -> dict[str, str]:
    groups: dict[str, list[str]] = {}
    for source_slug in source_slugs:
        groups.setdefault(tail_slug(source_slug), []).append(source_slug)
    result: dict[str, str] = {}
    for tail, sources in groups.items():
        sources.sort(key=lambda item: (_source_week(item), item))
        owner = SIMPLE_SLUG_OWNER_OVERRIDES.get(tail, sources[0])
        if owner not in sources:
            raise ValueError(f"slug-owner override {owner} is absent for {tail}")
        for source_slug in sources:
            result[source_slug] = tail if source_slug == owner else f"{tail}-semana-{_source_week(source_slug)}"
    if len(set(result.values())) != len(result):
        raise ValueError("WordPress slug mapping is not unique")
    return result


def load_catalog(root: Path) -> Catalog:
    root = root.resolve()
    source_files = sorted((root / "books").glob("week-*/index.html"))
    all_sources = tuple(path.parent.name for path in source_files)
    if len(all_sources) != EXPECTED_SOURCE_COUNT or len(set(all_sources)) != EXPECTED_SOURCE_COUNT:
        raise ValueError(
            f"source inventory drift: expected {EXPECTED_SOURCE_COUNT}, found {len(all_sources)} "
            f"({len(set(all_sources))} unique)"
        )

    server_raw = (root / "server.js").read_text(encoding="utf-8")
    server_rows: dict[str, dict[str, object]] = {}
    for match in SERVER_BOOK_RE.finditer(server_raw):
        row: dict[str, object] = match.groupdict()
        row["week"] = int(str(row["week"]))
        row["ready"] = row["ready"] == "true"
        server_rows[str(row["slug"])] = row
    modern_ready_sources = tuple(sorted(slug for slug, row in server_rows.items() if row["ready"]))

    raw_by_source = {path.parent.name: path.read_text(encoding="utf-8") for path in source_files}
    detected_legacy = tuple(sorted(slug for slug, raw in raw_by_source.items() if "const Icons" not in raw))
    if detected_legacy != tuple(sorted(LEGACY_READY_FOLDERS)):
        missing = sorted(set(LEGACY_READY_FOLDERS) - set(detected_legacy))
        extra = sorted(set(detected_legacy) - set(LEGACY_READY_FOLDERS))
        raise ValueError(f"legacy allowlist drift: missing={missing}, extra={extra}")
    detected_modern = tuple(sorted(set(all_sources) - set(detected_legacy)))
    if len(detected_modern) != EXPECTED_MODERN_SOURCE_COUNT:
        raise ValueError(
            f"modern source inventory drift: expected {EXPECTED_MODERN_SOURCE_COUNT}, found {len(detected_modern)}"
        )
    if not set(modern_ready_sources) <= set(detected_modern):
        raise ValueError("server.js marks a missing or non-modern source ready")
    if not (BASELINE_MODERN_READY_COUNT <= len(modern_ready_sources) <= EXPECTED_MODERN_SOURCE_COUNT):
        raise ValueError(
            f"modern-ready inventory regressed or overflowed: baseline {BASELINE_MODERN_READY_COUNT}, "
            f"capacity {EXPECTED_MODERN_SOURCE_COUNT}, found {len(modern_ready_sources)}"
        )

    ready_sources = tuple(sorted(set(modern_ready_sources) | set(LEGACY_READY_FOLDERS)))
    if not set(ready_sources) <= set(all_sources):
        raise ValueError("ready catalog references missing source folders")
    asset_incomplete = tuple(sorted(set(detected_modern) - set(modern_ready_sources)))
    if len(asset_incomplete) != EXPECTED_MODERN_SOURCE_COUNT - len(modern_ready_sources):
        raise ValueError("asset-incomplete modern inventory is inconsistent")

    wp_slugs = _wp_slug_map(all_sources)
    books: list[Book] = []
    for source_slug in ready_sources:
        raw = raw_by_source[source_slug]
        if source_slug in server_rows and server_rows[source_slug]["ready"]:
            metadata = _modern_metadata(raw, server_rows[source_slug])
            kind = "modern"
        elif source_slug in LEGACY_READY_FOLDERS:
            metadata = _legacy_metadata(source_slug, raw)
            kind = "legacy"
        else:
            raise ValueError(f"unclassified ready source: {source_slug}")
        books.append(Book(
            source_slug=source_slug,
            wp_slug=wp_slugs[source_slug],
            week=_source_week(source_slug),
            title=str(metadata["title"]),
            subtitle=str(metadata["subtitle"]),
            emoji=str(metadata["emoji"]),
            theme=str(metadata["theme"]),
            description=str(metadata["description"]),
            keywords=tuple(metadata["keywords"]),
            learning_points=tuple(metadata["learning_points"]),
            vocabulary=tuple(metadata["vocabulary"]),
            kind=kind,
        ))

    books.sort(key=lambda book: (book.week, book.source_slug))
    modern = tuple(book for book in books if book.kind == "modern")
    legacy = tuple(book for book in books if book.kind == "legacy")
    if len(modern) != len(modern_ready_sources) or len(legacy) != len(LEGACY_READY_FOLDERS):
        raise ValueError("ready catalog kind counts drifted")
    if len({book.wp_slug for book in books}) != len(books):
        raise ValueError("ready WordPress slugs are not unique")
    return Catalog(tuple(books), modern, legacy, all_sources, asset_incomplete)


def catalog_fingerprint(books: Sequence[Book]) -> str:
    payload = [
        {
            "source": book.source_slug,
            "wp": book.wp_slug,
            "week": book.week,
            "title": book.title,
            "subtitle": book.subtitle,
            "emoji": book.emoji,
            "theme": book.theme,
            "description": book.description,
        }
        for book in books
    ]
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()[:16]


def source_identity(content: str) -> str | None:
    marker = SOURCE_MARKER_RE.search(content)
    if marker:
        return marker.group(1)
    sources = sorted(set(SOURCE_RE.findall(content)))
    if len(sources) > 1:
        raise ValueError(f"page references multiple source folders: {sources}")
    return sources[0] if sources else None


def reconcile_wordpress_pages(books: Sequence[Book], pages: Sequence[dict[str, object]]) -> Reconciliation:
    by_source = {book.source_slug: book for book in books}
    by_wp_slug = {book.wp_slug: book for book in books}
    tail_counts: dict[str, int] = {}
    for book in books:
        tail = tail_slug(book.source_slug)
        tail_counts[tail] = tail_counts.get(tail, 0) + 1
    source_to_page: dict[str, dict[str, object]] = {}
    unexpected: list[dict[str, object]] = []

    for page in pages:
        content = str(page.get("post_content") or "")
        source = source_identity(content)
        post_slug = str(page.get("post_name") or "")
        # Six historical wrappers do not include a week-* source URL. Permit
        # slug-only recovery only when the catalog tail itself is unambiguous.
        # Collision pages must carry an explicit source marker/URL.
        if source is None and post_slug in by_wp_slug:
            candidate = by_wp_slug[post_slug]
            candidate_tail = tail_slug(candidate.source_slug)
            if post_slug == candidate_tail and tail_counts[candidate_tail] == 1:
                source = candidate.source_slug
        if source is None:
            unexpected.append(dict(page))
            continue
        if source not in by_source:
            raise ValueError(f"WordPress page {page.get('ID')} references unexpected source {source}")
        if source in source_to_page:
            raise ValueError(
                f"source {source} is represented more than once by pages "
                f"{source_to_page[source].get('ID')} and {page.get('ID')}"
            )
        expected_slug = by_source[source].wp_slug
        if post_slug != expected_slug:
            raise ValueError(
                f"WordPress page {page.get('ID')} source {source} has slug {post_slug}; expected {expected_slug}"
            )
        source_to_page[source] = dict(page)

    missing = tuple(book for book in books if book.source_slug not in source_to_page)
    unexpected_slugs = {str(page.get("post_name") or "") for page in unexpected}
    conflicts = sorted(book.wp_slug for book in missing if book.wp_slug in unexpected_slugs)
    if conflicts:
        raise ValueError(f"WordPress slug conflict blocks missing books: {conflicts}")
    represented = tuple(book for book in books if book.source_slug in source_to_page)
    return Reconciliation(represented, missing, unexpected, source_to_page)


def _json_ld(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def render_book_page(book: Book) -> str:
    points = book.learning_points or (f"Explore Spanish vocabulary about {book.title}.",)
    point_items = "".join(f"<li>{html.escape(point)}</li>" for point in points[:6])
    vocab_items = "".join(
        f"<li><strong lang=\"es\">{html.escape(es)}</strong> — {html.escape(en)}</li>"
        for es, en in book.vocabulary[:10]
    )
    if not vocab_items:
        vocab_items = "<li>Listen, repeat, and talk about each page together.</li>"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Book",
                "@id": f"{book.wordpress_url}#book",
                "name": book.title,
                "alternateName": book.subtitle,
                "description": book.description,
                "url": book.wordpress_url,
                "inLanguage": "es",
                "isAccessibleForFree": True,
                "author": {"@type": "Organization", "name": "Beibei Amigos Language Preschool", "url": "https://www.beibeiamigos.com/"},
                "audience": {"@type": "EducationalAudience", "educationalRole": "student", "suggestedMinAge": 2, "suggestedMaxAge": 5},
                "genre": ["Children's Literature", "Educational", "Bilingual"],
                "keywords": list(book.keywords),
            },
            {
                "@type": "LearningResource",
                "@id": f"{book.wordpress_url}#learning-resource",
                "name": f"{book.title} interactive Spanish reader",
                "description": book.description,
                "url": book.wordpress_url,
                "inLanguage": ["es", "en"],
                "learningResourceType": "Interactive book",
                "educationalLevel": "Preschool",
                "isAccessibleForFree": True,
                "about": {"@id": f"{book.wordpress_url}#book"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.beibeiamigos.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Spanish Books", "item": "https://www.beibeiamigos.com/spanish-books/"},
                    {"@type": "ListItem", "position": 3, "name": book.title, "item": book.wordpress_url},
                ],
            },
        ],
    }
    return f'''<!-- spanish-book-source:{book.source_slug} -->
<!-- spanish-book-template:v2 -->
<style>
.bb-reader{{max-width:1180px;margin:0 auto;padding:18px 18px 38px;font-family:"Sour Gummy",system-ui,sans-serif;color:#24324a}}
.bb-reader *{{box-sizing:border-box}}.bb-back{{display:inline-block;margin:0 0 14px;color:#5d4fc4;font-weight:800;text-decoration:none}}
.bb-intro{{text-align:center;max-width:840px;margin:0 auto 22px}}.bb-intro h2{{font-size:clamp(1.35rem,3vw,2rem);margin:.25rem 0;color:#382f75}}
.bb-intro p{{font:500 1.08rem/1.65 system-ui,sans-serif;color:#4b5563}}
.bb-frame{{width:100%;min-height:560px;height:clamp(560px,82vh,900px);border:0;border-radius:20px;box-shadow:0 12px 38px rgba(37,30,89,.18);background:#f5f3ff}}
.bb-learn{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:24px 0}}.bb-panel{{background:#fff;border:1px solid #e6e2ff;border-radius:18px;padding:22px;box-shadow:0 8px 24px rgba(37,30,89,.08)}}
.bb-panel h2{{font-size:1.35rem;color:#493a9a;margin:0 0 10px}}.bb-panel ul{{padding-left:1.25rem;margin:0}}.bb-panel li{{margin:.45rem 0;line-height:1.45}}
.bb-cta{{text-align:center;background:linear-gradient(135deg,#6153d8,#8c4fbc);color:#fff;border-radius:20px;padding:28px 20px}}
.bb-cta h2{{color:#fff;margin:0 0 8px}}.bb-cta a{{display:inline-block;background:#fff;color:#5936a6;text-decoration:none;font-weight:900;padding:12px 22px;border-radius:12px;margin-top:8px}}
@media(max-width:720px){{.bb-reader{{padding:10px 8px 24px}}.bb-frame{{min-height:520px;height:78svh;border-radius:12px}}.bb-learn{{grid-template-columns:1fr}}}}
</style>
<div class="bb-reader">
<a class="bb-back" href="/spanish-books/">← Todos los libros</a>
<section class="bb-intro"><div aria-hidden="true" style="font-size:2.5rem">{html.escape(book.emoji)}</div><h2>Libro interactivo gratis: {html.escape(book.title)}</h2><p>{html.escape(book.description)}</p></section>
<iframe class="bb-frame" src="{html.escape(book.reader_url)}" title="{html.escape(book.title)} — libro interactivo en español" loading="eager" allow="autoplay" referrerpolicy="strict-origin-when-cross-origin"></iframe>
<section class="bb-learn" aria-label="Learning guide"><div class="bb-panel"><h2>Qué aprenderán</h2><ul>{point_items}</ul></div><div class="bb-panel"><h2>Palabras para practicar</h2><ul>{vocab_items}</ul></div></section>
<section class="bb-cta"><h2>Más libros bilingües gratuitos</h2><p>Explore la biblioteca completa de Beibei Amigos para aprender español juntos.</p><a href="/spanish-books/">Ver todos los libros</a></section>
</div>
<script type="application/ld+json">{_json_ld(graph)}</script>'''


def render_hub(books: Sequence[Book]) -> str:
    fingerprint = catalog_fingerprint(books)
    cards = []
    item_list = []
    for position, book in enumerate(books, 1):
        cards.append(
            f'''<!-- spanish-book-source:{book.source_slug} --><a class="bb-book-card" href="{html.escape(book.wordpress_url)}" data-theme="{html.escape(book.theme)}" data-search="{html.escape((book.title + ' ' + book.subtitle).casefold())}"><span class="bb-emoji" aria-hidden="true">{html.escape(book.emoji)}</span><span class="bb-week">Semana {book.week}</span><strong>{html.escape(book.title)}</strong><span>{html.escape(book.subtitle)}</span></a>'''
        )
        item_list.append({
            "@type": "ListItem",
            "position": position,
            "url": book.wordpress_url,
            "name": book.title,
        })
    themes = sorted({book.theme for book in books})
    filters = ['<button type="button" class="active" data-theme="all">Todos</button>'] + [
        f'<button type="button" data-theme="{html.escape(theme)}">{html.escape(theme.replace("-", " ").title())}</button>'
        for theme in themes
    ]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": "https://www.beibeiamigos.com/spanish-books/#collection",
                "url": "https://www.beibeiamigos.com/spanish-books/",
                "name": "Free Interactive Spanish Books for Preschoolers",
                "description": "Free interactive Spanish and bilingual books for preschool children ages 2–5 from Beibei Amigos Language Preschool.",
                "inLanguage": ["en", "es"],
                "isPartOf": {"@type": "WebSite", "url": "https://www.beibeiamigos.com/"},
            },
            {
                "@type": "ItemList",
                "@id": "https://www.beibeiamigos.com/spanish-books/#books",
                "name": "Beibei Amigos Spanish book library",
                "numberOfItems": len(books),
                "itemListElement": item_list,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.beibeiamigos.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Spanish Books", "item": "https://www.beibeiamigos.com/spanish-books/"},
                ],
            },
        ],
    }
    return f'''<!-- spanish-books-catalog:{fingerprint} -->
<!-- spanish-books-hub-template:v2 -->
<style>
.bb-library{{max-width:1280px;margin:0 auto;padding:28px 20px 46px;font-family:"Sour Gummy",system-ui,sans-serif;color:#24324a}}
.bb-library *{{box-sizing:border-box}}.bb-hero{{text-align:center;background:linear-gradient(135deg,#6357d9,#894fc2);color:#fff;padding:38px 22px;border-radius:24px;margin-bottom:22px;box-shadow:0 14px 40px rgba(59,42,126,.2)}}
.bb-hero h2{{color:#fff;font-size:clamp(2rem,5vw,3.5rem);margin:0 0 8px}}.bb-hero p{{font:500 clamp(1rem,2vw,1.2rem)/1.55 system-ui,sans-serif;max-width:820px;margin:0 auto}}
.bb-count{{display:inline-block;margin-top:14px;background:rgba(255,255,255,.18);padding:8px 14px;border-radius:999px;font-weight:800}}
.bb-tools{{display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap;margin:18px 0}}.bb-search{{width:min(480px,100%);padding:13px 16px;border:2px solid #d9d3ff;border-radius:14px;font:600 1rem system-ui,sans-serif}}
.bb-filters{{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:22px}}.bb-filters button{{border:1px solid #d9d3ff;background:#fff;color:#493a9a;border-radius:999px;padding:8px 13px;font-weight:800;cursor:pointer}}
.bb-filters button.active,.bb-filters button:hover{{background:#5d4fc4;color:#fff;border-color:#5d4fc4}}.bb-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}}
.bb-book-card{{display:flex;min-height:190px;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:18px 14px;border-radius:18px;text-decoration:none;background:#fff;border:1px solid #ebe8ff;box-shadow:0 7px 24px rgba(51,42,110,.1);transition:.18s ease;color:#29324a}}
.bb-book-card:hover{{transform:translateY(-4px);box-shadow:0 13px 30px rgba(51,42,110,.18)}}.bb-emoji{{font-size:2.7rem;line-height:1.1;margin-bottom:6px}}.bb-week{{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:#7469b5;font-weight:800}}
.bb-book-card strong{{font-size:1.14rem;color:#382f75;margin:6px 0 2px}}.bb-book-card>span:last-child{{font:500 .92rem/1.3 system-ui,sans-serif;color:#667085}}.bb-empty{{display:none;text-align:center;padding:35px;font-weight:800;color:#6b628d}}
@media(max-width:980px){{.bb-grid{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}@media(max-width:720px){{.bb-library{{padding:16px 10px 30px}}.bb-grid{{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}}.bb-book-card{{min-height:165px;padding:13px 8px}}}}
@media(max-width:390px){{.bb-grid{{grid-template-columns:1fr}}}}
</style>
<div class="bb-library">
<header class="bb-hero"><h2>Libros de español gratis</h2><p>Lea, escuche y aprenda con libros interactivos bilingües para niños de 2 a 5 años.</p><span class="bb-count">{len(books)} libros disponibles</span></header>
<div class="bb-tools"><label for="bb-book-search" class="screen-reader-text">Buscar libros</label><input id="bb-book-search" class="bb-search" type="search" placeholder="Buscar un libro…" autocomplete="off"></div>
<nav class="bb-filters" aria-label="Temas">{''.join(filters)}</nav>
<div id="bb-book-grid" class="bb-grid">{''.join(cards)}</div><p id="bb-empty" class="bb-empty">No encontramos libros con esa búsqueda.</p>
</div>
<script>(function(){{const q=document.getElementById('bb-book-search'),buttons=[...document.querySelectorAll('.bb-filters button')],cards=[...document.querySelectorAll('.bb-book-card')],empty=document.getElementById('bb-empty');let theme='all';function apply(){{const text=(q.value||'').trim().toLocaleLowerCase('es');let shown=0;cards.forEach(card=>{{const okTheme=theme==='all'||card.dataset.theme===theme;const okText=!text||card.dataset.search.includes(text);const show=okTheme&&okText;card.hidden=!show;if(show)shown++;}});empty.style.display=shown?'none':'block';}}q.addEventListener('input',apply);buttons.forEach(button=>button.addEventListener('click',()=>{{theme=button.dataset.theme;buttons.forEach(item=>item.classList.toggle('active',item===button));apply();}}));apply();}})();</script>
<script type="application/ld+json">{_json_ld(graph)}</script>'''
