#!/usr/bin/env python3
"""Update the WordPress spanish-books page with latest Divi embed code."""
import json
import urllib.request

WP_USER = "Luciano"
WP_PASS = "ZjjW wlE4 tNJa 5sQr F6ym fLtV"
PAGE_ID = 1854

# Read the embed HTML
with open("/home/cryptonovado/Projects/preschool-books/divi-embeds/library-divi.html") as f:
    html = f.read()

# Wrap in Divi shortcodes
content = '[et_pb_section fb_built="1" _builder_version="4.27.4" _module_preset="default"][et_pb_row _builder_version="4.27.4" _module_preset="default"][et_pb_column type="4_4" _builder_version="4.27.4" _module_preset="default"][et_pb_code _builder_version="4.27.4" _module_preset="default"]' + html + '[/et_pb_code][/et_pb_column][/et_pb_row][/et_pb_section]'

data = json.dumps({"content": content}).encode()
req = urllib.request.Request(
    f"https://www.beibeiamigos.com/wp-json/wp/v2/pages/{PAGE_ID}",
    data=data,
    method="POST",
    headers={
        "Content-Type": "application/json",
        "Authorization": "Basic " + __import__('base64').b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode(),
        "User-Agent": "WordPress/6.0"
    }
)

resp = urllib.request.urlopen(req)
result = json.loads(resp.read())
print(f"Updated page {result['id']}: {result['slug']} ✅")
