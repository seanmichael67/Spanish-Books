/*
 * GET /api/access?session_id=cs_...
 * Called by the thank-you page. Asks Stripe "was this really paid?" and, if
 * yes, returns a signed access token that unlocks the printable pack.
 * Also emails the parent a link so they can print again on any device.
 */
const { getProduct, config } = require('./_lib/catalog');
const { stripe, configured } = require('./_lib/stripe');
const { sendEmail, canSend } = require('./_lib/email');
const { siteUrl, send, makeToken } = require('./_lib/util');
const { esc } = require('./_lib/text');

module.exports = async (req, res) => {
  const id = String((req.query && req.query.session_id) || '');
  if (!/^cs_[A-Za-z0-9_]+$/.test(id)) return send(res, 400, { error: 'Missing or invalid session_id' });
  if (!configured()) return send(res, 503, { error: 'The shop is not configured yet.' });

  try {
    const session = await stripe('GET', `/v1/checkout/sessions/${id}`);
    const product = getProduct(session.metadata && session.metadata.product);
    if (session.payment_status !== 'paid' || !product) return send(res, 402, { error: 'This payment is not complete yet.' });

    const email = (session.customer_details && session.customer_details.email) || '';
    const token = makeToken([product.id], email, product.recurring ? String(session.subscription || '') : '');

    let emailed = false;
    if (email && canSend()) {
      const link = `${siteUrl(req)}/mis-compras/?t=${encodeURIComponent(token)}`;
      try {
        await sendEmail({
          to: email,
          key: `purchase-${id}`,
          subject: `Your printable is ready: ${product.name}`,
          html: `<p>¡Gracias! Thank you for your purchase from ${esc(config.name)}.</p>
                 <p><a href="${link}"><strong>Open and print ${esc(product.name)}</strong></a></p>
                 <p>Keep this email. The link works on any computer, as many times as you like${product.recurring ? ', for as long as you are a member' : ''}.</p>
                 <p>Happy reading,<br>${esc(config.school)}</p>`,
        });
        emailed = true;
      } catch (err) { console.error('purchase email failed:', err.message); }
    }
    return send(res, 200, { token, product: product.id, name: product.name, email, emailed });
  } catch (err) {
    console.error('access failed:', err.message);
    return send(res, err.status === 404 ? 404 : 502, { error: 'We could not confirm this payment. Please contact us and we will sort it out.' });
  }
};
