# Launch checklist: what is still missing

Written after building the new site. Items are in the order I would do them.
"You" means a job only a person can do; the rest can be done in code.

## 1. Before the site can take money (you)

- [ ] **Replace the Google API key.** A key sat in `IMPROVED-BOOK-CODE.html` in this public
      repository since March. It is now removed from the file, but it is still in the
      history, so it must be deleted and re-created in the Google Cloud console.
- [ ] **Choose the address.** A subdomain such as `libros.beibeiamigos.com` is the fastest;
      a new brand domain is better if you want to sell to other schools later.
- [ ] **Create the Vercel project** and add the environment variables (see `site/README.md`).
- [ ] **Stripe account:** finish business verification, set the public business name and
      support email, and switch on Stripe Tax if your accountant says you must collect
      sales tax on digital goods.
- [ ] **Resend account:** verify your sending domain and create one Audience for the book club.
- [ ] **Have the Privacy and Terms pages reviewed.** They are honest plain-language drafts, not legal advice.
- [ ] **Decide the prices** in `site/site.config.json` (now $7 per pack, $39 for everything, $149 for a school).

## 2. Book quality (the product itself)

Done since the first version: audio for every page and word of every book (including the
corrected pages), the six missing pictures, and new photo pictures for all 30 unfinished books.
All 136 theme books are on the site.

- [ ] **Pictures for the syllable series.** Eight "Sílabas" books (vowels, M, P, S, L, T, N, D)
      are written and have audio, but need 56 pictures. Descriptions are in
      `site/data/image-prompts.json` under `silabas-…`. For each cover (page 0) leave out the
      "No text, no letters" part of the style, because the cover shows letter blocks. Save with
      `site/scripts/save-image.py`, then run `npm run import-books`. The books and their pack
      appear automatically.
- [ ] **Native-speaker review of every book.** I corrected the mistakes I found
      (see `site/data/text-fixes.json`), but a teacher should read each book once before it is sold.
- [ ] **Pick one art style.** The 30 newest books and most older ones are photos. About 30 older
      books (body, nature, numbers) are watercolour illustrations. Either is fine within a pack,
      but the brand promise says "real photos". New pictures cost about half a Higgsfield credit each.
- [ ] **Print quality of older books.** New pictures are 1600 pixels wide (good for printing).
      The first 106 books are 1024 pixels: fine at home, soft for a print shop or Amazon KDP.
- [ ] **Reading progression.** Most books are Nivel 2. Write more Nivel 3 books with questions
      (¿Dónde está…?), and a few simple stories with a beginning, middle and end.
- [ ] **Word-by-word highlighting.** The audio is one clip per page. Recording with word timings
      would let each word light up as it is read, which is the strongest read-along feature.
- [ ] **Syllable pages** (ma-me-mi-mo-mu). Spanish reading is taught by syllables; a short
      "Sílabas" series would make this a real reading programme, not only vocabulary.

## 3. Moving off the old site

- [ ] **Redirect the old pages.** Run `node site/scripts/make-redirects.js https://your-new-address`
      and load `site/old-site-redirects.csv` into a WordPress redirect plugin, so each old book
      page forwards (301) to its new page and Google ranking carries over.
- [ ] **Keep one page on the school site** ("Free Spanish Books") that links to the new site.
- [ ] **Turn off the old hosts** (Render and GitHub Pages) once redirects work.
- [ ] **Stop the nightly agent in `preschool-books`.** It has republished the same 12 titles
      about 9 times each. Keep its 36 unique stories as raw material for Nivel 3.
- [ ] **Submit the sitemap** in Google Search Console after `SITE_URL` is set.

## 4. Making it profitable

- [ ] **Follow-up emails.** Sign-up now sends one welcome email with the free book. Add two
      more in Resend a few days apart (how to read together → first pack offer).
- [ ] **Weekly email.** One new or featured book each week, sent as a Resend Broadcast.
- [ ] **Launch to school families first.** Give current Beibei Amigos families a discount code
      (checkout already accepts Stripe promotion codes) and ask for honest reviews.
- [ ] **Reviews on the packs page.** There are none yet, so the page has no social proof.
- [ ] **Pinterest and Teachers Pay Teachers.** Printable Spanish packs sell well on both;
      list the same packs there and link back.
- [ ] **Sell the school licence.** It exists on the packs page ($149). Email it to preschool
      directors and Spanish-immersion schools you know.
- [ ] **Subscription.** Everything is a one-time purchase today. A yearly "new pack every
      month" plan needs a Stripe webhook and is the next build once packs are selling.
- [ ] **Cookie notice.** Google Analytics loads on every page. Add a consent banner if you
      advertise to visitors in the EU, UK or California.
- [ ] **Mandarin track.** The same site can host a second language once Spanish is earning.

## 5. Known limits of this first version

- Purchases are remembered in the browser and by an emailed link, not by an account with a password.
- A buyer could share their link. This is normal for low-priced printables; the buyer's email is printed on each pack.
- Refunds are handled by hand in the Stripe dashboard. A refunded buyer keeps their link.
- The Stripe and Resend connections were tested against stand-ins, not the real services.
  Do one real test purchase (see `site/README.md`) before announcing.
