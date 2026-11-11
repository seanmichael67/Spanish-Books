/*
 * POST /api/restore   { "email": "..." }
 * "I bought a pack but lost my link." Looks up paid orders for that email in
 * Stripe and EMAILS a fresh link to that address. The link is never shown on
 * screen, so typing someone else's email does not unlock anything.
 */
const { getProduct, config } = require('./_lib/catalog');
const { stripe, configured } = require('./_lib/stripe');
const { sendEmail, canSend } = require('./_lib/email');
const { siteUrl, send, body, isEmail, makeToken } = require('./_lib/util');
const { esc } = require('./_lib/text');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return send(res, 405, { error: 'Use POST' });
  const email = String(body(req).email || '').trim().toLowerCase();
  if (!isEmail(email)) return send(res, 400, { error: 'Please enter a valid email address.' });
  if (!configured() || !canSend()) return send(res, 503, { error: `Email recovery is not set up yet. Please write to ${config.contactEmail}.` });

  // Same answer whether or not we find anything, so nobody can test which emails are customers.
  const done = () => send(res, 200, { ok: true });
  try {
    const found = await stripe('GET', '/v1/checkout/sessions', { 'customer_details[email]': email, status: 'complete', limit: '100' });
    const bought = (found.data || [])
      .filter((s) => s.payment_status === 'paid' && getProduct(s.metadata && s.metadata.product))
      .map((s) => s.metadata.product);
    if (!bought.length) return done();

    const link = `${siteUrl(req)}/mis-compras/?t=${encodeURIComponent(makeToken(bought, email))}`;
    await sendEmail({
      to: email,
      subject: `Your ${config.name} printables`,
      html: `<p>Here is your link to open and print everything you bought from ${esc(config.name)}:</p>
             <p><a href="${link}"><strong>Open my printables</strong></a></p>
             <p>If you did not ask for this email you can ignore it.</p>`,
    });
  } catch (err) { console.error('restore failed:', err.message); }
  return done();
};
