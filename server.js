const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3002;

// Books use pre-generated static images/audio; the client no longer needs a
// Gemini key. Serving the real key here exposed it to every visitor
// (config.js is fetchable by anyone). Set ALLOW_CLIENT_GEMINI=1 only as a
// temporary escape hatch if live API fallback is ever needed again.
const CLIENT_GEMINI_KEY = process.env.ALLOW_CLIENT_GEMINI === '1'
  ? (process.env.GEMINI_API_KEY || '')
  : '';

app.get(['/config.js', '*/config.js'], (req, res) => {
  res.type('application/javascript');
  res.send(`const GEMINI_API_KEY = "${CLIENT_GEMINI_KEY}";`);
});

// Book data with themes
const BOOKS = [
  { slug: 'week-00-frutas-y-verduras', emoji: '🍎', week: 0, title: 'Mis Frutas y Verduras', subtitle: 'Fruits & Vegetables', theme: 'comida', ready: true },
  { slug: 'week-01-el-oso', emoji: '🐻', week: 1, title: 'El Oso', subtitle: 'The Bear', theme: 'animales', ready: true },
  { slug: 'week-02-el-gato', emoji: '🐱', week: 2, title: 'El Gato', subtitle: 'The Cat', theme: 'animales', ready: true },
  { slug: 'week-03-el-perro', emoji: '🐶', week: 3, title: 'El Perro', subtitle: 'The Dog', theme: 'animales', ready: true },
  { slug: 'week-04-el-conejo', emoji: '🐰', week: 4, title: 'El Conejo', subtitle: 'The Rabbit', theme: 'animales', ready: true },
  { slug: 'week-05-el-caballo', emoji: '🐴', week: 5, title: 'El Caballo', subtitle: 'The Horse', theme: 'animales', ready: true },
  { slug: 'week-06-la-vaca', emoji: '🐄', week: 6, title: 'La Vaca', subtitle: 'The Cow', theme: 'animales', ready: true },
  { slug: 'week-07-el-pato', emoji: '🦆', week: 7, title: 'El Pato', subtitle: 'The Duck', theme: 'animales', ready: true },
  { slug: 'week-08-la-oveja', emoji: '🐑', week: 8, title: 'La Oveja', subtitle: 'The Sheep', theme: 'animales', ready: true },
  { slug: 'week-09-el-desayuno', emoji: '🥞', week: 9, title: 'El Desayuno', subtitle: 'Breakfast', theme: 'comida', ready: true },
  { slug: 'week-10-el-almuerzo', emoji: '🥪', week: 10, title: 'El Almuerzo', subtitle: 'Lunch', theme: 'comida', ready: true },
  { slug: 'week-11-la-cena', emoji: '🍝', week: 11, title: 'La Cena', subtitle: 'Dinner', theme: 'comida', ready: true },
  { slug: 'week-12-las-bebidas', emoji: '🥤', week: 12, title: 'Las Bebidas', subtitle: 'Drinks', theme: 'comida', ready: true },
  { slug: 'week-13-los-postres', emoji: '🍰', week: 13, title: 'Los Postres', subtitle: 'Desserts', theme: 'comida', ready: true },
  { slug: 'week-14-en-la-cocina', emoji: '👨‍🍳', week: 14, title: 'En la Cocina', subtitle: 'In the Kitchen', theme: 'comida', ready: true },
  { slug: 'week-15-la-merienda', emoji: '🍿', week: 15, title: 'La Merienda', subtitle: 'Snack Time', theme: 'comida', ready: true },
  { slug: 'week-16-la-mariposa', emoji: '🦋', week: 16, title: 'La Mariposa', subtitle: 'The Butterfly', theme: 'mariposas', ready: true },
  { slug: 'week-17-la-abeja', emoji: '🐝', week: 17, title: 'La Abeja', subtitle: 'The Bee', theme: 'mariposas', ready: true },
  { slug: 'week-18-la-catarina', emoji: '🐞', week: 18, title: 'La Catarina', subtitle: 'The Ladybug', theme: 'mariposas', ready: true },
  { slug: 'week-19-la-hormiga', emoji: '🐜', week: 19, title: 'La Hormiga', subtitle: 'The Ant', theme: 'mariposas', ready: true },
  { slug: 'week-20-el-grillo', emoji: '🦗', week: 20, title: 'El Grillo', subtitle: 'The Cricket', theme: 'mariposas', ready: true },
  { slug: 'week-21-la-libelula', emoji: '🪰', week: 21, title: 'La Libélula', subtitle: 'The Dragonfly', theme: 'mariposas', ready: true },
  { slug: 'week-22-la-oruga', emoji: '🐛', week: 22, title: 'La Oruga', subtitle: 'The Caterpillar', theme: 'mariposas', ready: true },
  { slug: 'week-23-el-escarabajo', emoji: '🪲', week: 23, title: 'El Escarabajo', subtitle: 'The Beetle', theme: 'mariposas', ready: true },
  { slug: 'week-24-el-pulpo', emoji: '🐙', week: 24, title: 'El Pulpo', subtitle: 'The Octopus', theme: 'oceano', ready: true },
  { slug: 'week-25-la-tortuga-marina', emoji: '🐢', week: 25, title: 'La Tortuga Marina', subtitle: 'The Sea Turtle', theme: 'oceano', ready: true },
  { slug: 'week-26-el-delfin', emoji: '🐬', week: 26, title: 'El Delfín', subtitle: 'The Dolphin', theme: 'oceano', ready: true },
  { slug: 'week-27-el-pez-payaso', emoji: '🐠', week: 27, title: 'El Pez Payaso', subtitle: 'The Clownfish', theme: 'oceano', ready: true },
  { slug: 'week-28-la-ballena', emoji: '🐋', week: 28, title: 'La Ballena', subtitle: 'The Whale', theme: 'oceano', ready: true },
  { slug: 'week-29-el-caballito-de-mar', emoji: '🦑', week: 29, title: 'El Caballito de Mar', subtitle: 'The Seahorse', theme: 'oceano', ready: true },
  { slug: 'week-30-la-estrella-de-mar', emoji: '⭐', week: 30, title: 'La Estrella de Mar', subtitle: 'The Starfish', theme: 'oceano', ready: true },
  { slug: 'week-39-la-medusa', emoji: '🪼', week: 39, title: 'La Medusa', subtitle: 'The Jellyfish', theme: 'oceano', ready: true },
  { slug: 'week-40-la-manzana', emoji: '🍎', week: 40, title: 'La Manzana', subtitle: 'The Apple', theme: 'nutricion', ready: true },
  { slug: 'week-41-el-platano', emoji: '🍌', week: 41, title: 'El Plátano', subtitle: 'The Banana', theme: 'nutricion', ready: true },
  { slug: 'week-42-la-zanahoria', emoji: '🥕', week: 42, title: 'La Zanahoria', subtitle: 'The Carrot', theme: 'nutricion', ready: true },
  { slug: 'week-43-el-brocoli', emoji: '🥦', week: 43, title: 'El Brócoli', subtitle: 'The Broccoli', theme: 'nutricion', ready: true },
  { slug: 'week-44-el-huevo', emoji: '🥚', week: 44, title: 'El Huevo', subtitle: 'The Egg', theme: 'nutricion', ready: true },
  { slug: 'week-45-la-leche', emoji: '🥛', week: 45, title: 'La Leche', subtitle: 'The Milk', theme: 'nutricion', ready: true },
  { slug: 'week-46-el-pan', emoji: '🍞', week: 46, title: 'El Pan', subtitle: 'The Bread', theme: 'nutricion', ready: true },
  { slug: 'week-47-el-yogur', emoji: '🥣', week: 47, title: 'El Yogur', subtitle: 'The Yogurt', theme: 'nutricion', ready: true },
  { slug: 'week-48-la-gota', emoji: '💧', week: 48, title: 'La Gota', subtitle: 'The Drop', theme: 'agua', ready: true },
  { slug: 'week-49-el-rio', emoji: '🏞️', week: 49, title: 'El Río', subtitle: 'The River', theme: 'agua', ready: true },
  { slug: 'week-50-el-lago', emoji: '🏔️', week: 50, title: 'El Lago', subtitle: 'The Lake', theme: 'agua', ready: true },
  { slug: 'week-51-la-lluvia', emoji: '🌧️', week: 51, title: 'La Lluvia', subtitle: 'The Rain', theme: 'agua', ready: true },
  { slug: 'week-52-el-hielo', emoji: '🧊', week: 52, title: 'El Hielo', subtitle: 'The Ice', theme: 'agua', ready: true },
  { slug: 'week-53-la-nieve', emoji: '❄️', week: 53, title: 'La Nieve', subtitle: 'The Snow', theme: 'agua', ready: true },
  { slug: 'week-54-el-vapor', emoji: '💨', week: 54, title: 'El Vapor', subtitle: 'The Steam', theme: 'agua', ready: true },
  { slug: 'week-55-el-oceano-agua', emoji: '🌊', week: 55, title: 'El Océano', subtitle: 'The Ocean', theme: 'agua', ready: true },
  { slug: 'week-31-la-rosa', emoji: '🌹', week: 31, title: 'La Rosa', subtitle: 'The Rose', theme: 'plantas', ready: true },
  { slug: 'week-32-el-girasol', emoji: '🌻', week: 32, title: 'El Girasol', subtitle: 'The Sunflower', theme: 'plantas', ready: true },
  { slug: 'week-33-el-arbol', emoji: '🌳', week: 33, title: 'El Árbol', subtitle: 'The Tree', theme: 'plantas', ready: true },
  { slug: 'week-34-el-cactus', emoji: '🌵', week: 34, title: 'El Cactus', subtitle: 'The Cactus', theme: 'plantas', ready: true },
  { slug: 'week-35-la-semilla', emoji: '🌱', week: 35, title: 'La Semilla', subtitle: 'The Seed', theme: 'plantas', ready: true },
  { slug: 'week-36-la-margarita', emoji: '🌼', week: 36, title: 'La Margarita', subtitle: 'The Daisy', theme: 'plantas', ready: true },
  { slug: 'week-37-el-tulipan', emoji: '🌷', week: 37, title: 'El Tulipán', subtitle: 'The Tulip', theme: 'plantas', ready: true },
  { slug: 'week-38-el-hongo', emoji: '🍄', week: 38, title: 'El Hongo', subtitle: 'The Mushroom', theme: 'plantas', ready: true },
  { slug: 'week-56-el-rojo', emoji: '🔴', week: 56, title: 'El Rojo', subtitle: 'The Color Red', theme: 'colores', ready: true },
  { slug: 'week-57-el-azul', emoji: '🔵', week: 57, title: 'El Azul', subtitle: 'The Color Blue', theme: 'colores', ready: true },
  { slug: 'week-58-el-amarillo', emoji: '🟡', week: 58, title: 'El Amarillo', subtitle: 'The Color Yellow', theme: 'colores', ready: true },
  { slug: 'week-59-el-verde', emoji: '🟢', week: 59, title: 'El Verde', subtitle: 'The Color Green', theme: 'colores', ready: true },
  { slug: 'week-60-el-circulo', emoji: '⭕', week: 60, title: 'El Círculo', subtitle: 'The Circle', theme: 'colores', ready: true },
  { slug: 'week-61-el-cuadrado', emoji: '🟦', week: 61, title: 'El Cuadrado', subtitle: 'The Square', theme: 'colores', ready: true },
  { slug: 'week-62-el-triangulo', emoji: '🔺', week: 62, title: 'El Triángulo', subtitle: 'The Triangle', theme: 'colores', ready: true },
  { slug: 'week-63-el-arcoiris', emoji: '🌈', week: 63, title: 'El Arcoíris', subtitle: 'The Rainbow', theme: 'colores', ready: true },
  { slug: 'week-64-la-mama', emoji: '👩', week: 64, title: 'La Mamá', subtitle: 'Mom', theme: 'familia', ready: true },
  { slug: 'week-65-el-papa', emoji: '👨', week: 65, title: 'El Papá', subtitle: 'Dad', theme: 'familia', ready: true },
  { slug: 'week-66-la-hermana', emoji: '👧', week: 66, title: 'La Hermana', subtitle: 'Sister', theme: 'familia', ready: true },
  { slug: 'week-67-el-hermano', emoji: '👦', week: 67, title: 'El Hermano', subtitle: 'Brother', theme: 'familia', ready: true },
  { slug: 'week-68-la-abuela', emoji: '👵', week: 68, title: 'La Abuela', subtitle: 'Grandmother', theme: 'familia', ready: true },
  { slug: 'week-69-el-abuelo', emoji: '👴', week: 69, title: 'El Abuelo', subtitle: 'Grandfather', theme: 'familia', ready: true },
  { slug: 'week-70-el-bebe', emoji: '👶', week: 70, title: 'El Bebé', subtitle: 'The Baby', theme: 'familia', ready: true },
  { slug: 'week-71-la-familia', emoji: '👨‍👩‍👧‍👦', week: 71, title: 'La Familia', subtitle: 'The Family', theme: 'familia', ready: true },
  { slug: 'week-72-mi-amigo', emoji: '👫', week: 72, title: 'Mi Amigo', subtitle: 'My Friend', theme: 'amigos', ready: true },
  { slug: 'week-73-jugamos', emoji: '🎮', week: 73, title: 'Jugamos', subtitle: 'We Play', theme: 'amigos', ready: true },
  { slug: 'week-74-compartir', emoji: '🤝', week: 74, title: 'Compartir', subtitle: 'Sharing', theme: 'amigos', ready: true },
  { slug: 'week-75-ayudar', emoji: '🙏', week: 75, title: 'Ayudar', subtitle: 'Helping', theme: 'amigos', ready: true },
  { slug: 'week-76-escuchar', emoji: '👂', week: 76, title: 'Escuchar', subtitle: 'Listening', theme: 'amigos', ready: true },
  { slug: 'week-77-reir', emoji: '😄', week: 77, title: 'Reír', subtitle: 'Laughing', theme: 'amigos', ready: true },
  { slug: 'week-78-perdonar', emoji: '💕', week: 78, title: 'Perdonar', subtitle: 'Forgiving', theme: 'amigos', ready: true },
  { slug: 'week-79-juntos', emoji: '🤗', week: 79, title: 'Juntos', subtitle: 'Together', theme: 'amigos', ready: true },
  { slug: 'week-80-el-sol', emoji: '☀️', week: 80, title: 'El Sol', subtitle: 'The Sun', theme: 'naturaleza', ready: true },
  { slug: 'week-81-la-luna', emoji: '🌙', week: 81, title: 'La Luna', subtitle: 'The Moon', theme: 'naturaleza', ready: true },
  { slug: 'week-82-las-estrellas', emoji: '⭐', week: 82, title: 'Las Estrellas', subtitle: 'The Stars', theme: 'naturaleza', ready: true },
  { slug: 'week-83-la-montana', emoji: '🏔️', week: 83, title: 'La Montaña', subtitle: 'The Mountain', theme: 'naturaleza', ready: true },
  { slug: 'week-84-el-bosque', emoji: '🌲', week: 84, title: 'El Bosque', subtitle: 'The Forest', theme: 'naturaleza', ready: true },
  { slug: 'week-85-el-desierto', emoji: '🏜️', week: 85, title: 'El Desierto', subtitle: 'The Desert', theme: 'naturaleza', ready: true },
  { slug: 'week-86-la-cascada', emoji: '💧', week: 86, title: 'La Cascada', subtitle: 'The Waterfall', theme: 'naturaleza', ready: true },
  { slug: 'week-87-el-volcan', emoji: '🌋', week: 87, title: 'El Volcán', subtitle: 'The Volcano', theme: 'naturaleza', ready: true },
  { slug: 'week-112-las-manos', emoji: '🖐️', week: 112, title: 'Las Manos', subtitle: 'The Hands', theme: 'cuerpo', ready: true },
  { slug: 'week-113-los-pies', emoji: '🦶', week: 113, title: 'Los Pies', subtitle: 'The Feet', theme: 'cuerpo', ready: true },
  { slug: 'week-114-los-ojos', emoji: '👀', week: 114, title: 'Los Ojos', subtitle: 'The Eyes', theme: 'cuerpo', ready: true },
  { slug: 'week-115-la-boca', emoji: '👄', week: 115, title: 'La Boca', subtitle: 'The Mouth', theme: 'cuerpo', ready: true },
  { slug: 'week-116-la-nariz', emoji: '👃', week: 116, title: 'La Nariz', subtitle: 'The Nose', theme: 'cuerpo', ready: true },
  { slug: 'week-117-las-orejas', emoji: '👂', week: 117, title: 'Las Orejas', subtitle: 'The Ears', theme: 'cuerpo', ready: true },
  { slug: 'week-118-el-corazon', emoji: '❤️', week: 118, title: 'El Corazón', subtitle: 'The Heart', theme: 'cuerpo', ready: true },
  { slug: 'week-119-el-cuerpo', emoji: '🧍', week: 119, title: 'El Cuerpo', subtitle: 'The Body', theme: 'cuerpo', ready: true },
  { slug: 'week-88-el-uno', emoji: '1️⃣', week: 88, title: 'El Uno', subtitle: 'The Number One', theme: 'numeros', ready: true },
  { slug: 'week-89-el-dos', emoji: '2️⃣', week: 89, title: 'El Dos', subtitle: 'The Number Two', theme: 'numeros', ready: true },
  { slug: 'week-90-el-tres', emoji: '3️⃣', week: 90, title: 'El Tres', subtitle: 'The Number Three', theme: 'numeros', ready: true },
  { slug: 'week-91-el-cuatro', emoji: '4️⃣', week: 91, title: 'El Cuatro', subtitle: 'The Number Four', theme: 'numeros', ready: true },
  { slug: 'week-92-el-cinco', emoji: '5️⃣', week: 92, title: 'El Cinco', subtitle: 'The Number Five', theme: 'numeros', ready: true },
  { slug: 'week-93-las-letras', emoji: '🔤', week: 93, title: 'Las Letras', subtitle: 'The Letters', theme: 'numeros', ready: true },
  { slug: 'week-94-el-abecedario', emoji: '🅰️', week: 94, title: 'El Abecedario', subtitle: 'The Alphabet', theme: 'numeros', ready: true },
  { slug: 'week-95-contar', emoji: '🔢', week: 95, title: 'Contar', subtitle: 'Counting', theme: 'numeros', ready: true },
  { slug: 'week-96-la-guitarra', emoji: '🎸', week: 96, title: 'La Guitarra', subtitle: 'The Guitar', theme: 'musica', ready: true },
  { slug: 'week-97-el-tambor', emoji: '🥁', week: 97, title: 'El Tambor', subtitle: 'The Drum', theme: 'musica', ready: true },
];

