#!/usr/bin/env python3
"""Repair WordPress book pages whose iframe src lost its book folder.

Six published pages under the hub carry src ".../Spanish-Books/books//" — the
folder name was dropped by an earlier bulk host swap, so the iframe 404s and the
reader sees an empty white box. The book each page was meant to show still
exists in this repo and is live on GitHub Pages.

Each mapping below was confirmed by rendering the target headless at 390px on
2026-08-23. Targets are named in full: week numbers are NOT unique in this repo
(week-71-el-viaje-espacial and week-71-la-familia both exist), so never map by
week number.

Dry-run by default. --apply writes, then re-reads each live page to confirm.

  WP_BEIBEI_USER / WP_BEIBEI_APP_PASSWORD from the environment.
"""
import argparse
import os
import sys

import requests

WP_API = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"
HUB_ID = 1854
HOST = "https://seanmichael67.github.io/Spanish-Books"
# Two independent defects on these pages, both from the same dropped slug:
#   1. the iframe src  -> .../Spanish-Books/books//        (renders an empty box)
#   2. the JSON-LD url -> .../spanish-books//              (tells Google the wrong URL)
# Match each exactly, never the bare "books//" substring, which hits both.
BROKEN_FRAME = "Spanish-Books/books//"
BROKEN_JSONLD = '"url": "https://www.beibeiamigos.com/spanish-books//"' 
BROWSER_UA = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile Safari/604.1"}

# wp page slug -> book folder. Verified live 2026-08-23.
# The two marked "broken images" render their text but their <img> tags 404;
# that is tracked separately — an empty white box is strictly worse.
MAP = {
    "el-viaje-espacial":          "week-71-el-viaje-espacial",
    "las-abejas-y-el-jardin":     "week-68-las-abejas-y-el-jardin",
    "el-parque-de-juegos":        "week-64-el-parque-de-juegos",          # broken images
    "los-amigos-de-la-comunidad": "week-54-los-amigos-de-la-comunidad",   # broken images
    "las-profesiones":            "week-45-las-profesiones",
    "los-deportes":               "week-43-los-deportes",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    user = os.environ.get("WP_BEIBEI_USER")
    pw = os.environ.get("WP_BEIBEI_APP_PASSWORD")
    if not (user and pw):
        sys.exit("Set WP_BEIBEI_USER and WP_BEIBEI_APP_PASSWORD")
    auth = (user, pw)
    s = requests.Session()
    s.headers["User-Agent"] = "WordPress/6.0"

    repo_books = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "books")
    plan = []
    for slug, folder in MAP.items():
        if not os.path.isdir(os.path.join(repo_books, folder)):
            sys.exit("refusing: %s is not a folder in this repo" % folder)
        probe = requests.get("%s/books/%s/" % (HOST, folder), timeout=30)
        if probe.status_code != 200:
            sys.exit("refusing: %s/books/%s/ is HTTP %s" % (HOST, folder, probe.status_code))

        r = s.get(WP_API, auth=auth, timeout=40,
                  params={"slug": slug, "parent": HUB_ID, "context": "edit", "status": "any"})
        r.raise_for_status()
        hits = r.json()
        if len(hits) != 1:
            sys.exit("refusing: expected 1 page for %r, got %d" % (slug, len(hits)))
        page = hits[0]
        raw = page["content"]["raw"]
        good_frame = "Spanish-Books/books/%s/" % folder
        good_jsonld = '"url": "https://www.beibeiamigos.com/spanish-books/%s/"' % slug
        if good_frame in raw and BROKEN_JSONLD not in raw:
            print("  %-28s already repaired" % slug)
            continue

        new_raw, fixed = raw, []
        n = new_raw.count(BROKEN_FRAME)
        if n > 1:
            sys.exit("refusing %s: %d broken iframe srcs, expected at most 1" % (slug, n))
        if n == 1:
            new_raw = new_raw.replace(BROKEN_FRAME, good_frame)
            fixed.append("iframe")
        j = new_raw.count(BROKEN_JSONLD)
        if j > 1:
            sys.exit("refusing %s: %d broken JSON-LD urls, expected at most 1" % (slug, j))
        if j == 1:
            new_raw = new_raw.replace(BROKEN_JSONLD, good_jsonld)
            fixed.append("json-ld url")

        # Length must move by exactly the two substitutions and nothing else.
        delta = (len(good_frame) - len(BROKEN_FRAME)) * (1 if "iframe" in fixed else 0) \
              + (len(good_jsonld) - len(BROKEN_JSONLD)) * (1 if "json-ld url" in fixed else 0)
        if len(new_raw) != len(raw) + delta:
            sys.exit("refusing %s: edit changed more than the targeted substrings" % slug)
        if not fixed:
            print("  %-28s nothing broken to fix" % slug)
            continue
        plan.append((page, slug, folder, new_raw))
        print("  %-28s id=%-6s fixes: %s -> %s" % (slug, page["id"], ", ".join(fixed), folder))

    if not plan:
        print("\nnothing to do.")
        return
    if not args.apply:
        print("\nDRY RUN — %d pages would change, nothing written." % len(plan))
        return

    ok = 0
    for page, slug, folder, new_raw in plan:
        w = s.post(WP_API + "/%d" % page["id"], auth=auth, json={"content": new_raw}, timeout=60)
        if w.status_code != 200:
            print("  FAILED %s: HTTP %s %s" % (slug, w.status_code, w.text[:120]))
            continue
        live = requests.get(page["link"], timeout=40, headers=BROWSER_UA).text
        if ('books/%s/' % folder) in live and BROKEN_FRAME not in live:
            print("  verified live: %s -> %s" % (page["link"], folder))
            ok += 1
        else:
            print("  WROTE BUT NOT VISIBLE LIVE: %s" % page["link"])
    print("\n%d/%d repaired and verified." % (ok, len(plan)))


if __name__ == "__main__":
    main()
