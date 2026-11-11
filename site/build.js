#!/usr/bin/env node
/*
 * Builds the whole website into site/dist.
 *
 *   node site/build.js
 *
 * It reads the books (site/data/books.json), makes one fast, plain web page
 * per book, plus the home page, library, shop and help pages, and copies the
 * pictures and audio next to them. Vercel runs this automatically on deploy.
 */
const fs = require('fs');
const path = require('path');
const { books, themes, config, packs, library, school, getTheme, booksByTheme } = require('../api/_lib/catalog');
const { esc, vocabImages, highlight, syllableWord } = require('../api/_lib/text');
const { renderPrintable } = require('../api/_lib/print');

const ROOT = path.join(__dirname, '..');
const DIST = path.join(__dirname, 'dist');
const SITE_URL = (process.env.SITE_URL || (process.env.VERCEL_PROJECT_PRODUCTION_URL ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}` : '')).replace(/\/+$/, '');
const YEAR = new Date().getFullYear();
const money = (cents) => '$' + (cents % 100 ? (cents / 100).toFixed(2) : cents / 100);
const sitemap = [];

/* ---------- helpers ---------- */
function write(file, html) {
  const full = path.join(DIST, file);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, html);
}

function copyMedia() {
  let files = 0;
  for (const book of books) {
    const from = path.join(ROOT, 'books', book.folder);
    const to = path.join(DIST, 'media', book.slug);
    fs.mkdirSync(to, { recursive: true });
    const wanted = new Set(['thumb.webp']);
    book.pages.forEach((p) => { if (p.image) wanted.add(p.image); if (p.audio) wanted.add(p.audio); });
    book.vocab.forEach((w) => { if (w.audio) wanted.add(w.audio); });
    for (const name of wanted) {
      const src = path.join(from, name.endsWith('.mp3') ? 'audio' : 'images', name);
      if (fs.existsSync(src)) { fs.copyFileSync(src, path.join(to, name)); files++; }
    }
  }
  return files;
}

const LEVELS = { 1: 'Nivel 1 · First words', 2: 'Nivel 2 · Short sentences', 3: 'Nivel 3 · Longer sentences' };
const media = (book, file) => `/media/${book.slug}/${file}`;
const hasThumb = (book) => fs.existsSync(path.join(ROOT, 'books', book.folder, 'images', 'thumb.webp'));

function bookCard(book) {
  const theme = getTheme(book.theme);
  const cover = hasThumb(book)
    ? `<img src="${media(book, 'thumb.webp')}" alt="" width="480" height="360" loading="lazy" decoding="async">`
    : esc(book.emoji);
  return `<a class="book" href="/libros/${book.slug}/" data-theme="${book.theme}" data-level="${book.level}" style="--c:${theme.color}">
    <div class="cov">${cover}</div>
    <div class="meta"><b>${esc(book.title)}</b><small>${esc(book.titleEn)}</small><span class="lvl">Nivel ${book.level}</span></div></a>`;
}

function signup(heading, text) {
  return `<div class="signup" id="club">
    <div><h2>${heading}</h2><p>${text}</p></div>
    <form data-signup novalidate>
      <label class="sr" for="su-name">Your first name</label>
      <input id="su-name" type="text" name="name" placeholder="Your first name (optional)" autocomplete="given-name">
      <label class="sr" for="su-email">Your email</label>
      <input id="su-email" type="email" name="email" placeholder="Your email" autocomplete="email" required>
      <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn" type="submit">Send me the free book</button>
      <div class="msg" role="status" aria-live="polite"></div>
      <p class="note">For parents and teachers. One short email a week. Unsubscribe any time. <a href="/privacidad/" style="color:inherit">Privacy</a></p>
    </form></div>`;
}

function layout({ title, description, urlPath, body, head = '', scripts = '', active = '', noindex = false }) {
  const canonical = SITE_URL ? `<link rel="canonical" href="${SITE_URL}${urlPath}">` : '';
  if (!noindex) sitemap.push(urlPath);
  const nav = [['/libros/', 'Books'], ['/packs/', 'Printable packs'], ['/padres/', 'For parents'], ['/mis-compras/', 'My purchases']]
    .map(([href, label]) => `<a href="${href}"${active === href ? ' aria-current="page"' : ''}>${label}</a>`).join('');
  const ga = config.analyticsId ? `<script async src="https://www.googletagmanager.com/gtag/js?id=${config.analyticsId}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','${config.analyticsId}');</script>` : '';
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(description)}">
${noindex ? '<meta name="robots" content="noindex">' : ''}
${canonical}
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:type" content="website">
${SITE_URL ? `<meta property="og:url" content="${SITE_URL}${urlPath}">` : ''}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📖</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&family=Fredoka:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css">
${head}
${ga}
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/"><i>📖</i>${esc(config.name)}</a>
  <button class="menu-btn" aria-label="Menu" aria-expanded="false">☰</button>
  <nav class="nav" aria-label="Main">${nav}</nav>
