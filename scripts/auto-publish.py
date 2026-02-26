#!/usr/bin/env python3
"""Auto-publish a new book from daily/ to WordPress + Render.

Usage: python3 scripts/auto-publish.py daily/week-25-la-cocina-de-abuela
"""

import os, re, json, sys, subprocess, time

BOOKS_DIR = os.path.expanduser("~/Projects/preschool-books/books")
DIVI_DIR = os.path.expanduser("~/Projects/preschool-books/divi-embeds/books")
REPO_DIR = os.path.expanduser("~/Projects/preschool-books")
WP_API = "https://www.beibeiamigos.com/wp-json/wp/v2/pages"
AUTH = ("luciano", "ZjjW wlE4 tNJa 5sQr F6ym fLtV")
PARENT = 1854  # spanish-books parent page
RENDER_BASE = "https://spanish-books.onrender.com/books"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/auto-publish.py daily/week-25-la-cocina-de-abuela")
        sys.exit(1)

    daily_path = os.path.join(REPO_DIR, sys.argv[1])
    if not os.path.isdir(daily_path):
        print(f"ERROR: {daily_path} not found")
        sys.exit(1)

    folder_name = os.path.basename(daily_path)  # e.g. week-25-la-cocina-de-abuela
    config_path = os.path.join(daily_path, "config.json")
    book_html_path = os.path.join(daily_path, "book.html")

    if not os.path.exists(book_html_path):
        print(f"ERROR: {book_html_path} not found")
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    title = config["title"]
    english = config.get("englishTranslation", "")
    seo = config.get("seo", {})
    meta_title = seo.get("metaTitle", f"{title} - Free Spanish Book | Beibei Amigos")
    meta_desc = seo.get("metaDescription", f"Interactive Spanish book: {title}. Free for ages 2-5.")
    keywords = ", ".join(seo.get("keywords", []))
    topic = config.get("topic", "")
    vocab_list = config.get("newVocabulary", [])
    vocab_count = len(vocab_list)

    # Derive slug from folder name (remove week-XX- prefix)
    slug = re.sub(r'^week-\d+-', '', folder_name)
    wp_title = f"{title} — {english}" if english else title

    # Add emoji based on topic
    topic_emoji = {
        "Animals": "🐾", "Food": "🍎", "Food & Cooking": "🍳", "Nature": "🌿",
        "Family": "👨‍👩‍👧‍👦", "Colors": "🎨", "Numbers": "🔢", "Body": "🧍",
        "Emotions": "😊", "Weather": "🌤️", "Ocean": "🐙", "Insects": "🦋",
        "Plants": "🌻", "Water": "💧", "Shapes": "🔷",
    }
    emoji = topic_emoji.get(topic, "📚")
    wp_title_full = f"{emoji} {wp_title}"

    print(f"📚 Publishing: {wp_title_full}")
    print(f"   Slug: {slug}")
    print(f"   Topic: {topic}")
    print(f"   Vocab: {vocab_count} words")

    # Step 1: Copy book to books/ for Render
    dest_dir = os.path.join(BOOKS_DIR, folder_name)
    if not os.path.exists(dest_dir):
        subprocess.run(["cp", "-r", daily_path, dest_dir], check=True)
        # Rename book.html to index.html if needed
        book_in_dest = os.path.join(dest_dir, "book.html")
        index_in_dest = os.path.join(dest_dir, "index.html")
        if os.path.exists(book_in_dest) and not os.path.exists(index_in_dest):
            os.rename(book_in_dest, index_in_dest)
        print("   ✅ Copied to books/")
    else:
        print("   ⏭️  Already in books/")

    # Step 2: Create Divi embed HTML
    iframe_url = f"{RENDER_BASE}/{folder_name}/"
    
    # Build description from config
    desc_text = meta_desc

    divi_html = f"""<!-- {title} - Divi Code Module -->
<link href="https://fonts.googleapis.com/css2?family=Sour+Gummy:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
.entry-title, .et_pb_post_title, h1.entry-title {{ display: none !important; }}
.et_pb_section .et_pb_row {{ max-width: 100% !important; width: 100% !important; padding: 0 !important; }}
.et_pb_section {{ padding: 0 !important; }}
.et_pb_column {{ padding: 0 !important; }}
.et_pb_code_inner {{ padding: 0 !important; }}
.book-page {{ max-width: 100%; margin: 0 auto; font-family: 'Sour Gummy', sans-serif; color: #333; }}
.book-page h2 {{ font-size: 1.3rem; text-align: center; color: #667eea; margin-bottom: 24px; font-weight: 600; }}
.book-page .desc {{ font-size: 1rem; line-height: 1.7; color: #555; text-align: center; max-width: 700px; margin: 0 auto 32px; }}
.book-page iframe {{ display: block; margin: 0 auto 20px; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.12); width: 100%; }}
.book-page .cta {{ text-align: center; background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px 24px; border-radius: 20px; margin-bottom: 20px; }}
.book-page .cta h3 {{ color: white; font-size: 1.5rem; margin-bottom: 8px; }}
.book-page .cta p {{ color: rgba(255,255,255,0.9); margin-bottom: 20px; }}
.book-page .cta a {{ background: white; color: #764ba2; padding: 14px 32px; border-radius: 12px; font-weight: 800; text-decoration: none; font-size: 1rem; display: inline-block; }}
.book-page .back-link {{ text-align: center; margin-bottom: 20px; }}
.book-page .back-link a {{ color: #667eea; text-decoration: none; font-weight: 600; font-size: 1rem; }}
</style>

<div class="book-page">
<div class="back-link"><a href="/spanish-books/">← Back to All Books</a></div>

<iframe id="bookFrame" src="{iframe_url}" width="100%" style="border:none; max-width:100%; min-height:900px;" allow="autoplay" loading="lazy" title="{title} - Free Spanish Book for Preschoolers"></iframe>

<script>
window.addEventListener('message', function(e) {{
  if (e.data && e.data.type === 'resize' && e.data.height) {{
    document.getElementById('bookFrame').style.height = e.data.height + 'px';
  }}
}});
</script>

<h2>Free Interactive Spanish Book for Preschoolers</h2>
<p class="desc">{desc_text}</p>

<div class="cta">
<h3>📚 Explore More Spanish Books!</h3>
<p>We have 100+ free interactive books across 10 themes!</p>
<a href="/spanish-books/">Browse Full Library →</a>
</div>

<div class="cta" style="background: linear-gradient(135deg, #f093fb, #f5576c); margin-top: -12px;">
<h3>👩🏫 Meet Sofia — Your Child's AI Spanish Teacher!</h3>
<p>Sofia talks, listens, and plays with your child in real-time — making Spanish fun and natural!</p>
<a href="https://tutti-sophia.onrender.com/sofia-fullscreen.html" style="color: #f5576c;">Try Sofia Free →</a>
</div>
</div>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Book",
  "name": "{title}",
  "alternateName": "{english}",
  "author": {{
    "@type": "Organization",
    "name": "Beibei Amigos Language Preschool",
    "url": "https://beibeiamigos.com"
  }},
  "inLanguage": "es",
  "audience": {{
    "@type": "EducationalAudience",
    "educationalRole": "student",
    "suggestedMinAge": 2,
    "suggestedMaxAge": 5
  }},
  "isAccessibleForFree": true,
  "url": "https://www.beibeiamigos.com/spanish-books/{slug}/",
  "description": "{meta_desc}",
  "genre": ["Children's Literature", "Educational", "Bilingual"],
  "keywords": "{keywords}"
}}
</script>
"""

    # Save Divi embed
    divi_path = os.path.join(DIVI_DIR, f"{folder_name}.html")
    with open(divi_path, 'w') as f:
        f.write(divi_html)
    print("   ✅ Divi embed created")

    # Step 3: Publish to WordPress (using curl to avoid ModSecurity issues with Python requests)
    def wp_curl(method, url, data=None):
        cmd = ["curl", "-s", "-X", method, "-u", f"{AUTH[0]}:{AUTH[1]}", url]
        if data:
            cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(data)]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(r.stdout) if r.stdout.strip() else {}

    # Check if page already exists
    existing = wp_curl("GET", f"{WP_API}?slug={slug}&parent={PARENT}&_fields=id")
    
    wp_content = f'[et_pb_section fb_built="1" fullwidth="on" _builder_version="4.27.4"][et_pb_fullwidth_code _builder_version="4.27.4"]\n{divi_html}\n[/et_pb_fullwidth_code][/et_pb_section]'

    if isinstance(existing, list) and existing:
        pid = existing[0]['id']
    else:
        # Create draft first
        result = wp_curl("POST", WP_API, {
            "title": wp_title_full, "slug": slug, "status": "draft",
            "parent": PARENT, "content": "<p>Loading...</p>",
        })
        pid = result.get('id')
        if not pid:
            print(f"   ❌ WordPress draft failed: {result}")
            return False
        print(f"   ✅ Draft created (id={pid})")
        time.sleep(1)

    # Update with full content
    result = wp_curl("POST", f"{WP_API}/{pid}", {
        "content": wp_content, "title": wp_title_full, "status": "publish",
    })
    if result.get('id'):
        print(f"   ✅ WordPress published (id={pid})")
        results_path = os.path.join(REPO_DIR, "wp_pages_results.json")
        try:
            with open(results_path) as f:
                results = json.load(f)
        except:
            results = []
        results.append({
            "file": f"{folder_name}.html", "title": wp_title_full, "slug": slug,
            "url": f"https://www.beibeiamigos.com/spanish-books/{slug}/", "status": "ok"
        })
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
    else:
        print(f"   ❌ WordPress publish failed: {str(result)[:200]}")
        return False

    # Step 4: Git commit and push (triggers Render deploy)
    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"📚 Auto-publish: {wp_title_full}"], check=True)
    result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ Pushed to GitHub (Render will auto-deploy)")
    else:
        print(f"   ⚠️  Git push: {result.stderr[:200]}")

    print(f"\n🎉 Published! https://www.beibeiamigos.com/spanish-books/{slug}/")
    return True

if __name__ == "__main__":
    main()
