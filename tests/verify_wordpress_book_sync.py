#!/usr/bin/env python3
"""Offline contract tests for the Beibei WordPress book sync."""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from book_catalog import (  # noqa: E402
    ASSET_INCOMPLETE_COUNT,
    EXPECTED_SOURCE_COUNT,
    LEGACY_READY_FOLDERS,
    Book,
    catalog_fingerprint,
    load_catalog,
    reconcile_wordpress_pages,
    render_book_page,
    render_hub,
)
from sync_wordpress_books import (  # noqa: E402
    book_apply_row,
    build_apply_php,
    build_payload,
    inventory_matches_before,
    verify_target_state,
)


def fake_wp_page(book: Book, page_id: int) -> dict[str, object]:
    return {
        "ID": page_id,
        "post_name": book.wp_slug,
        "post_status": "publish",
        "post_title": book.wordpress_title,
        "post_content": f"<!-- spanish-book-source:{book.source_slug} -->",
    }


def exact_wp_page(book: Book, page_id: int) -> dict[str, object]:
    return {
        "ID": page_id,
        "post_name": book.wp_slug,
        "post_status": "publish",
        "post_title": book.wordpress_title,
        "post_excerpt": book.description,
        "post_content": render_book_page(book),
        "post_modified_gmt": "2026-08-16 22:00:00",
        "layout": "et_no_sidebar",
        "builder": "off",
    }