</div></header>
<main>
${body}
</main>
<footer class="site"><div class="wrap">
  <div class="cols">
    <div><h3>📖 ${esc(config.name)}</h3><p>${esc(config.tagline)}. Written and read in the classroom by the teachers of <a href="${config.schoolUrl}">${esc(config.school)}</a>, a trilingual Montessori-inspired preschool in Phoenix, Arizona.</p></div>
    <div><h3>Read</h3><ul><li><a href="/libros/">All books</a></li><li><a href="/packs/">Printable packs</a></li><li><a href="/muestra/">Free printable book</a></li><li><a href="/padres/">How to read together</a></li></ul></div>
    <div><h3>Help</h3><ul><li><a href="/mis-compras/">My purchases</a></li><li><a href="mailto:${config.contactEmail}">${config.contactEmail}</a></li><li><a href="/privacidad/">Privacy</a></li><li><a href="/terminos/">Terms</a></li></ul></div>
  </div>
  <div class="fine">© ${YEAR} ${esc(config.school)}. Made with cariño for bilingual families.</div>
</div></footer>
<script src="/assets/site.js" defer></script>
${scripts}
</body>
</html>`;
}

/* ---------- Home ---------- */
function home() {
  const pick = (slug) => books.find((b) => b.slug === slug) || books[0];
  const fan = ['la-mariposa', 'el-pulpo', 'el-oso'].map(pick);
  const featured = themes.map((t) => booksByTheme(t.id)[0]).filter(Boolean).slice(0, 10);
  const faq = [
    ['Do I need to speak Spanish?', 'No. Every page has a recording by a native-sounding Spanish voice and a small English translation. You and your child can learn the words together.'],
    ['What ages are the books for?', 'Ages 2 to 6. Nivel 1 books use two or three word sentences for toddlers. Nivel 3 books use longer sentences for children who are starting to read.'],
    ['Are the books really free?', `Yes. All ${books.length} books are free to read on this site, with audio. The printable packs are the only thing we sell, and they pay for new books.`],
    ['What is in a printable pack?', 'Eight books on one theme, ready to print at home: one big sentence per page, a picture vocabulary page, cut-out flashcards, and a trace-and-write page for each book, plus a parent guide and a reading certificate.'],
    ['Can teachers use them in class?', 'Yes. One purchase covers one classroom or one family. Schools that want a licence for several classrooms can email us.'],
  ];
  const body = `
<section class="hero"><div class="wrap">
  <div>
    <span class="kicker">🇲🇽 ${books.length} free read-along books · ages 2–6</span>
    <h1>Your child's first books in Spanish.</h1>
    <p class="lead">Real photos, one short sentence per page, and a warm Spanish voice that reads along. Made by preschool teachers so that any family can read in Spanish, even if you are learning too.</p>
    <div class="cta"><a class="btn" href="/libros/">Start reading free</a><a class="btn alt" href="#club">Get a free printable book</a></div>
    <ul class="ticks"><li>No app, no login</li><li>Audio on every page</li><li>Vocabulary at the end of every book</li></ul>
  </div>
  <div class="fan">${fan.map((b) => `<a href="/libros/${b.slug}/"><img src="${media(b, 'thumb.webp')}" alt="Cover of ${esc(b.title)}" width="480" height="360"><span>${esc(b.title)}</span></a>`).join('')}</div>
</div></section>

<section class="block tint"><div class="wrap center">
  <h2>Reading that actually teaches</h2>
  <p class="sub">Each book follows the same gentle pattern, so children know what to expect and can focus on the new words.</p>
  <div class="steps" style="text-align:left">
    <div class="step"><span class="n">👀</span><h3>See it</h3><p>One clear picture and one short sentence per page. Nothing else competes for attention.</p></div>
    <div class="step"><span class="n">👂</span><h3>Hear it</h3><p>Tap Escuchar to hear the page in Spanish. Tap any coloured word to hear it on its own.</p></div>
    <div class="step"><span class="n">🗣️</span><h3>Say it</h3><p>Six key words come back at the end as picture cards, so your child says them again.</p></div>
    <div class="step"><span class="n">✏️</span><h3>Keep it</h3><p>Print the book, cut out the flashcards and trace the words. Paper is where reading sticks.</p></div>
  </div>
