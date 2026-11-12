#!/usr/bin/env python3
"""Record any audio that is missing, using free Microsoft neural voices.

For every page in site/data/books.json that has no recording it makes one clip:
the Spanish sentence, a short pause, then the English sentence. It also makes a
clip for every vocabulary word that has none. Safe to run again and again: it
only makes what is missing.

    pip install edge-tts          (also needs ffmpeg installed)
    python3 site/scripts/make-audio.py
    node site/scripts/import-books.js      <- so the site picks up the new clips
"""
import asyncio
import json
import os
import re
import subprocess
import tempfile
import unicodedata

import certifi

# Behind a company or cloud proxy? Use it, and trust its certificate file if one is set.
PROXY = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
if os.environ.get("SSL_CERT_FILE"):
    certifi.where = lambda: os.environ["SSL_CERT_FILE"]

import edge_tts  # noqa: E402  (must come after the certificate setting above)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ES_VOICE = "es-MX-DaliaNeural"   # same voices as the first 106 books
EN_VOICE = "en-US-JennyNeural"
books = json.load(open(os.path.join(ROOT, "site", "data", "books.json"), encoding="utf-8"))
waiting = os.path.join(ROOT, "site", "data", "books-waiting.json")  # books still missing pictures
if os.path.exists(waiting):
    books += json.load(open(waiting, encoding="utf-8"))
fixes = json.load(open(os.path.join(ROOT, "site", "data", "text-fixes.json"), encoding="utf-8"))
gate = asyncio.Semaphore(4)


def file_slug(word):
    plain = unicodedata.normalize("NFD", word).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", plain).strip("-")


async def speak(text, voice, path):
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, voice, rate="-10%", proxy=PROXY).save(path)
            if os.path.getsize(path) > 500:
                return True
        except Exception:
            await asyncio.sleep(3 * (attempt + 1))
    return False


def join(parts, out, pause=0.35):
    """Join clips with a short silence between them into one clean mp3."""
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for p in parts:
        cmd += ["-i", p]
    graph = [f"[{i}:a]aformat=sample_rates=24000:channel_layouts=mono[a{i}]" for i in range(len(parts))]
    chain = "[a0]"
    for i in range(1, len(parts)):
        graph.append(f"aevalsrc=0:d={pause}:s=24000[s{i}]")
        chain += f"[s{i}][a{i}]"
    graph.append(f"{chain}concat=n={2 * len(parts) - 1}:v=0:a=1[out]")
    cmd += ["-filter_complex", ";".join(graph), "-map", "[out]", "-b:a", "48k", out]
    return subprocess.run(cmd).returncode == 0


async def clip(lines, out):
    """lines = [(text, voice), ...]"""
    async with gate:
        with tempfile.TemporaryDirectory() as tmp:
            parts = []
            for n, (text, voice) in enumerate(lines):
                path = os.path.join(tmp, f"{n}.mp3")
                if not await speak(text, voice, path):
                    return out, False
                parts.append(path)
            return out, join(parts, out)


async def main():
    jobs = []
    for book in books:
        folder = os.path.join(ROOT, "books", book["folder"], "audio")
        os.makedirs(folder, exist_ok=True)
        fixed_pages = fixes.get(book["slug"], {}).get("pages", {})
        for i, page in enumerate(book["pages"]):
            if page.get("audio"):
                continue
            name = f"page-{i:02d}-fix.mp3" if str(i) in fixed_pages else f"page-{i:02d}.mp3"
            out = os.path.join(folder, name)
            if not os.path.exists(out):
                jobs.append(clip([(page.get("say") or page["es"], ES_VOICE), (page["en"], EN_VOICE)], out))
        for word in book["vocab"]:
            out = os.path.join(folder, f"word-{file_slug(word['es'])}.mp3")
            if not word.get("audio") and not os.path.exists(out):
                jobs.append(clip([(word["es"], ES_VOICE)], out))
    print(f"{len(jobs)} clips to record", flush=True)
    failed = 0
    for n, done in enumerate(asyncio.as_completed(jobs), 1):
        out, ok = await done
        failed += 0 if ok else 1
        if not ok:
            print("FAILED", os.path.relpath(out, ROOT), flush=True)
        if n % 50 == 0:
            print(f"{n}/{len(jobs)}", flush=True)
    print(f"Done. {len(jobs) - failed} recorded, {failed} failed.")


asyncio.run(main())
