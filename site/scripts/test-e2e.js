#!/usr/bin/env node
/*
 * End-to-end test. Starts the site with a PRETEND Stripe and a PRETEND Resend
 * (no real money, no real emails) and clicks through it in a real browser:
 * reading a book, joining the email list, buying a pack and printing it.
 *
 *   node site/build.js && node site/scripts/test-e2e.js
 *
 * Needs Playwright (npm i -D playwright). Screenshots go to SHOTS_DIR if set.
 */
const http = require('http');
const path = require('path');
const { spawn } = require('child_process');
const assert = require('assert');
const { chromium } = require('playwright');
const catalog = require('../../api/_lib/catalog');
const BOOKS = catalog.books.length;
const PACKS = catalog.packs.length;

const SITE = 'http://localhost:3100';
const MOCK = 'http://localhost:3101';
const SHOTS = process.env.SHOTS_DIR;
const sessions = {};
const emails = [];
const contacts = [];

const mock = http.createServer((req, res) => {
  let raw = '';
  req.on('data', (c) => { raw += c; });
  req.on('end', () => {
    const url = new URL(req.url, MOCK);
    const json = (code, data) => { res.writeHead(code, { 'Content-Type': 'application/json' }); res.end(JSON.stringify(data)); };
    if (req.headers.authorization !== 'Bearer sk_test_fake' && req.headers.authorization !== 'Bearer re_fake') return json(401, { error: { message: 'bad key' } });
    if (req.method === 'POST' && url.pathname === '/v1/checkout/sessions') {
      const p = new URLSearchParams(raw);
      const id = 'cs_test_' + Object.keys(sessions).length;
      sessions[id] = { id, payment_status: 'paid', status: 'complete', metadata: { product: p.get('metadata[product]') }, customer_details: { email: 'parent@example.com' }, amount: p.get('line_items[0][price_data][unit_amount]') };
      return json(200, { id, url: p.get('success_url').replace('{CHECKOUT_SESSION_ID}', id) });
    }
    if (req.method === 'GET' && url.pathname === '/v1/checkout/sessions') {
      const email = url.searchParams.get('customer_details[email]');
      return json(200, { data: Object.values(sessions).filter((s) => s.customer_details.email === email) });
    }
    if (req.method === 'GET' && url.pathname.startsWith('/v1/checkout/sessions/')) {
      const s = sessions[url.pathname.split('/').pop()];
      return s ? json(200, s) : json(404, { error: { message: 'No such session' } });
    }
    if (url.pathname === '/emails') { emails.push({ ...JSON.parse(raw), key: req.headers['idempotency-key'] }); return json(200, { id: 'em_1' }); }
    if (url.pathname === '/audiences/aud_1/contacts') { contacts.push(JSON.parse(raw)); return json(200, { id: 'c_1' }); }
    json(404, {});
  });
});

