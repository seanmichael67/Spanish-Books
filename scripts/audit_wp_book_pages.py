#!/usr/bin/env python3
"""Audit every live WordPress book page under the Spanish books hub (1854).

Answers one question the repo alone cannot: does each published page actually
show a reader a working book? Classifies every page as OK / LEGACY_STUB /
BROKEN_IFRAME / MISSING_FOLDER, and where a page is not OK, proposes the
modern library book that should replace it.

Read-only. Nothing here writes to WordPress; --json emits the remediation
mapping for a separate, gated apply step.

  WP_BEIBEI_USER / WP_BEIBEI_APP_PASSWORD are read from the environment.
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import sys
import unicodedata

import requests

HUB_ID = 1854
WP_API = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"
PAGES_HOST = "https://seanmichael67.github.io/Spanish-Books"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A book folder is a real, modern book only if its client bundle is present.
MODERN_MARKER = "const Icons"

STOP = {"el", "la", "los", "las", "un", "una", "de", "del", "y", "mi", "mis", "week"}

# WordPress/Divi serves a different (frame-less) document to non-browser agents,
# so the iframe check MUST use a browser User-Agent or every page looks broken.
BROWSER_UA = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile Safari/604.1"}


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]", " ", s.lower())


def tokens(s):
    return {t for t in norm(s).split() if t and t not in STOP and not t.isdigit()}


def library():
    """slug -> (title, subtitle) for every book listed in server.js."""
    srv = open(os.path.join(ROOT, "server.js"), encoding="utf-8").read()
    pairs = re.findall(
        r"slug:\s*['\"]([^'\"]+)['\"][^}]*?title:\s*['\"]([^'\"]+)['\"][^}]*?subtitle:\s*['\"]([^'\"]+)['\"]",
        srv, re.S)
    return {s: (t, sub) for s, t, sub in pairs}


def wp_children(auth):
    out, page = [], 1
    while True:
        r = requests.get(WP_API, auth=auth, timeout=40,
                         headers={"User-Agent": "WordPress/6.0"},
                         params={"parent": HUB_ID, "per_page": 100, "page": page,
                                 "status": "any", "_fields": "id,slug,status,title,link"})
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        out += batch
        page += 1
    return out


def classify(page):
    """Fetch the live page and decide what a reader actually sees."""
    try:
        body = requests.get(page["link"], timeout=40, headers=BROWSER_UA).text
    except Exception as exc:
        return dict(page, verdict="FETCH_ERROR", folder=None, detail=str(exc)[:80])
    m = re.search(r'id="bookFrame"[^>]*src="([^"]+)"', body)
    has_desc = bool(re.search(r'<meta\s+name="description"', body, re.I))
    if not m:
        return dict(page, verdict="NO_IFRAME", folder=None, has_desc=has_desc)
    src = m.group(1)
    folder = src.rstrip("/").split("/")[-1]
    if folder == "books" or not folder:
        return dict(page, verdict="BROKEN_IFRAME", folder=None, src=src, has_desc=has_desc)
    idx = os.path.join(ROOT, "books", folder, "index.html")
    if not os.path.exists(idx):
        return dict(page, verdict="MISSING_FOLDER", folder=folder, src=src, has_desc=has_desc)
    html = open(idx, encoding="utf-8", errors="ignore").read()
    verdict = "OK" if MODERN_MARKER in html else "LEGACY_STUB"
    return dict(page, verdict=verdict, folder=folder, src=src, has_desc=has_desc)


def propose(row, lib, taken):
    """Best modern-library replacement for a page that is not OK."""
    # Exact match on the slug tail is unambiguous: week-71-la-familia == la-familia.
    for slug in lib:
        if slug in taken:
            continue
        if re.sub(r"^week-\d+-", "", slug) == row["slug"]:
            return slug, 99
    want = tokens(row["slug"])
    if not want:
        return None, 0
    best, score = None, 0.0
    for slug, (title, sub) in lib.items():
        if slug in taken:
            continue
        have = tokens(slug) | tokens(title) | tokens(sub)
        if not have:
            continue
        # Jaccard, so a one-word slug matching a one-word book scores 1.0
        overlap = len(want & have) / len(want | have)
        if overlap > score:
            best, score = slug, overlap
    return (best, round(score, 2)) if score >= 0.34 else (None, round(score, 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write the full audit + proposed mapping here")
    ap.add_argument("--workers", type=int, default=10)
    args = ap.parse_args()

    user = os.environ.get("WP_BEIBEI_USER")
    pw = os.environ.get("WP_BEIBEI_APP_PASSWORD")
    if not (user and pw):
        sys.exit("Set WP_BEIBEI_USER and WP_BEIBEI_APP_PASSWORD")

    lib = library()
    kids = wp_children((user, pw))
    if not kids:
        sys.exit("No child pages returned for hub %d — check credentials" % HUB_ID)

    with cf.ThreadPoolExecutor(args.workers) as ex:
        rows = list(ex.map(classify, kids))

    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1

    linked = {r["folder"] for r in rows if r["verdict"] == "OK" and r["folder"]}
    broken = [r for r in rows if r["verdict"] != "OK"]
    taken = set(linked)
    for r in broken:
        cand, score = propose(r, lib, taken)
        r["proposed"] = cand
        r["proposed_score"] = score
        if cand:
            taken.add(cand)
        else:
            r["proposed"] = None

    print("Live WordPress book pages under hub %d: %d" % (HUB_ID, len(rows)))
    for k in sorted(counts, key=lambda k: -counts[k]):
        print("  %-15s %d" % (k, counts[k]))
    nodesc = sum(1 for r in rows if not r.get("has_desc"))
    print("  %-15s %d  (Google indexes these; none supply their own snippet)"
          % ("no meta desc", nodesc))
    unreachable = len(rows) - counts.get("OK", 0)
    print("\n%d of %d live pages (%d%%) show a reader nothing usable.\n"
          % (unreachable, len(rows), round(100 * unreachable / len(rows))))

    print("--- pages that need repair, with proposed replacement ---")
    for r in sorted(broken, key=lambda r: r["slug"]):
        prop = r.get("proposed")
        note = ("-> %s (match %s)" % (prop, r["proposed_score"])) if prop else "-> NO CONFIDENT MATCH"
        print("  %-30s %-15s %s" % (r["slug"], r["verdict"], note))

    orphans = sorted(set(lib) - {r["folder"] for r in rows if r["folder"]})
    if orphans:
        print("\n--- library books with no WordPress page (%d) ---" % len(orphans))
        for s in orphans:
            print("  ", s)

    if args.json:
        json.dump({"pages": rows, "orphan_books": orphans}, open(args.json, "w"), indent=1)
        print("\nwrote", args.json)


if __name__ == "__main__":
    main()
