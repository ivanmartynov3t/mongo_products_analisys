# Cumulative Report

This report provides the top-level index for the MongoDB tools analysis project, tracking feature coverage, key findings, and navigation to all comparison artifacts.

**Last reviewed:** 2026-07-31 — corrections from [research/studio-3t-desktop-review-2026/](../research/studio-3t-desktop-review-2026/)

## Navigation

- [High-level product comparison](comparisons/high-level-product-comparison.md)
- [Low-level feature comparison](comparisons/low-level-feature-comparison.md)
- [Feature dictionary](../feature-dictionary.md)
- [Studio 3T product report](../products/3t/studio-3t/product-report.md)
- [MongoDB Compass product report](../products/third-party/mongodb-compass/product-report.md)
- [VisuaLeaf product report](../products/third-party/visual-eaf/product-report.md)
- [Gap analysis: NOT on any 3T product](gap-analysis-not-on-3t-products.md)
- [Gap analysis: NOT on Studio 3T Desktop](gap-analysis-not-on-3t-desktop.md)

## Comparison layers

| Layer | File | Purpose |
| --- | --- | --- |
| Sub-feature comparison | [low-level-feature-comparison.md](comparisons/low-level-feature-comparison.md) | Row-per-sub-feature detail with source citations and gap types |
| Product comparison | [high-level-product-comparison.md](comparisons/high-level-product-comparison.md) | Feature-area summaries, unique differentiators, edition/pricing constraints |
| This report | cumulative-report.md | Coverage overview, executive summary, competitive positioning |
| 3T-portfolio gap analysis | [gap-analysis-not-on-3t-products.md](gap-analysis-not-on-3t-products.md) | Sub-features confirmed absent or unverified across all 3T Software Labs products combined |
| 3T Desktop gap analysis | [gap-analysis-not-on-3t-desktop.md](gap-analysis-not-on-3t-desktop.md) | Sub-features not on the Studio 3T Desktop IDE specifically, including ones covered by other 3T products |

## Current scope

| Item | Count |
| --- | --- |
| Products analyzed | 3 (MongoDB Compass, VisuaLeaf, Studio 3T) |
| Feature areas | 11 (F-CONN through F-SCHED) |
| Feature matrices | 28 as last counted here — **stale**: the repository now has 35 `feature-matrix.md` files (3T Explore, 3T MCP, 3T Lens, 3T Access, and 3TL Bridge were split out of the Studio 3T product folder into their own products on 2026-07-29; not yet re-tallied in this row) |
| Sub-feature IDs in dictionary | 328 total in `feature-dictionary.md` as of 2026-07-31 (grew from 311 after the Studio 3T Desktop source-code re-audit added 17 new IDs — see [research/studio-3t-desktop-review-2026/12-consolidated-corrections.md](../research/studio-3t-desktop-review-2026/12-consolidated-corrections.md) §1). Note: the "257+ rows" figure previously shown here for `low-level-feature-comparison.md` is a separate, not-yet-reconciled count — it has not been independently re-verified against the new 328 dictionary total in this pass. |

## Feature coverage matrix

| Feature area | MongoDB Compass | VisuaLeaf | Studio 3T |
| --- | --- | --- | --- |
| F-CONN — Connectivity | ✓ confirmed | ✓ confirmed | ✓ confirmed |
| F-QUERY — Querying | ✓ confirmed | ✓ confirmed | ✓ confirmed |
| F-AGG — Aggregation | ✓ confirmed | ✓ confirmed | ✓ confirmed |
| F-SCHEMA — Schema | ✓ confirmed | ✓ confirmed | ✓ confirmed |
| F-IDX — Indexing & Performance | ✓ confirmed | ✓ confirmed | ✓ confirmed |
| F-TRANSFER — Data Transfer | — not applicable | ✓ confirmed | ✓ confirmed |
| F-SHELL — Shell | — not applicable | ✓ confirmed | ✓ confirmed |
| F-AI — AI features | ✓ partial (NL query only, added 2026-07-28) | ✓ confirmed | ✓ confirmed |
| F-SQL — SQL tools | — not applicable | ✓ partial (SQL Mode, query-only, added 2026-07-28) | ✓ confirmed |
| F-GOV — Governance | ✓ confirmed | ✓ confirmed | ✓ confirmed |
| F-SCHED — Task scheduler | — not applicable | ✓ confirmed | ✓ confirmed |

## Executive summary

### Product positioning

