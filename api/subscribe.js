/*
 * POST /api/subscribe   { "email": "...", "name": "..." }
 * Adds a parent to the mailing list (Resend audience).
 */
const { addContact, canSubscribe, sendEmail, canSend } = require('./_lib/email');
const { send, body, isEmail, siteUrl } = require('./_lib/util');
const { config, getBook } = require('./_lib/catalog');
const { esc } = require('./_lib/text');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return send(res, 405, { error: 'Use POST' });
  const data = body(req);
  // "website" is a hidden field real people never fill in. Robots do.
  if (data.website) return send(res, 200, { ok: true });
  const email = String(data.email || '').trim().toLowerCase();
  if (!isEmail(email)) return send(res, 400, { error: 'Please enter a valid email address.' });
  if (!canSubscribe()) return send(res, 503, { error: 'Sign-up is not open yet. Please try again soon.' });

  try {
    const name = String(data.name || '').trim().slice(0, 80);
    await addContact(email, name);

    // Welcome email with the free printable book. If it fails, the sign-up still counts.
    if (canSend()) {
      const site = siteUrl(req);
      const book = getBook(config.freeSampleBook);
      try {
        await sendEmail({
          to: email,
          key: `welcome-${email}`,
          subject: `¡Bienvenidos! Your free Spanish book is inside`,
          html: `<p>¡Hola${name ? ' ' + esc(name) : ''}!</p>
                 <p>Welcome to the ${esc(config.name)} book club. Here is your free printable book, with flashcards and a tracing page:</p>
                 <p><a href="${site}/muestra/"><strong>Print “${esc(book.title)}” (${esc(book.titleEn)})</strong></a></p>
                 <p><strong>A 10-minute way to read it:</strong> look at the pictures first and ask «¿Qué ves?» (What do you see?). Then
                 <a href="${site}/libros/${book.slug}/">listen to the book online</a> and point to each word. Read it again tomorrow.</p>
                 <p>Each week we will send one new book to read together. There are ${require('./_lib/catalog').books.length} free books waiting in the <a href="${site}/libros/">library</a>.</p>
                 <p>Con cariño,<br>${esc(config.school)}</p>`,
        });
      } catch (err) { console.error('welcome email failed:', err.message); }
    }
    return send(res, 200, { ok: true });
  } catch (err) {
    console.error('subscribe failed:', err.message);
    return send(res, 502, { error: 'We could not save your email. Please try again.' });
  }
};
