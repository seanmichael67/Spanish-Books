#!/usr/bin/env python3
"""Localize SEO content for all Spanish book pages on beibeiamigos.com"""

import json
import urllib.request
import urllib.error
import base64
import re
import random
import time

SITE = "https://www.beibeiamigos.com"
WP_USER = "Luciano"
WP_PASS = "ZjjW wlE4 tNJa 5sQr F6ym fLtV"
PARENT_ID = 1854
AUTH = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()

TIER1 = [
    ("85254", "Scottsdale/Kierland"),
    ("85331", "Cave Creek/North Scottsdale"),
    ("85083", "Stetson Hills"),
    ("85085", "Norterra/North Gateway"),
    ("85050", "Desert Ridge"),
    ("85086", "Anthem"),
    ("85028", "Shadow Mountain"),
    ("85310", "Arrowhead Foothills"),
]
TIER2 = [
    ("85308", "Arrowhead Ranch"),
    ("85024", "Desert Ridge North"),
    ("85306", "North Glendale"),
    ("85020", "Sunnyslope"),
    ("85054", "City North"),
]
TIER3 = [
    ("85032", "Paradise Valley Village"),
    ("85029", "West Moon Valley"),
    ("85022", "Moon Valley South"),
    ("85027", "Deer Valley"),
    ("85023", "Moon Valley Central"),
    ("85051", "North Mountain"),
    ("85053", "North Phoenix"),
    ("85021", "North Central Phoenix"),
]

ALL_ZIPS = TIER1 + TIER2 + TIER3

# Book-specific description templates
DESC_TEMPLATES = [
    "Read {title} with your little one! This free interactive Spanish book teaches {topic} vocabulary with audio pronunciation — perfect for bilingual families in the {area1} and {area2} area.",
    "Discover {title} — a free bilingual Spanish book with audio! Your child will love learning {topic} words. Ideal for families near {area1} and {area2}.",
    "Explore {title}, a beautifully illustrated free Spanish book with native audio. Great for preschoolers learning {topic} vocabulary in {area1} and {area2}.",
    "Help your child learn Spanish with {title}! This free interactive book covers {topic} with audio pronunciation — loved by families in {area1} and {area2}.",
    "{title} is a free Spanish reading book with audio for kids. Teach your child {topic} words — designed for bilingual families in {area1}, {area2}.",
    "Introduce your preschooler to {title} — a free Spanish book featuring {topic} with native speaker audio. Popular with families in {area1} and {area2}.",
]

# Topic guesses from common book titles
TOPIC_MAP = {
    "oso": "bear and animal", "gato": "cat and pet", "perro": "dog and pet",
    "colores": "color", "numeros": "number and counting", "frutas": "fruit and food",
    "familia": "family", "cuerpo": "body part", "ropa": "clothing",
    "casa": "house and home", "comida": "food", "animales": "animal",
    "granja": "farm animal", "mar": "ocean and sea", "playa": "beach",
    "dinosaurio": "dinosaur", "mariposa": "butterfly and insect", "pajaro": "bird",
    "arbol": "tree and nature", "flor": "flower", "estrella": "star and space",
    "luna": "moon and night", "sol": "sun and weather", "lluvia": "rain and weather",
    "nieve": "snow and winter", "primavera": "spring", "verano": "summer",
    "otono": "autumn", "invierno": "winter", "escuela": "school",
    "juguete": "toy", "musica": "music", "deporte": "sport",
    "vehiculo": "vehicle", "tren": "train", "avion": "airplane",
    "barco": "boat", "bicicleta": "bicycle", "zapato": "shoe",
    "sombrero": "hat", "libro": "book and reading", "agua": "water",
    "leche": "milk", "pan": "bread", "huevo": "egg",
    "pollo": "chicken", "pez": "fish", "rana": "frog",
    "tortuga": "turtle", "conejo": "rabbit", "caballo": "horse",
    "vaca": "cow", "cerdo": "pig", "oveja": "sheep",
    "leon": "lion", "elefante": "elephant", "mono": "monkey",
    "jirafa": "giraffe", "serpiente": "snake", "arana": "spider",
}

