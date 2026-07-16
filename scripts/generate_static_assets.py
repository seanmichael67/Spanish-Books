#!/usr/bin/env python3
"""Pre-generate static audio (and missing images) for published books.

Audio: one MP3 per page (matching client readPage text) plus one MP3 per
vocab word (matching client speakWord), saved under books/<slug>/audio/.
Images: fills any missing books/<slug>/images/page-NN.png via Gemini.

Resumable: existing files are skipped. Throttles + backs off on 429.

Usage:
  GEMINI_API_KEY=... python3 scripts/generate_static_assets.py [--book SLUG] [--audio-only|--images-only]
"""
import base64
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_KEY = os.environ.get("GEMINI_API_KEY", "")
TTS_MODEL = "gemini-2.5-flash-preview-tts"
IMG_MODEL = "gemini-2.0-flash-exp-image-generation"
MIN_INTERVAL = float(os.environ.get("TTS_INTERVAL", "6"))  # seconds between API calls

_last_call = [0.0]


def throttle():
    wait = _last_call[0] + MIN_INTERVAL - time.time()
    if wait > 0:
        time.sleep(wait)
    _last_call[0] = time.time()


def api_call(model, payload, max_retries=5):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    body = json.dumps(payload).encode()
    for attempt in range(max_retries):
        throttle()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503):
                delay = min(120, 15 * (attempt + 1))
                print(f"    HTTP {e.code}, retry in {delay}s", flush=True)
                time.sleep(delay)
                continue
            print(f"    HTTP {e.code}: {e.read()[:300]}", flush=True)
            return None
        except Exception as e:
            print(f"    error: {e}", flush=True)
            time.sleep(10)
    return None


def ready_slugs():
    raw = open(os.path.join(ROOT, "server.js")).read()
    return re.findall(r"slug:\s*'([^']+)'[^\n]*ready:\s*true", raw)


def parse_book(slug):
    """Return list of page dicts {title, footer, words:[es,...]} from index.html."""
    raw = open(os.path.join(ROOT, "books", slug, "index.html")).read()
    m = re.search(r'["\']?pages["\']?\s*:\s*\[', raw)
    if not m:
        return []
    # brace-match the pages array
    i = raw.index("[", m.start())
    depth, j = 0, i
    while j < len(raw):
        if raw[j] == "[":
            depth += 1
        elif raw[j] == "]":
            depth -= 1
            if depth == 0:
                break
        j += 1
    seg = raw[i : j + 1]
    pages = []
    # brace-match each top-level object in the array
    k = 0
    while k < len(seg):
        if seg[k] == "{":
            depth, s = 0, k
            while k < len(seg):
                if seg[k] == "{":
                    depth += 1
                elif seg[k] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                k += 1
            obj = seg[s : k + 1]
            title = re.search(r'["\']?title["\']?\s*:\s*"([^"]*)"', obj)
            footer = re.search(r'["\']?footer["\']?\s*:\s*"([^"]*)"', obj)
            words = re.findall(r'["\']?es["\']?\s*:\s*"([^"]*)"', obj)
            pages.append({
                "title": title.group(1) if title else "",
                "footer": footer.group(1) if footer else "",
                "words": words,
            })
        k += 1
    return pages


def word_slug(word):
    s = unicodedata.normalize("NFD", word).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s)


def tts_to_mp3(prompt_text, out_path):
    data = api_call(TTS_MODEL, {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Leda"}}},
        },
        "model": TTS_MODEL,
    })
    if not data:
        return False
    try:
        part = data["candidates"][0]["content"]["parts"][0]["inlineData"]
        pcm = base64.b64decode(part["data"])
        rate = 24000
        m = re.search(r"rate=(\d+)", part.get("mimeType", ""))
        if m:
            rate = int(m.group(1))
    except (KeyError, IndexError):
        print(f"    unexpected TTS response: {str(data)[:200]}", flush=True)
        return False
    p = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(rate), "-ac", "1",
         "-i", "pipe:0", "-b:a", "48k", out_path],
        input=pcm, capture_output=True)
    if p.returncode != 0:
        print(f"    ffmpeg failed: {p.stderr[:200]}", flush=True)
        return False
    return True


def gen_audio(slug):
    pages = parse_book(slug)
    if not pages:
        print(f"  {slug}: could not parse pages, skipping", flush=True)
        return 0
    adir = os.path.join(ROOT, "books", slug, "audio")
    os.makedirs(adir, exist_ok=True)
    made = 0
    for idx, pg in enumerate(pages):
        out = os.path.join(adir, f"page-{idx:02d}.mp3")
        if os.path.exists(out):
            continue
        text = f"{pg['title']}. {pg['footer']}"
        ok = tts_to_mp3(f"Read standard neutral Spanish clearly: {text}", out)
        print(f"  {slug} page-{idx:02d} {'ok' if ok else 'FAIL'}", flush=True)
        made += ok
    for pg in pages:
        for w in pg["words"]:
            out = os.path.join(adir, f"word-{word_slug(w)}.mp3")
            if os.path.exists(out):
                continue
            ok = tts_to_mp3(f"Read this single Spanish word slowly and clearly: {w}", out)
            print(f"  {slug} word-{word_slug(w)} {'ok' if ok else 'FAIL'}", flush=True)
            made += ok
    return made


def gen_missing_images(slug):
    raw = open(os.path.join(ROOT, "books", slug, "index.html")).read()
    pages = parse_book(slug)
    idir = os.path.join(ROOT, "books", slug, "images")
    os.makedirs(idir, exist_ok=True)
    made = 0
    for idx, pg in enumerate(pages):
        obj_prompt = None
        # only pages with an image prompt need images
        m = re.findall(r'["\']?prompt["\']?\s*:\s*"([^"]*)"', raw)
        if idx < len(m):
            obj_prompt = m[idx]
        out = os.path.join(idir, f"page-{idx:02d}.png")
        if not obj_prompt or os.path.exists(out):
            continue
        data = api_call(IMG_MODEL, {
            "contents": [{"parts": [{"text": obj_prompt}]}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
        })
        if not data:
            print(f"  {slug} image page-{idx:02d} FAIL", flush=True)
            continue
        try:
            parts = data["candidates"][0]["content"]["parts"]
            img = next(p["inlineData"]["data"] for p in parts if "inlineData" in p)
        except (KeyError, IndexError, StopIteration):
            print(f"  {slug} image page-{idx:02d}: no image in response", flush=True)
            continue
        open(out, "wb").write(base64.b64decode(img))
        print(f"  {slug} image page-{idx:02d} ok", flush=True)
        made += 1
    return made


def main():
    if not API_KEY:
        sys.exit("GEMINI_API_KEY not set")
    args = sys.argv[1:]
    only = None
    if "--book" in args:
        only = args[args.index("--book") + 1]
    slugs = [only] if only else ready_slugs()
    audio = "--images-only" not in args
    images = "--audio-only" not in args
    total = 0
    for n, slug in enumerate(slugs, 1):
        print(f"[{n}/{len(slugs)}] {slug}", flush=True)
        if images:
            total += gen_missing_images(slug)
        if audio:
            total += gen_audio(slug)
    print(f"DONE: {total} assets generated", flush=True)


if __name__ == "__main__":
    main()
