# Unified Feature Dictionary

This file is the **authoritative reference** for all feature IDs and sub-feature IDs used across every product analysis in this repository. Every feature matrix, feature report, product report, and comparison report must use IDs and folder names defined here.

## Navigation

- [Repository README](README.md)
- [Cumulative report](reports/cumulative-report.md)
- [High-level comparison](reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](reports/comparisons/low-level-feature-comparison.md)

---

## Feature registry

| Feature ID | Folder name | Display name | Description |
|---|---|---|---|
| F-CONN | `connectivity` | Connectivity | Connection setup, topology, authentication, TLS, SSH, proxy, credential management |
| F-QUERY | `querying` | Querying | Query authoring, CRUD, result views, visual query builder, query management |
| F-AGG | `aggregation` | Aggregation | Pipeline builder, stage management, execution controls, code generation |
| F-SCHEMA | `schema` | Schema | Schema analysis, validation rules, visual ERD designer |
| F-IDX | `indexing-performance` | Indexing & Performance | Index lifecycle, explain plans, query profiler, performance monitoring |
| F-TRANSFER | `data-transfer` | Data Transfer | Import/export formats, data masking, migration, transformations |
| F-SHELL | `shell` | Shell | MongoDB shell / scripting environment |
| F-AI | `ai` | AI Features | AI-assisted query/pipeline generation, NL-to-query, model configuration |
| F-SQL | `sql-tools` | SQL Tools | SQL query authoring, SQL↔MongoDB migration, schema restructuring |
| F-GOV | `governance` | Governance & Security | RBAC, audit logging, security policies, collection compare/sync, platform governance |
| F-SCHED | `task-scheduler` | Task Scheduler | Scheduled task automation, execution config, monitoring, notifications |

---

## Sub-feature registry

Sub-feature IDs follow the pattern `<FEATURE>-<suffix>` where `<suffix>` is a short, dash-separated descriptor.

### F-CONN — Connectivity

| Sub-feature ID | Name | Description |
|---|---|---|
| CONN-topology | Topology types | Standalone, Replica Set, Sharded, DNS Seedlist (SRV) support |
| CONN-read-pref | Read preference | Primary / secondary read preference and tags |
| CONN-uri-paste | URI auto-fill | Paste mongodb:// or mongodb+srv:// URI to populate all fields |
| CONN-uri-export | URI export | Generate connection URI from form fields |
| CONN-import-clients | Import from clients | Import saved connections from other tools (Robo 3T, NoSQLBooster, etc.) |
| CONN-auth-std | Standard auth | None, SCRAM-SHA-256, SCRAM-SHA-1, X.509 |
| CONN-auth-enterprise | Enterprise auth | Kerberos (GSSAPI), LDAP (PLAIN), AWS IAM, MongoDB OIDC |
| CONN-tls | TLS/SSL config | CA cert, client cert, SNI, validation toggles |
| CONN-ssh | SSH tunnel | Password and private-key SSH tunnel modes |
| CONN-proxy | Proxy | HTTP and SOCKS proxy modes |
| CONN-pool-params | Pool & advanced params | Connection pool size, timeouts, retry writes, load balanced, write concern |
| CONN-org-folders | Organization & folders | Grouping connections into folders in the sidebar |
| CONN-color-coding | Color coding | Per-connection color applied to tabs and UI |
| CONN-team-sharing | Team sharing | Share connection folders with team members at permission levels |
| CONN-readonly-lock | Read-only lock | Per-connection lock preventing write operations |
| CONN-cred-storage | Credential storage | Encrypted-at-rest credential storage model |
| CONN-multi-active | Multiple active | Multiple MongoDB instances active concurrently |
| CONN-in-use-enc | In-use encryption | Queryable Encryption / CSFLE key vault configuration |
| CONN-role-docs | Role/privilege docs | Required access guide mapping features to privileges |
| CONN-test-steps | Connection test | Step-by-step connection validation (network, SSH, TLS, auth, DB, permissions) |
| CONN-sidebar-ops | Sidebar operations | Connect/disconnect, duplicate, favorite, search, refresh, error inspect |
| CONN-search-nav | Search & keyboard nav | Sidebar search bar with keyboard navigation |
| CONN-portability | Import/export configs | Export and import connection configurations as JSON or file |
| CONN-compat-docdb | Amazon DocumentDB | Compatibility with Amazon DocumentDB |
| CONN-compat-cosmos | Azure Cosmos DB | Compatibility with Azure Cosmos DB (MongoDB API) |
| CONN-compat-redis | Redis | Compatibility with Redis |

