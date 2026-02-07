const fs = require('fs');
const path = require('path');

const OPENAI_KEY = process.env.OPENAI_API_KEY || '';

async function generateImages(bookDir) {
  // Read index.html and extract BOOK_CONFIG
  const html = fs.readFileSync(path.join(bookDir, 'index.html'), 'utf8');
  const configMatch = html.match(/const BOOK_CONFIG = ({[\s\S]*?});/);
  if (!configMatch) { console.error('No BOOK_CONFIG found'); return; }
  
  // Extract prompts using regex
  const promptMatches = [...html.matchAll(/prompt:\s*"([^"]+)"/g)];
  const titleMatches = [...html.matchAll(/title:\s*"([^"]+)"/g)];
  
  const imgDir = path.join(bookDir, 'images');
  if (!fs.existsSync(imgDir)) fs.mkdirSync(imgDir, { recursive: true });

  console.log(`Generating ${promptMatches.length} images...`);

  const delay = ms => new Promise(r => setTimeout(r, ms));
  for (let i = 0; i < promptMatches.length; i++) {
    const match = promptMatches[i];
    if (i > 0) await delay(5000); // 5s between requests for free tier
    const prompt = match[1];
    const filename = `page-${String(i).padStart(2, '0')}.png`;
    const filepath = path.join(imgDir, filename);
    
    if (fs.existsSync(filepath)) {
      console.log(`  ✅ ${filename} (cached)`);
      return;
    }

    try {
      const res = await fetch('https://api.openai.com/v1/images/generations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${OPENAI_KEY}` },
        body: JSON.stringify({ model: 'dall-e-3', prompt, n: 1, size: '1024x1024', response_format: 'b64_json' })
      });
      const data = await res.json();
      if (data.data?.[0]?.b64_json) {
        const buffer = Buffer.from(data.data[0].b64_json, 'base64');
        fs.writeFileSync(filepath, buffer);
        console.log(`  ✅ ${filename} (${(buffer.length / 1024).toFixed(0)}KB)`);
      } else {
        console.error(`  ❌ ${filename}: No image in response`, JSON.stringify(data).slice(0, 200));
      }
    } catch (e) {
      console.error(`  ❌ ${filename}: ${e.message}`);
    }
  }
  console.log('Done!');
}

// Run on specified book or all books
const target = process.argv[2];
if (target) {
  generateImages(path.resolve(target));
} else {
  const booksDir = path.join(__dirname, '..', 'books');
  const books = fs.readdirSync(booksDir).filter(f => fs.statSync(path.join(booksDir, f)).isDirectory());
  (async () => {
    for (const book of books) {
      console.log(`\n📖 ${book}`);
      await generateImages(path.join(booksDir, book));
    }
  })();
}
