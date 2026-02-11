#!/usr/bin/env python3
"""Generate images for a book using Gemini API."""
import json, sys, os, time, base64, urllib.request, urllib.error

API_KEY = os.environ.get('GOOGLE_API_KEY') or os.environ.get('GEMINI_API_KEY', '')

def generate_images(config_path):
    with open(config_path) as f:
        config = json.load(f)
    
    slug = config['slug']
    img_dir = os.path.join(os.path.dirname(__file__), '..', 'books', slug, 'images')
    os.makedirs(img_dir, exist_ok=True)
    
    for i, page in enumerate(config['pages']):
        if 'prompt' not in page:
            continue
        
        out_path = os.path.join(img_dir, f'page-{str(i).zfill(2)}.png')
        if os.path.exists(out_path):
            print(f"  ⏭️  Page {i} already exists, skipping")
            continue
        
        print(f"  🎨 Generating page {i}: {page['title']}...")
        
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={API_KEY}'
        payload = json.dumps({
            'contents': [{'parts': [{'text': f"Generate a high quality image: {page['prompt']}"}]}],
            'generationConfig': {'responseModalities': ['IMAGE', 'TEXT']}
        }).encode()
        
        for attempt in range(10):
            try:
                req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = json.loads(resp.read())
                
                for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
                    if 'inlineData' in part:
                        img_bytes = base64.b64decode(part['inlineData']['data'])
                        with open(out_path, 'wb') as f:
                            f.write(img_bytes)
                        print(f"  ✅ Page {i} saved ({len(img_bytes)//1024}KB)")
                        break
                else:
                    print(f"  ⚠️  Page {i}: No image in response, attempt {attempt+1}")
                    time.sleep(10)
                    continue
                break
            except Exception as e:
                wait = min(30 + attempt * 15, 120)
                print(f"  ❌ Page {i} attempt {attempt+1}: {e} (waiting {wait}s)")
                time.sleep(wait)
    
    print(f"✅ Done: {slug}")

if __name__ == '__main__':
    generate_images(sys.argv[1])