### F-QUERY — Querying

| Sub-feature ID | Name | Description |
|---|---|---|
| QUERY-filter-bar | Filter bar | MongoDB filter syntax in query bar with auto-complete |
| QUERY-projection | Projection | Include/exclude field projection controls |
| QUERY-sort | Sort | Per-field sort document controls |
| QUERY-skip-limit | Skip & limit | Offset and result-size pagination controls |
| QUERY-collation | Collation | Query-level collation locale settings |
| QUERY-max-time | Max time | maxTimeMS timeout control |
| QUERY-history | Query history | Auto-saved recent query history |
| QUERY-saved | Saved queries | Named, reusable saved/favorite queries with export/import |
| QUERY-export-lang | Export to language | Export query/filter to driver languages (Node, Java, Python, etc.) |
| QUERY-view-tree | Tree view | Hierarchical document result view |
| QUERY-view-table | Table view | Rows/columns result view with sort and column controls |
| QUERY-view-json | JSON/BSON view | Raw JSON or Extended JSON result view |
| QUERY-view-explain | Explain view | Execution plan view in query result area |
| QUERY-inline-edit | Inline editing | Click-to-edit values directly in result view |
| QUERY-batch-edit | Batch editing | Select multiple rows and apply bulk update operators |
| QUERY-doc-dialog | Document dialog | Full-document dialog editor with JSON validation |
| QUERY-multi-update | Multi-document update | updateMany() style operation with query and update tabs |
| QUERY-vqb-core | Visual Query Builder core | Drag-and-drop condition builder with AND/OR groups and operator dropdowns |
| QUERY-vqb-proj-sort | VQB projection & sort | VQB sections for projection and sort in addition to query conditions |
| QUERY-vqb-bidirectional | VQB bidirectional sync | VQB and JSON query bar keep each other in sync in real time |
| QUERY-vqb-plan | VQB plan requirement | Edition/plan required to access Visual Query Builder |
| QUERY-date-tags | Date tags | Shorthand date/time macros expanding to $gt/$lt ranges at runtime |
| QUERY-run-variants | Run variants | find(), findOne(), count() / countDocuments() run options |
| QUERY-cancel | Cancel query | Abort in-flight query execution |
| QUERY-perf-timer | Execution timer | Visual timer with threshold alerts (e.g., amber at 2s, red at 5s) |
| QUERY-undo-redo | Undo/redo | Undo and redo document edits |
| QUERY-copy-options | Copy options | Copy as JSON, value, EJSON, field name, field path |
| QUERY-pagination | Result pagination | Page size selector and page navigation for results |
| QUERY-manager | Query manager | Folder-organized query library with search, preview, types |
| QUERY-open-in | Open-in integration | Open collection in aggregation, shell, SQL, stats, chart, import, export |
| QUERY-ai-builder | AI query builder | Natural language to query/filter via AI (in querying context) |

### F-AGG — Aggregation

