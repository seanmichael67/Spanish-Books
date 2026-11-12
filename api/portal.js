/*
 * POST /api/portal   { "t": "<access token>" }
 * For club members: opens Stripe's own "manage my subscription" page, where
 * they can update their card or cancel. Returns the address to send them to.
 * (Turn the customer portal on once in Stripe: Settings -> Billing -> Customer portal.)
 */
const { stripe, configured } = require('./_lib/stripe');
const { siteUrl, send, body, readToken } = require('./_lib/util');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return send(res, 405, { error: 'Use POST' });
  const access = readToken(String(body(req).t || ''));
  if (!access || !access.subscription) return send(res, 403, { error: 'No membership found for this link.' });
  if (!configured()) return send(res, 503, { error: 'The shop is not configured yet.' });
  try {
    const subscription = await stripe('GET', `/v1/subscriptions/${access.subscription}`);
    const portal = await stripe('POST', '/v1/billing_portal/sessions', { customer: subscription.customer, return_url: `${siteUrl(req)}/mis-compras/` });
    return send(res, 200, { url: portal.url });
  } catch (err) {
    console.error('portal failed:', err.message);
    return send(res, 502, { error: 'We could not open the membership page. Please email us and we will help.' });
  }
};
