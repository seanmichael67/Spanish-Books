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
import os
import sys
import time

import requests

# Site CSS has a phones-only rule `iframe{height:auto!important}` (old
# responsive fix), so the inline height MUST be !important to win on mobile.
OLD_STYLES = [
    'style="border:none; max-width:100%; min-height:900px;"',
    ('style="border:none; max-width:100%; width:100%; height:900px; '
     'height:clamp(480px, calc(100svh - 130px), 900px);"'),
]
NEW_STYLE = ('style="border:none; max-width:100%; width:100%; min-height:480px; '
             'height:900px !important; '
             'height:clamp(480px, calc(100svh - 130px), 900px) !important;"')
WP_API = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"
WP_USER = os.environ.get("WP_BEIBEI_USER")
WP_PASS = os.environ.get("WP_BEIBEI_APP_PASSWORD")
if not WP_USER or not WP_PASS:
    raise SystemExit("Set WP_BEIBEI_USER and WP_BEIBEI_APP_PASSWORD")
AUTH = (WP_USER, WP_PASS)
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
        old = next((o for o in OLD_STYLES if o in raw), None)
        if not old:
            skipped += 1
            continue
        if not args.apply:
            print(f"DRY {p['slug']} (id {p['id']})")
            changed += 1
            continue
        r = session.post(f"{WP_API}/{p['id']}", auth=AUTH,
                         json={"content": raw.replace(old, NEW_STYLE)},
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
