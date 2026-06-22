# High-Level Product Comparison

This report summarizes each product's positioning, feature breadth, and key gaps across the 11 analyzed feature areas.

## Navigation

- [Cumulative report index](../cumulative-report.md)
- [Low-level feature comparison](low-level-feature-comparison.md)
- [Feature dictionary](../../feature-dictionary.md)
- [Studio 3T product report](../../products/3t/studio-3t/product-report.md)
- [MongoDB Compass product report](../../products/third-party/mongodb-compass/product-report.md)
- [VisuaLeaf product report](../../products/third-party/visual-eaf/product-report.md)

## Compared products

| Product | Vendor | Type | Edition model |
| --- | --- | --- | --- |
| MongoDB Compass | MongoDB Inc. | Desktop GUI | Free / open-source |
| VisuaLeaf | SozoCode | Desktop GUI + web | Community / Basic / Professional (subscription) |
| Studio 3T | 3T Software Labs | Desktop GUI | Free / Base / Pro / Ultimate |

## Product-level comparison (feature areas present)

| Feature area | MongoDB Compass | VisuaLeaf | Studio 3T |
| --- | --- | --- | --- |
| F-CONN — Connectivity | ✓ | ✓ | ✓ |
| F-QUERY — Querying | ✓ | ✓ | ✓ |
| F-AGG — Aggregation | ✓ | ✓ | ✓ |
| F-SCHEMA — Schema | ✓ | ✓ | ✓ |
| F-IDX — Indexing & Performance | ✓ | ✓ | ✓ |
| F-TRANSFER — Data Transfer | — | ✓ | ✓ |
| F-SHELL — Shell | — | ✓ | ✓ |
| F-AI — AI features | — | ✓ | ✓ |
| F-SQL — SQL tools | — | — | ✓ |
| F-GOV — Governance | ✓ | ✓ | ✓ |
| F-SCHED — Task scheduler | — | ✓ | ✓ |

## Feature-group comparison

### F-CONN — Connectivity

| Dimension | MongoDB Compass | VisuaLeaf | Studio 3T |
| --- | --- | --- | --- |
| Topology coverage | Standalone, RS, Sharded, SRV; multiple concurrent (1.44.0+) | Standalone, RS (hidden nodes, resolve members), Sharded, DNS SRV + SRV Service Name override | Standalone, RS, Sharded, DNS SRV — all editions |
| Enterprise auth | Kerberos, LDAP, AWS IAM, OIDC — all confirmed | LDAP, AWS IAM confirmed; Kerberos + OIDC roadmap Q2 2026 | Kerberos, LDAP, AWS IAM, OIDC — Ultimate edition only |
| TLS | CA/client cert/key/passphrase; validation toggles | Custom Root CA, OS Trust Store, Accept Any; mTLS cert+key+passphrase | Own CA/OS-trusted/accept any; client PEM+passphrase; SNI; allow-invalid-hostnames toggle |
| SSH tunnel | Password + private key | Password or private key + optional passphrase | Password + private key; SSH Profiles (named/reusable; password updates propagate) |
| Proxy | SOCKS5 only | Not documented | 4 modes: Direct / App default / Custom HTTP / Custom SOCKS — per connection |
| Connection pool params | Not documented | Full set incl. Retry Reads + zlib compression | Full set incl. Azure idle-time workaround |
| Connection organization | Favorites, sidebar search | 3-level hierarchy (Project → Environment → Connection); Community max 3 | Folders + drag-and-drop; per-tab color coding |
| In-use encryption (QE/CSFLE) | ✓ (key vault + KMS config) | — | — |
| Connection test validation | Not documented | 6-step: Network/SSH/TLS/Auth/DB/Permissions | Not documented as multi-step |
| Team sharing | — | — | Pro/Base+: invite by email; Manage/Edit/View permissions |
| Credential storage | OS Keytar API | AES-256 local, never transmitted, air-gapped safe | Built-in key store OR master password (cryptographic) |
| Unique: Compass | Multiple concurrent connections (1.44.0+); QE/CSFLE in-use encryption; required-access guide | — | — |
| Unique: VisuaLeaf | 6-step connection test wizard; URI export; DocumentDB/Cosmos DB roadmap Q2 2026 | — | — |
| Unique: Studio 3T | SSH Profiles; 4-mode proxy; read-only UI lock; team sharing; import from Robo 3T/NoSQLBooster/.uri | — | — |

