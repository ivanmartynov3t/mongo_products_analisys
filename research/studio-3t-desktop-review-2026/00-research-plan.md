# Research Plan — Full Feature Review of Studio 3T Desktop

## Navigation

- [Repository README](../../README.md)
- [Feature dictionary](../../feature-dictionary.md)
- [Studio 3T product report](../../products/3t/studio-3t/product-report.md)
- [Copilot instructions (authoring rules)](../../.github/copilot-instructions.md)

## Objective

Perform a **full review of `products/3t/studio-3t/`** against what Studio 3T Desktop actually implements, in order to:

1. **Add new features** currently implemented in the product but not represented anywhere in the repo's feature dictionary/matrices.
2. **Update existing features** — correct completeness status (confirmed / partial / roadmap / unverified / absent) with fresh, source-backed evidence.
3. Do this with **better methodology** than a docs-only pass: direct source-code investigation, architecture-aware notes, and a git/release-note-derived changelog — then record everything as an explicit, dated change log.

This is a documentation-accuracy pass, not a feature-recommendation exercise (that already exists at [`research/feature-decision-2026/`](../feature-decision-2026/01-research-plan.md) and [`reports/next-feature-recommendation.md`](../../reports/next-feature-recommendation.md) — this effort is complementary: it fixes what's documented about *existing* Studio 3T Desktop capability, rather than proposing what to build next).

## Scope guardrail — where reads vs. writes happen

- **Read-only investigation**: the actual Studio 3T Desktop source repository (`3t.tools`, specifically `product-suite/` — code, plugin/action registrations, settings panels, git history, `release/studio-3t/` notes). Nothing there is modified.
- **Writes confined to `mongo_products_analisys/`**, primarily:
  - `products/3t/studio-3t/**` (product-report.md, all 11 features' `feature-matrix.md` + `feature-report.md`)
  - `reports/**` (cumulative report, both gap-analysis reports, both comparison reports)
  - `feature-dictionary.md` (new sub-feature IDs, if code reveals undocumented capability)
  - a new `products/3t/studio-3t/CHANGELOG.md`
  - this research folder

## Methodology

### 1. Evidence source
Primary evidence is the Studio 3T Desktop source code itself (`product-suite/`), not just the repo's existing analysis docs. Existing docs (`feature-dictionary.md`, current matrices/reports) are the starting checklist, not the ceiling.

### 2. New-feature discovery
Full sweep across all 11 existing Feature IDs (`F-CONN`, `F-QUERY`, `F-AGG`, `F-SCHEMA`, `F-IDX`, `F-TRANSFER`, `F-SHELL`, `F-AI`, `F-SQL`, `F-GOV`, `F-SCHED`) — not just areas suspected to be thin. Anything undocumented found in code is bucketed into an existing sub-feature ID where it fits; anything that doesn't fit any existing ID becomes a **new sub-feature ID candidate**, added to `feature-dictionary.md` first (per the repo's own authoring rule — never invented ad hoc in a matrix).

### 3. Completeness assessment — combined approach
All three of the following are applied together, not as alternatives:
- **Per-sub-feature-ID checklist against code**: every existing sub-feature ID under Studio 3T is individually verified against `product-suite/` source, with status updated (confirmed / partial / roadmap / unverified / absent) and a citation (module/plugin/class or file reference).
- **Spot-check + confidence rating**: used to prioritize where to go deep vs. where existing docs already hold up, rather than re-deriving everything from zero with equal effort.
- **Changelog/release-note diff**: recent git history cross-referenced with public release notes to see what's shipped since the docs were last accurate, and to date changes.

### 4. Architecture-aware depth
Default to documenting **user-observable behavior** (what a Studio 3T Desktop user can see/do), but add **implementation-level detail** (module/plugin/class, notable constraints) specifically where it explains a completeness limitation or an edition gate (Free/Base/Pro/Ultimate) — matching the repo's existing "implementation-aware, not generic" quality bar.

### 5. Changelog inputs
- **Git history** of `product-suite/`, windowed to the **recent ~12–24 months** (not full history — older commits are lower-value for current completeness, and full-history mining is disproportionately slow).
- **Public release notes** ("what's new" pages / in-repo release material), cross-referenced against the git-log findings so internal commit granularity and user-facing framing agree.

### 6. Change-log artifact
A new **`products/3t/studio-3t/CHANGELOG.md`** records every edit this review makes — new sub-feature IDs added, status changes (old → new, with reason/citation), new feature-report sections — dated, so future reviews can see what changed and why without diffing every file by hand.

### 7. Downstream propagation
Per the repo's own "Required workflow" (step 6 in the README), once Studio 3T's docs and the dictionary change, the following are updated in the same pass so nothing is left stale:
- `reports/cumulative-report.md` (including correcting the already-known-stale feature-matrix count)
- `reports/gap-analysis-not-on-3t-products.md` and `reports/gap-analysis-not-on-3t-desktop.md`
- `reports/comparisons/high-level-product-comparison.md` and `reports/comparisons/low-level-feature-comparison.md`

### 8. Execution mode
Parallelized: one subagent per Feature ID (11 total) investigates code + git history + release notes for that area and reports structured findings (sub-feature ID, old status → new status, evidence). Synthesis, dictionary/doc edits, changelog authoring, and downstream propagation are then done directly (not left as a separate approval step) — the result is one commit-able diff across `mongo_products_analisys/` for review via `git status`/`git diff`, following the same direct-edit convention already used in `research/feature-decision-2026/`.

## Deliverables checklist

- [ ] `feature-dictionary.md` — any new sub-feature IDs added under the correct Feature ID sections
- [ ] `products/3t/studio-3t/product-report.md` — updated if any feature-area summary shifts
- [ ] `products/3t/studio-3t/features/*/feature-matrix.md` (all 11) — status updates, new rows
- [ ] `products/3t/studio-3t/features/*/feature-report.md` (all 11) — narrative updates, architecture notes, new sections
- [ ] `products/3t/studio-3t/CHANGELOG.md` — new file, dated entries
- [ ] `reports/cumulative-report.md` — refreshed counts/summary
- [ ] `reports/gap-analysis-not-on-3t-products.md` — refreshed
- [ ] `reports/gap-analysis-not-on-3t-desktop.md` — refreshed
- [ ] `reports/comparisons/high-level-product-comparison.md` — refreshed
- [ ] `reports/comparisons/low-level-feature-comparison.md` — refreshed

## Decision log (this plan's own history)

- **2026-07-31** — Plan established via discussion with the user, one question at a time, each with a recommended default. Key decisions: source-code-grounded (not docs-only), full 11-feature sweep, combined checklist+spot-check+changelog completeness method, git (recent 12–24mo) + public release notes for the changelog, dedicated `CHANGELOG.md`, architecture-aware depth where it explains limits/gating, parallel subagent execution (one per Feature ID), write directly in one pass rather than findings-first, downstream reports updated in the same pass, and a hard guardrail that only `mongo_products_analisys/` is written to — the Studio 3T source repo is read-only evidence.
