# Library refresh — 2026-07-16 (branch `feat/library-refresh`)

## Why

Audit of www.beibeiamigos.com/spanish-books/ found:

1. **Gemini API key public** — `spanish-books.onrender.com/config.js` served the
   real key to every browser.
2. **Audio broken for visitors** — the key is on the Gemini **free tier: 10 TTS
   requests per day** for the entire site. Ten page-reads a day, then silence.
   The image-fallback model (`gemini-2.0-flash-exp-image-generation`) was
   retired upstream, so pages missing a static image spun "Generando…" forever.
3. **Weekly publishing stalled 2026-05-16**; weeks 96–97 (La Guitarra, El
   Tambor) were complete on disk but never listed.
4. **~2 MB PNG per page** (~14 MB per book) and Babel-in-browser compilation.
5. **SEO**: WP book pages contain only an H1 + iframe — Google never sees the
   book text on beibeiamigos.com.

## What changed on this branch

- **Static audio for every page and vocab word** of all 106 listed books,
  generated with edge-tts (free neural voices, no key): Spanish
  (`es-MX-DaliaNeural`) + pause + English (`en-US-JennyNeural`) per page;
  Spanish-only word clips. `scripts/gen_audio_edge.py`, resumable.
- **All 741 page PNGs converted to WebP** (562 MB → 35 MB); PNGs kept as
  fallback.
- **Client patched in all 136 modern books** (`scripts/patch_books.py`,
  idempotent): images try `.webp` → `.png` → API; audio tries static mp3 →
  API; words try static mp3 → API; Web Speech API fallback if no audio source
  exists; missing image shows 📖 instead of an infinite spinner.
- **`server.js` no longer serves the key** — `config.js` returns an empty
  string unless `ALLOW_CLIENT_GEMINI=1`.
- **Library +2**: weeks 96–97 added to `BOOKS`; WP draft pages 3902/3903
  created (invisible until published).
- **`scripts/update_wp_seo.py`**: appends a crawlable read-along section
  (Spanish text + English + vocab) + meta-description excerpt to each WP book
  page. Dry-run by default; applied only to the invisible la-guitarra draft.

## Verified locally (preview on :3012)

- `config.js` → empty key; library renders Semana 96/97.
- Book page: WebP fetched and rendered; `audio/page-00.mp3` plays on
  "Read to Me" with **zero** generativelanguage.googleapis.com calls;
  word files resolve; missing-image page shows 📖, no spinner.

## Still open (Sean gates — cockpit Session I)

- I1 rotate the exposed key (Google console) — it's still public until then.
- I2 merge this branch → Render redeploy.
- I3 publish WP drafts 3902/3903.
- I4 bulk-run `update_wp_seo.py --apply` over the 104 live pages.
- I5 move hosting off Render free tier (cold starts blank the iframe).
- I6 Mandarin book track decision.

## Loose ends

- 6 published books miss one content image (weeks 31, 32, 34, 37, 76, 77) —
  regenerate with `GEMINI_API_KEY=<new key> python3
  scripts/generate_static_assets.py --images-only --book week-NN-…` after the
  free-tier quota resets (script already points at `gemini-2.5-flash-image`),
  then convert to WebP.
- 29 future-week books (99+) have HTML but no images; 36 legacy stub folders
  (old naming) could be deleted.
- Precompiling JSX/Tailwind (drop Babel-standalone + CDN Tailwind) is the next
  perf win; not attempted in this pass.
