#!/usr/bin/env python3
"""Pre-generate static book audio with edge-tts (free neural voices, no key).

Replaces the Gemini TTS batch: the site's Gemini key is free-tier (10
requests/DAY), which is also why live audio has been broken for visitors.

Per page: Spanish sentence (es-MX-DaliaNeural) + 350ms pause + English
translation (en-US-JennyNeural), concatenated into audio/page-NN.mp3.
Footers that are actually Spanish (e.g. title page "Aprendiendo juntos")
are spoken with the Spanish voice. Per vocab word: Spanish voice only,
audio/word-<slug>.mp3.

Resumable (skips existing files). Run inside the edge-tts venv:
  <venv>/bin/python scripts/gen_audio_edge.py [--book SLUG]
"""
import asyncio
import os
import re
import subprocess
import sys
import tempfile

import edge_tts

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_static_assets import parse_book, ready_slugs, word_slug

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ES_VOICE = "es-MX-DaliaNeural"
EN_VOICE = "en-US-JennyNeural"
CONCURRENCY = 4
SPANISH_FOOTERS = {"Aprendiendo juntos", "Mis Palabras"}

sem = asyncio.Semaphore(CONCURRENCY)


async def synth(text, voice, path, retries=4):
    for attempt in range(retries):
        try:
            await edge_tts.Communicate(text, voice, rate="-10%").save(path)
            if os.path.getsize(path) > 500:
                return True
        except Exception as e:
            await asyncio.sleep(3 * (attempt + 1))
    return False


def concat_mp3(parts, out_path, pause_ms=350):
    """Decode parts, join with silence, re-encode one clean mp3."""
    inputs = []
    for p in parts:
        inputs += ["-i", p]
    n = len(parts)
    silence = f"aevalsrc=0:d={pause_ms/1000}:s=24000"
    graph = []
    for i in range(n):
        graph.append(f"[{i}:a]aformat=sample_rates=24000:channel_layouts=mono[a{i}]")
    join_in = ""
    extra = 0
    for i in range(n):
        join_in += f"[a{i}]"
        if i < n - 1:
            graph.append(f"{silence}[s{extra}]")
            join_in += f"[s{extra}]"
            extra += 1
    graph.append(f"{join_in}concat=n={n + extra}:v=0:a=1[out]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error"] + inputs + [
        "-filter_complex", ";".join(graph), "-map", "[out]", "-b:a", "48k", out_path]
    return subprocess.run(cmd, capture_output=True).returncode == 0


async def page_clip(slug, idx, title, footer, out):
    async with sem:
        with tempfile.TemporaryDirectory() as td:
            parts = []
            es_path = os.path.join(td, "es.mp3")
            if not await synth(title, ES_VOICE, es_path):
                return False
            parts.append(es_path)
            if footer:
                en_path = os.path.join(td, "en.mp3")
                voice = ES_VOICE if footer in SPANISH_FOOTERS else EN_VOICE
                if not await synth(footer, voice, en_path):
                    return False
                parts.append(en_path)
            return concat_mp3(parts, out)


async def word_clip(word, out):
    async with sem:
        with tempfile.TemporaryDirectory() as td:
            tmp = os.path.join(td, "w.mp3")
            if not await synth(word, ES_VOICE, tmp):
                return False
            return concat_mp3([tmp], out, pause_ms=0)


async def run(slugs):
    total_ok = total_fail = 0
    for n, slug in enumerate(slugs, 1):
        pages = parse_book(slug)
        if not pages:
            print(f"[{n}/{len(slugs)}] {slug}: no parseable pages, skipping", flush=True)
            continue
        adir = os.path.join(ROOT, "books", slug, "audio")
        os.makedirs(adir, exist_ok=True)
        jobs = []
        for idx, pg in enumerate(pages):
            out = os.path.join(adir, f"page-{idx:02d}.mp3")
            if not os.path.exists(out):
                jobs.append(page_clip(slug, idx, pg["title"], pg["footer"], out))
        seen_words = set()
        for pg in pages:
            for w in pg["words"]:
                ws = word_slug(w)
                if ws in seen_words:
                    continue
                seen_words.add(ws)
                out = os.path.join(adir, f"word-{ws}.mp3")
                if not os.path.exists(out):
                    jobs.append(word_clip(w, out))
        if not jobs:
            print(f"[{n}/{len(slugs)}] {slug}: complete", flush=True)
            continue
        results = await asyncio.gather(*jobs)
        ok = sum(bool(r) for r in results)
        total_ok += ok
        total_fail += len(results) - ok
        print(f"[{n}/{len(slugs)}] {slug}: {ok}/{len(results)} clips", flush=True)
    print(f"DONE: {total_ok} generated, {total_fail} failed", flush=True)
    return total_fail


def main():
    slugs = ready_slugs()
    if "--book" in sys.argv:
        slugs = [sys.argv[sys.argv.index("--book") + 1]]
    sys.exit(1 if asyncio.run(run(slugs)) else 0)


if __name__ == "__main__":
    main()
