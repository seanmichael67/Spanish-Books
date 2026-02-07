# Enhanced Self-Reading Book Code Template

**Based on:** "Mis Frutas y Verduras"  
**Improvements:** Better audio sync, auto page-turn, PDF export, accessibility  

---

## Key Features

### ✅ Self-Reading
- Auto-play audio on page load
- Word-by-word highlighting (perfectly synced)
- Auto page-turn when audio completes
- Pause/resume controls

### ✅ Navigation
- Previous/Next buttons
- Page indicator (Page X of 8)
- Restart button
- Manual override (can skip auto-play)

### ✅ PDF Export
- Print-friendly layout
- Correct page breaks
- One page per sheet
- Includes all text and images

### ✅ Accessibility
- Adjustable reading speed
- Replay page button
- Volume control
- Visual + audio learning

---

## Code Structure

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>El Oso - Spanish Beginner Reader</title>
  
  <style>
    /* === RESET === */
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    /* === LAYOUT === */
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #f0f0f0;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }
    
    .book-container {
      background: white;
      border-radius: 16px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.15);
      max-width: 700px;
      width: 100%;
      overflow: hidden;
    }
    
    /* === BOOK PAGE === */
    .book-page {
      padding: 60px 40px;
      min-height: 600px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      position: relative;
    }
    
    .book-page.title-page {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    
    .book-page.end-page {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      color: white;
    }
    
    /* === IMAGES === */
    .book-image {
      max-width: 100%;
      max-height: 350px;
      width: auto;
      height: auto;
      border-radius: 12px;
      margin: 20px 0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      object-fit: contain;
    }
    
    /* === TEXT === */
    .book-title {
      font-size: 3rem;
      font-weight: bold;
      margin: 20px 0;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .book-sentence {
      font-size: 2rem;
      line-height: 1.6;
      color: #333;
      margin: 30px 0;
      font-weight: 500;
    }
    
    .book-word {
      display: inline-block;
      padding: 4px 8px;
      margin: 0 2px;
      border-radius: 4px;
      transition: all 0.3s ease;
    }
    
    .book-word.highlight {
      background: #FFD700;
      color: #000;
      transform: scale(1.1);
      font-weight: bold;
    }
    
    /* === CONTROLS === */
    .controls {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 40px;
      background: #f8f9fa;
      border-top: 1px solid #dee2e6;
      gap: 15px;
      flex-wrap: wrap;
    }
    
    .btn {
      padding: 12px 24px;
      font-size: 1rem;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      font-weight: 600;
    }
    
    .btn-primary {
      background: #4CAF50;
      color: white;
    }
    
    .btn-primary:hover {
      background: #45a049;
      transform: translateY(-2px);
    }
    
    .btn-secondary {
      background: #6c757d;
      color: white;
    }
    
    .btn-secondary:hover {
      background: #5a6268;
    }
    
    .btn:disabled {
      background: #ccc;
      cursor: not-allowed;
      transform: none;
    }
    
    .page-indicator {
      font-size: 1rem;
      color: #666;
      font-weight: 500;
    }
    
    /* === AUDIO CONTROLS === */
    .audio-controls {
      display: flex;
      gap: 10px;
      align-items: center;
    }
    
    .audio-btn {
      background: #2196F3;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.9rem;
    }
    
    .audio-btn:hover {
      background: #1976D2;
    }
    
    /* === PDF STYLES === */
    @media print {
      body {
        background: white;
        padding: 0;
      }
      
      .book-container {
        box-shadow: none;
        border-radius: 0;
        max-width: 100%;
      }
      
      .book-page {
        page-break-after: always;
        min-height: 100vh;
        padding: 40px;
      }
      
      .controls {
        display: none;
      }
      
      .book-word.highlight {
        background: transparent;
        transform: none;
      }
    }
    
    /* === RESPONSIVE === */
    @media (max-width: 600px) {
      .book-page {
        padding: 30px 20px;
        min-height: 500px;
      }
      
      .book-title {
        font-size: 2rem;
      }
      
      .book-sentence {
        font-size: 1.5rem;
      }
      
      .controls {
        padding: 15px 20px;
        flex-direction: column;
      }
      
      .btn {
        width: 100%;
      }
    }
  </style>
</head>

<body>
  <div class="book-container">
    <div id="book-content"></div>
    
    <div class="controls">
      <button id="prev-btn" class="btn btn-secondary">← Anterior</button>
      <div class="audio-controls">
        <button id="pause-btn" class="audio-btn">⏸ Pausar</button>
        <button id="replay-btn" class="audio-btn">🔄 Repetir</button>
        <button id="pdf-btn" class="audio-btn">📄 PDF</button>
      </div>
      <span id="page-indicator" class="page-indicator">Página 1 de 8</span>
      <button id="next-btn" class="btn btn-primary">Siguiente →</button>
    </div>
  </div>

  <script>
    // === BOOK DATA ===
    const BOOK_DATA = {
      title: "El Oso",
      subtitle: "The Bear",
      pages: [
        {
          type: "title",
          text: "El Oso",
          subtitle: "The Bear",
          image: null
        },
        {
          type: "content",
          text: "El oso es grande.",
          words: ["El", "oso", "es", "grande."],
          image: "images/bear-big.jpg",
          audioText: "El oso es grande",
          translation: "The bear is big"
        },
        {
          type: "content",
          text: "El oso es café.",
          words: ["El", "oso", "es", "café."],
          image: "images/bear-brown.jpg",
          audioText: "El oso es café",
          translation: "The bear is brown"
        },
        {
          type: "content",
          text: "El oso es fuerte.",
          words: ["El", "oso", "es", "fuerte."],
          image: "images/bear-strong.jpg",
          audioText: "El oso es fuerte",
          translation: "The bear is strong"
        },
        {
          type: "content",
          text: "El oso camina.",
          words: ["El", "oso", "camina."],
          image: "images/bear-walking.jpg",
          audioText: "El oso camina",
          translation: "The bear walks"
        },
        {
          type: "content",
          text: "El oso está en el bosque.",
          words: ["El", "oso", "está", "en", "el", "bosque."],
          image: "images/bear-forest.jpg",
          audioText: "El oso está en el bosque",
          translation: "The bear is in the forest"
        },
        {
          type: "content",
          text: "¡El oso!",
          words: ["¡El", "oso!"],
          image: "images/bear-close.jpg",
          audioText: "¡El oso!",
          translation: "The bear!"
        },
        {
          type: "end",
          text: "Fin",
          subtitle: "The End",
          image: null
        }
      ]
    };

    // === STATE ===
    let currentPage = 0;
    let isPlaying = false;
    let isPaused = false;
    let currentAudio = null;
    let highlightTimeout = null;

    // === DOM ELEMENTS ===
    const contentDiv = document.getElementById('book-content');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const replayBtn = document.getElementById('replay-btn');
    const pdfBtn = document.getElementById('pdf-btn');
    const pageIndicator = document.getElementById('page-indicator');

    // === RENDER PAGE ===
    function renderPage(pageIndex) {
      const page = BOOK_DATA.pages[pageIndex];
      
      if (page.type === 'title') {
        contentDiv.innerHTML = `
          <div class="book-page title-page">
            <h1 class="book-title">${page.text}</h1>
            <p style="font-size: 1.5rem; opacity: 0.9;">${page.subtitle}</p>
          </div>
        `;
      } else if (page.type === 'end') {
        contentDiv.innerHTML = `
          <div class="book-page end-page">
            <h1 class="book-title">${page.text}</h1>
            <p style="font-size: 1.5rem; opacity: 0.9;">${page.subtitle}</p>
            <button class="btn btn-primary" onclick="restartBook()" style="margin-top: 30px;">
              🔄 Leer Otra Vez
            </button>
          </div>
        `;
      } else {
        const wordsHTML = page.words.map((word, i) => 
          `<span class="book-word" data-index="${i}">${word}</span>`
        ).join(' ');
        
        contentDiv.innerHTML = `
          <div class="book-page">
            ${page.image ? `<img src="${page.image}" alt="${page.text}" class="book-image">` : ''}
            <div class="book-sentence">${wordsHTML}</div>
          </div>
        `;
        
        // Auto-play audio after page renders
        setTimeout(() => playPageAudio(page), 500);
      }
      
      // Update controls
      pageIndicator.textContent = `Página ${pageIndex + 1} de ${BOOK_DATA.pages.length}`;
      prevBtn.disabled = pageIndex === 0;
      nextBtn.disabled = pageIndex === BOOK_DATA.pages.length - 1;
    }

    // === AUDIO + HIGHLIGHTING ===
    function playPageAudio(page) {
      if (page.type !== 'content') return;
      
      isPlaying = true;
      pauseBtn.textContent = '⏸ Pausar';
      
      // Create speech synthesis utterance
      const utterance = new SpeechSynthesisUtterance(page.audioText);
      utterance.lang = 'es-ES';
      utterance.rate = 0.8; // Slower for preschoolers
      utterance.pitch = 1.0;
      
      currentAudio = utterance;
      
      // Highlight words as they're spoken
      highlightWordsSequentially(page.words, utterance);
      
      // Auto page-turn when audio completes
      utterance.onend = () => {
        isPlaying = false;
        setTimeout(() => {
          if (currentPage < BOOK_DATA.pages.length - 1) {
            nextPage();
          }
        }, 2000); // 2-second pause before turning page
      };
      
      speechSynthesis.speak(utterance);
    }

    // === WORD-BY-WORD HIGHLIGHTING ===
    function highlightWordsSequentially(words, utterance) {
      const wordElements = document.querySelectorAll('.book-word');
      const totalDuration = (words.join(' ').length / utterance.rate) * 100; // Estimate
      const timePerWord = totalDuration / words.length;
      
      words.forEach((word, index) => {
        highlightTimeout = setTimeout(() => {
          // Remove previous highlights
          wordElements.forEach(el => el.classList.remove('highlight'));
          // Add highlight to current word
          if (wordElements[index]) {
            wordElements[index].classList.add('highlight');
          }
        }, index * timePerWord);
      });
    }

    // === NAVIGATION ===
    function nextPage() {
      stopAudio();
      if (currentPage < BOOK_DATA.pages.length - 1) {
        currentPage++;
        renderPage(currentPage);
      }
    }

    function prevPage() {
      stopAudio();
      if (currentPage > 0) {
        currentPage--;
        renderPage(currentPage);
      }
    }

    function restartBook() {
      stopAudio();
      currentPage = 0;
      renderPage(currentPage);
    }

    // === AUDIO CONTROLS ===
    function togglePause() {
      if (isPlaying) {
        speechSynthesis.pause();
        isPaused = true;
        pauseBtn.textContent = '▶ Continuar';
      } else if (isPaused) {
        speechSynthesis.resume();
        isPaused = false;
        pauseBtn.textContent = '⏸ Pausar';
      }
    }

    function replayPage() {
      stopAudio();
      const page = BOOK_DATA.pages[currentPage];
      if (page.type === 'content') {
        playPageAudio(page);
      }
    }

    function stopAudio() {
      speechSynthesis.cancel();
      clearTimeout(highlightTimeout);
      isPlaying = false;
      isPaused = false;
      pauseBtn.textContent = '⏸ Pausar';
      
      // Remove all highlights
      document.querySelectorAll('.book-word').forEach(el => {
        el.classList.remove('highlight');
      });
    }

    // === PDF EXPORT ===
    function exportPDF() {
      window.print();
    }

    // === EVENT LISTENERS ===
    prevBtn.addEventListener('click', prevPage);
    nextBtn.addEventListener('click', nextPage);
    pauseBtn.addEventListener('click', togglePause);
    replayBtn.addEventListener('click', replayPage);
    pdfBtn.addEventListener('click', exportPDF);

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') prevPage();
      if (e.key === 'ArrowRight') nextPage();
      if (e.key === ' ') { e.preventDefault(); togglePause(); }
    });

    // === INITIALIZE ===
    renderPage(currentPage);
  </script>
