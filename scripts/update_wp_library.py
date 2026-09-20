#!/usr/bin/env python3
"""Build a full-width WordPress preview for the Spanish library.

The default path is local-only. Passing ``--apply`` performs the gated live
write after fetching and backing up authenticated ``content.raw``.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKDIR = Path("/tmp/spanish-books-wp")
PREVIEW_DIR = WORKDIR / "preview"
BACKUP_DIR = WORKDIR / "backups"
PAGE_ID = 1854
PAGE_URL = "https://www.beibeiamigos.com/spanish-books/"
API_URL = f"https://www.beibeiamigos.com/wp-json/wp/v2/pages/{PAGE_ID}"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


def divi_content(embed_html: str) -> str:
    prefix = (
        '[et_pb_section fb_built="1" _builder_version="4.27.4" '
        'custom_padding="0px||0px||false|false"]'
        '[et_pb_row column_structure="4_4" _builder_version="4.27.4" '
        'use_custom_gutter="on" gutter_width="1" width="100%" max_width="1600px"]'
        '[et_pb_column type="4_4" _builder_version="4.27.4"]'
        '[et_pb_code _builder_version="4.27.4"]'
    )
    suffix = "[/et_pb_code][/et_pb_column][/et_pb_row][/et_pb_section]"
    content = prefix + embed_html.strip() + suffix
    if any(char in content for char in "“”"):
        raise ValueError("Smart quotes found in Divi content; refusing to continue")
    if 'type="4_4"' not in content:
        raise ValueError("The required full-width Divi column is missing")
    return content


def build_preview(preview_dir: Path) -> dict[str, str | int]:
    preview_dir.mkdir(parents=True, exist_ok=True)
    embed = (ROOT / "divi-embeds" / "library-divi.html").read_text(
        encoding="utf-8"
    )
    raw = divi_content(embed)

    local_embed = embed.replace(
        "https://seanmichael67.github.io/Spanish-Books/",
        "./library-index.html",
        1,
    )
    preview = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Spanish Books WordPress preview</title>
  <link rel="icon" href="data:,">
  <style>
    html, body {{ margin: 0; background: #fffdf7; }}
    body {{ padding: 20px; }}
    @media (max-width: 600px) {{ body {{ padding: 0; }} }}
  </style>
</head>
<body>
{local_embed}
</body>
</html>
"""
    (preview_dir / "preview.html").write_text(preview, encoding="utf-8")
    (preview_dir / "content.raw.txt").write_text(raw, encoding="utf-8")
    shutil.copy2(ROOT / "index.html", preview_dir / "library-index.html")
    manifest = {
        "page_id": PAGE_ID,
        "page_url": PAGE_URL,
        "source_embed": str(ROOT / "divi-embeds" / "library-divi.html"),
        "source_library": str(ROOT / "index.html"),
        "preview": str(preview_dir / "preview.html"),
        "content_raw_bytes": len(raw.encode("utf-8")),
        "apply_requested": False,
    }
    (preview_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def auth_header() -> str:
    user = os.environ.get("WP_BEIBEI_USER")
    password = os.environ.get("WP_BEIBEI_APP_PASSWORD")
    if not user or not password:
        raise SystemExit(
            "--apply requires WP_BEIBEI_USER and WP_BEIBEI_APP_PASSWORD"
        )
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    return f"Basic {token}"


def request_json(url: str, authorization: str, *, method: str = "GET", data=None):
    headers = {
        "Authorization": authorization,
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)


def get_content_raw(page: dict) -> str:
    """Return content.raw only; content.rendered must never be posted back."""
    raw = page.get("content", {}).get("raw")
    if not isinstance(raw, str):
        raise ValueError("Authenticated context=edit response did not include content.raw")
    return raw


def apply_live(raw: str) -> dict:
    authorization = auth_header()
    current = request_json(f"{API_URL}?context=edit", authorization)
    get_content_raw(current)

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup = BACKUP_DIR / f"spanish-books-{PAGE_ID}-{stamp}.json"
    backup.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")

    result = request_json(
        API_URL,
        authorization,
        method="PUT",
        data={"content": raw},
    )
    return {
        "id": result.get("id"),
        "slug": result.get("slug"),
        "link": result.get("link"),
        "backup": str(backup),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
        help="BACK UP content.raw and write the approved page to live WordPress",
    )
    parser.add_argument("--preview-dir", type=Path, default=PREVIEW_DIR)
    args = parser.parse_args()

    manifest = build_preview(args.preview_dir)
    print(json.dumps(manifest, indent=2))
    if not args.apply:
        print("Preview built; live WordPress was not changed.")
        return 0

    raw = (args.preview_dir / "content.raw.txt").read_text(encoding="utf-8")
    result = apply_live(raw)
    (args.preview_dir / "apply-result.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