</div></section>

<section class="block"><div class="wrap">
  <h2>Start with one of these</h2>
  <p class="sub">A first book from each theme. Free to read, with audio.</p>
  <div class="books">${featured.map(bookCard).join('')}</div>
  <p style="margin-top:26px"><a class="btn alt" href="/libros/">See all ${books.length} books</a></p>
</div></section>

<section class="block tint"><div class="wrap">
  <h2>Printable packs for home and classroom</h2>
  <p class="sub">Take the books off the screen. Each pack is 8 books on one theme with vocabulary, flashcards and tracing pages. ${money(config.packPriceCents)} per pack, or every pack for ${money(config.libraryPriceCents)}.</p>
  <div class="packs">${packs.slice(0, 3).map(packCard).join('')}</div>
  <p style="margin-top:26px"><a class="btn" href="/packs/">See all ${packs.length} packs</a></p>
</div></section>

<section class="block"><div class="wrap">
  ${signup('Get a free printable book', `Join the Beibei book club and we will send you <b>${esc(pick(config.freeSampleBook).title)}</b> to print today, plus a new book and a simple Spanish tip each week.`)}
</div></section>

<section class="block tint"><div class="narrow">
  <h2 class="center">Questions parents ask</h2>
  <div style="margin-top:22px">${faq.map(([q, a]) => `<details><summary>${q}</summary><p>${a}</p></details>`).join('')}</div>
</div></section>`;

  const ld = {
    '@context': 'https://schema.org',
    '@graph': [
      { '@type': 'WebSite', name: config.name, description: config.tagline, ...(SITE_URL ? { url: SITE_URL } : {}) },
      { '@type': 'FAQPage', mainEntity: faq.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) },
    ],
  };
  write('index.html', layout({
    title: `${config.name}: free Spanish read-along books for kids ages 2–6`,
    description: `${books.length} free Spanish books for toddlers and preschoolers with real photos, audio on every page and vocabulary at the end. Printable packs with flashcards for parents and teachers.`,
    urlPath: '/',
    body,
    head: `<script type="application/ld+json">${JSON.stringify(ld)}</script>`,
  }));
}

/* ---------- Library ---------- */
function libraryPage() {
  const body = `
<div class="wrap page-head">
  <h1>Spanish books for little readers</h1>
  <p class="sub">All free to read, with audio. Pick a theme or a reading level. Showing <b data-count>${books.length}</b> books.</p>
  <p class="progress" data-progress hidden></p>
  <div class="filters" role="group" aria-label="Filter books">
    <button data-filter="theme" value="all" aria-pressed="true">📚 All themes</button>
    ${themes.filter((t) => booksByTheme(t.id).length).map((t) => `<button data-filter="theme" value="${t.id}" aria-pressed="false">${t.emoji} ${esc(t.en)}</button>`).join('')}
    <span class="sep"></span>
    <button data-filter="level" value="all" aria-pressed="true">All levels</button>
    ${[1, 2, 3].map((n) => `<button data-filter="level" value="${n}" aria-pressed="false">${LEVELS[n]}</button>`).join('')}
  </div>
</div>
<div class="wrap" data-library>
  <div class="books">${books.map(bookCard).join('')}</div>
  <p class="empty-note">No books match yet. Try another theme or level.</p>
