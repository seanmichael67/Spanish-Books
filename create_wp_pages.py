#!/usr/bin/env python3
"""Create WordPress pages for all Spanish preschool book embeds."""

import os, re, json, time, requests

BOOKS_DIR = os.path.expanduser("~/Projects/preschool-books/divi-embeds/books/")
WP_API = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"
AUTH = ("Luciano", "ZjjW wlE4 tNJa 5sQr F6ym fLtV")
PARENT = 1854

DIVI_WRAP = '[et_pb_section fb_built="1" _builder_version="4.27.4"][et_pb_row _builder_version="4.27.4"][et_pb_column type="4_4" _builder_version="4.27.4"][et_pb_code _builder_version="4.27.4"]\n{}\n[/et_pb_code][/et_pb_column][/et_pb_row][/et_pb_section]'

SESSION = requests.Session()
SESSION.headers['User-Agent'] = 'WordPress/6.0'
results = []

files = sorted(os.listdir(BOOKS_DIR))
print(f"Found {len(files)} files\n")

for i, fname in enumerate(files):
    if not fname.endswith(".html"):
        continue
    
    # Read content
    with open(os.path.join(BOOKS_DIR, fname), "r") as f:
        html = f.read()
    
    # Extract title from H1
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    title = m.group(1).strip() if m else fname.replace(".html", "")
    
    # Slug: remove week-XX- prefix and .html
    slug = re.sub(r'^week-\d+-', '', fname.replace('.html', ''))
    
    # Wrap in Divi
    content = DIVI_WRAP.format(html)
    
    # POST
    data = {
        "title": title,
        "slug": slug,
        "status": "publish",
        "parent": PARENT,
        "content": content,
    }
    
    try:
        r = SESSION.post(WP_API, auth=AUTH, json=data, timeout=30)
        if r.status_code == 201:
            page = r.json()
            url = page.get("link", "?")
            actual_slug = page.get("slug", "?")
            print(f"✅ [{i+1}/{len(files)}] {title} → {url}")
            if actual_slug != slug:
                print(f"   ⚠️  Slug changed: {slug} → {actual_slug}")
            results.append({"file": fname, "title": title, "slug": actual_slug, "url": url, "status": "ok"})
        else:
            print(f"❌ [{i+1}/{len(files)}] {title} — HTTP {r.status_code}: {r.text[:200]}")
            results.append({"file": fname, "title": title, "slug": slug, "status": "error", "code": r.status_code})
    except Exception as e:
        print(f"❌ [{i+1}/{len(files)}] {title} — {e}")
        results.append({"file": fname, "title": title, "slug": slug, "status": "error", "error": str(e)})
    
    # Small delay to be nice to the server
    time.sleep(1)

# Summary
ok = [r for r in results if r["status"] == "ok"]
err = [r for r in results if r["status"] != "ok"]
print(f"\n{'='*60}")
print(f"DONE: {len(ok)} created, {len(err)} failed out of {len(results)} total")
if err:
    print("\nFailed:")
    for e in err:
        print(f"  - {e['file']}: {e.get('code', e.get('error', '?'))}")

# Save results
with open(os.path.expanduser("~/Projects/preschool-books/wp_pages_results.json"), "w") as f:
    json.dump(results, f, indent=2)
print("\nResults saved to wp_pages_results.json")
