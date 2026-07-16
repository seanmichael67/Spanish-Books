#!/usr/bin/env python3
"""Make the book iframe fit the phone screen on the WP book pages.

The book app fills 100% of its iframe height, but the iframe was fixed at
min-height:900px — on a ~660px-tall phone screen the whole book could never
be on screen at once (bottom nav or title always cut off). Swap to a
progressive height: 900px for browsers without svh support / desktop cap,
clamp(480px, 100svh - 130px, 900px) elsewhere so the full book fits the
visible screen.

Dry-run by default; --apply to write; --slug to limit.
"""
import argparse
import sys
import time

import requests

OLD_STYLE = 'style="border:none; max-width:100%; min-height:900px;"'
NEW_STYLE = ('style="border:none; max-width:100%; width:100%; height:900px; '
             'height:clamp(480px, calc(100svh - 130px), 900px);"')
WP_API = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"
AUTH = ("Luciano", "ZjjW wlE4 tNJa 5sQr F6ym fLtV")
HUB_ID = 1854

session = requests.Session()
session.headers["User-Agent"] = "WordPress/6.0"


def child_pages():
    pages = []
    for pn in range(1, 5):
        r = session.get(WP_API, auth=AUTH, params={
            "parent": HUB_ID, "per_page": 100, "page": pn,
            "context": "edit", "status": "publish,draft"}, timeout=30)
        if r.status_code != 200 or not r.json():
            break
        pages.extend(r.json())
        if len(r.json()) < 100:
            break
    return pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--slug")
    args = ap.parse_args()

    changed = skipped = failed = 0
    for p in child_pages():
        if args.slug and p["slug"] != args.slug:
            continue
        raw = p["content"]["raw"]
        if OLD_STYLE not in raw:
            skipped += 1
            continue
        if not args.apply:
            print(f"DRY {p['slug']} (id {p['id']})")
            changed += 1
            continue
        r = session.post(f"{WP_API}/{p['id']}", auth=AUTH,
                         json={"content": raw.replace(OLD_STYLE, NEW_STYLE)},
                         timeout=30)
        if r.status_code == 200:
            print(f"✅ {p['slug']}")
            changed += 1
        else:
            print(f"❌ {p['slug']} HTTP {r.status_code}: {r.text[:120]}")
            failed += 1
        time.sleep(0.5)
    print(f"\n{changed} changed, {skipped} skipped, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