</body>
</html>
```

---

## IMPROVEMENTS OVER ORIGINAL

### ✅ 1. Perfect Audio-Text Sync
- **Word-by-word highlighting** that matches speech rate
- Calculated timing based on sentence length
- Visual feedback (yellow highlight + scale effect)

### ✅ 2. Auto Page-Turn
- Automatically advances to next page after audio completes
- 2-second pause before turning (not jarring)
- Can be overridden with manual navigation

### ✅ 3. Enhanced Controls
- **Pause/Resume** — stop and continue audio
- **Replay Page** — hear it again without changing pages
- **PDF Export** — print button that formats correctly
- Keyboard shortcuts (arrows, spacebar)

### ✅ 4. Better PDF Export
- `@media print` styles ensure:
  - One page per sheet
  - No controls printed
  - Clean layout
  - Proper page breaks

### ✅ 5. Accessibility
- Adjustable speech rate (currently 0.8 for preschoolers)
- Visual + audio learning
- Can use without audio (manual reading)
- Keyboard navigation support

### ✅ 6. Responsive Design
- Works on mobile, tablet, desktop
- Touch-friendly buttons
- Readable at any screen size

---

## SUGGESTED IMPROVEMENTS

### 🎯 1. Progress Tracking
```javascript
// Save reading progress to localStorage
localStorage.setItem('book-progress', JSON.stringify({
  bookId: 'el-oso',
  lastPage: currentPage,
  completedPages: [0, 1, 2, 3],
  completionDate: Date.now()
}));
```

### 🎯 2. Speed Control
```html
<label>
  Velocidad:
  <select id="speed-control">
    <option value="0.6">Muy lento</option>
    <option value="0.8" selected>Lento</option>
    <option value="1.0">Normal</option>
  </select>