**Assessment:** All three products cover core connectivity (standalone/RS/sharded/SRV, standard auth, TLS, SSH). Compass leads on in-use encryption and enterprise auth completeness. VisuaLeaf offers the best connection-test UX and uniquely plans DocumentDB/Cosmos compatibility. Studio 3T has the most advanced proxy, SSH, team-sharing, and credential-import capabilities.

---

### F-QUERY — Querying

| Dimension | MongoDB Compass | VisuaLeaf | Studio 3T |
| --- | --- | --- | --- |
| Filter bar / autocomplete | ✓ with examples/shortcuts | ACE editor + Ctrl+Space field-name autocomplete from schema | 5-field bar; full autocomplete incl. BSON wrappers; shorthand ObjectId |
| Visual Query Builder | — | Basic+ — type-aware inputs (date pickers, sliders, booleans), AND/OR nested groups, bidirectional | All editions — AND/OR/NOR; BSON type auto-detected; Binary/Reference/Regex editors; bidirectional |
| Date tags / shortcuts | — | — | ~20 tags (#today/#yesterday/#lastNdays etc.) — all editions |
| AI query builder | — | Professional — NL → find() + pipeline; 11 OpenAI models; plain-English explanation always on | Pro/Base+ — NL → query/pipeline; Azure AI / OpenAI GPT-4o / Anthropic |
| Query history | Depth-capped recent list + save | Basic+ — per-collection with timestamp + exec time | Auto-save on run; shared folder save Pro/Base+ |
| Saved queries / manager | My Queries + favorites | Basic+ — by collection or global; export/import JSON; team share | Query Manager — folders/drag-and-drop; 4 query types incl. SQL + Aggregation |
| Multi-document update | Not documented | Table View Batch Update ($set/$unset/$inc/$push/$pull + preview) | Update Documents dialog (updateMany()); separate query+update tabs |
| Performance timer | Not documented | Amber at 2s; red at 5s | Not documented as visual timer |
| Cancel in-flight query | Not documented | ✓ cancel button | Not documented |
| Explain view | ✓ | Exec plan, index usage, docs examined vs returned, index suggestions | Visual Explain across 5 entry points |
| Export to driver language | 8 languages (Java/Node/C#/Python/Ruby/Go/Rust/PHP) | Not documented | 9 languages (adds MongoDB Shell) |
| Undo/redo | Not documented | Ctrl+Z / Ctrl+Shift+Z | Not documented |
| Unique: Compass | Collation in filter bar; max-time (60,000ms default) | — | — |
| Unique: VisuaLeaf | Performance timer; cancel button; Run Find One / Run Count variants; 7 "open in" integrations; undo/redo; batch update from table view; EJSON copy | — | — |
| Unique: Studio 3T | Date tags (~20); Query Manager with 4 query types; "open in Aggregation Editor" converts filter → $match+$project | — | — |

**Assessment:** Compass is the only product with collation in the filter bar. VisuaLeaf has the most user-friendly query execution UX (timer, cancel, run-variants, undo/redo). Studio 3T's date tags and Query Manager are unique value adds for power users. VQB is absent in Compass; VisuaLeaf's is plan-gated; Studio 3T's is available on all editions.

---

### F-AGG — Aggregation

| Dimension | MongoDB Compass | VisuaLeaf | Studio 3T |
| --- | --- | --- | --- |
| Stage count / coverage | All standard stages | 37+ stages incl. $densify/$fill/$setWindowFields/$search/$documents/$listSearchIndexes | All standard stages |
| Editor layout | Stage View, Stage Wizard, Focus Mode, Text View | Visual pipeline canvas with stage cards | 5-region UI: Pipeline panel, Stage editor, Stage I/O, Pipeline output, Query Code + Explain tab |
| Per-stage editing mode | Stage Wizard + per-stage mode switching | Form Mode (VQB/$group accumulator builder) OR Monaco editor per stage; preference saved | Code editor only |
| Stage toggle (enable/disable) | ✓ confirmed | Unknown/unverified | ✓ confirmed |
| Stage preview | Sampled preview per stage | Input/Output split-view; 20-doc sample; Auto-Preview toggle | Stage I/O panels per stage |
| Code generation | Major driver languages | Not documented | 9 languages; "Open in IntelliShell" button |
| Create MongoDB view | ✓ | Not documented | ✓ (requires MongoDB 3.4+) |
| Export pipeline results | JSON/CSV + Extended JSON | JSON, CSV, BSON, SQL INSERT statements | Export Wizard from Pipeline output or Stage I/O |
| Chart builder from output | — | ✓ opens Chart Builder | — |
| Pipeline options | Custom collation + pipeline maxTimeMS | Allow Disk Use, Max Time 300s, Auto Collapse | allowDiskUse, custom collation, index hint |
| Switch collection mid-session | Not documented | Not documented | ✓ |
| Date tags in $match | — | — | ✓ all editions |
| Execution timer + cancel | Not documented | ✓ real-time timer + cancel | Not documented |
| Unique: Compass | Stage Wizard mode (GUI form for stage params) | — | — |
| Unique: VisuaLeaf | 37+ stages (widest coverage); Form Mode with VQB for $match + accumulator builder for $group; chart builder from output; execution timer + cancel | — | — |
| Unique: Studio 3T | 9-language code gen; date tags in $match; switch collection mid-session; clipboard copy of full pipeline JSON | — | — |

**Assessment:** VisuaLeaf has the widest stage coverage and the most ergonomic per-stage editing (Form Mode). Studio 3T has the most powerful code-gen and integration options. Compass's Stage Wizard provides good accessibility for less-experienced users. Stage toggle availability is confirmed for Compass and Studio 3T but unverified in VisuaLeaf.

---

### F-SCHEMA — Schema

| Dimension | MongoDB Compass | VisuaLeaf | Studio 3T |
| --- | --- | --- | --- |
| Field statistics analytics (probability/type/histogram) | ✓ (field prob, type prob, histogram) | — (no analytics) | ✓ (field prob, type prob, histogram, top values, date distributions) |
| Geo field analysis | ✓ (map-backed, interactive filter drawing, geo query generation) | — | — |
| JSON schema editor | — | ✓ tree editor (expand/collapse, drag-to-reorder, required toggle, View/Edit toggle, polymorphic types) | — |
| Schema validation deploy | ✓ via UI workflow | ✓ push to collection as $jsonSchema | — |
| Validation strictness (warn/error, strict/moderate) | ✓ confirmed | Unknown/unverified | N/A |
| Visual ERD designer | — | ✓ Basic+ (infinite canvas; graph-theory relationship detection; 11 color presets; named layouts; export/import) | — |
| View creation from schema tool | Not documented | Not documented | ✓ db.createView() builder — all editions |
| Schema doc export | Multiple formats (fails if >1000 distinct fields) | $jsonSchema-compatible JSON | Word (.docx) or CSV with field names/types/probabilities |
| Explore docs by field presence | Not documented | Not documented | ✓ right-click → opens Collection Tab with {$exists} filter |
| Rename field across all docs | Not documented | Not documented | ✓ via schema tree outlier workflow |
| Unique: Compass | Geo field analysis with interactive map and geo-query generation | — | — |
| Unique: VisuaLeaf | Full JSON schema tree editor with BSON types; visual ERD designer with relationship detection | — | — |
| Unique: Studio 3T | Field statistics analytics (top values, date distributions); explore docs by field presence; rename field workflow; create view from schema | — | — |

**Assessment:** Compass and Studio 3T provide rich schema analytics (field probability, histograms). Compass adds geo analysis. VisuaLeaf uniquely offers a full JSON schema editor and a visual ERD designer with graph-theory relationship detection. Compass and VisuaLeaf have schema validator deploy; Studio 3T does not. Studio 3T has the most schema-to-data-repair workflows (explore, rename, view creation).

---

### F-IDX — Indexing & Performance

| Dimension | MongoDB Compass | VisuaLeaf | Studio 3T |
| --- | --- | --- | --- |
| Index types supported | single, compound, TTL, unique, sparse, partial, hidden (others not documented) | single, compound, text, wildcard, hashed, TTL, 2d, 2dsphere, partial, sparse, hidden | single, compound, text, wildcard, TTL, 2d, 2dsphere, geoHaystack (deprecated — no warning shown), partial, sparse, hidden |
| Atlas Search / Vector Search | ✓ (Atlas M10+ or local MongoDB 7.0+) | — | — |
| Advanced index options | Not documented | Partial Filter Expression (JSON editor), Wildcard Projection, Storage Engine config, Commit Quorum, Clustered index | Not documented as grouped options |
| Collation index options | Not documented | 60+ ICU locales; Strength 1-5; Case First/Level/Numeric/Alternate/Backwards | Locale + strength only |
| Quick-action templates | — | 4 templates (Wildcard Text/$**/\_id/createdAt) | — |
| Copy/paste index across connections | — | — | ✓ even across different connections |
| Hide/unhide index | ✓ | Unknown/unverified | ✓ (MongoDB 4.4+) |
| Visual Explain | ✓ plan + execution stats | Exec plan, index usage, docs examined vs returned, index suggestions | ✓ plan + execution stats; hover tooltips; JSON fragment view; available in 5 contexts |
| Profiler | Not documented in matrix | Slow query threshold; levels 0/1/2; sample rate; P50/P95/P99 percentiles; COLLSCAN flagging; 4 recommendation types; CSV/JSON export | system.profile reader; levels 0/1/2; exact query vs shape grouping; 5 drilldown actions |
| Profiler export | — | ✓ CSV or JSON | — |
| Real-time performance monitoring | ✓ mongostat/mongotop/currentOp; pause/play | Not documented | — |
| Kill running operations | ✓ (requires killop privilege) | ✓ kill button per operation | — |
| Unique: Compass | Atlas Search + Vector Search index creation; real-time perf monitoring (mongostat/mongotop/currentOp) | — | — |
| Unique: VisuaLeaf | P50/P95/P99 profiler percentiles; 4 index recommendation types; profiler export; hashed index; 60+ ICU locale collation; Commit Quorum; clustered index; 4 quick-action templates | — | — |
| Unique: Studio 3T | Index copy-paste across connections; geoHaystack (unwarned deprecation); Explain available in 5 contexts incl. SQL Query + IntelliShell | — | — |

**Assessment:** Compass exclusively supports Atlas Search and Vector Search. VisuaLeaf has the most complete index type coverage and the most sophisticated profiler (P50/P95/P99, 4 recommendation types, export). Studio 3T's Explain is available in the widest set of contexts. Note: geoHaystack displayed by Studio 3T without deprecation warning is a confirmed bug.

---

### F-TRANSFER — Data Transfer

*MongoDB Compass: N/A — not supported*

| Dimension | VisuaLeaf | Studio 3T |
| --- | --- | --- |
| Import formats | JSON, CSV, BSON | JSON, CSV, BSON, SQL (Pro/Base+), cross-server MongoDB |
| Export formats | JSON, CSV, BSON, SQL INSERT statements | JSON, CSV, BSON, Excel (.xlsx), SQL (Pro/Base+), cross-server MongoDB |
| Import write modes | Upsert only | 5 modes: Insert/fail, Insert/ignore, Upsert, Merge, Replace |
| Document filter before import | ✓ include/exclude by condition | — |
| User-defined JS transform per document | ✓ | — |
| Server-side $pipeline pre-export transform | ✓ | — |
| Field mapping and rename | ✓ | ✓ (CSV/SQL path) |
| Incremental export with resume points | — | ✓ up to 5 historical resume points; does NOT track updates to existing docs |
| Data masking | — | ✓ Pro/Base+: 8 masking types; inline during Import/Export; standalone tool |
| Task save for scheduler | ✓ (Basic: 2; Professional: unlimited) | ✓ Pro/Base+ |
| Export source granularity | Not documented | 6 sources: entire collection / view / find() result / aggregation result / current cursor / selected documents |

**Assessment:** Studio 3T has deeper export/import format coverage (SQL, Excel, cross-server MongoDB), more import modes, data masking, and incremental export. VisuaLeaf uniquely offers pre-import JS transforms, document filter conditions, and server-side $pipeline pre-export transforms — better for ETL scenarios. VisuaLeaf's plan limits (Community = 0 tasks) are more restrictive.

---

### F-SHELL — Shell

*MongoDB Compass: N/A — not supported*

| Dimension | VisuaLeaf | Studio 3T |
| --- | --- | --- |
| Editor engine | Monaco (minimap, multi-session) | ACE editor (format code Ctrl+Alt+L, line comments Ctrl+/) |
| Autocomplete | Contextual | Ctrl+Space — JS functions, shell types/methods, operators, collection names, field names |
| Live syntax validation | — | ✓ red gutter markers + right-ruler |
| Run all / selection | ✓ | ✓ F5 (all) / F9 or Ctrl+Enter (selection) |
| Run to cursor line | — | ✓ F6 |
| Shell modes | Not documented as named modes | Shell mode (all → Raw tab) vs Query Assist mode (per-query editable result tabs; Visual Explain; destructive op warnings) |
| Per-query result tabs (pinnable) | — | ✓ pin tab persists across re-runs |
| Result views | Tree View, Table View, BSON View | Tree View, Table View, JSON/BSON View, Query Code tab (9 languages), Visual Explain tab |
| Multiple concurrent sessions | ✓ | Single session per tab |
| Background execution | ✓ | — |
| Auto-reconnect | ✓ | — |
| Persistent session variables | ✓ | — |
| History with search/filter/preview | ✓ | Auto-save on run; navigable |
| Open in shell from other tools | — | ✓ from Collection Tab, Aggregation Editor, Query Profiler, Query Manager |

**Assessment:** Studio 3T's Query Assist mode (per-query result tabs, Visual Explain, code gen) is the more powerful execution model for iterative development. VisuaLeaf's Monaco editor offers more modern editor features (minimap, multi-session, background execution, auto-reconnect, persistent variables) useful for longer-running or operational scripts.

---

### F-AI — AI Features

*MongoDB Compass: N/A — not supported*

| Dimension | VisuaLeaf | Studio 3T |
| --- | --- | --- |
| NL → find() query | ✓ Professional | ✓ Pro/Base+ |
| NL → aggregation pipeline | ✓ Professional | ✓ Pro/Base+ |
| Plain-English explanation always on | ✓ (every query) | Not documented as always-on |
| AI providers | OpenAI (confirmed); Anthropic (unverified) | Azure AI, OpenAI GPT-4o, Anthropic Claude Opus 4.1 |
| Model selection | 11 OpenAI models user-selectable | 3 provider options |
| "Send sample data" privacy toggle | ✓ ON = Better Accuracy / OFF = More Private | Not documented as user-facing toggle |
| Conversation turns for refinement | ✓ prior turns used | Not documented |
| Multiple named AI configs | ✓ | Not documented |
| API key storage | AES-masked in Settings; never transmitted to SozoCode | Not documented as AES-masked |
| Local MCP server | — | ✓ AI-007: HTTP at 127.0.0.1:27117; 10 tools |
| MCP client integrations | — | ✓ AI-009: VS Code, Cursor, Claude Desktop, others |
| Total MCP tools | — | 10 via local server; 59 via 3T Lens platform |
| stt-cli + PII scanner | — | ✓ AI-010 |

**Assessment:** VisuaLeaf's AI focuses on in-product UX (11 model choices, plain-English explanations, privacy toggle, conversation turns). Studio 3T's AI extends outward via MCP — enabling AI agents in external tools (VS Code, Cursor, Claude Desktop) to operate against MongoDB through Studio 3T, which is a fundamentally different capability.

---

### F-SQL — SQL Tools

*MongoDB Compass: N/A — not supported. VisuaLeaf: N/A — not supported.*
*Studio 3T Pro/Base+ only.*

Studio 3T provides the only SQL capability in this comparison: full SELECT/WHERE/JOIN/GROUP BY/ORDER BY/HAVING with JOIN → $lookup translation, 9-language code gen, SQL database migration wizard (MySQL/PostgreSQL/Oracle/SQL Server via JDBC), and SQL export to MySQL/MSSQL/Oracle/PostgreSQL/IBM DB2/Sybase. In-place MongoDB schema migration (reschema) is schedulable via Task Scheduler.

---

### F-GOV — Governance

| Dimension | MongoDB Compass | VisuaLeaf | Studio 3T |
| --- | --- | --- | --- |
| Protect / write-prevention mode | ✓ (Compass "Protect mode") | — | Per-connection UI lock (UI layer only) |
| Network policy | ✓ admin-configurable | — | — |
| Telemetry configuration | ✓ | — | — |
| Startup / CLI policy (EJSON/YAML) | ✓ | — | — |
| Isolated / air-gapped edition | ✓ Isolated Edition (offline) | ✓ AES-256 local creds, never transmitted | Not documented as separate edition |
| AI controls with human approval gate | ✓ | — | — |
| RBAC user/role management | — | ✓ Professional (users/roles/inheritance/tree/actions) | ✓ via 3T Access platform |
| Visual role inheritance tree | — | ✓ Professional | — |
| Audit log | — | ✓ Professional | ✓ via 3T Lens platform |
| Collection compare (3-panel diff) | — | ✓ Professional | ✓ Pro/Base+ |
| Collection sync with direction toggle | — | ✓ Professional | ✓ Pro/Base+ |
| CDC pipeline (Kafka/Pub/Sub/HTTP) | — | — | ✓ 3TL Bridge |
| Kubernetes Helm chart | — | — | ✓ for platform components |
| OIDC multi-provider for platform auth | — | — | ✓ |
| Credential protection | OS Keytar API | AES-256 local; never transmitted; AI keys AES-masked | Built-in key store OR master password |

**Assessment:** Compass has the most comprehensive built-in policy enforcement (network policy, startup/CLI policy, AI controls, protect mode, isolated edition). VisuaLeaf has strong RBAC for teams (visual role tree, audit log) without requiring a separate platform. Studio 3T's governance scales via 3T Lens + 3T Access + 3TL Bridge for enterprise CDC, event streaming, and Kubernetes deployments.

---

### F-SCHED — Task Scheduler

*MongoDB Compass: N/A — not supported*

| Dimension | VisuaLeaf | Studio 3T |
| --- | --- | --- |
| Task types | Import, Export, Script + Professional types | Import, Export, Data Masking, Reschema, Data Compare & Sync, IntelliShell Script, SQL Migration (7 types) |
| Schedule options | 5 presets + cron | Standard + cron |
| Timezone-aware with DST | ✓ | Not documented |
| Execution config | Batch size, retry policy, timeout, concurrent execution, history retention | Not documented as named exec-config group |
| Task status states | 5 states: Pending/Running/Completed/Failed/Paused | Running/Completed/Error |
| Task actions | Run Now, Pause, Resume, Clone, Delete | Run Now, Enable/Disable, Edit, Delete |
| Email notifications | ✓ SendGrid integration | ✓ configurable (provider not specified) |
| Multiple script units per task | Not documented | ✓ multiple IntelliShell script units per task |
| Compare/sync task with diff view | — | ✓ setup wizard + results panel + sync action with direction toggle |
| Plan limits | Community: 0 tasks; Basic: 2 tasks; Professional: unlimited | Pro/Base+ required for task save |

**Assessment:** Studio 3T has more task types (7 vs. VisuaLeaf's fewer), unique multi-script-unit tasks, and a dedicated compare/sync workflow. VisuaLeaf has timezone/DST awareness, richer execution config (retry/batch/concurrent), 5 task status states, and Clone action. VisuaLeaf's Community plan cannot schedule any tasks (0 limit).

---

## Unique differentiators per product

### MongoDB Compass
- **In-use encryption (QE/CSFLE):** Only product with Queryable Encryption and CSFLE key vault + KMS configuration in the GUI.
- **Real-time performance monitoring:** Only product with live mongostat/mongotop/currentOp drill-down with pause/play visualization.
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

### Studio 3T
- **SQL tools (F-SQL):** Only product in this comparison with SQL querying, JOIN→$lookup translation, SQL migration wizard, and SQL export to relational databases.
- **Date tags (~20 shortcuts):** Only product with date-shorthand syntax (#today/#yesterday/#lastNdays etc.) expanding to MongoDB range queries at runtime — available on all editions.
- **MCP ecosystem (3T Lens, MCP server, MCP client, stt-cli):** Only product exposing MongoDB operations to external AI agents via MCP — enabling VS Code Copilot, Cursor, and Claude Desktop to operate against MongoDB.
- **Data masking (standalone + inline):** Only product with field-level data masking, offering 8 operation types applicable during Import/Export runs without modifying the original.
- **Incremental export with 5 resume points:** Unique capability for time-based incremental data extraction with persistent resume state.
- **Index copy-paste across connections:** Only product allowing an index definition to be copied from one collection and pasted to another, even across different server connections.
- **SSH Profiles with password propagation:** Named, reusable SSH tunnel profiles where password updates propagate to all dependent connections.
- **3T platform suite (3T Lens + 3T Access + 3TL Bridge):** Only product with a separate enterprise platform for CDC pipelines (MongoDB/Kafka/Pub/Sub/HTTP), Kubernetes deployment, and OIDC multi-provider.
- **Query Assist mode (per-query result tabs + Visual Explain in shell):** Only product where shell queries produce individual editable, pinnable result tabs with Visual Explain and code-gen integrated.

---

## Edition / pricing constraints

| Feature | MongoDB Compass | VisuaLeaf | Studio 3T |
| --- | --- | --- | --- |
| Visual Query Builder | N/A | Basic+ required | All editions (free) |
| AI query builder | N/A | Professional required | Pro/Base+ required |
| Enterprise auth (Kerberos/LDAP/AWS/OIDC) | Free (all confirmed) | LDAP/AWS IAM free (others roadmap) | Ultimate edition only |
| Shell / IntelliShell | N/A | Available (plan details unclear) | All editions (free) |
| Data Transfer | N/A | Community: no automation (0 tasks); Basic: 2 tasks | Pro/Base+ for task save; formats available all editions |
| Team connection sharing | N/A | N/A | Pro/Base+ required |
| Data masking | N/A | N/A | Pro/Base+ required |
| SQL tools | N/A | N/A | Pro/Base+ required |
| Task scheduler | N/A | Community: 0 tasks; Basic: 2; Professional: unlimited | Pro/Base+ required |
| Query Manager (multi-type) | No (My Queries only) | Basic+ for saved queries | All editions (Collection query type free) |
| Collection compare + sync | N/A | Professional required | Pro/Base+ required |
| RBAC dashboard | N/A | Professional required | Via 3T Access platform |
| Audit log | N/A | Professional required | Via 3T Lens platform |
| Schema validation UI | Free | Basic+ | N/A (not supported) |
| Visual ERD designer | N/A | Basic+ required | N/A |
| Atlas Search / Vector Search indexes | Free (requires Atlas M10+ or MongoDB 7.0+ local) | N/A | N/A |

---

## Key gaps summary

| Gap | Products affected |
| --- | --- |
| No SQL querying or migration | Compass, VisuaLeaf |
| No data transfer/ETL | Compass |
| No integrated shell | Compass |
| No AI features | Compass |
| No task scheduler | Compass |
| No visual ERD designer | Compass, Studio 3T |
| No JSON schema tree editor | Compass, Studio 3T |
| No schema validator creation/deploy | Studio 3T |
| No incremental export | Compass, VisuaLeaf |
| No data masking | Compass, VisuaLeaf |
| No in-use encryption (QE/CSFLE) | VisuaLeaf, Studio 3T |
| No real-time performance monitoring | VisuaLeaf, Studio 3T |
| No Atlas Search / Vector Search | VisuaLeaf, Studio 3T |
| No MCP / AI agent integration | Compass, VisuaLeaf |
| Enterprise auth gated to Ultimate edition | Studio 3T (Compass/VisuaLeaf free/roadmap) |
| geoHaystack shown without deprecation warning | Studio 3T (bug) |
| AGG-stage-toggle unverified | VisuaLeaf |
| IDX-hide-unhide unverified | VisuaLeaf |
| AGG code generation unverified | VisuaLeaf |
| AGG create view unverified | VisuaLeaf |
| SCHEMA validation strictness (warn/error) unverified | VisuaLeaf |
