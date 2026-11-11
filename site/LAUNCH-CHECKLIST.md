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
- [ ] **Decide the prices** in `site/site.config.json` (now $7 per pack, $39 for everything).

## 2. Book quality (the product itself)

- [ ] **Native-speaker review of all 106 books.** I corrected 21 pages
      (see `site/data/text-fixes.json`), but a teacher should read every book once before it is sold.
- [ ] **Re-record audio for corrected pages.** These 21 pages and 4 words now use the
      device's built-in Spanish voice because the old recording no longer matches the text:
      - `frutas-y-verduras` page 1: “La manzana es roja.”
      - `frutas-y-verduras` page 2: “El plátano es amarillo.”
      - `frutas-y-verduras` page 3: “La pera es verde.”
      - `frutas-y-verduras` page 4: “La zanahoria es anaranjada.”
      - `frutas-y-verduras` page 5: “El brócoli es verde.”
      - `frutas-y-verduras` page 6: “El tomate es rojo.”
      - `el-perro` page 1: “El perro es mi amigo.”
      - `el-conejo` page 3: “El conejo come zanahorias.”
      - `el-desayuno` page 5: “El jugo es de naranja.”
      - `las-bebidas` page 2: “El jugo es de manzana.”
      - `el-huevo` page 2: “El huevo es ovalado.”
      - `el-yogur` page 3: “El yogur es bueno para mí.”
      - `el-vapor` page 3: “El vapor es agua en forma de gas.”
      - `la-hermana` page 3: “Mi hermana me ayuda.”
      - `la-hermana` page 4: “Mi hermana es divertida.”
      - `la-hermana` page 5: “Mi hermana es mi amiga.”
      - `el-hermano` page 3: “Mi hermano es valiente.”
      - `el-hermano` page 4: “Mi hermano construye.”
      - `el-hermano` page 5: “Mi hermano es mi amigo.”
      - `compartir` page 4: “Compartir nos hace felices.”
      - `escuchar` page 5: “Escuchar me ayuda a aprender.”
      - word `el-conejo`: “zanahorias”
      - word `el-huevo`: “ovalado”
      - word `el-hielo`: “congelada”
      - word `el-vapor`: “gas”
- [ ] **Six missing pictures.** These pages show a coloured panel with an emoji instead of a picture:
      `la-rosa` page 2, `el-girasol` page 5, `el-cactus` page 4, `el-tulipan` page 6, `escuchar` page 3, `reir` page 2.
- [ ] **Pick one art style.** 76 books use photos and 30 use watercolour illustrations
      (`la-hormiga`, `el-yogur`, `el-cuadrado`, `el-triangulo`, `el-sol`, `la-luna`, …). The body, nature and numbers packs are illustrated;
      the rest are photos. Either is fine within a pack, but the brand promise says "real photos".
- [ ] **Print quality.** Pictures are 1024 pixels wide. That is fine for home printing, too soft
      for a professionally printed book. Regenerate or upscale to at least 2400 pixels before
      Amazon KDP or a print shop.
- [ ] **Finish the 28 written books** (weeks 98–135: music, my world, transport, seasons).
      They need pictures and audio. That adds three more packs.
- [ ] **Reading progression.** 19 books are Nivel 1, 74 are Nivel 2 and only 13 are Nivel 3.
      Write more Nivel 3 books with questions (¿Dónde está…?), and a few simple stories with a
      beginning, middle and end.
- [ ] **Word-by-word highlighting.** The audio is one clip per page. Recording with word timings
      would let each word light up as it is read, which is the strongest read-along feature.
- [ ] **Syllable pages** (ma-me-mi-mo-mu). Spanish reading is taught by syllables; a short
      "Sílabas" series would make this a real reading programme, not only vocabulary.

## 3. Moving off the old site

- [ ] **Redirect the old pages.** Each `beibeiamigos.com/spanish-books/<book>/` page should
      forward (301) to the new `/libros/<book>/` page so Google ranking carries over.
- [ ] **Keep one page on the school site** ("Free Spanish Books") that links to the new site.
- [ ] **Turn off the old hosts** (Render and GitHub Pages) once redirects work.
- [ ] **Stop the nightly agent in `preschool-books`.** It has republished the same 12 titles
      about 9 times each. Keep its 36 unique stories as raw material for Nivel 3.
- [ ] **Submit the sitemap** in Google Search Console after `SITE_URL` is set.

## 4. Making it profitable

- [ ] **Welcome emails.** Sign-up only adds the parent to the list. Write a 3-email welcome
      series in Resend (free book → how to read together → first pack offer).
- [ ] **Weekly email.** One new or featured book each week, sent as a Resend Broadcast.
- [ ] **Launch to school families first.** Give current Beibei Amigos families a discount code
      (checkout already accepts Stripe promotion codes) and ask for honest reviews.
- [ ] **Reviews on the packs page.** There are none yet, so the page has no social proof.
- [ ] **Pinterest and Teachers Pay Teachers.** Printable Spanish packs sell well on both;
      list the same packs there and link back.
- [ ] **School licence.** Add a "for schools" product (several classrooms) at a higher price.
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
