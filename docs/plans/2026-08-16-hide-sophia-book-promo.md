# Hide Sophia promo from Spanish book pages

## Goal
Remove the visible Sophia AI Spanish Teacher promotion from every individual Spanish book page until Sophia is parent-ready.

## Scope
- Add `tools/hide_sophia_book_promo.py` as an idempotent bulk transformer.
- Remove the Sophia card, URL, and readiness claim from all `books/week-*/index.html` pages.
- Rebalance the remaining upsell cards from three desktop columns to two.
- Preserve the existing social-sharing block, book content, navigation, school links, and social-preview metadata.
- Add `tests/verify_no_sophia_book_promo.py` so future books cannot expose Sophia accidentally.

## Verification
1. Prove the regression test fails before the sweep.
2. Run the transformer and require exactly 136 changed pages.
3. Run the regression test and transformer `--check` mode.
4. Validate all 136 book documents retain their existing social block and complete HTML shell.
5. Require each touched book diff to contain only the Sophia-card deletion and `md:grid-cols-3` → `md:grid-cols-2` rebalance.
6. Run `git diff --check` and representative browser checks.

## Rollback
Revert the single feature-branch commit; no production, Render, or WordPress mutation is part of this task.
