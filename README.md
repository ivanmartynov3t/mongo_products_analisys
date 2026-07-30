# Mongo Products Analysis

This repository is for **hierarchical, deep feature analysis** of products that communicate with MongoDB — 3T Software Labs' own product family plus third-party competitors — plus a growing set of raw market/competitive research feeding that analysis.

## Quick navigation

- [**Unified Feature Dictionary**](feature-dictionary.md) ← start here for feature IDs
- [Products index](products/README.md)
- [3t products](products/3t/README.md) · [Third-party products](products/third-party/README.md)
- [Cumulative report index](reports/cumulative-report.md)
- [High-level comparison](reports/comparisons/high-level-product-comparison.md) · [Low-level comparison](reports/comparisons/low-level-feature-comparison.md)
- [Gap analysis: NOT on any 3T product](reports/gap-analysis-not-on-3t-products.md) · [Gap analysis: NOT on Studio 3T Desktop](reports/gap-analysis-not-on-3t-desktop.md)
- [Voice-of-customer metrics (pilot)](reports/voice-of-customer-metrics.md)
- [Google research overview](research/google_research/overview.md) ← raw competitive/market research, not yet reconciled into the dictionary
- [Copilot instructions](.github/copilot-instructions.md)

## Repository map

```text
.
├── README.md                        ← you are here
├── feature-dictionary.md            ← canonical Feature ID + sub-feature ID registry
├── write_high_level.py              ← STALE generator script — do not run (see note below)
├── .github/
│   ├── copilot-instructions.md      ← authoring rules for any AI agent working in this repo
│   └── prompts/                     ← one *.prompt.md per artifact type (product report, feature
│                                        matrix/report, high/low comparison, cumulative report)
├── products/
│   ├── README.md                    ← product index + hierarchy convention
│   ├── 3t/                          ← 3T Software Labs' own products (6)
│   │   ├── README.md
│   │   ├── studio-3t/               ← Desktop IDE (Build track) — flagship, all 11 features
│   │   ├── 3t-explore/              ← browser IDE (Build track)
│   │   ├── 3t-mcp/                  ← standalone stt-cli MCP binary (Build track)
│   │   ├── 3tl-bridge/              ← CDC pipeline engine (Pipeline track)
│   │   ├── 3t-lens/                 ← governed workspace (Governed Access track)
│   │   └── 3t-access/               ← identity/permissions plane (Governed Access track)
│   │       (each: product-report.md + features/<feature-folder>/{feature-matrix,feature-report}.md)
│   └── third-party/                 ← external competitors (2)
│       ├── README.md
│       ├── mongodb-compass/         ← MongoDB Inc.'s official free GUI
│       └── visual-eaf/              ← VisuaLeaf, polyglot GUI by SozoCode
├── reports/
│   ├── cumulative-report.md         ← top-level index: coverage, executive summary, positioning
│   ├── gap-analysis-not-on-3t-products.md   ← sub-features absent across the whole 3T portfolio
│   ├── gap-analysis-not-on-3t-desktop.md    ← sub-features absent from Studio 3T Desktop specifically
│   ├── voice-of-customer-metrics.md ← pilot VoC report (compliant subset of research/ methodology)
│   └── comparisons/
│       ├── high-level-product-comparison.md ← feature-area level, per product
│       └── low-level-feature-comparison.md  ← sub-feature level, per product, with icon legend
├── research/
│   ├── gather-metrics-instructions.md    ← metrics-gathering framework (unconfirmed origin, partly non-compliant — see note below)
│   ├── report-building-framework.md      ← FPI scoring / roadmap framework (unconfirmed origin, not applied)
│   ├── research-methodology-general.md   ← general JTBD/conjoint/telemetry methodology (unconfirmed origin, not executed)
│   └── google_research/
│       ├── overview.md              ← index: overview + problems + answers for each file below
│       └── <21 topic directories>/  ← one raw research file per directory (see below)
└── templates/
    ├── product-report-template.md
    ├── feature-matrix-template.md
    ├── feature-report-template.md
    ├── high-level-comparison-template.md
    └── low-level-comparison-template.md
```

## Core approach

Analysis is organized in levels:

