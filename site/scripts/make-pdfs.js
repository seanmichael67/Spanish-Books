#!/usr/bin/env node
/*
 * Saves every printable pack as a PDF in site/marketing/pdfs/ (for Teachers
 * Pay Teachers, Etsy, or emailing a school). Runs the site on this computer,
 * opens each pack the way a buyer would, and prints it to PDF.
 *
 *   node site/build.js
 *   node site/scripts/make-pdfs.js              (all packs)
 *   node site/scripts/make-pdfs.js pack-animales (just one)
 *
 * Needs Playwright (npm i -D playwright). The PDFs are not committed to git.
 */
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const { spawn, execFileSync } = require('child_process');
const { chromium } = require('playwright');

process.env.ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET || crypto.randomBytes(24).toString('hex');
const { makeToken } = require('../../api/_lib/util');
const { packs, books } = require('../../api/_lib/catalog');

const PORT = 3300;
const OUT = path.join(__dirname, '..', 'marketing', 'pdfs');
const only = process.argv.slice(2);

/* Browsers store .webp pictures in a PDF without compression, which made one pack
   about 70 MB. JPEG copies are stored as they are, so we hand the browser those. */
const CACHE = path.join(OUT, '.jpeg-cache');
function makeJpegs() {
  execFileSync('python3', ['-c', `
import os, sys
from PIL import Image
root, cache = sys.argv[1], sys.argv[2]
for folder in os.listdir(os.path.join(root, 'books')):
    src = os.path.join(root, 'books', folder, 'images')
    if not os.path.isdir(src): continue
    for name in os.listdir(src):
        if not name.endswith('.webp'): continue
        out = os.path.join(cache, folder, name[:-5] + '.jpg')
        if os.path.exists(out): continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        img = Image.open(os.path.join(src, name)).convert('RGB')
        img.thumbnail((1400, 1400))
        img.save(out, 'JPEG', quality=80, optimize=True, progressive=True)
`, path.join(__dirname, '..', '..'), CACHE], { stdio: 'inherit' });
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  makeJpegs();
  const folderOf = Object.fromEntries(books.map((b) => [b.slug, b.folder]));
  const server = spawn('node', [path.join(__dirname, 'dev-server.js')], { env: { ...process.env, PORT: String(PORT) }, stdio: 'ignore' });
  await new Promise((r) => setTimeout(r, 800));
  const token = encodeURIComponent(makeToken(['biblioteca'], 'pdf export'));
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.route('**/media/*/*.webp', (route) => {
      const [, slug, name] = new URL(route.request().url()).pathname.match(/\/media\/([^/]+)\/([^/]+)\.webp$/) || [];
      const jpg = slug && path.join(CACHE, folderOf[slug] || '', name + '.jpg');
      if (jpg && fs.existsSync(jpg)) route.fulfill({ contentType: 'image/jpeg', body: fs.readFileSync(jpg) });
      else route.continue();
    });
    for (const pack of packs.filter((p) => !only.length || only.includes(p.id))) {
      await page.goto(`http://localhost:${PORT}/api/pack?product=${pack.id}&t=${token}`, { waitUntil: 'networkidle', timeout: 120000 });
      await page.evaluate(() => document.fonts.ready);
      const file = path.join(OUT, `${pack.id}.pdf`);
      await page.pdf({ path: file, preferCSSPageSize: true, printBackground: true });
      console.log(`saved ${path.relative(process.cwd(), file)} (${(fs.statSync(file).size / 1024 / 1024).toFixed(1)} MB)`);
    }
  } finally {
    await browser.close();
    server.kill();
  }
})().catch((e) => { console.error(e); process.exit(1); });
