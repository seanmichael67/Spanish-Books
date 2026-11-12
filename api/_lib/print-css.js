/* Styles for the printable books (US Letter, landscape). Kept as a string so
   the same styles work in the static free sample and in the paid /api/pack page. */
module.exports = `
@page { size: 11in 8.5in; margin: 0; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; background: #e9e4da; font-family: 'Andika', 'Trebuchet MS', Verdana, sans-serif; color: #1f2a44; }
.toolbar { position: sticky; top: 0; z-index: 5; background: #1f2a44; color: #fff; padding: 12px 18px; display: flex; gap: 14px; align-items: center; flex-wrap: wrap; font-family: 'Fredoka', 'Trebuchet MS', sans-serif; }
.toolbar strong { font-size: 1.05rem; }
.toolbar span { opacity: .8; font-size: .9rem; flex: 1; min-width: 200px; }
.toolbar button, .toolbar a { background: #ffc93c; color: #1f2a44; border: 0; border-radius: 999px; padding: 10px 20px; font: inherit; font-weight: 600; cursor: pointer; text-decoration: none; }
.toolbar a { background: transparent; color: #fff; border: 1.5px solid rgba(255,255,255,.5); }
.sheet { width: 11in; height: 8.5in; margin: 18px auto; background: #fff; position: relative; overflow: hidden; padding: .5in; display: flex; flex-direction: column; box-shadow: 0 6px 24px rgba(0,0,0,.18); page-break-after: always; break-after: page; }
.sheet:last-child { page-break-after: auto; break-after: auto; }
.foot { position: absolute; left: .5in; right: .5in; bottom: .22in; display: flex; justify-content: space-between; font-size: 8.5pt; color: #8a8fa3; }
.band { position: absolute; left: 0; top: 0; bottom: 0; width: .18in; background: var(--c, #ff6b4a); }
h1, h2, h3 { font-family: 'Fredoka', 'Trebuchet MS', sans-serif; margin: 0; }

.pic { background: #f6f1e7; border-radius: .22in; overflow: hidden; display: flex; align-items: center; justify-content: center; }
.pic img { width: 100%; height: 100%; object-fit: cover; display: block; }
.pic.empty { font-size: 110pt; background: color-mix(in srgb, var(--c, #ff6b4a) 16%, #fff); }

.cover { align-items: center; justify-content: center; text-align: center; gap: .16in; }
.cover h1 { font-size: 50pt; line-height: 1.05; }
.cover .en { font-size: 18pt; color: #5b6480; }
.chip { display: inline-block; background: color-mix(in srgb, var(--c, #ff6b4a) 18%, #fff); border-radius: 999px; padding: 4px 16px; font-size: 11pt; font-family: 'Fredoka', sans-serif; font-weight: 600; }

.story { flex-direction: row; gap: .4in; align-items: center; }
.story .pic { flex: 0 0 auto; }
.story .words { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: .3in; padding-bottom: .3in; }
.story .es { font-size: 40pt; line-height: 1.25; font-weight: 700; letter-spacing: .01em; }
.story .syl { font-size: 84pt; line-height: 1; font-weight: 700; color: var(--c, #ff6b4a); }
.story .es b { color: var(--c, #ff6b4a); font-weight: 700; }
.story .en { font-size: 15pt; color: #6b728c; border-top: 2px dotted #d5d0c4; padding-top: .16in; }

.sheet > h2 { font-size: 26pt; margin-bottom: .05in; }
.sheet > .sub { font-size: 12pt; color: #6b728c; margin-bottom: .2in; }
.grid6 { flex: 1; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(2, 1fr); gap: .22in; padding-bottom: .25in; min-height: 0; }
.card { border: 2.5px solid color-mix(in srgb, var(--c, #ff6b4a) 55%, #fff); border-radius: .2in; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: .12in; text-align: center; min-height: 0; }
.card .pic { width: 100%; flex: 1; min-height: 0; margin-bottom: .08in; }
.card .pic.emoji { font-size: 54pt; background: color-mix(in srgb, var(--c, #ff6b4a) 12%, #fff); }
.card .w { font-size: 24pt; font-weight: 700; line-height: 1.1; }
.card .t { font-size: 11pt; color: #6b728c; }
.cut .card { border: 2px dashed #9aa0b5; border-radius: 0; }
.cut .grid6 { gap: 0; }

.trace { display: grid; grid-template-columns: 1fr 1fr; gap: .1in .5in; flex: 1; align-content: start; }
.trace .row { border-bottom: 2px solid #c9cfdf; background: linear-gradient(to bottom, transparent 49%, #e3e7f2 49%, #e3e7f2 51%, transparent 51%); height: .95in; display: flex; align-items: flex-end; gap: .3in; padding: 0 .1in; }
.trace .row span { font-size: 46pt; line-height: .95in; color: #c3c8d6; font-weight: 400; letter-spacing: .06em; white-space: nowrap; }
.trace .row small { font-size: 10pt; color: #8a8fa3; margin-left: auto; padding-bottom: 6px; white-space: nowrap; }
.talk { margin: .16in 0 .28in; background: #fff7e0; border-radius: .16in; padding: .14in .2in; font-size: 11.5pt; line-height: 1.45; }
.talk b { font-family: 'Fredoka', sans-serif; }

.guide { font-size: 12.5pt; line-height: 1.5; }
.guide h1 { font-size: 30pt; margin-bottom: .12in; }
.guide .cols { display: grid; grid-template-columns: 1fr 1fr; gap: .2in .45in; flex: 1; align-content: start; }
.guide h3 { font-size: 14pt; margin-bottom: 2px; color: var(--c, #ff6b4a); }
.guide p { margin: 0; }
.plan { width: 100%; border-collapse: collapse; margin: .12in 0 .16in; font-size: 12pt; }
.plan th, .plan td { text-align: left; vertical-align: top; padding: .09in .12in; border-bottom: 1.5px solid #e6e1d6; }
.plan th { white-space: nowrap; color: var(--c, #ff6b4a); font-family: 'Fredoka', sans-serif; width: 2.1in; }
.toc { columns: 2; margin: .1in 0 0; padding-left: 1.2em; font-size: 13pt; line-height: 1.7; }

.cert { align-items: center; justify-content: center; text-align: center; gap: .14in; border: .14in solid color-mix(in srgb, var(--c, #ff6b4a) 60%, #fff); }
.cert .medal { font-size: 80pt; line-height: 1; }
.cert h1 { font-size: 38pt; }
.cert .line { width: 5in; border-bottom: 2px solid #1f2a44; height: .55in; }
.cert p { margin: 0; font-size: 14pt; color: #5b6480; }
.stars { display: flex; gap: .12in; flex-wrap: wrap; justify-content: center; max-width: 8in; }
.stars div { width: .95in; font-size: 8.5pt; color: #5b6480; line-height: 1.2; }
.stars div i { display: block; font-style: normal; font-size: 26pt; color: #d9dce6; }

@media print {
  html, body { background: #fff; }
  .toolbar { display: none !important; }
  .sheet { margin: 0; box-shadow: none; }
}
`;
