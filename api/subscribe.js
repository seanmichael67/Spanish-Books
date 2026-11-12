/*
 * POST /api/subscribe   { "email": "...", "name": "..." }
 * Adds a parent to the mailing list (Resend audience).
 */
const { addContact, canSubscribe, sendEmail, canSend } = require('./_lib/email');
const { send, body, isEmail, siteUrl } = require('./_lib/util');
const { config, getBook, packs } = require('./_lib/catalog');
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
        // Two follow-ups, scheduled now and delivered later by Resend.
        const pack = packs[0];
        await sendEmail({
          to: email,
          key: `tips-${email}`,
          inHours: 24,
          subject: 'A 10-minute Spanish reading routine',
          html: `<p>¡Hola${name ? ' ' + esc(name) : ''}!</p>
                 <p>Here is the routine our teachers use. It takes ten minutes and works even if you are learning Spanish too.</p>
                 <ol><li><strong>Picture walk.</strong> Turn the pages without reading and ask «¿Qué ves?»</li>
                 <li><strong>Listen.</strong> Play each page and point under each word.</li>
                 <li><strong>Echo.</strong> You say the sentence, your child repeats it.</li>
                 <li><strong>Play.</strong> At the end, press “Jugar” and let your child find each word.</li></ol>
                 <p>Read the same book for three days in a row. <a href="${site}/padres/">The full guide is here</a>, and
                 <a href="${site}/libros/">all the books are here</a>.</p>
                 <p>Con cariño,<br>${esc(config.school)}</p>`,
        });
        await sendEmail({
          to: email,
          key: `offer-${email}`,
          inHours: 70,
          subject: 'Take the books off the screen',
          html: `<p>¡Hola${name ? ' ' + esc(name) : ''}!</p>
                 <p>Children remember words best when they can hold them. Our printable packs turn each theme into paper books
                 with picture vocabulary, cut-out flashcards and tracing pages.</p>
                 <p>Each pack has 8 books and costs $${(pack.priceCents / 100).toFixed(0)}, once. You print it as many times as you need.</p>
                 <p><a href="${site}/packs/"><strong>See the printable packs</strong></a></p>
                 <p>Did you try the free sample yet? <a href="${site}/muestra/">Print “${esc(book.title)}” here.</a></p>
                 <p>Con cariño,<br>${esc(config.school)}</p>`,
        });
      } catch (err) { console.error('welcome emails failed:', err.message); }
    }
    return send(res, 200, { ok: true });
  } catch (err) {
    console.error('subscribe failed:', err.message);
    return send(res, 502, { error: 'We could not save your email. Please try again.' });
  }
};
