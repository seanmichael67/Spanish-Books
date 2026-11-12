#!/usr/bin/env python3
"""Add a "Pantalla completa" (full screen) button to the book reader.

On beibeiamigos.com each book sits in a frame with a fixed height, so the
picture can be small. The button appears only when the book is inside a frame
and opens the same book in its own tab, where it fills the whole window. The
text on the WordPress page is not touched.

Safe to run again: books that already have the button are skipped.
    python3 scripts/add_fullscreen_link.py
"""
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANCHOR = '<button onClick={handleDownloadPdf} disabled={generatingPdf}'
LINK = ('{window.self !== window.top && (<a href={window.location.href} target="_blank" rel="noopener" '
        'onClick={() => window.bookEvent && bookEvent(\'full_screen\')} '
        'className="hidden md:flex items-center gap-2 px-5 md:px-7 py-2.5 md:py-3 bg-indigo-600 text-white rounded-xl '
        'text-sm md:text-base font-bold hover:bg-indigo-700 transition shadow-md no-underline">⛶ Pantalla completa</a>)}\n'
        '                            ')
added = 0
for path in sorted(glob.glob(os.path.join(ROOT, 'books', '*', 'index.html'))):
    html = open(path, encoding='utf-8').read()
    if ANCHOR in html and 'Pantalla completa' not in html:
        open(path, 'w', encoding='utf-8').write(html.replace(ANCHOR, LINK + ANCHOR, 1))
        added += 1
print(f'added the full-screen button to {added} books')
