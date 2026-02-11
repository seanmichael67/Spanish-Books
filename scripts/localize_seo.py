#!/usr/bin/env python3
"""Localize SEO content for all Spanish book pages on beibeiamigos.com"""

import json
import urllib.request
import urllib.error
import base64
import re
import time

SITE = "https://www.beibeiamigos.com"
WP_USER = "Luciano"
WP_PASS = "ZjjW wlE4 tNJa 5sQr F6ym fLtV"
PARENT_ID = 1854
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()

TIER1 = [
    ("85254", "Scottsdale/Kierland"), ("85331", "Cave Creek/North Scottsdale"),
    ("85083", "Stetson Hills"), ("85085", "Norterra/North Gateway"),
    ("85050", "Desert Ridge"), ("85086", "Anthem"),
    ("85028", "Shadow Mountain"), ("85310", "Arrowhead Foothills"),
]
TIER2 = [
    ("85308", "Arrowhead Ranch"), ("85024", "Desert Ridge North"),
    ("85306", "North Glendale"), ("85020", "Sunnyslope"), ("85054", "City North"),
]
TIER3 = [
    ("85032", "Paradise Valley Village"), ("85029", "West Moon Valley"),
    ("85022", "Moon Valley South"), ("85027", "Deer Valley"),
    ("85023", "Moon Valley Central"), ("85051", "North Mountain"),
    ("85053", "North Phoenix"), ("85021", "North Central Phoenix"),
]

# Weighted pool: Tier1 appears 3x, Tier2 2x, Tier3 1x
POOL = TIER1 * 3 + TIER2 * 2 + TIER3

