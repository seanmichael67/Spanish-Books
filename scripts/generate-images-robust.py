#!/usr/bin/env python3
"""Generate images for a book using Gemini API with robust retry."""
import json, sys, os, time, base64, urllib.request, urllib.error

API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY', '')

def generate_image(prompt, out_path, max_attempts=10):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={API_KEY}'
    payload = json.dumps({
        'contents': [{'parts': [{'text': f"Generate a high quality image: {prompt}"}]}],
        'generationConfig': {'responseModalities': ['IMAGE', 'TEXT']}
    }).encode()
    
    for attempt in range(max_attempts):
        try:
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read())
            
            for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
                if 'inlineData' in part:
                    img_bytes = base64.b64decode(part['inlineData']['data'])
                    with open(out_path, 'wb') as f:
                        f.write(img_bytes)
                    return len(img_bytes)
            
            print(f"    ⚠️ No image in response, attempt {attempt+1}", flush=True)
            time.sleep(10)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = min(30 + attempt * 15, 120)
                print(f"    ⏳ Rate limited, waiting {wait}s (attempt {attempt+1}/{max_attempts})", flush=True)
                time.sleep(wait)
            else:
                print(f"    ❌ HTTP {e.code}: {e.read().decode()[:200]}", flush=True)
                time.sleep(10)
        except Exception as e:
            print(f"    ❌ Error: {e}", flush=True)
            time.sleep(10)
    return None

def process_book(config_path):
    with open(config_path) as f:
        config = json.load(f)
    
    slug = config['slug']
    img_dir = os.path.join(os.path.dirname(__file__), '..', 'books', slug, 'images')
    os.makedirs(img_dir, exist_ok=True)
    
    print(f"\n📖 Processing: {slug}", flush=True)
    
    for i, page in enumerate(config['pages']):
        if 'prompt' not in page:
            continue
        
        out_path = os.path.join(img_dir, f'page-{str(i).zfill(2)}.png')
        if os.path.exists(out_path):
            print(f"  ⏭️ Page {i} exists", flush=True)
            continue
        
        print(f"  🎨 Page {i}: {page['title']}", flush=True)
        size = generate_image(page['prompt'], out_path)
        if size:
            print(f"  ✅ Page {i} saved ({size//1024}KB)", flush=True)
            time.sleep(5)  # pace between successful calls
        else:
            print(f"  ❌ Page {i} FAILED after all attempts", flush=True)
    
    print(f"✅ Done: {slug}", flush=True)

if __name__ == '__main__':
    for path in sys.argv[1:]:
        process_book(path)
