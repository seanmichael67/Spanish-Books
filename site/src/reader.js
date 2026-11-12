/* The book reader: turns pages, plays the recorded audio, and lets children
   tap a coloured word to hear it. Works with arrow keys and swipes too. */
(function () {
  var reader = document.querySelector('.reader');
  if (!reader) return;
  document.documentElement.classList.add('js');

  var pages = [].slice.call(reader.querySelectorAll('.pg'));
  var dots = reader.querySelector('.dots');
  var prev = reader.querySelector('[data-prev]');
  var next = reader.querySelector('[data-next]');
  var listen = reader.querySelector('[data-listen]');
  var auto = reader.querySelector('[data-auto]');
  var english = reader.querySelector('[data-english]');
  var player = new Audio();
  var current = 0;
  var slug = reader.getAttribute('data-book');

  function track(name, extra) {
    if (window.gtag) window.gtag('event', name, Object.assign({ book: slug }, extra || {}));
  }

  pages.forEach(function () { dots.appendChild(document.createElement('i')); });

  /* ---- Reading helpers: slower voice and "my turn" (remembered in this browser) ---- */
  var slowBtn = reader.querySelector('[data-slow]');
  var turnBtn = reader.querySelector('[data-turn]');
  var turnNote = reader.querySelector('[data-turn-note]');
  var turnTimer = null;
  var clipTimer = null;
  function remembered(key) { try { return localStorage.getItem('beibei-libros-' + key) === '1'; } catch (e) { return false; } }
  function remember(key, on) { try { localStorage.setItem('beibei-libros-' + key, on ? '1' : '0'); } catch (e) {} }
  function pressed(btn) { return btn.getAttribute('aria-pressed') === 'true'; }
  function turnOn() { return pressed(turnBtn); }
  function speed() { return pressed(slowBtn) ? 0.75 : 1; }
  [[slowBtn, 'slow'], [turnBtn, 'turn']].forEach(function (pair) {
    var btn = pair[0];
    btn.setAttribute('aria-pressed', remembered(pair[1]));
    btn.addEventListener('click', function () {
      var on = !pressed(btn);
      btn.setAttribute('aria-pressed', on);
      remember(pair[1], on);
      player.playbackRate = speed();
      track('helper_' + pair[1], { on: on });
    });
  });

  /* ---- Word-by-word highlighting ----
     Each Spanish word is wrapped in a small box so it can light up while it is
     spoken. The page text itself is untouched in the HTML that Google reads. */
  var hasLetter = /[A-Za-zÀ-ÿ0-9]/;
  function wrapWords(node) {
    [].slice.call(node.childNodes).forEach(function (child) {
      if (child.nodeType === 3) {
        var frag = document.createDocumentFragment();
        child.nodeValue.split(/(\s+)/).forEach(function (piece) {
          if (hasLetter.test(piece)) {
            var span = document.createElement('span');
            span.className = 'w';
            span.textContent = piece;
            frag.appendChild(span);
          } else if (piece && /\S/.test(piece)) {
            /* Punctuation: keep it glued to the word before it, so a full stop never wraps onto its own line. */
            var before = frag.lastChild || child.previousSibling;
            if (before && before.nodeType === 1) {
              var glue = document.createElement('span');
              glue.className = 'nb';
              before.parentNode.insertBefore(glue, before);
              glue.appendChild(before);
              glue.appendChild(document.createTextNode(piece));
            } else frag.appendChild(document.createTextNode(piece));
          } else if (piece) frag.appendChild(document.createTextNode(piece));
        });
        node.replaceChild(frag, child);
      } else if (child.nodeType === 1) {
        if (/\s/.test(child.textContent.trim())) wrapWords(child); else child.classList.add('w');
      }
    });
  }
  pages.forEach(function (pg) {
    var es = pg.querySelector('.txt .es');
    if (!es) return;
    wrapWords(es);
    pg.words = [].slice.call(es.querySelectorAll('.w'));
    var raw = pg.getAttribute('data-t');
    var times = raw ? raw.split(',').map(function (x) { return x.split('-').map(Number); }) : null;
    pg.times = times && times.length === pg.words.length ? times : null;
  });

  var ticking = null;
  function clearWords() {
    if (ticking) cancelAnimationFrame(ticking);
    ticking = null;
    reader.querySelectorAll('.w.now, .en.now').forEach(function (el) { el.classList.remove('now'); });
  }
  function lightWord(pg, index) {
    pg.words.forEach(function (w, n) { w.classList.toggle('now', n === index); });
  }
  /* Follow the recording: light the word whose time has come, then the English line. */
  function follow(pg) {
    if (!pg.times) return;
    var last = pg.times[pg.times.length - 1][1];
    var en = pg.querySelector('.txt .en');
    (function tick() {
      var t = player.currentTime * 1000;
      var index = -1;
      for (var n = 0; n < pg.times.length; n++) if (t >= pg.times[n][0] - 40) index = n;
      if (t > last + 120) index = -1;
      /* "Mi turno": stop after the Spanish sentence so the child can say it, then carry on. */
      if (turnOn() && !pg.turnDone && t > last + 250 && !player.paused) {
        pg.turnDone = true;
        player.pause();
        var es = pg.querySelector('.txt .es');
        es.classList.add('your-turn');
        turnNote.hidden = false;
        turnTimer = setTimeout(function () {
          es.classList.remove('your-turn');
          turnNote.hidden = true;
          var p = player.play();
          if (p && p.catch) p.catch(function () {});
        }, 1400 + 700 * pg.words.length);
      }
      lightWord(pg, index);
      if (en) en.classList.toggle('now', t > last + 1400); /* the English voice starts about 1.5 seconds after the Spanish ends */
      ticking = requestAnimationFrame(tick);
    })();
  }

  function stop() {
    player.pause();
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    listen.classList.remove('playing');
    reader.querySelectorAll('.say').forEach(function (el) { el.classList.remove('say'); });
    clearWords();
    clearTimeout(turnTimer);
    clearTimeout(clipTimer);
    turnNote.hidden = true;
    reader.querySelectorAll('.your-turn').forEach(function (el) { el.classList.remove('your-turn'); });
  }

  /* Play a recording. If there is none (or it fails), use the device's Spanish voice. */
  function say(src, text, done, pg) {
    stop();
    function fallback() {
      if (!window.speechSynthesis || !text) { if (done) done(); return; }
      var u = new SpeechSynthesisUtterance(text);
      u.lang = 'es-MX';
      u.rate = 0.8 * speed();
      u.onend = u.onerror = function () { clearWords(); if (done) done(); };
      /* The device voice tells us which letter it has reached; count the spaces before it. */
      if (pg && pg.words) u.onboundary = function (e) { lightWord(pg, text.slice(0, e.charIndex).split(/\s+/).filter(function (x) { return hasLetter.test(x); }).length); };
      window.speechSynthesis.speak(u);
    }
    if (!src) return fallback();
    player.src = src;
    player.preservesPitch = true;
    player.playbackRate = speed();
    if (pg) pg.turnDone = false;
    player.onended = function () { clearWords(); if (done) done(); };
    player.onplaying = function () { clearWords(); if (pg) follow(pg); };
    player.onerror = fallback;
    var p = player.play();
    if (p && p.catch) p.catch(function () { if (done) done(); });
  }

  function playPage() {
    var pg = pages[current];
    var text = pg.getAttribute('data-say');
    if (!text) return;
    say(pg.getAttribute('data-audio'), text, function () { listen.classList.remove('playing'); }, pg);
    listen.classList.add('playing'); // after say(), because say() first stops anything already playing
  }

  function show(i, dir) {
    if (i < 0 || i >= pages.length) return;
    stop();
    if (reader.classList.contains('gaming')) { reader.classList.remove('gaming'); queue = []; target = null; ask.textContent = ''; gameBtn.hidden = false; }
    pages[current].classList.remove('on');
    current = i;
    pages[current].style.setProperty('--dx', (dir < 0 ? -18 : 18) + 'px');
    pages[current].classList.add('on');
    [].forEach.call(dots.children, function (d, n) { d.classList.toggle('on', n === current); });
    prev.disabled = current === 0;
    next.disabled = current === pages.length - 1;
    listen.style.visibility = pages[current].getAttribute('data-say') ? 'visible' : 'hidden';
    if (dir && auto.checked) playPage();
    if (dir) track('book_page', { page: current + 1 });
    if (current === pages.length - 1) { track('book_finished'); markRead(); }
  }

  prev.addEventListener('click', function () { show(current - 1, -1); });
  next.addEventListener('click', function () { show(current + 1, 1); });
  listen.addEventListener('click', function () {
    if (listen.classList.contains('playing')) stop(); else playPage();
  });

  english.addEventListener('change', function () { reader.classList.toggle('no-en', !english.checked); });

  /* ---- Full-screen book mode ("Leer en grande") ----
     The same page elements are simply shown large over the whole window, so
     nothing is duplicated and the text stays on the page for search engines. */
  var fullBtn = reader.querySelector('[data-full]');
  var closeBtn = reader.querySelector('[data-close]');
  function setFull(on) {
    reader.classList.toggle('full', on);
    document.documentElement.classList.toggle('reading', on);
    closeBtn.hidden = !on;
    if (on) {
      if (reader.requestFullscreen) reader.requestFullscreen().catch(function () {});
      track('full_screen');
      if (auto.checked && current > 0) playPage();
    } else if (document.fullscreenElement && document.exitFullscreen) document.exitFullscreen().catch(function () {});
  }
  if (fullBtn) {
    fullBtn.addEventListener('click', function () { setFull(true); });
    closeBtn.addEventListener('click', function () { setFull(false); });
    document.addEventListener('fullscreenchange', function () { if (!document.fullscreenElement && reader.classList.contains('full')) setFull(false); });
  }

  document.addEventListener('keydown', function (e) {
    if (e.target.matches('input, textarea')) return;
    if (e.key === 'ArrowRight') show(current + 1, 1);
    if (e.key === 'ArrowLeft') show(current - 1, -1);
    if (e.key === 'Escape' && reader.classList.contains('full')) setFull(false);
    if (e.key === ' ' && reader.classList.contains('full')) { e.preventDefault(); if (listen.classList.contains('playing')) stop(); else playPage(); }
  });

  var startX = null;
  var stage = reader.querySelector('.stage');
  stage.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
  stage.addEventListener('touchend', function (e) {
    if (startX === null) return;
    var dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1);
    startX = null;
  });

  /* Remember finished books in this browser, so the library can show stars. */
  function markRead() {
    var list = [];
    try { list = JSON.parse(localStorage.getItem('beibei-libros-read') || '[]'); } catch (e) {}
    if (list.indexOf(slug) < 0) list.push(slug);
    try { localStorage.setItem('beibei-libros-read', JSON.stringify(list)); } catch (e) {}
    var out = reader.querySelector('[data-read-count]');
    if (out) out.textContent = '⭐ ' + list.length + (list.length === 1 ? ' book' : ' books') + ' read so far!';
  }

  /* The word game: "¿Dónde está…?" The child hears and reads a word and taps its picture. */
  var gameBtn = reader.querySelector('[data-game]');
  var ask = reader.querySelector('[data-ask]');
  var stars = reader.querySelector('[data-stars]');
  var cards = [].slice.call(reader.querySelectorAll('.vcard'));
  var queue = [];
  var target = null;

  function nextWord() {
    target = queue.shift() || null;
    if (!target) {
      reader.classList.remove('gaming');
      cards.forEach(function (c) { c.classList.remove('found'); });
      ask.textContent = '¡Muy bien! 🎉';
      gameBtn.textContent = '🎮 Jugar otra vez';
      gameBtn.hidden = false;
      track('game_finished');
      return;
    }
    ask.textContent = '¿Dónde está «' + target.getAttribute('data-word') + '»?';
    say(target.getAttribute('data-word-audio'), target.getAttribute('data-word'));
  }

  if (gameBtn) gameBtn.addEventListener('click', function () {
    queue = cards.slice().sort(function () { return Math.random() - 0.5; });
    cards.forEach(function (c) { c.classList.remove('found'); });
    stars.textContent = '';
    reader.classList.add('gaming');
    gameBtn.hidden = true;
    track('game_start');
    nextWord();
  });

  /* Tap a coloured word or a vocabulary card to hear just that word. */
  /* Tap any other word in the sentence: play only that word's slice of the page recording. */
  reader.addEventListener('click', function (e) {
    var w = e.target.closest('.txt .es .w');
    if (!w || w.hasAttribute('data-word') || w.closest('[data-word]')) return;
    var pg = pages[current];
    var n = pg.words ? pg.words.indexOf(w) : -1;
    var src = pg.getAttribute('data-audio');
    if (n < 0) return;
    stop();
    if (!pg.times || !src) {
      if (window.speechSynthesis) { var u = new SpeechSynthesisUtterance(w.textContent); u.lang = 'es-MX'; u.rate = 0.8 * speed(); window.speechSynthesis.speak(u); }
      return;
    }
    var from = Math.max(0, pg.times[n][0] - 60) / 1000;
    var to = (n + 1 < pg.times.length ? Math.min(pg.times[n][1] + 80, pg.times[n + 1][0]) : pg.times[n][1] + 120) / 1000;
    var go = function () {
      player.onplaying = null;
      player.onended = null;
      player.playbackRate = speed();
      player.currentTime = from;
      w.classList.add('now');
      var p = player.play();
      if (p && p.catch) p.catch(function () {});
      clipTimer = setTimeout(function () { player.pause(); w.classList.remove('now'); }, ((to - from) / speed()) * 1000 + 60);
    };
    if (player.src && player.src.indexOf(src) >= 0 && player.readyState >= 1) go();
    else { player.src = src; player.onloadedmetadata = function () { player.onloadedmetadata = null; go(); }; }
    track('word_tap', { word: w.textContent });
  });

  reader.addEventListener('click', function (e) {
    var el = e.target.closest('[data-word]');
    if (!el) return;
    if (reader.classList.contains('gaming') && el.classList.contains('vcard')) {
      if (el === target) {
        el.classList.add('found');
        stars.textContent += '⭐';
        setTimeout(nextWord, 700);
      } else if (!el.classList.contains('found')) {
        el.classList.remove('nope');
        void el.offsetWidth;
        el.classList.add('nope');
        say(target.getAttribute('data-word-audio'), target.getAttribute('data-word'));
      }
      return;
    }
    say(el.getAttribute('data-word-audio'), el.getAttribute('data-word'), function () { el.classList.remove('say'); });
    el.classList.add('say');
    track('word_tap', { word: el.getAttribute('data-word') });
  });

  show(0, 0);
})();
