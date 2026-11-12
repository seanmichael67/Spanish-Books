/*
 * A tiny Stripe client. We call Stripe's web API directly with fetch, so there
 * is no extra package to install. Needs STRIPE_SECRET_KEY (starts with sk_).
 */
const BASE = () => process.env.STRIPE_API_BASE || 'https://api.stripe.com';

const configured = () => Boolean(process.env.STRIPE_SECRET_KEY);

async function stripe(method, path, params) {
  const qs = params ? new URLSearchParams(params).toString() : '';
  const url = BASE() + path + (method === 'GET' && qs ? `?${qs}` : '');
  const res = await fetch(url, {
    method,
    headers: {
      Authorization: `Bearer ${process.env.STRIPE_SECRET_KEY}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: method === 'GET' ? undefined : qs,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error((data.error && data.error.message) || `Stripe error ${res.status}`);
    err.status = res.status;
    throw err;
  }
  return data;
}

/** Is this membership still running? (Stripe statuses "active" and "trialing" count.) */
async function membershipActive(subscriptionId) {
  if (!/^sub_[A-Za-z0-9_]+$/.test(subscriptionId || '')) return false;
  try {
    const s = await stripe('GET', `/v1/subscriptions/${subscriptionId}`);
    return s.status === 'active' || s.status === 'trialing';
  } catch (err) { return false; }
}

module.exports = { stripe, configured, membershipActive };
