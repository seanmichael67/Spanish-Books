#!/usr/bin/env node
/*
 * Writes site/old-site-redirects.csv: one line per old book page on
 * beibeiamigos.com and the new page it should forward to (a "301 redirect").
 * Give this file to whoever manages the WordPress site, or paste it into a
 * redirect plugin, once the new site has its address.
 *
 *   node site/scripts/make-redirects.js https://libros.beibeiamigos.com
 */
const fs = require('fs');
const path = require('path');
const books = require('../data/books.json');
const old = require('../../wp_pages_results.json');

const site = (process.argv[2] || 'https://YOUR-NEW-SITE').replace(/\/+$/, '');
const rows = [['old_url', 'new_url'], ['https://www.beibeiamigos.com/spanish-books/', `${site}/libros/`]];
let unmatched = 0;
const seen = new Set();
for (const page of old) {
  if (!/\/spanish-books\/[^/]+\/$/.test(page.url || '') || seen.has(page.url)) continue; // skip failed or repeated entries
  seen.add(page.url);
  const folder = page.file.replace(/\.html$/, '');
  const book = books.find((b) => b.folder === folder) || books.find((b) => b.slug === page.slug);
  if (book) rows.push([page.url, `${site}/libros/${book.slug}/`]);
  else { rows.push([page.url, `${site}/libros/`]); unmatched++; }
}
const out = path.join(__dirname, '..', 'old-site-redirects.csv');
fs.writeFileSync(out, rows.map((r) => r.join(',')).join('\n') + '\n');
console.log(`Wrote ${rows.length - 1} redirects to site/old-site-redirects.csv (${unmatched} old pages have no matching book and go to the library)`);
