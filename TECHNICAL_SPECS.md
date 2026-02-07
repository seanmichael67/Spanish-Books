# Technical Specifications - WordPress/Divi Embedding

## Overview

Interactive Spanish books embedded in WordPress Divi modules with optimal performance and SEO.

---

## WordPress/Divi Integration

### Embedding Method

**Option 1: iFrame Embed (Recommended)**
```html
<!-- Divi Code Module -->
<div class="beibei-book-container">
  <iframe 
    src="/books/week-1-colors/index.html"
    width="100%"
    height="600px"
    frameborder="0"
    loading="lazy"
    title="Los Colores - Spanish Colors Book"
    allow="autoplay"
  ></iframe>
</div>

<style>
.beibei-book-container {
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  border-radius: 8px;
  overflow: hidden;
}
.beibei-book-container iframe {
  display: block;
}
</style>
```

**Option 2: Direct HTML Embed**
```html
<!-- All CSS/JS inline for standalone operation -->
<div id="book-app-week-1"></div>
<script>
  // Inline React or vanilla JS
  // Full book code here
</script>
```

---

## Performance Optimization

### Image Loading
```javascript
// Lazy loading with Intersection Observer
const images = document.querySelectorAll('img[data-src]');
const imageObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
      imageObserver.unobserve(img);
    }
  });
});

images.forEach(img => imageObserver.observe(img));
```

### Image Format & Size
- **Format:** WebP (with JPG fallback for Safari <14)
- **Dimensions:** Max 800px width, auto height
- **Compression:** 80% quality
- **File size:** <100KB per image
- **Total book:** <1.5MB including all assets

### Code Minification
```bash
# Minify JavaScript
npx terser book.js -o book.min.js -c -m

# Minify CSS
npx cssnano book.css book.min.css

# Inline critical CSS, defer non-critical
```

### Font Loading
```html
<!-- System font stack (no external fonts) -->
<style>
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
               "Helvetica Neue", Arial, sans-serif;
}
</style>

<!-- OR: Google Fonts with preconnect -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&display=swap" rel="stylesheet">
```

---

## Code Structure