def wp_get(endpoint):
    req = urllib.request.Request(
        f"{SITE}/wp-json/wp/v2/{endpoint}",
        headers={"Authorization": f"Basic {AUTH}", "User-Agent": "WordPress/6.0"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())

def wp_update(page_id, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        f"{SITE}/wp-json/wp/v2/pages/{page_id}",
        data=body, method="POST",
        headers={"Authorization": f"Basic {AUTH}", "User-Agent": "WordPress/6.0", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())

def get_all_pages():
    pages = []
    for pg in range(1, 10):
        try:
            batch = wp_get(f"pages?parent={PARENT_ID}&per_page=100&page={pg}&status=publish&context=edit")
            pages.extend(batch)
            if len(batch) < 100:
                break
        except urllib.error.HTTPError:
            break
    return pages

def assign_areas(num_pages):
    """Deterministic unique area assignments for each page."""
    assignments = []
    pool_idx = 0
    used = set()
    for i in range(num_pages):
        count = 3 if i % 3 == 0 else 2
        selected = []
        while len(selected) < count:
            pick = POOL[pool_idx % len(POOL)]
            pool_idx += 1
            if pick not in selected:
                selected.append(pick)
        # Ensure unique combo
        key = tuple(sorted(s[0] for s in selected))
        while key in used:
            selected[-1] = POOL[pool_idx % len(POOL)]
            pool_idx += 1
            key = tuple(sorted(s[0] for s in selected))
        used.add(key)
        assignments.append(selected)
    return assignments

def guess_topic(title):
    """Extract a natural topic description from the book title."""
    # Title format: "emoji Name — English Name"
    t = title.lower()
    # Remove emoji
    t = re.sub(r'[^\w\s—\-]', '', t).strip()
    # Get English part after —
    if '—' in t:
        eng = t.split('—')[1].strip()
        return eng
    return "Spanish vocabulary"

def make_desc(title, topic, area1, area2):
    """Generate unique description based on page index hash."""
    templates = [
        f"Read {title.split('—')[0].strip()} with your little one! This free interactive Spanish book teaches {topic} vocabulary with audio pronunciation — perfect for bilingual families in the {area1} and {area2} area.",
        f"Discover {title.split('—')[0].strip()} — a free bilingual Spanish book with native audio! Your child will love learning about {topic}. Ideal for families near {area1} and {area2}.",
        f"Explore {title.split('—')[0].strip()}, a beautifully illustrated free Spanish book with native audio. Great for preschoolers learning about {topic} in {area1} and {area2}.",
        f"Help your child learn Spanish with {title.split('—')[0].strip()}! This free interactive book covers {topic} with audio pronunciation — loved by families in {area1} and {area2}.",
        f"{title.split('—')[0].strip()} is a free Spanish reading book with audio for kids. Teach your child about {topic} — designed for bilingual families in {area1} and {area2}.",
        f"Introduce your preschooler to {title.split('—')[0].strip()} — a free Spanish book featuring {topic} with native speaker audio. Popular with families in {area1} and {area2}.",
    ]
    idx = sum(ord(c) for c in title) % len(templates)
    return templates[idx]

def build_footer(areas):
    names = [a[1] for a in areas]
    if len(names) == 2:
        area_text = f"{names[0]} and {names[1]}"
    else:
        area_text = f"{names[0]}, {names[1]}, and {names[2]}"
    return f'''<div style="max-width:900px; margin:20px auto; text-align:center; padding:16px 24px; background:#f8f9fa; border-radius:12px;">
  <p style="color:#666; font-size:0.95rem; line-height:1.6; font-family:'Sour Gummy',sans-serif;">
    This free bilingual book is brought to you by <a href="https://www.beibeiamigos.com" style="color:#667eea; font-weight:700;">Beibei Amigos Language Preschool</a>, 
    North Phoenix's premier Spanish and Mandarin immersion school. Proudly serving families in {area_text}. 
    <a href="https://www.beibeiamigos.com/spanish-books/" style="color:#667eea;">Explore all our free Spanish books →</a>
  </p>
</div>'''

def build_schema(title, slug, areas):
    # Clean title
    clean = re.sub(r'[^\w\s—\-áéíóúñ]', '', title).strip()
    name_es = clean.split('—')[0].strip() if '—' in clean else clean
    name_en = clean.split('—')[1].strip() if '—' in clean else ""
    
    area_served = []
    for z, name in areas:
        area_served.append({
            "@type": "Place",
            "name": name + ", AZ",
            "address": {"@type": "PostalAddress", "postalCode": z, "addressRegion": "AZ", "addressCountry": "US"}
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": name_es,
        "alternateName": name_en,
        "author": {"@type": "Organization", "name": "Beibei Amigos Language Preschool", "url": "https://beibeiamigos.com"},
        "inLanguage": ["es", "en"],
        "audience": {"@type": "EducationalAudience", "educationalRole": "student", "suggestedMinAge": 2, "suggestedMaxAge": 5},
        "isAccessibleForFree": True,
        "url": f"{SITE}/spanish-books/{slug}/",
        "publisher": {
            "@type": "EducationalOrganization",
            "name": "Beibei Amigos Language Preschool",
            "url": "https://www.beibeiamigos.com",
            "areaServed": area_served
        }
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, indent=2, ensure_ascii=False) + '\n</script>'

def update_page_content(content, title, slug, areas, idx):
    topic = guess_topic(title)
    area1 = areas[0][1]
    area2 = areas[1][1]
    
    # 1. Update desc paragraph
    new_desc = make_desc(title, topic, area1, area2)
    content = re.sub(
        r'(<p class="desc">)\s*(.*?)\s*(</p>)',
        lambda m: m.group(1) + '\n' + new_desc + '\n' + m.group(3),
        content, count=1, flags=re.DOTALL
    )
    
    # 2. Remove existing localized footer if present (idempotent)
    content = re.sub(
        r'\n*<div style="max-width:900px; margin:20px auto; text-align:center; padding:16px 24px; background:#f8f9fa[^"]*">.*?</div>\s*',
        '\n', content, flags=re.DOTALL
    )
    
    # 3. Insert footer before Sofia CTA
    # Pattern: the Sofia CTA div
    sofia_pattern = r'(<div class="cta" style="background: linear-gradient\(135deg, #f093fb, #f5576c\))'
    m = re.search(sofia_pattern, content)
    if m:
        footer = build_footer(areas)
        content = content[:m.start()] + footer + '\n\n' + content[m.start():]
    else:
        # Fallback: insert before </div>\n\n<script
        fallback = r'(</div>\s*<script type="application/ld\+json")'
        m2 = re.search(fallback, content, re.DOTALL)
        if m2:
            footer = build_footer(areas)
            content = content[:m2.start()] + footer + '\n\n' + content[m2.start():]
    
    # 4. Replace schema (keep it inside [/et_pb_code])
    new_schema = build_schema(title, slug, areas)
    content = re.sub(
        r'<script type="application/ld\+json">\s*\{.*?\}\s*</script>',
        new_schema,
        content, count=1, flags=re.DOTALL
    )
    
    # Ensure schema is before [/et_pb_code], not after
    schema_match = re.search(r'(<script type="application/ld\+json">.*?</script>)', content, re.DOTALL)
    close_match = re.search(r'\[/et_pb_code\]', content)
    if schema_match and close_match and schema_match.start() > close_match.start():
        # Remove schema from current position and insert before [/et_pb_code]
        schema_text = schema_match.group(1)
        content = content[:schema_match.start()] + content[schema_match.end():]
        close_match2 = re.search(r'\[/et_pb_code\]', content)
        if close_match2:
            content = content[:close_match2.start()] + schema_text + '\n' + content[close_match2.start():]
    
    return content

def main():
    print("Fetching all Spanish book pages...")
    pages = get_all_pages()
    print(f"Found {len(pages)} pages")
    
    pages.sort(key=lambda p: p['id'])
    assignments = assign_areas(len(pages))
    
    successes = 0
    failures = []
    
    for i, page in enumerate(pages):
        pid = page['id']
        title = page['title']['raw']
        slug = page['slug']
        areas = assignments[i]
        content = page['content']['raw']
        
        area_str = ", ".join(f"{a[1]} ({a[0]})" for a in areas)
        print(f"[{i+1}/{len(pages)}] {title[:45]:45s} → {area_str}")
        
        try:
            new_content = update_page_content(content, title, slug, areas, i)
            wp_update(pid, {"content": new_content})
            print(f"  ✅")
            successes += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"  ❌ {e}")
            failures.append((title, str(e)))
    
    print(f"\nDone! {successes}/{len(pages)} updated, {len(failures)} failed")
    if failures:
        for t, e in failures:
            print(f"  FAIL: {t}: {e}")

if __name__ == "__main__":
    main()