**MongoDB Compass** is a free, open-source GUI distributed by MongoDB Inc. as the official first-party tool. It covers the 6 core feature areas (connectivity, querying, aggregation, schema, indexing/performance, governance) and exclusively provides real-time server performance monitoring (mongostat/mongotop/currentOp), in-use encryption configuration (Queryable Encryption/CSFLE), Atlas Search/Vector Search index management, geo field schema analysis, and enterprise-grade policy enforcement (startup policy, CLI policy, network policy, AI controls with human approval gate, isolated edition). Compass requires no paid license for any of these capabilities. As of 2026-07-28, Compass's official product page also confirms a natural language query generation capability — a narrower AI feature set than Studio 3T or VisuaLeaf, but no longer a complete AI gap as previously documented.

**VisuaLeaf** (by SozoCode) is a subscription-based GUI targeting teams and individuals who prioritize schema design, visual query building, and modern UX. Its Community plan is the most restrictive (3 connections maximum, 0 scheduled tasks, no AI). The Basic+ tier unlocks VQB, schema validation, saved queries, and the ERD designer. The Professional tier adds AI, RBAC, audit log, collection compare/sync, and unlimited scheduled tasks. VisuaLeaf's exclusive capabilities include: a full visual ERD designer with graph-theory relationship detection, a standalone JSON Schema tree editor with all BSON types, a 6-step connection test wizard, a performance timer with color thresholds, an execution cancel button, pre-import JS transforms, server-side $pipeline pre-export transforms, P50/P95/P99 profiler percentiles with 4 recommendation types, 11 selectable OpenAI models with always-on plain-English explanations, a GridFS file viewer, split-panel workspace layouts, and MongoSync (guided cross-server MongoDB copy). VisuaLeaf also added SQL Mode (2026-07-28) — SQL syntax querying against MongoDB collections only, not a relational migration tool. VisuaLeaf is a polyglot database GUI (also natively connecting to PostgreSQL, MySQL, SQL Server, Oracle, and others); this analysis covers its MongoDB-facing capabilities only.

**Studio 3T** (by 3T Software Labs) is the most feature-complete product in this analysis, covering all 11 feature areas. Its Base/Pro editions add SQL tools, data masking, incremental export, team-connection sharing, SQL migration, and task scheduling. The Ultimate edition unlocks enterprise auth (Kerberos/LDAP/AWS IAM/OIDC). Studio 3T is the only product with a full SQL migration/export toolchain (SQL querying, JOIN→$lookup translation, migration wizard, relational export — VisuaLeaf has query-only SQL Mode as of 2026-07-28), date tags (~20 shortcuts for time-range queries), an MCP server + MCP client ecosystem enabling AI agents in VS Code/Cursor/Claude Desktop to operate against MongoDB, data masking with 19 operation types, incremental export with 5 resume points, index copy-paste across connections, a Query Assist shell mode with per-query pinnable result tabs, and the 3T enterprise platform organized into three tracks: Build (Desktop IDE, 3T Explore browser IDE, 3T MCP), Pipeline (3TL Bridge CDC), and Governed Access (3T Lens, 3T Access). Studio 3T also states compatibility with FerretDB alongside DocumentDB and Cosmos DB.

---

### Key competitive gaps

#### Compass is the only product that provides:
- Queryable Encryption (QE) and CSFLE in-use encryption configuration
- Real-time live server performance monitoring (mongostat/mongotop/currentOp) with pause/play
- Atlas Search and Vector Search index creation + status tracking
- Geo field schema analysis with map-backed interactive filter drawing
- Enterprise policy enforcement: startup policy (EJSON/YAML), CLI policy, network policy, telemetry config
- AI controls with human approval gate
- Multiple concurrent active connections (1.44.0+)