### Standalone HTML Template
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- SEO Meta Tags -->
  <title>Los Colores - Free Spanish Book for Preschool | Beibei Amigos</title>
  <meta name="description" content="Free interactive Spanish book teaching colors to preschoolers ages 2-5. AI-powered audio helps kids learn: rojo, azul, amarillo, verde, and more!">
  <meta name="keywords" content="spanish preschool books, learn colors spanish, free spanish books, montessori language, phoenix preschool">
  
  <!-- Schema.org Markup -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Book",
    "name": "Los Colores",
    "description": "Interactive Spanish vocabulary book for preschoolers",
    "inLanguage": "es",
    "educationalLevel": "Preschool",
    "audience": {
      "@type": "EducationalAudience",
      "educationalRole": "student",
      "audienceType": "children ages 2-5"
    },
    "author": {
      "@type": "Organization",
      "name": "Beibei Amigos Language Preschool",
      "url": "https://beibeiamigos.com"
    }
  }
  </script>
  
  <!-- Inline CSS (critical) -->
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #f5f5f5;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }
    .book-container {
      background: white;
      border-radius: 12px;
      box-shadow: 0 8px 16px rgba(0,0,0,0.1);
      max-width: 600px;
      width: 100%;
      overflow: hidden;
    }
    .book-page {
      padding: 40px;
      text-align: center;
      min-height: 500px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .book-page img {
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      margin: 20px 0;
    }
    .vocabulary {
      font-size: 2.5rem;
      font-weight: bold;
      color: #333;
      margin: 20px 0;
    }
    .sentence {
      font-size: 1.5rem;
      color: #666;
      line-height: 1.6;
    }
    .word-highlight {
      background: #ffeb3b;
      padding: 2px 4px;
      border-radius: 3px;
    }
    .navigation {
      display: flex;
      justify-content: space-between;
      padding: 20px 40px;
      border-top: 1px solid #eee;
    }
    button {
      padding: 12px 24px;
      font-size: 1rem;
      border: none;
      border-radius: 8px;
      background: #4CAF50;
      color: white;
      cursor: pointer;
      transition: background 0.3s;
    }
    button:hover { background: #45a049; }
    button:disabled { background: #ccc; cursor: not-allowed; }
    .audio-btn {
      background: #2196F3;
      margin: 20px 0;
    }
    .audio-btn:hover { background: #1976D2; }
    
    /* Mobile responsive */
    @media (max-width: 600px) {
      .book-page { padding: 20px; min-height: 400px; }
      .vocabulary { font-size: 2rem; }
      .sentence { font-size: 1.2rem; }
      .navigation { padding: 15px 20px; }
    }
  </style>
</head>
<body>
  <div class="book-container">
    <div id="book-content"></div>
    <div class="navigation">
      <button id="prev-btn">← Anterior</button>
      <span id="page-indicator">Página 1 de 10</span>
      <button id="next-btn">Siguiente →</button>
    </div>
  </div>

  <!-- Inline JavaScript -->
  <script>
    const BOOK_DATA = {
      title: "Los Colores",
      pages: [
        {
          text: "El cielo es <span class='word-highlight'>azul</span>.",
          vocabulary: "azul",
          translation: "blue",
          image: "images/blue-sky.webp",
          audioText: "El cielo es azul"
        },
        // ... more pages
      ]
    };

    let currentPage = 0;
    const contentDiv = document.getElementById('book-content');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const pageIndicator = document.getElementById('page-indicator');

    function renderPage(pageIndex) {
      const page = BOOK_DATA.pages[pageIndex];
      contentDiv.innerHTML = `
        <div class="book-page">
          <h2 class="vocabulary">${page.vocabulary}</h2>
          <img src="${page.image}" alt="${page.vocabulary}" loading="lazy">
          <p class="sentence">${page.text}</p>
          <button class="audio-btn" onclick="playAudio('${page.audioText}')">
            🔊 Escuchar
          </button>
        </div>
      `;
      
      pageIndicator.textContent = `Página ${pageIndex + 1} de ${BOOK_DATA.pages.length}`;
      prevBtn.disabled = pageIndex === 0;
      nextBtn.disabled = pageIndex === BOOK_DATA.pages.length - 1;
    }

    function playAudio(text) {
      // Web Speech API (free, works in modern browsers)
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'es-ES';
      utterance.rate = 0.9; // Slightly slower for preschoolers
      speechSynthesis.speak(utterance);
    }

    prevBtn.addEventListener('click', () => {
      if (currentPage > 0) {
        currentPage--;
        renderPage(currentPage);
      }
    });

    nextBtn.addEventListener('click', () => {
      if (currentPage < BOOK_DATA.pages.length - 1) {
        currentPage++;
        renderPage(currentPage);
      }
    });

    // Initialize
    renderPage(currentPage);
  </script>
</body>
</html>
```

---

## SEO Optimization

### URL Structure
```
https://beibeiamigos.com/spanish-books/week-1-colors/
https://beibeiamigos.com/spanish-books/week-2-shapes/
https://beibeiamigos.com/spanish-books/week-3-numbers/
```

### Meta Tags (per book)
```html
<title>{Spanish Title} - Free Spanish Book for Preschool | Beibei Amigos</title>
<meta name="description" content="{Theme description}. Free interactive book with audio. Ages 2-5. By Beibei Amigos, Phoenix's premier trilingual preschool.">
<meta name="keywords" content="spanish books preschool, {theme} spanish, free spanish learning, montessori, phoenix preschool, beibei amigos">

<!-- Open Graph (Facebook) -->
<meta property="og:title" content="{Spanish Title} - Free Spanish Book">
<meta property="og:description" content="Interactive Spanish book teaching {theme} to preschoolers">
<meta property="og:image" content="https://beibeiamigos.com/books/week-1/cover.jpg">
<meta property="og:url" content="https://beibeiamigos.com/spanish-books/week-1-colors/">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{Spanish Title}">
<meta name="twitter:description" content="Free Spanish vocabulary book for ages 2-5">
<meta name="twitter:image" content="https://beibeiamigos.com/books/week-1/cover.jpg">
```

### Schema Markup (Book + Organization)
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Book",
      "name": "Los Colores",
      "alternateName": "The Colors",
      "description": "Interactive Spanish vocabulary book teaching colors to preschoolers",
      "inLanguage": "es",
      "educationalLevel": "Preschool",
      "url": "https://beibeiamigos.com/spanish-books/week-1-colors/",
      "image": "https://beibeiamigos.com/books/week-1/cover.jpg",
      "audience": {
        "@type": "EducationalAudience",
        "educationalRole": "student",
        "audienceType": "children ages 2-5"
      },
      "author": {
        "@id": "https://beibeiamigos.com/#organization"
      },
      "publisher": {
        "@id": "https://beibeiamigos.com/#organization"
      },
      "keywords": ["spanish", "preschool", "colors", "vocabulary", "trilingual"],
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5.0",
        "reviewCount": "47"
      }
    },
    {
      "@type": "Organization",
      "@id": "https://beibeiamigos.com/#organization",
      "name": "Beibei Amigos Language Preschool",
      "url": "https://beibeiamigos.com",
      "logo": "https://beibeiamigos.com/logo.png",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Phoenix",
        "addressRegion": "AZ",
        "addressCountry": "US"
      },
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+1-XXX-XXX-XXXX",
        "contactType": "Admissions"
      }
    }
  ]
}
```

---

## Business Integration

### Call-to-Action Placement

**1. Top Banner (sticky)**
```html
<div class="cta-banner">
  📚 Love this book? Explore our preschool programs!
  <a href="/enroll">Schedule Tour</a>
</div>
```

**2. Sidebar (desktop only)**
```html
<div class="sidebar-cta">
  <h3>🛍️ Shop Learning Materials</h3>
  <ul>
    <li>Spanish Language CDs - $19.99</li>
    <li>Trilingual Flashcards - $14.99</li>
    <li>Montessori Materials - Starting at $9.99</li>
  </ul>
  <a href="/shop" class="btn-primary">Shop Now</a>
</div>
```

**3. End of Book**
```html
<div class="book-end-cta">
  <h2>🌟 Did your child love this book?</h2>
  <p>Leave us a Google review and unlock a BONUS book!</p>
  <a href="https://g.page/r/..." class="btn-review">Leave Review</a>
  
  <hr>
  
  <h3>📧 Get a new book every week!</h3>
  <form action="/subscribe" method="post">
    <input type="email" placeholder="Your email" required>
    <button type="submit">Subscribe Free</button>
  </form>
</div>
```

### Analytics Tracking
```html
<!-- Google Tag Manager -->
<script>
dataLayer.push({
  'event': 'book_view',
  'book_title': 'Los Colores',
  'book_week': '1',
  'book_theme': 'Colors'
});
</script>

<!-- Track page completion -->
<script>
// Fire when user reaches last page
if (currentPage === BOOK_DATA.pages.length - 1) {
  dataLayer.push({
    'event': 'book_complete',
    'book_title': 'Los Colores'
  });
}
</script>
```

---

## Testing Checklist

Before deployment:

### Performance
- [ ] Page load < 2 seconds (Google PageSpeed Insights)
- [ ] Images lazy-loaded
- [ ] No render-blocking resources
- [ ] Mobile-friendly (Google Mobile-Friendly Test)

### SEO
- [ ] Schema validates (Google Rich Results Test)
- [ ] Meta tags present and accurate
- [ ] Alt tags on all images
- [ ] Heading hierarchy correct (H1 → H2 → H3)
- [ ] Internal links working

### Functionality
- [ ] Page navigation works (prev/next buttons)
- [ ] Audio plays on all devices
- [ ] Responsive on mobile/tablet/desktop
- [ ] Works in WordPress Divi module
- [ ] CTAs clickable and track correctly

### Business
- [ ] Review link correct (Google My Business)
- [ ] Shop links working
- [ ] Email signup functional
- [ ] Analytics tracking firing

---

**Last Updated:** 2026-01-28  
**For:** Books Agent - Automated Preschool Book Builder