def guess_topic(title):
    slug = title.lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    for key, topic in TOPIC_MAP.items():
        if key in slug:
            return topic
    return "Spanish language"

def wp_request(endpoint, method="GET", data=None):
    url = f"{SITE}/wp-json/wp/v2/{endpoint}"
    headers = {
        "Authorization": f"Basic {AUTH}",
        "User-Agent": "WordPress/6.0",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  HTTP {e.code}: {body[:300]}")
        raise

def get_all_pages():
    pages = []
    page_num = 1
    while True:
        batch = wp_request(f"pages?parent={PARENT_ID}&per_page=100&page={page_num}&status=publish")
        if not batch:
            break
        pages.extend(batch)
        if len(batch) < 100:
            break
        page_num += 1
    return pages

def assign_zips(num_pages):
    """Assign 2-3 zip/area combos per page, rotating with Tier 1 emphasis."""
    assignments = []
    # Build weighted pool: Tier1 x3, Tier2 x2, Tier3 x1
    pool = TIER1 * 3 + TIER2 * 2 + TIER3
    random.seed(42)  # reproducible
    random.shuffle(pool)
    
    idx = 0
    used_combos = set()
    for i in range(num_pages):
        count = 2 if i % 3 != 0 else 3
        selected = []
        attempts = 0
        while len(selected) < count and attempts < 50:
            pick = pool[idx % len(pool)]
            idx += 1
            if pick not in selected:
                selected.append(pick)
            attempts += 1
        # Make combo unique
        combo_key = tuple(sorted(z[0] for z in selected))
        while combo_key in used_combos and attempts < 100:
            selected[-1] = pool[idx % len(pool)]
            idx += 1
            combo_key = tuple(sorted(z[0] for z in selected))
            attempts += 1
        used_combos.add(combo_key)
        assignments.append(selected)
    return assignments

def build_footer(areas):
    area_names = [a[1] for a in areas]
    if len(area_names) == 2:
        area_text = f"{area_names[0]} and {area_names[1]}"
    else:
        area_text = f"{area_names[0]}, {area_names[1]}, and {area_names[2]}"
    
    return f'''<div style="max-width:900px; margin:20px auto; text-align:center; padding:16px 24px; background:#f8f9fa; border-radius:12px;">
  <p style="color:#666; font-size:0.95rem; line-height:1.6; font-family:'Sour Gummy',sans-serif;">
    This free bilingual book is brought to you by <a href="https://www.beibeiamigos.com" style="color:#667eea; font-weight:700;">Beibei Amigos Language Preschool</a>, 
    North Phoenix's premier Spanish and Mandarin immersion school. Proudly serving families in {area_text}. 
    <a href="https://www.beibeiamigos.com/spanish-books/" style="color:#667eea;">Explore all our free Spanish books →</a>
  </p>
</div>'''

def build_schema(title, slug, areas):
    area_served = []
    for z, name in areas:
        area_served.append({
            "@type": "Place",
            "name": name,
            "address": {
                "@type": "PostalAddress",
                "postalCode": z,
                "addressRegion": "AZ",
                "addressCountry": "US"
            }
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": title,
        "url": f"{SITE}/spanish-books/{slug}/",
        "inLanguage": ["es", "en"],
        "isAccessibleForFree": True,
        "audience": {
            "@type": "EducationalAudience",
            "educationalRole": "student",
            "suggestedAge": "2-6"
        },
        "publisher": {
            "@type": "EducationalOrganization",
            "name": "Beibei Amigos Language Preschool",
            "url": "https://www.beibeiamigos.com",
            "areaServed": area_served
        }
    }
    return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

def update_content(content, title, slug, areas, page_idx):
    topic = guess_topic(title)
    area_names = [a[1] for a in areas]
    
    # Build new description
    template = DESC_TEMPLATES[page_idx % len(DESC_TEMPLATES)]
    new_desc = template.format(
        title=title,
        topic=topic,
        area1=area_names[0],
        area2=area_names[1] if len(area_names) > 1 else "North Phoenix"
    )
    
    # Remove any existing localized footer (idempotent)
    content = re.sub(
        r'<div style="max-width:900px; margin:20px auto; text-align:center; padding:16px 24px; background:#f8f9fa[^"]*">\s*<p[^>]*>.*?This free bilingual book is brought to you by.*?</p>\s*</div>',
        '', content, flags=re.DOTALL
    )
    
    # Remove existing schema
    content = re.sub(r'<script type="application/ld\+json">.*?</script>', '', content, flags=re.DOTALL)
    
    # Build footer and schema
    footer = build_footer(areas)
    schema = build_schema(title, slug, areas)
    
    # Try to update existing description paragraph
    # Look for common desc patterns
    desc_updated = False
    # Pattern: paragraph containing "free" and "Spanish" or "book"
    desc_pattern = r'(<p[^>]*style="[^"]*color:#[56789a-f]{3,6}[^"]*font-size:0\.9[0-9]*rem[^"]*">)(.*?)(</p>)'
    def replace_desc(m):
        nonlocal desc_updated
        # Only replace the first matching desc-like paragraph
        if not desc_updated and ('book' in m.group(2).lower() or 'spanish' in m.group(2).lower() or 'read' in m.group(2).lower() or 'bilingual' in m.group(2).lower()):
            desc_updated = True
            return m.group(1) + new_desc + m.group(3)
        return m.group(0)
    
    content = re.sub(desc_pattern, replace_desc, content, flags=re.DOTALL)
    
    # Insert footer before Sofia CTA or at end
    # Look for Sofia iframe/embed or "sofia" reference
    sofia_pattern = r'(<(?:div|iframe)[^>]*(?:sofia|tutti-sophia|chat)[^>]*>)'
    sofia_match = re.search(sofia_pattern, content, re.IGNORECASE)
    
    if sofia_match:
        insert_pos = sofia_match.start()
        # Find the parent div start before sofia
        # Look backwards for a div that wraps the sofia section
        preceding = content[:insert_pos]
        # Find last <div before sofia
        last_div = preceding.rfind('<div')
        if last_div > 0 and insert_pos - last_div < 500:
            insert_pos = last_div
        content = content[:insert_pos] + footer + "\n" + content[insert_pos:]
    else:
        # Insert before closing shortcode or at end
        # Look for closing Divi shortcodes
        close_patterns = [r'\[/et_pb_code\]', r'\[/et_pb_text\]', r'</div>\s*$']
        inserted = False
        for cp in close_patterns:
            m = re.search(cp, content)
            if m:
                content = content[:m.start()] + "\n" + footer + "\n" + content[m.start():]
                inserted = True
                break
        if not inserted:
            content = content + "\n" + footer
    
    # Add schema at the very end
    content = content + "\n" + schema
    
    return content

def main():
    print("Fetching all Spanish book pages...")
    pages = get_all_pages()
    print(f"Found {len(pages)} pages")
    
    if not pages:
        print("No pages found!")
        return
    
    # Sort by ID for consistency
    pages.sort(key=lambda p: p['id'])
    
    # Assign zips
    assignments = assign_zips(len(pages))
    
    successes = []
    failures = []
    
    for i, page in enumerate(pages):
        pid = page['id']
        title = page['title']['rendered']
        slug = page['slug']
        areas = assignments[i]
        area_str = ", ".join(f"{a[1]} ({a[0]})" for a in areas)
        
        print(f"\n[{i+1}/{len(pages)}] {title} (ID:{pid}) → {area_str}")
        
        try:
            content = page['content']['rendered']
            new_content = update_content(content, title, slug, areas, i)
            
            # Update via API
            wp_request(f"pages/{pid}", method="POST", data={"content": new_content})
            print(f"  ✅ Updated")
            successes.append(title)
            time.sleep(0.5)  # rate limit
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            failures.append((title, str(e)))
    
    print(f"\n{'='*50}")
    print(f"Done! {len(successes)} updated, {len(failures)} failed")
    if failures:
        print("Failures:")
        for t, e in failures:
            print(f"  - {t}: {e}")

if __name__ == "__main__":
    main()
