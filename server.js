const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3002;

// Inject API key server-side so it's not in the repo
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || '';

// Serve config.js dynamically (keeps key out of repo)
app.get('/config.js', (req, res) => {
  res.type('application/javascript');
  res.send(`const GEMINI_API_KEY = "${GEMINI_API_KEY}";`);
});

// Serve static files
app.use(express.static(path.join(__dirname)));

// Book index page
app.get('/', (req, res) => {
  res.send(`<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Beibei Amigos - Spanish Books</title>
  <link href="https://fonts.googleapis.com/css2?family=Sour+Gummy:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Sour Gummy', cursive; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 40px 20px; }
    .container { max-width: 900px; margin: 0 auto; }
    .header { text-align: center; color: white; margin-bottom: 40px; }
    .header img { width: 80px; height: 80px; border-radius: 50%; background: white; padding: 8px; margin-bottom: 16px; }
    .header h1 { font-size: 2.5rem; margin-bottom: 8px; }
    .header p { font-size: 1.1rem; opacity: 0.9; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 24px; }
    .card { background: white; border-radius: 20px; padding: 32px 24px; text-align: center; text-decoration: none; color: #333;
      box-shadow: 0 10px 30px rgba(0,0,0,0.15); transition: transform 0.2s, box-shadow 0.2s; }
    .card:hover { transform: translateY(-6px); box-shadow: 0 16px 40px rgba(0,0,0,0.2); }
    .card .emoji { font-size: 3rem; margin-bottom: 12px; }
    .card .week { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; color: #999; margin-bottom: 8px; }
    .card .title { font-size: 1.4rem; font-weight: 800; margin-bottom: 4px; }
    .card .subtitle { font-size: 0.85rem; color: #777; }
    .coming-soon { opacity: 0.5; pointer-events: none; }
    .coming-soon .title::after { content: ' 🔒'; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="https://www.beibeiamigos.com/wp-content/uploads/2025/12/ChatGPT-Image-Aug-18-2025-05_26_03-PM.png" alt="Beibei Amigos">
      <h1>📚 Mis Libros en Español</h1>
      <p>Beibei Amigos Language Preschool • Lectura Temprana</p>
    </div>
    <div class="grid">
      <a href="/books/week-00-frutas-y-verduras/" class="card">
        <div class="emoji">🍎</div>
        <div class="week">Semana 0</div>
        <div class="title">Mis Frutas y Verduras</div>
        <div class="subtitle">Fruits & Vegetables</div>
      </a>
      <a href="/books/week-01-el-oso/" class="card">
        <div class="emoji">🐻</div>
        <div class="week">Semana 1</div>
        <div class="title">El Oso</div>
        <div class="subtitle">The Bear</div>
      </a>
      <a href="#" class="card coming-soon">
        <div class="emoji">🐶</div>
        <div class="week">Semana 2</div>
        <div class="title">El Perro</div>
        <div class="subtitle">The Dog</div>
      </a>
      <a href="#" class="card coming-soon">
        <div class="emoji">🐱</div>
        <div class="week">Semana 3</div>
        <div class="title">El Gato</div>
        <div class="subtitle">The Cat</div>
      </a>
      <a href="#" class="card coming-soon">
        <div class="emoji">🐦</div>
        <div class="week">Semana 4</div>
        <div class="title">El Pájaro</div>
        <div class="subtitle">The Bird</div>
      </a>
      <a href="#" class="card coming-soon">
        <div class="emoji">🐟</div>
        <div class="week">Semana 5</div>
        <div class="title">El Pez</div>
        <div class="subtitle">The Fish</div>
      </a>
    </div>
  </div>
</body>
</html>`);
});

app.listen(PORT, () => console.log(`📚 Books server running on port ${PORT}`));