</div>
<section class="block"><div class="wrap">${signup('A new book every week', 'Join the book club for a free printable book today and a short email each week with a new book to read together.')}</div></section>`;
  write('libros/index.html', layout({
    title: `All ${books.length} free Spanish books for kids · ${config.name}`,
    description: `Browse ${books.length} free Spanish read-along books for ages 2–6 by theme and reading level: animals, food, family, colors, numbers and more.`,
    urlPath: '/libros/',
    body,
    active: '/libros/',
  }));
}

/* ---------- One book ---------- */
function bookPage(book) {
  const theme = getTheme(book.theme);
  const siblings = booksByTheme(book.theme);
  const nextBook = siblings[(siblings.indexOf(book) + 1) % siblings.length];
  const pack = packs.find((p) => p.theme === book.theme);
  const isSample = book.slug === config.freeSampleBook;

  const kw = (word, v) => `<button type="button" class="kw" data-word="${esc(v.es)}"${v.audio ? ` data-word-audio="${media(book, v.audio)}"` : ''}>${word}</button>`;

  const story = book.pages.map((p, i) => {
    const art = p.image
      ? `<img class="bg" src="${media(book, p.image)}" alt="" aria-hidden="true" ${i ? 'loading="lazy"' : ''}><img class="fg" src="${media(book, p.image)}" alt="${esc(p.en)}" ${i ? 'loading="lazy"' : 'fetchpriority="high"'}>`
      : `<span class="ph" aria-hidden="true">${esc(book.emoji)}</span>`;
    const text = p.syllable
      ? `<span class="syl">${esc(p.syllable)}</span>${(() => { const v = book.vocab.find((w) => w.es === p.es); return v ? kw(syllableWord(p), v) : syllableWord(p); })()}`
      : i === 0 ? esc(p.es) : highlight(p.es, book.vocab, kw);
    return `<section class="pg${i === 0 ? ' on' : ''}" data-say="${esc(p.say || p.es)}"${p.audio ? ` data-audio="${media(book, p.audio)}"` : ''}>
      <figure class="frame">${art}</figure>
      <div class="txt"><p class="es" lang="es">${text}</p><p class="en">${esc(p.en)}</p></div></section>`;
  }).join('\n');

  const vocab = `<section class="pg vocab"><h2 lang="es">Mis palabras</h2><p data-vocab-help>My words. Tap a card to hear it, then say it together.</p>
    <div class="game-bar"><button type="button" class="btn small sun" data-game>🎮 Jugar: ¿Dónde está…?</button><span class="ask" data-ask lang="es" aria-live="polite"></span><span class="stars" data-stars aria-hidden="true"></span></div>
    <div class="vgrid">${book.vocab.map((w) => {
      const img = vocabImages(book)[w.es];
      return `<button type="button" class="vcard" data-word="${esc(w.es)}"${w.audio ? ` data-word-audio="${media(book, w.audio)}"` : ''}>
        <span class="vp">${img ? `<img src="${media(book, img)}" alt="" loading="lazy">` : esc(w.emoji || '⭐')}</span>
        <span class="w" lang="es">${esc(w.es)}</span><span class="t">${esc(w.en)}</span></button>`;
    }).join('')}</div></section>`;

  const printLink = isSample
    ? `<a href="/muestra/"><b>🖨 Print this book free</b><span>With flashcards and tracing page.</span></a>`
    : pack ? `<a href="/packs/#${pack.id}"><b>🖨 Print this book</b><span>In the ${esc(theme.en)} pack: 8 books, flashcards and tracing.</span></a>` : '';
  const badge = `<section class="pg badge"><div class="medal">${esc(book.badge.emoji)}</div>
    <h2 lang="es">¡Lo lograste!</h2><p>You did it! You earned the <b lang="es">${esc(book.badge.es)}</b> badge (${esc(book.badge.en)}).</p>
    <p class="progress" data-read-count></p>
    <div class="next">
      <a href="/libros/${nextBook.slug}/"><b>📖 Next: ${esc(nextBook.title)}</b><span>${esc(nextBook.titleEn)} · ${esc(theme.en)}</span></a>
      ${printLink}
      <a href="/temas/${book.theme}/"><b>${theme.emoji} More ${esc(theme.en)}</b><span>All ${siblings.length} books in this theme.</span></a>
    </div></section>`;

  const body = `
<div class="wrap">
  <p class="crumbs"><a href="/libros/">Books</a> › <a href="/temas/${book.theme}/">${esc(theme.en)}</a> › ${esc(book.title)}</p>
  <article class="reader" data-book="${book.slug}" style="--c:${theme.color}">
    <div class="reader-head"><h1><span lang="es">${esc(book.title)}</span></h1><span class="lvl">${LEVELS[book.level]}</span></div>
    <div class="stage">${story}\n${vocab}\n${badge}</div>
    <div class="controls">
      <button class="round" data-prev aria-label="Previous page">←</button>
      <button class="round listen" data-listen>🔊 Escuchar</button>
      <div class="dots" aria-hidden="true"></div>
      <button class="round" data-next aria-label="Next page">→</button>
    </div>
    <div class="toggles">
      <label><input type="checkbox" data-auto> Read each page aloud when I turn it</label>
      <label><input type="checkbox" data-english checked> Show English</label>
    </div>
  </article>

  <div class="under">
    <div class="box"><h2>Read it together</h2>
      <ol>
        <li><b>Look first.</b> Before reading, ask <span lang="es">«¿Qué ves?»</span> <i>(What do you see?)</i></li>
        <li><b>Listen and point.</b> Tap Escuchar and point to each word as it is read.</li>
        <li><b>Find the coloured words.</b> Can your child say <span lang="es">«${esc(book.vocab[0].es)}»</span> and <span lang="es">«${esc(book.vocab[1].es)}»</span>?</li>
        <li><b>Read it again tomorrow.</b> Repetition is how young children learn to read.</li>
      </ol>
    </div>
    <div class="box"><h2>Words in this book</h2>
      <ul>${book.vocab.map((w) => `<li><b lang="es">${esc(w.es)}</b> <i>· ${esc(w.en)}</i></li>`).join('')}</ul>
      <p style="margin:14px 0 0"><a class="btn small sun" href="${isSample ? '/muestra/' : pack ? `/packs/#${pack.id}` : '/packs/'}">🖨 ${isSample ? 'Print this book free' : 'Get the printable'}</a></p>
    </div>
  </div>
