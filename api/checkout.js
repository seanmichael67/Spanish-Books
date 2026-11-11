/*
 * POST /api/checkout   { "product": "pack-animales" }
 * Creates a Stripe Checkout page for one product and returns its address.
 * The browser then sends the parent to Stripe to pay.
 */
const { getProduct, config } = require('./_lib/catalog');
const { stripe, configured } = require('./_lib/stripe');
const { siteUrl, send, body } = require('./_lib/util');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return send(res, 405, { error: 'Use POST' });
  const product = getProduct(body(req).product);
  if (!product) return send(res, 400, { error: 'Unknown product' });
  if (!configured()) return send(res, 503, { error: 'The shop is not open yet. Please check back soon.' });

  const site = siteUrl(req);
  try {
    const session = await stripe('POST', '/v1/checkout/sessions', {
      mode: 'payment',
      'line_items[0][quantity]': '1',
      'line_items[0][price_data][currency]': 'usd',
      'line_items[0][price_data][unit_amount]': String(product.priceCents),
      'line_items[0][price_data][product_data][name]': product.name,
      'line_items[0][price_data][product_data][description]': product.description,
      'metadata[product]': product.id,
      allow_promotion_codes: 'true',
      success_url: `${site}/gracias/?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${site}/packs/`,
      'custom_text[submit][message]': `Digital printable from ${config.name}. You can print it right after paying.`,
    });
    return send(res, 200, { url: session.url });
  } catch (err) {
    console.error('checkout failed:', err.message);
    return send(res, 502, { error: 'We could not start the checkout. Please try again.' });
  }
};
