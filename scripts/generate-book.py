#!/usr/bin/env python3
"""Generate a new book HTML from a config dict."""
import json, sys, os, re

def generate_book(config):
    """config = { slug, title, subtitle, theme, week, emoji, 
                  meta_desc, keywords, pages: [{title, footer, prompt}...], 
                  vocab: [{es, en, emoji}...], badge: {emoji, name, nameEn} }"""
    
    slug = config['slug']
    title = config['title']
    
    # Build pages JSON
    pages = []
    for p in config['pages']:
        pages.append(p)
    
    # Add vocab page
    pages.append({
        'title': 'Mis Palabras',
        'footer': 'My Words', 
        'type': 'vocab',
        'words': config['vocab']
    })
    
    # Add badge page
    pages.append({
        'title': '¡Ganaste tu insignia!',
        'footer': 'You earned your badge!',
        'type': 'badge',
        'badgeEmoji': config['badge']['emoji'],
        'badgeName': config['badge']['name'],
        'badgeNameEn': config['badge']['nameEn']
    })
    
    pages_json = json.dumps(pages, ensure_ascii=False, indent=16)
    
    # Read template
    template_path = os.path.join(os.path.dirname(__file__), '..', 'books', 'week-01-el-oso', 'index.html')
    with open(template_path) as f:
        html = f.read()
    
    # Replace meta tags
    html = re.sub(r'<title>.*?</title>', f'<title>{title} - Learn Spanish for Preschoolers | Beibei Amigos</title>', html)
    html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{config.get("meta_desc", "")}">', html)
    html = re.sub(r'<meta name="keywords" content=".*?">', f'<meta name="keywords" content="{config.get("keywords", "")}">', html)
    html = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title} - Learn Spanish | Beibei Amigos">', html)
    html = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="Free interactive Spanish book for preschoolers. {config.get("meta_desc", "")}">', html)
    html = re.sub(r'<meta property="og:url" content=".*?">', f'<meta property="og:url" content="https://spanish-books.onrender.com/books/{slug}/">', html)
    html = re.sub(r'<link rel="canonical" href=".*?">', f'<link rel="canonical" href="https://spanish-books.onrender.com/books/{slug}/">', html)
    
    # Replace BOOK_CONFIG
    config_block = f'''const BOOK_CONFIG = {{
            slug: "{slug}",
            title: "{title}",
            schoolName: "Beibei Amigos Language Preschool",
            websiteUrl: "https://www.beibeiamigos.com",
            logoUrl: "https://www.beibeiamigos.com/wp-content/uploads/2025/12/ChatGPT-Image-Aug-18-2025-05_26_03-PM.png",
            pages: {pages_json}
        }};'''
    
    html = re.sub(r'const BOOK_CONFIG = \{.*?\};', config_block, html, flags=re.DOTALL)
    
    # Fix share links
    html = html.replace('week-01-el-oso', slug)
    html = html.replace("El_Oso_Beibei", f"{title.replace(' ', '_')}_Beibei")
    
    # Write output
    book_dir = os.path.join(os.path.dirname(__file__), '..', 'books', slug)
    os.makedirs(os.path.join(book_dir, 'images'), exist_ok=True)
    
    with open(os.path.join(book_dir, 'index.html'), 'w') as f:
        f.write(html)
    
    print(f"✅ Created books/{slug}/index.html")
    return book_dir

if __name__ == '__main__':
    config_file = sys.argv[1]
    with open(config_file) as f:
        config = json.load(f)
    generate_book(config)
