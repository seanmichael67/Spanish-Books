#!/usr/bin/env python3
"""Apply the site-wide Sour Gummy font + uniform 1200px content width to
every beibeiamigos.com page and post by appending a marked, idempotent
<style> block to the content (same delivery pattern as update_wp_seo.py —
there is no REST route for Divi theme options, so per-page injection is
the only API path).

Font rule uses !important but excludes icon-font elements (ETmodules /
FontAwesome / dashicons) so Divi icons keep rendering. Width rule has NO
!important on purpose: pages with deliberate full-width custom code (the
homepage .bebei-landing-page) keep their own !important overrides.

Default is DRY RUN. --apply to write, --slug <slug> to limit to one page,
--posts-too to include blog posts.
"""
import argparse
import os
import re
import sys
import time

import requests

WP_BASE = "https://www.beibeiamigos.com/wp-json/wp/v2"
WP_USER = os.environ.get("WP_BEIBEI_USER")
WP_PASS = os.environ.get("WP_BEIBEI_APP_PASSWORD")
if not WP_USER or not WP_PASS:
    raise SystemExit("Set WP_BEIBEI_USER and WP_BEIBEI_APP_PASSWORD")
AUTH = (WP_USER, WP_PASS)

MARKER_START = "<!-- ba-global-style-v1 -->"
MARKER_END = "<!-- /ba-global-style-v1 -->"

# Single line to stay safe from wpautop on non-builder content.
FONT_STACK = "'Sour Gummy','Quicksand','Comic Sans MS',cursive,sans-serif"
ICON_EXCLUDE = (
    ":not(.et-pb-icon):not([class*='et_pb_icon']):not(.fa):not(.fas)"
    ":not(.far):not(.fab):not([class^='fa-']):not([class*=' fa-'])"
    ":not(.dashicons):not([class*='ETmodules'])"
)
STYLE_BLOCK = (
    f"{MARKER_START}"
    "<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
    "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Sour+Gummy:ital,wght@0,100..900;1,100..900&display=swap'>"
    "<style id='ba-global-style'>"
    f"body, body {ICON_EXCLUDE} {{ font-family: {FONT_STACK} !important; }} "
    # fallback for browsers without :has()
    ".et_pb_row { max-width: 1200px; } "
    ".bebei-container { max-width: 1200px; } "
    # Divi rows default to width:80% -> page width varies with viewport.
    # Force identical gutters + 1200px cap everywhere, EXCEPT rows hosting
    # full-bleed custom landing code (home/enroll/family-handbook), whose
    # inner .bebei-container is already 1200px.
    "#page-container .et_pb_row:not(:has(.bebei-landing-page)) "
    "{ width: calc(100% - 48px) !important; max-width: 1200px !important; } "
    "</style>"
    f"{MARKER_END}"
)

BLOCK_RE = re.compile(
    re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), re.DOTALL
)

session = requests.Session()
session.headers["User-Agent"] = "WordPress/6.0"


def fetch_all(kind):
    items, page = [], 1
    while True:
        r = session.get(
            f"{WP_BASE}/{kind}",
            params={
                "per_page": 100,
                "page": page,
                "context": "edit",
                "status": "publish,draft,private",
                "_fields": "id,slug,content",
            },
            auth=AUTH,
            timeout=60,
        )
        if r.status_code == 400:  # past last page
            break
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return items


def process(kind, items, apply, only_slug=None):
    changed = skipped = failed = 0
    for it in items:
        slug = it["slug"]
        if only_slug and slug != only_slug:
            continue
        raw = it["content"]["raw"]
        if MARKER_START in raw:
            new = BLOCK_RE.sub(STYLE_BLOCK, raw)
            action = "update-in-place"
        else:
            new = raw.rstrip() + "\n" + STYLE_BLOCK
            action = "append"
        if new == raw:
            skipped += 1
            continue
        if not apply:
            print(f"DRY {kind} {it['id']} {slug}: would {action}")
            changed += 1
            continue
        r = session.post(
            f"{WP_BASE}/{kind}/{it['id']}",
            json={"content": new},
            auth=AUTH,
            timeout=60,
        )
        if r.ok:
            print(f"OK  {kind} {it['id']} {slug}: {action}")
            changed += 1
        else:
            print(f"ERR {kind} {it['id']} {slug}: {r.status_code} {r.text[:120]}")
            failed += 1
        time.sleep(0.4)
    print(f"== {kind}: {changed} changed, {skipped} already current, {failed} failed ==")
    return failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--slug")
    ap.add_argument("--posts-too", action="store_true")
    args = ap.parse_args()

    pages = fetch_all("pages")
    print(f"fetched {len(pages)} pages")
    rc = process("pages", pages, args.apply, args.slug)
    if args.posts_too and not args.slug:
        posts = fetch_all("posts")
        print(f"fetched {len(posts)} posts")
        rc += process("posts", posts, args.apply)
    sys.exit(1 if rc else 0)


if __name__ == "__main__":
    main()
