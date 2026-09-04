# High-Level Product Comparison

This report summarizes each product's positioning, feature breadth, and key gaps across the 11 analyzed feature areas.

## Navigation

- [Cumulative report index](../cumulative-report.md)
- [Low-level feature comparison](low-level-feature-comparison.md)
- [Feature dictionary](../../feature-dictionary.md)
- [Studio 3T product report](../../products/3t/studio-3t/product-report.md)
- [MongoDB Compass product report](../../products/third-party/mongodb-compass/product-report.md)
- [VisuaLeaf product report](../../products/third-party/visual-eaf/product-report.md)
- [DBeaver product report](../../products/third-party/dbeaver/product-report.md)
- [DataGrip product report](../../products/third-party/datagrip/product-report.md)

**Last reviewed:** 2026-09-04 — added DataGrip (Plan 4, `update-plans/04-extend-competitor-coverage.md`)

## Compared products

| Product | Vendor | Type | Edition model |
| --- | --- | --- | --- |
| MongoDB Compass | MongoDB Inc. | Desktop GUI | Free / open-source |
| VisuaLeaf | SozoCode | Desktop GUI + web | Community / Basic / Professional (subscription) |
| Studio 3T | 3T Software Labs | Desktop GUI | Free / Base / Pro / Ultimate |
| DBeaver | DBeaver Corporation | Desktop GUI (Eclipse RCP) + web (CloudBeaver) | Community (free/OSS) / Lite / Enterprise / Ultimate / Team (subscription) |
| DataGrip | JetBrains | Desktop GUI (IntelliJ platform) | Free non-commercial / Individual / Business (subscription); AI Free / AI Pro Add-on |

## Product-level comparison (feature areas present)

| Feature area | Studio 3T | MongoDB Compass | VisuaLeaf | DBeaver | DataGrip |
| --- | --- | --- | --- | --- | --- |
| F-CONN — Connectivity | ✓ | ✓ | ✓ | ✓ | ✓ (thin — general connectivity architecture, not MongoDB-specific) |
| F-QUERY — Querying | ✓ | ✓ | ✓ | — (see F-SQL) | — (see F-SQL) |
| F-AGG — Aggregation | ✓ | ✓ | ✓ | ✓ (partial — text-based JSON console, no visual builder) | — (confirmed absent — no visual or text pipeline builder at all; hand-coded JSON in a text console) |
| F-SCHEMA — Schema | ✓ | ✓ | ✓ | ✓ (partial — generic column listing + confirmed BSON fidelity bugs) | — (confirmed absent — basic tabular/tree rendering only, no analytics) |
| F-IDX — Indexing & Performance | ✓ | ✓ | ✓ | — | — |
| F-TRANSFER — Data Transfer | ✓ | — | ✓ | ✓ (unverified depth) | — |
| F-SHELL — Shell | ✓ | — | ✓ | — | — |
| F-AI — AI features | ✓ | 🧪 (partial — NL query only) | ✓ | ✓ | ✓ (agentic MCP tooling — deepest MCP tool inventory reviewed) |
| F-SQL — SQL tools | ✓ | — | 🧪 (partial — SQL Mode query-only, no migration) | ✓ (primary MongoDB query surface — SQL-first architecture) | ✓ (primary and only MongoDB query surface — SQL-to-JS translation) |
| F-GOV — Governance | ✓ | ✓ | ✓ | ✓ | — (only governance-adjacent mechanism is an AI consent gate, tracked under F-AI instead) |
| F-SCHED — Task scheduler | ✓ | — | ✓ | ✓ (partial — Enterprise/Ultimate only) | — (2026.2 "CLI data-source management" is connection config, not task scheduling — see product report) |

DBeaver has no F-QUERY folder: MongoDB is queried through a generic, engine-agnostic SQL Console (confirmed via MongoDB's own "SQL Interface" documentation), not a native filter-bar/tree-view surface — see [DBeaver's product report](../../products/third-party/dbeaver/product-report.md) for the full reasoning. DBeaver has no F-IDX or F-SHELL folder: the source material does not discuss MongoDB index management or a shell/scripting environment for DBeaver.

