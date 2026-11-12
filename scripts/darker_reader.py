#!/usr/bin/env python3
"""Give the book reader a darker background with a warm paper-coloured page.

The reader was almost all white (white page on a pale grey background). A dark
surround keeps a child's eyes on the book, and a cream page is gentler than
pure white. The words stay dark on light so they remain easy to read.

Safe to run again.   python3 scripts/darker_reader.py
"""
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWAPS = [
    ('<body class="bg-slate-100 antialiased overflow-x-hidden">', '<body class="bg-indigo-950 antialiased overflow-x-hidden">'),
    # the book card and the page inside it
    ('bg-white shadow-none md:shadow-2xl rounded-none md:rounded-2xl', 'bg-amber-50 shadow-none md:shadow-2xl rounded-none md:rounded-2xl'),
    ("relative flex flex-col items-center justify-between bg-white ${isPrint ?", "relative flex flex-col items-center justify-between ${isPrint ? 'bg-white' : 'bg-amber-50'} ${isPrint ?"),
    # page dots that were pale grey on pale grey
    ('"bg-indigo-500 w-6 md:w-8" : "bg-slate-200 w-1.5 md:w-2.5"', '"bg-amber-300 w-6 md:w-8" : "bg-white/30 w-1.5 md:w-2.5"'),
]
changed = 0
for path in sorted(glob.glob(os.path.join(ROOT, 'books', '*', 'index.html'))):
    html = open(path, encoding='utf-8').read()
    new = html
    for old, rep in SWAPS:
        new = new.replace(old, rep)
    if new != html:
        open(path, 'w', encoding='utf-8').write(new)
        changed += 1
print(f'darkened {changed} books')
