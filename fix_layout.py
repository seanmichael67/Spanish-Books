#!/usr/bin/env python3
"""Move book description text below the iframe on all WP book pages.
Layout: back-link → iframe+script → h2 → desc → CTAs
"""
import json, re, subprocess, time, sys

AUTH = "luciano:ZjjW wlE4 tNJa 5sQr F6ym fLtV"
BASE = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"

def wp_get(url):
    r = subprocess.run(["curl", "-s", "-u", AUTH, url], capture_output=True, text=True, timeout=30)
    return json.loads(r.stdout)

def wp_post(url, data):
    r = subprocess.run(
        ["curl", "-s", "-u", AUTH, "-X", "POST", url,
         "-H", "Content-Type: application/json",
         "-d", json.dumps(data)],
        capture_output=True, text=True, timeout=30
    )
    return json.loads(r.stdout) if r.stdout.strip() else None

# 1. Get all child pages of spanish-books (parent=1854)
all_pages = []
for pg in range(1, 5):
    data = wp_get(f"{BASE}?parent=1854&per_page=100&page={pg}&_fields=id,slug")
    if not data or isinstance(data, dict):  # error response
        break
    all_pages.extend(data)

print(f"Found {len(all_pages)} book pages")

dry_run = "--dry-run" in sys.argv
if dry_run:
    print("DRY RUN MODE")

updated = 0
skipped = 0
errors = 0

for pg in all_pages:
    pid = pg['id']
    slug = pg['slug']
    
    data = wp_get(f"{BASE}/{pid}?_fields=id,content")
    raw = data['content']['rendered']
    
    # Find h2 and desc
    h2_match = re.search(r'<h2>[^<]*</h2>', raw)
    desc_match = re.search(r'<p class="desc">\s*.*?\s*</p>', raw, re.DOTALL)
    iframe_match = re.search(r'<iframe[^>]*id="bookFrame"', raw)
    
    if not iframe_match:
        print(f"  SKIP {slug}: no iframe")
        skipped += 1
        continue
    
    if not h2_match or not desc_match:
        print(f"  SKIP {slug}: no h2/desc (h2={h2_match is not None}, desc={desc_match is not None})")
        skipped += 1
        continue
    
    # Already fixed?
    if h2_match.start() > iframe_match.start():
        print(f"  OK   {slug}: already fixed")
        skipped += 1
        continue
    
    h2_text = h2_match.group(0)
    desc_text = desc_match.group(0)
    
    # Remove h2 and desc from current position (remove desc first since it's after h2)
    new_content = raw[:desc_match.start()] + raw[desc_match.end():]
    # Now remove h2 (position unchanged since desc was after)
    h2_in_new = re.search(re.escape(h2_text), new_content)
    if h2_in_new:
        new_content = new_content[:h2_in_new.start()] + new_content[h2_in_new.end():]
    
    # Clean empty paragraphs
    new_content = re.sub(r'<p>\s*</p>', '', new_content)
    
    # Find insert point: after the resize script block
    script_match = re.search(r'(?:<p>)?<script>\s*window\.addEventListener.*?</script>(?:</p>)?', new_content, re.DOTALL)
    if script_match:
        insert_pos = script_match.end()
    else:
        # Fallback: after iframe closing tag
        iframe_end = re.search(r'</iframe>', new_content)
        insert_pos = iframe_end.end() if iframe_end else None
    
    if insert_pos is None:
        print(f"  SKIP {slug}: can't find insert point")
        skipped += 1
        continue
    
    # Insert h2 and desc after iframe/script
    new_content = new_content[:insert_pos] + f'\n{h2_text}\n{desc_text}\n' + new_content[insert_pos:]
    
    if dry_run:
        print(f"  WOULD UPDATE {slug} (pid={pid})")
        updated += 1
        continue
    
    # Update via WP API
    result = wp_post(f"{BASE}/{pid}", {"content": new_content})
    if result and 'id' in result:
        print(f"  ✅ {slug}")
        updated += 1
    else:
        print(f"  ❌ {slug}: {str(result)[:200]}")
        errors += 1
    
    time.sleep(0.5)

print(f"\nDone! Updated: {updated}, Skipped: {skipped}, Errors: {errors}")