#### VisuaLeaf is the only product that provides:
- Visual ERD designer (infinite canvas, graph-theory relationship detection, named exportable layouts) — Basic+
- Full tree-based JSON Schema editor with BSON type support and polymorphic field handling — Basic+
- 6-step connection test wizard validating each phase individually (Network/SSH/TLS/Auth/DB/Permissions)
- Pre-import document filter conditions (include/exclude docs before import)
- User-defined JavaScript document transforms during import
- Server-side $pipeline pre-export transform
- P50/P95/P99 latency percentile lines in profiler with 4 actionable index recommendation types
- Profiler data export (CSV or JSON)
- 11 selectable OpenAI model choices (gpt-4o through gpt-3.5-turbo)
- Always-on plain-English explanation for every AI-generated query
- "Send sample data" privacy toggle (ON = Better Accuracy / OFF = More Private)
- Performance execution timer (amber at 2s, red at 5s) + cancel button
- Multiple concurrent shell sessions, background execution, auto-reconnect, persistent session variables
- DocumentDB 8.0+ and Cosmos DB 4.2+ compatibility (roadmap Q2 2026)
- GridFS file viewer (browse, preview, bulk upload/download, metadata editing) — added 2026-07-28
- Split panel workspace views (horizontal/vertical/nested, drag-and-drop tabs) — added 2026-07-28
- MongoSync guided cross-server/cluster MongoDB copy with selective sync, field filtering, and scheduled jobs — added 2026-07-28
- Native support for non-MongoDB database engines (PostgreSQL, MySQL, SQL Server, Oracle, and others) in the same client — out of scope for this repository's MongoDB-focused analysis

