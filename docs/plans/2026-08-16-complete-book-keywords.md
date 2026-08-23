# Complete keyword metadata across Spanish book pages

## Goal
Ensure every `books/week-*/index.html` page has one populated, relevant meta-keywords tag without rewriting the 143 existing keyword sets, and add useful descriptions to the 19 touched pages that lack them.

## Scope
- Add page-specific keyword sets to the 29 pages currently missing them.
- Add curated 120–160 character Spanish descriptions to the 19 touched pages currently missing descriptions.
- Keep each keyword set to five distinct phrases covering the page topic, Spanish-learning intent, preschool audience, and bilingual-book context.
- Preserve existing titles, descriptions, canonicals, content, sharing UI, and book behavior.
- Add an idempotent transformer and independent regression gates.

## Verification
- Baseline audit: 143/172 populated keyword tags; 29 missing. Of those 29 pages, 19 also lack descriptions.
- Transformer must add keywords to exactly 29 pages and descriptions to exactly 19 of them, then report zero remaining changes.
- Regression gates must find exactly one non-empty keyword tag per page, 3–8 unique phrases, 172/172 keyword coverage, and one 120–160 character description on each of the 19 targets.
- Every modified page must differ from `HEAD` only by the inserted metadata tags.
- `git diff --check` must pass.

## SEO note
Google does not use meta-keywords as a ranking signal. The added descriptions are the meaningful search-snippet metadata in this change; broader canonical and description coverage outside these 29 pages remains separate work.
