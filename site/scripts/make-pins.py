#!/usr/bin/env python3
"""Draw the marketing pictures from the book photos (no AI credits needed).

Makes, in site/marketing/:
  pins/<id>.jpg   1000x1500 Pinterest pins: one per pack, plus the library
                  and the free sample. The site also serves them at /pins/.
  tpt/<id>.jpg    1000x1000 square covers for Teachers Pay Teachers listings.

    pip install pillow
    python3 site/scripts/make-pins.py
"""
import json
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "site", "data")
OUT = os.path.join(ROOT, "site", "marketing")
FONTS = os.path.join(OUT, "fonts")
INK = (31, 42, 68)
CREAM = (255, 246, 227)

books = json.load(open(os.path.join(DATA, "books.json"), encoding="utf-8"))
themes = json.load(open(os.path.join(DATA, "themes.json"), encoding="utf-8"))
config = json.load(open(os.path.join(ROOT, "site", "site.config.json"), encoding="utf-8"))


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def photo(book, size):
    page = book["pages"][0]
    if not page.get("image"):
        page = next((p for p in book["pages"] if p.get("image")), None)
    if not page:
        return Image.new("RGB", size, (230, 230, 230))
    img = Image.open(os.path.join(ROOT, "books", book["folder"], "images", page["image"])).convert("RGB")
    return ImageOps.fit(img, size, Image.LANCZOS, centering=(0.5, 0.45))


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1], radius, fill=255)
    out = Image.new("RGBA", img.size)
    out.paste(img, (0, 0), mask)
    return out


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if draw.textlength(test, font=fnt) <= width or not line:
            line = test
        else:
            lines.append(line)
            line = word
    return lines + ([line] if line else [])


def centred(draw, y, text, fnt, fill, width, canvas_w, gap=8):
    for line in wrap(draw, text, fnt, width):
        w = draw.textlength(line, font=fnt)
        draw.text(((canvas_w - w) / 2, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def grid(chosen, area_w, area_h, gap):
    """2x2 grid of rounded photos with a soft shadow."""
    cell = ((area_w - gap) // 2, (area_h - gap) // 2)
    layer = Image.new("RGBA", (area_w + 40, area_h + 40), (0, 0, 0, 0))
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for i, book in enumerate(chosen[:4]):
        x, y = 20 + (i % 2) * (cell[0] + gap), 20 + (i // 2) * (cell[1] + gap)
        sd.rounded_rectangle([x, y + 8, x + cell[0], y + cell[1] + 8], 26, fill=(0, 0, 0, 70))
    layer = Image.alpha_composite(layer, shadow.filter(ImageFilter.GaussianBlur(10)))
    for i, book in enumerate(chosen[:4]):
        x, y = 20 + (i % 2) * (cell[0] + gap), 20 + (i // 2) * (cell[1] + gap)
        layer.alpha_composite(rounded(photo(book, cell), 26), (x, y))
    return layer


def card(size, color, chosen, kicker, title, subtitle, line, footer):
    w, h = size
    canvas = Image.new("RGBA", size, color + (255,))
    draw = ImageDraw.Draw(canvas)
    # soft cream panel behind the text
    tall = h > w
    grid_h = int(h * (0.50 if tall else 0.50))
    canvas.alpha_composite(grid(chosen, w - 100, grid_h, 22), (30, 30))
    top = grid_h + 70
    draw.rounded_rectangle([40, top, w - 40, h - 40], 40, fill=CREAM)
    y = top + (40 if tall else 26)
    y = centred(draw, y, kicker.upper(), font("Fredoka-SemiBold.ttf", 34 if tall else 28), color, w - 160, w)
    y += 8
    y = centred(draw, y, title, font("Fredoka-Bold.ttf", 96 if tall else 74), INK, w - 140, w, gap=4)
    if subtitle:
        y = centred(draw, y + 4, subtitle, font("Fredoka-SemiBold.ttf", 46 if tall else 38), color, w - 160, w)
    y = centred(draw, y + (22 if tall else 10), line, font("Andika-Regular.ttf", 40 if tall else 32), INK, w - 180, w)
    fnt = font("Fredoka-SemiBold.ttf", 34 if tall else 28)
    tw = draw.textlength(footer, font=fnt)
    pad = 26
    bx, by = (w - tw) / 2 - pad, h - 40 - (110 if tall else 84)
    draw.rounded_rectangle([bx, by, bx + tw + 2 * pad, by + fnt.size + 28], 999, fill=INK)
    draw.text((bx + pad, by + 12), footer, font=fnt, fill=(255, 255, 255))
    return canvas.convert("RGB")


def save(img, folder, name):
    path = os.path.join(OUT, folder, name + ".jpg")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, "JPEG", quality=86, optimize=True, progressive=True)
    return path


by_theme = {}
for b in books:
    by_theme.setdefault(b["theme"], []).append(b)

made = 0
brand = config["name"]
for t in themes:
    group = by_theme.get(t["id"], [])
    if len(group) < 8:
        continue
    color = hex_rgb(t["color"])
    picks = [b for b in group if b["pages"][0].get("image")][:4]
    common = dict(kicker="Spanish books for kids", title=t["en"], subtitle=t["es"],
                  line=f"{len(group)} read-along books · audio · flashcards · tracing pages")
    save(card((1000, 1500), color, picks, footer=f"{brand} · ages 2–6", **common), "pins", "pack-" + t["id"])
    save(card((1000, 1000), color, picks, footer=f"{len(group)} printable books · {brand}", **common), "tpt", "pack-" + t["id"])
    made += 2

# The whole library and the free sample
mix = [by_theme[k][0] for k in ("animales", "oceano", "silabas", "cuentos") if k in by_theme]
save(card((1000, 1500), (31, 42, 68), mix, "Free read-along books", f"{len(books)} Spanish books for kids",
          None, "Real photos, audio on every page, and the words light up as they are read.", f"{brand} · free to read"), "pins", "library")
save(card((1000, 1000), (31, 42, 68), mix, "Every printable pack", "Biblioteca Completa", None,
          f"{len(books)} printable Spanish books with flashcards and tracing pages.", brand), "tpt", "library")
sample = [b for b in books if b["slug"] in (config.get("freeSampleBook"), config.get("freeSyllableSample"))]
for extra in [by_theme["animales"][1], by_theme["cuentos"][0], by_theme["silabas"][2], by_theme["oceano"][0]]:
    if len(sample) < 4 and extra["slug"] not in [b["slug"] for b in sample]:
        sample.append(extra)
save(card((1000, 1500), (255, 107, 74), sample, "Free printable", "Spanish books to print", None,
          "Two free books with picture vocabulary, flashcards and tracing pages.", f"{brand} · print today"), "pins", "free-sample")
print(f"Made {made + 3} pictures in site/marketing/pins and site/marketing/tpt")
