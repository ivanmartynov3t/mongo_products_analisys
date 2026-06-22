# Low-Level Feature Comparison

This report compares normalized sub-feature capabilities across all analyzed products. Sub-feature IDs come from the [unified feature dictionary](../../feature-dictionary.md).

## Navigation

- [Cumulative report index](../cumulative-report.md)
- [High-level comparison](high-level-product-comparison.md)
- [Feature dictionary](../../feature-dictionary.md)
- [Studio 3T product report](../../products/3t/studio-3t/product-report.md)
- [MongoDB Compass product report](../../products/third-party/mongodb-compass/product-report.md)
- [VisuaLeaf product report](../../products/third-party/visual-eaf/product-report.md)

## Current baseline coverage

- MongoDB Compass: F-CONN, F-QUERY, F-AGG, F-SCHEMA, F-IDX, F-GOV
- VisuaLeaf: F-CONN, F-QUERY, F-AGG, F-SCHEMA, F-IDX, F-TRANSFER, F-SHELL, F-AI, F-GOV, F-SCHED
- Studio 3T: all 11 features

## Sub-feature comparison table

Gap types: `Missing` | `Partial` | `Mismatch` | `Constraint` | `Roadmap`

| Feature ID | Sub-feature ID | Sub-feature name | MongoDB Compass | VisuaLeaf | Studio 3T | Gap type | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F-CONN | CONN-topology | Topology types | Supported (standalone, RS, sharded, SRV) | Supported (all 4 topology types) | Supported (all 4 topology types) | — | [Compass](../../products/third-party/mongodb-compass/features/connectivity/feature-matrix.md) · [VisuaLeaf](../../products/third-party/visual-eaf/features/connectivity/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/connectivity/feature-matrix.md) |
| F-CONN | CONN-multi-active | Multiple active connections | Supported (Compass 1.44.0+) | Not documented | Not documented as a UI concept (separate tabs per connection) | Partial | [Compass](../../products/third-party/mongodb-compass/features/connectivity/feature-matrix.md) |
| F-CONN | CONN-auth-std | Standard auth | Supported (SCRAM, X.509, None) | Supported (None, SCRAM-256, SCRAM-1, X.509) | Supported (None, SCRAM-256, SCRAM-1, X.509) | — | All |
| F-CONN | CONN-auth-enterprise | Enterprise auth | Supported (OIDC, Kerberos, LDAP, AWS IAM) | Partial (LDAP, AWS IAM confirmed; Kerberos/OIDC roadmap Q2 2026) | Supported (Ultimate only — Kerberos, LDAP, AWS IAM, OIDC) | Constraint/Roadmap | All |
| F-CONN | CONN-tls | TLS/SSL config | Supported | Supported | Supported | — | All |
| F-CONN | CONN-ssh | SSH tunnel | Supported (password + key) | Supported (password + key) | Supported (SSH Profiles with reuse) | — | All |
| F-CONN | CONN-proxy | Proxy | Supported (Socks5) | Not documented | Supported (HTTP + SOCKS per connection) | Missing (VisuaLeaf) | [Compass](../../products/third-party/mongodb-compass/features/connectivity/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/connectivity/feature-matrix.md) |
| F-CONN | CONN-team-sharing | Team sharing | Not supported | Not supported | Supported (Pro/Base+ — invite by email, permission levels) | Missing | [Studio 3T](../../products/3t/studio-3t/features/connectivity/feature-matrix.md) |
| F-CONN | CONN-in-use-enc | In-use encryption | Supported (QE/CSFLE config) | Not documented | Not documented | Missing (VisuaLeaf, Studio 3T) | [Compass](../../products/third-party/mongodb-compass/features/connectivity/feature-matrix.md) |
| F-CONN | CONN-cred-storage | Credential storage | Supported (OS Keytar API) | Supported (AES-256, local only) | Supported (built-in key or master password) | — | All |
| F-QUERY | QUERY-filter-bar | Filter bar | Supported | Supported (ACE editor, Ctrl+Space) | Supported (auto-complete, BSON shortcuts) | — | All |
| F-QUERY | QUERY-vqb-core | Visual Query Builder | Not supported | Supported (Basic+, drag-and-drop conditions) | Supported (all editions, bidirectional sync) | Missing (Compass) | [VisuaLeaf](../../products/third-party/visual-eaf/features/querying/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/querying/feature-matrix.md) |
| F-QUERY | QUERY-export-lang | Export to driver language | Supported (8 languages) | Not documented | Supported via Aggregation Code tab | Partial (VisuaLeaf) | [Compass](../../products/third-party/mongodb-compass/features/querying/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/querying/feature-matrix.md) |
| F-QUERY | QUERY-ai-builder | AI query builder | Not supported | Supported (Professional, 11 OpenAI models) | Supported (Pro/Base+, Azure/OpenAI/Anthropic) | Missing (Compass) | [VisuaLeaf](../../products/third-party/visual-eaf/features/querying/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/ai/feature-matrix.md) |
| F-QUERY | QUERY-date-tags | Date tags | Not supported | Not supported | Supported (all editions) | Missing (Compass, VisuaLeaf) | [Studio 3T](../../products/3t/studio-3t/features/querying/feature-matrix.md) |
| F-QUERY | QUERY-manager | Query manager | Supported (My Queries view) | Supported (Basic+, folder hierarchy) | Supported (folder hierarchy, multi-type) | Constraint | All |
| F-AGG | AGG-editor-layout | Editor layout | Supported (Stage View, Text View, Focus Mode) | Supported (stage list + Monaco editor + preview) | Supported (5-region UI) | — | All |
| F-AGG | AGG-code-gen | Code generation | Supported (8 languages) | Not documented | Supported (9 language targets) | Partial (VisuaLeaf) | [Compass](../../products/third-party/mongodb-compass/features/aggregation/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/aggregation/feature-matrix.md) |
| F-AGG | AGG-stage-modes | Stage edit modes | Supported (Stage Wizard + Text View) | Supported (Form Mode + MongoDB Editor per stage) | Supported (code editor only) | Mismatch | All |
| F-AGG | AGG-chart-builder | Chart builder | Not documented | Supported (opens Chart Builder from pipeline) | Not documented | Missing (Compass, Studio 3T) | [VisuaLeaf](../../products/third-party/visual-eaf/features/aggregation/feature-matrix.md) |
| F-SCHEMA | SCHEMA-sampling | Sampling config | Supported ($sample, 1000 docs) | Supported (100-doc sample for schema import) | Supported (random/first/last/all, configurable count) | Mismatch | All |
| F-SCHEMA | SCHEMA-validation-model | Validation rule model | Supported ($jsonSchema + query-operator) | Supported ($jsonSchema, JSON Schema Draft 4) | Not supported (Studio 3T has view creation but not validation rules) | Missing (Studio 3T) | [Compass](../../products/third-party/mongodb-compass/features/schema/feature-matrix.md) · [VisuaLeaf](../../products/third-party/visual-eaf/features/schema/feature-matrix.md) |
| F-SCHEMA | SCHEMA-designer-canvas | Visual ERD canvas | Not supported | Supported (Basic+, infinite canvas) | Not supported | Missing (Compass, Studio 3T) | [VisuaLeaf](../../products/third-party/visual-eaf/features/schema/feature-matrix.md) |
| F-SCHEMA | SCHEMA-view-editor | View editor | Not documented | Not documented | Supported (db.createView() builder) | Missing (Compass, VisuaLeaf) | [Studio 3T](../../products/3t/studio-3t/features/schema/feature-matrix.md) |
| F-IDX | IDX-inventory | Index inventory | Supported | Supported | Supported | — | All |
| F-IDX | IDX-atlas-search | Atlas Search index | Supported (Atlas M10+ / MongoDB 7.0+) | Not documented | Not documented | Missing (VisuaLeaf, Studio 3T) | [Compass](../../products/third-party/mongodb-compass/features/indexing-performance/feature-matrix.md) |
| F-IDX | IDX-vector-search | Vector Search index | Supported (Atlas/local constraints) | Not documented | Not documented | Missing (VisuaLeaf, Studio 3T) | [Compass](../../products/third-party/mongodb-compass/features/indexing-performance/feature-matrix.md) |
| F-IDX | IDX-profiler-config | Profiler configuration | Not documented | Supported (threshold, level, sample rate, log size) | Supported (level 0/1/2, slow threshold) | Partial (Compass) | [VisuaLeaf](../../products/third-party/visual-eaf/features/indexing-performance/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/indexing-performance/feature-matrix.md) |
| F-IDX | IDX-perf-insights | Performance insights | Supported (advisory recommendations) | Supported (index recommendations in profiler) | Not documented as separate insights | Partial | [Compass](../../products/third-party/mongodb-compass/features/indexing-performance/feature-matrix.md) · [VisuaLeaf](../../products/third-party/visual-eaf/features/indexing-performance/feature-matrix.md) |
| F-TRANSFER | TRANSFER-import-sql | Import from SQL | Not supported | Not supported | Supported (Pro/Base+ — MySQL, PostgreSQL, Oracle, MSSQL) | Missing | [Studio 3T](../../products/3t/studio-3t/features/data-transfer/feature-matrix.md) |
| F-TRANSFER | TRANSFER-masking-tool | Data masking tool | Not supported | Partial (Basic+, limited docs) | Supported (Pro/Base+ — full standalone tool) | Constraint/Partial | [Studio 3T](../../products/3t/studio-3t/features/data-transfer/feature-matrix.md) |
| F-TRANSFER | TRANSFER-incremental | Incremental export | Not supported | Not supported | Supported | Missing (Compass, VisuaLeaf) | [Studio 3T](../../products/3t/studio-3t/features/data-transfer/feature-matrix.md) |
| F-SHELL | SHELL-engine | Shell engine | Not available | Supported (Monaco + mongosh) | Supported (ACE editor + mongosh) | Missing (Compass) | [VisuaLeaf](../../products/third-party/visual-eaf/features/shell/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/shell/feature-matrix.md) |
| F-SHELL | SHELL-modes | Execution modes | Not available | Not documented as separate modes | Supported (Shell mode vs Query Assist mode) | Mismatch | [Studio 3T](../../products/3t/studio-3t/features/shell/feature-matrix.md) |
| F-AI | AI-nl-query | NL to query | Not supported | Supported (Professional, 11 OpenAI models) | Supported (Pro/Base+) | Missing (Compass) | [VisuaLeaf](../../products/third-party/visual-eaf/features/ai/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/ai/feature-matrix.md) |
| F-AI | AI-providers | Provider support | Not supported | Partial (OpenAI confirmed; Anthropic unverified) | Supported (Azure OpenAI, OpenAI, Anthropic) | Constraint | [VisuaLeaf](../../products/third-party/visual-eaf/features/ai/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/ai/feature-matrix.md) |
| F-SQL | SQL-expressions | SQL expressions | Not supported | Not supported | Supported (Pro/Base+, full SELECT/WHERE/JOIN/GROUP BY) | Missing (Compass, VisuaLeaf) | [Studio 3T](../../products/3t/studio-3t/features/sql-tools/feature-matrix.md) |
| F-SQL | SQL-migration | SQL migration wizard | Not supported | Not supported | Supported (Pro/Base+) | Missing (Compass, VisuaLeaf) | [Studio 3T](../../products/3t/studio-3t/features/sql-tools/feature-matrix.md) |
| F-GOV | GOV-rbac-users | RBAC user management | Not documented | Supported (Professional) | Partial (via 3T Access platform) | Constraint/Missing | [VisuaLeaf](../../products/third-party/visual-eaf/features/governance/feature-matrix.md) |
| F-GOV | GOV-audit-log | Audit logging | Not documented | Supported (Professional) | Partial (via 3T Lens platform) | Constraint | [VisuaLeaf](../../products/third-party/visual-eaf/features/governance/feature-matrix.md) |
| F-GOV | GOV-collection-compare | Collection compare | Not documented | Supported (Professional, 3-panel diff) | Supported (Pro/Base+) | Missing (Compass) | [VisuaLeaf](../../products/third-party/visual-eaf/features/governance/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/governance/feature-matrix.md) |
| F-GOV | GOV-platform-cdc | CDC pipeline | Not supported | Not supported | Supported (3TL Bridge — Studio 3T platform) | Missing (Compass, VisuaLeaf) | [Studio 3T](../../products/3t/studio-3t/features/governance/feature-matrix.md) |
| F-SCHED | SCHED-task-types | Task types | Not supported | Import/Export only | Import, Export, Masking, Reschema, Compare/Sync, Shell scripts | Missing (Compass) | [VisuaLeaf](../../products/third-party/visual-eaf/features/task-scheduler/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/task-scheduler/feature-matrix.md) |
| F-SCHED | SCHED-notifications | Notifications | Not supported | Supported (email via SendGrid + in-app) | Supported (configurable per task) | Missing (Compass) | [VisuaLeaf](../../products/third-party/visual-eaf/features/task-scheduler/feature-matrix.md) · [Studio 3T](../../products/3t/studio-3t/features/task-scheduler/feature-matrix.md) |

## Notes

- All sub-feature IDs in this table come from [feature-dictionary.md](../../feature-dictionary.md).
- As more features are fully analyzed, replace `Not documented` with explicit behavior from the product's feature matrix.
- The gap type `Constraint` means the feature exists but requires a specific edition, deployment, or plan.
