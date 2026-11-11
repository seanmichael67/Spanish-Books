/* Helpers shared by the /api functions. */
const crypto = require('crypto');

/** The public address of the site, e.g. https://libros.example.com (no trailing slash). */
function siteUrl(req) {
  if (process.env.SITE_URL) return process.env.SITE_URL.replace(/\/+$/, '');
  const host = req.headers['x-forwarded-host'] || req.headers.host;
  const proto = req.headers['x-forwarded-proto'] || (String(host).startsWith('localhost') ? 'http' : 'https');
  return `${proto}://${host}`;
}

const isEmail = (s) => typeof s === 'string' && s.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(s);

function send(res, status, data) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(data));
}

/** Vercel parses JSON bodies for us; this also copes with a raw string. */
function body(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  try { return JSON.parse(req.body || '{}'); } catch (e) { return {}; }
}

/* ---- Access tokens -------------------------------------------------------
 * After a purchase we give the browser a signed "access token": a small note
 * that says which packs were bought. It is signed with ACCESS_TOKEN_SECRET so
 * nobody can invent one. No database needed.
 */
const b64 = (s) => Buffer.from(s).toString('base64url');
const secret = () => process.env.ACCESS_TOKEN_SECRET || '';
const sign = (payload) => crypto.createHmac('sha256', secret()).update(payload).digest('base64url');

function makeToken(products, email) {
  if (!secret()) throw new Error('ACCESS_TOKEN_SECRET is not set');
  const payload = b64(JSON.stringify({ p: [...new Set(products)].sort(), e: email || '', t: Math.floor(Date.now() / 1000) }));
  return `${payload}.${sign(payload)}`;
}

function readToken(token) {
  if (!secret() || typeof token !== 'string' || !token.includes('.')) return null;
  const [payload, sig] = token.split('.');
  const good = sign(payload);
  if (sig.length !== good.length || !crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(good))) return null;
  try {
    const data = JSON.parse(Buffer.from(payload, 'base64url').toString());
    return { products: Array.isArray(data.p) ? data.p : [], email: data.e || '' };
  } catch (e) { return null; }
}

module.exports = { siteUrl, isEmail, send, body, makeToken, readToken };
