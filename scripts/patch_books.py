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

SPEECH_ANCHOR = """if (!url) {
                    setIsReading(false);
                    setIsAutoAdvancing(false);
                    return;
                }"""
SPEECH_NEW = """if (!url) {
                    setIsReading(false);
                    setIsAutoAdvancing(false);
                    if ('speechSynthesis' in window) {
                        const utter = new SpeechSynthesisUtterance(`${BOOK_CONFIG.pages[idx].title}. ${BOOK_CONFIG.pages[idx].footer}`);
                        utter.lang = 'es-US';
                        utter.rate = 0.85;
                        speechSynthesis.cancel();
                        speechSynthesis.speak(utter);
                    }
                    return;
                }"""

PLACEHOLDER_OLD = """<div className="flex flex-col items-center gap-2">
                                    <Icons.Loader size={32} className="text-blue-200" />
                                    <span className="text-[8px] uppercase tracking-tighter text-blue-300 animate-pulse">Generando...</span>
                                </div>"""
PLACEHOLDER_NEW = """<div className="flex flex-col items-center gap-2">
                                    <span className="text-8xl" role="img">📖</span>
                                </div>"""

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


BUTTON_OLD = re.compile(
    r"\s*".join(
        re.escape(line.strip())
        for line in [
            '{/* Read to Me button - between header and book */}',
            "{viewMode === 'preview' && (",
            '<div className="flex justify-center py-1 md:py-2">',
            '<button onClick={() => readPage(true)} className={`flex items-center gap-2 md:gap-3 px-6 md:px-10 py-2 md:py-4 rounded-xl md:rounded-2xl text-base md:text-xl font-black transition shadow-2xl ${isAutoAdvancing ? "bg-red-500 text-white hover:bg-red-600 animate-pulse" : "bg-indigo-600 text-white hover:bg-indigo-700 hover:scale-105 active:scale-95"}`}>',
            '{isAutoAdvancing ? <Icons.Stop size={24} /> : <Icons.Play size={24} />}',
            '{isAutoAdvancing ? "Stop" : "📖 Read to Me"}',
            '</button>',
            '</div>',
            ')}',
        ]
    )
)

BUTTON_NEW = """{/* Reading starts automatically; button appears only as Stop while reading */}
                    {viewMode === 'preview' && isAutoAdvancing && (
                        <div className="flex justify-center py-1 md:py-2">
                            <button onClick={() => readPage(true)} className="flex items-center gap-2 md:gap-3 px-6 md:px-10 py-2 md:py-4 rounded-xl md:rounded-2xl text-base md:text-xl font-black transition shadow-2xl bg-red-500 text-white hover:bg-red-600 animate-pulse">
                                <Icons.Stop size={24} />
                                Stop
                            </button>
                        </div>
                    )}"""

PLAY_OLD = "audio.play().catch(() => setIsReading(false));"
PLAY_NEW = ("audio.play().catch(() => { setIsReading(false); setIsAutoAdvancing(false); "
            "if (audioRef.current === audio) audioRef.current = null; });")

AUTOSTART_ANCHOR = "const nav = (idx, dir, fromAuto = false) => {"
AUTOSTART_INSERT = """// Start reading automatically; if the browser blocks autoplay,
            // begin on the child's first tap instead.
            useEffect(() => {
                let kicked = false;
                const kick = () => {
                    if (kicked) return;
                    kicked = true;
                    document.removeEventListener('pointerdown', kick, true);
                    if (!audioRef.current) readPage(true);
                };
                const t = setTimeout(() => readPage(true), 1000);
                document.addEventListener('pointerdown', kick, true);
                return () => { clearTimeout(t); document.removeEventListener('pointerdown', kick, true); };
            }, []);

            """


GA4_ID = "G-WP9V5R7T9N"  # site's GA4 property, extracted from GTM-56PSPXFR
GTAG_ANCHOR = '<script src="../../config.js"></script>'
GTAG_INSERT = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag() {{ dataLayer.push(arguments); }}
      gtag('js', new Date());
      gtag('config', '{GA4_ID}', {{ content_group: 'spanish-books' }});
      window.bookEvent = function (name, params) {{
        try {{ gtag('event', name, Object.assign({{ book: location.pathname.split('/').filter(Boolean).pop() }}, params || {{}})); }} catch (e) {{}}
      }};
    </script>"""

EVT_OPEN_ANCHOR = "let kicked = false;"
EVT_OPEN = "window.bookEvent && bookEvent('book_open');\n                "
EVT_TURN_ANCHOR = "const nav = (idx, dir, fromAuto = false) => {"
EVT_TURN = "\n                window.bookEvent && bookEvent('page_turn', { page_index: idx, auto: fromAuto });"
EVT_READ_ANCHOR = "if (auto) setIsAutoAdvancing(true);"
EVT_READ = "\n                window.bookEvent && bookEvent('read_page', { page_index: idx });"
EVT_WORD_ANCHOR = "const speakWord = async (word, retries = 2) => {"
EVT_WORD = "\n                        window.bookEvent && bookEvent('word_tap', { word: word });"
EVT_DONE_ANCHOR = "if (page && page.type === 'badge') {"
EVT_DONE = "\n                    window.bookEvent && bookEvent('book_complete');"


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
    if "speechSynthesis.speak" not in raw:
        if SPEECH_ANCHOR in raw:
            raw = raw.replace(SPEECH_ANCHOR, SPEECH_NEW, 1)
        else:
            notes.append("SPEECH-MISS")
    if PLACEHOLDER_OLD in raw:
        raw = raw.replace(PLACEHOLDER_OLD, PLACEHOLDER_NEW)
    elif 'role="img">📖' not in raw:
        notes.append("PLACEHOLDER-MISS")
    if "Reading starts automatically" not in raw:
        raw, n = BUTTON_OLD.subn(BUTTON_NEW, raw, count=1)
        if n == 0:
            notes.append("BUTTON-MISS")
    if PLAY_OLD in raw:
        raw = raw.replace(PLAY_OLD, PLAY_NEW, 1)
    elif PLAY_NEW not in raw:
        notes.append("PLAY-MISS")
    if "begin on the child's first tap" not in raw:
        if AUTOSTART_ANCHOR in raw:
            raw = raw.replace(AUTOSTART_ANCHOR, AUTOSTART_INSERT + AUTOSTART_ANCHOR, 1)
        else:
            notes.append("AUTOSTART-MISS")
    if GA4_ID not in raw:
        if GTAG_ANCHOR in raw:
            raw = raw.replace(GTAG_ANCHOR, GTAG_ANCHOR + GTAG_INSERT, 1)
        else:
            notes.append("GTAG-MISS")
        for anchor, ins, marker in [
            (EVT_OPEN_ANCHOR, EVT_OPEN, "bookEvent('book_open')"),
            (EVT_TURN_ANCHOR, EVT_TURN, "bookEvent('page_turn'"),
            (EVT_READ_ANCHOR, EVT_READ, "bookEvent('read_page'"),
            (EVT_WORD_ANCHOR, EVT_WORD, "bookEvent('word_tap'"),
            (EVT_DONE_ANCHOR, EVT_DONE, "bookEvent('book_complete')"),
        ]:
            if marker in raw:
                continue
            if anchor not in raw:
                notes.append(f"EVT-MISS:{marker[:24]}")
                continue
            if marker == "bookEvent('book_open')":
                raw = raw.replace(anchor, ins + anchor, 1)
            else:
                raw = raw.replace(anchor, anchor + ins, 1)

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
