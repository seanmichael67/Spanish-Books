/*
 * Builds the printable version of one or more books as a single web page.
 * Parents open it and choose "Print" (or "Save as PDF") in their browser.
 *
 * Each book prints as: cover · 6 story pages · picture vocabulary ·
 * cut-out flashcards · word tracing with talk-together questions.
 */
const { esc, vocabImages, highlight } = require('./text');
const { getTheme, config } = require('./catalog');
const CSS = require('./print-css');

const MEDIA = '/media';

/** A picture box. With `page` given, the box takes the picture's own shape so nothing is cropped. */
function pic(book, image, page, maxW, maxH) {
  const ratio = page && page.ratio ? page.ratio : 1.5;
  const size = maxW ? ` style="width:min(${maxW}in, ${(maxH * ratio).toFixed(2)}in);aspect-ratio:${ratio}"` : '';
  if (!image) return `<div class="pic empty"${size}>${esc(book.emoji)}</div>`;
  return `<div class="pic"${size}><img src="${MEDIA}/${book.slug}/${image}" alt=""></div>`;
}

function foot(book, label) {
  return `<div class="foot"><span>${esc(book.title)} · ${esc(label)}</span><span>${esc(config.name)} · ${esc(config.school)}</span></div>`;
}

function bookSheets(book) {
  const theme = getTheme(book.theme) || { color: '#ff6b4a', es: '', en: '' };
  const style = `style="--c:${theme.color}"`;
  const band = '<div class="band"></div>';
  const out = [];

  out.push(`<section class="sheet cover" ${style}>${band}
    ${pic(book, book.pages[0].image, book.pages[0], 6.6, 4.4)}
    <h1>${esc(book.title)}</h1>
    <div class="en">${esc(book.titleEn)}</div>
    <div class="chip">${esc(theme.es)} · Nivel ${book.level}</div>
    ${foot(book, 'Portada')}</section>`);

  book.pages.slice(1).forEach((p, i) => {
    out.push(`<section class="sheet story" ${style}>${band}
      ${pic(book, p.image, p, 6, 6.4)}
      <div class="words"><div class="es">${highlight(p.es, book.vocab, (w) => `<b>${w}</b>`)}</div><div class="en">${esc(p.en)}</div></div>
      ${foot(book, `Página ${i + 1}`)}</section>`);
  });

  const images = vocabImages(book);
  const cards = book.vocab.map((w) => {
    const img = images[w.es];
    const art = img ? pic(book, img) : `<div class="pic emoji">${esc(w.emoji || '⭐')}</div>`;
    return `<div class="card">${art}<div class="w">${esc(w.es)}</div><div class="t">${esc(w.en)}</div></div>`;
  }).join('');

  out.push(`<section class="sheet" ${style}>${band}<h2>Mis palabras</h2><div class="sub">My words. Point to each picture and say the word together.</div>
    <div class="grid6">${cards}</div>${foot(book, 'Vocabulario')}</section>`);

  out.push(`<section class="sheet cut" ${style}><h2>✂ Tarjetas</h2><div class="sub">Flashcards. Cut along the dotted lines. Play memory, or hide them around the room and go on a word hunt.</div>
    <div class="grid6">${cards}</div>${foot(book, 'Tarjetas')}</section>`);

  const [a, b] = book.vocab;
  out.push(`<section class="sheet" ${style}>${band}<h2>Traza y escribe</h2><div class="sub">Trace and write. Say each word out loud while you trace it.</div>
    <div class="trace">${book.vocab.map((w) => `<div class="row"><span>${esc(w.es)}</span><small>${esc(w.en)}</small></div>`).join('')}</div>
    <div class="talk"><b>Hablemos · Talk together:</b> ¿Qué ves en la portada? (What do you see on the cover?) · ¿Dónde está «${esc(a ? a.es : book.title)}»? Point to it! ·
      ¿Puedes decir «${esc(b ? b.es : book.title)}»? · ¿Cuál es tu página favorita? (Which page is your favorite?)</div>
    ${foot(book, 'Escritura')}</section>`);

  return out.join('\n');
}

function guideSheet(title, books, color) {
  return `<section class="sheet guide" style="--c:${color}"><div class="band"></div>
    <h1>${esc(title)}</h1>
    <p>Thank you for reading in Spanish with your child. You do not need to speak Spanish to use these books. A few minutes a day is enough.</p>
    <ol class="toc">${books.map((b) => `<li><b>${esc(b.title)}</b> · ${esc(b.titleEn)}</li>`).join('')}</ol>
    <div class="cols" style="margin-top:.2in">
      <div><h3>1. Look first</h3><p>Before reading, look at the picture together. Ask «¿Qué ves?» (What do you see?). Any answer, in any language, is a good answer.</p></div>
      <div><h3>2. Read and point</h3><p>Read the Spanish sentence slowly and point to each word. The coloured words are the new vocabulary. The website reads every page aloud if you want to hear it first.</p></div>
      <div><h3>3. Read it again</h3><p>Young children learn by repetition. Read the same book three or four days in a row and let your child finish the sentences.</p></div>
      <div><h3>4. Play with the words</h3><p>Cut out the flashcards, trace the words, and use them during the day: at breakfast, in the car, at the park.</p></div>
    </div>
    <div class="foot"><span>Guía para familias · Parent guide</span><span>${esc(config.name)} · ${esc(config.school)}</span></div></section>`;
}

function certificateSheet(books, color) {
  return `<section class="sheet cert" style="--c:${color}">
    <div class="medal">🏅</div><h1>¡Yo puedo leer en español!</h1><p>I can read in Spanish!</p>
    <div class="line"></div><p>Nombre · Name</p>
    <div class="stars">${books.map((b) => `<div><i>★</i>${esc(b.title)}</div>`).join('')}</div>
    <p style="font-size:11pt">Colour a star each time you finish a book.</p></section>`;
}

/**
 * @param {object} o
 * @param {string} o.title   Heading shown in the toolbar and browser tab
 * @param {object[]} o.books Books to include
 * @param {string} [o.note]  Small line in the toolbar (e.g. "Licensed to you@example.com")
 * @param {string} [o.backUrl]
 */
function renderPrintable({ title, books, note = '', backUrl = '/' }) {
  const color = (getTheme(books[0].theme) || {}).color || '#ff6b4a';
  const many = books.length > 1;
  return `<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=.5">
<meta name="robots" content="noindex">
<title>${esc(title)} · ${esc(config.name)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Fredoka:wght@500;600;700&display=swap" rel="stylesheet">
<style>${CSS}</style></head>
<body>
<div class="toolbar"><strong>${esc(title)}</strong><span>${esc(note || 'Paper: US Letter, landscape. For a PDF, choose "Save as PDF" as the printer.')}</span>
<a href="${esc(backUrl)}">← Back</a><button type="button" onclick="window.print()">🖨 Print / Save as PDF</button></div>
${many ? guideSheet(title, books, color) : ''}
${books.map(bookSheets).join('\n')}
${many ? certificateSheet(books, color) : ''}
</body></html>`;
}

module.exports = { renderPrintable };