async function main() {
  await new Promise((r) => mock.listen(3101, r));
  const server = spawn('node', [path.join(__dirname, 'dev-server.js')], {
    env: { ...process.env, PORT: '3100', STRIPE_SECRET_KEY: 'sk_test_fake', STRIPE_API_BASE: MOCK, RESEND_API_KEY: 're_fake', RESEND_API_BASE: MOCK, RESEND_AUDIENCE_ID: 'aud_1', RESEND_FROM: 'Test <t@example.com>', ACCESS_TOKEN_SECRET: 'test-secret', SITE_URL: '' },
    stdio: 'inherit',
  });
  await new Promise((r) => setTimeout(r, 700));
  const browser = await chromium.launch();
  const errors = [];
  const shot = async (page, name, full = false) => { if (SHOTS) await page.screenshot({ path: path.join(SHOTS, name + '.png'), fullPage: full }); };
  let passed = 0;
  const step = async (name, fn) => { await fn(); passed++; console.log('  ✓ ' + name); };

  try {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 860 } });
    const page = await ctx.newPage();
    page.on('pageerror', (e) => errors.push(e.message));
    page.on('response', (r) => { if (r.status() >= 400 && r.url().startsWith(SITE) && !r.url().includes('/api/')) errors.push(`${r.status()} ${r.url()}`); });

    await step('home page shows books, packs and sign-up', async () => {
      await page.goto(SITE + '/');
      assert.match(await page.textContent('h1'), /first books in Spanish/);
      assert.ok((await page.locator('.book').count()) >= 8);
      assert.strictEqual(await page.locator('.pack').count(), 3);
      await page.waitForLoadState('networkidle');
      await shot(page, 'home', true);
    });

    await step('library filters by theme and level', async () => {
      await page.goto(SITE + '/libros/');
      assert.strictEqual(await page.locator('.book:visible').count(), BOOKS);
      await page.click('button[value="oceano"]');
      assert.strictEqual(await page.locator('.book:visible').count(), 8);
      await page.click('button[data-filter="level"][value="1"]');
      assert.ok((await page.locator('.book:visible').count()) < 8);
      await page.goto(SITE + '/libros/?tema=animales');
      assert.strictEqual(await page.locator('.book:visible').count(), 8);
      await page.waitForLoadState('networkidle');
      await shot(page, 'library');
    });

    await step('reader turns pages, plays audio, ends with vocabulary', async () => {
      await page.goto(SITE + '/libros/el-oso/');
      assert.strictEqual(await page.locator('.pg').count(), 9);
      assert.strictEqual(await page.locator('.pg:visible').count(), 1);
      await page.click('[data-next]');
      assert.match(await page.textContent('.pg.on .es'), /El oso es grande\./);
      await page.waitForLoadState('networkidle');
      await shot(page, 'reader');
      const audio = page.waitForResponse((r) => r.url().endsWith('/media/el-oso/page-01.mp3'));
      await page.click('[data-listen]');
      assert.ok((await audio).ok());
      const word = page.waitForResponse((r) => r.url().endsWith('/media/el-oso/word-grande.mp3'));
      assert.ok(await page.locator('[data-listen].playing').count(), 'listen button shows it is playing');
      await page.click('.pg.on .kw[data-word="grande"]');
      assert.ok((await word).ok());
      for (let i = 0; i < 6; i++) await page.click('[data-next]');
      assert.strictEqual(await page.locator('.pg.vocab.on .vcard').count(), 6);
      await shot(page, 'vocab');
      // Word game: tap the right picture for each word, six times.
      await page.click('[data-game]');
      for (let i = 0; i < 6; i++) {
        const word = (await page.textContent('[data-ask]')).match(/«(.+)»/)[1];
        const wrong = page.locator(`.vcard:not(.found):not([data-word="${word}"])`).first();
        if (await wrong.count()) await wrong.click();
        await page.click(`.vcard[data-word="${word}"]`);
        await page.waitForTimeout(800);
      }
      assert.match(await page.textContent('[data-ask]'), /Muy bien/);
      assert.strictEqual((await page.textContent('[data-stars]')).length, 6);
      await page.click('[data-next]');
      assert.match(await page.textContent('[data-read-count]'), /1 book read/);
      assert.ok(await page.locator('.pg.badge.on').isVisible());
      assert.ok(await page.locator('[data-next]').isDisabled());
      await shot(page, 'badge');
    });

    await step('finished books get a star in the library', async () => {
      await page.goto(SITE + '/libros/');
      assert.strictEqual(await page.locator('.book.done').count(), 1);
      assert.ok(await page.locator('[data-progress]').isVisible());
    });

    await step('email sign-up adds the parent to the list', async () => {
      await page.goto(SITE + '/#club');
      await page.fill('#su-email', 'not-an-email');
      await page.click('form[data-signup] button');
      await page.waitForSelector('.msg.bad');
      await page.fill('#su-name', 'Ana');
      await page.fill('#su-email', 'Ana@Example.com');
      await page.click('form[data-signup] button');
      await page.waitForSelector('.msg.ok');
      assert.deepStrictEqual(contacts, [{ email: 'ana@example.com', first_name: 'Ana', unsubscribed: false }]);
      assert.strictEqual(emails.length, 1, 'welcome email sent');
      assert.match(emails[0].html, /\/muestra\//);
      emails.length = 0;
    });

    await step('free sample printable has all 10 sheets', async () => {
      await page.goto(SITE + '/muestra/');
      assert.strictEqual(await page.locator('.sheet').count(), 10);
      await page.waitForLoadState('networkidle');
      await shot(page, 'print-sample', true);
    });

    await step('paid pack is locked without a purchase', async () => {
      const r = await page.goto(SITE + '/api/pack?product=pack-animales');
      assert.strictEqual(r.status(), 403);
      const forged = Buffer.from(JSON.stringify({ p: ['biblioteca'], e: '', t: 1 })).toString('base64url') + '.AAAA';
      assert.strictEqual((await page.goto(SITE + '/api/pack?product=pack-animales&t=' + forged)).status(), 403);
    });

    await step('buying a pack unlocks it and emails the link', async () => {
      await page.goto(SITE + '/packs/');
      await page.waitForLoadState('networkidle');
      await shot(page, 'packs', true);
      await page.click('#pack-animales [data-buy]');
      await page.waitForSelector('[data-status].ok');
      assert.strictEqual(sessions.cs_test_0.amount, '700');
      assert.ok(!page.url().includes('session_id'));
      assert.strictEqual(emails.length, 1);
      assert.strictEqual(emails[0].key, 'purchase-cs_test_0');
      await shot(page, 'thanks');
      const href = await page.getAttribute('[data-owned] a.btn', 'href');
      const r = await page.goto(SITE + href);
      assert.strictEqual(r.status(), 200);
      assert.strictEqual(await page.locator('.sheet').count(), 8 * 10 + 2);
      // That token must not open a different pack.
      assert.strictEqual((await page.goto(SITE + href.replace('pack-animales', 'pack-oceano'))).status(), 403);
      const one = await page.goto(SITE + href + '&book=el-gato');
      assert.strictEqual(one.status(), 200);
      assert.strictEqual(await page.locator('.sheet').count(), 10);
    });

    await step('my purchases remembers the pack and can email a restore link', async () => {
      await page.goto(SITE + '/mis-compras/');
      assert.strictEqual(await page.locator('[data-owned] .box').count(), 1);
      await page.fill('#re-email', 'parent@example.com');
      await page.click('form[data-restore] button');
      await page.waitForSelector('form[data-restore] .msg.ok');
      assert.strictEqual(emails.length, 2);
      const link = emails[1].html.match(/href="([^"]+)"/)[1];
      const fresh = await (await browser.newContext()).newPage();
      await fresh.goto(link);
      assert.strictEqual(await fresh.locator('[data-owned] .box').count(), 1);
      // Unknown email: same friendly answer, but no email is sent.
      await page.fill('#re-email', 'stranger@example.com');
      await page.click('form[data-restore] button');
      await page.waitForTimeout(400);
      assert.strictEqual(emails.length, 2);
    });

    await step('the full library unlocks every pack', async () => {
      await page.goto(SITE + '/packs/');
      await page.click('.bundle [data-buy]');
      await page.waitForSelector('[data-status].ok');
      assert.strictEqual(await page.locator('[data-owned] .box').count(), PACKS);
    });

    await step('a school licence unlocks every pack too', async () => {
      const school = await (await browser.newContext()).newPage();
      await school.goto(SITE + '/packs/');
      await school.click('#escuela [data-buy]');
      await school.waitForSelector('[data-status].ok');
      assert.strictEqual(await school.locator('[data-owned] .box').count(), PACKS);
      const r = await school.goto(SITE + (await school.getAttribute('[data-owned] a.btn', 'href')));
      assert.match(await school.textContent('.toolbar'), /School licence/);
      assert.strictEqual(r.status(), 200);
    });

    await step('theme page lists its books, words and pack', async () => {
      await page.goto(SITE + '/temas/animales/');
      assert.strictEqual(await page.locator('.book').count(), 8);
      assert.ok((await page.locator('.wordlist li').count()) > 20);
      assert.strictEqual(await page.locator('[data-buy="pack-animales"]').count(), 1);
      await page.waitForLoadState('networkidle');
      await shot(page, 'theme', true);
    });

    await step('phone layout works', async () => {
      const phone = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
      const m = await phone.newPage();
      await m.goto(SITE + '/libros/la-mariposa/');
      await m.click('[data-next]');
      const overflow = await m.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
      assert.strictEqual(overflow, false);
      await m.waitForLoadState('networkidle');
      await shot(m, 'phone-reader');
      await m.goto(SITE + '/');
      assert.strictEqual(await m.evaluate(() => document.documentElement.scrollWidth > window.innerWidth), false);
      await m.waitForLoadState('networkidle');
      await shot(m, 'phone-home');
    });

    assert.deepStrictEqual(errors, [], 'no page errors or broken files');
    console.log(`\nAll ${passed} checks passed.`);
  } finally {
    await browser.close();
    server.kill();
    mock.close();
  }
}

main().catch((e) => { console.error('\nFAILED:', e.message); process.exit(1); });
