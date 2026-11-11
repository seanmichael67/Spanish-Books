/* Small text helpers shared by the website builder and the printable packs. */
const esc = (s) => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const norm = (s) => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

/**
 * Give each vocabulary word the story picture that shows it, without using the
 * same picture twice. Words that match the fewest pages choose first, so
 * "bosque" gets the forest page and "oso" (which is on every page) takes what is left.
 * Returns { word: imageFile or null }.
 */
function vocabImages(book) {
  const pages = book.pages.slice(1).filter((p) => p.image);
  const matches = book.vocab.map((word) => {
    const w = norm(word.es);
    const stems = [w, w.length > 4 ? w.slice(0, -1) : null, w.length > 5 ? w.slice(0, -2) : null].filter(Boolean);
    const hits = pages.filter((p) => norm(p.es).split(/[^a-zñ]+/).some((t) => stems.some((s) => t.startsWith(s))));
    return { es: word.es, hits };
  });
  const used = new Set();
  const out = {};
  [...matches].sort((a, b) => a.hits.length - b.hits.length).forEach((m) => {
    const free = m.hits.find((p) => !used.has(p.image));
    out[m.es] = free ? free.image : null;
    if (free) used.add(free.image);
  });
  return out;
}

/** Wrap the book's vocabulary words inside a sentence so they can be shown in colour. */
function highlight(sentence, vocab, wrap) {
  const words = vocab.map((v) => v.es).sort((a, b) => b.length - a.length);
  if (!words.length) return esc(sentence);
  const L = 'A-Za-zÁÉÍÓÚÜÑáéíóúüñ';
  const pattern = new RegExp(`(^|[^${L}])(${words.map((w) => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})(?![${L}])`, 'gi');
  let out = '';
  let last = 0;
  let m;
  while ((m = pattern.exec(sentence))) {
    const start = m.index + m[1].length;
    out += esc(sentence.slice(last, start));
    const v = vocab.find((x) => x.es.toLowerCase() === m[2].toLowerCase());
    out += wrap(esc(m[2]), v);
    last = start + m[2].length;
  }
  return out + esc(sentence.slice(last));
}

module.exports = { esc, norm, vocabImages, highlight };
