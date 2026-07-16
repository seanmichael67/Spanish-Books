#!/usr/bin/env python3
"""Add crawlable SEO content + meta description to the WP book pages.

For every published book, Google currently sees only an H1 and an iframe —
all book text lives on spanish-books.onrender.com, so beibeiamigos.com gets
no credit. This script appends a marked, idempotent "Read along" section
(Spanish sentences + English + vocabulary) to each WP book page and sets
the excerpt + Yoast meta description.

Default is DRY RUN (prints what it would do). Use --apply to write.
Use --slug <page_slug> to limit to one page (e.g. --slug la-guitarra).

Sean gate: run --apply against the 100+ live pages only after sign-off.
"""
import argparse
import html
import json
import os
import re
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_static_assets import parse_book, ready_slugs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WP_API = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"
AUTH = ("Luciano", "ZjjW wlE4 tNJa 5sQr F6ym fLtV")
MARKER = "<!-- seo-read-along-v1 -->"

session = requests.Session()
session.headers["User-Agent"] = "WordPress/6.0"


def seo_section(slug, title, subtitle):
    pages = parse_book(slug)
    sentences = []
    words = []
    for pg in pages:
        t, f = pg["title"].strip(), pg["footer"].strip()
        if pg["words"]:
            words = pg["words"]
        # skip structural pages
        if t in ("Mis Palabras", "¡Ganaste tu insignia!") or not f or f == "Aprendiendo juntos":
            continue
        sentences.append((t, f))
    if not sentences:
        return None
    rows = "\n".join(
        f"<li><strong lang=\"es\">{html.escape(es)}</strong> — {html.escape(en)}</li>"
        for es, en in sentences
    )
    vocab = ", ".join(html.escape(w) for w in words)
    vocab_html = (
        f"<p><strong>Vocabulary in this book:</strong> <span lang=\"es\">{vocab}</span></p>"
        if words else ""
    )
    return f"""{MARKER}
<div class="book-read-along" style="max-width:700px;margin:24px auto;font-size:1rem;line-height:1.7;color:#444;">
<h2 style="text-align:center;">Read Along: {html.escape(title)} ({html.escape(subtitle)})</h2>
<p>Every page of this free interactive Spanish book for preschoolers, with English translations. Read it together, then press play in the book above to hear native Spanish audio:</p>
<ul>
{rows}
</ul>
{vocab_html}
<p>{html.escape(title)} is part of the free Beibei Amigos Spanish library for children ages 2–5 — one new book every week, each with audio pronunciation, word highlighting and a collectible badge. <a href="/spanish-books/">Browse all our free Spanish books</a> or <a href="/tour/">schedule a tour</a> of our Mandarin &amp; Spanish immersion preschool in Phoenix.</p>
</div>"""


def book_meta():
    """slug -> (page_slug, title, subtitle) from server.js"""
    raw = open(os.path.join(ROOT, "server.js")).read()
    out = {}
    for m in re.finditer(
        r"slug:\s*'(week-\d+-([^']+))'.*?title:\s*'([^']*)'.*?subtitle:\s*'([^']*)'.*?ready:\s*true", raw
    ):
        out[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    return out


def find_page(page_slug):
    r = session.get(WP_API, auth=AUTH,
                    params={"slug": page_slug, "status": "publish,draft", "context": "edit"},
                    timeout=30)
    items = r.json() if r.status_code == 200 else []
    return items[0] if items else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--slug", help="limit to one WP page slug")
    args = ap.parse_args()

    meta = book_meta()
    done = skipped = missing = 0
    for book_slug, (page_slug, title, subtitle) in sorted(meta.items()):
        if args.slug and page_slug != args.slug:
            continue
        section = seo_section(book_slug, title, subtitle)
        if not section:
            print(f"⚠️  {page_slug}: could not build section (no parseable pages)")
            continue
        page = find_page(page_slug)
        if not page:
            print(f"❌ {page_slug}: WP page not found")
            missing += 1
            continue
        content = page["content"]["raw"]
        if MARKER in content:
            print(f"= {page_slug}: already has read-along section")
            skipped += 1
            continue
        desc = (f"Free interactive Spanish book “{title}” ({subtitle}) for kids 2-5: "
                f"native audio, word highlighting and a collectible badge. Read free online!")[:156]
        payload = {
            "content": content + "\n" + section,
            "excerpt": desc,
            "meta": {"_yoast_wpseo_metadesc": desc},
        }
        if not args.apply:
            print(f"DRY {page_slug}: would append {len(section)} chars + meta desc: {desc[:70]}…")
            done += 1
            continue
        r = session.post(f"{WP_API}/{page['id']}", auth=AUTH, json=payload, timeout=30)
        if r.status_code == 200:
            print(f"✅ {page_slug} updated (page {page['id']})")
            done += 1
        else:
            print(f"❌ {page_slug} HTTP {r.status_code}: {r.text[:150]}")
        time.sleep(1)
    print(f"\n{done} updated/planned, {skipped} already done, {missing} missing")


if __name__ == "__main__":
    main()
