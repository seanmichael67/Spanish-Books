#!/usr/bin/env python3
"""Replace dead <img> tags in legacy books with an intentional placeholder.

Eight legacy books render broken-image icons. Two causes:

  * `via.placeholder.com` — the service is gone, so every one of those srcs
    now fails.
  * local files that were never generated (`page1.jpg`, `placeholder-2.jpg`).

Neither can be fixed without generating illustrations, which is a spend
decision. Until then a broken-image icon is the worst possible rendering: it
reads as a bug. This swaps each dead img for a captioned placeholder card
carrying the image's own alt text, so the page reads as a book that is still
being illustrated.

Any `data-prompt` on the original img is preserved on the placeholder — those
are the generation prompts, and they are the only copy.

Idempotent; safe to re-run. Dry-run by default. Local-only, no network writes.
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = os.path.join(ROOT, "books")
MARKER = "ba-pending-illustration"

DEAD_HOSTS = ("via.placeholder.com", "placeholder.com")

TARGETS = [
    "week-73-el-clima",
    "week-70-el-reino-submarino",
    "week-64-el-parque-de-juegos",
    "week-54-los-amigos-de-la-comunidad",
    "week-51-las-maravillas-del-mar",
    "week-39-las-frutas",
    "week-31-la-ropa",
    "week-30-los-colores",
]

CARD = (
    '<div class="{marker}" role="img" aria-label="{alt}"{prompt}'
    ' style="display:flex;flex-direction:column;align-items:center;justify-content:center;'
    'gap:8px;min-height:200px;margin:0 auto 20px;padding:24px;max-width:600px;'
    'background:linear-gradient(135deg,#eef2ff,#f5f3ff);border:2px dashed #c7d2fe;'
    'border-radius:14px;color:#4338ca;font-size:15px;text-align:center;">'
    '<span style="font-size:44px;line-height:1;">\U0001F4D6</span>'
    '<span>{alt}</span></div>'
)


def is_dead(src, folder):
    if not src:
        return True
    if any(h in src for h in DEAD_HOSTS):
        return True
    if src.startswith(("http://", "https://", "//", "data:")):
        return False
    return not os.path.exists(os.path.join(folder, src.lstrip("./")))


def attr(tag, name):
    m = re.search(r'%s="([^"]*)"' % name, tag)
    return m.group(1) if m else ""


def process(slug, apply_):
    folder = os.path.join(BOOKS, slug)
    path = os.path.join(folder, "index.html")
    if not os.path.exists(path):
        return None
    html = open(path, encoding="utf-8").read()
    if MARKER in html:
        return (slug, 0, "already done")

    dead = []

    def sub(m):
        tag = m.group(0)
        src = attr(tag, "src")
        if not is_dead(src, folder):
            return tag
        alt = attr(tag, "alt") or "Ilustración en camino"
        prompt = attr(tag, "data-prompt")
        dead.append(src)
        return CARD.format(
            marker=MARKER,
            alt=alt.replace('"', "&quot;"),
            prompt=(' data-prompt="%s"' % prompt.replace('"', "&quot;")) if prompt else "",
        )

    out = re.sub(r"<img\b[^>]*>", sub, html)
    if not dead:
        return (slug, 0, "no dead images")
    if apply_:
        open(path, "w", encoding="utf-8").write(out)
    return (slug, len(dead), "replaced" if apply_ else "would replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    total = 0
    for slug in TARGETS:
        res = process(slug, args.apply)
        if res is None:
            sys.exit("missing book folder: %s" % slug)
        s, n, note = res
        total += n
        print("  %-36s %2d  %s" % (s, n, note))
    print("\n%d dead images %s across %d books."
          % (total, "replaced" if args.apply else "would be replaced", len(TARGETS)))
    if not args.apply:
        print("DRY RUN — no files written.")


if __name__ == "__main__":
    main()
