# Marketing kit

Everything here is made from the real books and prices by two scripts, so it
stays accurate. Re-run them after adding books or changing prices.

| What | Where | Made by |
|---|---|---|
| Pinterest pins (1000x1500) | `pins/` (also served at `/pins/` on the site and used as share images) | `python3 site/scripts/make-pins.py` |
| Square covers for Teachers Pay Teachers | `tpt/` | `python3 site/scripts/make-pins.py` |
| Pinterest bulk-upload sheet | `pinterest-pins.csv` | `node site/scripts/make-marketing.js https://your-site` |
| Teachers Pay Teachers titles, descriptions and tags | `tpt-listings.md` | same |
| Four weekly book-club emails | `emails/` | same |
| A PDF of every printable pack | `pdfs/` (not committed) | `node site/scripts/make-pdfs.js` |

Run `make-marketing.js` with your real address once the site is live, so every
link in the sheet, listings and emails points to it.

## Pinterest

Pinterest → Create → **Create Pins in bulk** → upload `pinterest-pins.csv`. The
pin pictures must already be live at `https://your-site/pins/…` (they are, once
the site is deployed). Make a board called "Spanish Books for Kids" first.

## Teachers Pay Teachers

1. Make the PDFs: `node site/build.js && node site/scripts/make-pdfs.js` (about a minute per pack; each is about 6 MB).
2. For each product in `tpt-listings.md`: upload the PDF, the cover from `tpt/`, and paste the title, description and tags.
3. For the bundle, zip all the PDFs into one file.

Check TpT's current seller terms and fees before listing; the licence on TpT is
TpT's own, so the school licence on our site is a separate, cheaper option for
whole schools.
