# Beibei Libros: the Spanish books website

This folder is the new website for the Spanish books. It replaces the old
WordPress + iframe setup with one fast site that you host on Vercel.

**What it does**

- Shows all 106 finished books as real web pages (good for Google), with audio.
- Ends every book with a picture vocabulary page and a badge.
- Collects parent emails (book club) and gives a free printable book.
- Sells printable packs through Stripe and unlocks them after payment.

## How it is organised

| Path | What it is |
|---|---|
| `site/data/books.json` | Every book's words, pictures and vocabulary. **The source of truth.** |
| `site/data/text-fixes.json` | Spanish corrections applied on top of the original books. |
| `site/data/themes.json` | The themes (Animals, Food, …) and their colours. |
| `site/site.config.json` | Site name, prices, contact email, Google Analytics ID. |
| `site/build.js` | Turns the data into the website (`site/dist`). |
| `site/src/` | The look (CSS) and behaviour (JavaScript) of the site. |
| `api/` | Small server functions: checkout, email sign-up, unlocking packs. |
| `api/_lib/print.js` | The layout of the printable books. |
| `books/` | The original books. Pictures and audio are copied from here. |

## Try it on your computer

```bash
npm run dev
```

Then open http://localhost:3000. Reading works right away. Buying and email
sign-up answer "not open yet" until you add the keys below.

To run the automatic test (it uses a pretend Stripe, so no real money):

```bash
npm install --no-save playwright
```

```bash
npm test
```

## Put it online (Vercel)

1. Go to vercel.com → **Add New… → Project** → import the `Spanish-Books` repository.
2. Leave every build setting alone. `vercel.json` already tells Vercel what to do.
3. Add the **Environment Variables** below (Project → Settings → Environment Variables).
4. Press **Deploy**.
5. Add your domain under Project → Settings → Domains, then set `SITE_URL` to it and redeploy.

### Environment variables

| Name | Where it comes from | Needed for |
|---|---|---|
| `SITE_URL` | Your address, e.g. `https://libros.beibeiamigos.com` | Google links, sitemap |
| `ACCESS_TOKEN_SECRET` | Make up a long random password (40+ characters). Never change it afterwards or old purchase links stop working. | Unlocking packs |
| `STRIPE_SECRET_KEY` | Stripe dashboard → Developers → API keys (`sk_test_…` first, `sk_live_…` when ready) | Selling |
| `RESEND_API_KEY` | resend.com → API Keys | Email |
| `RESEND_AUDIENCE_ID` | resend.com → Audiences → your list | Book club sign-up |
| `RESEND_FROM` | e.g. `Beibei Libros <hola@yourdomain.com>` (the domain must be verified in Resend) | Purchase and restore emails |

Never put these keys in a file in this repository. They only go in Vercel.

### Test a purchase before going live

Use a `sk_test_…` Stripe key, buy a pack with card number `4242 4242 4242 4242`,
any future date and any CVC. You should land on the thank-you page and be able
to print. When that works, swap in the `sk_live_…` key.

## Everyday jobs

- **Fix a typo in a book:** add it to `site/data/text-fixes.json`, then run `npm run import-books`.
- **Change a price or the site name:** edit `site/site.config.json`.
- **Add a new finished book:** add it to the `BOOKS` list in `server.js` (as before), then run
  `npm run import-books` and `python3 site/scripts/make-thumbs.py`.
- A theme becomes a printable pack automatically once it has 8 books.

See `site/LAUNCH-CHECKLIST.md` for what is still missing before launch.