</div>`;

  const ld = {
    '@context': 'https://schema.org', '@type': 'Book', name: book.title, alternateName: book.titleEn, inLanguage: 'es',
    bookFormat: 'https://schema.org/EBook', isAccessibleForFree: true, typicalAgeRange: '2-6', genre: `Children's Spanish reader: ${theme.en}`,
    abstract: book.pages.slice(1).map((p) => p.es).join(' '),
    publisher: { '@type': 'Organization', name: config.school, url: config.schoolUrl },
    ...(SITE_URL ? { url: `${SITE_URL}/libros/${book.slug}/`, image: `${SITE_URL}${media(book, book.pages[0].image || 'thumb.webp')}` } : {}),
  };
  write(`libros/${book.slug}/index.html`, layout({
    title: `${book.title} (${book.titleEn}): free Spanish book for kids with audio · ${config.name}`,
    description: `Read “${book.title}” free online: a Spanish read-along book for ages 2–6 about ${book.titleEn.toLowerCase().replace(/^the /, '')}. Audio on every page. Words: ${book.vocab.map((w) => w.es).join(', ')}.`,
    urlPath: `/libros/${book.slug}/`,
    body,
    active: '/libros/',
    head: `<script type="application/ld+json">${JSON.stringify(ld)}</script>${SITE_URL && book.pages[0].image ? `<meta property="og:image" content="${SITE_URL}${media(book, book.pages[0].image)}">` : ''}`,
    scripts: '<script src="/assets/reader.js" defer></script>',
  }));
}

/* ---------- One page per theme (good for Google, and it sells the matching pack) ---------- */
function themePages() {
  themes.filter((t) => booksByTheme(t.id).length).forEach((t) => {
    const list = booksByTheme(t.id);
    const pack = packs.find((p) => p.theme === t.id);
    const words = [];
    list.forEach((b) => b.vocab.forEach((w) => { if (!words.some((x) => x.es === w.es)) words.push(w); }));
    const body = `
<div class="wrap page-head" style="--c:${t.color}">
  <p class="crumbs" style="padding-top:0"><a href="/libros/">Books</a> › ${esc(t.en)}</p>
  <h1>${t.emoji} Spanish books about ${esc(t.en.toLowerCase())}</h1>
  <p class="sub"><span lang="es">${esc(t.es)}</span>: ${list.length} free read-along books for ages 2–6, with audio on every page and ${words.length} Spanish words to learn.</p>
  <div class="books">${list.map(bookCard).join('')}</div>
</div>
<section class="block"><div class="wrap">
  ${pack ? `<div class="bundle"><div><h2>Print the ${esc(t.en)} pack</h2><p>All ${list.length} books on paper, with picture vocabulary, ${list.length * 6} cut-out flashcards, tracing pages, a parent guide and a reading certificate.</p></div>
    <div style="text-align:center"><div class="price">${money(pack.priceCents)} <small>one time</small></div><button class="btn sun" data-buy="${pack.id}" style="margin-top:10px">Buy this pack</button><p style="margin-top:10px"><a href="/muestra/" style="color:#fff">See a free sample</a></p></div></div>` : ''}
</div></section>
<section class="block tint"><div class="wrap">
  <h2>${words.length} Spanish words in this theme</h2>
  <p class="sub">Every word below is taught in one of the books above, with its picture and sound.</p>
  <ul class="wordlist">${words.map((w) => `<li><b lang="es">${esc(w.es)}</b> <span>${esc(w.en)}</span></li>`).join('')}</ul>
</div></section>`;
    write(`temas/${t.id}/index.html`, layout({
      title: `Spanish books about ${t.en.toLowerCase()} for kids (${t.es}) · ${config.name}`,
      description: `${list.length} free Spanish read-along books about ${t.en.toLowerCase()} for ages 2–6, with audio. Learn ${words.slice(0, 6).map((w) => w.es).join(', ')} and more. Printable pack available.`,
      urlPath: `/temas/${t.id}/`,
      body,
      active: '/libros/',
    }));
  });
}

