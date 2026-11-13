# Spanish-Books

Interactive Spanish picture books for preschoolers (ages 2–5), made for Beibei Amigos Language Preschool. Each book is a single web page with photos, read-aloud audio, a vocabulary page and a badge page. A new book is published every week.

## Working with the owner

Sean is a teacher who is learning to code. Explain what you are doing in plain language, define technical terms the first time you use them, and keep changes small enough to review.

## How the project fits together

- `books/week-NN-slug/index.html` is one book. Each book is a self-contained HTML file (its CSS and JavaScript are inside it), with `images/` and `audio/` folders next to it.
- `server.js` holds the `BOOKS` list. This list is the source of truth for which books appear in the library and in what order. A book only shows up when its entry has `ready: true`.
- `index.html` at the repo root is the library page. It is generated from `server.js`, so do not edit it by hand. Rebuild it with `scripts/rebuild_index.sh`.
- `divi-embeds/` holds the snippets pasted into WordPress (Divi) pages on beibeiamigos.com, which show each book inside an iframe.
- `scripts/configs/*.json` are the per-book inputs (pages, vocabulary, badge) used by `scripts/generate-book.py`.
- `daily/` holds older draft books and their image prompts. `templates/TEMPLATE-BOOK.html` and `IMPROVED-BOOK-CODE.html` are earlier templates; new books are generated from `books/week-01-el-oso/index.html`.

The site is published two ways: GitHub Pages serves this repo as static files (pushing to `main` redeploys it), and the WordPress site embeds those pages.

## Commands

```bash
npm install            # one time: installs Express
npm start              # runs the library locally at http://localhost:3002
```

```bash
bash scripts/rebuild_index.sh                      # regenerate index.html from server.js
python3 scripts/publish_next_week.py --dry-run     # show what the weekly publish would do
```

```bash
python3 tests/verify_book_keyword_meta.py
python3 tests/verify_book_keyword_transformer.py
python3 tests/verify_book_sweep_fail_closed.py
```

Each test is a plain Python script that prints `PASS` and exits 0 when it succeeds. Run all three after changing any book's `<head>` metadata.

## Publishing a book

`scripts/publish_next_week.py` does the whole weekly publish: it generates missing images, generates audio, converts images to WebP, adds the book to `server.js`, rebuilds `index.html`, commits and pushes, then creates the WordPress page. It stops before the public steps if anything is incomplete, and it can be re-run safely.

Without `--dry-run` it pushes to GitHub and publishes to the live WordPress site. Always run `--dry-run` first and get Sean's go-ahead before a real run.

It needs these environment variables (names only; values live outside the repo):

- `GEMINI_API_KEY` for image generation
- `EDGE_TTS_PYTHON` pointing at a Python that has `edge-tts` installed (or a virtual environment at `scripts/tts-venv/`)
- `WP_BEIBEI_USER` and `WP_BEIBEI_APP_PASSWORD` for WordPress

## Rules for book content

- Images are realistic photographs, never cartoons or illustrations. This follows the Montessori principle of reality-based learning. See `IMAGE-STYLE-REALISTIC.md`.
- Themes come from `BEGINNER-SERIES-20-WEEKS.md` and `52-WEEK-SPANISH-THEMES-CULTURAL.md`.
- Audio is pre-generated: Spanish in the `es-MX-DaliaNeural` voice, then the English translation in `en-US-JennyNeural` (`scripts/gen_audio_edge.py`). Books do not call an AI service while a child is reading.
- Every book page needs a `<title>`, a meta description and one meta keywords tag. The tests enforce the keywords.

## Things to be careful about

- Never put passwords or API keys in a file. `config.js` is deliberately served with an empty key, and WordPress credentials were removed from the scripts on purpose.
- Scripts whose names start with `update_wp_`, `create_wp_` or `apply_global_style` change the live WordPress site. Ask before running them.
- The repo has about 3,800 files, mostly images and audio. Search by folder or file name instead of reading whole directories.
- Some of the older guides (`MUST-READ-FIRST.md`, `TECHNICAL_SPECS.md`, `BOOKS_AGENT_SOUL.md`) describe the original plan and do not always match the current code. Where they disagree, trust the scripts and the existing books.
