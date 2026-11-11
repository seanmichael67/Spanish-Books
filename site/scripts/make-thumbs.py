#!/usr/bin/env python3
"""Make a small cover picture (thumb.webp) for every book in site/data/books.json.

The library page shows 100+ covers at once. Small covers make it load fast on
phones. Run this once after adding a new book:

    pip install pillow
    python3 site/scripts/make-thumbs.py
"""
import json
import os
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
books = json.load(open(os.path.join(ROOT, "site", "data", "books.json"), encoding="utf-8"))
made = 0
for book in books:
    cover = book["pages"][0].get("image")
    if not cover:
        continue
    folder = os.path.join(ROOT, "books", book["folder"], "images")
    out = os.path.join(folder, "thumb.webp")
    if os.path.exists(out):
        continue
    img = ImageOps.fit(Image.open(os.path.join(folder, cover)).convert("RGB"), (480, 360), Image.LANCZOS)
    img.save(out, "WEBP", quality=78, method=6)
    made += 1
print(f"Made {made} new cover thumbnails")