DataGrip has no F-QUERY folder for the same reason: its own source is even more categorical than DBeaver's, stating MongoDB access "relies on translating queries into standard SQL rather than offering a native document workspace," confirmed by JetBrains' own "SQL for MongoDB" documentation — tracked under F-SQL. DataGrip has no F-AGG or F-SCHEMA folder at all (confirmed absent by direct statement in the source, not merely unverified): no visual/text pipeline builder and no schema-analysis surface beyond basic grids. DataGrip has no F-IDX, F-TRANSFER, or F-SHELL folder: none is discussed for MongoDB in the source. DataGrip has no F-GOV folder: its only governance-adjacent mechanism — a 4-category AI-action consent gate (Schema/Data Access, Schema/Data Modification) — is an AI execution safeguard, tracked under F-AI's `AI-safety-guards` instead (the same judgment applied to DBeaver's AI guardrails). DataGrip has no F-SCHED folder: its 2026.2 "CLI data-source management" is command-line connection configuration, not task/script scheduling, and does not fit any existing sub-feature ID — see [DataGrip's product report](../../products/third-party/datagrip/product-report.md).

## Icon legend (normalized status)

| Icon | Meaning |
| --- | --- |
| ✅ | confirmed |
| 🧪 | partial / limited |
| 🗺️ | roadmap / planned |
| ❓ | unknown / unverified |
| ❌ | not supported |
| 💼 | paid-tier only |
| 🏢 | enterprise-tier only |
| 🔌 | integration/platform-dependent |
| ⚠️ | contradictory source or caveat |
| ⛔ | blocked by edition/policy/runtime |

## Icon-only quick scan (key sub-features)

| Feature ID | Sub-feature ID | Sub-feature name | Studio 3T | MongoDB Compass | VisuaLeaf | DBeaver | DataGrip |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F-CONN | CONN-topology | Topology types | ✅ | ✅ | ✅ | ❓ | ❓ (driver/connection type confirmed; topology detail unverified) |
| F-CONN | CONN-multi-active | Multiple concurrent connections | ❓ | ✅ | ❓ | ❓ | ❓ |
| F-CONN | CONN-read-pref | Read preference | ✅ | ❓ | ✅ | ❓ | ❓ |
| F-QUERY | QUERY-filter-bar | Filter bar / query editor | ✅ | ✅ | ✅ | ❌ (SQL Console instead — see F-SQL) | ❌ (SQL-to-JS translation instead — see F-SQL) |
| F-QUERY | QUERY-projection | Projection editor | ✅ | ✅ | ✅ | ❌ | ❌ |
| F-QUERY | QUERY-sort | Sort editor | ✅ | ✅ | ✅ | ❌ | ❌ |
| F-AGG | AGG-stage-count | Number of supported pipeline stages | ❓ | ❓ | ✅ | ❓ | ❌ (no pipeline builder of any kind) |
| F-AGG | AGG-editor-layout | Pipeline editor layout | ✅ | ✅ | ✅ | 🧪 (text-based JSON array console only) | ❌ (confirmed absent — hand-coded JSON in a generic text console) |
| F-AGG | AGG-stage-mgmt | Stage management operations | ✅ | ✅ | ✅ | ❌ | ❌ |
| F-SCHEMA | SCHEMA-sampling | Schema sampling configuration | ✅ | ✅ | ✅ | ❌ | ❌ (confirmed absent) |
| F-SCHEMA | SCHEMA-field-prob | Field probability statistics | ✅ | ✅ | ❌ | ❌ | ❌ |
| F-SCHEMA | SCHEMA-type-prob | Per-field BSON type probabilities | ✅ | ✅ | ❌ | ❌ | ❌ |
| F-IDX | IDX-inventory | Index list / inventory | ✅ | ✅ | ✅ | ❓ | ❓ |
| F-IDX | IDX-type-single | Single-field index | ✅ | ✅ | ✅ | ❓ | ❓ |
| F-IDX | IDX-type-compound | Compound index | ✅ | ✅ | ✅ | ❓ | ❓ |
| F-TRANSFER | TRANSFER-import-csv | CSV import | ✅ | ❌ | ✅ | ❓ | ❓ |
| F-TRANSFER | TRANSFER-import-json | JSON import | ✅ | ❌ | ✅ | ❓ | ❓ |
| F-TRANSFER | TRANSFER-import-bson | BSON / mongodump import | ✅ | ❌ | ✅ | ❓ | ❓ |
| F-SHELL | SHELL-engine | Shell engine and code editor | ✅ | ❌ | ✅ | ❓ | ❌ (no MongoDB shell surface; SQL console only) |
| F-SHELL | SHELL-autocomplete | Shell autocomplete | ✅ | ❌ | ✅ | ❓ | ❌ |
| F-SHELL | SHELL-validation | Live syntax validation | ✅ | ❌ | ✅ | ❓ | ❓ |
| F-AI | AI-nl-query | NL to find() query | 💼 | 🧪 | 💼 | 🧪 (generates SQL, not a native find() filter) | 🧪 (agentic chat generates/executes SQL, not a native find() filter) |
| F-AI | AI-nl-pipeline | NL to aggregation pipeline | 💼 | ❓ | 💼 | ❌ | ❌ (no aggregation surface exists at all) |
| F-AI | AI-explanation | Plain-English explanation always included | ❓ | ❓ | ✅ | ❓ | ❓ |
| F-SQL | SQL-expressions | SQL SELECT/WHERE/GROUP BY/HAVING | 💼 | ❌ | 🧪 (MongoDB-only, no migration) | ✅ (via MongoDB's own SQL Interface; primary MongoDB query surface) | ✅ (via JetBrains' own "SQL for MongoDB" docs; primary and only MongoDB query surface) |
| F-SQL | SQL-join-mapping | SQL JOIN → $lookup mapping | 🧪 (plain SQL text only; no visual editor; single equality conditions only) | ❌ | ❌ | ❓ | ❌ (confirmed absent — single equality condition only, no visual editor, no subqueries/USING) |
| F-SQL | SQL-code-gen | SQL query → driver language code gen | ✅ | ❌ | 🧪 (translation view only) | ❌ | 🧪 (translates to MongoDB shell JS only, not application driver languages) |
| F-GOV | GOV-readonly-mode | Protect / destructive-write prevention mode | 🧪 | ✅ | ❓ | ✅ (per-connection, client-side) | ❓ (not discussed) |
| F-GOV | GOV-network-policy | Network access policy | ❓ | ✅ | ❓ | ❓ | ❓ |
| F-GOV | GOV-telemetry | Telemetry opt-out/configuration | ❓ | ✅ | ❓ | ❓ | ❓ |
| F-SCHED | SCHED-task-types | Task types supported | ✅ | ❌ | 💼 | 🏢 (Enterprise/Ultimate only) | ❌ (no task automation; CLI data-source management is connection config, not scheduling) |
| F-SCHED | SCHED-types-time | Preset schedule types | ✅ | ❌ | ✅ | ❓ | ❌ |
| F-SCHED | SCHED-cron | Cron expression support | ✅ | ❌ | ✅ | ❓ | ❌ |

## Detailed iconized tables

These are icon-only analogs of the detailed comparison tables below. Product columns are iconized; non-product columns are preserved.

### Product-level comparison (feature areas present) — iconized

| Feature area | Studio 3T | MongoDB Compass | VisuaLeaf | DBeaver | DataGrip |
| --- | --- | --- | --- | --- | --- |
| F-CONN — Connectivity | ✅ | ✅ | ✅ | ✅ | 🧪 (thin, not MongoDB-specific) |
| F-QUERY — Querying | ✅ | ✅ | ✅ | ❌ | ❌ |
| F-AGG — Aggregation | ✅ | ✅ | ✅ | 🧪 | ❌ |
| F-SCHEMA — Schema | ✅ | ✅ | ✅ | 🧪 | ❌ |
| F-IDX — Indexing & Performance | ✅ | ✅ | ✅ | ❌ | ❌ |
| F-TRANSFER — Data Transfer | ✅ | ❌ | ✅ | 🧪 | ❌ |
| F-SHELL — Shell | ✅ | ❌ | ✅ | ❌ | ❌ |
| F-AI — AI features | ✅ | 🧪 | ✅ | ✅ | ✅ |
| F-SQL — SQL tools | ✅ | ❌ | 🧪 | ✅ | ✅ |
| F-GOV — Governance | ✅ | ✅ | ✅ | ✅ | ❌ |
| F-SCHED — Task scheduler | ✅ | ❌ | ✅ | 🧪 | ❌ |

### F-CONN — Connectivity — iconized

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf | DBeaver | DataGrip |
| --- | --- | --- | --- | --- | --- |
| Topology coverage | ✅ | ✅ | ✅ | ❓ | ❓ (connection type/driver confirmed; topology detail unverified) |
| Enterprise auth | 🏢 | ✅ | 🗺️ | 🏢 | ❓ (not discussed for MongoDB) |
| TLS | ✅ | ✅ | ✅ | ❓ (existence confirmed, depth unverified) | ❓ |
| SSH tunnel | ✅ | ✅ | ✅ | ❓ | ❓ |
| Proxy | ✅ | ✅ | ❓ | ❓ | ❓ |
| Connection pool params | ✅ | ❓ | ✅ | ❓ | ❓ |
| Connection organization | ✅ | ✅ | ✅ | ❓ | ❓ |
| In-use encryption (QE/CSFLE) | ❌ | ✅ | ❌ | ❓ | ❓ |
| Connection test validation | ❓ | ❓ | ✅ | ❓ | ❓ |
| Team sharing | 💼 | ❌ | ❌ | 🏢 (Team Edition/CloudBeaver) | ❓ (JetBrains Account syncs templates per-user, not team-permissioned sharing) |
| Credential storage | ✅ | ✅ | ✅ | ✅ (local keystore; external vault — see F-GOV) | ❓ (templates strip credentials before sync; storage mechanism not detailed) |
| MongoDB-alternative compatibility (FerretDB/DocumentDB/Cosmos) | ✅ | ❓ | 🗺️ | ❓ | ❓ |
| Read-only connection lock | 🧪 | ✅ | ❓ | ✅ (vendor-documented) | ❓ |
| Unique: Compass | — | ✅ | — | — | — |
| Unique: VisuaLeaf | — | — | 🗺️ | — | — |
| Unique: Studio 3T | ✅ | — | — | — | — |
| Unique: DBeaver | — | — | — | 100+ supported database engines via one JDBC-driver architecture | — |
| Unique: DataGrip | — | — | — | — | Git-committable, human-readable XML connection/query-file storage (`.idea/db-forest-config.xml`) |

### F-QUERY — Querying — iconized

*DBeaver: N/A — no native MongoDB filter-bar/tree-view surface; MongoDB is queried via a generic SQL Console, tracked under F-SQL instead (see [DBeaver's product report](../../products/third-party/dbeaver/product-report.md)).*
*DataGrip: N/A — no native MongoDB filter-bar/tree-view surface; MongoDB is queried via SQL-to-JS translation, tracked under F-SQL instead (see [DataGrip's product report](../../products/third-party/datagrip/product-report.md)).*

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Filter bar / autocomplete | ✅ | ✅ | ✅ |
| Visual Query Builder | ✅ | ❌ | 💼 |
| Date tags / shortcuts | ✅ | ❌ | ❌ |
| AI query builder | 💼 | ❌ | 💼 |
| Query history | 💼 | ✅ | 💼 |
| Saved queries / manager | ✅ | ✅ | 💼 |
| Multi-document update | ✅ | ❓ | ✅ |
| Performance timer | ❓ | ❓ | ✅ |
| Cancel in-flight query | ❓ | ❓ | ✅ |
| Explain view | ✅ | ✅ | ✅ |
| Export to driver language | ✅ | ✅ | ❓ |
| Undo/redo | ❓ | ❓ | ✅ |
| GridFS viewer | ❓ | ❓ | ✅ |
| Split panel views | ❓ | ❓ | ✅ |
| Charts & dashboards | ❓ | ❓ | ✅ |
| Unique: Compass | — | ✅ | — |
| Unique: VisuaLeaf | — | — | 🔌 |
| Unique: Studio 3T | ✅ | — | — |

### F-AGG — Aggregation — iconized

*DataGrip: N/A — confirmed absent. The source states directly that DataGrip "lacks a visual stage-by-stage pipeline builder," with multi-stage aggregations hand-coded as JSON in a text console; no matrix folder was created (see [DataGrip's product report](../../products/third-party/datagrip/product-report.md)).*

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf | DBeaver |
| --- | --- | --- | --- | --- |
| Stage count / coverage | ✅ | ✅ | ✅ | ❓ |
| Editor layout | ✅ | ✅ | ✅ | 🧪 (text-based JSON array console only) |
| Per-stage editing mode | ✅ | ✅ | ✅ | ❌ |
| Stage toggle (enable/disable) | ✅ | ✅ | ❓ | ❌ |
| Stage preview | ✅ | ✅ | ✅ | ❌ |
| Code generation | ✅ | ✅ | ❓ | ❓ |
| Create MongoDB view | ✅ | ✅ | ❓ | ❓ |
| Export pipeline results | ✅ | ✅ | ✅ | ❓ |
| Chart builder from output | ❌ | ❌ | ✅ | ❌ |
| Pipeline options | ✅ | ✅ | ✅ | ❓ |
| Switch collection mid-session | ✅ | ❓ | ❓ | ❓ |
| Date tags in $match | ✅ | ❌ | ❌ | ❌ |
| Execution timer + cancel | ❓ | ❓ | ✅ | ❓ |
| Unique: Compass | — | ✅ | — | — |
| Unique: VisuaLeaf | — | — | ✅ | — |
| Unique: Studio 3T | ✅ | — | — | — |
| Unique: DBeaver | — | — | — | (none — this is a confirmed competitive weakness, not a strength; see [DBeaver's aggregation feature report](../../products/third-party/dbeaver/features/aggregation/feature-report.md)) |

### F-SCHEMA — Schema — iconized

*DataGrip: N/A — confirmed absent. The source states directly that DataGrip "lacks comprehensive schema structural analysis, field type probability distribution charts, or document structure drift detection," rendering documents only in basic tabular grids or tree views; no matrix folder was created (see [DataGrip's product report](../../products/third-party/datagrip/product-report.md)).*

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf | DBeaver |
| --- | --- | --- | --- | --- |
| Field statistics analytics (probability/type/histogram) | ✅ | ✅ | ✅ | ❌ (generic column-metadata listing only, confirmed by direct contrast in source) |
| Geo field analysis | ❌ | ✅ | ❌ | ❓ |
| JSON schema editor | ❌ | ❌ | ✅ | ❓ |
| Schema validation deploy | ❌ | ✅ | ✅ | ❓ |
| Validation strictness (warn/error, strict/moderate) | ❌ | ✅ | ❓ | ❓ |
| Visual ERD designer | ❌ | ❌ | 💼 | ❓ |
| View creation from schema tool | ✅ | ❓ | ❓ | ❓ |
| Schema doc export | ✅ | ✅ | ✅ | ❓ |
| Explore docs by field presence | ✅ | ❓ | ❓ | ❓ |
| Rename field across all docs | ✅ | ❓ | ❓ | ❓ |
| BSON type fidelity (dates, ObjectId) | ❓ | ❓ | ❓ | ⚠️ (confirmed bugs: millisecond-precision truncation, ObjectId misinterpretation — 3 GitHub issues) |
| Schema/structure compare | 💼 (collection sync) | ❌ | 💼 | 🧪 (relational-DDL-oriented; reportedly weak on nested BSON) |
| Unique: Compass | — | ✅ | — | — |
| Unique: VisuaLeaf | — | — | ✅ | — |
| Unique: Studio 3T | ✅ | — | — | — |
| Unique: DBeaver | — | — | — | (none — schema tooling is a confirmed relative weakness) |

### F-IDX — Indexing & Performance — iconized

*DBeaver: N/A — the source material does not discuss MongoDB index management, explain plans, or a query profiler for DBeaver specifically.*
*DataGrip: N/A — the source's Explain Plan/diagnostic engine section names only relational engines (PostgreSQL, Redshift, MySQL, MariaDB, Oracle, SQL Server, Snowflake) as supported targets; no MongoDB index-management capability is discussed.*

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Index types supported | 🧪 | ❓ | 🧪 |
| Atlas Search / Vector Search | ❌ | ✅ | ❌ |
| Advanced index options | ❓ | ❓ | 🧪 |
| Collation index options | ✅ | ❓ | ✅ |
| Quick-action templates | ❌ | ❌ | ✅ |
| Copy/paste index across connections | ✅ | ❌ | ❌ |
| Hide/unhide index | ✅ | ✅ | ❓ |
| Visual Explain | ✅ | ✅ | ✅ |
| Profiler | ✅ | ❓ | ✅ |
| Profiler export | ❌ | ❌ | ✅ |
| Real-time performance monitoring | ✅ | ✅ | ❓ |
| Kill running operations | ❌ | ✅ | ✅ |
| Unique: Compass | — | ✅ | — |
| Unique: VisuaLeaf | — | — | ✅ |
| Unique: Studio 3T | ✅ | — | — |

### F-TRANSFER — Data Transfer — iconized

*MongoDB Compass: N/A — not supported.*
*DataGrip: N/A — no MongoDB import/export, migration, or masking capability is discussed in the source.*

| Dimension | Studio 3T | VisuaLeaf | DBeaver |
| --- | --- | --- | --- |
| Import formats | 💼 | ✅ | ❓ (CSV/table wizards asserted, no primary citation) |
| Export formats | 💼 | ✅ | ❓ (CSV/table wizards asserted, no primary citation) |
| Import write modes | ✅ | ✅ | ❓ |
| Document filter before import | ❌ | ✅ | ❓ |
| User-defined JS transform per document | ❌ | ✅ | ❓ |
| Server-side $pipeline pre-export transform | ❌ | ✅ | ❓ |
| Field mapping and rename | ✅ | ✅ | ❓ |
| Incremental export with resume points | ✅ | ❌ | ❓ |
| Data masking | 💼 | ❌ | ❓ |
| Task save for scheduler | 💼 | 💼 | ❓ |
| Export source granularity | ✅ | ❓ | ❓ |

### F-SHELL — Shell — iconized

*DBeaver: N/A — no MongoDB shell/scripting environment discussed in the source; its "SQL Console" is SQL-oriented and tracked under F-SQL.*
*DataGrip: N/A — no MongoDB shell/scripting environment discussed in the source; its only MongoDB query surface is the SQL-to-JS translation console, tracked under F-SQL.*

| Dimension | Studio 3T | VisuaLeaf |
| --- | --- | --- |
| Editor engine | ✅ | ✅ |
| Autocomplete | ✅ | ✅ |
| Live syntax validation | ✅ | ✅ |
| Run all / selection | ✅ | ✅ |
| Run to cursor line | ✅ | ✅ |
| Shell modes | ✅ | ❓ |
| Per-query result tabs (pinnable) | ✅ | 🧪 |
| Result views | ✅ | ✅ |
| Multiple concurrent sessions | 🧪 | ✅ |
| Background execution | ❌ | ✅ |
| Auto-reconnect | ❌ | ✅ |
| Persistent session variables | ❌ | ✅ |
| History with search/filter/preview | ✅ | ✅ |
| Open in shell from other tools | ✅ | ❌ |

### F-AI — AI Features — iconized

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf | DBeaver | DataGrip |
| --- | --- | --- | --- | --- | --- |
| NL → find() query | 💼 | 🧪 | 💼 | 🧪 (generates SQL, not a native find() filter) | 🧪 (agentic chat generates/executes SQL, not a native find() filter) |
| NL → aggregation pipeline | 💼 | ❓ | 💼 | ❌ | ❌ (no aggregation surface exists at all) |
| Plain-English explanation always on | ❓ | ❓ | ✅ | ❓ | ❓ |
| AI providers | ✅ | ❓ | 🧪 | ✅ (OpenAI/GPT-5 default, Azure OpenAI, Google Gemini, GitHub Copilot/Codex — widest documented list) | ✅ (Anthropic Claude Agent [Claude 4.5 Sonnet], OpenAI Codex; BYOK supported) |
| Model selection | ✅ | ❓ | ✅ | ❓ | ✅ (choice of Claude Agent or Codex) |
| "Send sample data" privacy toggle | ❓ | ❓ | ✅ | ❓ | ❓ |
| Conversation turns for refinement | ❓ | ❓ | ✅ | ❓ | ❓ |
| Multiple named AI configs | ❓ | ❓ | ✅ | ❓ | ❓ |
| API key storage | ❓ | ❓ | ✅ | ❓ | ❓ (BYOK tokens mentioned; storage mechanism not detailed) |
| File-attachment AI context (CSV/JSON/Parquet/XLSX) | ❓ | ❓ | ❓ | ✅ (unique mechanism — temp in-memory tables from attached files) | ❓ |
| Voice/speech-to-text AI input | ❓ | ❓ | ❓ | ❓ (claimed "v25.2," but no matching primary source in Works Cited) | ❓ (not discussed) |
| Execution safety guards + token analytics | ❓ | ❓ | ❓ | ❓ | ✅ (4-category consent gate: Schema Access/Data Access/Schema Modification/Data Modification; token-analytics half of the ID unverified) |
| Local MCP server | ✅ | ❌ | ❌ | ❓ (claimed "v26.1.2," but no matching primary source in Works Cited) | ✅ (14-tool database-specific MCP server, confirmed via JetBrains' own 2026.1 release notes) |
| MCP client integrations | ✅ | ❌ | ❌ | ❓ | ❓ (source describes only DataGrip's own embedded agent using its own MCP server — no confirmed external-client access) |
| Total MCP tools | 🔌 | ❌ | ❌ | ❓ | ✅ (14, individually named — most granular tool inventory reviewed) |
| stt-cli + PII scanner | ✅ | ❌ | ❌ | ❌ | ❌ |
| 3T Explore AI Helper | ✅ | ❌ | ❌ | ❌ | ❌ |

### F-SQL — SQL Tools — iconized

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf | DBeaver | DataGrip |
| --- | --- | --- | --- | --- | --- |
| SQL query syntax over MongoDB | ✅ | ❌ | 🧪 | ✅ (independently confirmed via MongoDB's own SQL Interface docs — primary MongoDB query surface) | ✅ (independently confirmed via JetBrains' own "SQL for MongoDB" docs and a 2020 feature-announcement blog post — primary and only MongoDB query surface) |
| SQL → MongoDB translation/code-gen | ✅ | ❌ | 🧪 | ❓ | 🧪 (translates to MongoDB shell JS only; no application driver-language code-gen) |
| SQL JOIN → $lookup visual mapping | ✅ | ❌ | ❓ | ❓ | ❌ (confirmed absent — single equality condition only, plain SQL text, no visual editor) |
| SQL migration wizard (relational → Mongo) | 💼 | ❌ | ❌ | ❌ | ❌ (confirmed absent, by direct contrast in source) |
| SQL export to relational targets | 💼 | ❌ | ❌ | ❌ | ❌ |
| Federated cross-database query | ❌ | ❌ | ❌ | ❌ | ✅ (`dg_cross`, DuckDB-backed; general capability confirmed, MongoDB-specific scope unverified — see [DataGrip's SQL Tools feature report](../../products/third-party/datagrip/features/sql-tools/feature-report.md)) |

### F-GOV — Governance — iconized

*DataGrip: N/A — the only governance-adjacent mechanism the source describes (a 4-category AI-action consent gate) is an AI execution safeguard, tracked under F-AI's `AI-safety-guards` instead; no RBAC, audit-log, data-masking, or platform-governance capability is discussed.*

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf | DBeaver |
| --- | --- | --- | --- | --- |
| Protect / write-prevention mode | 🧪 | ✅ | ❌ | ✅ (per-connection, client-side, vendor-documented) |
| Network policy | ❌ | ✅ | ❌ | ❓ |
| Telemetry configuration | ❌ | ✅ | ❌ | ❓ |
| Startup / CLI policy (EJSON/YAML) | ❌ | ✅ | ❌ | ❓ |
| Isolated / air-gapped edition | ❓ | ✅ | ✅ | ❓ |
| AI controls with human approval gate | ❌ | ✅ | ❌ | ❓ |
| External secrets manager integration (Vault/CyberArk/AWS Secrets Manager) | ❓ | ❓ | ❓ | ❓ (asserted, no primary citation in source's own Works Cited) |
| RBAC user/role management | 🔌 | ❌ | 💼 | ❓ (Team Edition/CloudBeaver RBAC mentioned only in passing) |
| Visual role inheritance tree | ❌ | ❌ | 💼 | ❓ |
| Audit log | 🧪 | ❌ | 💼 | ❓ |
| Collection compare (3-panel diff) | 💼 | ❌ | 💼 | 🧪 (relational-DDL-oriented schema compare, not a 3-panel collection-data diff; reportedly weak on nested BSON) |
| Collection sync with direction toggle | 💼 | ❌ | 💼 | ❓ |
| CDC pipeline (Kafka/Pub/Sub/HTTP) | 🔌 | ❌ | ❌ | ❌ |
| Kubernetes Helm chart | ✅ | ❌ | ❌ | ❌ |
| OIDC multi-provider for platform auth | ✅ | ❌ | ❌ | ❓ |
| Credential protection | ✅ | ✅ | ✅ | ✅ (local keystore baseline) |
| 3T Explore governed workspace (workspace switcher + access control) | ✅ | ❌ | ❌ | ❌ |

### F-SCHED — Task Scheduler — iconized

*MongoDB Compass: N/A — not supported.*
*DataGrip: N/A — its 2026.2 "CLI data-source management" feature is command-line connection-configuration management, not task/script scheduling, and does not fit any existing F-SCHED sub-feature ID (see [DataGrip's product report](../../products/third-party/datagrip/product-report.md)).*

| Dimension | Studio 3T | VisuaLeaf | DBeaver |
| --- | --- | --- | --- |
| Task types | ✅ | 💼 | 🏢 (Enterprise/Ultimate only) |
| Schedule options | ✅ | ✅ | ❓ |
| Timezone-aware with DST | ❓ | ✅ | ❓ |
| Execution config | ❓ | ✅ | ❓ |
| Task status states | ✅ | ✅ | ❓ |
| Task actions | ✅ | ✅ | ❓ |
| Email notifications | ✅ | 🔌 | ❓ |
| Multiple script units per task | ✅ | ❓ | ❓ |
| Compare/sync task with diff view | ✅ | ❌ | ❓ |
| Headless CLI automation | ❓ | ❓ | 🏢 (`dbvr`, unverified against a primary source) |
| Plan limits | 💼 | 💼 | 🏢 |

### Edition / pricing constraints — iconized

| Feature | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Visual Query Builder | ✅ | ❌ | 💼 |
| AI query builder | 💼 | ❌ | 💼 |
| Enterprise auth (Kerberos/LDAP/AWS/OIDC) | 🏢 | ✅ | 🗺️ |
| Shell / IntelliShell | ✅ | ❌ | ✅ |
| Data Transfer | 💼 | ❌ | ✅ |
| Team connection sharing | 💼 | ❌ | ❌ |
| Data masking | 💼 | ❌ | 💼 |
| SQL tools | 💼 | ❌ | 🧪 (tier unverified) |
| Task scheduler | 💼 | ❌ | 💼 |
| Query Manager (multi-type) | ✅ | ✅ | 💼 |
| Collection compare + sync | 💼 | ❌ | 💼 |
| RBAC dashboard | 🔌 | ❌ | 💼 |
| Audit log | 🧪 | ❌ | 💼 |
| Schema validation UI | ❌ | ✅ | 💼 |
| Visual ERD designer | ❌ | ❌ | 💼 |
| Atlas Search / Vector Search indexes | ❌ | ✅ | ❌ |

### DBeaver edition / pricing constraints — iconized

| Feature | Community (free) | Lite | Enterprise | Ultimate | Team / CloudBeaver |
| --- | --- | --- | --- | --- | --- |
| MongoDB connectivity at all | ❌ | ✅ | ✅ | ✅ | ❓ |
| Enterprise auth (SAML/Kerberos/Azure AD) | ❌ | ❓ | ✅ | ✅ | ❓ |
| External secrets manager (Vault/CyberArk/AWS Secrets Manager) | ❌ | ❓ | ❓ | ❓ | ❓ |
| Task Scheduler | ❌ | ❌ | ✅ | ✅ | ❓ |
| Headless CLI (`dbvr`) | ❓ | ❓ | ❓ | ❓ | ❓ |
| AI Assistant | ❓ | ❓ | ❓ | ❓ | ❓ |
| Team/RBAC workspace | ❌ | ❌ | ❌ | ❌ | ✅ |

Per-tier gating above the MongoDB-connectivity row is Confirmed via the source's own pricing/edition comparison table; per-tier gating of individual sub-capabilities below that row is largely Unverified — the source only states broad tier groupings without itemizing every capability per tier.

### DataGrip edition / pricing constraints — iconized

| Feature | Free non-commercial | Individual | Business | AI Free | AI Pro Add-on |
| --- | --- | --- | --- | --- | --- |
| MongoDB connectivity at all | ✅ | ✅ | ✅ | n/a | n/a |
| SQL-to-MongoDB translation (F-SQL) | ✅ (unverified whether restricted) | ✅ | ✅ | n/a | n/a |
| `dg_cross` federated queries | ❓ | ❓ | ❓ | n/a | n/a |
| Claude Agent / OpenAI Codex agentic chat | n/a | n/a | n/a | ✅ (baseline) | ✅ (full) |
| MCP server (14 tools) | ❓ | ❓ | ❓ | ❓ | ✅ (implied by AI Agentic Flow, exact AI Free vs. AI Pro split unverified) |

Confirmed via two independent JetBrains primary sources (DataGrip buy page, JetBrains Toolbox store page) that a Free non-commercial tier, a $109→$65/yr Individual tier, and a $259→$155/yr Business tier all exist, alongside a separately-priced AI Free/AI Pro Add-on split ($100/yr individual, $200/yr organization) — but the source does not itemize which specific AI Agentic Flow capabilities (agent choice, MCP tool access, consent-gate granularity) differ between AI Free and AI Pro, so those cells above are Unverified rather than assumed equal or gated.

## Deep-review coverage reconciliation

| Scope | Result |
| --- | --- |
| Product matrix IDs not present in low-level baseline table (before reconciliation pass) | 52 |
| Product matrix IDs missing from feature dictionary | 0 |
| Comparison-table IDs missing from feature dictionary | 0 |

Detailed additions are captured in the low-level report under **Reconciliation table (product-matrix IDs added by deep review)**.

## Feature-group comparison

*Scope note (2026-09-04): the detailed prose tables in this section were authored for Studio 3T, MongoDB Compass, and VisuaLeaf. DBeaver's and DataGrip's equivalent detail lives in their own `feature-report.md`/`feature-matrix.md` files under `products/third-party/dbeaver/features/` and `products/third-party/datagrip/features/` respectively, and is summarized at icon-scan granularity in the "iconized" tables above (per feature area) and in "Unique differentiators per product" and "Key gaps summary" below, rather than repeated row-by-row here.*

### F-CONN — Connectivity

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Topology coverage | Standalone, RS, Sharded, DNS SRV — all editions | Standalone, RS, Sharded, SRV; multiple concurrent (1.44.0+) | Standalone, RS (hidden nodes, resolve members), Sharded, DNS SRV + SRV Service Name override |
| Enterprise auth | Kerberos, LDAP, AWS IAM, OIDC — Ultimate edition only | Kerberos, LDAP, AWS IAM, OIDC — all confirmed | LDAP, AWS IAM confirmed; Kerberos + OIDC roadmap Q2 2026 |
| TLS | Own CA/OS-trusted/accept any; client PEM+passphrase; SNI; allow-invalid-hostnames toggle | CA/client cert/key/passphrase; validation toggles | Custom Root CA, OS Trust Store, Accept Any; mTLS cert+key+passphrase |
| SSH tunnel | Password + private key; SSH Profiles (named/reusable; password updates propagate) | Password + private key | Password or private key + optional passphrase |
| Proxy | 4 modes: Direct / App default / Custom HTTP / Custom SOCKS — per connection | SOCKS5 only | Not documented |
| Connection pool params | Full set incl. Azure idle-time workaround | Not documented | Full set incl. Retry Reads + zlib compression |
| Connection organization | Folders + drag-and-drop; per-tab color coding | Favorites, sidebar search | 3-level hierarchy (Project → Environment → Connection); Community max 3 |
| In-use encryption (QE/CSFLE) | — | ✓ (key vault + KMS config) | — |
| Connection test validation | Not documented as multi-step | Not documented | 6-step: Network/SSH/TLS/Auth/DB/Permissions |
| Team sharing | Pro/Base+: invite by email; Manage/Edit/View permissions | — | — |
| Credential storage | Built-in key store OR master password (cryptographic) | OS Keytar API | AES-256 local, never transmitted, air-gapped safe |
| MongoDB-alternative compatibility | FerretDB, Amazon DocumentDB, Azure Cosmos DB (per studio3t.com; depth unverified) | Not documented | DocumentDB/Cosmos DB/Redis — roadmap Q2 2026 |
| Unique: Compass | — | Multiple concurrent connections (1.44.0+); QE/CSFLE in-use encryption; required-access guide | — |
| Unique: VisuaLeaf | — | — | 6-step connection test wizard; URI export; DocumentDB/Cosmos DB roadmap Q2 2026 |
| Unique: Studio 3T | SSH Profiles; 4-mode proxy; read-only UI lock; team sharing; import from Robo 3T/NoSQLBooster/.uri | — | — |

**Assessment:** All three products cover core connectivity (standalone/RS/sharded/SRV, standard auth, TLS, SSH). Compass leads on in-use encryption and enterprise auth completeness. VisuaLeaf offers the best connection-test UX and uniquely plans DocumentDB/Cosmos compatibility. Studio 3T has the most advanced proxy, SSH, team-sharing, and credential-import capabilities.

---

### F-QUERY — Querying

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Filter bar / autocomplete | 5-field bar; full autocomplete incl. BSON wrappers; shorthand ObjectId | ✓ with examples/shortcuts | ACE editor + Ctrl+Space field-name autocomplete from schema |
| Visual Query Builder | All editions — AND/OR/NOR; BSON type auto-detected; Binary/Reference/Regex editors; one-way handoff to query bar/Aggregation Editor (no live bidirectional sync) | — | Basic+ — type-aware inputs (date pickers, sliders, booleans), AND/OR nested groups, bidirectional |
| Date tags / shortcuts | ~20 tags (#today/#yesterday/#lastNdays etc.) — all editions | — | — |
| AI query builder | Pro/Base+ — NL → query/pipeline; Azure AI / OpenAI GPT-4o / Anthropic | — | Professional — NL → find() + pipeline; 11 OpenAI models; plain-English explanation always on |
| Query history | Auto-save on run; shared folder save Pro/Base+ | Depth-capped recent list + save | Basic+ — per-collection with timestamp + exec time |
| Saved queries / manager | Query Manager — folders/drag-and-drop; 4 query types incl. SQL + Aggregation | My Queries + favorites | Basic+ — by collection or global; export/import JSON; team share |
| Multi-document update | Update Documents dialog (updateMany()); separate query+update tabs | Not documented | Table View Batch Update ($set/$unset/$inc/$push/$pull + preview) |
| Performance timer | Not documented as visual timer | Not documented | Amber at 2s; red at 5s |
| Cancel in-flight query | Not documented | Not documented | ✓ cancel button |
| Explain view | Visual Explain across 5 entry points | ✓ | Exec plan, index usage, docs examined vs returned, index suggestions |
| Export to driver language | 9 languages (adds MongoDB Shell) | 8 languages (Java/Node/C#/Python/Ruby/Go/Rust/PHP) | Not documented |
| Undo/redo | Not documented | Not documented | Ctrl+Z / Ctrl+Shift+Z |
| GridFS viewer | Not documented | Not documented | ✓ browse/preview/upload/download/metadata edit for GridFS files |
| Split panel views | Not documented | Not documented | ✓ horizontal/vertical/nested splits with drag-and-drop tabs |
| Charts & dashboards | Not documented | Not documented | ✓ confirmed as Core Feature; chart types/dashboard composition unverified |
| Unique: Compass | — | Collation in filter bar; max-time (60,000ms default) | — |
| Unique: VisuaLeaf | — | — | Performance timer; cancel button; Run Find One / Run Count variants; 7 "open in" integrations; undo/redo; batch update from table view; EJSON copy |
| Unique: Studio 3T | Date tags (~20); Query Manager with 4 query types; "open in Aggregation Editor" converts filter → $match+$project | — | — |

**Assessment:** Compass is the only product with collation in the filter bar. VisuaLeaf has the most user-friendly query execution UX (timer, cancel, run-variants, undo/redo). Studio 3T's date tags and Query Manager are unique value adds for power users. VQB is absent in Compass; VisuaLeaf's is plan-gated; Studio 3T's is available on all editions. Note: Studio 3T's VQB hands off to the query bar/Aggregation Editor via a one-way "Open in..." action, not a live bidirectional sync.

---

### F-AGG — Aggregation

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Stage count / coverage | All standard stages | All standard stages | 37+ stages incl. $densify/$fill/$setWindowFields/$search/$documents/$listSearchIndexes |
| Editor layout | 5-region UI: Pipeline panel, Stage editor, Stage I/O, Pipeline output, Query Code + Explain tab | Stage View, Stage Wizard, Focus Mode, Text View | Visual pipeline canvas with stage cards |
| Per-stage editing mode | Code editor only | Stage Wizard + per-stage mode switching | Form Mode (VQB/$group accumulator builder) OR Monaco editor per stage; preference saved |
| Stage toggle (enable/disable) | ✓ confirmed | ✓ confirmed | Unknown/unverified |
| Stage preview | Stage I/O panels per stage | Sampled preview per stage | Input/Output split-view; 20-doc sample; Auto-Preview toggle |
| Code generation | 9 generators via single dropdown (7 target languages: MongoDB Shell, JavaScript/Node.js, Java, C#, Python, PHP, Ruby; Java offers 2.x/3.x/4.x driver-API variants — no separate sub-tabs); "Open in IntelliShell" button | Major driver languages | Not documented |
| Create MongoDB view | ✓ (requires MongoDB 3.4+) | ✓ | Not documented |
| Export pipeline results | Export Wizard from Pipeline output or Stage I/O | JSON/CSV + Extended JSON | JSON, CSV, BSON, SQL INSERT statements |
| Chart builder from output | — | — | ✓ opens Chart Builder |
| Pipeline options | allowDiskUse, custom collation, index hint | Custom collation + pipeline maxTimeMS | Allow Disk Use, Max Time 300s, Auto Collapse |
| Switch collection mid-session | ✓ | Not documented | Not documented |
| Date tags in $match | ✓ all editions | — | — |
| Execution timer + cancel | Not documented | Not documented | ✓ real-time timer + cancel |
| Unique: Compass | — | Stage Wizard mode (GUI form for stage params) | — |
| Unique: VisuaLeaf | — | — | 37+ stages (widest coverage); Form Mode with VQB for $match + accumulator builder for $group; chart builder from output; execution timer + cancel |
| Unique: Studio 3T | Aggregation code gen (9 generators, 7 target languages via single dropdown); date tags in $match; switch collection mid-session; clipboard copy of full pipeline JSON | — | — |

**Assessment:** VisuaLeaf has the widest stage coverage and the most ergonomic per-stage editing (Form Mode). Studio 3T has the most powerful code-gen and integration options. Compass's Stage Wizard provides good accessibility for less-experienced users. Stage toggle availability is confirmed for Compass and Studio 3T but unverified in VisuaLeaf.

---

### F-SCHEMA — Schema

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Field statistics analytics (probability/type/histogram) | ✓ (field prob, type prob, histogram, top values, date distributions) | ✓ (field prob, type prob, histogram) | — (no analytics) |
| Geo field analysis | — | ✓ (map-backed, interactive filter drawing, geo query generation) | — |
| JSON schema editor | — | — | ✓ tree editor (expand/collapse, drag-to-reorder, required toggle, View/Edit toggle, polymorphic types) |
| Schema validation deploy | — | ✓ via UI workflow | ✓ push to collection as $jsonSchema |
| Validation strictness (warn/error, strict/moderate) | N/A | ✓ confirmed | Unknown/unverified |
| Visual ERD designer | — | — | ✓ Basic+ (infinite canvas; graph-theory relationship detection; 11 color presets; named layouts; export/import) |
| View creation from schema tool | ✓ db.createView() builder — all editions | Not documented | Not documented |
| Schema doc export | Word (.docx) or CSV with field names/types/probabilities | Multiple formats (fails if >1000 distinct fields) | $jsonSchema-compatible JSON |
| Explore docs by field presence | ✓ right-click → opens Collection Tab with {$exists} filter | Not documented | Not documented |
| Rename field across all docs | ✓ via schema tree outlier workflow | Not documented | Not documented |
| Unique: Compass | — | Geo field analysis with interactive map and geo-query generation | — |
| Unique: VisuaLeaf | — | — | Full JSON schema tree editor with BSON types; visual ERD designer with relationship detection |
| Unique: Studio 3T | Field statistics analytics (top values, date distributions); explore docs by field presence; rename field workflow; create view from schema | — | — |

**Assessment:** Compass and Studio 3T provide rich schema analytics (field probability, histograms). Compass adds geo analysis. VisuaLeaf uniquely offers a full JSON schema editor and a visual ERD designer with graph-theory relationship detection. Compass and VisuaLeaf have schema validator deploy; Studio 3T does not. Studio 3T has the most schema-to-data-repair workflows (explore, rename, view creation).

---

### F-IDX — Indexing & Performance

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Index types supported | single, compound, text, wildcard, TTL, 2d, 2dsphere, geoHaystack (deprecated — no warning shown), partial, sparse, hidden | single, compound, TTL, unique, sparse, partial, hidden (others not documented) | single, compound, text, wildcard, hashed, TTL, 2d, 2dsphere, partial, sparse, hidden |
| Atlas Search / Vector Search | — | ✓ (Atlas M10+ or local MongoDB 7.0+) | — |
| Advanced index options | Not documented as grouped options | Not documented | Partial Filter Expression (JSON editor), Wildcard Projection, Storage Engine config, Commit Quorum, Clustered index |
| Collation index options | Locale + strength only | Not documented | 60+ ICU locales; Strength 1-5; Case First/Level/Numeric/Alternate/Backwards |
| Quick-action templates | — | — | 4 templates (Wildcard Text/$**/\_id/createdAt) |
| Copy/paste index across connections | ✓ Professional tier and above — even across different connections | — | — |
| Hide/unhide index | ✓ (MongoDB 4.4+) | ✓ | Unknown/unverified |
| Visual Explain | ✓ plan + execution stats; hover tooltips; JSON fragment view; available in 5 contexts | ✓ plan + execution stats | Exec plan, index usage, docs examined vs returned, index suggestions |
| Profiler | system.profile reader; levels 0/1/2; exact query vs shape grouping; 5 drilldown actions | Not documented in matrix | Slow query threshold; levels 0/1/2; sample rate; P50/P95/P99 percentiles; COLLSCAN flagging; 4 recommendation types; CSV/JSON export |
| Profiler export | — | — | ✓ CSV or JSON |
| Real-time performance monitoring | ✓ mongostat/currentOp equivalent (Server Status Charts + Task Monitor tabs) | ✓ mongostat/mongotop/currentOp; pause/play | Not documented |
| Kill running operations | — | ✓ (requires killop privilege) | ✓ kill button per operation |
| Unique: Compass | — | Atlas Search + Vector Search index creation | — |
| Unique: VisuaLeaf | — | — | P50/P95/P99 profiler percentiles; 4 index recommendation types; profiler export; hashed index; 60+ ICU locale collation; Commit Quorum; clustered index; 4 quick-action templates |
| Unique: Studio 3T | Index copy-paste across connections (Professional tier+); real-time monitoring (mongostat/currentOp equivalent); geoHaystack (unwarned deprecation); Explain available in 5 contexts incl. SQL Query + IntelliShell | — | — |

**Assessment:** Compass exclusively supports Atlas Search and Vector Search. VisuaLeaf has the most complete index type coverage and the most sophisticated profiler (P50/P95/P99, 4 recommendation types, export). Studio 3T's Explain is available in the widest set of contexts, and it also has a mongostat/currentOp-equivalent real-time monitoring capability (Server Status Charts + Task Monitor tabs) — previously underdocumented and not exclusive to Compass. Note: geoHaystack displayed by Studio 3T without deprecation warning is a confirmed bug.

---

### F-TRANSFER — Data Transfer

*MongoDB Compass: N/A — not supported*

| Dimension | Studio 3T | VisuaLeaf |
| --- | --- | --- |
| Import formats | JSON, CSV, BSON, SQL (Pro/Base+), cross-server MongoDB | JSON, CSV, BSON |
| Export formats | JSON, CSV, BSON, Excel (.xlsx), SQL (Pro/Base+), cross-server MongoDB | JSON, CSV, BSON, SQL INSERT statements |
| Import write modes | 5 modes: Insert/fail, Insert/ignore, Upsert, Merge, Replace | Upsert only |
| Document filter before import | — | ✓ include/exclude by condition |
| User-defined JS transform per document | — | ✓ |
| Server-side $pipeline pre-export transform | — | ✓ |
| Field mapping and rename | ✓ (CSV/SQL path) | ✓ |
| Incremental export with resume points | ✓ up to 5 historical resume points; does NOT track updates to existing docs | — |
| Data masking | ✓ Pro/Base+: 19 masking operations (+1 no-op state) across 6 BSON-type categories; inline during Import/Export; standalone tool | — |
| Task save for scheduler | ✓ Pro/Base+ | ✓ (Basic: 2; Professional: unlimited) |
| Export source granularity | 6 sources: entire collection / view / find() result / aggregation result / current cursor / selected documents | Not documented |

**Assessment:** Studio 3T has deeper export/import format coverage (SQL, Excel, cross-server MongoDB), more import modes, data masking, and incremental export. VisuaLeaf uniquely offers pre-import JS transforms, document filter conditions, and server-side $pipeline pre-export transforms — better for ETL scenarios. VisuaLeaf's plan limits (Community = 0 tasks) are more restrictive.

---

### F-SHELL — Shell

*MongoDB Compass: N/A — not supported*

| Dimension | Studio 3T | VisuaLeaf |
| --- | --- | --- |
| Editor engine | ACE editor (format code Ctrl+Alt+L, line comments Ctrl+/) | Monaco (minimap, multi-session) |
| Autocomplete | Ctrl+Space — JS functions, shell types/methods, operators, collection names, field names | Contextual |
| Live syntax validation | ✓ red gutter markers + right-ruler | ✓ real-time highlighting; failed execution line highlighted red |
| Run all / selection | ✓ F5 (all) / F9 or Ctrl+Enter (selection) | ✓ |
| Run to cursor line | ✓ F6 | ✓ Ctrl+Shift+F5 |
| Shell modes | Shell mode (all → Raw tab) vs Query Assist mode (per-query editable result tabs; Visual Explain; destructive op warnings) | Not documented as named modes |
| Per-query result tabs (pinnable) | ✓ pin tab persists across re-runs | Separate per-query result tab confirmed; pin/keep-across-re-run behavior unconfirmed |
| Result views | Tree View, Table View, JSON/BSON View, Query Code tab (9 languages), Visual Explain tab | Tree View, Table View, BSON View |
| Multiple concurrent sessions | Single session per tab | ✓ |
| Background execution | — | ✓ |
| Auto-reconnect | — | ✓ |
| Persistent session variables | — | ✓ |
| History with search/filter/preview | Auto-save on run; navigable | ✓ |
| Open in shell from other tools | ✓ from Collection Tab, Aggregation Editor, Query Profiler, Query Manager | — |

**Assessment:** Studio 3T's Query Assist mode (per-query result tabs, Visual Explain, code gen) is the more powerful execution model for iterative development. VisuaLeaf's Monaco editor offers more modern editor features (minimap, multi-session, background execution, auto-reconnect, persistent variables) useful for longer-running or operational scripts.

---

### F-AI — AI Features

*MongoDB Compass: partial — see below (updated 2026-07-28; previously N/A).*

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| NL → find() query | ✓ Pro/Base+ | ✓ confirmed via product page; implementation depth unverified | ✓ Professional |
| NL → aggregation pipeline | ✓ Pro/Base+ | Not documented | ✓ Professional |
| Plain-English explanation always on | Not documented as always-on | Not documented | ✓ (every query) |
| AI providers | Azure AI, OpenAI GPT-4o, Anthropic Claude Opus 4.1 | Not documented | OpenAI (confirmed); Anthropic (unverified) |
| Model selection | 3 provider options | Not documented | 11 OpenAI models user-selectable |
| "Send sample data" privacy toggle | Not documented as user-facing toggle | Not documented | ✓ ON = Better Accuracy / OFF = More Private |
| Conversation turns for refinement | Not documented | Not documented | ✓ prior turns used |
| Multiple named AI configs | Not documented | Not documented | ✓ |
| API key storage | Not documented as AES-masked | Not documented | AES-masked in Settings; never transmitted to SozoCode |
| Local MCP server | ✓ AI-007: HTTP at 127.0.0.1:27117; 10 tools | — | — |
| MCP client integrations | ✓ AI-009: VS Code, Cursor, Claude Desktop, others | — | — |
| Total MCP tools | 10 via local server; 59 via 3T Lens platform | — | — |
| stt-cli + PII scanner | ✓ AI-010 | — | — |
| 3T Explore AI Helper | ✓ AI-012 (edition/plan unverified) | — | — |

**Assessment:** VisuaLeaf's AI focuses on in-product UX (11 model choices, plain-English explanations, privacy toggle, conversation turns). Studio 3T's AI extends outward via MCP — enabling AI agents in external tools (VS Code, Cursor, Claude Desktop) to operate against MongoDB through Studio 3T, which is a fundamentally different capability. MongoDB Compass's AI feature set, confirmed 2026-07-28 via the official product page, is limited to natural language query generation — a much shallower surface than either competitor, but no longer a complete gap as previously documented. **As of release 2026.12.0 (17-Jul-2026), Studio 3T's AI Helper is disabled by default (opt-in)** — a reversal of the previously-documented default-enabled/opt-out model; do not read Studio 3T's AI surface above as lower-friction to reach than a competitor's by default (see [12-consolidated-corrections.md §10](../../research/studio-3t-desktop-review-2026/12-consolidated-corrections.md#10-f-ai--most-time-sensitive-correction-ai-helper-flipped-to-disabled-by-default)).

---

### F-SQL — SQL Tools

*MongoDB Compass: N/A — not supported.*
*Studio 3T: Pro/Base+ — full migration toolchain. VisuaLeaf: partial (SQL Mode, updated 2026-07-28; previously N/A) — plan tier unverified.*

| Dimension | Studio 3T | VisuaLeaf |
| --- | --- | --- |
| SQL query syntax over MongoDB | ✓ full SELECT/WHERE/JOIN/GROUP BY/ORDER BY/HAVING | ✓ SELECT/WHERE/ORDER BY/LIMIT + COUNT/SUM/AVG; JOIN/GROUP BY/subqueries via SQL Helper examples |
| SQL → MongoDB translation / code-gen | ✓ 9-language driver code gen | ✓ MongoDB translation view (pipeline equivalent); driver-language export not documented |
| SQL JOIN → $lookup mapping | No visual/drag-drop mapping editor — joins authored as plain SQL text; only single equality-comparison JOIN conditions supported (compound ANDed joins throw `NotImplementedException`) | Not documented (JOIN syntax supported in SQL text only) |
| SQL migration wizard (relational → Mongo) | ✓ 6 dialects via JDBC: MySQL/PostgreSQL/Oracle/SQL Server/Sybase/IBM DB2 (Sybase and DB2 are Enterprise-gated, migration-source only) | Not supported |
| SQL export to relational targets | ✓ MySQL/MSSQL/Oracle/PostgreSQL (4 targets — Sybase and IBM DB2 are migration-source only; neither has a direct SQL-export-wizard target) | Not supported (separate SQL INSERT statement export exists under Data Transfer) |
| In-place MongoDB schema migration (reschema) | ✓ schedulable via Task Scheduler | Not supported |

**Assessment:** Studio 3T remains the only product with a full SQL↔MongoDB migration toolchain (SQL-to-$lookup JOIN translation, migration wizard, relational export, reschema). Note: JOINs are authored as plain SQL text with only single equality-comparison conditions supported — there is no visual/drag-drop JOIN mapping editor. VisuaLeaf's SQL Mode, confirmed 2026-07-28, is a narrower capability: SQL syntax for querying MongoDB collections only, with a translation view to the equivalent pipeline — useful for SQL-background users, but not a migration or export tool. VisuaLeaf's own documentation directs users to the Aggregation Pipeline for advanced transformations.

---

### F-GOV — Governance

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Protect / write-prevention mode | Per-connection UI lock (UI layer only) | ✓ (Compass "Protect mode") | — |
| Network policy | — | ✓ admin-configurable | — |
| Telemetry configuration | — | ✓ | — |
| Startup / CLI policy (EJSON/YAML) | — | ✓ | — |
| Isolated / air-gapped edition | Not documented as separate edition | ✓ Isolated Edition (offline) | ✓ AES-256 local creds, never transmitted |
| AI controls with human approval gate | — | ✓ | — |
| RBAC user/role management | ✓ via 3T Access platform | — | ✓ Professional (users/roles/inheritance/tree/actions) |
| Visual role inheritance tree | — | — | ✓ Professional |
| Audit log | Local tamper-evident (chained-MD5) log, but narrow: Connection Manager actions only (create/edit/delete/duplicate/import connections) — not queries or document changes; off by default; enabled only via Windows Group Policy/registry. A separate HTTP audit-event sender to 3T Access exists in code but has no call sites (unwired scaffolding, not shipped). | — | ✓ Professional |
| Collection compare (3-panel diff) | ✓ Pro/Base+ | — | ✓ Professional |
| Collection sync with direction toggle | ✓ Pro/Base+ | — | ✓ Professional |
| CDC pipeline (Kafka/Pub/Sub/HTTP) | ✓ 3TL Bridge | — | — |
| Kubernetes Helm chart | ✓ for platform components | — | — |
| OIDC multi-provider for platform auth | ✓ | — | — |
| Credential protection | Built-in key store OR master password | OS Keytar API | AES-256 local; never transmitted; AI keys AES-masked |
| 3T Explore governed workspace | ✓ Workspace Switcher + 3T Access Manager integration (browser IDE; edition/plan unverified) | — | — |

**Assessment:** Compass has the most comprehensive built-in policy enforcement (network policy, startup/CLI policy, AI controls, protect mode, isolated edition). VisuaLeaf has strong RBAC for teams (visual role tree, audit log) without requiring a separate platform. Studio 3T's governance scales via 3T Lens + 3T Access + 3TL Bridge for enterprise CDC, event streaming, and Kubernetes deployments. Studio 3T Desktop's own built-in audit log is much narrower than that framing implies: it covers only Connection Manager actions, ships off by default, and is enabled only via Windows Group Policy — it is not a query/document audit trail.

---

### F-SCHED — Task Scheduler

*MongoDB Compass: N/A — not supported*

| Dimension | Studio 3T | VisuaLeaf |
| --- | --- | --- |
| Task types | Import, Export, Data Masking, Reschema, Data Compare & Sync, IntelliShell Script, SQL Migration (7 types) | Import, Export, Script + Professional types |
| Schedule options | Standard + cron | 5 presets + cron |
| Timezone-aware with DST | Not documented | ✓ |
| Execution config | Not documented as named exec-config group | Batch size, retry policy, timeout, concurrent execution, history retention |
| Task status states | Running/Completed/Error | 5 states: Pending/Running/Completed/Failed/Paused |
| Task actions | Run Now, Enable/Disable, Edit, Delete | Run Now, Pause, Resume, Clone, Delete |
| Email notifications | ✓ configurable (provider not specified) | ✓ SendGrid integration |
| Multiple script units per task | ✓ multiple IntelliShell script units per task | Not documented |
| Compare/sync task with diff view | ✓ setup wizard + results panel + sync action with direction toggle | — |
| Plan limits | Pro/Base+ required for task save | Community: 0 tasks; Basic: 2 tasks; Professional: unlimited |

**Assessment:** Studio 3T has more task types (7 vs. VisuaLeaf's fewer), unique multi-script-unit tasks, and a dedicated compare/sync workflow. VisuaLeaf has timezone/DST awareness, richer execution config (retry/batch/concurrent), 5 task status states, and Clone action. VisuaLeaf's Community plan cannot schedule any tasks (0 limit).

---

## Unique differentiators per product

### MongoDB Compass
- **In-use encryption (QE/CSFLE):** Only product with Queryable Encryption and CSFLE key vault + KMS configuration in the GUI.
- **Real-time performance monitoring:** Only product with live mongostat/mongotop/currentOp drill-down with pause/play visualization out of the box. (Studio 3T has a confirmed mongostat/currentOp-equivalent via its Server Status Charts + Task Monitor tabs, without pause/play.)
- **Atlas Search + Vector Search index creation:** Only product supporting Atlas Search and Vector Search index management, including status tracking.
- **Geo field schema analysis:** Only product with map-backed schema analysis that generates geo queries interactively.
- **Enterprise policy enforcement:** Uniquely offers startup policy (EJSON/YAML), CLI policy, network policy, telemetry config, and AI controls with human approval gate.
- **Multiple concurrent connections:** First product to support multiple active connections simultaneously (1.44.0+).
- **Required-access documentation guide:** Maps every feature to the required MongoDB privilege — unique operational reference.

### VisuaLeaf
- **Visual ERD designer:** Only product with an infinite canvas ERD designer, graph-theory-based relationship detection, 11 color presets, and named exportable layouts.
- **Full JSON schema tree editor:** Only product with a standalone tree-based JSON Schema editor supporting all BSON types with polymorphic fields and full constraint definitions.
- **6-step connection test wizard:** Only product that validates 6 distinct connection phases (Network/SSH/TLS/Auth/DB/Permissions) step-by-step.
- **AI with 11 model choices and plain-English explanations always on:** Widest model selection; every AI-generated query includes an always-on human-readable explanation.
- **P50/P95/P99 profiler percentiles + 4 recommendation types:** Most analytically rich query profiler, with latency percentiles, COLLSCAN flagging, and actionable index recommendations.
- **Pre-import JS transforms and document filter conditions:** Only product allowing user-defined JavaScript transforms and pre-import document filters — strongest ETL capability.
- **Server-side $pipeline pre-export transform:** Unique capability for pre-export data shaping.
- **Monaco editor with multi-session + background execution + auto-reconnect:** Most modern shell editor environment.
- **DocumentDB/Cosmos DB roadmap:** Only product with stated plans for DocumentDB 8.0+ and Cosmos DB 4.2+ compatibility (Q2 2026).
- **GridFS Viewer:** Only product in this comparison with a dedicated GridFS file browser (preview, bulk upload/download, metadata editing) — confirmed 2026-07-28.
- **Split Panel Views:** Only product with flexible horizontal/vertical/nested workspace splits and drag-and-drop tab management across panels — confirmed 2026-07-28.
- **MongoSync guided cross-server MongoDB copy:** Confirmed 2026-07-28 — selective sync, conflict handling, field filtering, transformation mappings, and scheduled jobs for moving data between local instances, Atlas, and clusters (complements, and is distinct from, Collection Compare & Sync).
- **Polyglot database support:** Only product in this comparison that also natively connects to non-MongoDB engines (PostgreSQL, MySQL, SQL Server, Oracle, SQLite, MariaDB, CockroachDB, ClickHouse, DuckDB, TiDB) in the same client — out of scope for this repository's MongoDB-focused analysis, but a material product-classification difference from Compass and Studio 3T.

### Studio 3T
- **SQL tools (F-SQL):** Only product in this comparison with a full SQL↔MongoDB migration toolchain — SQL-to-$lookup JOIN translation (plain SQL text, single equality-comparison conditions only — no visual/drag-drop JOIN mapping editor), SQL migration wizard (6 dialects), and SQL export to relational databases (4 targets). (VisuaLeaf added query-only "SQL Mode" against MongoDB in 2026-07-28 research, but has no migration/export tooling — see the F-SQL section above.)
- **Date tags (~20 shortcuts):** Only product with date-shorthand syntax (#today/#yesterday/#lastNdays etc.) expanding to MongoDB range queries at runtime — available on all editions.
- **MCP ecosystem (3T Lens, MCP server, MCP client, stt-cli):** Only product exposing MongoDB operations to external AI agents via MCP — enabling VS Code Copilot, Cursor, and Claude Desktop to operate against MongoDB.
- **Data masking (standalone + inline):** Only product with field-level data masking, offering 19 masking operations (across 6 BSON-type categories) applicable during Import/Export runs without modifying the original.
- **Incremental export with 5 resume points:** Unique capability for time-based incremental data extraction with persistent resume state.
- **Index copy-paste across connections:** Only product allowing an index definition to be copied from one collection and pasted to another, even across different server connections (Professional tier and above).
- **SSH Profiles with password propagation:** Named, reusable SSH tunnel profiles where password updates propagate to all dependent connections.
- **3T platform suite (3T Explore + 3T Lens + 3T Access + 3TL Bridge):** Only product with a separate enterprise platform spanning a browser IDE (3T Explore, governed via 3T Access), CDC pipelines (MongoDB/Kafka/Pub/Sub/HTTP), Kubernetes deployment, and OIDC multi-provider. (This report previously used the name "3T Build" for the browser IDE product; corrected to "3T Explore" — "Build" is the product track, not the product.)
- **FerretDB compatibility:** Only product in this comparison with stated compatibility for FerretDB, the open-source MongoDB-wire-protocol-compatible database, alongside DocumentDB and Cosmos DB.
- **Query Assist mode (per-query result tabs + Visual Explain in shell):** Only product where shell queries produce individual editable, pinnable result tabs with Visual Explain and code-gen integrated.

### DBeaver
- **100+ supported database engines:** Only product in this comparison with a single-client footprint spanning relational, cloud-warehouse, NoSQL, graph, and flat-file "database" engines through one JDBC-driver architecture — a fundamentally different value proposition (breadth over MongoDB depth) than Compass, VisuaLeaf, or Studio 3T.
- **Widest documented AI provider list:** OpenAI (GPT-5 default), Azure OpenAI, Google Gemini, and GitHub Copilot/Codex — broader than any other product reviewed here (unverified in depth, but broadest in breadth).
- **File-attachment AI context:** Unique mechanism letting a user attach a CSV/JSON/Parquet/XLSX file into an AI Chat session, which DBeaver parses into a temporary in-memory table for combined file-and-database natural-language querying.
- **MCP server exposure of live connections:** Positions DBeaver in the same agentic-AI/MCP space as Studio 3T's own local MCP server, exposing any of its 100+ connections (not just MongoDB) as governed AI-agent tool interfaces (version claim unverified).
- **Headless CLI (`dbvr`):** Dedicated command-line executable for CI/CD-driven database operations, exports, and schema migrations — the named competitive comparator for this repository's own `PROP-cli-automation` proposal in the [Proposed Feature Registry](../../feature-dictionary.md#proposed-feature-registry-research-pipeline).
- **External secrets manager integration:** HashiCorp Vault, CyberArk, and AWS Secrets Manager credential sourcing (Unverified against a primary source, but a real enterprise-relevant claim not made for any other product in this comparison).
- Note: DBeaver's MongoDB support is a confirmed net *weakness* relative to every other product compared here — no native document query surface, no visual aggregation builder, no sampling-based schema analytics, and three primary-sourced GitHub issues documenting BSON type-fidelity bugs. Its differentiators above are about breadth-of-engine-coverage and general-purpose tooling maturity, not MongoDB-specific depth.

### DataGrip
- **Deepest, most itemized agentic-AI/MCP architecture reviewed to date:** Native Claude Agent (Claude 4.5 Sonnet via the Anthropic Agent SDK) and OpenAI Codex, driving a 14-tool database-specific MCP server, with every tool individually named in the source — a more granular tool inventory than any other product's AI/MCP surface documented in this repository.
- **Most structured pre-execution AI consent model reviewed:** A 4-category approval gate (Schema Access / Data Access / Schema Modification / Data Modification) before any AI-generated action executes — more granular than a single blanket "AI enabled" toggle.
- **`dg_cross` federated cross-database query engine:** A DuckDB-backed engine letting one SQL query join tables across multiple, independently-configured data source connections without a pre-flight migration — confirmed via DataGrip's own 2026.2 release notes, though its applicability to MongoDB specifically is unverified (the source's worked example joins only relational engines).
- **Materially lower individual/team TCO:** A free non-commercial tier (since late 2025), a $109→$65/yr individual commercial tier with a perpetual fallback license, and JetBrains All Products Pack bundling — a fundamentally different pricing posture from Studio 3T's flat $499–$699/yr annual-only model.
- **Git-committable, human-readable connection configuration:** Data Source Templates stored as plain XML project files (`.idea/db-forest-config.xml`) rather than an opaque binary store.
- Note: like DBeaver, DataGrip's MongoDB depth is a confirmed net *weakness* relative to Compass, VisuaLeaf, and Studio 3T — its own source states directly that it has no native document workspace, no visual (or even text-based) aggregation pipeline builder at all, no INSERT/UPDATE/DELETE via SQL, no application-language code generation, and only basic (non-analytical) schema rendering. Its differentiators above are about AI/MCP architecture depth and IDE-ecosystem economics, not MongoDB-specific query/aggregation/schema tooling.

---

## Edition / pricing constraints

| Feature | Studio 3T | MongoDB Compass | VisuaLeaf | DBeaver | DataGrip |
| --- | --- | --- | --- | --- | --- |
| Visual Query Builder | All editions (free) | N/A | Basic+ required | Generic relational VQB only; MongoDB applicability unverified | N/A (no query builder of any kind — SQL text only) |
| AI query builder | Pro/Base+ required | N/A | Professional required | Included (tier unverified); generates SQL, not a native MongoDB filter | AI Free (baseline) / AI Pro Add-on (full); agentic chat generates/executes SQL, not a native MongoDB filter |
| Enterprise auth (Kerberos/LDAP/AWS/OIDC) | Ultimate edition only | Free (all confirmed) | LDAP/AWS IAM free (others roadmap) | Community: none; Enterprise/Ultimate: SAML/Kerberos/Azure AD (MongoDB-specific scope unverified) | Not discussed for MongoDB in source |
| Shell / IntelliShell | All editions (free) | N/A | Available (plan details unclear) | N/A (no MongoDB shell/scripting environment evidenced) | N/A (no MongoDB shell/scripting environment evidenced) |
| Data Transfer | Pro/Base+ for task save; formats available all editions | N/A | Community: no automation (0 tasks); Basic: 2 tasks | CSV/table wizards asserted; tier requirement unverified | N/A (not discussed for MongoDB) |
| Team connection sharing | Pro/Base+ required | N/A | N/A | Team Edition / CloudBeaver (detail unverified) | Not team-permissioned; JetBrains Account syncs templates per individual user |
| Data masking | Pro/Base+ required | N/A | Basic/Professional — query-result masking; no dedicated import/export masking tool documented | Not discussed in source | Not discussed in source |
| SQL tools | Pro/Base+ required (full migration toolchain) | N/A | Plan tier unverified (SQL Mode — query-only, no migration) | Included in Lite+ — primary MongoDB query surface (SQL-first architecture), not a separate add-on | Included in all commercial + free non-commercial tiers (unverified whether restricted) — primary and only MongoDB query surface |
| Task scheduler | Pro/Base+ required | N/A | Community: 0 tasks; Basic: 2; Professional: unlimited | Enterprise/Ultimate only | N/A — no task automation; 2026.2's CLI feature is connection-config management, not scheduling |
| Query Manager (multi-type) | All editions (Collection query type free) | No (My Queries only) | Basic+ for saved queries | Not discussed in source | Not discussed in source |
| Collection compare + sync | Pro/Base+ required | N/A | Professional required | Schema/structure compare included (tier unverified); DDL-oriented, not a collection-data 3-panel diff | Not discussed in source |
| RBAC dashboard | Via 3T Access platform | N/A | Professional required | Team Edition / CloudBeaver only (detail unverified) | Not discussed in source |
| Audit log | Built-in local feature (edition tier not specified in source) — Connection Manager actions only; off by default; Windows GPO/registry activation only | N/A | Professional required | Not discussed in source | Not discussed in source |
| Schema validation UI | N/A (not supported) | Free | Basic+ | Not discussed in source | N/A (confirmed absent — no schema analysis surface) |
| Visual ERD designer | N/A | N/A | Basic+ required | Not discussed in source | N/A |
| Atlas Search / Vector Search indexes | N/A | Free (requires Atlas M10+ or MongoDB 7.0+ local) | N/A | N/A (F-IDX not evidenced for DBeaver) | N/A (F-IDX not evidenced for DataGrip) |
| MongoDB connectivity at all | Free Community tier (limited) | Free (full) | Free Community tier (limited) | Not available in free Community Edition — requires Lite or above | Free non-commercial tier included (bundled MongoDB driver, all commercial tiers too) |

---

## Key gaps summary

| Gap | Products affected |
| --- | --- |
| No SQL migration/export toolchain | Compass, VisuaLeaf (VisuaLeaf has query-only SQL Mode against MongoDB as of 2026-07-28; no migration or relational export) |
| No SQL querying at all | Compass |
| No data transfer/ETL | Compass |
| No integrated shell | Compass |
| No AI features beyond basic NL query | Compass (natural language querying confirmed 2026-07-28; no pipeline generation, schema-aware context, or model/provider choice documented) |
| No task scheduler | Compass |
| No visual ERD designer | Compass, Studio 3T |
| No JSON schema tree editor | Compass, Studio 3T |
| No schema validator creation/deploy | Studio 3T |
| No incremental export | Compass, VisuaLeaf |
| No data masking | Compass, VisuaLeaf |
| No in-use encryption (QE/CSFLE) | VisuaLeaf, Studio 3T |
| No real-time performance monitoring | VisuaLeaf (unverified) |
| No Atlas Search / Vector Search | VisuaLeaf, Studio 3T |
| No MCP / AI agent integration | Compass, VisuaLeaf |
| Enterprise auth gated to Ultimate edition | Studio 3T (Compass/VisuaLeaf free/roadmap) |
| geoHaystack shown without deprecation warning | Studio 3T (bug) |
| AGG-stage-toggle unverified | VisuaLeaf |
| IDX-hide-unhide unverified | VisuaLeaf |
| AGG code generation unverified | VisuaLeaf |
| AGG create view unverified | VisuaLeaf |
| SCHEMA validation strictness (warn/error) unverified | VisuaLeaf |
| Charts & Dashboards implementation detail (chart types, dashboard composition) unverified | VisuaLeaf |
| GridFS Viewer / Split Panel Views / MongoSync / SQL Mode plan-tier requirement unverified | VisuaLeaf |
| 3T Explore edition/plan requirement unverified | Studio 3T |
| FerretDB compatibility depth (which features work) unverified | Studio 3T |
| No native document query surface (filter bar/tree view) — MongoDB access is SQL-first | DBeaver, DataGrip |
| No dedicated visual aggregation pipeline builder for MongoDB (JSON-array console only) | DBeaver |
| No aggregation pipeline builder of any kind (visual or text-console) — hand-coded JSON in a generic text editor | DataGrip |
| No sampling-based schema analytics (field probability, type probability) | DBeaver, DataGrip |
| Confirmed BSON type-fidelity bugs (date-millisecond truncation, ObjectId misinterpretation) — 3 GitHub issues | DBeaver |
| No MongoDB connectivity in free Community Edition | DBeaver |
| No SQL migration wizard or SQL-to-MongoDB code generation | DBeaver, DataGrip |
| Secrets-manager integration, voice-query, and MCP-server version claims unverified against source's own Works Cited | DBeaver |
| No SQL-based INSERT/UPDATE/DELETE against MongoDB — writes require native shell syntax or cell-by-cell grid edits | DataGrip |
| No application-language code generation (Java/Python/C#/Node.js/PHP) from queries or pipelines | DataGrip |
| SQL JOIN restricted to a single equality condition, no visual mapping editor, no subqueries/USING | DataGrip |
| `dg_cross` federated query engine's MongoDB-inclusive scope unverified (worked example covers only relational engines) | DataGrip |
| External MCP client access to the local MCP server unverified (source describes internal-agent use only) | DataGrip |
| RBAC, audit logging, and platform governance not discussed for MongoDB in source | DataGrip |
