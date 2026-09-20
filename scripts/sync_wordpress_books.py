#!/usr/bin/env python3
"""Synchronize publication-ready Spanish books to Beibei WordPress.

Dry-run is the default. ``--apply`` is required for any WordPress write.
The command uses one WP-CLI PHP boot per inventory/apply operation, backs up
raw content and metadata before writes, and refuses concurrent drift.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
import zlib
from pathlib import Path
from typing import Any, Sequence

from book_catalog import (
    Book,
    Catalog,
    catalog_fingerprint,
    load_catalog,
    reconcile_wordpress_pages,
    render_book_page,
    render_hub,
    source_identity,
)

HUB_ID = 1854
WP_AUTHOR_ID = 9
WP_ROOT = "/home3/amicimon/beibeiamigos.com"
SSH_HOST = "amicimon@amicimontessori.com"
SSH_PORT = "2222"
SSH_KEY = str(Path.home() / ".ssh" / "id_rsa_hostgator")
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"
DURABLE_BACKUP_ROOT = Path.home() / ".hermes" / "backups" / "beibei-spanish-books"
TMP_BACKUP_ROOT = Path("/tmp/beibei-books-publish/backups")

INVENTORY_PHP = r'''<?php
global $wpdb;
$hub = get_post(%d);
if (!$hub) { fwrite(STDERR, "hub not found\n"); exit(2); }
$posts = get_posts([
  'post_type' => 'page',
  'post_parent' => %d,
  'post_status' => ['publish','draft','pending','private','future'],
  'numberposts' => -1,
  'orderby' => 'ID',
  'order' => 'ASC',
]);
function row_for($post) {
  return [
    'ID' => (int)$post->ID,
    'post_name' => $post->post_name,
    'post_status' => $post->post_status,
    'post_title' => $post->post_title,
    'post_excerpt' => $post->post_excerpt,
    'post_content' => $post->post_content,
    'post_modified_gmt' => $post->post_modified_gmt,
    'layout' => get_post_meta($post->ID, '_et_pb_page_layout', true),
    'builder' => get_post_meta($post->ID, '_et_pb_use_builder', true),
  ];
}
$table_engines = [];
foreach ([$wpdb->posts, $wpdb->postmeta] as $table_name) {
  $table_engines[$table_name] = $wpdb->get_var($wpdb->prepare(
    'SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %%s',
    $table_name
  ));
}
echo wp_json_encode([
  'hub' => row_for($hub),
  'pages' => array_map('row_for', $posts),
  'site_url' => get_site_url(),
  'table_engines' => $table_engines,
], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
''' % (HUB_ID, HUB_ID)


def utc_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def ssh_base_args() -> list[str]:
    return [
        "ssh", "-p", SSH_PORT, "-i", SSH_KEY,
        "-o", "IdentitiesOnly=yes", "-o", "IdentityAgent=none",
        "-o", "BatchMode=yes", "-o", "ConnectTimeout=20",
        SSH_HOST,
    ]


def scp_base_args() -> list[str]:
    return [
        "scp", "-P", SSH_PORT, "-i", SSH_KEY,
        "-o", "IdentitiesOnly=yes", "-o", "IdentityAgent=none",
        "-o", "BatchMode=yes", "-o", "ConnectTimeout=20",
    ]


def run_wp_php(code: str, timeout: int = 180) -> dict[str, Any]:
    token = hashlib.sha256(code.encode("utf-8")).hexdigest()[:12]
    local_path = Path(f"/tmp/beibei-book-sync-{os.getpid()}-{token}.php")
    remote_path = f"/tmp/beibei-book-sync-{os.getpid()}-{token}.php"
    local_path.write_text(code, encoding="utf-8")
    try:
        upload = subprocess.run(
            [*scp_base_args(), str(local_path), f"{SSH_HOST}:{remote_path}"],
            text=True, capture_output=True, timeout=60, check=False,
        )
        if upload.returncode != 0:
            raise RuntimeError(f"WP-CLI PHP upload failed: {upload.stderr.strip()}")
        result = subprocess.run(
            [*ssh_base_args(), f"cd {WP_ROOT} && wp eval-file {remote_path}"],
            text=True, capture_output=True, timeout=timeout, check=False,
        )
    finally:
        local_path.unlink(missing_ok=True)
        subprocess.run(
            [*ssh_base_args(), f"rm -f {remote_path}"],
            text=True, capture_output=True, timeout=30, check=False,
        )
    if result.returncode != 0:
        raise RuntimeError(
            f"WP-CLI PHP failed ({result.returncode}): {result.stderr.strip() or result.stdout.strip()}"
        )
    raw = result.stdout.strip()
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"WP-CLI returned non-JSON output: {raw[:500]}") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError("WP-CLI response was not a JSON object")
    return parsed


def fetch_live_inventory() -> dict[str, Any]:
    data = run_wp_php(INVENTORY_PHP)
    if not isinstance(data.get("hub"), dict) or not isinstance(data.get("pages"), list):
        raise RuntimeError("WordPress inventory response is incomplete")
    return data


def page_state(pages: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        [
            {
                "ID": int(page["ID"]),
                "post_name": str(page["post_name"]),
                "post_status": str(page["post_status"]),
                "post_modified_gmt": str(page["post_modified_gmt"]),
            }
            for page in pages
        ],
        key=lambda row: row["ID"],
    )


def build_apply_php(payload: dict[str, Any]) -> str:
    encoded = base64.b64encode(zlib.compress(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
        level=9,
    )).decode("ascii")
    return r'''<?php
global $wpdb;
$decoded_payload = gzuncompress(base64_decode('%s'));
$payload = $decoded_payload === false ? null : json_decode($decoded_payload, true);
if (!is_array($payload)) { fwrite(STDERR, "invalid compressed payload\n"); exit(2); }
$lock_name = 'beibei_spanish_books_sync_v2';
$lock_acquired = false;
$transaction_open = false;
$created = [];
function fail_sync($message) { throw new Exception($message); }
function exact_page_readback($id, $book, $expected_status) {
  $post = get_post($id);
  if (!$post) fail_sync('page missing during exact readback: ' . $id);
  if ((int)$post->post_parent !== (int)$book['post_parent']) fail_sync('parent mismatch for ' . $book['post_name']);
  if ($post->post_name !== $book['post_name']) fail_sync('slug mismatch for ' . $book['post_name']);
  if ($post->post_title !== $book['post_title']) fail_sync('title mismatch for ' . $book['post_name']);
  if ($post->post_excerpt !== $book['post_excerpt']) fail_sync('excerpt mismatch for ' . $book['post_name']);
  if ($post->post_status !== $expected_status) fail_sync('status mismatch for ' . $book['post_name']);
  if (hash('sha256', $post->post_content) !== $book['post_content_sha256']) fail_sync('raw content mismatch for ' . $book['post_name']);
  foreach ($book['required_markers'] as $marker) {
    if (strpos($post->post_content, $marker) === false) fail_sync('required marker missing for ' . $book['post_name'] . ': ' . $marker);
  }
  if (get_post_meta($id, '_et_pb_use_builder', true) !== 'off') fail_sync('builder flag mismatch for ' . $book['post_name']);
  if (get_post_meta($id, '_et_pb_page_layout', true) !== 'et_no_sidebar') fail_sync('layout flag mismatch for ' . $book['post_name']);
  return $post;
}
try {
  $got_lock = (int)$wpdb->get_var($wpdb->prepare('SELECT GET_LOCK(%%s, 0)', $lock_name));
  if ($got_lock !== 1) fail_sync('another Spanish-book sync holds the exclusive lock');
  $lock_acquired = true;
  foreach ([$wpdb->posts, $wpdb->postmeta] as $table_name) {
    $engine = $wpdb->get_var($wpdb->prepare(
      'SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %%s',
      $table_name
    ));
    if (strtoupper((string)$engine) !== 'INNODB') fail_sync('transactional apply requires InnoDB: ' . $table_name);
  }
  if ($wpdb->query('START TRANSACTION') === false) fail_sync('could not start transaction');
  $transaction_open = true;
  $hub_id = (int)$payload['hub_id'];
  $hub_row = $wpdb->get_row($wpdb->prepare(
    "SELECT ID, post_modified_gmt, post_content FROM {$wpdb->posts} WHERE ID = %%d FOR UPDATE",
    $hub_id
  ), ARRAY_A);
  if (!$hub_row) fail_sync('hub missing during locked apply');
  if ($hub_row['post_modified_gmt'] !== $payload['expected_hub_modified_gmt']) fail_sync('hub modified concurrently');
  if (hash('sha256', $hub_row['post_content']) !== $payload['expected_hub_sha256']) fail_sync('hub raw content changed concurrently');
  $locked_rows = $wpdb->get_results($wpdb->prepare(
    "SELECT ID, post_name, post_status, post_modified_gmt FROM {$wpdb->posts}
     WHERE post_type = 'page' AND post_parent = %%d
       AND post_status IN ('publish','draft','pending','private','future')
     ORDER BY ID FOR UPDATE",
    $hub_id
  ), ARRAY_A);
  $state = [];
  $existing_slugs = [];
  foreach ($locked_rows as $row) {
    $state[] = [
      'ID' => (int)$row['ID'], 'post_name' => $row['post_name'],
      'post_status' => $row['post_status'], 'post_modified_gmt' => $row['post_modified_gmt'],
    ];
    $existing_slugs[$row['post_name']] = (int)$row['ID'];
  }
  if (wp_json_encode($state, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) !== wp_json_encode($payload['expected_page_state'], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE)) {
    fail_sync('child page inventory changed before locked apply');
  }
  foreach ($payload['create'] as $book) {
    if (isset($existing_slugs[$book['post_name']])) fail_sync('slug already exists: ' . $book['post_name']);
    $book['post_parent'] = $hub_id;
    $id = wp_insert_post([
      'post_type' => 'page', 'post_parent' => $hub_id, 'post_author' => (int)$payload['author_id'],
      'post_status' => 'draft', 'post_name' => $book['post_name'],
      'post_title' => $book['post_title'], 'post_excerpt' => $book['post_excerpt'],
      'post_content' => $book['post_content'], 'comment_status' => 'closed', 'ping_status' => 'closed',
    ], true);
    if (is_wp_error($id)) fail_sync('draft create failed for ' . $book['post_name'] . ': ' . $id->get_error_message());
    update_post_meta($id, '_et_pb_use_builder', 'off');
    update_post_meta($id, '_et_pb_page_layout', 'et_no_sidebar');
    exact_page_readback($id, $book, 'draft');
    $created[] = ['ID' => (int)$id, 'post_name' => $book['post_name'], 'source_slug' => $book['source_slug'], 'status' => 'draft'];
    $existing_slugs[$book['post_name']] = (int)$id;
  }
  foreach ($created as &$created_row) {
    $book = null;
    foreach ($payload['create'] as $candidate) {
      if ($candidate['source_slug'] === $created_row['source_slug']) { $book = $candidate; break; }
    }
    if (!$book) fail_sync('created page payload disappeared for ' . $created_row['source_slug']);
    $book['post_parent'] = $hub_id;
    $result = wp_update_post(['ID' => $created_row['ID'], 'post_status' => 'publish'], true);
    if (is_wp_error($result)) fail_sync('publish failed for ' . $created_row['post_name'] . ': ' . $result->get_error_message());
    exact_page_readback($created_row['ID'], $book, 'publish');
    $created_row['status'] = 'publish';
  }
  unset($created_row);
  $hub_result = wp_update_post([
    'ID' => $hub_id, 'post_content' => $payload['hub_content'], 'post_excerpt' => $payload['hub_excerpt'],
  ], true);
  if (is_wp_error($hub_result)) fail_sync('hub update failed: ' . $hub_result->get_error_message());
  update_post_meta($hub_id, '_et_pb_use_builder', 'off');
  update_post_meta($hub_id, '_et_pb_page_layout', 'et_no_sidebar');
  $hub_after = get_post($hub_id);
  if (!$hub_after || hash('sha256', $hub_after->post_content) !== $payload['hub_content_sha256']) fail_sync('hub raw-content readback mismatch');
  if ($hub_after->post_excerpt !== $payload['hub_excerpt']) fail_sync('hub excerpt readback mismatch');
  if (get_post_meta($hub_id, '_et_pb_use_builder', true) !== 'off') fail_sync('hub builder flag mismatch');
  if (get_post_meta($hub_id, '_et_pb_page_layout', true) !== 'et_no_sidebar') fail_sync('hub layout flag mismatch');
  if ($wpdb->query('COMMIT') === false) fail_sync('transaction commit failed');
  $transaction_open = false;
  $wpdb->get_var($wpdb->prepare('SELECT RELEASE_LOCK(%%s)', $lock_name));
  $lock_acquired = false;
  echo wp_json_encode([
    'ok' => true, 'transaction_committed' => true, 'created' => $created,
    'hub_id' => $hub_id, 'hub_modified_gmt' => $hub_after->post_modified_gmt,
    'hub_sha256' => hash('sha256', $hub_after->post_content),
  ], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
} catch (Throwable $error) {
  if ($transaction_open) $wpdb->query('ROLLBACK');
  if ($lock_acquired) $wpdb->get_var($wpdb->prepare('SELECT RELEASE_LOCK(%%s)', $lock_name));
  echo wp_json_encode([
    'ok' => false, 'rolled_back' => $transaction_open,
    'error' => $error->getMessage(), 'attempted' => $created,
  ], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
}
''' % encoded


def reader_reachable(book: Book, timeout: int = 30) -> tuple[bool, str]:
    request = urllib.request.Request(
        book.reader_url,
        method="GET",
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = int(response.status)
            content_type = str(response.headers.get("Content-Type") or "").lower()
            body = response.read(750_000).decode("utf-8", errors="ignore")
    except (urllib.error.URLError, TimeoutError) as exc:
        return False, str(exc)
    if status != 200:
        return False, f"HTTP {status}"
    if "text/html" not in content_type:
        return False, f"unexpected content type {content_type or 'missing'}"
    if "<html" not in body.lower() and "<!doctype" not in body.lower():
        return False, "response is not HTML"
    if re.search(r"tutti[-_.]?sophia|sofia-fullscreen|AI Spanish Teacher|real AI tutor", body, re.I):
        return False, "reader contains a blocked tutor promotion"
    return True, f"HTTP {status} text/html promo-free"


def preview_document(title: str, raw_content: str) -> str:
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>body{{margin:0;background:#f7f7fb}}.preview-banner{{position:sticky;top:0;z-index:9999;background:#14213d;color:#fff;padding:8px 14px;font:700 14px system-ui}}.entry-title{{font:800 2.1rem system-ui;text-align:center;color:#2d2765;margin:28px 12px 8px}}</style></head><body><div class="preview-banner">LOCAL PREVIEW — NOT LIVE</div><h1 class="entry-title">{html.escape(title)}</h1>{raw_content}</body></html>'''


def write_previews(preview_dir: Path, catalog: Catalog, missing: Sequence[Book]) -> dict[str, str]:
    preview_dir.mkdir(parents=True, exist_ok=True)
    hub_path = preview_dir / "hub.html"
    hub_path.write_text(preview_document("Spanish Books", render_hub(catalog.ready)), encoding="utf-8")
    links = [f'<li><a href="hub.html">Library hub — {len(catalog.ready)} cards</a></li>']
    paths = {"hub": str(hub_path)}
    for book in missing:
        filename = f"book-{book.wp_slug}.html"
        path = preview_dir / filename
        path.write_text(preview_document(book.wordpress_title, render_book_page(book)), encoding="utf-8")
        links.append(f'<li><a href="{html.escape(filename)}">{html.escape(book.wordpress_title)}</a></li>')
        paths[book.source_slug] = str(path)
    index = preview_dir / "index.html"
    index.write_text(
        '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Beibei Spanish Books publication previews</title><style>body{font:18px/1.6 system-ui;max-width:850px;margin:40px auto;padding:0 20px}code{background:#eee;padding:2px 5px}</style>'
        f'<h1>Beibei Spanish Books publication previews</h1><p><strong>{len(catalog.ready)} ready</strong>; '
        f'<strong>{len(catalog.asset_incomplete)} asset-incomplete and gated</strong>.</p><ul>{"".join(links)}</ul>',
        encoding="utf-8",
    )
    paths["index"] = str(index)
    return paths


def save_backup(inventory: dict[str, Any], stamp: str) -> tuple[Path, Path]:
    payload = json.dumps(inventory, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    durable_dir = DURABLE_BACKUP_ROOT / stamp
    durable_dir.mkdir(parents=True, exist_ok=False)
    durable_path = durable_dir / "inventory-before.json"
    durable_path.write_text(payload, encoding="utf-8")
    TMP_BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    tmp_path = TMP_BACKUP_ROOT / f"inventory-before-{stamp}.json"
    tmp_path.write_text(payload, encoding="utf-8")
    return durable_path, tmp_path


def write_receipt(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)
    return path


def book_apply_row(book: Book) -> dict[str, Any]:
    content = render_book_page(book)
    return {
        "source_slug": book.source_slug,
        "post_name": book.wp_slug,
        "post_title": book.wordpress_title,
        "post_excerpt": book.description,
        "post_content": content,
        "post_content_sha256": sha256_text(content),
        "required_markers": [
            f"spanish-book-source:{book.source_slug}",
            "spanish-book-template:v2",
            "<iframe",
            book.reader_url,
            book.wordpress_url,
            '"@type":"Book"',
            '"@type":"LearningResource"',
        ],
    }


def verify_target_state(
    inventory: dict[str, Any],
    catalog: Catalog,
    created_books: Sequence[Book],
    hub_content: str,
    expected_created: Sequence[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    reconciliation = reconcile_wordpress_pages(catalog.ready, inventory["pages"])
    if reconciliation.unexpected_pages or reconciliation.missing:
        raise RuntimeError(
            f"target reconciliation failed: missing={[book.source_slug for book in reconciliation.missing]}, "
            f"unexpected={[page.get('ID') for page in reconciliation.unexpected_pages]}"
        )
    hub = inventory["hub"]
    expected_excerpt = (
        f"{len(catalog.ready)} free interactive Spanish and bilingual books "
        "for preschool children ages 2–5."
    )
    if str(hub.get("post_content")) != hub_content:
        raise RuntimeError("target hub raw content differs from generated content")
    if str(hub.get("post_excerpt")) != expected_excerpt:
        raise RuntimeError("target hub excerpt differs from generated excerpt")
    if str(hub.get("layout")) != "et_no_sidebar" or str(hub.get("builder")) != "off":
        raise RuntimeError("target hub Divi layout flags differ")

    expected_ids = {
        str(row["source_slug"]): int(row["ID"])
        for row in (expected_created or [])
    }
    if expected_created is not None and set(expected_ids) != {book.source_slug for book in created_books}:
        raise RuntimeError("committed created-page receipt does not match the planned source set")
    pages_by_source: dict[str, dict[str, Any]] = {}
    for page in inventory["pages"]:
        source = source_identity(str(page.get("post_content") or ""))
        if source:
            pages_by_source[source] = page
    verified: list[dict[str, Any]] = []
    for book in created_books:
        expected = book_apply_row(book)
        page = pages_by_source.get(book.source_slug)
        if not page:
            raise RuntimeError(f"created source is absent after apply: {book.source_slug}")
        if expected_created is not None and int(page["ID"]) != expected_ids[book.source_slug]:
            raise RuntimeError(f"created page ID changed for {book.source_slug}")
        exact_fields = {
            "post_name": expected["post_name"],
            "post_status": "publish",
            "post_title": expected["post_title"],
            "post_excerpt": expected["post_excerpt"],
            "post_content": expected["post_content"],
            "layout": "et_no_sidebar",
            "builder": "off",
        }
        mismatched = [key for key, value in exact_fields.items() if str(page.get(key)) != value]
        if mismatched:
            raise RuntimeError(f"exact raw page verification failed for {book.source_slug}: {mismatched}")
        missing_markers = [marker for marker in expected["required_markers"] if marker not in str(page["post_content"])]
        if missing_markers:
            raise RuntimeError(f"required raw markers missing for {book.source_slug}: {missing_markers}")
        verified.append({
            "ID": int(page["ID"]),
            "post_name": str(page["post_name"]),
            "source_slug": book.source_slug,
            "status": "publish",
            "post_content_sha256": expected["post_content_sha256"],
        })
    return verified


def inventory_matches_before(before: dict[str, Any], after: dict[str, Any]) -> bool:
    before_hub = before["hub"]
    after_hub = after["hub"]
    hub_keys = (
        "ID", "post_name", "post_status", "post_title", "post_excerpt",
        "post_content", "post_modified_gmt", "layout", "builder",
    )
    return (
        all(str(before_hub.get(key)) == str(after_hub.get(key)) for key in hub_keys)
        and page_state(before["pages"]) == page_state(after["pages"])
    )


def build_payload(
    inventory: dict[str, Any], catalog: Catalog, missing: Sequence[Book], hub_content: str,
) -> dict[str, Any]:
    hub = inventory["hub"]
    return {
        "hub_id": HUB_ID,
        "author_id": WP_AUTHOR_ID,
        "expected_hub_modified_gmt": hub["post_modified_gmt"],
        "expected_hub_sha256": sha256_text(str(hub["post_content"])),
        "expected_page_state": page_state(inventory["pages"]),
        "hub_content": hub_content,
        "hub_content_sha256": sha256_text(hub_content),
        "hub_excerpt": f"{len(catalog.ready)} free interactive Spanish and bilingual books for preschool children ages 2–5.",
        "create": [book_apply_row(book) for book in missing],
    }


def verify_live_url(
    url: str, markers: Sequence[str], timeout: int = 30,
) -> tuple[int, dict[str, bool]]:
    separator = "&" if "?" in url else "?"
    request = urllib.request.Request(
        f"{url}{separator}_cb={int(dt.datetime.now().timestamp())}",
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="ignore")
        return int(response.status), {marker: marker in body for marker in markers}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--inventory-json", type=Path, help="Use a saved inventory instead of SSH (offline only)")
    parser.add_argument("--preview-dir", type=Path, default=Path("/tmp/beibei-books-publish/preview"))
    parser.add_argument("--apply", action="store_true", help="Create missing pages and update the live hub")
    parser.add_argument("--skip-previews", action="store_true")
    parser.add_argument("--receipt", type=Path, help="Additional path for the final JSON receipt")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog = load_catalog(args.root)
    if args.inventory_json:
        inventory = json.loads(args.inventory_json.read_text(encoding="utf-8"))
        if args.apply:
            raise SystemExit("--apply cannot be combined with --inventory-json")
    else:
        inventory = fetch_live_inventory()

    table_engines = inventory.get("table_engines") or {}
    transactional_tables = bool(table_engines) and all(
        str(engine).upper() == "INNODB" for engine in table_engines.values()
    )
    if args.apply and not transactional_tables:
        raise RuntimeError(f"WordPress apply requires InnoDB posts/postmeta tables; found {table_engines}")

    reconciliation = reconcile_wordpress_pages(catalog.ready, inventory["pages"])
    if reconciliation.unexpected_pages:
        ids = [page.get("ID") for page in reconciliation.unexpected_pages]
        raise RuntimeError(f"unexpected WordPress child pages fail closed: {ids}")
    nonpublished = [
        page for page in inventory["pages"]
        if str(page.get("post_status")) != "publish"
    ]
    if nonpublished:
        raise RuntimeError(f"non-published child pages fail closed: {[page.get('ID') for page in nonpublished]}")

    hub_content = render_hub(catalog.ready)
    hub_needs_update = str(inventory["hub"]["post_content"]) != hub_content
    preview_paths: dict[str, str] = {}
    if not args.skip_previews:
        preview_paths = write_previews(args.preview_dir, catalog, reconciliation.missing)

    reachability = {}
    for book in reconciliation.missing:
        ok, detail = reader_reachable(book)
        reachability[book.source_slug] = {"ok": ok, "detail": detail, "url": book.reader_url}
        if not ok:
            raise RuntimeError(f"reader is not public for {book.source_slug}: {detail}")

    summary: dict[str, Any] = {
        "mode": "apply" if args.apply else "dry-run",
        "source_folders": len(catalog.all_source_folders),
        "ready": len(catalog.ready),
        "represented_before": len(reconciliation.represented),
        "missing_before": [book.source_slug for book in reconciliation.missing],
        "asset_incomplete_gated": list(catalog.asset_incomplete),
        "hub_cards_before": str(inventory["hub"]["post_content"]).count('class="bb-book-card"'),
        "hub_cards_after": len(catalog.ready),
        "hub_needs_update": hub_needs_update,
        "catalog_fingerprint": catalog_fingerprint(catalog.ready),
        "table_engines": table_engines,
        "transactional_tables": transactional_tables,
        "reachability": reachability,
        "preview_paths": preview_paths,
        "writes_planned": len(reconciliation.missing) + (1 if hub_needs_update else 0),
    }
    if not args.apply:
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    if not reconciliation.missing and not hub_needs_update:
        summary.update({"status": "NO_CHANGE", "writes_applied": 0})
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
        return 0

    stamp = utc_stamp()
    durable_backup, tmp_backup = save_backup(inventory, stamp)
    backup_dir = durable_backup.parent
    planned_books = tuple(reconciliation.missing)
    payload = build_payload(inventory, catalog, planned_books, hub_content)
    plan_receipt = write_receipt(backup_dir / "apply-plan.json", {
        "status": "PREPARED_NOT_MUTATED",
        "stamp": stamp,
        "backup": {"durable": str(durable_backup), "tmp": str(tmp_backup)},
        "expected_hub_sha256": payload["expected_hub_sha256"],
        "target_hub_sha256": payload["hub_content_sha256"],
        "planned_create": [
            {
                "source_slug": row["source_slug"],
                "post_name": row["post_name"],
                "post_content_sha256": row["post_content_sha256"],
            }
            for row in payload["create"]
        ],
    })

    recovered_inventory: dict[str, Any] | None = None
    try:
        apply_result = run_wp_php(build_apply_php(payload), timeout=300)
    except Exception as apply_error:
        unknown_path = write_receipt(backup_dir / "unknown-outcome.json", {
            "status": "UNKNOWN_OUTCOME_RECONCILING",
            "error": str(apply_error),
            "plan_receipt": str(plan_receipt),
            "backup": str(durable_backup),
        })
        try:
            recovered_inventory = fetch_live_inventory()
        except Exception as recovery_error:
            write_receipt(unknown_path, {
                "status": "UNKNOWN_OUTCOME_UNRECONCILED",
                "apply_error": str(apply_error),
                "recovery_error": str(recovery_error),
                "plan_receipt": str(plan_receipt),
                "backup": str(durable_backup),
            })
            raise RuntimeError(f"unknown WordPress outcome; inspect {unknown_path}") from apply_error
        try:
            recovered_created = verify_target_state(
                recovered_inventory, catalog, planned_books, hub_content
            )
        except Exception as target_error:
            if inventory_matches_before(inventory, recovered_inventory):
                write_receipt(unknown_path, {
                    "status": "NOT_COMMITTED_OR_ROLLED_BACK_VERIFIED",
                    "apply_error": str(apply_error),
                    "target_error": str(target_error),
                    "plan_receipt": str(plan_receipt),
                    "backup": str(durable_backup),
                })
                raise RuntimeError(f"WordPress mutation did not commit; verified receipt: {unknown_path}") from apply_error
            write_receipt(unknown_path, {
                "status": "AMBIGUOUS_STATE_FAIL_CLOSED",
                "apply_error": str(apply_error),
                "target_error": str(target_error),
                "observed_page_state": page_state(recovered_inventory["pages"]),
                "plan_receipt": str(plan_receipt),
                "backup": str(durable_backup),
            })
            raise RuntimeError(f"ambiguous WordPress state; inspect {unknown_path}") from apply_error
        apply_result = {
            "ok": True,
            "transaction_committed": True,
            "created": recovered_created,
            "recovered_unknown_outcome": True,
        }
        write_receipt(unknown_path, {
            "status": "COMMITTED_TARGET_RECOVERED",
            "apply_error": str(apply_error),
            "created": recovered_created,
            "plan_receipt": str(plan_receipt),
            "backup": str(durable_backup),
        })

    if not apply_result.get("ok") or not apply_result.get("transaction_committed"):
        failure_path = write_receipt(backup_dir / "apply-failure.json", {
            "status": "TRANSACTION_REPORTED_FAILURE_RECONCILING",
            "result": apply_result,
            "plan_receipt": str(plan_receipt),
            "backup": str(durable_backup),
        })
        try:
            rollback_inventory = fetch_live_inventory()
        except Exception as rollback_check_error:
            write_receipt(failure_path, {
                "status": "TRANSACTION_FAILURE_ROLLBACK_UNVERIFIED",
                "result": apply_result,
                "rollback_check_error": str(rollback_check_error),
                "plan_receipt": str(plan_receipt),
                "backup": str(durable_backup),
            })
            raise RuntimeError(f"WordPress transaction failed; rollback unverified: {failure_path}") from rollback_check_error
        rollback_verified = inventory_matches_before(inventory, rollback_inventory)
        write_receipt(failure_path, {
            "status": "ROLLED_BACK_VERIFIED" if rollback_verified else "ROLLBACK_MISMATCH_FAIL_CLOSED",
            "result": apply_result,
            "plan_receipt": str(plan_receipt),
            "backup": str(durable_backup),
            "observed_page_state": page_state(rollback_inventory["pages"]),
        })
        raise RuntimeError(f"WordPress transaction failed; inspect {failure_path}: {apply_result}")

    mutation_receipt = write_receipt(backup_dir / "mutation-receipt.json", {
        "status": "TRANSACTION_COMMITTED_PENDING_EXTERNAL_VERIFICATION",
        "created": apply_result.get("created", []),
        "hub_id": HUB_ID,
        "hub_sha256": payload["hub_content_sha256"],
        "recovered_unknown_outcome": bool(apply_result.get("recovered_unknown_outcome")),
        "plan_receipt": str(plan_receipt),
        "backup": str(durable_backup),
    })

    after = recovered_inventory or fetch_live_inventory()
    verified_created = verify_target_state(
        after, catalog, planned_books, hub_content, apply_result.get("created", [])
    )
    after_reconciliation = reconcile_wordpress_pages(catalog.ready, after["pages"])

    live_checks: dict[str, Any] = {}
    for created in verified_created:
        source = str(created["source_slug"])
        book = next(book for book in catalog.ready if book.source_slug == source)
        required_live_markers = [
            book.title,
            f"spanish-book-source:{book.source_slug}",
            "spanish-book-template:v2",
            book.reader_url,
            '"@type":"Book"',
            '"@type":"LearningResource"',
        ]
        status, markers = verify_live_url(book.wordpress_url, required_live_markers)
        live_checks[source] = {"url": book.wordpress_url, "status": status, "markers": markers}
        if status != 200 or not all(markers.values()):
            raise RuntimeError(f"live verification failed for {source}: {live_checks[source]}")
    hub_marker_text = f"{len(catalog.ready)} libros disponibles"
    hub_status, hub_markers = verify_live_url(
        "https://www.beibeiamigos.com/spanish-books/",
        [hub_marker_text, 'class="bb-book-grid"', 'spanish-books-hub:v2'],
    )
    if hub_status != 200 or not all(hub_markers.values()):
        raise RuntimeError(f"live hub verification failed: HTTP {hub_status}, markers={hub_markers}")

    summary.update({
        "status": "APPLIED_AND_VERIFIED",
        "writes_applied": len(verified_created) + (1 if hub_needs_update else 0),
        "created": verified_created,
        "represented_after": len(after_reconciliation.represented),
        "missing_after": [],
        "live_checks": live_checks,
        "hub_live": {
            "url": "https://www.beibeiamigos.com/spanish-books/",
            "status": hub_status,
            "markers": hub_markers,
        },
        "backup": {"durable": str(durable_backup), "tmp": str(tmp_backup)},
        "plan_receipt": str(plan_receipt),
        "mutation_receipt": str(mutation_receipt),
        "rollback": {
            "hub": f"restore post_content and excerpt for page {HUB_ID} from inventory-before.json, plus its layout/builder meta",
            "created_pages": [f"set page {row['ID']} ({row['post_name']}) back to draft; do not delete" for row in verified_created],
        },
    })
    receipt_path = write_receipt(backup_dir / "apply-receipt.json", summary)
    if args.receipt:
        write_receipt(args.receipt, summary)
    print(json.dumps({
        "status": summary["status"],
        "ready": summary["ready"],
        "created": summary["created"],
        "represented_after": summary["represented_after"],
        "hub_live": summary["hub_live"],
        "backup": summary["backup"],
        "receipt": str(receipt_path),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
