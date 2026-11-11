#!/usr/bin/env node
/** Dependency-free Chrome DevTools smoke test for the local WP preview. */
import fs from 'node:fs/promises';
import path from 'node:path';

const targetUrl = process.argv[2] || 'http://127.0.0.1:4179/preview.html';
const outDir = process.argv[3] || '/tmp/spanish-books-wp/preview/screenshots';
const debugPort = process.env.CHROME_DEBUG_PORT || '9222';

class CDP {
  constructor(url) {
    this.nextId = 1;
    this.pending = new Map();
    this.waiters = new Map();
    this.events = [];
    this.ready = new Promise((resolve, reject) => {
      this.ws = new WebSocket(url);
      this.ws.onopen = resolve;
      this.ws.onerror = reject;
      this.ws.onmessage = (event) => this.onMessage(event.data);
    });
  }
  onMessage(raw) {
    const message = JSON.parse(raw);
    if (message.id) {
      const pending = this.pending.get(message.id);
      if (!pending) return;
      this.pending.delete(message.id);
      if (message.error) pending.reject(new Error(JSON.stringify(message.error)));
      else pending.resolve(message.result);
      return;
    }
    this.events.push(message);
    const waiters = this.waiters.get(message.method) || [];
    this.waiters.delete(message.method);
    for (const waiter of waiters) waiter(message.params);
  }
  async send(method, params = {}) {
    await this.ready;
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }
  wait(method, timeoutMs = 15000) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error(`Timed out waiting for ${method}`)), timeoutMs);
      const wrapped = (params) => { clearTimeout(timer); resolve(params); };
      const waiters = this.waiters.get(method) || [];
      waiters.push(wrapped);
      this.waiters.set(method, waiters);
    });
  }
  close() { this.ws.close(); }
}

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function connect() {
  const targets = await fetch(`http://127.0.0.1:${debugPort}/json/list`).then(r => r.json());
  const page = targets.find(target => target.type === 'page');
  if (!page) throw new Error('No Chrome page target is available');
  return new CDP(page.webSocketDebuggerUrl);
}

async function evaluate(client, expression) {
  const result = await client.send('Runtime.evaluate', {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.exception?.description || 'Runtime evaluation failed');
  }
  return result.result.value;
}

async function navigate(client, url) {
  const loaded = client.wait('Page.loadEventFired');
  await client.send('Page.navigate', { url });
  await loaded;
  await sleep(2500);
}

async function screenshot(client, filename) {
  const metrics = await client.send('Page.getLayoutMetrics');
  const size = metrics.cssContentSize;
  const capture = await client.send('Page.captureScreenshot', {
    format: 'png',
    captureBeyondViewport: true,
    clip: {
      x: 0,
      y: 0,
      width: Math.min(size.width, 1600),
      height: Math.min(size.height, 12000),
      scale: 1,
    },
  });
  await fs.writeFile(filename, Buffer.from(capture.data, 'base64'));
}

function assertions(metrics, expectedViewport) {
  const failures = [];
  const check = (condition, message) => { if (!condition) failures.push(message); };
  check(metrics.parentOverflow <= expectedViewport, `parent overflow ${metrics.parentOverflow} > ${expectedViewport}`);
  check(metrics.frameOverflow <= metrics.frameClientWidth + 1, `iframe overflow ${metrics.frameOverflow} > ${metrics.frameClientWidth}`);
  check(metrics.h1 === 'Pick a story.Read together.', `unexpected H1: ${metrics.h1}`);
  check(metrics.themeButtons === 15, `expected 15 populated theme buttons, got ${metrics.themeButtons}`);
  check(metrics.visibleCards === 8, `expected 8 initial Animals books, got ${metrics.visibleCards}`);
  check(metrics.totalCards === 106, `expected 106 total books, got ${metrics.totalCards}`);
  check(metrics.brokenCovers === 0, `${metrics.brokenCovers} visible covers failed to load`);
  check(metrics.searchPresent, 'search input missing');
  return failures;
}

async function pageMetrics(client) {
  return evaluate(client, `(() => {
    const frame = document.querySelector('#booksFrame');
    const doc = frame && frame.contentDocument;
    if (!frame || !doc) return { error: 'same-origin preview iframe unavailable' };
    const visible = [...doc.querySelectorAll('.card')].filter(card => getComputedStyle(card).display !== 'none');
    const covers = visible.map(card => card.querySelector('.card-cover')).filter(Boolean);
    return {
      viewport: innerWidth,
      parentOverflow: document.documentElement.scrollWidth,
      frameWidth: frame.getBoundingClientRect().width,
      frameHeight: frame.getBoundingClientRect().height,
      frameClientWidth: doc.documentElement.clientWidth,
      frameOverflow: doc.documentElement.scrollWidth,
      h1: (doc.querySelector('h1')?.textContent || '').replace(/\\s+/g, ' ').trim(),
      resultStatus: doc.querySelector('#resultsStatus')?.textContent,
      searchPresent: Boolean(doc.querySelector('#bookSearch')),
      themeButtons: doc.querySelectorAll('.theme-btn').length,
      totalCards: doc.querySelectorAll('.card').length,
      visibleCards: visible.length,
      brokenCovers: covers.filter(img => img.complete && img.naturalWidth === 0).length,
      loadedCovers: covers.filter(img => img.complete && img.naturalWidth > 0).length,
      mobileCardDisplay: visible[0] ? getComputedStyle(visible[0]).display : null,
    };
  })()`);
}

