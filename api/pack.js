/*
 * GET /api/pack?product=pack-animales&t=<access token>[&book=el-oso]
 * Returns the printable pack as a page the parent can print or save as PDF.
 * Only works with a valid access token for that product.
 */
const { getProduct, getBook, owns, SCHOOL_ID } = require('./_lib/catalog');
const { renderPrintable } = require('./_lib/print');
const { readToken } = require('./_lib/util');

function deny(res, status, message) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(`<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Printable pack</title>
<body style="font-family:system-ui,sans-serif;max-width:34rem;margin:15vh auto;padding:0 1.25rem;line-height:1.6">
<h1>${message}</h1><p><a href="/mis-compras/">Find my purchases</a> · <a href="/packs/">See the printable packs</a></p></body>`);
}

module.exports = async (req, res) => {
  const q = req.query || {};
  const product = getProduct(String(q.product || ''));
  if (!product || product.kind !== 'pack') return deny(res, 404, 'We could not find that pack.');

  const access = readToken(String(q.t || ''));
  if (!access || !owns(access.products, product.id)) return deny(res, 403, 'This pack needs a purchase to open.');

  let books = product.books.map(getBook);
  if (q.book) {
    books = books.filter((b) => b.slug === q.book);
    if (!books.length) return deny(res, 404, 'That book is not part of this pack.');
  }

  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.setHeader('Cache-Control', 'private, no-store');
  res.setHeader('X-Robots-Tag', 'noindex');
  res.end(renderPrintable({
    title: books.length === 1 ? `${books[0].title} · printable book` : product.name,
    books,
    note: access.products.includes(SCHOOL_ID)
      ? `School licence for ${access.email || 'one school'}: all classrooms at one school. Paper: US Letter, landscape.`
      : access.email ? `For personal and classroom use by ${access.email}. Paper: US Letter, landscape.` : '',
    backUrl: '/mis-compras/',
  }));
};