const THEMES = [
  { id: 'animales', emoji: '🐻', label: 'Animales', labelEn: 'Animals' },
  { id: 'mariposas', emoji: '🦋', label: 'Mariposas e Insectos', labelEn: 'Butterflies & Bugs' },
  { id: 'oceano', emoji: '🐙', label: 'Criaturas del Océano', labelEn: 'Ocean Creatures' },
  { id: 'plantas', emoji: '🌸', label: 'Plantas y Flores', labelEn: 'Plants & Flowers' },
  { id: 'nutricion', emoji: '🥗', label: 'Nutrición', labelEn: 'Nutrition' },
  { id: 'comida', emoji: '🍎', label: 'Comida', labelEn: 'Food' },
  { id: 'agua', emoji: '💧', label: 'El Agua', labelEn: 'Water' },
  { id: 'colores', emoji: '🌈', label: 'Colores y Formas', labelEn: 'Colors & Shapes' },
  { id: 'familia', emoji: '👨‍👩‍👧', label: 'Mi Familia', labelEn: 'Family' },
  { id: 'amigos', emoji: '🤝', label: 'Mis Amigos', labelEn: 'Friends' },
  { id: 'naturaleza', emoji: '🌿', label: 'Naturaleza', labelEn: 'Nature' },
  { id: 'numeros', emoji: '🔢', label: 'Números y Letras', labelEn: 'Numbers & Letters' },
  { id: 'musica', emoji: '🎵', label: 'Música y Juegos', labelEn: 'Music & Games' },
  { id: 'mi-mundo', emoji: '🏠', label: 'Mi Mundo', labelEn: 'My World' },
  { id: 'cuerpo', emoji: '🫀', label: 'Mi Cuerpo', labelEn: 'My Body' },
  { id: 'transporte', emoji: '🚗', label: 'Transporte', labelEn: 'Transportation' },
  { id: 'estaciones', emoji: '☀️', label: 'Estaciones y Clima', labelEn: 'Seasons & Weather' },
  { id: 'todos', emoji: '📚', label: 'Todos', labelEn: 'All' },
];

