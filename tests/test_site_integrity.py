import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "server.js"


def live_books():
    source = SERVER.read_text(encoding="utf-8")
    return re.findall(
        r"slug:\s*'(week-[^']+)'.*?ready:\s*true",
        source,
    )


def page_slug(book_slug):
    return re.sub(r"^week-\d+-", "", book_slug)


def modern_books():
    return sorted(
        path.parent.name
        for path in (ROOT / "books").glob("week-*/index.html")
        if "const Icons" in path.read_text(encoding="utf-8")
    )


class SiteIntegrityTests(unittest.TestCase):
    def test_catalog_is_complete_and_every_cover_exists(self):
        books = live_books()
        self.assertEqual(106, len(books))
        self.assertEqual(len(books), len(set(books)))
        for slug in books:
            with self.subTest(slug=slug):
                self.assertTrue(
                    (ROOT / "books" / slug / "images" / "page-00.webp").is_file()
                )

    def test_library_hub_is_branded_searchable_and_canonical(self):
        source = SERVER.read_text(encoding="utf-8")
        built = (ROOT / "index.html").read_text(encoding="utf-8")
        for html in (source, built):
            self.assertNotIn("spanish-books.onrender.com", html)
            self.assertIn(
                "https://www.beibeiamigos.com/spanish-books/",
                html,
            )
            self.assertIn('id="bookSearch"', html)
            self.assertIn('id="resultsStatus"', html)
            self.assertIn('aria-live="polite"', html)
            self.assertIn('class="card-cover"', html)
        self.assertIn("populatedThemeIds", source)
        self.assertEqual(15, built.count('class="theme-btn'))

    def test_all_live_book_apps_use_canonical_urls_and_accessible_controls(self):
        for slug in modern_books():
            path = ROOT / "books" / slug / "index.html"
            html = path.read_text(encoding="utf-8")
            canonical = (
                "https://www.beibeiamigos.com/spanish-books/"
                f"{page_slug(slug)}/"
            )
            with self.subTest(slug=slug):
                self.assertIn(canonical, html)
                self.assertNotIn("spanish-books.onrender.com", html)
                self.assertNotRegex(html, r"\bSofia\b")
                self.assertIn("Meet Sophia", html)
                self.assertNotIn("52 weeks of Spanish reading adventures", html)
                self.assertNotIn("→copy; 2026", html)
                self.assertEqual(1, html.count("&copy; 2026"))
                self.assertIn('aria-label="Previous page"', html)
                self.assertIn('aria-label="Next page"', html)
                self.assertIn('aria-label="Stop reading"', html)
                self.assertIn('alt={BOOK_CONFIG.title}', html)
                self.assertIn('alt={BOOK_CONFIG.schoolName}', html)

    def test_all_live_wordpress_embeds_avoid_stale_claims(self):
        paths = sorted((ROOT / "divi-embeds" / "books").glob("week-*.html"))
        for path in paths:
            slug = path.stem
            html = path.read_text(encoding="utf-8")
            with self.subTest(slug=slug):
                self.assertNotRegex(
                    html,
                    r"\d+\+ free interactive books",
                )
                self.assertNotRegex(html, r"\bSofia\b")
                self.assertIn("Sophia", html)

    def test_library_wordpress_embed_uses_current_brand_and_full_width_source(self):
        html = (ROOT / "divi-embeds" / "library-divi.html").read_text(
            encoding="utf-8"
        )
        self.assertNotRegex(html, r"\bSofia\b")
        self.assertIn("Sophia", html)
        self.assertNotIn("80+", html)
        self.assertIn('id="booksFrame"', html)
        self.assertIn('width="100%"', html)

    def test_wordpress_library_updater_is_preview_first_and_repo_local(self):
        source = (ROOT / "scripts" / "update_wp_library.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("Projects/preschool-books", source)
        self.assertIn('type="4_4"', source)
        self.assertIn("--apply", source)
        self.assertIn("context=edit", source)
        self.assertIn("backups", source)
        self.assertIn("preview", source)
        self.assertIn("content.raw", source)


if __name__ == "__main__":
    unittest.main()
