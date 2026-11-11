#!/usr/bin/env node
/*
 * A small local web server so you can try the site on your own computer:
 *
 *   node site/build.js && node site/scripts/dev-server.js
 *
 * then open http://localhost:3000. It serves site/dist and runs the /api
 * functions the same way Vercel does. (On Vercel you do not need this file.)
 */
const http = require('http');
const fs = require('fs');
const path = require('path');

const DIST = path.join(__dirname, '..', 'dist');
const API = path.join(__dirname, '..', '..', 'api');
const PORT = Number(process.env.PORT || 3000);
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.webp': 'image/webp', '.mp3': 'audio/mpeg', '.xml': 'application/xml', '.txt': 'text/plain' };

http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  if (url.pathname.startsWith('/api/')) {
    const name = url.pathname.slice(5).replace(/[^a-z-]/g, '');
    const file = path.join(API, name + '.js');
    if (!fs.existsSync(file)) { res.statusCode = 404; return res.end('No such function'); }
    let raw = '';
    req.on('data', (c) => { raw += c; });
    req.on('end', () => {
      req.query = Object.fromEntries(url.searchParams);
      try { req.body = raw ? JSON.parse(raw) : {}; } catch (e) { req.body = {}; }
      Promise.resolve(require(file)(req, res)).catch((err) => { console.error(err); res.statusCode = 500; res.end('Function crashed'); });
    });
    return;
  }
  let file = path.join(DIST, decodeURIComponent(url.pathname));
  if (!file.startsWith(DIST)) { res.statusCode = 403; return res.end(); }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!fs.existsSync(file)) { res.statusCode = 404; file = path.join(DIST, '404.html'); }
  res.setHeader('Content-Type', TYPES[path.extname(file)] || 'application/octet-stream');
  fs.createReadStream(file).pipe(res);
}).listen(PORT, () => console.log(`Site running at http://localhost:${PORT}`));
