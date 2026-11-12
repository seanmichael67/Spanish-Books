#!/usr/bin/env node
/*
 * One-time importer: reads the finished books in /books (the old React pages)
 * and writes ONE clean data file: site/data/books.json
 *
 * After this runs, site/data/books.json is the "source of truth" for the new
 * website. To fix a typo in a book, edit books.json — not the old HTML.
 *
 * Run:  node site/scripts/import-books.js
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.join(__dirname, '..', '..');
const OUT = path.join(ROOT, 'site', 'data', 'books.json');

const server = fs.readFileSync(path.join(ROOT, 'server.js'), 'utf8');
const LISTED = vm.runInNewContext('(' + server.match(/const BOOKS = (\[[\s\S]*?\n\]);/)[1] + ')');

const fileSlug = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

// Proofreading corrections live in their own file so they are never lost.
const FIXES = JSON.parse(fs.readFileSync(path.join(ROOT, 'site', 'data', 'text-fixes.json'), 'utf8'));

/** Read the width/height of a .webp picture so pages can be laid out without cropping. */
function webpRatio(file) {
  const b = fs.readFileSync(file);
  const kind = b.toString('ascii', 12, 16);
  let w, h;
  if (kind === 'VP8 ') { w = b.readUInt16LE(26) & 0x3fff; h = b.readUInt16LE(28) & 0x3fff; }
  else if (kind === 'VP8L') { const n = b.readUInt32LE(21); w = (n & 0x3fff) + 1; h = ((n >> 14) & 0x3fff) + 1; }
  else { w = b.readUIntLE(24, 3) + 1; h = b.readUIntLE(27, 3) + 1; }
  return Math.round((w / h) * 100) / 100;
}

// Books whose pictures were re-made as photos (their old HTML still describes watercolours).
const PHOTO_BOOKS = Object.keys(JSON.parse(fs.readFileSync(path.join(ROOT, 'site', 'data', 'image-prompts.json'), 'utf8')).books);