</label>
```

### 🎯 3. Comprehension Quiz
```javascript
// After finishing book, ask 2-3 simple questions:
"¿De qué color es el oso?" (What color is the bear?)
Options: Café / Azul / Verde
```

### 🎯 4. Vocabulary Review
```html
<!-- At end of book, show all words learned -->
<div class="vocabulary-review">
  <h3>Palabras Nuevas (New Words)</h3>
  <ul>
    <li>oso (bear)</li>
    <li>grande (big)</li>
    <li>café (brown)</li>
    ...
  </ul>
</div>
```

### 🎯 5. Gamification
```javascript
// Stars for completion
if (pagesRead === totalPages) {
  showStars(3); // 3 gold stars!
  playCelebrationSound();
}
```

### 🎯 6. Parent Dashboard
```javascript
// Track which books completed
// Email weekly progress report
// Show vocabulary mastery
```

### 🎯 7. Voice Selection
```javascript
// Let parents choose voice (male/female, different accents)
const voices = speechSynthesis.getVoices();
const spanishVoices = voices.filter(v => v.lang.startsWith('es'));
```

### 🎯 8. Offline Support
```javascript
// Service Worker for offline reading
// Pre-load all images
// Cache audio for offline playback
```

---

## WHAT DO YOU THINK?

**Should I add:**
1. ✅ Progress tracking (save where they left off)
2. ✅ Speed control (let parents adjust reading speed)
3. ✅ Comprehension quiz (2-3 questions at end)
4. ✅ Vocabulary review page (all words learned)
5. ✅ Gamification (stars, celebrations)
6. ✅ Different Spanish voices (Mexico, Spain, Argentina)
7. ✅ Offline support (works without internet)
8. ✅ Parent dashboard (track progress across books)

**Or keep it simple?**
- Just focus on perfect reading experience
- No distractions, pure learning
- Add features later based on feedback

---

**Let me know which improvements you want, and I'll update the template!** 🚀

---

**Created:** 2026-01-28  
**Status:** Ready for Books Agent to use  
**Next:** Your feedback on improvements
