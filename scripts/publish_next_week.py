#!/usr/bin/env python3
"""Publish the next weekly book end-to-end ("new book every week").

Finds the lowest-numbered week that has a finished book HTML but is not
yet in the library, then:
  1. generates any missing page images (Gemini, GEMINI_API_KEY env)
  2. generates static audio (edge-tts; needs the edge-tts venv python —
     EDGE_TTS_PYTHON env or scripts/tts-venv/bin/python)
  3. converts images to WebP and applies all client patches
  4. adds the book to server.js BOOKS and rebuilds index.html
  5. commits + pushes (GitHub Pages redeploys the library)
  6. runs the shared fail-closed WordPress sync, which transactionally
     creates the new page and regenerates the complete library hub

Asset-generation failures abort before the list/index/push steps, so an
incomplete reader is never advertised. The shared WordPress sync is idempotent
and exits nonzero on any gate or verification failure; rerunning it reconciles
a reader that was pushed successfully but whose WordPress step was interrupted.
``--dry-run`` reports the candidate only.
"""
import argparse
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from generate_static_assets import parse_book  # noqa: E402

# Planned metadata for the pre-written future weeks (HTML already exists).
PLAN = {
    98:  ("cantar", "🎤", "Cantar", "Singing", "musica"),
    99:  ("bailar", "💃", "Bailar", "Dancing", "musica"),
    100: ("el-piano", "🎹", "El Piano", "The Piano", "musica"),
    101: ("la-flauta", "🪈", "La Flauta", "The Flute", "musica"),
    102: ("la-musica", "🎵", "La Música", "Music", "musica"),
    103: ("los-juegos", "🎲", "Los Juegos", "Games", "musica"),
    104: ("mi-casa", "🏠", "Mi Casa", "My House", "mi-mundo"),
    105: ("mi-escuela", "🏫", "Mi Escuela", "My School", "mi-mundo"),
    106: ("mi-parque", "🛝", "Mi Parque", "My Park", "mi-mundo"),
    107: ("mi-jardin", "🌷", "Mi Jardín", "My Garden", "mi-mundo"),
    108: ("mi-tienda", "🛒", "Mi Tienda", "My Store", "mi-mundo"),
    109: ("mi-biblioteca", "📚", "Mi Biblioteca", "My Library", "mi-mundo"),
    110: ("mi-iglesia", "⛪", "Mi Iglesia", "My Church", "mi-mundo"),
    111: ("mi-ciudad", "🏙️", "Mi Ciudad", "My City", "mi-mundo"),
    120: ("el-carro", "🚗", "El Carro", "The Car", "transporte"),
    121: ("el-autobus", "🚌", "El Autobús", "The Bus", "transporte"),
    122: ("el-avion", "✈️", "El Avión", "The Airplane", "transporte"),
    123: ("el-tren", "🚂", "El Tren", "The Train", "transporte"),
    124: ("la-bicicleta", "🚲", "La Bicicleta", "The Bicycle", "transporte"),
    125: ("el-barco", "⛵", "El Barco", "The Boat", "transporte"),
    126: ("el-cohete", "🚀", "El Cohete", "The Rocket", "transporte"),
    127: ("el-helicoptero", "🚁", "El Helicóptero", "The Helicopter", "transporte"),
    128: ("la-primavera", "🌸", "La Primavera", "Spring", "estaciones"),
    129: ("el-verano", "☀️", "El Verano", "Summer", "estaciones"),
    130: ("el-otono", "🍂", "El Otoño", "Autumn", "estaciones"),
    131: ("el-invierno", "⛄", "El Invierno", "Winter", "estaciones"),
    132: ("el-arcoiris", "🌈", "El Arcoíris", "The Rainbow", "estaciones"),
    133: ("el-trueno", "⛈️", "El Trueno", "Thunder", "estaciones"),
    134: ("el-viento", "🌬️", "El Viento", "The Wind", "estaciones"),
    135: ("el-clima", "🌤️", "El Clima", "The Weather", "estaciones"),
}


def sh(cmd, **kw):
    print("+", " ".join(cmd) if isinstance(cmd, list) else cmd, flush=True)
    return subprocess.run(cmd, cwd=ROOT, check=True, shell=isinstance(cmd, str), **kw)


def listed_slugs():
    return set(re.findall(r"slug: '([^']+)'", open(os.path.join(ROOT, "server.js")).read()))