1. **Feature dictionary** ([feature-dictionary.md](feature-dictionary.md)): canonical registry of all 11 Feature IDs and every sub-feature ID. Every matrix, report, and comparison must use these IDs.
2. **Product level**: one high-level product report composed of feature summaries using Feature IDs.
3. **Feature level**: each applicable feature has a **feature matrix** (sub-feature IDs) and a **feature report**.
4. **Comparison level**: high-level product comparison (Feature ID rows) and low-level feature-by-feature comparison (sub-feature ID rows), rolled up into the cumulative report and the two gap-analysis reports.

## Feature IDs

| Feature ID | Folder | Display name |
|---|---|---|
| F-CONN | `connectivity` | Connectivity |
| F-QUERY | `querying` | Querying |
| F-AGG | `aggregation` | Aggregation |
| F-SCHEMA | `schema` | Schema |
| F-IDX | `indexing-performance` | Indexing & Performance |
| F-TRANSFER | `data-transfer` | Data Transfer |
| F-SHELL | `shell` | Shell |
| F-AI | `ai` | AI Features |
| F-SQL | `sql-tools` | SQL Tools |
| F-GOV | `governance` | Governance & Security |
| F-SCHED | `task-scheduler` | Task Scheduler |

Full sub-feature registry and the product × feature coverage matrix: [feature-dictionary.md](feature-dictionary.md).

## Products

All products follow the same per-product hierarchy: `product-report.md` + `features/<feature-folder>/{feature-matrix.md,feature-report.md}`. See [products/README.md](products/README.md) for the convention.

### 3T Software Labs — [products/3t/](products/3t/README.md)

- **Studio 3T** — Build track, Desktop IDE — [product-report.md](products/3t/studio-3t/product-report.md)
  - Only product covering all 11 feature areas; sole full SQL↔MongoDB migration/export toolchain, data masking (8 op types), and cross-connection index copy-paste (VisuaLeaf also has its own task scheduler — not exclusive to Studio 3T)
  - Editions: Free / Base / Pro / Ultimate — enterprise auth (Kerberos/LDAP/AWS IAM/OIDC) on Ultimate
  - Anchors the wider 3T platform (the five products below)
- **3T Explore** — Build track, browser IDE — [product-report.md](products/3t/3t-explore/product-report.md)
  - Browser-based Explore + Visual Query Builder + IntelliShell + Aggregation Editor + AI Helper
  - Workspace Switcher with 3T Access Manager integration for access control
- **3T MCP** — Build track, standalone binary — [product-report.md](products/3t/3t-mcp/product-report.md)
  - `stt-cli`: read-only MongoDB access for AI coding agents over MCP/stdio — distinct from Desktop's built-in local MCP server (HTTP transport)
- **3TL Bridge** — Pipeline track, CDC engine — [product-report.md](products/3t/3tl-bridge/product-report.md)
  - Real-time change-data-capture: MongoDB ↔ Kafka / Google Pub-Sub / HTTP
  - In-flight Transform Studio + pipeline-layer PII masking; Kubernetes/Docker Compose deployment
- **3T Lens** — Governed Access track, governed workspace — [product-report.md](products/3t/3t-lens/product-report.md)
  - Centralized connection management, compliance policy templates, PII classification, versioned field history
  - MCP tool access gated by 3T Access role policies
- **3T Access** — Governed Access track, identity plane — [product-report.md](products/3t/3t-access/product-report.md)
  - Shared identity/role/permission plane and full audit trail (human + AI agent access) spanning the Desktop IDE, 3T Explore, 3T Lens, and 3TL Bridge; whether it also governs 3T MCP is unverified

### Third-party — [products/third-party/](products/third-party/README.md)

- **MongoDB Compass** — MongoDB Inc., free/open-source — [product-report.md](products/third-party/mongodb-compass/product-report.md)
  - Only product with Queryable Encryption/CSFLE config, live mongostat/mongotop/currentOp monitoring, Atlas Search/Vector Search index management, geo schema analysis, and enterprise policy enforcement (startup/CLI/network policy, human-approval-gated AI)
  - No F-TRANSFER/F-SHELL/F-SQL/F-SCHED; F-AI limited to natural-language query only (confirmed 2026-07-28)
