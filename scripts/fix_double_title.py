#!/usr/bin/env python3
"""Update all WP book pages with H1-removed embed content."""
import json, urllib.request, base64, os, re, glob

WP_USER = "Luciano"
WP_PASS = "ZjjW wlE4 tNJa 5sQr F6ym fLtV"
AUTH = "Basic " + base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()

embed_dir = os.path.expanduser("~/Projects/preschool-books/divi-embeds/books/")

# Get all WP book pages using search to avoid the Divi PHP bug
# We'll just update each page by finding its embed file via slug
results_file = os.path.expanduser("~/Projects/preschool-books/wp_pages_results.json")
if os.path.exists(results_file):
    with open(results_file) as f:
        results = json.load(f)
else:
    results = []

# Build slug->id map from results
slug_to_id = {}
for r in results:
    if 'wp_id' in r:
        slug_to_id[r['slug']] = r['wp_id']

# Also try to get pages from WP API with error handling
try:
    req = urllib.request.Request(
        "https://www.beibeiamigos.com/wp-json/wp/v2/pages?parent=1854&per_page=100&status=publish&_fields=id,slug",
        headers={"Authorization": AUTH, "User-Agent": "WordPress/6.0"}
    )
    resp = urllib.request.urlopen(req)
    # Skip any PHP warnings
    raw = resp.read().decode()
    json_start = raw.find('[')
    if json_start >= 0:
        pages = json.loads(raw[json_start:])
        for p in pages:
            wp_slug = p['slug']
            slug_to_id[wp_slug] = p['id']
except Exception as e:
    print(f"Warning: Could not fetch pages from API: {e}")

print(f"Found {len(slug_to_id)} page mappings")

# Update each page
updated = 0
errors = 0
for filepath in sorted(glob.glob(os.path.join(embed_dir, "*.html"))):
    with open(filepath) as f:
        html = f.read()
    
    # Extract slug from filename (remove week-XX- prefix)
    fname = os.path.basename(filepath).replace('.html', '')
    slug = re.sub(r'^week-\d+-', '', fname)
    
    if slug not in slug_to_id:
        continue
    
    page_id = slug_to_id[slug]
    
    divi_content = '[et_pb_section fb_built="1" _builder_version="4.27.4"][et_pb_row _builder_version="4.27.4"][et_pb_column type="4_4" _builder_version="4.27.4"][et_pb_code _builder_version="4.27.4"]' + html + '[/et_pb_code][/et_pb_column][/et_pb_row][/et_pb_section]'
    
    data = json.dumps({"content": divi_content}).encode()
    req = urllib.request.Request(
        f"https://www.beibeiamigos.com/wp-json/wp/v2/pages/{page_id}",
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": AUTH,
            "User-Agent": "WordPress/6.0"
        }
    )
    try:
        resp = urllib.request.urlopen(req)
        # Skip PHP warnings in response
        raw = resp.read().decode()
        updated += 1
        if updated % 10 == 0:
            print(f"  Updated {updated} pages...")
    except Exception as e:
        errors += 1
        print(f"  ❌ {slug} (ID {page_id}): {e}")

print(f"\nDone: {updated} updated, {errors} errors")
