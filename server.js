const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3002;

// Inject API keys server-side so they're not in the repo
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || '';

// Serve config.js dynamically from any path depth (keeps key out of repo)
app.get('*/config.js', (req, res) => {
  res.type('application/javascript');
  res.send(`const GEMINI_API_KEY = "${GEMINI_API_KEY}";`);
});
app.get('/config.js', (req, res) => {
  res.type('application/javascript');
  res.send(`const GEMINI_API_KEY = "${GEMINI_API_KEY}";`);
});

// Serve static files
app.use(express.static(path.join(__dirname)));

// Book data with themes
const BOOKS = [
  { slug: 'week-00-frutas-y-verduras', emoji: '🍎', week: 0, title: 'Mis Frutas y Verduras', subtitle: 'Fruits & Vegetables', theme: 'comida', ready: true },
  { slug: 'week-01-el-oso', emoji: '🐻', week: 1, title: 'El Oso', subtitle: 'The Bear', theme: 'animales', ready: true },
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
    const cls = b.ready ? 'card' : 'card coming-soon';
    const href = b.ready ? '/books/' + b.slug + '/' : '#';
    return '<a href="' + href + '" class="' + cls + '" data-theme="' + b.theme + '">' +
      '<div class="emoji">' + b.emoji + '</div>' +
      '<div class="week">Semana ' + b.week + '</div>' +
      '<div class="title">' + b.title + '</div>' +
      '<div class="subtitle">' + b.subtitle + '</div>' +
      '</a>';
  }).join('\n      ');

  const themeBtns = THEMES.map(t =>
    '<button class="theme-btn' + (t.id === 'animales' ? ' active' : '') + '" data-filter="' + t.id + '">' +
    '<span class="theme-emoji">' + t.emoji + '</span>' +
    '<span class="theme-label">' + t.labelEn + '</span>' +
    '</button>'
  ).join('\n        ');

  const bookCount = BOOKS.filter(b => b.ready).length;

  res.send(`<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Free Spanish Books for Preschoolers | Beibei Amigos - Learn Spanish Reading</title>
  <meta name="description" content="Free interactive Spanish reading books for preschoolers ages 2-5. Audio pronunciation, word highlighting, and beautiful photos. New books every week! By Beibei Amigos Language Preschool.">
  <meta name="keywords" content="free Spanish books kids, learn Spanish preschool, bilingual children books, Spanish reading preschoolers, interactive Spanish books, Beibei Amigos, Spanish vocabulary kids, bilingual education Phoenix">
  <meta property="og:title" content="Free Spanish Books for Preschoolers | Beibei Amigos">
  <meta property="og:description" content="Free interactive Spanish books with audio! Your child learns to read Spanish through play. New books every week.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://spanish-books.onrender.com/">
  <meta property="og:image" content="https://www.beibeiamigos.com/wp-content/uploads/2025/12/ChatGPT-Image-Aug-18-2025-05_26_03-PM.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="https://spanish-books.onrender.com/">
  <link href="https://fonts.googleapis.com/css2?family=Sour+Gummy:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Sour Gummy', cursive; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 40px 20px; }
    .container { max-width: 1000px; margin: 0 auto; }
    .header { text-align: center; color: white; margin-bottom: 32px; }
    .header img { width: 80px; height: 80px; border-radius: 50%; background: white; padding: 8px; margin-bottom: 16px; }
    .header h1 { font-size: 2.5rem; margin-bottom: 8px; }
    .header p { font-size: 1.1rem; opacity: 0.9; }
    .header .count { font-size: 0.85rem; opacity: 0.7; margin-top: 4px; }

    /* Theme filter */
    .themes { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin-bottom: 32px; padding: 0 10px; }
    .theme-btn { background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.3); color: white; padding: 10px 20px; border-radius: 50px; cursor: pointer; font-family: inherit; font-size: 1.1rem; font-weight: 700; display: flex; align-items: center; gap: 8px; transition: all 0.2s; }
    .theme-btn:hover { background: rgba(255,255,255,0.25); transform: translateY(-2px); }
    .theme-btn.active { background: white; color: #5b4a9e; border-color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .theme-emoji { font-size: 1.1rem; }
    @media (max-width: 600px) { .theme-btn { padding: 8px 14px; font-size: 0.9rem; } .theme-emoji { font-size: 1.2rem; } }

    /* Book grid */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }
    .card { background: white; border-radius: 20px; padding: 28px 20px; text-align: center; text-decoration: none; color: #333;
      box-shadow: 0 10px 30px rgba(0,0,0,0.15); transition: transform 0.2s, box-shadow 0.2s, opacity 0.3s; }
    .card:hover { transform: translateY(-6px); box-shadow: 0 16px 40px rgba(0,0,0,0.2); }
    .card .emoji { font-size: 3rem; margin-bottom: 10px; }
    .card .week { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 2px; color: #999; margin-bottom: 6px; }
    .card .title { font-size: 1.3rem; font-weight: 800; margin-bottom: 4px; }
    .card .subtitle { font-size: 0.8rem; color: #777; }
    .card .theme-tag { font-size: 0.65rem; color: #5b4a9e; background: #ede9fe; padding: 2px 10px; border-radius: 20px; display: inline-block; margin-top: 8px; font-weight: 600; }
    .card.coming-soon { opacity: 0.5; pointer-events: none; }
    .card.coming-soon .title::after { content: ' 🔒'; }
    .card.hidden { display: none; }

    .no-books { text-align: center; color: rgba(255,255,255,0.7); padding: 60px 20px; font-size: 1.2rem; display: none; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="https://www.beibeiamigos.com/wp-content/uploads/2025/12/ChatGPT-Image-Aug-18-2025-05_26_03-PM.png" alt="Beibei Amigos">
      <h1>📚 Mis Libros en Español</h1>
      <p>Beibei Amigos Language Preschool • Lectura Temprana</p>
      <p class="count">${bookCount} libros disponibles • ¡Nuevos cada semana!</p>
    </div>

    <div class="themes">
      ${themeBtns}
    </div>

    <div class="grid" id="bookGrid">
      ${bookCards}
    </div>

    <div class="no-books" id="noBooks">🔍 No hay libros en este tema todavía.<br>¡Pronto habrá más!</div>

    <!-- Upsell Banner -->
    <div style="max-width:900px; margin:40px auto 0; background:white; border-radius:20px; padding:32px; box-shadow:0 10px 30px rgba(0,0,0,0.1); text-align:center;">
      <h2 style="font-size:2.2rem; margin-bottom:12px; color:#333;">👩‍🏫 Meet Sofia — Your Child's AI Spanish Teacher!</h2>
      <p style="color:#666; margin-bottom:24px; font-size:1.2rem;">Sofia talks, listens, and plays with your child in real-time — making Spanish fun and natural!</p>
      <a href="https://tutti-sophia.onrender.com/sofia-fullscreen.html" target="_blank" style="display:inline-block; background:linear-gradient(135deg,#667eea,#764ba2); color:white; padding:16px 40px; border-radius:12px; font-weight:800; font-size:1.2rem; text-decoration:none; box-shadow:0 4px 15px rgba(102,126,234,0.4);">Try Sofia Free →</a>
    </div>

    <!-- School CTA -->
    <div style="max-width:900px; margin:24px auto; text-align:center; padding:20px;">
      <p style="color:rgba(255,255,255,0.8); font-size:0.85rem;">Made with ❤️ by <a href="https://www.beibeiamigos.com" target="_blank" style="color:white; font-weight:700;">Beibei Amigos Language Preschool</a> — Spanish Immersion · Mandarin Preschool · Bilingual Books — Phoenix, AZ</p>
      <p style="color:rgba(255,255,255,0.6); font-size:0.75rem; margin-top:8px;">🏫 Now Enrolling for 2026! Spanish Immersion • Mandarin • English | Ages 2-6</p>
    </div>
  </div>

  <script>
    function filterBooks(filter) {
      const cards = document.querySelectorAll('#bookGrid .card');
      let visible = 0;
      cards.forEach(card => {
        if (filter === 'todos' || card.dataset.theme === filter) {
          card.classList.remove('hidden');
          visible++;
        } else {
          card.classList.add('hidden');
        }
      });
      document.getElementById('noBooks').style.display = visible === 0 ? 'block' : 'none';
    }
    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.theme-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        filterBooks(btn.dataset.filter);
      });
    });
    // Default filter on load
    filterBooks('animales');
  </script>
</body>
</html>`);
});

app.listen(PORT, () => console.log(`📚 Books server running on port ${PORT}`));