const seen = new Set();
const books = LISTED.map((entry) => {
  const html = fs.readFileSync(path.join(ROOT, 'books', entry.slug, 'index.html'), 'utf8');
  const start = html.indexOf('const BOOK_CONFIG = ') + 20;
  const src = html.slice(start, html.indexOf('const Icons', start)).trim().replace(/;\s*$/, '');
  const cfg = vm.runInNewContext('(' + src + ')');

  let slug = entry.slug.replace(/^week-\d+-/, '');
  if (seen.has(slug)) slug = slug + '-' + entry.theme; // e.g. a second "el-arcoiris" in another theme
  seen.add(slug);

  const dir = path.join(ROOT, 'books', entry.slug);
  const pages = [];
  let vocab = [];
  let badge = null;
  cfg.pages.forEach((p, i) => {
    const n = String(i).padStart(2, '0');
    if (p.type === 'vocab') {
      vocab = p.words.map((w) => ({ es: w.es, en: w.en, emoji: w.emoji, audio: fs.existsSync(path.join(dir, 'audio', `word-${fileSlug(w.es)}.mp3`)) ? `word-${fileSlug(w.es)}.mp3` : null }));
    } else if (p.type === 'badge') {
      badge = { emoji: p.badgeEmoji, es: p.badgeName, en: p.badgeNameEn };
    } else {
      pages.push({
        es: p.title,
        en: i === 0 ? entry.subtitle : p.footer,
        image: fs.existsSync(path.join(dir, 'images', `page-${n}.webp`)) ? `page-${n}.webp` : null,
        audio: fs.existsSync(path.join(dir, 'audio', `page-${n}.mp3`)) ? `page-${n}.mp3` : null,
        prompt: p.prompt,
      });
    }
  });

  const prompts = pages.map((p) => p.prompt || '').join(' ').toLowerCase();
  const fix = FIXES[slug] || {};
  Object.entries(fix.pages || {}).forEach(([i, f]) => {
    const page = pages[Number(i)];
    if (page.es !== f.es || page.en !== f.en) {
      // The old recording no longer matches the words. Use the re-recorded
      // clip (page-NN-fix.mp3, made by make-audio.py) if it exists yet.
      const redo = `page-${String(i).padStart(2, '0')}-fix.mp3`;
      page.audio = fs.existsSync(path.join(dir, 'audio', redo)) ? redo : null;
    }
    page.es = f.es;
    page.en = f.en;
  });
  vocab = vocab.map((w) => {
    if (!fix.vocab || !fix.vocab[w.es]) return w;
    const fixed = Object.assign({}, w, fix.vocab[w.es]);
    const clip = `word-${fileSlug(fixed.es)}.mp3`;
    fixed.audio = fs.existsSync(path.join(dir, 'audio', clip)) ? clip : null;
    return fixed;
  });
  pages.forEach((p) => {
    delete p.prompt;
    if (p.image) {
      // A picture that is still being saved (or is damaged) counts as missing.
      try { p.ratio = webpRatio(path.join(dir, 'images', p.image)); } catch (e) { p.image = null; }
    }
  });

  // Reading level: based on how long the sentences are.
  const words = pages.slice(1).map((p) => p.es.replace(/[¡!¿?.,']/g, '').split(/\s+/).filter(Boolean).length);
  const avg = words.reduce((a, b) => a + b, 0) / words.length;
  const level = avg <= 3.4 ? 1 : avg <= 4.3 ? 2 : 3;
  return {
    slug,
    folder: entry.slug,
    order: entry.week,
    theme: entry.theme,
    emoji: entry.emoji,
    title: cfg.title || entry.title,
    titleEn: entry.subtitle,
    art: !PHOTO_BOOKS.includes(entry.slug) && /watercolor|illustration/.test(prompts) ? 'illustration' : 'photo',
    level,
    pages,
    vocab,
    badge,
  };
});

// Books written directly as data (for example the syllable series). They have
// no old HTML page; we only look up which pictures and recordings exist yet.
const extra = JSON.parse(fs.readFileSync(path.join(ROOT, 'site', 'data', 'extra-books.json'), 'utf8')).books;
for (const book of extra) {
  const dir = path.join(ROOT, 'books', book.folder);
  book.pages.forEach((p, i) => {
    const n = String(i).padStart(2, '0');
    p.image = fs.existsSync(path.join(dir, 'images', `page-${n}.webp`)) ? `page-${n}.webp` : null;
    p.audio = fs.existsSync(path.join(dir, 'audio', `page-${n}.mp3`)) ? `page-${n}.mp3` : null;
    if (p.image) { try { p.ratio = webpRatio(path.join(dir, 'images', p.image)); } catch (e) { p.image = null; } }
  });
  book.vocab.forEach((w) => {
    const clip = `word-${fileSlug(w.es)}.mp3`;
    w.audio = fs.existsSync(path.join(dir, 'audio', clip)) ? clip : null;
  });
  books.unshift(book); // syllable books go first: they are where reading starts
}
books.sort((a, b) => (a.theme === 'silabas' ? 0 : 1) - (b.theme === 'silabas' ? 0 : 1) || (a.theme === 'silabas' ? a.order - b.order : 0));

// A book only goes on the site when its pictures are done (one gap is tolerated).
const ready = books.filter((b) => b.pages.filter((p) => !p.image).length <= 1);
const waiting = books.filter((b) => !ready.includes(b));

fs.writeFileSync(OUT, JSON.stringify(ready, null, 1) + '\n');
// make-audio.py also records the waiting books, so they are ready the moment their pictures arrive.
fs.writeFileSync(path.join(ROOT, 'site', 'data', 'books-waiting.json'), JSON.stringify(waiting, null, 1) + '\n');
console.log(`Wrote ${ready.length} books to site/data/books.json`);
if (waiting.length) console.log(`Not on the site yet (pictures missing): ${waiting.map((b) => b.folder).join(', ')}`);