def main() -> None:
    catalog = load_catalog(ROOT)
    assert len(catalog.ready) == 142
    assert len(catalog.modern_ready) == 106
    assert len(catalog.legacy_ready) == 36
    assert len(LEGACY_READY_FOLDERS) == 36
    assert len(catalog.all_source_folders) == EXPECTED_SOURCE_COUNT == 172
    assert len(catalog.asset_incomplete) == ASSET_INCOMPLETE_COUNT == 30
    assert not set(catalog.ready_slugs) & set(catalog.asset_incomplete)

    # The current 106/30 split is a baseline, not a frozen ceiling. A newly
    # completed planned modern reader is accepted and decreases the gated set;
    # a regression below the reviewed baseline still fails closed.
    server_raw = (ROOT / "server.js").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        (tmp_root / "books").symlink_to(ROOT / "books", target_is_directory=True)
        future_entry = (
            "  { slug: 'week-98-cantar', emoji: '🎤', week: 98, title: 'Cantar', "
            "subtitle: 'Singing', theme: 'musica', ready: true },\n"
        )
        (tmp_root / "server.js").write_text(
            server_raw.replace("\n];", f"\n{future_entry}];", 1), encoding="utf-8"
        )
        future_catalog = load_catalog(tmp_root)
        assert len(future_catalog.modern_ready) == 107
        assert len(future_catalog.ready) == 143
        assert len(future_catalog.asset_incomplete) == 29
        assert "week-98-cantar" in future_catalog.ready_slugs

        first_entry = re.search(r"^  \{ slug: '[^\n]+ready: true \},\n", server_raw, re.M)
        assert first_entry
        (tmp_root / "server.js").write_text(
            server_raw[: first_entry.start()] + server_raw[first_entry.end() :], encoding="utf-8"
        )
        try:
            load_catalog(tmp_root)
        except ValueError as exc:
            assert "regressed" in str(exc)
        else:
            raise AssertionError("modern-ready regression below baseline did not fail closed")

    by_source = {book.source_slug: book for book in catalog.ready}
    expected_collision_slugs = {
        "week-33-las-emociones": "las-emociones-semana-33",
        "week-61-las-emociones": "las-emociones",
        "week-41-la-familia": "la-familia",
        "week-71-la-familia": "la-familia-semana-71",
    }
    for source, wp_slug in expected_collision_slugs.items():
        assert by_source[source].wp_slug == wp_slug, (source, by_source[source].wp_slug)

    # Every ready source receives exactly one unique WordPress slug.
    assert len({book.wp_slug for book in catalog.ready}) == 142
    assert by_source["week-71-la-familia"].reader_url == (
        "https://www.beibeiamigos.com/wp-content/uploads/spanish-books/week-71-la-familia/"
    )
    assert all(
        book.reader_url.startswith("https://seanmichael67.github.io/Spanish-Books/books/week-")
        for book in catalog.ready
        if book.source_slug != "week-71-la-familia"
    )

    # A synthetic live inventory missing only the two known collision pages
    # must reconcile to exactly those two sources, with no updates/deletions.
    missing_sources = {"week-33-las-emociones", "week-71-la-familia"}
    rows = [
        fake_wp_page(book, 1000 + index)
        for index, book in enumerate(catalog.ready)
        if book.source_slug not in missing_sources
    ]
    reconciliation = reconcile_wordpress_pages(catalog.ready, rows)
    assert {book.source_slug for book in reconciliation.missing} == missing_sources
    assert reconciliation.unexpected_pages == []
    assert len(reconciliation.represented) == 140

    # Duplicate source markers, unexpected source identities and slug conflicts
    # fail closed instead of overwriting or silently making a duplicate.
    duplicate_rows = rows + [dict(rows[0], ID=9999, post_name="duplicate-source")]
    try:
        reconcile_wordpress_pages(catalog.ready, duplicate_rows)
    except ValueError as exc:
        assert "represented more than once" in str(exc)
    else:
        raise AssertionError("duplicate source identity did not fail closed")

    conflict_rows = rows + [{
        "ID": 9998,
        "post_name": "la-familia-semana-71",
        "post_status": "publish",
        "post_title": "Unrelated page",
        "post_content": "<!-- no source marker -->",
    }]
    try:
        reconcile_wordpress_pages(catalog.ready, conflict_rows)
    except ValueError as exc:
        assert "slug conflict" in str(exc)
    else:
        raise AssertionError("WordPress slug conflict did not fail closed")

    # The hub is crawlable inline content, contains every ready book once,
    # carries deterministic provenance, and never promotes Sophia/Sofia.
    hub = render_hub(catalog.ready)
    assert hub.count('class="bb-book-card"') == 142
    assert hub.count("spanish-book-source:") == 142
    assert f"spanish-books-catalog:{catalog_fingerprint(catalog.ready)}" in hub
    assert "<iframe" not in hub
    assert not re.search(r"tutti[-_.]?sophia|sofia-fullscreen|AI Spanish Teacher|real AI tutor", hub, re.I)
    assert '"@type":"ItemList"' in hub
    assert '"numberOfItems":142' in hub

    # New page shells are source-identified, canonicalized to WordPress,
    # expose crawlable learning copy/schema, and contain no unready tutor promo.
    for source in sorted(missing_sources):
        book = by_source[source]
        page = render_book_page(book)
        assert f"spanish-book-source:{source}" in page
        assert book.reader_url in page
        assert book.wordpress_url in page
        assert '"@type":"Book"' in page
        assert '"@type":"LearningResource"' in page
        assert "<iframe" in page
        assert not re.search(r"tutti[-_.]?sophia|sofia-fullscreen|AI Spanish Teacher|real AI tutor", page, re.I)

    # The server-side apply is one InnoDB transaction guarded by a named lock
    # and row locks. Exact generated content and Divi metadata are checked both
    # before commit and again from a fresh inventory after commit.
    planned_books = tuple(by_source[source] for source in sorted(missing_sources))
    before_rows = [
        exact_wp_page(book, 2000 + index)
        for index, book in enumerate(catalog.ready)
        if book.source_slug not in missing_sources
    ]
    before_inventory = {
        "hub": {
            "ID": 1854,
            "post_name": "spanish-books",
            "post_status": "publish",
            "post_title": "Spanish Books",
            "post_excerpt": "old excerpt",
            "post_content": "old hub content",
            "post_modified_gmt": "2026-08-16 21:00:00",
            "layout": "et_no_sidebar",
            "builder": "off",
        },
        "pages": before_rows,
        "table_engines": {"wp_posts": "InnoDB", "wp_postmeta": "InnoDB"},
    }
    payload = build_payload(before_inventory, catalog, planned_books, hub)
    apply_php = build_apply_php(payload)
    for required_php_guard in (
        "GET_LOCK(%s, 0)",
        "gzuncompress(base64_decode(",
        "START TRANSACTION",
        "FOR UPDATE",
        "exact_page_readback",
        "post_content_sha256",
        "_et_pb_use_builder",
        "_et_pb_page_layout",
        "COMMIT",
        "ROLLBACK",
        "RELEASE_LOCK(%s)",
    ):
        assert required_php_guard in apply_php, required_php_guard
    assert apply_php.index("GET_LOCK(%s, 0)") < apply_php.index("START TRANSACTION")
    assert apply_php.index("exact_page_readback") < apply_php.index("COMMIT")
    assert len(apply_php.encode("utf-8")) < 50_000  # HostGator silently skips oversized wp eval-file programs.
    assert all(row["post_content_sha256"] == book_apply_row(book)["post_content_sha256"]
               for row, book in zip(payload["create"], planned_books))

    target_rows = [exact_wp_page(book, 3000 + index) for index, book in enumerate(catalog.ready)]
    target_inventory = {
        "hub": {
            "ID": 1854,
            "post_name": "spanish-books",
            "post_status": "publish",
            "post_title": "Spanish Books",
            "post_excerpt": "142 free interactive Spanish and bilingual books for preschool children ages 2–5.",
            "post_content": hub,
            "post_modified_gmt": "2026-08-16 22:00:00",
            "layout": "et_no_sidebar",
            "builder": "off",
        },
        "pages": target_rows,
        "table_engines": {"wp_posts": "InnoDB", "wp_postmeta": "InnoDB"},
    }
    target_by_source: dict[str, dict[str, object]] = {}
    for page in target_rows:
        marker = re.search(r"spanish-book-source:([^ ]+)", str(page["post_content"]))
        assert marker
        target_by_source[marker.group(1)] = page
    committed_rows = [
        {
            "ID": int(str(target_by_source[book.source_slug]["ID"])),
            "post_name": book.wp_slug,
            "source_slug": book.source_slug,
            "status": "publish",
        }
        for book in planned_books
    ]
    verified = verify_target_state(target_inventory, catalog, planned_books, hub, committed_rows)
    assert {row["source_slug"] for row in verified} == missing_sources
    altered_inventory = json.loads(json.dumps(target_inventory))
    altered = next(page for page in altered_inventory["pages"] if page["ID"] == committed_rows[0]["ID"])
    altered["post_content"] = str(altered["post_content"]).replace("<iframe", "<not-an-iframe", 1)
    try:
        verify_target_state(altered_inventory, catalog, planned_books, hub, committed_rows)
    except RuntimeError as exc:
        assert "exact raw page verification failed" in str(exc)
    else:
        raise AssertionError("post-commit content alteration did not fail exact verification")
    assert inventory_matches_before(before_inventory, json.loads(json.dumps(before_inventory)))
    drifted_before = json.loads(json.dumps(before_inventory))
    drifted_before["hub"]["post_content"] = "concurrent edit"
    assert not inventory_matches_before(before_inventory, drifted_before)

    # Future weekly publication and the legacy hub command both delegate to
    # this same sync; no second direct REST template publisher remains.
    weekly_source = (ROOT / "scripts" / "publish_next_week.py").read_text(encoding="utf-8")
    wrapper_source = (ROOT / "scripts" / "update_wp_library.py").read_text(encoding="utf-8")
    assert '"scripts/sync_wordpress_books.py"' in weekly_source
    assert '"--apply"' in weekly_source
    assert "requests.Session" not in weekly_source
    assert "WP_BEIBEI_APP_PASSWORD" not in weekly_source
    assert "wp-json/wp/v2/pages" not in weekly_source
    assert "sync_wordpress_books.py" in wrapper_source
    assert "preschool-books" not in wrapper_source

    # The catalog fingerprint is stable and content-sensitive.
    fp = catalog_fingerprint(catalog.ready)
    assert re.fullmatch(r"[0-9a-f]{16}", fp)
    changed = list(catalog.ready)
    changed[0] = Book(**{**changed[0].__dict__, "title": changed[0].title + " changed"})
    assert catalog_fingerprint(changed) != fp

    print(json.dumps({
        "status": "PASS",
        "source_folders": len(catalog.all_source_folders),
        "ready": len(catalog.ready),
        "modern_ready": len(catalog.modern_ready),
        "legacy_ready": len(catalog.legacy_ready),
        "asset_incomplete": len(catalog.asset_incomplete),
        "initial_missing": sorted(missing_sources),
        "catalog_fingerprint": fp,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
