#!/usr/bin/env python3
"""Make the whole book page fit inside its frame on desktop.

The reader let the picture take 70% of the window height, on top of the
title, sentence and controls. With square pictures (and in short windows) the
title and sentence were pushed out of view and clipped.

Fix, for screens 768px and wider only (phones are unchanged):
  * the book area gets a definite height (window height minus header, Stop
    button, padding and page dots), and
  * the picture may only use the space left between the title and sentence.

Safe to run again: it skips files that are already fixed.
    python3 scripts/fix_desktop_fit.py
"""
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWAPS = [
    ('h-full flex-1 max-h-[calc(100vh-56px)] md:max-h-[calc(100vh-160px)]',
     'h-full flex-1 max-h-[calc(100vh-56px)] md:flex-none md:max-h-none md:h-[calc(100vh-244px)] md:min-h-[360px]'),
    ('max-h-[65vh] md:max-h-[70vh] max-w-full object-contain',
     'max-h-[65vh] md:max-h-full max-w-full object-contain'),
    # The picture's box needs a real height for "max-h-full" to mean anything.
    ('flex-1 flex items-center justify-center w-full my-0 md:my-4 min-h-0',
     'flex-1 flex items-center justify-center w-full my-0 md:my-2 min-h-0 md:overflow-hidden'),
    # Less padding and tighter spacing on desktop, so the picture gets the room.
    ("'w-full h-full p-1 md:p-10 shadow-none md:shadow-inner", "'w-full h-full p-1 md:p-5 xl:p-8 shadow-none md:shadow-inner"),
    ('w-full text-center space-y-1 md:space-y-4 flex-shrink-0', 'w-full text-center space-y-1 md:space-y-2 flex-shrink-0'),
    ('pt-1 md:pt-4 border-t border-gray-100 flex justify-between', 'pt-1 md:pt-2 border-t border-gray-100 flex justify-between'),
    # Smaller title on mid-size screens leaves more room for the picture.
    ('text-2xl md:text-6xl font-bold text-gray-800 mb-0 md:mb-3 leading-tight',
     'text-2xl md:text-4xl xl:text-6xl font-bold text-gray-800 mb-0 md:mb-3 leading-tight'),
]
fixed = skipped = 0
for path in sorted(glob.glob(os.path.join(ROOT, 'books', '*', 'index.html'))):
    html = open(path, encoding='utf-8').read()
    new = html
    for old, rep in SWAPS:
        new = new.replace(old, rep)
    if new != html:
        open(path, 'w', encoding='utf-8').write(new)
        fixed += 1
    else:
        skipped += 1
print(f'fixed {fixed} books, {skipped} unchanged (already fixed or a different layout)')
