#!/usr/bin/env python3
"""Add the Book Club email signup to the hub page (1854).

Appends a Divi section (anchor id book-club) with a native Divi contact
form: Parent name + Email, submissions emailed to admin@beibeiamigos.com
with a clear subject. Idempotent via marker check. Dry-run by default.
"""
import argparse
import os
import sys

import requests

WP_API = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"
WP_USER = os.environ.get("WP_BEIBEI_USER", "Luciano")
WP_PASS = os.environ.get("WP_BEIBEI_APP_PASSWORD")
if not WP_PASS:
    raise SystemExit("Set WP_BEIBEI_APP_PASSWORD")
AUTH = (WP_USER, WP_PASS)
HUB_ID = 1854
MARKER = 'module_id="book-club"'

SECTION = """[et_pb_section fb_built="1" module_id="book-club" _builder_version="4.27.4" background_color="#667eea" custom_padding="40px|20px|40px|20px"][et_pb_row _builder_version="4.27.4"][et_pb_column type="4_4" _builder_version="4.27.4"][et_pb_text _builder_version="4.27.4" text_orientation="center" background_layout="dark"]
<h2 style="color:#ffffff;">📬 Free Spanish Book Club</h2>
<p style="color:rgba(255,255,255,0.92); max-width:560px; margin:8px auto 0;">A brand-new interactive Spanish book for your child every week — with native audio, word highlighting and collectible badges. Join free and never miss one!</p>
[/et_pb_text][et_pb_contact_form email="admin@beibeiamigos.com" title="" custom_message="New Book Club signup!||et_pb_line_break_holder||Parent: %%Name%%||et_pb_line_break_holder||Email: %%Email%%" success_message="¡Bienvenidos! You're in — look out for a new book every week. 🎉" submit_button_text="Join the Book Club" _builder_version="4.27.4" _unique_id="bookclub-form-2026"][et_pb_contact_field field_id="Name" field_title="Parent name" fullwidth_field="off" _builder_version="4.27.4" button_text_size__hover_enabled="off"][/et_pb_contact_field][et_pb_contact_field field_id="Email" field_title="Email" field_type="email" fullwidth_field="off" _builder_version="4.27.4" button_text_size__hover_enabled="off"][/et_pb_contact_field][/et_pb_contact_form][/et_pb_column][/et_pb_row][/et_pb_section]"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    s = requests.Session()
    s.headers["User-Agent"] = "WordPress/6.0"
    r = s.get(f"{WP_API}/{HUB_ID}", auth=AUTH, params={"context": "edit"}, timeout=30)
    raw = r.json()["content"]["raw"]
    if MARKER in raw:
        print("hub already has book-club section")
        return
    if not args.apply:
        print(f"DRY: would append {len(SECTION)} chars to hub page")
        return
    r2 = s.post(f"{WP_API}/{HUB_ID}", auth=AUTH,
                json={"content": raw + "\n" + SECTION}, timeout=30)
    print("hub update:", r2.status_code)
    sys.exit(0 if r2.status_code == 200 else 1)


if __name__ == "__main__":
    main()