/* ---------- Shop ---------- */
function packCard(p) {
  const theme = getTheme(p.theme);
  return `<div class="pack" id="${p.id}" style="--c:${theme.color}">
    <div class="em">${theme.emoji}</div><h3>${esc(theme.en)}</h3><div class="es" lang="es">${esc(theme.es)}</div>
    <ul lang="es">${booksByTheme(p.theme).map((b) => `<li>${esc(b.title)}</li>`).join('')}</ul>
    <div class="buy"><span class="price">${money(p.priceCents)} <small>one time</small></span><button class="btn small" data-buy="${p.id}">Buy pack</button></div></div>`;
}

function packsPage() {
  const full = packs.length * config.packPriceCents;
  const body = `
<div class="wrap page-head">
  <h1>Printable Spanish book packs</h1>
  <p class="sub">Eight books on one theme, ready to print at home or school. Pay once, print as many times as you need for your family or your classroom.</p>
  <div class="inside">
    <div><span>📖</span><b>8 books per pack</b><p>One big sentence and one picture per page, sized for small hands and group reading.</p></div>
    <div><span>🖼️</span><b>Picture vocabulary</b><p>Six key words per book with their pictures, at the end of every book.</p></div>
    <div><span>✂️</span><b>Cut-out flashcards</b><p>48 cards per pack for memory games and word hunts.</p></div>
    <div><span>✏️</span><b>Trace and write</b><p>A writing page for each book, plus questions to talk about together.</p></div>
    <div><span>🏅</span><b>Guide and certificate</b><p>A one-page parent guide and a reading certificate to colour in.</p></div>
  </div>
  <p style="margin-top:22px"><a class="btn alt small" href="/muestra/">👀 See a free sample book first</a></p>
  <div class="bundle">
    <div><h2>Biblioteca Completa</h2><p>Every pack: ${library.books.length} printable books, ${library.books.length * 6} flashcards, and every pack we add later this year. Best for teachers and homeschool families.</p></div>
    <div style="text-align:center"><s>${money(full)}</s><div class="price">${money(library.priceCents)} <small>one time</small></div><button class="btn sun" data-buy="${library.id}" style="margin-top:10px">Get every pack</button></div>
  </div>
  <div class="bundle school" id="${school.id}">
    <div><h2>🏫 For schools</h2><p>One licence for every classroom and teacher at your school: all ${library.books.length} printable books, flashcards and tracing pages, plus every pack we add. Made and classroom-tested at ${esc(config.school)}.</p></div>
    <div style="text-align:center"><div class="price">${money(school.priceCents)} <small>one time</small></div><button class="btn" data-buy="${school.id}" style="margin-top:10px">Get the school licence</button></div>
  </div>
</div>
<div class="wrap"><div class="packs">${packs.map(packCard).join('')}</div>
<p class="note" style="margin-top:24px">Secure checkout by Stripe. Digital product: you print it yourself on US Letter paper. Not happy? Email ${config.contactEmail} within 14 days for a refund.</p></div>`;
  const ld = {
    '@context': 'https://schema.org', '@graph': [...packs, library, school].map((p) => ({
      '@type': 'Product', name: p.name, description: p.description, brand: { '@type': 'Brand', name: config.name },
      offers: { '@type': 'Offer', price: (p.priceCents / 100).toFixed(2), priceCurrency: 'USD', availability: 'https://schema.org/InStock', ...(SITE_URL ? { url: `${SITE_URL}/packs/#${p.id}` } : {}) },
    })),
  };
  write('packs/index.html', layout({
    title: `Printable Spanish books for kids with flashcards · ${config.name}`,
    description: `Printable Spanish book packs for ages 2–6: 8 books per theme with picture vocabulary, cut-out flashcards and tracing pages. ${money(config.packPriceCents)} per pack.`,
    urlPath: '/packs/',
    body,
    active: '/packs/',
    head: `<script type="application/ld+json">${JSON.stringify(ld)}</script>`,
  }));
}