- **VisuaLeaf** — SozoCode, subscription polyglot GUI — [product-report.md](products/third-party/visual-eaf/product-report.md)
  - Only product with a full visual ERD designer, standalone JSON Schema tree editor, 6-step connection test wizard, GridFS viewer, split-panel layouts, MongoSync
  - Tiers: Community (3 connections, no AI) / Basic+ (VQB, validation, ERD) / Professional (AI, RBAC, audit log, compare/sync)
  - Also connects to PostgreSQL/MySQL/SQL Server/Oracle/etc. — this repo covers its MongoDB-facing capabilities only

## Reports

- **[cumulative-report.md](reports/cumulative-report.md)** — top-level index
  - States 3 products / 11 feature areas / 28 feature matrices / 257+ sub-feature rows — reflects the comparison layer's 3-column view (the whole 3T family merged into one "Studio 3T" column)
  - ⚠️ The feature-matrix count is stale: it predates the 2026-07-29 3T product split; the repo now has **35** `feature-matrix.md` files across all 8 product folders, not 28
  - Executive summary, feature coverage matrix, and "key competitive gaps" per product (for the original 3: Compass, VisuaLeaf, Studio 3T)
- **[comparisons/high-level-product-comparison.md](reports/comparisons/high-level-product-comparison.md)**
  - One row per Feature ID: positioning, edition/pricing constraints, unique differentiators
- **[comparisons/low-level-feature-comparison.md](reports/comparisons/low-level-feature-comparison.md)**
  - One row per sub-feature ID with source citations
  - Icon legend: ✅ confirmed · 🧪 partial/limited · 🗺️ roadmap · ❓ unverified · ❌ not supported · 💼 paid-tier · 🏢 enterprise-tier
- **[gap-analysis-not-on-3t-products.md](reports/gap-analysis-not-on-3t-products.md)**
  - Checks all 311 dictionary sub-feature IDs against the **whole 3T portfolio combined**
  - 13 confirmed absent (all in F-SCHEMA: validation authoring, JSON schema editor, visual-ERD cluster) · 78 unverified
- **[gap-analysis-not-on-3t-desktop.md](reports/gap-analysis-not-on-3t-desktop.md)**
  - Same 311-ID check, scoped to **Studio 3T Desktop specifically**
  - 13 confirmed absent portfolio-wide + 17 present elsewhere in the 3T family (3T Explore/MCP/Lens/Access/Bridge) but not on Desktop + 78 unverified
