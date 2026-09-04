# Repository Structure — `mongo_products_analisys`

This document is a full map of the repository as it exists today, for anyone (human or agent) who needs to work in it without re-discovering the conventions from scratch. It is descriptive, not aspirational — see `update-plans/` for what should change.

## What this repository is

A source-backed competitive-intelligence knowledge base comparing MongoDB-facing GUI products: 3T Software Labs' own six-product family versus two structurally-analyzed third-party competitors (MongoDB Compass, VisuaLeaf), plus a much larger set of raw, not-yet-structured research on five more competitors and market/persona topics. The repository is maintained by AI coding agents (GitHub Copilot / Claude) against a strict, self-documented convention: every fact must trace to a source, every feature must use a canonical ID from a single dictionary, and every claim must be labeled confirmed / roadmap / unverified.

It is a **documentation-only repo** — no application code, no build system, no tests. The one script present (`write_high_level.py`) is explicitly marked stale and not to be run.

## Top-level layout

```
.
├── README.md                     Entry point: navigation, repo map, core approach, required workflow
├── feature-dictionary.md         Canonical registry: 11 Feature IDs, 328 sub-feature IDs, product×feature coverage matrix, Proposed Feature Registry (PROP- pipeline)
├── write_high_level.py           STALE generator — do not run; diverged from hand-maintained high-level-product-comparison.md
├── .github/
│   ├── copilot-instructions.md   Authoring rules binding on any agent editing this repo
│   └── prompts/                  One *.prompt.md per artifact type (mirrors templates/)
├── .claude/
│   └── settings.local.json       Local Claude Code tool-permission allowlist (not portable / not part of the analysis)
├── .idea/                        IntelliJ project metadata (editor-only, not analysis content)
├── products/                     Structured, ID-driven per-product analysis (the "hierarchical" layer)
├── reports/                      Roll-up comparison and gap-analysis reports built from products/
├── research/                     Raw and semi-structured research feeding the structured layers above
├── templates/                    Blank scaffolds, one per artifact type
└── .git/, .DS_Store              VCS internals / OS cruft (see update-plans/02 on the latter)
```

## `.github/` — agent operating rules

- **`copilot-instructions.md`** — the binding ruleset: mandatory product/feature folder hierarchy, mandatory use of Feature IDs and sub-feature IDs from the dictionary (never invent one), mandatory `feature-matrix.md` + `feature-report.md` pair per feature, mandatory comparison-report layer, mandatory `Navigation` section in every new file, mandatory confirmed/roadmap/unverified labeling.
- **`prompts/`** — six task-specific prompt files, one per artifact type, each a short imperative checklist for the AI agent producing that artifact:
  - `create-product-report.prompt.md`
  - `create-feature-matrix.prompt.md`
  - `create-feature-report.prompt.md`
  - `create-high-level-comparison.prompt.md`
  - `create-low-level-comparison.prompt.md`
  - `create-cumulative-report.prompt.md`

These prompts are the existing template for "direct, literal instructions for an agent" — the update plans in `update-plans/` follow the same style.

## `products/` — the structured, per-product hierarchy

Convention (defined in `products/README.md` and enforced by `copilot-instructions.md`):

```
products/<group>/<product-name>/
├── product-report.md
└── features/<feature-folder>/
    ├── feature-matrix.md
    └── feature-report.md
```

`<group>` is either `third-party` or `3t`. `<feature-folder>` names are fixed by `feature-dictionary.md` (e.g. `connectivity`, `querying`, `schema` …) and must match exactly. A feature folder only exists for a product if that product actually has the feature — no placeholders.

### `products/3t/` — 6 products, 17 feature-matrix files total

| Product | Track | Feature folders present |
|---|---|---|
| `studio-3t/` | Build — Desktop IDE (flagship) | all 11: connectivity, querying, aggregation, schema, indexing-performance, data-transfer, shell, ai, sql-tools, governance, task-scheduler — plus its own `CHANGELOG.md` |
| `3t-explore/` | Build — browser IDE | ai, governance (both partial per dictionary) |
| `3t-mcp/` | Build — standalone `stt-cli` binary | ai (partial) |
| `3tl-bridge/` | Pipeline — CDC engine | governance |
| `3t-lens/` | Governed Access — governed workspace | governance |
| `3t-access/` | Governed Access — identity plane | governance |

### `products/third-party/` — 2 products, 18 feature-matrix files total

| Product | Feature folders present |
|---|---|
| `mongodb-compass/` | connectivity, querying, aggregation, schema, indexing-performance, ai (partial), governance — 7 |
| `visual-eaf/` (branded "VisuaLeaf" — see update-plans/02 on the name mismatch) | all 11 |

