# Plan 4 — Extend Structured Competitor Coverage

## Non-negotiable: dictionary-first, classification-compliant

Before writing a single product file: any capability that doesn't already have a sub-feature ID **must be added to `feature-dictionary.md`'s Sub-feature registry first**, under the correct Feature ID section, following the exact `<FEATURE>-<suffix>` naming pattern — never invent an ID inline in a matrix and backfill the dictionary later, and never reuse an existing ID for a materially different capability just because the name is close. Every new ID needs: a one-line description matching the dictionary's existing style, and at least one citation (from the product's own research file, ideally a primary source that file itself cites) justifying why it's a distinct, real capability and not a duplicate of something already in the registry — check the full registry (all 11 feature areas, not just the obviously-related one) before minting anything new.

Every fact in every new product-report.md / feature-matrix.md / feature-report.md must carry one of exactly three statuses, using the vocabulary already fixed by `copilot-instructions.md` and the low-level comparison's icon legend — no other status words, no hedging phrases that aren't one of these three:
- **Confirmed** — traceable to a primary source, or to a secondary research file that itself names a primary source for that specific claim.
- **Roadmap/planned** — the source explicitly says a capability is announced-but-not-shipped, beta, or feature-flagged.
- **Unverified** — the source only asserts it without a primary citation, or the matrix compiler couldn't confirm one either way. This is the default for any claim that doesn't clear the "Confirmed" bar — do not round up.

This rule is stricter than "just cite something": a secondary competitive-intelligence research file saying "DBeaver supports X" is not, by itself, enough to mark X confirmed — check whether that file's own Works Cited backs the specific claim with a primary source (vendor doc, GitHub issue, release note) before writing "Confirmed." If it doesn't, write "Unverified — per secondary source, no primary citation" rather than silently treating the research file's prose as ground truth.

## Objective

`research/google_research/` contains raw competitive-intelligence write-ups on five direct competitors that have never been turned into structured `products/third-party/` entries: DBeaver, DataGrip, Navicat, NoSQLBooster (two files: `nosqlbooster-competitive-analysis/` and `nosqlbooster-competitive-intelligence-analysis/`), and TablePlus. This plan turns each into a first-class product entry following the exact same convention already used for MongoDB Compass and VisuaLeaf.

## Before starting

Read, in order: `.github/prompts/create-product-report.prompt.md`, `.github/prompts/create-feature-matrix.prompt.md`, `.github/prompts/create-feature-report.prompt.md`, and the two existing third-party products (`products/third-party/mongodb-compass/`, `products/third-party/visual-eaf/`) as worked examples of the target shape. Match their structure exactly — do not improvise a different layout for the new products.

## Per-product procedure (repeat for each of the 5 products)

1. **Locate source material.** For DBeaver: `research/google_research/dbeaver-competitive-intelligence-analysis/`. DataGrip: `research/google_research/datagrip-competitive-analysis/`. Navicat: `research/google_research/navicat-competitive-intelligence-analysis/`. NoSQLBooster: both `research/google_research/nosqlbooster-competitive-analysis/` and `research/google_research/nosqlbooster-competitive-intelligence-analysis/` (read both, reconcile any conflicts by preferring the more specific/cited claim, and note the conflict if it can't be reconciled). TablePlus: `research/google_research/tableplus-competitive-intelligence-analysis/`.
2. **Assess source sufficiency before writing anything.** These are secondary-research documents (Google-research-style competitive analyses), not primary-source product audits like the Studio 3T Desktop review. Every fact pulled from them into the structured layer must be labeled with the confirmed/roadmap/unverified discipline `copilot-instructions.md` requires — and because the source itself is secondary, default to **unverified** for any claim it doesn't itself cite to a primary source (vendor doc, pricing page, changelog). Do not upgrade a secondary-research claim to "confirmed" just because it appears in a well-written research file.
3. **Create the product folder**: `products/third-party/<slug>/`, where `<slug>` is a short lowercase-dash name consistent with the existing `mongodb-compass` / `visual-eaf` style (suggested: `dbeaver`, `datagrip`, `navicat`, `nosqlbooster`, `tableplus`).
4. **Determine which of the 11 Feature IDs apply**, using the same rule already applied to Compass/VisuaLeaf: only create a `features/<folder>/` directory for a feature area the source material actually discusses. Do not create placeholder folders for feature areas with no evidence either way — that's what "unverified, omitted" means under the existing convention (see `products/README.md` and `feature-dictionary.md` naming rule #5).
5. **Write `product-report.md`** from `templates/product-report-template.md`, following `create-product-report.prompt.md`'s requirements exactly: Feature ID-based inventory table, links to each feature matrix/report, constraints/prerequisites/known-unknowns section, Navigation section.
6. **For each applicable feature**, write `feature-matrix.md` (from `templates/feature-matrix-template.md`, using sub-feature IDs from `feature-dictionary.md` — if the source material describes a capability with no existing sub-feature ID, add the ID to the dictionary first per the Ground Rules in `00-overview-and-master-plan.md`) and `feature-report.md` (from `templates/feature-report-template.md`).
7. **Update `feature-dictionary.md`'s product×feature coverage matrix** to add a column for the new product, marked per the same ✓/— convention already used.
8. **Update `reports/comparisons/high-level-product-comparison.md` and `low-level-feature-comparison.md`** to add the new product as a column/row-set, following the existing icon legend.
9. **Do not touch `reports/gap-analysis-not-on-3t-products.md` or `gap-analysis-not-on-3t-desktop.md`** — those reports are explicitly scoped to the 3T portfolio and are not affected by adding third-party competitors.
10. **Update `products/third-party/README.md`** to list the new product in its index, matching the existing entries' format.

## Sequencing across the five products

Do one product fully (all steps above, including the dictionary and comparison-report updates) before starting the next, rather than doing "step 3 for all five, then step 4 for all five." This keeps each product's addition independently revertible and matches the "one plan, one commit" discipline — treat each product as its own commit within this plan.

## What NOT to do

- Do not attempt to independently verify every secondary-research claim against a primary source as part of this plan — that is Plan 3's job, and trying to do both at once will stall this plan indefinitely. Land the structured entries with honest unverified/roadmap labeling first; Plan 3's ongoing verification work will pick them up over time.
- Do not merge or rename the two NoSQLBooster source directories — read both, but keep the product folder singular (`products/third-party/nosqlbooster/`) since it's one product regardless of how many raw research files describe it.
- Do not add a `reports/gap-analysis-not-on-<new-product>.md` file — the two existing gap-analysis reports are a 3T-specific report type, not a per-competitor template.

## Verification before marking a product done

- `product-report.md` exists, links resolve, and every feature listed has both a `feature-matrix.md` and `feature-report.md`.
- Every sub-feature ID used exists in `feature-dictionary.md` (grep the new files' IDs against the dictionary).
- The product appears in `feature-dictionary.md`'s coverage matrix and both comparison reports.
- No claim in the new files is labeled "confirmed" without a citation more specific than "per research file X" — trace it to what that file itself cited, or relabel as unverified.

## Execution log

(One line per product completed: date, product, feature areas covered, count of new sub-feature IDs added if any.)
