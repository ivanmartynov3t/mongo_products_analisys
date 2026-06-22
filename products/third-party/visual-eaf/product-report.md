# VisuaLeaf — Product Report

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

---

## Feature Inventory

| Feature | Report | Matrix | Plan |
|---|---|---|---|
| Connectivity | [feature-report.md](features/connectivity/feature-report.md) | [feature-matrix.md](features/connectivity/feature-matrix.md) | All (Community: 3-connection cap) |
| Querying | [feature-report.md](features/querying/feature-report.md) | [feature-matrix.md](features/querying/feature-matrix.md) | All (Visual Query Builder: Basic+; AI Query: Professional) |
| Aggregation | [feature-report.md](features/aggregation/feature-report.md) | [feature-matrix.md](features/aggregation/feature-matrix.md) | All |
| Schema Validation | [feature-report.md](features/schema-validation/feature-report.md) | [feature-matrix.md](features/schema-validation/feature-matrix.md) | Basic+ |
| Indexing & Performance | [feature-report.md](features/indexing-performance/feature-report.md) | [feature-matrix.md](features/indexing-performance/feature-matrix.md) | All |
| Data Import/Export | [feature-report.md](features/data-import-export/feature-report.md) | [feature-matrix.md](features/data-import-export/feature-matrix.md) | Basic+ (Community: 0 tasks) |
| Visual Schema Designer | [feature-report.md](features/visual-schema/feature-report.md) | [feature-matrix.md](features/visual-schema/feature-matrix.md) | Basic+ |
| MongoDB Shell | [feature-report.md](features/shell/feature-report.md) | [feature-matrix.md](features/shell/feature-matrix.md) | All |
| AI Assistant | [feature-report.md](features/ai-assistant/feature-report.md) | [feature-matrix.md](features/ai-assistant/feature-matrix.md) | Professional only |
| Security & Governance | [feature-report.md](features/security-governance/feature-report.md) | [feature-matrix.md](features/security-governance/feature-matrix.md) | Basic+ (RBAC/Audit: Professional) |

---

## Editions & Pricing

| Edition | Price | Key Capabilities | Key Limits |
|---|---|---|---|
| **Community** | Free | Core querying, aggregation, shell, index management | 3 connections max; no Visual Query Builder; no Saved Queries; no Tasks; no Schema Validation; no Visual Schema; no RBAC |
| **Basic** | $42 one-time **or** $42/year | All Community + unlimited connections, Visual Query Builder, Saved Queries, up to 2 import/export tasks, Schema Validation, Visual Schema Designer, Data Masking | No AI Assistant; No RBAC Dashboard; No Collection Compare & Sync |
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
| **Chart Builder** | Referenced in "Open In" context menus and aggregation export, but no dedicated documentation found — **unknown/unverified** |
| **SQL Query Mode** | Listed in "Open In" context menu of query view but no documentation page found — **unknown/unverified** |
| **Open-source scope** | GitHub repo is "partially open source"; which modules are open vs proprietary is not documented |
| **MongoDB version matrix** | No published compatibility matrix; per-feature minimum versions noted (e.g., Hidden Index requires 4.4+) but no comprehensive table |
| **snappy/zstd compression** | Only zlib compression documented; MongoDB 4.2+ snappy/zstd support not referenced |
| **Team licensing / multi-seat** | Saved queries can be shared via JSON export but no explicit team seat management documented |
| **Export diagram format** | Visual Schema Designer export format not specified |

---

## Navigation

- [→ Connectivity](features/connectivity/feature-report.md)
- [→ Querying](features/querying/feature-report.md)
- [→ Aggregation](features/aggregation/feature-report.md)
- [→ Schema Validation](features/schema-validation/feature-report.md)
- [→ Indexing & Performance](features/indexing-performance/feature-report.md)
- [→ Data Import/Export](features/data-import-export/feature-report.md)
- [→ Visual Schema Designer](features/visual-schema/feature-report.md)
- [→ MongoDB Shell](features/shell/feature-report.md)
- [→ AI Assistant](features/ai-assistant/feature-report.md)
- [→ Security & Governance](features/security-governance/feature-report.md)
- [← Third-Party Products Index](../)
- [Comparison Reports](../../../reports/comparisons/)
