#!/usr/bin/env python3
"""Patch all modern book index.html files to prefer static assets:

1. Image loader: try images/page-NN.webp, then .png, then fall back to API.
2. prefetchAudio: try static audio/page-NN.mp3 before calling the TTS API.
3. speakWord: try static audio/word-<slug>.mp3 before calling the TTS API.

Idempotent: skips files already patched. Reports any file where an
expected snippet was not found.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMG_OLD = re.compile(
    r"\s*".join(
        re.escape(line.strip())
        for line in [
            "const filename = `images/page-${String(i).padStart(2, '0')}.png`;",
            "try {",
            "const res = await fetch(filename, { method: 'HEAD' });",
            "if (res.ok) {",
            "setImages(prev => ({ ...prev, [i]: filename }));",
            "return true;",
            "}",
            "} catch(e) {}",
            "return false;",
        ]
    )
)

IMG_NEW = """for (const ext of ['webp', 'png']) {
                            const filename = `images/page-${String(i).padStart(2, '0')}.${ext}`;
                            try {
                                const res = await fetch(filename, { method: 'HEAD' });
                                if (res.ok) {
                                    setImages(prev => ({ ...prev, [i]: filename }));
                                    return true;
                                }
                            } catch(e) {}
                        }
                        return false;"""

AUDIO_ANCHOR = "fetchPromisesRef.current[index] = (async () => {"
AUDIO_INSERT = """
                    const staticUrl = `audio/page-${String(index).padStart(2, '0')}.mp3`;
                    try {
                        const head = await fetch(staticUrl, { method: 'HEAD' });
                        if (head.ok) {
                            setAudioCache(prev => ({ ...prev, [index]: staticUrl }));
                            delete fetchPromisesRef.current[index];
                            return staticUrl;
                        }
                    } catch (e) {}"""

WORD_ANCHOR = "const speakWord = async (word, retries = 2) => {"
WORD_INSERT = """
                        const wordSlug = word.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/[^a-z0-9]+/g, '-');
                        try {
                            const head = await fetch(`audio/word-${wordSlug}.mp3`, { method: 'HEAD' });
                            if (head.ok) {
                                const audio = new Audio(`audio/word-${wordSlug}.mp3`);
                                return new Promise(resolve => { audio.onended = resolve; audio.play(); });
                            }
                        } catch (e) {}"""


def patch(path):
    raw = open(path).read()
    orig = raw
    notes = []

    if "for (const ext of ['webp', 'png'])" not in raw:
        raw, n = IMG_OLD.subn(IMG_NEW, raw, count=1)
        if n == 0:
            notes.append("IMG-MISS")
    if "const staticUrl = `audio/page-" not in raw:
        if AUDIO_ANCHOR in raw:
            raw = raw.replace(AUDIO_ANCHOR, AUDIO_ANCHOR + AUDIO_INSERT, 1)
        else:
            notes.append("AUDIO-MISS")
    if "audio/word-${wordSlug}.mp3" not in raw:
        if WORD_ANCHOR in raw:
            raw = raw.replace(WORD_ANCHOR, WORD_ANCHOR + WORD_INSERT, 1)
        else:
            notes.append("WORD-MISS")

    if raw != orig:
        open(path, "w").write(raw)
        return "patched", notes
    return "unchanged", notes


def main():
    fails = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "books", "week-*", "index.html"))):
        raw = open(f).read()
        if "const Icons" not in raw:  # legacy stub, skip
            continue
        status, notes = patch(f)
        slug = f.split(os.sep)[-2]
        if notes:
            fails += 1
            print(f"{slug}: {status} WARN {notes}")
        else:
            print(f"{slug}: {status}")
    if fails:
        print(f"\n{fails} files had missing snippets — inspect before shipping")
        sys.exit(1)
    print("\nAll files patched cleanly")


if __name__ == "__main__":
    main()