#### Studio 3T is the only product that provides:
- A full SQL migration/export toolchain: SQL querying (SELECT/WHERE/JOIN/GROUP BY/ORDER BY/HAVING) with JOIN→$lookup translation, a migration wizard, and relational export (VisuaLeaf added query-only SQL Mode against MongoDB in 2026-07-28 research — no migration/export)
- SQL migration wizard supporting 6 dialects (MySQL/PostgreSQL/Oracle/SQL Server/Sybase/IBM DB2 → MongoDB), up from the previously documented 4 — Sybase and IBM DB2 are both Enterprise-gated and asymmetric (Sybase has no direct SQL-export-wizard target; DB2 is migration-only)
- SQL export to relational targets (MySQL/MSSQL/Oracle/PostgreSQL/IBM DB2/Sybase)
- Date tags (~20: #today/#yesterday/#lastNdays/#lastcalweek/#thismonth etc.) — all editions, all query contexts
- MCP server (HTTP at 127.0.0.1:27117, 10 tools) enabling external AI agents (VS Code Copilot, Cursor, Claude Desktop) to operate on MongoDB
- 59 MCP tools via 3T Lens platform
- stt-cli standalone binary with PII scanner
- Data masking with 19 field-level operation types across 6 BSON-type categories (standalone tool + inline during Import/Export) — corrected 2026-07-31 from a previously documented count of 8
- Incremental export with up to 5 persistent resume points
- Index definition copy-paste across collections and connections
- SSH Profiles (named/reusable; password updates propagate to all connections)
- 4-mode proxy (Direct/App default/Custom HTTP/Custom SOCKS) per connection
- Team connection sharing (invite by email; Manage/Edit/View permissions) — Pro/Base+
- Query Assist shell mode: per-query pinnable result tabs, Visual Explain, 9-language code gen from shell
- Import connections from Robo 3T, Robomongo, NoSQLBooster, .uri files
- 3T enterprise platform: 3T Explore (governed browser IDE), 3T Lens (CDC/Kafka/Google Pub/Sub/HTTP), 3T Access (RBAC), 3TL Bridge (event streaming), Kubernetes Helm chart, OIDC multi-provider
- Stated FerretDB compatibility (alongside DocumentDB and Cosmos DB) — added 2026-07-28

---

### Unverified items requiring follow-up

| Product | Sub-feature | Status |
| --- | --- | --- |
| VisuaLeaf | AGG-stage-toggle (enable/disable stage without deletion) | Unknown/unverified |
| VisuaLeaf | AGG code generation to driver languages | Unknown/unverified |
| VisuaLeaf | AGG create MongoDB view from pipeline | Unknown/unverified |
| VisuaLeaf | SCHEMA-validation-strictness (warn/error action, strict/moderate level) | Unknown/unverified |
| VisuaLeaf | IDX-hide-unhide (hide index for A/B testing) | Unknown/unverified |
| VisuaLeaf | QUERY-charts-dashboards (chart types, dashboard composition) | Unknown/unverified |
| VisuaLeaf | Plan tier for GridFS Viewer, Split Panel Views, MongoSync, and SQL Mode | Unknown/unverified |
| Compass | AI feature depth beyond confirmed NL query (pipeline generation, schema-awareness, model/provider choice, privacy controls) | Unknown/unverified |
| Studio 3T | 3T Explore edition/plan requirement | Unknown/unverified |
| Studio 3T | FerretDB compatibility depth (which features work against FerretDB) | Unknown/unverified |

### Known issues

| Product | Sub-feature | Issue |
| --- | --- | --- |
| Studio 3T | IDX-type-haystack | geoHaystack index surfaced in UI without deprecation warning; deprecated in MongoDB 4.4, removed in 5.0 — users on MongoDB 5.0+ will encounter an error |
| Compass | SCHEMA-file-export | Export fails if schema has >1000 distinct fields; also blocks validation workflow at that threshold |

---

### Edition and plan access summary

| Capability | Compass | VisuaLeaf | Studio 3T |
| --- | --- | --- | --- |
| Free tier restrictions | None (all features free) | Community: max 3 connections, 0 scheduled tasks, no AI, Basic-gated VQB/schema | Free edition: no SQL, no masking, no task save, no team sharing |
| Visual Query Builder | N/A | Basic+ ($) | All editions (free) |
| AI query/pipeline builder | N/A | Professional ($$$) | Pro/Base+ ($$) |
| Enterprise auth (Kerberos/LDAP/AWS/OIDC) | Free | LDAP/AWS free; others roadmap | Ultimate ($$$) |
| SQL tools | N/A | Plan tier unverified (SQL Mode — query-only) | Pro/Base+ ($$) |
| Data masking | N/A | Basic/Professional (query-result masking; no import/export masking tool) | Pro/Base+ ($$) |
| Task scheduler | N/A | Community: 0; Basic: 2; Pro: unlimited | Pro/Base+ |
| Team connection sharing | N/A | N/A | Pro/Base+ |
| Schema validation + deploy | Free | Basic+ | N/A |
| Visual ERD designer | N/A | Basic+ | N/A |
| RBAC + audit log | N/A | Professional | Via platform (enterprise) |
| Collection compare + sync | N/A | Professional | Pro/Base+ |
| Atlas Search / Vector Search | Free (requires Atlas or MongoDB 7.0+) | N/A | N/A |

---

*Analysis covers publicly available documentation as of the matrix capture dates. Items marked unknown/unverified require direct product testing or vendor confirmation.*

*Last updated 2026-07-28: reviewed studio3t.com, mongodb.com/products/tools/compass, and visualeaf.com homepages (plus targeted verification fetches). See the "2026-07-28 update scope" note in the [low-level comparison](comparisons/low-level-feature-comparison.md#2026-07-28-update-scope) for exactly what was and was not re-verified in this pass.*

*Updated 2026-07-29: every row across all three comparison-layer reports was cross-checked directly against each product's own `feature-matrix.md` files. Six data-entry errors were found and fixed (Studio 3T's enterprise auth was wrongly marked unsupported; VisuaLeaf's live syntax validation, run-to-cursor, per-query result tabs, AI provider support, and data masking were wrongly marked unverified/absent) plus one missing row added (SQL-query-manager). See the "2026-07-29 deep-file verification pass" note in the [low-level comparison](comparisons/low-level-feature-comparison.md#2026-07-29-deep-file-verification-pass) for the full list. 3T Explore, 3T MCP, 3T Lens, 3T Access, and 3TL Bridge were also split out of the Studio 3T product folder into their own product folders under `products/3t/` on 2026-07-29 — see [products/3t/README.md](../products/3t/README.md).*

*Updated 2026-07-31: propagated corrections from a full Studio 3T Desktop source-code re-audit (`research/studio-3t-desktop-review-2026/`, consolidated in [12-consolidated-corrections.md](../research/studio-3t-desktop-review-2026/12-consolidated-corrections.md)). Key changes reflected above: data masking corrected from 8 to 19 operation types; SQL migration dialect count corrected from 4 to 6 (adds Sybase, IBM DB2 — both Enterprise-gated and asymmetric); the feature-dictionary sub-feature-ID total grew from 311 to 328 (17 new IDs, all Studio-3T-Desktop-confirmed and unverified elsewhere pending independent confirmation). Not yet reconciled in this pass: the "257+ rows" low-level-comparison count against the new 328-ID dictionary total; the stale "28 feature matrices" figure against the real count of 35; row-level edits to the comparison reports for the F-SCHEMA gap narrowing (13→9 confirmed-absent IDs), the F-SCHED completeness downgrade, the F-IDX completeness upgrade, the VQB "one-way handoff" (not bidirectional sync) correction, and the F-GOV audit-logging scope narrowing — see the consolidated-corrections file, §§2-11, for the full detail those reports still need applied.*
