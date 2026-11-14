# Publish all Beibei Spanish books

Date: 2026-08-16
Branch: `hermes/spanish-books-publish-all`

## Goal

Make every publication-ready book discoverable on the Beibei Amigos WordPress library and make future ready books publish idempotently without exposing asset-incomplete drafts.

## Ground truth

- Canonical source: this `Spanish-Books` repository.
- Source folders: 172.
- Explicitly ready modern books in `server.js`: 106.
- Self-contained legacy books: 36.
- Ready total: 142.
- Asset-incomplete modern drafts: 30 (`week-98`–`week-111`, `week-120`–`week-135`).
- Live WordPress book child pages under page 1854: 140, all published.
- Ready source folders represented live: 140.
- Ready source folders missing because their tail slugs collide with existing books:
  - `week-33-las-emociones` → `las-emociones-semana-33`
  - `week-71-la-familia` → `la-familia-semana-71`
- Public library hub currently lists 106 cards, so 34 existing live books are not discoverable there.
- The disconnected `~/Projects/preschool-books` nightly output is excluded: 87/115 drafts are fallback-template books, only 38 tail slugs are unique, and its GitHub Pages URL is 404.

## Architecture

1. Add a checked-in catalog module that combines:
   - explicit `ready: true` entries from `server.js`, and
   - an explicit allowlist of the 36 reviewed self-contained legacy books.
2. Add a fail-closed WordPress sync command:
   - dry-run by default;
   - source-folder identity markers, not title-only matching;
   - deterministic collision slugs;
   - public-reader reachability and local readiness checks;
   - authenticated WordPress inventory via one WP-CLI PHP boot;
   - backup hub `content.raw` before any mutation;
   - create missing pages as drafts, publish after validation, then update the hub;
   - optimistic concurrency on the hub modification timestamp;
   - JSON receipt and rollback instructions.
3. Generate the Beibei hub from the full ready catalog with 142 cards, filtering/search, Book/ItemList/Breadcrumb schema, and no Sophia promotion.
4. Extend `publish_next_week.py` so successful future creation calls the same sync command after the reader is public/ready; direct WordPress writes remain fail-closed if source or credentials are unavailable.
5. Replace the disconnected nightly fallback generator with a no-agent ready-book sync only after local/live verification.

## Files

- `scripts/book_catalog.py` — ready catalog and collision mapping.
- `scripts/sync_wordpress_books.py` — inventory, preview, backup, apply, receipt.
- `scripts/publish_next_week.py` — call sync after a ready book is created.
- `scripts/update_wp_library.py` — replace stale hard-coded path with the shared sync generator.
- `tests/verify_wordpress_book_sync.py` — catalog, collision, idempotency, fail-closed and rollback tests.
- `docs/plans/2026-08-16-publish-all-beibei-books.md` — this plan.

## Apply order

1. Build/test catalog and dry-run sync.
2. Generate local hub and missing-page previews.
3. Render desktop/mobile previews and check overflow, reader URLs, schema and Sophia absence.
4. Save live hub/page inventory backup.
5. Create two missing pages and update the hub.
6. Verify 142 published children, 142 source identities, live HTTP 200, iframe reader reachability and hub card count.
7. Install/verify the no-agent sync schedule; immediately run once and prove an idempotent no-op.
8. Push the feature branch and open a review PR. Do not push or merge `main`.

## Rollback

- Restore hub page 1854 from the timestamped pre-write `content.raw` backup.
- Move newly created page IDs back to draft using the apply receipt; do not delete them.
- Disable/pause the auto-sync job.
- Static reader files and the prior 140 pages remain untouched.

## Honest completion labels

- `LIVE`: WordPress page exists, returns 200, reader loads, and hub links it.
- `AUTO-PUBLISH ACTIVE`: scheduled no-agent sync has a successful run plus idempotent no-op replay.
- `GATED`: one of the 30 asset-incomplete source folders; not published until readiness passes.
- `PR OPEN`: code pushed for review but not merged to `main`.
