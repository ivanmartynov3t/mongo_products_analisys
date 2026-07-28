# VisuaLeaf — Product Report

## Navigation

- [Repository README](../../../README.md)
- [Feature dictionary](../../../feature-dictionary.md)
- [Third-Party Products Index](../)
- [High-level comparison](../../../reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](../../../reports/comparisons/low-level-feature-comparison.md)

## Product Overview

| Field | Value |
|---|---|
| **Product** | VisuaLeaf |
| **Maker** | SozoCode (support@sozocode.com, [@SozoCode](https://twitter.com/SozoCode)) |
| **Website** | https://visualeaf.com |
| **GitHub** | https://github.com/sozocode/VisuaLeaf (partially open source) |
| **Platform** | Desktop — Windows, macOS, Linux; no web version |
| **Tech Stack** | Modern web technologies; Electron strongly implied |
| **Min Requirements** | 4 GB RAM, 500 MB disk space |
| **Air-gapped Support** | Fully offline after one-time license activation |
| **Credential Storage** | AES-256 encrypted, stored locally; never transmitted to SozoCode servers |
| **Also connects to** | visualeaf.com (homepage, 2026-07-28) lists native support for PostgreSQL, MySQL, MariaDB, Microsoft SQL Server, SQLite, Oracle, CockroachDB, ClickHouse, DuckDB, and TiDB, in addition to MongoDB, Azure Cosmos DB, and Amazon DocumentDB. VisuaLeaf is positioned as a polyglot database GUI, not a MongoDB-only tool — this analysis covers its MongoDB-facing capabilities only; the non-MongoDB engines are out of scope for this repository. |

---

## Feature Inventory

Feature IDs and folder names from [feature-dictionary.md](../../../feature-dictionary.md).

| Feature ID | Feature | Matrix | Report | Plan |
|---|---|---|---|---|
| F-CONN | Connectivity | [feature-matrix.md](features/connectivity/feature-matrix.md) | [feature-report.md](features/connectivity/feature-report.md) | All (Community: 3-connection cap) |
| F-QUERY | Querying | [feature-matrix.md](features/querying/feature-matrix.md) | [feature-report.md](features/querying/feature-report.md) | All (VQB: Basic+; AI Query: Professional) |
| F-AGG | Aggregation | [feature-matrix.md](features/aggregation/feature-matrix.md) | [feature-report.md](features/aggregation/feature-report.md) | All |
| F-SCHEMA | Schema | [feature-matrix.md](features/schema/feature-matrix.md) | [feature-report.md](features/schema/feature-report.md) | Basic+ (Validation + Visual Designer: Basic+) |
| F-IDX | Indexing & Performance | [feature-matrix.md](features/indexing-performance/feature-matrix.md) | [feature-report.md](features/indexing-performance/feature-report.md) | All |
| F-TRANSFER | Data Transfer | [feature-matrix.md](features/data-transfer/feature-matrix.md) | [feature-report.md](features/data-transfer/feature-report.md) | Basic+ (Community: 0 tasks) |
| F-SHELL | Shell | [feature-matrix.md](features/shell/feature-matrix.md) | [feature-report.md](features/shell/feature-report.md) | All |
| F-AI | AI Features | [feature-matrix.md](features/ai/feature-matrix.md) | [feature-report.md](features/ai/feature-report.md) | Professional only |
| F-SQL | SQL Tools (partial — SQL Mode) | [feature-matrix.md](features/sql-tools/feature-matrix.md) | [feature-report.md](features/sql-tools/feature-report.md) | Plan tier unverified |
| F-GOV | Governance & Security | [feature-matrix.md](features/governance/feature-matrix.md) | [feature-report.md](features/governance/feature-report.md) | Basic+ (RBAC/Audit: Professional) |
| F-SCHED | Task Scheduler | [feature-matrix.md](features/task-scheduler/feature-matrix.md) | [feature-report.md](features/task-scheduler/feature-report.md) | Basic+ (Community: 0 tasks) |

---

## Editions & Pricing

| Edition | Price | Key Capabilities | Key Limits |
|---|---|---|---|
| **Community** | Free | Core querying, aggregation, shell, index management | 3 connections max; no VQB; no Saved Queries; no Tasks; no Schema Validation; no Visual Schema; no RBAC |
| **Basic** | $42 one-time **or** $42/year | All Community + unlimited connections, VQB, Saved Queries, up to 2 import/export tasks, Schema Validation, Visual Schema Designer, Data Masking | No AI Assistant; No RBAC Dashboard; No Collection Compare & Sync |
| **Professional** | $149/year | All Basic + AI Assistant, unlimited tasks, RBAC Dashboard, Audit Logging, Collection Compare & Sync | — |

Source: https://visualeaf.com

---

## Deployment & Platform

- **Desktop only:** Windows, macOS, Linux native apps — **confirmed**
- **No web/cloud version** — **confirmed**
- **Air-gapped:** Fully offline after one-time license activation — **confirmed**
- **Credential storage:** AES-256 encrypted, stored locally; never transmitted to SozoCode servers — **confirmed**
- **App Name tag:** Registered as "VisuaLeaf" visible in `db.currentOp()` and MongoDB profiler — **confirmed**
- **Partially open source:** GitHub repo at https://github.com/sozocode/VisuaLeaf; extent of open-source components not fully documented — **unknown/unverified**

---

## Roadmap

| Item | Status | Target |
|---|---|---|
| Kerberos (GSSAPI) authentication | **roadmap/planned** | Q2 2026 |
| OIDC authentication | **roadmap/planned** | Q2 2026 |
| Amazon DocumentDB 8.0+ support | **roadmap/planned** | unknown/unverified |
| Azure Cosmos DB 4.2+ (MongoDB API) support | **roadmap/planned** | unknown/unverified |
| Redis 7.0+ support | **roadmap/planned** | unknown/unverified |
| Anthropic AI provider | **unknown/unverified** | — |

Sources: https://visualeaf.com/docs/connection-manager, https://visualeaf.com/features/connection-manager/

---

## Gaps & Uncertainties

| Item | Detail |
|---|---|
| **Data Masking** | Available on Basic+ per pricing page but no dedicated documentation page found; implementation details **unknown/unverified** |
| **Anthropic AI** | Mentioned in FAQ but absent from Settings documentation — **unknown/unverified** |
| **Charts & Dashboards** | Resolved 2026-07-28: confirmed as a Core Feature on visualeaf.com and cross-referenced from Split Panel Views documentation; still **unknown/unverified** which chart types are supported and how dashboards (multi-chart composition) work — no dedicated feature page found (visualeaf.com/features/charts-dashboards/ returns 404) |
| **SQL Mode** | Resolved 2026-07-28: confirmed as a documented Core Feature (visualeaf.com/features/sql-mode/) — SQL syntax querying against MongoDB only, not a relational migration tool. See [F-SQL feature report](features/sql-tools/feature-report.md). Plan tier still **unknown/unverified** |
| **GridFS Viewer** | Added 2026-07-28: confirmed feature (visualeaf.com/features/gridfs-viewer/) — file browsing/preview/upload/download/metadata editing for GridFS storage. Plan tier **unknown/unverified** |
| **Split Panel Views** | Added 2026-07-28: confirmed feature (visualeaf.com/features/split-panel-views/) — multi-panel layouts with drag-and-drop tab management. Plan tier **unknown/unverified** |
| **MongoSync** | Added 2026-07-28: confirmed feature (visualeaf.com/features/mongosync/) — guided cross-server/cluster MongoDB-to-MongoDB data movement with selective sync, conflict handling, field filtering, transformation mappings, and scheduled jobs. Distinct from Collection Compare & Sync (GOV-collection-compare/GOV-collection-sync), which is a diff-then-directed-sync tool between already-linked collections; MongoSync is the broader migration/copy workflow (mapped to TRANSFER-import-mongo/TRANSFER-export-mongo). Plan tier: page mentions Pro tier inclusion but does not state this explicitly — **unknown/unverified** |
| **Open-source scope** | GitHub repo is "partially open source"; which modules are open vs proprietary is not documented |
| **MongoDB version matrix** | No published compatibility matrix; per-feature minimum versions noted (e.g., Hidden Index requires 4.4+) but no comprehensive table |
| **snappy/zstd compression** | Only zlib compression documented; MongoDB 4.2+ snappy/zstd support not referenced |
| **Team licensing / multi-seat** | Saved queries can be shared via JSON export but no explicit team seat management documented |
| **Export diagram format** | Visual Schema Designer export format not specified |
