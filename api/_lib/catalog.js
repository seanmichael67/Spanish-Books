/*
 * The catalog: every book, theme and product the site knows about.
 * Used by the build script (to make the pages) AND by the /api functions
 * (to know what a customer bought). Prices come from site/site.config.json.
 */
const books = require('../../site/data/books.json');
const themes = require('../../site/data/themes.json');
const config = require('../../site/site.config.json');

const LIBRARY_ID = 'biblioteca';

const booksByTheme = (themeId) => books.filter((b) => b.theme === themeId);

// A theme becomes a printable pack once it has a full set of 8 books.
const packs = themes
  .filter((t) => booksByTheme(t.id).length >= 8)
  .map((t) => ({
    id: 'pack-' + t.id,
    kind: 'pack',
    theme: t.id,
    name: `${t.en} Printable Pack (${t.es})`,
    description: `${booksByTheme(t.id).length} printable Spanish books (${t.en}), with picture vocabulary, flashcards and word tracing.`,
    priceCents: config.packPriceCents,
    books: booksByTheme(t.id).map((b) => b.slug),
  }));

const library = {
  id: LIBRARY_ID,
  kind: 'library',
  name: 'Biblioteca Completa: every printable pack',
  description: `All ${packs.length} printable packs (${packs.reduce((n, p) => n + p.books.length, 0)} books) with vocabulary, flashcards and word tracing.`,
  priceCents: config.libraryPriceCents,
  books: packs.flatMap((p) => p.books),
};

// For preschools and language schools: every pack, for every classroom in one school.
const SCHOOL_ID = 'escuela';
const school = {
  id: SCHOOL_ID,
  kind: 'school',
  name: 'School Licence: every printable pack for one school',
  description: `All ${packs.length} printable packs for every classroom and teacher at one school.`,
  priceCents: config.schoolPriceCents,
  books: library.books,
};

const products = [...packs, library, school];
const getProduct = (id) => products.find((p) => p.id === id) || null;
const getBook = (slug) => books.find((b) => b.slug === slug) || null;
const getTheme = (id) => themes.find((t) => t.id === id) || null;

/** Does a list of purchased product ids unlock this product? */
const owns = (purchased, productId) => purchased.includes(LIBRARY_ID) || purchased.includes(SCHOOL_ID) || purchased.includes(productId);

module.exports = { books, themes, config, packs, library, school, products, SCHOOL_ID, getProduct, getBook, getTheme, booksByTheme, owns, LIBRARY_ID };
