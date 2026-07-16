#!/usr/bin/env python3
"""Generate divi-embeds for weeks 96-97 and create DRAFT WordPress pages.

Pages are created with status=draft so nothing is publicly visible until
Sean publishes them (one click each in wp-admin).
"""
import json
import os
import re
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WP_API = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"
WP_USER = os.environ.get("WP_BEIBEI_USER")
WP_PASS = os.environ.get("WP_BEIBEI_APP_PASSWORD")
if not WP_USER or not WP_PASS:
    raise SystemExit("Set WP_BEIBEI_USER and WP_BEIBEI_APP_PASSWORD")
AUTH = (WP_USER, WP_PASS)
PARENT = 1854

DIVI_WRAP = ('[et_pb_section fb_built="1" _builder_version="4.27.4"]'
             '[et_pb_row _builder_version="4.27.4"]'
             '[et_pb_column type="4_4" _builder_version="4.27.4"]'
             '[et_pb_code _builder_version="4.27.4"]\n{}\n[/et_pb_code]'
             '[/et_pb_column][/et_pb_row][/et_pb_section]')

BOOKS = [
    {
        "slug": "week-96-la-guitarra", "page_slug": "la-guitarra",
        "title": "🎸 La Guitarra — The Guitar", "name": "La Guitarra",
        "alt": "The Guitar", "theme": "music & games",
        "desc": ("Strum along with la guitarra! This interactive Spanish book teaches "
                 "preschoolers guitar and music words with native audio. Earn a music "
                 "badge from Beibei Amigos, ages 2-5!"),
    },
    {
        "slug": "week-97-el-tambor", "page_slug": "el-tambor",
        "title": "🥁 El Tambor — The Drum", "name": "El Tambor",
        "alt": "The Drum", "theme": "music & games",
        "desc": ("Drum to the beat with el tambor! This interactive Spanish book teaches "
                 "preschoolers drum and rhythm words with native audio. Earn a music "
                 "badge from Beibei Amigos, ages 2-5!"),
    },
]

# use week-95's embed as the canonical template
template = open(os.path.join(ROOT, "divi-embeds", "books", "week-95-contar.html")).read()

session = requests.Session()
session.headers["User-Agent"] = "WordPress/6.0"

for b in BOOKS:
    html = template
    html = html.replace("week-95-contar", b["slug"])
    html = html.replace("/spanish-books/contar/", f"/spanish-books/{b['page_slug']}/")
    html = html.replace('"name": "Contar"', f'"name": "{b["name"]}"')
    html = html.replace('"alternateName": "Counting"', f'"alternateName": "{b["alt"]}"')
    html = html.replace("<!-- Contar -", f"<!-- {b['name']} -")
    html = html.replace('title="Contar - Free Spanish Book', f'title="{b["name"]} - Free Spanish Book')
    # description paragraph + JSON-LD description/keywords
    html = re.sub(r'<p class="desc">.*?</p>', f'<p class="desc">\n{b["desc"]}\n</p>', html, flags=re.S)
    html = html.replace(
        "Free interactive Spanish book about contar for preschoolers ages 2-5. Learn numbers & letters vocabulary with audio!",
        f"Free interactive Spanish book about {b['name'].lower()} for preschoolers ages 2-5. Learn {b['theme']} vocabulary with audio!")
    html = html.replace("numbers & letters", b["theme"])

    out = os.path.join(ROOT, "divi-embeds", "books", f"{b['slug']}.html")
    open(out, "w").write(html)
    print(f"embed written: {out}")

    data = {
        "title": b["title"],
        "slug": b["page_slug"],
        "status": "draft",
        "parent": PARENT,
        "content": DIVI_WRAP.format(html),
        "excerpt": b["desc"],
    }
    r = session.post(WP_API, auth=AUTH, json=data, timeout=30)
    if r.status_code == 201:
        p = r.json()
        print(f"✅ draft created: {b['title']} → id {p['id']} ({p.get('link')})")
    else:
        print(f"❌ {b['title']} — HTTP {r.status_code}: {r.text[:200]}")