def next_candidate():
    listed = listed_slugs()
    for week in sorted(PLAN):
        slug_tail, emoji, title, subtitle, theme = PLAN[week]
        slug = f"week-{week}-{slug_tail}"
        idx = os.path.join(ROOT, "books", slug, "index.html")
        if slug in listed or not os.path.exists(idx):
            continue
        if "const Icons" not in open(idx).read():
            continue  # legacy stub
        return week, slug, emoji, title, subtitle, theme
    return None


def image_status(slug):
    pages = parse_book(slug)
    raw = open(os.path.join(ROOT, "books", slug, "index.html")).read()
    n_prompts = len(re.findall(r'["\']?prompt["\']?\s*:\s*"', raw))
    have = {int(m.group(1)) for f in glob.glob(f"{ROOT}/books/{slug}/images/page-*.png")
            if (m := re.search(r"page-(\d+)\.png$", f))}
    need = [i for i in range(n_prompts) if i not in have]
    return n_prompts, need


def audio_complete(slug):
    pages = parse_book(slug)
    adir = os.path.join(ROOT, "books", slug, "audio")
    return all(os.path.exists(os.path.join(adir, f"page-{i:02d}.mp3")) for i in range(len(pages)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-wp", action="store_true")
    args = ap.parse_args()

    cand = next_candidate()
    if not cand:
        print("No publishable candidate found (all planned weeks listed or missing HTML).")
        return
    week, slug, emoji, title, subtitle, theme = cand
    n_prompts, missing_imgs = image_status(slug)
    print(f"Next book: {slug} — {emoji} {title} ({subtitle}) theme={theme}")
    print(f"Images: {n_prompts - len(missing_imgs)}/{n_prompts}; audio complete: {audio_complete(slug)}")
    if args.dry_run:
        return

    # 1. images
    if missing_imgs:
        if not os.environ.get("GEMINI_API_KEY"):
            sys.exit("Missing images and no GEMINI_API_KEY set — aborting before publish.")
        sh([sys.executable, "scripts/generate_static_assets.py", "--images-only", "--book", slug])
        _, still = image_status(slug)
        if still:
            sys.exit(f"Images still missing after generation ({still}) — likely quota; aborting. Re-run later.")

    # 2. audio
    if not audio_complete(slug):
        venv_py = os.environ.get("EDGE_TTS_PYTHON") or os.path.join(ROOT, "scripts", "tts-venv", "bin", "python")
        if not os.path.exists(venv_py):
            sys.exit(f"edge-tts python not found at {venv_py} — set EDGE_TTS_PYTHON. Aborting.")
        # gen_audio_edge reads ready slugs from server.js; use --book to target
        sh([venv_py, "scripts/gen_audio_edge.py", "--book", slug])
        if not audio_complete(slug):
            sys.exit("Audio incomplete after generation — aborting.")

    # 3. webp + client patches
    sh(f'find books/{slug}/images -name "*.png" | while read p; do '
       f'o="${{p%.png}}.webp"; [ -f "$o" ] || ffmpeg -y -loglevel error -i "$p" -c:v libwebp -quality 82 "$o"; done')
    sh([sys.executable, "scripts/patch_books.py"])

    # 4. list + index
    srv_path = os.path.join(ROOT, "server.js")
    srv = open(srv_path).read()
    if slug not in srv:
        entry = (f"  {{ slug: '{slug}', emoji: '{emoji}', week: {week}, title: '{title}', "
                 f"subtitle: '{subtitle}', theme: '{theme}', ready: true }},\n")
        srv = srv.replace("];\n\nconst THEMES", entry + "];\n\nconst THEMES", 1)
        open(srv_path, "w").write(srv)
    sh(["bash", "scripts/rebuild_index.sh"])

    # 5. commit + push
    sh(["git", "add", "-A"])
    sh(["git", "commit", "-m", f"📚 Weekly book: {emoji} {title} — {subtitle} (week {week})"])
    sh(["git", "push", "origin", "main"])

    # 6. Shared transactional WordPress publisher + complete hub rebuild.
    # Explicit --skip-wp is for asset-only recovery; the default fails loudly
    # so scheduled runs cannot report success while WordPress is stale.
    if args.skip_wp:
        print("Skipping shared WordPress sync (--skip-wp).")
        return
    sh([
        sys.executable,
        "scripts/sync_wordpress_books.py",
        "--root", ROOT,
        "--apply",
        "--skip-previews",
    ])


if __name__ == "__main__":
    main()
