#!/usr/bin/env python3
"""Swap the books iframe host on the WP pages (hub 1854 + all book pages).

Replaces https://spanish-books.onrender.com with the new static host in each
page's content. Idempotent (skips pages without the old host). Dry-run by
default; --apply to write. --slug <page_slug> or --id <page_id> to limit.
"""
import argparse
import sys
import time

import requests

OLD = "https://spanish-books.onrender.com"
NEW = "https://seanmichael67.github.io/Spanish-Books"
WP_API = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"
WP_USER = os.environ.get("WP_BEIBEI_USER")
WP_PASS = os.environ.get("WP_BEIBEI_APP_PASSWORD")
if not WP_USER or not WP_PASS:
    raise SystemExit("Set WP_BEIBEI_USER and WP_BEIBEI_APP_PASSWORD")
AUTH = (WP_USER, WP_PASS)
HUB_ID = 1854

session = requests.Session()
session.headers["User-Agent"] = "WordPress/6.0"


def all_target_pages():
    pages = []
    for pagenum in range(1, 5):
        r = session.get(WP_API, auth=AUTH, params={
            "parent": HUB_ID, "per_page": 100, "page": pagenum,
            "context": "edit", "status": "publish,draft"}, timeout=30)
        if r.status_code != 200 or not r.json():
            break
        pages.extend(r.json())
        if len(r.json()) < 100:
            break
    hub = session.get(f"{WP_API}/{HUB_ID}", auth=AUTH,
                      params={"context": "edit"}, timeout=30)
    if hub.status_code == 200:
        pages.append(hub.json())
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--slug")
    ap.add_argument("--id", type=int)
    args = ap.parse_args()

    changed = skipped = failed = 0
    for p in all_target_pages():
        if args.slug and p["slug"] != args.slug:
            continue
        if args.id and p["id"] != args.id:
            continue
        raw = p["content"]["raw"]
        n = raw.count(OLD)
        if n == 0:
            skipped += 1
            continue
        if not args.apply:
            print(f"DRY {p['slug']} (id {p['id']}): {n} occurrence(s)")
            changed += 1
            continue
        r = session.post(f"{WP_API}/{p['id']}", auth=AUTH,
                         json={"content": raw.replace(OLD, NEW)}, timeout=30)
        if r.status_code == 200:
            print(f"✅ {p['slug']} (id {p['id']}): {n} swapped")
            changed += 1
        else:
            print(f"❌ {p['slug']} HTTP {r.status_code}: {r.text[:120]}")
            failed += 1
        time.sleep(0.5)
    print(f"\n{changed} changed, {skipped} already clean, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