/* ---------- Purchases ---------- */
function catalogJson() {
  const data = packs.map((p) => {
    const t = getTheme(p.theme);
    return { id: p.id, name: `${t.en} pack`, emoji: t.emoji, books: booksByTheme(p.theme).map((b) => ({ slug: b.slug, title: b.title })) };
  });
  return `<script type="application/json" id="catalog">${JSON.stringify(data).replace(/</g, '\\u003c')}</script>`;
}

function purchasePages() {
  write('gracias/index.html', layout({
    title: `Thank you · ${config.name}`, description: 'Your printable pack is ready.', urlPath: '/gracias/', noindex: true,
    body: `<div class="narrow page-head" data-thanks><h1>¡Gracias!</h1>
      <p class="msg" data-status role="status">Confirming your payment…</p>
      <div class="owned" data-owned></div>
      <div class="callout"><b>Printing tips:</b> choose US Letter paper, landscape, and turn on “background graphics”. To keep a PDF, choose “Save as PDF” as the printer. You can come back any time from <a href="/mis-compras/">My purchases</a>.</div>
      ${catalogJson()}</div>`,
  }));
  write('mis-compras/index.html', layout({
    title: `My purchases · ${config.name}`, description: 'Open and print the packs you bought.', urlPath: '/mis-compras/', noindex: true, active: '/mis-compras/',
    body: `<div class="narrow page-head" data-mine><h1>My purchases</h1>
      <div class="owned" data-owned></div>
      <div data-none><p class="sub">No packs are saved in this browser yet.</p><p><a class="btn" href="/packs/">See the printable packs</a></p></div>
      <div class="box" style="margin-top:30px"><h2>Bought on another device?</h2>
        <p>Enter the email you paid with and we will send you a link to your printables.</p>
        <form data-restore style="display:grid;gap:10px;max-width:420px">
          <label class="sr" for="re-email">Email</label><input class="field" id="re-email" type="email" name="email" placeholder="Email you used at checkout" required>
          <button class="btn small" type="submit">Email me my link</button><div class="msg" role="status" aria-live="polite"></div>
        </form></div>
      ${catalogJson()}</div>`,
  }));
}

