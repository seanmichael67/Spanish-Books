#!/usr/bin/env python3
"""Find out WHEN each Spanish word is spoken, so the reader can light words up.

The voice service reports the start and length of every word it speaks. We ask
it to speak each page's Spanish text again (same voice and speed as the saved
recordings) and keep only those times in site/data/timings.json. No audio is
changed. Safe to re-run: pages whose text has not changed are skipped.

    pip install edge-tts
    python3 site/scripts/make-timings.py
    node site/scripts/import-books.js
"""
import asyncio
import json
import os

import certifi

PROXY = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
if os.environ.get("SSL_CERT_FILE"):
    certifi.where = lambda: os.environ["SSL_CERT_FILE"]

import edge_tts  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "site", "data", "timings.json")
ES_VOICE = "es-MX-DaliaNeural"
books = json.load(open(os.path.join(ROOT, "site", "data", "books.json"), encoding="utf-8"))
waiting = os.path.join(ROOT, "site", "data", "books-waiting.json")  # books still missing pictures
if os.path.exists(waiting):
    books += json.load(open(waiting, encoding="utf-8"))
timings = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
gate = asyncio.Semaphore(4)


async def measure(key, text):
    async with gate:
        for attempt in range(4):
            try:
                words = []
                talk = edge_tts.Communicate(text, ES_VOICE, rate="-10%", proxy=PROXY, boundary="WordBoundary")
                async for part in talk.stream():
                    if part["type"] == "WordBoundary":
                        start = round(part["offset"] / 10000)          # service counts in 100-nanosecond units
                        words.append([start, start + round(part["duration"] / 10000)])
                if words:
                    return key, {"text": text, "w": words}
            except Exception:
                await asyncio.sleep(3 * (attempt + 1))
        return key, None


async def main():
    jobs = []
    for book in books:
        for i, page in enumerate(book["pages"]):
            text = page.get("say") or page["es"]
            key = f"{book['folder']}/{i}"
            if timings.get(key, {}).get("text") != text:
                jobs.append(measure(key, text))
    print(f"{len(jobs)} pages to measure", flush=True)
    failed = 0
    for n, done in enumerate(asyncio.as_completed(jobs), 1):
        key, result = await done
        if result:
            timings[key] = result
        else:
            failed += 1
            print("FAILED", key, flush=True)
        if n % 100 == 0:
            print(f"{n}/{len(jobs)}", flush=True)
            json.dump(timings, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(dict(sorted(timings.items())), open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"Done. {len(jobs) - failed} measured, {failed} failed.")


asyncio.run(main())
