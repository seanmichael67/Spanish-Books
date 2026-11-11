/*
 * POST /api/subscribe   { "email": "...", "name": "..." }
 * Adds a parent to the mailing list (Resend audience).
 */
const { addContact, canSubscribe } = require('./_lib/email');
const { send, body, isEmail } = require('./_lib/util');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return send(res, 405, { error: 'Use POST' });
  const data = body(req);
  // "website" is a hidden field real people never fill in. Robots do.
  if (data.website) return send(res, 200, { ok: true });
  const email = String(data.email || '').trim().toLowerCase();
  if (!isEmail(email)) return send(res, 400, { error: 'Please enter a valid email address.' });
  if (!canSubscribe()) return send(res, 503, { error: 'Sign-up is not open yet. Please try again soon.' });

  try {
    await addContact(email, String(data.name || '').trim().slice(0, 80));
    return send(res, 200, { ok: true });
  } catch (err) {
    console.error('subscribe failed:', err.message);
    return send(res, 502, { error: 'We could not save your email. Please try again.' });
  }
};