/* ---------- Simple text pages ---------- */
function textPages() {
  const page = (file, urlPath, title, description, html, active = '') => write(file, layout({ title: `${title} · ${config.name}`, description, urlPath, active, body: `<div class="narrow page-head prose"><h1>${title}</h1>${html}</div>` }));

  page('padres/index.html', '/padres/', 'How to read in Spanish with your child', 'A simple guide for parents: how to use short Spanish read-along books with children ages 2 to 6, even if you do not speak Spanish.', `
    <p class="sub">You do not need to be fluent. You need ten minutes, one book, and a child on your lap.</p>
    <h2>Why these books look the way they do</h2>
    <ul>
      <li><b>Real photographs.</b> Following the Montessori idea that young children learn best from the real world, most of our books use photos so a child links <span lang="es">«el oso»</span> to a real bear.</li>
      <li><b>One sentence per page.</b> A short, repeated pattern (<span lang="es">«El oso es grande. El oso es fuerte.»</span>) lets children predict the next word. Predicting is the first step of reading.</li>
      <li><b>Six key words.</b> Every book teaches six words, shows them in colour in the story, and brings them back at the end with pictures.</li>
      <li><b>Sound first.</b> Spanish is read almost exactly as it is written. Hearing each page read slowly helps children connect letters to sounds.</li>
    </ul>
    <h2>A ten-minute routine</h2>
    <ol>
      <li><b>Picture walk (2 minutes).</b> Turn the pages without reading. Ask <span lang="es">«¿Qué ves?»</span> and accept answers in any language.</li>
      <li><b>Listen (3 minutes).</b> Play each page. Point under each word as it is spoken.</li>
      <li><b>Echo (3 minutes).</b> Read again. You say the sentence, your child repeats it. Tap the coloured words to hear them alone.</li>
      <li><b>Play (2 minutes).</b> On the <span lang="es">«Mis palabras»</span> page, say a word and let your child tap the right picture.</li>
    </ol>
    <div class="callout"><b>Read the same book for several days.</b> Children ask for the same story again because repetition feels good and builds memory. By day three, pause before the last word and let your child finish the sentence.</div>
    <h2>Reading levels</h2>
    <ul>
      <li><b>Nivel 1 · First words.</b> Two or three word sentences. For ages 2–3 and children new to Spanish.</li>
      <li><b>Nivel 2 · Short sentences.</b> Four word sentences with describing words. For ages 3–5.</li>
      <li><b>Nivel 3 · Longer sentences.</b> Five words and more, with places and actions. For ages 4–6 and early readers.</li>
    </ul>
    <h2>Away from the screen</h2>
    <p>Screens are a good way to hear the language. Paper is where children slow down, point, trace and remember. Our <a href="/packs/">printable packs</a> turn each book into a paper book with flashcards and a tracing page. You can try one free: <a href="/muestra/">print the sample book</a>.</p>
    <p><a class="btn" href="/libros/">Choose a book</a></p>`, '/padres/');

  page('privacidad/index.html', '/privacidad/', 'Privacy', `How ${config.name} handles your information.`, `
    <p><i>Last updated ${new Date().toISOString().slice(0, 10)}. Plain-language summary; please have this reviewed before you rely on it.</i></p>
    <h2>What we collect</h2>
    <ul>
      <li><b>Email sign-up:</b> if a parent or teacher joins the book club we store their email address and optional first name with our email provider (Resend) to send book emails. Every email has an unsubscribe link.</li>
      <li><b>Purchases:</b> payments are handled by Stripe. We never see or store card numbers. Stripe shares the buyer's email and what was bought so we can deliver the printable.</li>
      <li><b>Visits:</b> we use Google Analytics to count page views and which books are read. We do not use this to identify anyone.</li>
    </ul>
    <h2>Children</h2>
    <p>This site is for parents and teachers to use with children. Children do not need an account, and we do not knowingly collect personal information from children under 13. Reading a book does not require entering any information.</p>
    <h2>Your choices</h2>
    <p>To see, correct or delete your information, email <a href="mailto:${config.contactEmail}">${config.contactEmail}</a>.</p>`);

  page('terminos/index.html', '/terminos/', 'Terms', `Terms for using ${config.name}.`, `
    <p><i>Last updated ${new Date().toISOString().slice(0, 10)}. Plain-language summary; please have this reviewed before you rely on it.</i></p>
    <h2>Free books</h2><p>You may read the online books for free at home or in class. Please link to them rather than copying them to other websites.</p>
    <h2>Printable packs</h2><p>A printable pack is a digital product. One purchase lets one family or one classroom print it as many times as they need. Please do not resell it or share the files publicly. Schools that need several classrooms can email us for a licence.</p>
    <h2>Refunds</h2><p>If a pack is not what you expected, email <a href="mailto:${config.contactEmail}">${config.contactEmail}</a> within 14 days and we will refund you.</p>
    <h2>Who we are</h2><p>${esc(config.name)} is published by ${esc(config.school)}, Phoenix, Arizona.</p>`);

  write('404.html', layout({ title: `Page not found · ${config.name}`, description: 'Page not found.', urlPath: '/404', noindex: true, body: `<div class="narrow page-head center"><h1>¡Ay! Page not found</h1><p class="sub">That page ran away like <span lang="es">el conejo</span>.</p><p><a class="btn" href="/libros/">Go to the books</a></p></div>` }));
}

/* ---------- Run ---------- */
fs.rmSync(DIST, { recursive: true, force: true });
fs.mkdirSync(path.join(DIST, 'assets'), { recursive: true });
for (const f of ['styles.css', 'site.js', 'reader.js']) fs.copyFileSync(path.join(__dirname, 'src', f), path.join(DIST, 'assets', f));

const files = copyMedia();
home();
libraryPage();
themePages();
books.forEach(bookPage);
packsPage();
purchasePages();
textPages();

// The free sample printable (static, no purchase needed).
const sample = books.find((b) => b.slug === config.freeSampleBook) || books[0];
write('muestra/index.html', renderPrintable({ title: `${sample.title} · free printable book`, books: [sample], backUrl: '/packs/' }));

write('robots.txt', `User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /gracias/\nDisallow: /mis-compras/\n${SITE_URL ? `Sitemap: ${SITE_URL}/sitemap.xml\n` : ''}`);
if (SITE_URL) {
  write('sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${sitemap.map((u) => `<url><loc>${SITE_URL}${u}</loc></url>`).join('\n')}\n</urlset>\n`);
}

console.log(`Built ${books.length} book pages, ${packs.length} packs, ${files} media files → site/dist`);
if (!SITE_URL) console.log('Note: SITE_URL is not set, so canonical links and sitemap.xml were skipped.');
