# Complete keyword metadata across Spanish book pages

## Goal
Ensure every `books/week-*/index.html` page has one populated, relevant meta-keywords tag without rewriting the 143 existing keyword sets.

## Scope
- Add page-specific keyword sets to the 29 pages currently missing them.
- Keep each set to five distinct phrases covering the page topic, Spanish-learning intent, preschool audience, and bilingual-book context.
- Preserve existing titles, descriptions, canonicals, content, sharing UI, and book behavior.
- Add an idempotent transformer and an all-page regression gate.

## Verification
- Baseline audit: 143/172 populated; 29 missing.
- Transformer must change exactly 29 pages and then report zero remaining changes.
- Regression gate must find exactly one non-empty tag per page, 3–8 unique phrases, and 172/172 coverage.
- Every modified page must differ from `HEAD` only by the one inserted meta tag.
- `git diff --check` must pass.

## SEO note
Google does not use meta-keywords as a ranking signal. This completes the requested metadata coverage; the separately audited missing canonical and meta-description tags remain higher-priority SEO work.