- **[voice-of-customer-metrics.md](reports/voice-of-customer-metrics.md)** — pilot, not a completed program
  - 7 records from one compliant source (`community.studio3t.com`); G2/Capterra/TrustRadius/Reddit excluded (ToS), Stack Overflow excluded (no signal found)
  - Per-record pain severity (1–5), workaround, enterprise signal — no aggregate FPI scoring (sample too small for the framework's own threshold)

## Research

`research/` holds two kinds of material, both upstream of the structured analysis in `products/` and `reports/` — treat everything here as raw input to be mined, not as verified fact.

### Methodology documents (root of `research/`)

- **[gather-metrics-instructions.md](research/gather-metrics-instructions.md)** — Part 1: public-scraping framework (forum posts, Reddit, G2/Capterra, competitor changelogs) → semantic processing → structured metric store
- **[report-building-framework.md](research/report-building-framework.md)** — Part 2: metric rollup → 0–100 score normalization → Public/Composite FPI (Feature Prioritization Index) formula → effort estimation → executive roadmap
- **[research-methodology-general.md](research/research-methodology-general.md)** — general triangulated methodology: JTBD/ODI interviews, MaxDiff/conjoint surveys, CRM ARR weighting, NLP support-ticket mining, in-app telemetry, SUS/NASA-TLX usability scoring
- Origin of all three is **unconfirmed** (found in-repo, not authored in-session), and they are **not compliant/executable as written** — e.g. scraping G2/Capterra/Reddit violates those sites' Terms of Service, and CRM/Zendesk/telemetry access doesn't exist in this environment. [voice-of-customer-metrics.md](reports/voice-of-customer-metrics.md) documents exactly which parts were actually (compliantly) adopted and which were deliberately dropped rather than simulated.

### [google_research/](research/google_research/overview.md) — 21 raw research files, one per topic directory

**[overview.md](research/google_research/overview.md) is the index** — overview, problems raised, and short answers for every file, so you can decide what's worth opening in full.

- **Direct competitor reports (7):** [DBeaver](research/google_research/dbeaver-competitive-intelligence-analysis/), [DataGrip](research/google_research/datagrip-competitive-analysis/), [MongoDB Compass](research/google_research/mongodb-compass-competitive-analysis/), [Navicat](research/google_research/navicat-competitive-intelligence-analysis/), NoSQLBooster ([analysis](research/google_research/nosqlbooster-competitive-analysis/), [intelligence](research/google_research/nosqlbooster-competitive-intelligence-analysis/)), [TablePlus](research/google_research/tableplus-competitive-intelligence-analysis/)
- **Studio 3T self-diagnostics (3):** [enterprise governance gap analysis](research/google_research/studio-3t-enterprise-gap-analysis/), [missing tooling integrations](research/google_research/studio-3t-missing-integrations/), [review mining](research/google_research/studio-3t-review-mining/)
- **Pain points & personas (4):** [tool pain points](research/google_research/mongodb-gui-tool-pain-points/), [user pain points (comprehensive)](research/google_research/mongodb-gui-user-pain-points-analysis/), [user personas research](research/google_research/mongodb-gui-user-personas-research/), [user personas](research/google_research/mongodb-gui-user-personas/)
- **Market & platform trends (4):** [GUI competitor landscape](research/google_research/mongodb-gui-competitor-landscape-analysis/), [GUI technology trends](research/google_research/mongodb-gui-technology-trends/), [MongoDB evolution & roadmap](research/google_research/mongodb-evolution-and-roadmap/), [database GUI churn analysis](research/google_research/database-gui-churn-analysis/)
- **Workflow & AI automation (3):** [GUI developer workflow analysis](research/google_research/mongodb-gui-developer-workflow-analysis/), [developer workflow automation](research/google_research/mongodb-developer-workflow-automation/), [AI automation opportunities](research/google_research/mongodb-ai-automation-opportunities/)

## Templates

Blank scaffolds for each artifact type, mirrored by prompts in `.github/prompts/`: [product-report-template.md](templates/product-report-template.md), [feature-matrix-template.md](templates/feature-matrix-template.md), [feature-report-template.md](templates/feature-report-template.md), [high-level-comparison-template.md](templates/high-level-comparison-template.md), [low-level-comparison-template.md](templates/low-level-comparison-template.md).

## AI agent instructions

[.github/copilot-instructions.md](.github/copilot-instructions.md) has the authoring rules (structure, ID discipline, confirmed/roadmap/unverified labeling) any agent must follow when extending this repo. [.github/prompts/](.github/prompts) has one `*.prompt.md` per artifact type — product report, feature matrix, feature report, high-level comparison, low-level comparison, cumulative report.

> **`write_high_level.py`** (repo root) is a stale one-off generator whose embedded content has diverged from the hand-maintained `high-level-product-comparison.md`. Do not run it to "sync" — it would silently overwrite hand-authored content. Edit the `.md` files directly.

## Required workflow

1. Read `feature-dictionary.md` to understand all Feature IDs and sub-feature IDs.
2. Choose product group (`third-party` or `3t`) and product.
3. Create/update the product-level report using Feature IDs from the dictionary.
4. For each applicable feature, create `features/<feature-folder>/feature-matrix.md` and `feature-report.md`.
5. If a needed sub-feature ID does not exist in the dictionary, add it there first.
6. Update the high-level and low-level comparison reports (and the gap-analysis reports, if the change affects a confirmed/absent status).

## Quality bar

- Feature analysis must be **implementation-aware** and low-level, not generic.
- Every major claim must be **source-backed**.
- All IDs must come from `feature-dictionary.md`.
- Clearly separate **confirmed behavior**, **roadmap/planned behavior**, and **unknown/unverified behavior**.
