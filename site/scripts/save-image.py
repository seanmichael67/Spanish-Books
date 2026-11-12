#!/usr/bin/env python3
"""Download one generated picture and save it as a book page.

    python3 site/scripts/save-image.py <book-folder> <page-number> <picture-url>

Example:
    python3 site/scripts/save-image.py week-104-mi-casa 2 https://.../picture.png

The picture is saved as books/<book-folder>/images/page-NN.webp, 1600 pixels
wide (sharp enough to print, small enough to load fast).
"""
import io
import os
import sys
import urllib.request

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
folder, page, url = sys.argv[1], int(sys.argv[2]), sys.argv[3]
out_dir = os.path.join(ROOT, "books", folder, "images")
if not os.path.isdir(os.path.join(ROOT, "books", folder)):
    sys.exit(f"No such book folder: {folder}")
os.makedirs(out_dir, exist_ok=True)

data = urllib.request.urlopen(url, timeout=120).read()
img = Image.open(io.BytesIO(data)).convert("RGB")
if img.width > 1600:
    img = img.resize((1600, round(img.height * 1600 / img.width)), Image.LANCZOS)
out = os.path.join(out_dir, f"page-{page:02d}.webp")
img.save(out, "WEBP", quality=82, method=6)
print(f"saved {os.path.relpath(out, ROOT)} {img.size[0]}x{img.size[1]} {os.path.getsize(out) // 1024} KB")
