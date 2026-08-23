#!/usr/bin/env python3
"""Repoint /spanish-books/la-familia/ at the real book.

The page embeds `week-41-la-familia`, a pre-migration stub with
via.placeholder.com images and no audio. `week-71-la-familia` is a complete
modern book (7 images, full audio, analytics) and is the only book in the
106-book library with no WordPress page of its own.

This swaps exactly one iframe src on exactly one page. Nothing else on the
page is touched: the surrounding Divi content, the read-along SEO section and
the mobile !important height rules are all preserved byte for byte.

Dry-run by default. Requires --apply to write.

  WP_BEIBEI_USER / WP_BEIBEI_APP_PASSWORD from the environment.
"""
import argparse
import difflib
import os
import sys

import requests

WP_API = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"
PAGE_SLUG = "la-familia"
OLD = "books/week-41-la-familia/"
NEW = "books/week-71-la-familia/"
LIVE = "https://www.beibeiamigos.com/spanish-books/la-familia/"
BROWSER_UA = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile Safari/604.1"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually write to WordPress")
    args = ap.parse_args()

    user = os.environ.get("WP_BEIBEI_USER")
    pw = os.environ.get("WP_BEIBEI_APP_PASSWORD")
    if not (user and pw):
        sys.exit("Set WP_BEIBEI_USER and WP_BEIBEI_APP_PASSWORD")
    auth = (user, pw)
    s = requests.Session()
    s.headers["User-Agent"] = "WordPress/6.0"

    # The replacement must exist and be a real book before we point anyone at it.
    probe = requests.get(
        "https://seanmichael67.github.io/Spanish-Books/" + NEW, timeout=30)
    if probe.status_code != 200 or "const Icons" not in probe.text:
        sys.exit("refusing: %s is not a live modern book (HTTP %s)" % (NEW, probe.status_code))
    print("replacement verified: %s is live and modern" % NEW)

    r = s.get(WP_API, auth=auth, params={"slug": PAGE_SLUG, "parent": 1854,
                                         "context": "edit", "status": "any"}, timeout=40)
    r.raise_for_status()
    hits = r.json()
    if len(hits) != 1:
        sys.exit("refusing: expected exactly 1 page for slug %r, got %d" % (PAGE_SLUG, len(hits)))
    page = hits[0]
    raw = page["content"]["raw"]

    if NEW in raw:
        print("already repaired — page %d embeds %s" % (page["id"], NEW))
        return
    n = raw.count(OLD)
    if n != 1:
        sys.exit("refusing: expected exactly 1 occurrence of %r, found %d" % (OLD, n))

    new_raw = raw.replace(OLD, NEW)
    if len(new_raw) != len(raw) - len(OLD) + len(NEW):
        sys.exit("refusing: replacement changed more than the iframe src")

    print("\npage %d (%s)\n" % (page["id"], page["link"]))
    for line in difflib.unified_diff(raw.splitlines(), new_raw.splitlines(),
                                     "before", "after", n=0, lineterm=""):
        if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
            print("  " + line[:200])

    if not args.apply:
        print("\nDRY RUN — nothing written. Re-run with --apply to fire.")
        return

    w = s.post(WP_API + "/%d" % page["id"], auth=auth,
               json={"content": new_raw}, timeout=60)
    if w.status_code != 200:
        sys.exit("write failed: HTTP %s %s" % (w.status_code, w.text[:200]))
    print("\nwrote page %d" % page["id"])

    live = requests.get(LIVE, timeout=40, headers=BROWSER_UA).text
    if NEW in live and OLD not in live:
        print("verified live: %s now embeds %s" % (LIVE, NEW))
    else:
        sys.exit("WROTE BUT LIVE PAGE DOES NOT SHOW THE NEW BOOK — check caching")


if __name__ == "__main__":
    main()