// Book index page
app.get('/', (req, res) => {
  const bookCards = BOOKS.map(b => {
    const cls = b.ready
      ? 'card' + (b.theme === 'animales' ? '' : ' hidden')
      : 'card coming-soon hidden';
    const bookSlug = b.slug.replace(/^week-\d+-/, '');
    const href = b.ready ? 'https://www.beibeiamigos.com/spanish-books/' + bookSlug + '/' : '#';
    const cover = 'https://seanmichael67.github.io/Spanish-Books/books/' + b.slug + '/images/page-00.webp';
    return '<a href="' + href + '" target="_top" class="' + cls + '" data-theme="' + b.theme + '" data-search="' + b.title + ' ' + b.subtitle + '">' +
      '<img class="card-cover" src="' + cover + '" alt="Cover of ' + b.title + ' — ' + b.subtitle + '" loading="lazy" width="480" height="360">' +
      '<div class="card-body">' +
      '<div class="card-meta"><span>Semana ' + b.week + '</span><span aria-hidden="true">' + b.emoji + '</span></div>' +
      '<div class="title" lang="es">' + b.title + '</div>' +
      '<div class="subtitle">' + b.subtitle + '</div>' +
      '<div class="read-cue">Abrir libro <span aria-hidden="true">→</span></div>' +
      '</div>' +
      '</a>';
  }).join('\n      ');

  const populatedThemeIds = new Set(BOOKS.filter(b => b.ready).map(b => b.theme));
  const populatedThemes = THEMES.filter(t => t.id === 'todos' || populatedThemeIds.has(t.id));
  const themeBtns = populatedThemes.map(t =>
    '<button type="button" class="theme-btn' + (t.id === 'animales' ? ' active' : '') + '" data-filter="' + t.id + '" aria-pressed="' + (t.id === 'animales' ? 'true' : 'false') + '">' +
    '<span class="theme-emoji">' + t.emoji + '</span>' +
    '<span class="theme-label">' + t.labelEn + '</span>' +
    '</button>'
  ).join('\n        ');

  const bookCount = BOOKS.filter(b => b.ready).length;
  const themeCount = populatedThemeIds.size;

  res.send(`<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Free Spanish Books for Preschoolers | Beibei Amigos - Learn Spanish Reading</title>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-WP9V5R7T9N"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', 'G-WP9V5R7T9N', { content_group: 'spanish-books-library' });
  </script>
  <meta name="description" content="Free interactive Spanish reading books for preschoolers ages 2-5. Audio pronunciation, word highlighting, and beautiful photos. New books every week! By Beibei Amigos Language Preschool.">
  <meta name="keywords" content="free Spanish books kids, learn Spanish preschool, bilingual children books, Spanish reading preschoolers, interactive Spanish books, Beibei Amigos, Spanish vocabulary kids, bilingual education Phoenix">
  <meta property="og:title" content="Free Spanish Books for Preschoolers | Beibei Amigos">
  <meta property="og:description" content="Free interactive Spanish books with audio! Your child learns to read Spanish through play. New books every week.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.beibeiamigos.com/spanish-books/">
  <meta property="og:image" content="https://www.beibeiamigos.com/wp-content/uploads/2025/12/ChatGPT-Image-Aug-18-2025-05_26_03-PM.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="https://www.beibeiamigos.com/spanish-books/">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@500;600;700;800&family=Sour+Gummy:ital,wght@0,500..800;1,500..800&display=swap" rel="stylesheet">
  <style>
    :root {
      --ink: #28213a;
      --orchid: #6d4cc5;
      --orchid-dark: #52359f;
      --sky: #41b7c7;
      --mango: #ffbf47;
      --paper: #fffdf7;
      --mist: #f4f0ff;
      --line: #ded6f2;
      --shadow: 0 18px 40px rgba(40, 33, 58, 0.12);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { background: var(--paper); scroll-behavior: smooth; }
    body { font-family: 'Nunito', sans-serif; background: var(--paper); color: var(--ink); padding: 20px; margin: 0; }
    button, input { font: inherit; }
    .container { width: min(100%, 1440px); margin: 0 auto; }
    .hero { position: relative; overflow: hidden; display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(280px, 0.75fr); gap: 48px; align-items: center; min-height: 430px; padding: clamp(32px, 6vw, 76px); border: 2px solid var(--ink); border-radius: 34px; background: var(--ink); color: white; box-shadow: 10px 10px 0 var(--mango); }
    .hero::before { content: ''; position: absolute; inset: auto -10% -45% 35%; height: 360px; border-radius: 50%; background: var(--orchid); opacity: 0.46; transform: rotate(-8deg); }
    .hero-copy, .story-stack { position: relative; z-index: 1; }
    .brand-row { display: flex; align-items: center; gap: 12px; margin-bottom: 36px; color: #eee8ff; font-weight: 800; letter-spacing: 0.02em; }
    .brand-row img { width: 58px; height: 58px; border-radius: 50%; background: white; padding: 6px; }
    .eyebrow { display: inline-flex; align-items: center; gap: 8px; margin-bottom: 12px; color: var(--mango); font-size: 0.78rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; }
    .hero h1 { max-width: 780px; font-family: 'Sour Gummy', cursive; font-size: clamp(3rem, 7vw, 6.4rem); line-height: 0.88; letter-spacing: -0.045em; }
    .hero h1 em { color: var(--mango); font-style: normal; }
    .hero-intro { max-width: 640px; margin-top: 24px; color: #eee8ff; font-size: clamp(1rem, 2vw, 1.22rem); line-height: 1.6; }
    .hero-count { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }
    .hero-count span { padding: 9px 14px; border: 1px solid rgba(255,255,255,0.28); border-radius: 999px; background: rgba(255,255,255,0.09); font-size: 0.86rem; font-weight: 800; }
    .story-stack { min-height: 300px; }
    .story-stack img { position: absolute; width: min(240px, 70%); aspect-ratio: 4 / 3; object-fit: cover; border: 7px solid white; border-radius: 22px; box-shadow: 0 22px 45px rgba(0,0,0,0.28); }
    .story-stack img:nth-child(1) { top: 5%; left: 3%; transform: rotate(-10deg); }
    .story-stack img:nth-child(2) { top: 18%; right: 0; transform: rotate(9deg); }
    .story-stack img:nth-child(3) { bottom: 0; left: 22%; transform: rotate(-1deg); }
    .library-shell { margin-top: 54px; }
    .library-heading { display: flex; align-items: end; justify-content: space-between; gap: 30px; margin-bottom: 24px; }
    .library-heading h2 { font-family: 'Sour Gummy', cursive; font-size: clamp(2.2rem, 5vw, 4rem); line-height: 1; letter-spacing: -0.025em; }
    .library-heading p { max-width: 580px; margin-top: 8px; color: #655d74; line-height: 1.55; }
    .search { position: relative; display: block; width: min(100%, 380px); flex: 0 0 min(100%, 380px); }
    .search span { position: absolute; left: 17px; top: 50%; transform: translateY(-50%); font-size: 1.2rem; }
    .search input { width: 100%; height: 54px; padding: 0 18px 0 50px; border: 2px solid var(--ink); border-radius: 16px; background: white; color: var(--ink); outline: none; box-shadow: 5px 5px 0 var(--sky); }
    .search input:focus { box-shadow: 5px 5px 0 var(--mango); }
    .themes { display: flex; flex-wrap: wrap; gap: 9px; margin-bottom: 18px; }
    .theme-btn { min-height: 44px; padding: 8px 14px; border: 2px solid var(--line); border-radius: 999px; background: white; color: var(--ink); cursor: pointer; font-weight: 800; transition: transform 0.16s ease, background 0.16s ease, border-color 0.16s ease; }
    .theme-btn:hover { transform: translateY(-2px); border-color: var(--orchid); }
    .theme-btn.active { border-color: var(--ink); background: var(--ink); color: white; }
    .theme-emoji { margin-right: 5px; }
    .results-status { min-height: 24px; margin-bottom: 18px; color: #6d6677; font-size: 0.9rem; font-weight: 700; }
    .grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 22px; }
    .card { overflow: hidden; display: flex; flex-direction: column; min-width: 0; border: 2px solid var(--ink); border-radius: 22px; background: white; color: var(--ink); text-decoration: none; box-shadow: 7px 7px 0 var(--mist); transition: transform 0.18s ease, box-shadow 0.18s ease; }
    .card:hover { transform: translate(-2px, -4px); box-shadow: 10px 12px 0 var(--mango); }
    .card-cover { display: block; width: 100%; aspect-ratio: 4 / 3; object-fit: cover; background: var(--mist); border-bottom: 2px solid var(--ink); }
    .card-body { display: flex; flex: 1; flex-direction: column; padding: 18px; }
    .card-meta { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; color: var(--orchid-dark); font-size: 0.68rem; font-weight: 800; letter-spacing: 0.11em; text-transform: uppercase; }
    .card .title { font-family: 'Sour Gummy', cursive; font-size: 1.55rem; font-weight: 800; line-height: 1.05; }
    .card .subtitle { margin-top: 5px; color: #726a7e; font-size: 0.88rem; }
    .read-cue { margin-top: auto; padding-top: 18px; color: var(--orchid-dark); font-size: 0.82rem; font-weight: 800; }
    .card.coming-soon { opacity: 0.55; pointer-events: none; }
    .card.hidden { display: none; }
    .no-books { display: none; padding: 58px 24px; border: 2px dashed var(--line); border-radius: 22px; background: var(--mist); text-align: center; color: #625a70; font-size: 1.05rem; }
    .site-note { margin: 52px auto 8px; padding: 26px; border-top: 2px solid var(--line); text-align: center; color: #6d6677; line-height: 1.6; }
    .site-note a { color: var(--orchid-dark); font-weight: 800; }
    :focus-visible { outline: 4px solid var(--mango); outline-offset: 4px; }
    @media (max-width: 1050px) { .grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
    @media (max-width: 820px) {
      body { padding: 12px; }
      .hero { grid-template-columns: 1fr; gap: 28px; min-height: auto; padding: 34px 26px 44px; border-radius: 26px; box-shadow: 6px 6px 0 var(--mango); }
      .brand-row { margin-bottom: 26px; }
      .story-stack { min-height: 240px; }
      .library-heading { align-items: stretch; flex-direction: column; }
      .search { width: 100%; flex-basis: auto; }
      .themes { flex-wrap: nowrap; overflow-x: auto; padding: 4px 4px 12px; scroll-snap-type: x proximity; }
      .theme-btn { flex: 0 0 auto; scroll-snap-align: start; }
      .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
    }
    @media (max-width: 520px) {
      .hero h1 { font-size: clamp(2.8rem, 15vw, 4.2rem); }
      .story-stack { min-height: 205px; }
      .story-stack img { width: 62%; border-width: 5px; border-radius: 16px; }
      .library-shell { margin-top: 42px; }
      .grid { grid-template-columns: 1fr; }
      .card { display: grid; grid-template-columns: 42% 1fr; }
      .card-cover { height: 100%; aspect-ratio: auto; border-right: 2px solid var(--ink); border-bottom: 0; }
      .card-body { padding: 16px; }
      .card .title { font-size: 1.35rem; }
    }
    @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } *, *::before, *::after { transition: none !important; } }
  </style>
</head>
<body>
  <main class="container">
    <section class="hero" aria-labelledby="libraryTitle">
      <div class="hero-copy">
        <div class="brand-row">
          <img src="https://www.beibeiamigos.com/wp-content/uploads/2025/12/ChatGPT-Image-Aug-18-2025-05_26_03-PM.png" alt="Beibei Amigos Language Preschool">
          <span>Beibei Amigos · Lectura temprana</span>
        </div>
        <p class="eyebrow"><span aria-hidden="true">●</span> Free bilingual story library</p>
        <h1 id="libraryTitle">Pick a story.<br><em>Read together.</em></h1>
        <p class="hero-intro">Short Spanish books with English support, native audio, word highlighting and a little badge at the finish. Choose a topic your child already loves.</p>
        <div class="hero-count" aria-label="Library highlights">
          <span>${bookCount} free stories</span>
          <span>${themeCount} ready-to-read themes</span>
          <span>Audio on every page</span>
        </div>
      </div>
      <div class="story-stack" aria-hidden="true">
        <img src="https://seanmichael67.github.io/Spanish-Books/books/week-01-el-oso/images/page-00.webp" alt="">
        <img src="https://seanmichael67.github.io/Spanish-Books/books/week-16-la-mariposa/images/page-00.webp" alt="">
        <img src="https://seanmichael67.github.io/Spanish-Books/books/week-24-el-pulpo/images/page-00.webp" alt="">
      </div>
    </section>

    <section class="library-shell" aria-labelledby="browseTitle">
      <div class="library-heading">
        <div>
          <h2 id="browseTitle">Find tonight's book</h2>
          <p>Search in Spanish or English, or follow a topic trail. The Animals shelf is open first.</p>
        </div>
        <label class="search" for="bookSearch">
          <span aria-hidden="true">⌕</span>
          <input id="bookSearch" type="search" placeholder="Search oso, bear, familia…" autocomplete="off">
        </label>
      </div>

      <div class="themes" role="group" aria-label="Filter books by theme">
        ${themeBtns}
      </div>
      <p class="results-status" id="resultsStatus" aria-live="polite">8 books in Animals</p>

      <div class="grid" id="bookGrid">
        ${bookCards}
      </div>

      <div class="no-books" id="noBooks" role="status">
        <strong>No encontramos ese libro todavía.</strong><br>
        Try another word or choose a different theme.
      </div>
    </section>

    <footer class="site-note">
      Made with care by <a href="https://www.beibeiamigos.com" target="_top">Beibei Amigos Language Preschool</a><br>
      Spanish immersion · Mandarin · English · Phoenix, Arizona
    </footer>
  </main>

  <script>
    const cards = Array.from(document.querySelectorAll('#bookGrid .card'));
    const searchInput = document.getElementById('bookSearch');
    const status = document.getElementById('resultsStatus');
    const noBooks = document.getElementById('noBooks');
    let activeFilter = 'animales';

    function normalise(value) {
      return (value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
    }

    function filterBooks(filter) {
      activeFilter = filter || activeFilter;
      const query = normalise(searchInput.value);
      let visible = 0;
      cards.forEach(card => {
        const matchesTheme = activeFilter === 'todos' || card.dataset.theme === activeFilter;
        const matchesSearch = !query || normalise(card.dataset.search).includes(query);
        const show = matchesTheme && matchesSearch;
        card.classList.toggle('hidden', !show);
        card.setAttribute('aria-hidden', show ? 'false' : 'true');
        if (show) visible++;
      });
      const activeButton = document.querySelector('.theme-btn.active .theme-label');
      const themeName = activeButton ? activeButton.textContent : 'books';
      status.textContent = visible + (visible === 1 ? ' book' : ' books') + ' in ' + themeName + (query ? ' matching “' + searchInput.value.trim() + '”' : '');
      noBooks.style.display = visible === 0 ? 'block' : 'none';
      reportHeight();
    }

    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.theme-btn').forEach(other => {
          const selected = other === btn;
          other.classList.toggle('active', selected);
          other.setAttribute('aria-pressed', selected ? 'true' : 'false');
        });
        filterBooks(btn.dataset.filter);
      });
    });
    searchInput.addEventListener('input', () => filterBooks(activeFilter));
    filterBooks('animales');

    // GA4: which books get opened from the library
    document.addEventListener('click', function (e) {
      var card = e.target.closest && e.target.closest('a.card');
      if (card) { try { gtag('event', 'book_click', { book: (card.getAttribute('href') || '').split('/').filter(Boolean).pop() }); } catch (err) {} }
      var theme = e.target.closest && e.target.closest('.theme-btn');
      if (theme) { try { gtag('event', 'theme_filter', { theme: theme.dataset.filter }); } catch (err) {} }
    }, true);

    // Tell the WordPress parent iframe our height so it never needs a nested scrollbar.
    function reportHeight() {
      if (window.parent !== window) {
        window.parent.postMessage({ type: 'resize', height: document.body.scrollHeight + 40 }, '*');
      }
    }
    window.addEventListener('load', reportHeight);
    if ('ResizeObserver' in window) new ResizeObserver(reportHeight).observe(document.body);
  </script>
</body>
</html>`);
});

// Serve book assets after the explicit library route so `/` is generated
// from the catalog above instead of returning a stale checked-in index.html.
app.use(express.static(path.join(__dirname)));

app.listen(PORT, () => console.log(`📚 Books server running on port ${PORT}`));
