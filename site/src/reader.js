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

  function stop() {
    player.pause();
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    listen.classList.remove('playing');
    reader.querySelectorAll('.say').forEach(function (el) { el.classList.remove('say'); });
  }

  /* Play a recording. If there is none (or it fails), use the device's Spanish voice. */
  function say(src, text, done) {
    stop();
    function fallback() {
      if (!window.speechSynthesis || !text) { if (done) done(); return; }
      var u = new SpeechSynthesisUtterance(text);
      u.lang = 'es-MX';
      u.rate = 0.8;
      u.onend = u.onerror = function () { if (done) done(); };
      window.speechSynthesis.speak(u);
    }
    if (!src) return fallback();
    player.src = src;
    player.onended = function () { if (done) done(); };
    player.onerror = fallback;
    var p = player.play();
    if (p && p.catch) p.catch(function () { if (done) done(); });
  }

  function playPage() {
    var pg = pages[current];
    var text = pg.getAttribute('data-say');
    if (!text) return;
    say(pg.getAttribute('data-audio'), text, function () { listen.classList.remove('playing'); });
    listen.classList.add('playing'); // after say(), because say() first stops anything already playing
  }

  function show(i, dir) {
    if (i < 0 || i >= pages.length) return;
    stop();
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
    if (current === pages.length - 1) track('book_finished');
  }

  prev.addEventListener('click', function () { show(current - 1, -1); });
  next.addEventListener('click', function () { show(current + 1, 1); });
  listen.addEventListener('click', function () {
    if (listen.classList.contains('playing')) stop(); else playPage();
  });

  english.addEventListener('change', function () { reader.classList.toggle('no-en', !english.checked); });

  document.addEventListener('keydown', function (e) {
    if (e.target.matches('input, textarea')) return;
    if (e.key === 'ArrowRight') show(current + 1, 1);
    if (e.key === 'ArrowLeft') show(current - 1, -1);
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

  /* Tap a coloured word or a vocabulary card to hear just that word. */
  reader.addEventListener('click', function (e) {
    var el = e.target.closest('[data-word]');
    if (!el) return;
    say(el.getAttribute('data-word-audio'), el.getAttribute('data-word'), function () { el.classList.remove('say'); });
    el.classList.add('say');
    track('word_tap', { word: el.getAttribute('data-word') });
  });

  show(0, 0);
})();
