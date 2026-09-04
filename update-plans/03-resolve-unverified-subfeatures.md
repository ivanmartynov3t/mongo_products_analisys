# Plan 3 — Resolve Unverified Sub-Features

## Objective

`reports/gap-analysis-not-on-3t-products.md` currently lists 77 sub-feature IDs as unverified for the 3T portfolio (after Plan 1's corrections land — recount before starting, since Plan 1 changes this number). A comparable unverified set exists for MongoDB Compass and VisuaLeaf in `reports/comparisons/low-level-feature-comparison.md`. This plan is open-ended research, not a fixed checklist — it has an explicit stopping rule instead of a fixed end state.

## Scope rule — what counts as "resolved"

An unverified sub-feature ID is resolved when it moves to exactly one of these states, each requiring a citation:

- **Confirmed present** — a primary source (vendor documentation, pricing/edition page, official changelog, or for 3T products, source code under `product-suite/` if accessible) states or shows the capability exists.
- **Confirmed absent** — a primary source explicitly documents the product's scope in a way that rules the capability out (e.g., an edition comparison table that lists the feature area but not this specific capability, or documentation stating a narrower alternative exists instead).
- **Still unverified, with a documented reason** — you checked and found no primary source either way. Do not leave it silently unverified; add a one-line note of what was checked and came up empty, so the next pass doesn't repeat the same dead-end search.

Never mark something confirmed based on a blog post, forum comment, review site, or your own inference about "how these tools usually work." Secondary sources may justify effort spent looking, not the conclusion.

## Priority order

Work through unverified IDs in this order, stopping at any natural session boundary (this plan does not need to be finished in one pass):

1. **3T-portfolio gaps that are also cited in `feature-decision-2026/`'s Proposed Feature Registry** (`feature-dictionary.md`) as `🔗 Dictionary-Tracked` — resolving these has a direct payoff for Plan 5's roadmap decisions. Cross-reference the `PROP-` table's "Dictionary link" column against the unverified list.
2. **IDs unverified for more than one product simultaneously** (check both gap-analysis reports and the low-level comparison) — resolving one source often resolves several rows at once (e.g., a single vendor pricing page can confirm/deny 5–10 IDs in one fetch).
3. Everything else, in the order it appears in `reports/gap-analysis-not-on-3t-products.md`.

## Per-ID research procedure

1. Look up the sub-feature ID's full description in `feature-dictionary.md`.
2. Identify which product(s) have it marked unverified (check `reports/comparisons/low-level-feature-comparison.md`, not just the gap-analysis reports — the gap-analysis reports are derived from it and can lag).
3. For a 3T product: check the product's own `product-report.md` and `feature-matrix.md` first — the answer may already exist there and just not be reflected upstream (a sync gap, not a research gap). If genuinely absent from those, do not attempt to access `product-suite/` source unless you already have access rules for it from a prior session — this plan does not grant new source-code access.
4. For MongoDB Compass or VisuaLeaf: check the vendor's own documentation and pricing/edition pages first (`mongodb.com/products/tools/compass`, `visualeaf.com`). Use the exact page URL as the citation, with the access date.
5. Update, in this order: the product's own `feature-matrix.md` row (source of truth) → `reports/comparisons/low-level-feature-comparison.md` → the relevant gap-analysis report(s) → `reports/comparisons/high-level-product-comparison.md` only if the change affects that report's feature-area-level summary.
6. Never update a downstream report (comparison, gap-analysis, cumulative) without also updating the product-level `feature-matrix.md`/`feature-report.md` it derives from — the product files are the source of truth per `copilot-instructions.md`.

## Batching rule

Do not open a browser session or fetch a URL per single sub-feature ID. Group by source: fetch each distinct vendor page once, extract every sub-feature ID it can confirm or deny in that one visit, then move to the next page. This keeps the work proportional to the number of distinct sources, not the number of IDs (328 IDs, but far fewer distinct source pages).

## Stopping rule for a single session

Stop and log progress when either:
- You've resolved (in any of the three end states above) at least 15 sub-feature IDs, or
- You've exhausted the priority-1 and priority-2 buckets and the next available source page in priority-3 requires access this plan doesn't grant (e.g., a paywalled review, a login-gated forum).

Do not attempt to reach 0 unverified IDs in one pass — the "still unverified, with a documented reason" state is an acceptable and expected outcome for a meaningful fraction of these.

## Verification before logging a session as done

- Every ID you touched has a citation in the report where you recorded its new status.
- No ID was moved to confirmed based on a non-primary source.
- The gap-analysis reports' unverified counts were recounted (not hand-decremented) after your edits, and the new count matches what you can verify by reading the tables.

## Execution log

- 2026-09-04 — Primary-source verification pass: verified 8 sub-feature IDs (`CONN-in-use-enc`, `CONN-role-docs`, `IDX-perf-insights`, `IDX-vector-search`, `IDX-atlas-search`, `IDX-type-hashed`, `QUERY-collation`, `QUERY-max-time`) against MongoDB Compass documentation (`https://www.mongodb.com/docs/compass/current/`). Resolved `IDX-type-hashed` as confirmed present in MongoDB Compass's feature-matrix and low-level comparison tables.