Total: **35 `feature-matrix.md` files** across 8 product folders (7 + 11 + 11 + 2 + 1 + 1 + 1 + 1). The README's older "28" figure and `reports/cumulative-report.md`'s scope table are stale against this — see `update-plans/02-repo-hygiene-and-stale-content.md`.

## `reports/` — roll-up layer

- **`cumulative-report.md`** — top-level index: scope counts, feature coverage matrix, executive summary per product, key competitive gaps, unverified items, known issues, edition/pricing summary. Contains multiple dated "Updated" addenda rather than being fully rewritten each time — several are flagged stale in-place.
- **`comparisons/high-level-product-comparison.md`** — one row per Feature ID, cross-product.
- **`comparisons/low-level-feature-comparison.md`** — one row per sub-feature ID, cross-product, with an icon legend (✅🧪🗺️❓❌💼🏢) and source citations. This is the master fact table gap-analysis and cumulative reports both derive from.
- **`gap-analysis-not-on-3t-products.md`** — checks all 328 dictionary sub-feature IDs against the whole 3T portfolio combined. Currently: 9 confirmed absent (all F-SCHEMA), 77 unverified.
- **`gap-analysis-not-on-3t-desktop.md`** — same 328-ID check, scoped to Studio 3T Desktop specifically (features present elsewhere in the 3T family but not on Desktop get their own bucket).
- **`voice-of-customer-metrics.md`** — a small (7-record), explicitly-labeled pilot VoC report; not a completed program.

## `research/` — raw and semi-structured input, upstream of everything else

Three methodology documents sit directly in `research/`:
- `gather-metrics-instructions.md`, `report-building-framework.md`, `research-methodology-general.md` — all three are explicitly flagged in `README.md` as **unconfirmed origin** and **not compliant/executable as written** (they assume scraping G2/Capterra/Reddit, which violates ToS, and CRM/telemetry access this environment doesn't have). `voice-of-customer-metrics.md` documents what was actually adopted from them.

Two research programs live in dated subdirectories:

- **`studio-3t-desktop-review-2026/`** — a completed full source-code re-audit of Studio 3T Desktop, one file per feature area (`00-research-plan.md`, `01-connectivity-findings.md` … `11-task-scheduler-findings.md`) plus `12-consolidated-corrections.md`, which is the single source of truth for corrections not yet fully propagated into `reports/` (see `update-plans/01`).
- **`feature-decision-2026/`** — an active "what should Studio 3T build next" decision pipeline: `00-dialog-and-inputs.md`, `01-research-plan.md` (scoring rubric), `02-data-inventory.md`, `03-candidate-longlist.md`, `04-scored-longlist.md`, `05-shortlist-deepdive.md`, `06-verification-notes.md`, `07-v1.1-research-plan.md`, and two recommendation memos (`next-feature-recommendationv.1.0.md`, `next-feature-recommendationv.1.1.md`). Its output feeds the "Proposed Feature Registry" section of `feature-dictionary.md`.

`research/google_research/` holds **21 raw research files**, one per topic subdirectory, indexed by `overview.md`. Seven are direct-competitor reports on products that have **no** structured `products/third-party/` entry yet: DBeaver, DataGrip, Navicat, NoSQLBooster (two files), TablePlus. The rest cover Studio 3T self-diagnostics, user pain points/personas, and market/workflow trends. None of this has been reconciled into `feature-dictionary.md` or the structured product hierarchy.

## `templates/` — blank scaffolds

One template per artifact type, mirrored 1:1 by `.github/prompts/`: `product-report-template.md`, `feature-matrix-template.md`, `feature-report-template.md`, `high-level-comparison-template.md`, `low-level-comparison-template.md`.

## Known inconsistencies at time of writing

(Full detail and fix instructions in `update-plans/`.)

1. `reports/cumulative-report.md` scope table says 28 feature matrices / 3 products; actual is 35 matrices / 8 product folders.
2. `feature-dictionary.md` and `README.md` link to `reports/next-feature-recommendation.md`, which does not exist — the real files are `research/feature-decision-2026/next-feature-recommendationv.1.0.md` and `v.1.1.md`.
3. `research/studio-3t-desktop-review-2026/12-consolidated-corrections.md` lists specific edits still owed to four `reports/` files (§"What downstream reports need") that have not been applied yet.
4. Directory name `products/third-party/visual-eaf/` vs. the product's actual brand name "VisuaLeaf" — inconsistent casing/spelling used across files.
5. `.DS_Store` files are committed under `products/`, `research/`, and `.git/`.
6. `write_high_level.py` is dead code with no scheduled removal or archival decision.
7. Three `research/` methodology documents are known non-executable as written, with no decision recorded on whether to rewrite, replace, or delete them.
8. 77 of 328 sub-feature IDs remain unverified for the 3T portfolio (per `gap-analysis-not-on-3t-products.md`), and a comparable unverified count exists for Compass/VisuaLeaf in the low-level comparison.
