/*
 * Email through Resend (https://resend.com). One account does both jobs:
 *   - the mailing list  (RESEND_AUDIENCE_ID)
 *   - sending purchase links (RESEND_FROM, e.g. "Beibei Libros <hola@yourdomain.com>")
 * Needs RESEND_API_KEY (starts with re_).
 */
const BASE = () => process.env.RESEND_API_BASE || 'https://api.resend.com';
const configured = () => Boolean(process.env.RESEND_API_KEY);

async function resend(path, payload, extraHeaders = {}) {
  const res = await fetch(BASE() + path, {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json', ...extraHeaders },
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.message || `Resend error ${res.status}`);
    err.status = res.status;
    throw err;
  }
  return data;
}

/** Add a parent to the mailing list. */
function addContact(email, firstName) {
  return resend(`/audiences/${process.env.RESEND_AUDIENCE_ID}/contacts`, { email, first_name: firstName || undefined, unsubscribed: false });
}

/** Send one email. `key` stops the same email being sent twice. */
function sendEmail({ to, subject, html, key }) {
  return resend('/emails', { from: process.env.RESEND_FROM, to: [to], subject, html }, key ? { 'Idempotency-Key': key } : {});
}

const canSend = () => configured() && Boolean(process.env.RESEND_FROM);
const canSubscribe = () => configured() && Boolean(process.env.RESEND_AUDIENCE_ID);

module.exports = { addContact, sendEmail, canSend, canSubscribe };