| Sub-feature ID | Name | Description |
|---|---|---|
| AGG-editor-layout | Editor layout | Multi-panel pipeline editor UI (stage list, stage editor, I/O panels, output) |
| AGG-stage-mgmt | Stage management | Add/duplicate/move/delete stages with keyboard shortcuts |
| AGG-stage-toggle | Stage enable/disable | Per-stage enable/disable checkbox without deletion |
| AGG-pipeline-opts | Pipeline options | allowDiskUse, collation, index hint, maxTimeMS for the whole pipeline |
| AGG-code-gen | Code generation | Export pipeline to driver languages (Node, Java, C#, Python, Ruby, PHP, etc.) |
| AGG-export-results | Export results | Export pipeline output to JSON, CSV, BSON, Excel, SQL INSERT |
| AGG-result-formats | Export format range | Specific formats supported for pipeline result export |
| AGG-save-load | Save & load pipelines | Save named pipelines with connection/DB/collection context; load from library |
| AGG-create-view | Create view | db.createView() from current pipeline |
| AGG-vqb-sync | VQB sync | Side-by-side VQB syncing bidirectionally with $match/$project stages |
| AGG-change-target | Change target | Switch source collection/database/connection mid-session |
| AGG-date-tags | Date tags | Date tag macros usable inside $match stage conditions |
| AGG-clipboard | Clipboard paste | Copy/paste full pipeline JSON to/from clipboard |
| AGG-stage-modes | Stage edit modes | Per-stage mode: form/visual, raw JSON editor, wizard |
| AGG-stage-preview | Stage preview | Per-stage input/output document preview panel |
| AGG-pagination | Result pagination | Page navigation for large pipeline output |
| AGG-timer-cancel | Timer & cancel | Live execution timer with cancel button |
| AGG-keyboard | Keyboard shortcuts | Keyboard shortcuts for execute, save, delete, duplicate, auto-complete |
| AGG-js-import-export | JS file import/export | Export/import pipeline as mongosh-format .js file |
| AGG-code-tab | Query code tab | Bidirectional read/edit JSON representation of full pipeline |
| AGG-chart-builder | Chart builder | Open pipeline output in chart/visualization builder |
| AGG-stage-count | Stage catalog | Total number of pipeline stages supported in the builder |

### F-SCHEMA — Schema

| Sub-feature ID | Name | Description |
|---|---|---|
| SCHEMA-sampling | Sampling config | Sample mode (random/first/last/all), sample count, query filter on sample |
| SCHEMA-field-prob | Field probability | Per-field probability (% of sampled docs containing that field) |
| SCHEMA-type-prob | Type probabilities | Per-field per-type breakdown revealing polymorphic fields |
| SCHEMA-explore-docs | Explore from field | Right-click field → explore docs containing / not containing that field |
| SCHEMA-histogram | Value histogram | Frequency histogram of numeric field value distribution |
| SCHEMA-top-values | Top values chart | Top-N string value frequency chart |
| SCHEMA-date-dist | Date distribution | Hourly/daily/weekly/monthly/all-time date field distribution charts |
| SCHEMA-stats-notes | Statistics & notes | Per-field numeric statistics and annotation/comments |
| SCHEMA-doc-export | Documentation export | Export schema documentation to Word/CSV/JSON |
| SCHEMA-rename-discover | Rename from discovery | Trigger bulk field rename from outlier field found in schema tree |
| SCHEMA-geo-analysis | Geo schema analysis | Map-backed analysis for geo fields with interactive filter drawing |
| SCHEMA-file-export | Schema file export | Export analyzed schema to standard file formats (JSON Schema, etc.) |
| SCHEMA-view-editor | View editor | Visual db.createView() pipeline builder |
| SCHEMA-view-from-sql | View from SQL | Create view pipeline from SQL query (requires SQL Tools feature) |
| SCHEMA-views-tree | Views in tree | Created views visible as first-class queryable objects in connection tree |
| SCHEMA-validation-model | Validation rule model | $jsonSchema and query-operator style validation rule authoring |
| SCHEMA-validation-strictness | Validation strictness | warn/error action and strict/moderate level configuration |
| SCHEMA-validation-ui | Validation UI workflows | Add/edit/generate/preview/apply validation rule flows |
| SCHEMA-validation-limits | Validation limits | Scope limits (e.g., max distinct fields, unsupported deployment types) |
| SCHEMA-json-editor | JSON schema editor | Tree-based visual JSON schema editor with field type constraints |
| SCHEMA-deploy-validator | Deploy validator | Push local schema as $jsonSchema validator to live collection |
| SCHEMA-import-from-db | Import from database | Analyze collection sample and auto-generate schema definition |
| SCHEMA-bson-types | BSON type coverage | All BSON types supported in schema definition (string, number, objectId, etc.) |
| SCHEMA-field-constraints | Field constraints | Per-type constraints (minLength, maxLength, pattern, minimum, maximum, etc.) |
| SCHEMA-verify | Schema verification | Run $jsonSchema filter; view all non-conforming documents |
| SCHEMA-designer-canvas | Visual canvas | Infinite canvas for displaying collection/relationship diagrams |
| SCHEMA-designer-auto | Auto-generate diagram | Auto-generate full diagram from all collections in a database |
| SCHEMA-designer-links | Relationship detection | Graph-theory algorithm to detect and draw collection relationships |
| SCHEMA-designer-color | Color coding | Per-collection color presets on canvas |
| SCHEMA-designer-layouts | Named layouts | Save and restore named custom canvas arrangements |
| SCHEMA-designer-portability | Diagram portability | Export/import diagram to/from file |

### F-IDX — Indexing & Performance

| Sub-feature ID | Name | Description |
|---|---|---|
| IDX-inventory | Index inventory | List indexes with name, type, size, usage count |
| IDX-type-single | Single-field index | Single ascending/descending field index |
| IDX-type-compound | Compound index | Multi-field index with ESR guidance |
| IDX-type-multikey | Multikey index | Array field auto-multikey index |
| IDX-type-text | Text index | Full-text search index with language/weight config |
| IDX-type-wildcard | Wildcard index | $** or path.** wildcard index for dynamic schemas |
| IDX-type-2d | 2D index | Flat-geometry 2d geospatial index |
| IDX-type-2dsphere | 2DSphere index | Earth-sphere GeoJSON geospatial index |
| IDX-type-hashed | Hashed index | Equality and sharding key hashed index |
| IDX-type-ttl | TTL index | Date-field auto-expiry TTL index |
| IDX-type-haystack | geoHaystack index | Deprecated (MongoDB 4.4+) bucket geospatial index |
| IDX-props-unique-sparse | Unique & sparse | Unique constraint and sparse (skip missing field) properties |
| IDX-props-hidden | Hidden index | Hide index from query planner without dropping (MongoDB 4.4+) |
| IDX-props-partial | Partial index | Filter expression to index only matching documents |
| IDX-props-collation | Collation index | Case-insensitive and locale-aware index via collation |
| IDX-build-mode | Build mode | Foreground vs background index creation mode |
| IDX-copy-paste | Copy/paste index | Copy index definition and paste to another collection |
| IDX-hide-unhide | Hide/unhide | Toggle index visibility for query planner impact testing |
| IDX-atlas-search | Atlas Search index | Create/manage Atlas Search (Lucene) indexes |
| IDX-vector-search | Vector Search index | Create/manage Vector Search indexes for semantic search |
| IDX-collation-opts | Collation options | Full ICU locale/strength/case/numeric collation configuration |
| IDX-text-opts | Text index options | Language, language-override field, text index version, field weights |
| IDX-geo-opts | Geo index options | Bounds, precision bits, 2dsphere version configuration |
| IDX-advanced-opts | Advanced index opts | Partial filter expression, wildcard projection, commit quorum, clustered |
| IDX-quick-actions | Quick-action presets | One-click common index creation presets |
| IDX-explain-brief | Explain — plan mode | Plan-only explain (no execution); fast, always available |
| IDX-explain-full | Explain — full stats | Full execution-stats explain with per-stage timing and doc counts |
| IDX-explain-sources | Explain entry points | Explain available from query tab, shell, aggregation, profiler |
| IDX-profiler-config | Profiler configuration | Profiling level (0/1/2), slow threshold, sample rate, max log size |
| IDX-profiler-analysis | Profiler analysis | Query grouping (exact vs shape), time filters, percentile lines, COLLSCAN flags |
| IDX-profiler-drilldown | Profiler drill-down | Per-execution detail, open in tools, add index shortcut |
| IDX-profiler-export | Profiler export | Export profiler data as CSV or JSON |
| IDX-profiler-live | Live monitoring | Real-time current operations view with kill button |
| IDX-perf-insights | Performance insights | System-level modeling/indexing improvement suggestions |
| IDX-realtime-perf | Real-time performance | Live operational metrics (mongostat/mongotop/currentOp) with pause/play |
| IDX-stop-ops | Stop operations | Kill long-running operations from performance view |

### F-TRANSFER — Data Transfer

| Sub-feature ID | Name | Description |
|---|---|---|
| TRANSFER-import-csv | Import CSV | Import from CSV file with delimiter, header, type, and encoding options |
| TRANSFER-import-json | Import JSON | Import from JSON file with validation and insertion mode options |
| TRANSFER-import-bson | Import BSON | Import from BSON/mongodump folder or archive |
| TRANSFER-import-sql | Import from SQL | Import from relational database (MySQL, PostgreSQL, Oracle, SQL Server) |
| TRANSFER-import-mongo | Import from MongoDB | Copy from another MongoDB collection (cross-server/database) |
| TRANSFER-import-modes | Insertion modes | Insert / ignore-duplicate / upsert / merge / replace on import |
| TRANSFER-export-src | Export source selection | Choose: collection, view, query result, aggregation result, selected docs |
| TRANSFER-export-csv | Export CSV | Export to CSV with delimiter, field list, null handling, presets |
| TRANSFER-export-excel | Export Excel | Export to .xlsx with auto-sizing and text alignment |
| TRANSFER-export-json | Export JSON | Export to JSON (shell format or mongoexport-compatible) |
| TRANSFER-export-bson | Export BSON | Export to BSON/mongodump folder or archive with compression |
| TRANSFER-export-sql | Export SQL | Export to relational database (MySQL, MSSQL, Oracle, PostgreSQL) |
| TRANSFER-export-mongo | Export to MongoDB | Copy to another MongoDB collection (cross-server/database) |
| TRANSFER-export-sql-stmts | Export SQL INSERT | Export as SQL INSERT statements file |
| TRANSFER-incremental | Incremental export | Tracking-field–based incremental export with resume points |
| TRANSFER-masking-tool | Data masking tool | Standalone field-level obfuscation tool with preview and exception logs |
| TRANSFER-masking-types | Masking techniques | Per-BSON-type masking rules (null, exclude, shuffle, scramble, substitute, etc.) |
| TRANSFER-masking-inline | Inline masking | Apply masking rules during import/export without modifying source |
| TRANSFER-task-save | Save as task | Save import/export config as a schedulable task |
| TRANSFER-field-mapping | Field mapping | Map source field names to destination field names |
| TRANSFER-transform-types | Type conversion | Data type conversion during import (e.g., string → date) |
| TRANSFER-transform-filter | Import filter | Filter out documents by condition before import |
| TRANSFER-transform-js | Custom JS transform | User-defined JavaScript functions applied per document during transfer |
| TRANSFER-transform-pipeline | Pipeline pre-export | Apply aggregation pipeline stages as server-side pre-export transform |

### F-SHELL — Shell

| Sub-feature ID | Name | Description |
|---|---|---|
| SHELL-engine | Shell engine | Underlying editor engine and shell runtime (mongosh, Monaco, etc.) |
| SHELL-autocomplete | Auto-complete | db., collection., field names, operators, shell methods auto-complete |
| SHELL-validation | Syntax validation | Real-time syntax error highlighting and error line marking |
| SHELL-minimap | Minimap | Code minimap for navigation in large scripts |
| SHELL-run-all | Run all | Execute entire script top-to-bottom (F5) |
| SHELL-run-select | Run selected | Execute only selected/highlighted text (Ctrl+F5) |
| SHELL-run-cursor | Run to cursor | Execute from start of script to cursor line |
| SHELL-result-tabs | Result tabs | Per-query result tabs with shell output tab |
| SHELL-result-views | Result view modes | Tree, table, BSON view modes in result tabs |
| SHELL-save-load | Save & load scripts | Save, load, export (.js/.json), and import scripts |
| SHELL-history | Script history | Auto-saved query history with search and preview |
| SHELL-sessions-multi | Multiple sessions | Independent shell sessions via multiple activity tabs |
| SHELL-sessions-vars | Session variable scope | Variables persist within a session across executions |
| SHELL-reconnect | Auto-reconnect | Automatic reconnect on network interruption |
| SHELL-background | Background execution | Script continues executing when switching to other tabs |
| SHELL-integrations | Tool integrations | Open shell results in other tools; open from other tools into shell |
| SHELL-modes | Execution modes | Shell mode (raw output) vs Query Assist mode (editable result tabs) |

### F-AI — AI Features

| Sub-feature ID | Name | Description |
|---|---|---|
| AI-nl-query | NL to query | Natural language converted to find()-style query filter |
| AI-nl-pipeline | NL to pipeline | Natural language converted to full aggregation pipeline |
| AI-explanation | Query explanation | Plain-English explanation included with every AI-generated output |
| AI-schema-aware | Schema-aware | Uses collection field names and BSON types from live schema |
| AI-sample-context | Sample context | Optionally includes sample documents for higher AI accuracy |
| AI-conversation | Conversation context | Prior conversation turns used for iterative query refinement |
| AI-models | Model selection | Supported AI model list and default recommendation |
| AI-providers | Provider support | Supported AI provider integrations (OpenAI, Azure, Anthropic, etc.) |
| AI-privacy | Privacy mode | Toggle between schema-only (private) and schema+samples (accurate) modes |
| AI-key-storage | API key storage | Local encrypted storage of API keys; never transmitted to vendor |
| AI-multi-config | Multiple configs | Multiple named AI configurations with enable/disable toggle |
| AI-plan-req | Plan requirement | Edition or subscription tier required to access AI features |
| AI-001 | AI helper backends | Studio 3T AI helper provider backend set (Azure/OpenAI/Anthropic) |
| AI-002 | AI helper configuration | Studio 3T AI helper runtime configuration controls (temperature/enable) |
| AI-003 | AI helper NL generation | Studio 3T natural-language query/pipeline/script generation workflow |
| AI-004 | AI helper apply results | Apply/copy generated AI results into active editors |
| AI-005 | AI helper history | Local AI session history and restore across restarts |
| AI-006 | AI helper shortcuts | Keyboard shortcut support for AI helper actions |
| AI-007 | Local MCP server config | Local MCP HTTP server availability and configuration |
| AI-008 | Local MCP toolset | Local MCP tool catalog exposed by Studio 3T |
| AI-009 | MCP client compatibility | Supported MCP client integrations for Studio 3T local server |
| AI-010 | stt-cli binary | Standalone 3T MCP binary capability surface |
| AI-011 | stt-cli feature set | stt-cli read-only browsing/query/schema/PII capabilities |
| AI-012 | 3T Build AI agent | AI agent support in 3T Build browser IDE context |
| AI-model-chooser | Model chooser | User-selectable AI model per configuration |
| AI-sample-data-toggle | Sample data toggle | User-facing toggle for sending sample data to improve AI accuracy |
| AI-context-turns | Conversation turns | Multi-turn context retention for iterative refinement |
| AI-named-configs | Named AI configs | Multiple named AI configurations in settings |
| AI-schema-context | Schema context | Injection of field/schema metadata into AI prompts |
| AI-local-mcp | Local MCP server | Presence of local MCP server endpoint for AI tooling |
| AI-mcp-client | MCP client support | External MCP clients supported by product integration |
| AI-mcp-tools | MCP tools count | Number and scope of MCP tools exposed by product |
| AI-stt-cli | stt-cli + PII scanner | Standalone CLI with read-only operations and PII scanner |
| AI-plan-gate | AI plan gate | Edition/plan gating for AI features |

### F-SQL — SQL Tools

| Sub-feature ID | Name | Description |
|---|---|---|
| SQL-expressions | SQL expressions | Supported SQL syntax: SELECT, WHERE, JOIN, GROUP BY, aggregates, LIKE, etc. |
| SQL-join-mapping | JOIN mapping | Visual JOIN condition editor mapping SQL joins to MongoDB lookups |
| SQL-migration | SQL migration wizard | Guided migration of SQL schema/data to MongoDB collections |
| SQL-reschema | Schema restructuring | Reshape MongoDB schema: merge, split, rename, type-change operations |
| SQL-code-gen | Code generation | Generate equivalent MongoDB query/aggregation from SQL query |
| SQL-query-manager | SQL query manager | Save, organize, and rerun SQL queries with target collection binding |
| SQL-migration-schema | SQL migration schema mapping | Schema mapping/transformation stage in SQL→Mongo migration |
| SQL-migration-1to1 | SQL one-to-one mapping | One-to-one relationship mapping in SQL→Mongo migration |
| SQL-migration-1to-many | SQL one-to-many mapping | One-to-many relationship mapping in SQL→Mongo migration |
| SQL-export-field-map | SQL export field mapping | Field-to-column mapping modes for Mongo→SQL export |
| SQL-export-relations | SQL export relations | Relationship mapping options for Mongo→SQL export |
| SQL-export-monitor | SQL export monitoring | SQL export preview/monitoring/logging workflow |
| SQL-export-targets | SQL export targets | Supported destination SQL engines for Mongo→SQL export |

### F-GOV — Governance & Security

| Sub-feature ID | Name | Description |
|---|---|---|
| GOV-readonly-mode | Read-only mode | UI-level read-only/write-protect mode hiding write operations |
| GOV-cred-protection | Credential protection | Protect mode masking secrets and blocking edit/copy in UI |
| GOV-network-policy | Network policy | Restrict outbound network traffic to DB-only communication mode |
| GOV-telemetry | Telemetry controls | Configurable telemetry behavior via settings/CLI/config |
| GOV-startup-policy | Startup policy | EJSON/YAML config setting immutable startup behavior |
| GOV-cli-policy | CLI policy | Command-line enforcement of security/governance settings at launch |
| GOV-ai-controls | AI data controls | AI context disclosure and approval/disable workflows |
| GOV-cred-storage-os | OS credential storage | OS-level credential API (Keytar/AES-256) for secrets |
| GOV-isolated-edition | Isolated edition | Edition variant restricting outbound requests to chosen server only |
| GOV-air-gapped | Air-gapped support | Fully offline operation after one-time activation |
| GOV-rbac-users | RBAC user management | Create, modify, delete MongoDB database users |
| GOV-rbac-roles | Custom role creation | Granular privilege definition on specific databases and collections |
| GOV-rbac-inheritance | Role inheritance | Inherit from built-in or custom roles (role chains) |
| GOV-rbac-tree | Privilege tree view | Hierarchical display of effective privileges |
| GOV-rbac-actions | Privilege actions | Full set of MongoDB privilege actions (read, write, dbAdmin, etc.) |
| GOV-audit-log | Audit logging | Track queries, modifications, and connections with timestamp and user info |
| GOV-data-masking | Data masking | Mask sensitive fields in query/export results for governance |
| GOV-collection-compare | Collection compare | Field-level diff comparison between collections across connections |
| GOV-collection-sync | Collection sync | Directed sync (insert/update/delete) between compared collections |
| GOV-platform-lens | 3T Lens workspace | 3T Lens browser-based governance workspace (Studio 3T platform) |
| GOV-platform-access | 3T Access identity | 3T Access identity and permission management plane (Studio 3T platform) |
| GOV-platform-cdc | CDC pipeline | 3TL Bridge change-data-capture pipeline engine (Studio 3T platform) |
| GOV-002 | Lens policy templates | 3T Lens compliance policy templates and checks |
| GOV-003 | Lens alert channels | 3T Lens alert channels (Slack/email/webhook) |
| GOV-004 | Lens PII classification | 3T Lens PII scanning/classification workflow |
| GOV-005 | Lens versioned diffs | 3T Lens field history and document diff tracking |
| GOV-006 | Lens performance suggestions | 3T Lens performance/index suggestions |
| GOV-007 | Lens MCP integration | 3T Lens MCP integration and governed tool access |
| GOV-010 | Bridge transform studio | 3TL Bridge transformation studio pipeline tooling |
| GOV-011 | Bridge PII masking | 3TL Bridge real-time PII masking with compliance templates |
| GOV-012 | Bridge security identity | 3TL Bridge credentials/OIDC security configuration |
| GOV-013 | Bridge deployment scaling | 3TL Bridge Helm/deployment/scaling/observability support |
| GOV-platform-bridge | Platform bridge integration | 3TL Bridge integration surface for event/data pipelines |
| GOV-platform-k8s | Platform Kubernetes deployment | Kubernetes Helm deployment support for platform components |
| GOV-platform-oidc | Platform OIDC providers | Multi-provider OIDC support in platform auth stack |
| GOV-protect-mode | Protect mode | UI-level destructive-write prevention mode |
| GOV-telemetry-config | Telemetry configuration | Telemetry opt-out/configuration controls |

### F-SCHED — Task Scheduler

| Sub-feature ID | Name | Description |
|---|---|---|
| SCHED-types-time | Time-based schedules | One-time, hourly, daily, weekly, monthly schedule types |
| SCHED-cron | Cron expression | Full cron expression support for advanced schedules |
| SCHED-timezone | Timezone support | Timezone-aware scheduling with DST handling |
| SCHED-task-types | Task types | Supported task types (import, export, masking, reschema, compare, script, etc.) |
| SCHED-exec-config | Execution config | Batch size, retry count, timeout, concurrent task limit |
| SCHED-history-retention | History retention | Maximum execution records retained |
| SCHED-progress | Progress monitoring | Real-time progress bars and document counts during execution |
| SCHED-status-states | Task status states | Scheduled / Running / Completed / Failed / Paused state machine |
| SCHED-actions | Task actions | Run Now, Pause/Resume, Edit, Clone, Delete, View History |
| SCHED-notifications | Notifications | Email and in-app notifications on success, failure, warning |
| SCHED-preset-types | Preset schedule types | Named schedule presets (once/hourly/daily/weekly/monthly) |
| SCHED-task-actions | Task management actions | Run/enable-disable/edit/clone/delete style lifecycle actions |
| SCHED-script-tasks | Script task units | Scheduler support for script-based task definitions |
| SCHED-compare-setup | Compare setup | Data compare task setup workflow |
| SCHED-compare-results | Compare results | Data compare result/diff presentation |
| SCHED-compare-sync | Compare sync actions | Sync operations launched from compare results |
| SCHED-compare-schedule | Compare schedule save | Save compare workflows as scheduled tasks |
| SCHED-plan-limits | Scheduler plan limits | Plan-tier limits for task scheduler capabilities |
| SCHED-task-save | Task save from tools | Save import/export/compare configs as scheduler tasks |
| SCHED-retry | Retry policy | Retry behavior configuration for scheduled runs |
| SCHED-concurrent | Concurrent execution | Max concurrent task execution control |
| SCHED-batch | Batch size | Batch size configuration for scheduled execution |
| SCHED-history | Execution history | Historical execution record visibility |
| SCHED-email | Email provider config | Email notification provider-level configuration |
| SCHED-recur-once | Recurrence once | One-time scheduled execution pattern |
| SCHED-recur-daily | Recurrence daily | Daily scheduled execution pattern |
| SCHED-recur-interval | Recurrence interval | Every N minutes/hours execution pattern |
| SCHED-recur-weekly | Recurrence weekly | Weekly scheduled execution pattern |
| SCHED-recur-monthly | Recurrence monthly | Monthly scheduled execution pattern |

### Supplemental aliases used in current matrices

| Sub-feature ID | Name | Description |
|---|---|---|
| SHELL-open-from | Open in shell from tools | Open shell from query/aggregation/profiler/manager contexts |
| SHELL-sessions | Shell sessions | Multiple concurrent shell sessions |
| SHELL-background-exec | Background execution | Shell script execution continues when switching tabs |
| SHELL-auto-reconnect | Auto reconnect | Shell reconnect behavior on connection drop |
| SHELL-persistent-vars | Persistent variables | Variables persist within same shell session |
| TRANSFER-plan-limits | Transfer task plan limits | Plan-tier limits specifically for transfer task automation |

---

## Product × feature coverage matrix

This table shows which features are applicable per product. Features not in a product's folder do not apply to that product.

| Feature | Studio 3T | MongoDB Compass | VisuaLeaf |
|---|---|---|---|
| F-CONN | ✓ | ✓ | ✓ |
| F-QUERY | ✓ | ✓ | ✓ |
| F-AGG | ✓ | ✓ | ✓ |
| F-SCHEMA | ✓ | ✓ | ✓ |
| F-IDX | ✓ | ✓ | ✓ |
| F-TRANSFER | ✓ | — | ✓ |
| F-SHELL | ✓ | — | ✓ |
| F-AI | ✓ | — | ✓ |
| F-SQL | ✓ | — | — |
| F-GOV | ✓ | ✓ | ✓ |
| F-SCHED | ✓ | — | ✓ |

---

## Naming rules for future analysis

1. **Feature folder names** must match the `Folder name` column exactly.
2. **Sub-feature IDs** must be used verbatim in all capability matrices.
3. A sub-feature ID not in this dictionary must be proposed and added here before use.
4. Product-specific sub-features that have no cross-product equivalent should still use a dictionary ID — add it to this file first.
5. Features not applicable to a product are omitted from that product's folder — do not add a placeholder.

---

## Changelog

| Date | Change | Author |
|---|---|---|
| 2026-06-24 | Added missing sub-feature IDs currently used in `products/` and comparison reports; synchronized dictionary coverage with active matrices | Copilot |
| 2026-06-22 | Initial unified dictionary created; all 11 features and all sub-feature IDs defined | Copilot |