async function interactionMetrics(client) {
  return evaluate(client, `(async () => {
    const doc = document.querySelector('#booksFrame').contentDocument;
    const input = doc.querySelector('#bookSearch');
    const visibleCount = () => [...doc.querySelectorAll('.card')].filter(card => getComputedStyle(card).display !== 'none').length;
    const fireInput = value => { input.value = value; input.dispatchEvent(new Event('input', { bubbles: true })); };
    fireInput('oso');
    await new Promise(resolve => setTimeout(resolve, 80));
    const search = { visible: visibleCount(), status: doc.querySelector('#resultsStatus').textContent };
    fireInput('');
    const all = doc.querySelector('[data-filter="todos"]');
    all.click();
    await new Promise(resolve => setTimeout(resolve, 80));
    const allBooks = { visible: visibleCount(), pressed: all.getAttribute('aria-pressed') };
    fireInput('not-a-real-book');
    await new Promise(resolve => setTimeout(resolve, 80));
    const empty = { visible: visibleCount(), display: getComputedStyle(doc.querySelector('#noBooks')).display };
    fireInput('');
    doc.querySelector('[data-filter="animales"]').click();
    return { search, allBooks, empty };
  })()`);
}

async function main() {
  await fs.mkdir(outDir, { recursive: true });
  const client = await connect();
  await Promise.all([
    client.send('Page.enable'),
    client.send('Runtime.enable'),
    client.send('Log.enable'),
    client.send('Network.enable'),
  ]);

  const report = { url: targetUrl, desktop: {}, mobile: {}, interactions: {}, errors: [], screenshots: {} };

  await client.send('Emulation.setDeviceMetricsOverride', {
    width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false,
  });
  await navigate(client, targetUrl);
  report.desktop = await pageMetrics(client);
  const desktopPath = path.join(outDir, 'spanish-library-desktop.png');
  await screenshot(client, desktopPath);
  report.screenshots.desktop = desktopPath;
  report.interactions = await interactionMetrics(client);

  await client.send('Emulation.setDeviceMetricsOverride', {
    width: 390, height: 844, deviceScaleFactor: 1, mobile: true,
  });
  await navigate(client, `${targetUrl}?mobile=1`);
  report.mobile = await pageMetrics(client);
  const mobilePath = path.join(outDir, 'spanish-library-mobile.png');
  await screenshot(client, mobilePath);
  report.screenshots.mobile = mobilePath;

  const runtimeErrors = client.events
    .filter(event => event.method === 'Runtime.exceptionThrown')
    .map(event => event.params.exceptionDetails?.exception?.description || event.params.exceptionDetails?.text);
  const logErrors = client.events
    .filter(event => event.method === 'Log.entryAdded' && event.params.entry.level === 'error')
    .map(event => event.params.entry.text)
    .filter(text => !/google-analytics|googletagmanager/i.test(text));
  report.errors = [...runtimeErrors, ...logErrors];

  const failures = [
    ...assertions(report.desktop, 1440),
    ...assertions(report.mobile, 390),
  ];
  if (report.desktop.error) failures.push(report.desktop.error);
  if (report.mobile.error) failures.push(report.mobile.error);
  if (report.interactions.search?.visible !== 1) failures.push('search for oso did not return exactly one Animals book');
  if (report.interactions.allBooks?.visible !== 106) failures.push('All filter did not show 106 books');
  if (report.interactions.allBooks?.pressed !== 'true') failures.push('All filter aria-pressed state did not update');
  if (report.interactions.empty?.visible !== 0 || report.interactions.empty?.display === 'none') failures.push('empty-search state did not render');
  if (report.errors.length) failures.push(`${report.errors.length} browser error(s) detected`);
  report.failures = failures;

  const reportPath = path.join(outDir, 'browser-smoke-report.json');
  await fs.writeFile(reportPath, JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
  client.close();
  process.exitCode = failures.length ? 1 : 0;
}

main().catch(error => {
  console.error(error.stack || error);
  process.exitCode = 1;
});
