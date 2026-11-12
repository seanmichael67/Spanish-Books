/* Everything on the site that is not the book reader:
   menu, email sign-up, buy buttons, library filters, and "my purchases". */
(function () {
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return [].slice.call((el || document).querySelectorAll(s)); };
  var track = function (name, data) { if (window.gtag) window.gtag('event', name, data || {}); };

  /* ---- Mobile menu ---- */
  var menu = $('.menu-btn');
  if (menu) menu.addEventListener('click', function () {
    var open = $('.nav').classList.toggle('open');
    menu.setAttribute('aria-expanded', open);
  });

  function post(url, data) {
    return fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, data: j }; }); })
      .catch(function () { return { ok: false, data: { error: 'No connection. Please try again.' } }; });
  }

  /* ---- Email sign-up ---- */
  $$('form[data-signup]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = $('.msg', form);
      var btn = $('button', form);
      btn.disabled = true;
      msg.className = 'msg';
      msg.textContent = 'Un momento…';
      post('/api/subscribe', { email: form.email.value, name: form.name ? form.name.value : '', website: form.website.value }).then(function (r) {
        btn.disabled = false;
        if (r.ok) {
          msg.className = 'msg ok';
          msg.innerHTML = '¡Listo! You are on the list. <a href="/muestra/">Open your free printable book →</a>';
          form.reset();
          track('sign_up', { method: 'email' });
        } else {
          msg.className = 'msg bad';
          msg.textContent = r.data.error || 'Something went wrong. Please try again.';
        }
      });
    });
  });

  /* ---- Buy buttons ---- */
  $$('[data-buy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var label = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Opening checkout…';
      track('begin_checkout', { item_id: btn.getAttribute('data-buy') });
      post('/api/checkout', { product: btn.getAttribute('data-buy') }).then(function (r) {
        if (r.ok && r.data.url) { window.location.href = r.data.url; return; }
        btn.disabled = false;
        btn.textContent = label;
        alert(r.data.error || 'We could not open the checkout. Please try again.');
      });
    });
  });

  /* ---- Stars on books this child has finished (saved in this browser) ---- */
  var read = [];
  try { read = JSON.parse(localStorage.getItem('beibei-libros-read') || '[]'); } catch (e) {}
  $$('.book').forEach(function (b) {
    var m = b.getAttribute('href').match(/\/libros\/([^/]+)\//);
    if (m && read.indexOf(m[1]) >= 0) b.classList.add('done');
  });
  var prog = $('[data-progress]');
  if (prog && read.length) { prog.hidden = false; prog.textContent = '⭐ You have read ' + read.length + (read.length === 1 ? ' book' : ' books') + '. ¡Sigue leyendo!'; }

  /* ---- Library filters ---- */
  var lib = $('[data-library]');
  if (lib) {
    var query = new URLSearchParams(location.search);
    var state = { theme: query.get('tema') || 'all', level: query.get('nivel') || 'all' };
    var apply = function () {
      var shown = 0;
      $$('.book', lib).forEach(function (b) {
        var ok = (state.theme === 'all' || b.getAttribute('data-theme') === state.theme) && (state.level === 'all' || b.getAttribute('data-level') === state.level);
        b.hidden = !ok;
        if (ok) shown++;
      });
      $$('[data-filter]').forEach(function (btn) {
        btn.setAttribute('aria-pressed', state[btn.getAttribute('data-filter')] === btn.value);
      });
      $('.empty-note').style.display = shown ? 'none' : 'block';
      $('[data-count]').textContent = shown;
    };
    $$('[data-filter]').forEach(function (btn) {
      btn.addEventListener('click', function () { state[btn.getAttribute('data-filter')] = btn.value; apply(); });
    });
    apply();
  }

  /* ---- Purchases (saved in this browser) ---- */
  var KEY = 'beibei-libros-access';
  function tokens() { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; } }
  function saveToken(t) {
    var all = tokens();
    if (t && all.indexOf(t) < 0) { all.push(t); try { localStorage.setItem(KEY, JSON.stringify(all)); } catch (e) {} }
  }
  function productsIn(token) {
    try {
      var b = token.split('.')[0].replace(/-/g, '+').replace(/_/g, '/');
      return JSON.parse(decodeURIComponent(escape(atob(b)))).p || [];
    } catch (e) { return []; }
  }
  /* Which token opens which pack? (the library token opens them all) */
  function accessMap() {
    var map = {};
    tokens().forEach(function (t) {
      productsIn(t).forEach(function (p) { map[p] = t; });
    });
    return map;
  }

  function renderOwned(el) {
    var catalog = JSON.parse($('#catalog').textContent);
    var map = accessMap();
    var all = map.biblioteca || map.escuela || map.club; /* these unlock every pack */
    var html = catalog.filter(function (p) { return map[p.id] || all; }).map(function (p) {
      var t = encodeURIComponent(map[p.id] || all);
      var base = '/api/pack?product=' + p.id + '&t=' + t;
      return '<div class="box"><h3>' + p.emoji + ' ' + p.name + '</h3>' +
        '<div class="row"><a class="btn small" href="' + base + '" target="_blank" rel="noopener">🖨 Print the whole pack</a></div>' +
        '<p style="margin:14px 0 6px">Or print one book at a time:</p><ul>' +
        p.books.map(function (b) { return '<li><a href="' + base + '&book=' + b.slug + '" target="_blank" rel="noopener">' + b.title + '</a></li>'; }).join('') +
        '</ul></div>';
    }).join('');
    el.innerHTML = html;
    return Boolean(html);
  }

  /* Thank-you page: confirm the payment, then unlock. */
  var thanks = $('[data-thanks]');
  if (thanks) {
    var id = new URLSearchParams(location.search).get('session_id');
    var status = $('[data-status]', thanks);
    if (!id) { status.innerHTML = 'No order found here. <a href="/mis-compras/">Find my purchases</a>'; }
    else fetch('/api/access?session_id=' + encodeURIComponent(id)).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, data: j }; }); }).then(function (r) {
      if (!r.ok) { status.className = 'msg bad'; status.textContent = r.data.error || 'We could not confirm the payment.'; return; }
      saveToken(r.data.token);
      history.replaceState(null, '', location.pathname);
      status.className = 'msg ok';
      status.textContent = '¡Gracias! Your payment is confirmed.' + (r.data.emailed ? ' We also emailed your link to ' + r.data.email + '.' : '');
      renderOwned($('[data-owned]', thanks));
      track('purchase', { transaction_id: id, items: [{ item_id: r.data.product }] });
    }).catch(function () { status.className = 'msg bad'; status.textContent = 'No connection. Refresh this page to try again.'; });
  }

  /* My purchases page */
  var mine = $('[data-mine]');
  if (mine) {
    var t = new URLSearchParams(location.search).get('t');
    if (t) { saveToken(t); history.replaceState(null, '', location.pathname); }
    var any = renderOwned($('[data-owned]', mine));
    var clubToken = accessMap().club;
    if (clubToken) {
      $('[data-member]', mine).hidden = false;
      $('[data-portal]', mine).addEventListener('click', function () {
        var note = $('[data-portal-msg]', mine);
        note.textContent = 'Un momento…';
        post('/api/portal', { t: clubToken }).then(function (r) {
          if (r.ok && r.data.url) { window.location.href = r.data.url; return; }
          note.className = 'msg bad';
          note.textContent = r.data.error || 'Please try again.';
        });
      });
    }
    $('[data-none]', mine).hidden = any;
    var form = $('form[data-restore]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = $('.msg', form);
      msg.className = 'msg';
      msg.textContent = 'Un momento…';
      post('/api/restore', { email: form.email.value }).then(function (r) {
        msg.className = 'msg ' + (r.ok ? 'ok' : 'bad');
        msg.textContent = r.ok ? 'If that email has purchases, a link is on its way. Check your inbox in a minute.' : (r.data.error || 'Please try again.');
      });
    });
  }
})();
