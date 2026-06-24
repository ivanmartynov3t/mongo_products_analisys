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

| Feature area | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| F-CONN — Connectivity | ✓ | ✓ | ✓ |
| F-QUERY — Querying | ✓ | ✓ | ✓ |
| F-AGG — Aggregation | ✓ | ✓ | ✓ |
| F-SCHEMA — Schema | ✓ | ✓ | ✓ |
| F-IDX — Indexing & Performance | ✓ | ✓ | ✓ |
| F-TRANSFER — Data Transfer | ✓ | — | ✓ |
| F-SHELL — Shell | ✓ | — | ✓ |
| F-AI — AI features | ✓ | — | ✓ |
| F-SQL — SQL tools | ✓ | — | — |
| F-GOV — Governance | ✓ | ✓ | ✓ |
| F-SCHED — Task scheduler | ✓ | — | ✓ |

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

| Feature ID | Sub-feature ID | Sub-feature name | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- | --- | --- |
| F-CONN | CONN-topology | Topology types | ✅ | ✅ | ✅ |
| F-CONN | CONN-multi-active | Multiple concurrent connections | ❓ | ✅ | ❓ |
| F-CONN | CONN-read-pref | Read preference | ✅ | ❓ | ✅ |
| F-QUERY | QUERY-filter-bar | Filter bar / query editor | ✅ | ✅ | ✅ |
| F-QUERY | QUERY-projection | Projection editor | ✅ | ✅ | ✅ |
| F-QUERY | QUERY-sort | Sort editor | ✅ | ✅ | ✅ |
| F-AGG | AGG-stage-count | Number of supported pipeline stages | ❓ | ❓ | ✅ |
| F-AGG | AGG-editor-layout | Pipeline editor layout | ✅ | ✅ | ✅ |
| F-AGG | AGG-stage-mgmt | Stage management operations | ✅ | ✅ | ✅ |
| F-SCHEMA | SCHEMA-sampling | Schema sampling configuration | ✅ | ✅ | ✅ |
| F-SCHEMA | SCHEMA-field-prob | Field probability statistics | ✅ | ✅ | ❌ |
| F-SCHEMA | SCHEMA-type-prob | Per-field BSON type probabilities | ✅ | ✅ | ❌ |
| F-IDX | IDX-inventory | Index list / inventory | ✅ | ✅ | ✅ |
| F-IDX | IDX-type-single | Single-field index | ✅ | ✅ | ✅ |
| F-IDX | IDX-type-compound | Compound index | ✅ | ✅ | ✅ |
| F-TRANSFER | TRANSFER-import-csv | CSV import | ✅ | ❌ | ✅ |
| F-TRANSFER | TRANSFER-import-json | JSON import | ✅ | ❌ | ✅ |
| F-TRANSFER | TRANSFER-import-bson | BSON / mongodump import | ✅ | ❌ | ✅ |
| F-SHELL | SHELL-engine | Shell engine and code editor | ✅ | ❌ | ✅ |
| F-SHELL | SHELL-autocomplete | Shell autocomplete | ✅ | ❌ | ✅ |
| F-SHELL | SHELL-validation | Live syntax validation | ✅ | ❌ | ❓ |
| F-AI | AI-nl-query | NL to find() query | 💼 | ❌ | 💼 |
| F-AI | AI-nl-pipeline | NL to aggregation pipeline | 💼 | ❌ | 💼 |
| F-AI | AI-explanation | Plain-English explanation always included | ❓ | ❌ | ✅ |
| F-SQL | SQL-expressions | SQL SELECT/WHERE/GROUP BY/HAVING | 💼 | ❌ | ❌ |
| F-SQL | SQL-join-mapping | SQL JOIN → $lookup mapping | ✅ | ❌ | ❌ |
| F-SQL | SQL-code-gen | SQL query → driver language code gen | ✅ | ❌ | ❌ |
| F-GOV | GOV-readonly-mode | Protect / destructive-write prevention mode | 🧪 | ✅ | ❓ |
| F-GOV | GOV-network-policy | Network access policy | ❓ | ✅ | ❓ |
| F-GOV | GOV-telemetry | Telemetry opt-out/configuration | ❓ | ✅ | ❓ |
| F-SCHED | SCHED-task-types | Task types supported | ✅ | ❌ | 💼 |
| F-SCHED | SCHED-types-time | Preset schedule types | ✅ | ❌ | ✅ |
| F-SCHED | SCHED-cron | Cron expression support | ✅ | ❌ | ✅ |

## Detailed iconized tables

These are icon-only analogs of the detailed comparison tables below. Product columns are iconized; non-product columns are preserved.

### Product-level comparison (feature areas present) — iconized

| Feature area | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| F-CONN — Connectivity | ✅ | ✅ | ✅ |
| F-QUERY — Querying | ✅ | ✅ | ✅ |
| F-AGG — Aggregation | ✅ | ✅ | ✅ |
| F-SCHEMA — Schema | ✅ | ✅ | ✅ |
| F-IDX — Indexing & Performance | ✅ | ✅ | ✅ |
| F-TRANSFER — Data Transfer | ✅ | ❌ | ✅ |
| F-SHELL — Shell | ✅ | ❌ | ✅ |
| F-AI — AI features | ✅ | ❌ | ✅ |
| F-SQL — SQL tools | ✅ | ❌ | ❌ |
| F-GOV — Governance | ✅ | ✅ | ✅ |
| F-SCHED — Task scheduler | ✅ | ❌ | ✅ |

### F-CONN — Connectivity — iconized

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Topology coverage | ✅ | ✅ | ✅ |
| Enterprise auth | 🏢 | ✅ | 🗺️ |
| TLS | ✅ | ✅ | ✅ |
| SSH tunnel | ✅ | ✅ | ✅ |
| Proxy | ✅ | ✅ | ❓ |
| Connection pool params | ✅ | ❓ | ✅ |
| Connection organization | ✅ | ✅ | ✅ |
| In-use encryption (QE/CSFLE) | ❌ | ✅ | ❌ |
| Connection test validation | ❓ | ❓ | ✅ |
| Team sharing | 💼 | ❌ | ❌ |
| Credential storage | ✅ | ✅ | ✅ |
| Unique: Compass | — | ✅ | — |
| Unique: VisuaLeaf | — | — | 🗺️ |
| Unique: Studio 3T | ✅ | — | — |

### F-QUERY — Querying — iconized

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
| Unique: Compass | — | ✅ | — |
| Unique: VisuaLeaf | — | — | 🔌 |
| Unique: Studio 3T | ✅ | — | — |

### F-AGG — Aggregation — iconized

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Stage count / coverage | ✅ | ✅ | ✅ |
| Editor layout | ✅ | ✅ | ✅ |
| Per-stage editing mode | ✅ | ✅ | ✅ |
| Stage toggle (enable/disable) | ✅ | ✅ | ❓ |
| Stage preview | ✅ | ✅ | ✅ |
| Code generation | ✅ | ✅ | ❓ |
| Create MongoDB view | ✅ | ✅ | ❓ |
| Export pipeline results | ✅ | ✅ | ✅ |
| Chart builder from output | ❌ | ❌ | ✅ |
| Pipeline options | ✅ | ✅ | ✅ |
| Switch collection mid-session | ✅ | ❓ | ❓ |
| Date tags in $match | ✅ | ❌ | ❌ |
| Execution timer + cancel | ❓ | ❓ | ✅ |
| Unique: Compass | — | ✅ | — |
| Unique: VisuaLeaf | — | — | ✅ |
| Unique: Studio 3T | ✅ | — | — |

### F-SCHEMA — Schema — iconized

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Field statistics analytics (probability/type/histogram) | ✅ | ✅ | ✅ |
| Geo field analysis | ❌ | ✅ | ❌ |
| JSON schema editor | ❌ | ❌ | ✅ |
| Schema validation deploy | ❌ | ✅ | ✅ |
| Validation strictness (warn/error, strict/moderate) | ❌ | ✅ | ❓ |
| Visual ERD designer | ❌ | ❌ | 💼 |
| View creation from schema tool | ✅ | ❓ | ❓ |
| Schema doc export | ✅ | ✅ | ✅ |
| Explore docs by field presence | ✅ | ❓ | ❓ |
| Rename field across all docs | ✅ | ❓ | ❓ |
| Unique: Compass | — | ✅ | — |
| Unique: VisuaLeaf | — | — | ✅ |
| Unique: Studio 3T | ✅ | — | — |

### F-IDX — Indexing & Performance — iconized

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
| Real-time performance monitoring | ❌ | ✅ | ❓ |
| Kill running operations | ❌ | ✅ | ✅ |
| Unique: Compass | — | ✅ | — |
| Unique: VisuaLeaf | — | — | ✅ |
| Unique: Studio 3T | ✅ | — | — |

### F-TRANSFER — Data Transfer — iconized

| Dimension | Studio 3T | VisuaLeaf |
| --- | --- | --- |
| Import formats | 💼 | ✅ |
| Export formats | 💼 | ✅ |
| Import write modes | ✅ | ✅ |
| Document filter before import | ❌ | ✅ |
| User-defined JS transform per document | ❌ | ✅ |
| Server-side $pipeline pre-export transform | ❌ | ✅ |
| Field mapping and rename | ✅ | ✅ |
| Incremental export with resume points | ✅ | ❌ |
| Data masking | 💼 | ❌ |
| Task save for scheduler | 💼 | 💼 |
| Export source granularity | ✅ | ❓ |

### F-SHELL — Shell — iconized

| Dimension | Studio 3T | VisuaLeaf |
| --- | --- | --- |
| Editor engine | ✅ | ✅ |
| Autocomplete | ✅ | ✅ |
| Live syntax validation | ✅ | ❌ |
| Run all / selection | ✅ | ✅ |
| Run to cursor line | ✅ | ❌ |
| Shell modes | ✅ | ❓ |
| Per-query result tabs (pinnable) | ✅ | ❌ |
| Result views | ✅ | ✅ |
| Multiple concurrent sessions | 🧪 | ✅ |
| Background execution | ❌ | ✅ |
| Auto-reconnect | ❌ | ✅ |
| Persistent session variables | ❌ | ✅ |
| History with search/filter/preview | ✅ | ✅ |
| Open in shell from other tools | ✅ | ❌ |

### F-AI — AI Features — iconized

| Dimension | Studio 3T | VisuaLeaf |
| --- | --- | --- |
| NL → find() query | 💼 | 💼 |
| NL → aggregation pipeline | 💼 | 💼 |
| Plain-English explanation always on | ❓ | ✅ |
| AI providers | ✅ | ❓ |
| Model selection | ✅ | ✅ |
| "Send sample data" privacy toggle | ❓ | ✅ |
| Conversation turns for refinement | ❓ | ✅ |
| Multiple named AI configs | ❓ | ✅ |
| API key storage | ❓ | ✅ |
| Local MCP server | ✅ | ❌ |
| MCP client integrations | ✅ | ❌ |
| Total MCP tools | 🔌 | ❌ |
| stt-cli + PII scanner | ✅ | ❌ |

### F-GOV — Governance — iconized

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Protect / write-prevention mode | 🧪 | ✅ | ❌ |
| Network policy | ❌ | ✅ | ❌ |
| Telemetry configuration | ❌ | ✅ | ❌ |
| Startup / CLI policy (EJSON/YAML) | ❌ | ✅ | ❌ |
| Isolated / air-gapped edition | ❓ | ✅ | ✅ |
| AI controls with human approval gate | ❌ | ✅ | ❌ |
| RBAC user/role management | 🔌 | ❌ | 💼 |
| Visual role inheritance tree | ❌ | ❌ | 💼 |
| Audit log | 🔌 | ❌ | 💼 |
| Collection compare (3-panel diff) | 💼 | ❌ | 💼 |
| Collection sync with direction toggle | 💼 | ❌ | 💼 |
| CDC pipeline (Kafka/Pub/Sub/HTTP) | 🔌 | ❌ | ❌ |
| Kubernetes Helm chart | ✅ | ❌ | ❌ |
| OIDC multi-provider for platform auth | ✅ | ❌ | ❌ |
| Credential protection | ✅ | ✅ | ✅ |

### F-SCHED — Task Scheduler — iconized

| Dimension | Studio 3T | VisuaLeaf |
| --- | --- | --- |
| Task types | ✅ | 💼 |
| Schedule options | ✅ | ✅ |
| Timezone-aware with DST | ❓ | ✅ |
| Execution config | ❓ | ✅ |
| Task status states | ✅ | ✅ |
| Task actions | ✅ | ✅ |
| Email notifications | ✅ | 🔌 |
| Multiple script units per task | ✅ | ❓ |
| Compare/sync task with diff view | ✅ | ❌ |
| Plan limits | 💼 | 💼 |

### Edition / pricing constraints — iconized

| Feature | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Visual Query Builder | ✅ | ❌ | 💼 |
| AI query builder | 💼 | ❌ | 💼 |
| Enterprise auth (Kerberos/LDAP/AWS/OIDC) | 🏢 | ✅ | 🗺️ |
| Shell / IntelliShell | ✅ | ❌ | ✅ |
| Data Transfer | 💼 | ❌ | ✅ |
| Team connection sharing | 💼 | ❌ | ❌ |
| Data masking | 💼 | ❌ | ❌ |
| SQL tools | 💼 | ❌ | ❌ |
| Task scheduler | 💼 | ❌ | 💼 |
| Query Manager (multi-type) | ✅ | ✅ | 💼 |
| Collection compare + sync | 💼 | ❌ | 💼 |
| RBAC dashboard | 🔌 | ❌ | 💼 |
| Audit log | 🔌 | ❌ | 💼 |
| Schema validation UI | ❌ | ✅ | 💼 |
| Visual ERD designer | ❌ | ❌ | 💼 |
| Atlas Search / Vector Search indexes | ❌ | ✅ | ❌ |


## Deep-review coverage reconciliation

| Scope | Result |
| --- | --- |
| Product matrix IDs not present in low-level baseline table (before reconciliation pass) | 52 |
| Product matrix IDs missing from feature dictionary | 0 |
| Comparison-table IDs missing from feature dictionary | 0 |

Detailed additions are captured in the low-level report under **Reconciliation table (product-matrix IDs added by deep review)**.

## Feature-group comparison

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
| Unique: Compass | — | Multiple concurrent connections (1.44.0+); QE/CSFLE in-use encryption; required-access guide | — |
| Unique: VisuaLeaf | — | — | 6-step connection test wizard; URI export; DocumentDB/Cosmos DB roadmap Q2 2026 |
| Unique: Studio 3T | SSH Profiles; 4-mode proxy; read-only UI lock; team sharing; import from Robo 3T/NoSQLBooster/.uri | — | — |

**Assessment:** All three products cover core connectivity (standalone/RS/sharded/SRV, standard auth, TLS, SSH). Compass leads on in-use encryption and enterprise auth completeness. VisuaLeaf offers the best connection-test UX and uniquely plans DocumentDB/Cosmos compatibility. Studio 3T has the most advanced proxy, SSH, team-sharing, and credential-import capabilities.

---

### F-QUERY — Querying

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Filter bar / autocomplete | 5-field bar; full autocomplete incl. BSON wrappers; shorthand ObjectId | ✓ with examples/shortcuts | ACE editor + Ctrl+Space field-name autocomplete from schema |
| Visual Query Builder | All editions — AND/OR/NOR; BSON type auto-detected; Binary/Reference/Regex editors; bidirectional | — | Basic+ — type-aware inputs (date pickers, sliders, booleans), AND/OR nested groups, bidirectional |
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
| Unique: Compass | — | Collation in filter bar; max-time (60,000ms default) | — |
| Unique: VisuaLeaf | — | — | Performance timer; cancel button; Run Find One / Run Count variants; 7 "open in" integrations; undo/redo; batch update from table view; EJSON copy |
| Unique: Studio 3T | Date tags (~20); Query Manager with 4 query types; "open in Aggregation Editor" converts filter → $match+$project | — | — |

**Assessment:** Compass is the only product with collation in the filter bar. VisuaLeaf has the most user-friendly query execution UX (timer, cancel, run-variants, undo/redo). Studio 3T's date tags and Query Manager are unique value adds for power users. VQB is absent in Compass; VisuaLeaf's is plan-gated; Studio 3T's is available on all editions.

---

### F-AGG — Aggregation

| Dimension | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Stage count / coverage | All standard stages | All standard stages | 37+ stages incl. $densify/$fill/$setWindowFields/$search/$documents/$listSearchIndexes |
| Editor layout | 5-region UI: Pipeline panel, Stage editor, Stage I/O, Pipeline output, Query Code + Explain tab | Stage View, Stage Wizard, Focus Mode, Text View | Visual pipeline canvas with stage cards |
| Per-stage editing mode | Code editor only | Stage Wizard + per-stage mode switching | Form Mode (VQB/$group accumulator builder) OR Monaco editor per stage; preference saved |
| Stage toggle (enable/disable) | ✓ confirmed | ✓ confirmed | Unknown/unverified |
| Stage preview | Stage I/O panels per stage | Sampled preview per stage | Input/Output split-view; 20-doc sample; Auto-Preview toggle |
| Code generation | 9 languages; "Open in IntelliShell" button | Major driver languages | Not documented |
| Create MongoDB view | ✓ (requires MongoDB 3.4+) | ✓ | Not documented |
| Export pipeline results | Export Wizard from Pipeline output or Stage I/O | JSON/CSV + Extended JSON | JSON, CSV, BSON, SQL INSERT statements |
| Chart builder from output | — | — | ✓ opens Chart Builder |
| Pipeline options | allowDiskUse, custom collation, index hint | Custom collation + pipeline maxTimeMS | Allow Disk Use, Max Time 300s, Auto Collapse |
| Switch collection mid-session | ✓ | Not documented | Not documented |
| Date tags in $match | ✓ all editions | — | — |
| Execution timer + cancel | Not documented | Not documented | ✓ real-time timer + cancel |
| Unique: Compass | — | Stage Wizard mode (GUI form for stage params) | — |
| Unique: VisuaLeaf | — | — | 37+ stages (widest coverage); Form Mode with VQB for $match + accumulator builder for $group; chart builder from output; execution timer + cancel |
| Unique: Studio 3T | 9-language code gen; date tags in $match; switch collection mid-session; clipboard copy of full pipeline JSON | — | — |

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
| Copy/paste index across connections | ✓ even across different connections | — | — |
| Hide/unhide index | ✓ (MongoDB 4.4+) | ✓ | Unknown/unverified |
| Visual Explain | ✓ plan + execution stats; hover tooltips; JSON fragment view; available in 5 contexts | ✓ plan + execution stats | Exec plan, index usage, docs examined vs returned, index suggestions |
| Profiler | system.profile reader; levels 0/1/2; exact query vs shape grouping; 5 drilldown actions | Not documented in matrix | Slow query threshold; levels 0/1/2; sample rate; P50/P95/P99 percentiles; COLLSCAN flagging; 4 recommendation types; CSV/JSON export |
| Profiler export | — | — | ✓ CSV or JSON |
| Real-time performance monitoring | — | ✓ mongostat/mongotop/currentOp; pause/play | Not documented |
| Kill running operations | — | ✓ (requires killop privilege) | ✓ kill button per operation |
| Unique: Compass | — | Atlas Search + Vector Search index creation; real-time perf monitoring (mongostat/mongotop/currentOp) | — |
| Unique: VisuaLeaf | — | — | P50/P95/P99 profiler percentiles; 4 index recommendation types; profiler export; hashed index; 60+ ICU locale collation; Commit Quorum; clustered index; 4 quick-action templates |
| Unique: Studio 3T | Index copy-paste across connections; geoHaystack (unwarned deprecation); Explain available in 5 contexts incl. SQL Query + IntelliShell | — | — |

**Assessment:** Compass exclusively supports Atlas Search and Vector Search. VisuaLeaf has the most complete index type coverage and the most sophisticated profiler (P50/P95/P99, 4 recommendation types, export). Studio 3T's Explain is available in the widest set of contexts. Note: geoHaystack displayed by Studio 3T without deprecation warning is a confirmed bug.

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
| Data masking | ✓ Pro/Base+: 8 masking types; inline during Import/Export; standalone tool | — |
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
| Live syntax validation | ✓ red gutter markers + right-ruler | — |
| Run all / selection | ✓ F5 (all) / F9 or Ctrl+Enter (selection) | ✓ |
| Run to cursor line | ✓ F6 | — |
| Shell modes | Shell mode (all → Raw tab) vs Query Assist mode (per-query editable result tabs; Visual Explain; destructive op warnings) | Not documented as named modes |
| Per-query result tabs (pinnable) | ✓ pin tab persists across re-runs | — |
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

*MongoDB Compass: N/A — not supported*

| Dimension | Studio 3T | VisuaLeaf |
| --- | --- | --- |
| NL → find() query | ✓ Pro/Base+ | ✓ Professional |
| NL → aggregation pipeline | ✓ Pro/Base+ | ✓ Professional |
| Plain-English explanation always on | Not documented as always-on | ✓ (every query) |
| AI providers | Azure AI, OpenAI GPT-4o, Anthropic Claude Opus 4.1 | OpenAI (confirmed); Anthropic (unverified) |
| Model selection | 3 provider options | 11 OpenAI models user-selectable |
| "Send sample data" privacy toggle | Not documented as user-facing toggle | ✓ ON = Better Accuracy / OFF = More Private |
| Conversation turns for refinement | Not documented | ✓ prior turns used |
| Multiple named AI configs | Not documented | ✓ |
| API key storage | Not documented as AES-masked | AES-masked in Settings; never transmitted to SozoCode |
| Local MCP server | ✓ AI-007: HTTP at 127.0.0.1:27117; 10 tools | — |
| MCP client integrations | ✓ AI-009: VS Code, Cursor, Claude Desktop, others | — |
| Total MCP tools | 10 via local server; 59 via 3T Lens platform | — |
| stt-cli + PII scanner | ✓ AI-010 | — |

**Assessment:** VisuaLeaf's AI focuses on in-product UX (11 model choices, plain-English explanations, privacy toggle, conversation turns). Studio 3T's AI extends outward via MCP — enabling AI agents in external tools (VS Code, Cursor, Claude Desktop) to operate against MongoDB through Studio 3T, which is a fundamentally different capability.

---

### F-SQL — SQL Tools

*MongoDB Compass: N/A — not supported. VisuaLeaf: N/A — not supported.*
*Studio 3T Pro/Base+ only.*

Studio 3T provides the only SQL capability in this comparison: full SELECT/WHERE/JOIN/GROUP BY/ORDER BY/HAVING with JOIN → $lookup translation, 9-language code gen, SQL database migration wizard (MySQL/PostgreSQL/Oracle/SQL Server via JDBC), and SQL export to MySQL/MSSQL/Oracle/PostgreSQL/IBM DB2/Sybase. In-place MongoDB schema migration (reschema) is schedulable via Task Scheduler.

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
| Audit log | ✓ via 3T Lens platform | — | ✓ Professional |
| Collection compare (3-panel diff) | ✓ Pro/Base+ | — | ✓ Professional |
| Collection sync with direction toggle | ✓ Pro/Base+ | — | ✓ Professional |
| CDC pipeline (Kafka/Pub/Sub/HTTP) | ✓ 3TL Bridge | — | — |
| Kubernetes Helm chart | ✓ for platform components | — | — |
| OIDC multi-provider for platform auth | ✓ | — | — |
| Credential protection | Built-in key store OR master password | OS Keytar API | AES-256 local; never transmitted; AI keys AES-masked |

**Assessment:** Compass has the most comprehensive built-in policy enforcement (network policy, startup/CLI policy, AI controls, protect mode, isolated edition). VisuaLeaf has strong RBAC for teams (visual role tree, audit log) without requiring a separate platform. Studio 3T's governance scales via 3T Lens + 3T Access + 3TL Bridge for enterprise CDC, event streaming, and Kubernetes deployments.

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

| Feature | Studio 3T | MongoDB Compass | VisuaLeaf |
| --- | --- | --- | --- |
| Visual Query Builder | All editions (free) | N/A | Basic+ required |
| AI query builder | Pro/Base+ required | N/A | Professional required |
| Enterprise auth (Kerberos/LDAP/AWS/OIDC) | Ultimate edition only | Free (all confirmed) | LDAP/AWS IAM free (others roadmap) |
| Shell / IntelliShell | All editions (free) | N/A | Available (plan details unclear) |
| Data Transfer | Pro/Base+ for task save; formats available all editions | N/A | Community: no automation (0 tasks); Basic: 2 tasks |
| Team connection sharing | Pro/Base+ required | N/A | N/A |
| Data masking | Pro/Base+ required | N/A | N/A |
| SQL tools | Pro/Base+ required | N/A | N/A |
| Task scheduler | Pro/Base+ required | N/A | Community: 0 tasks; Basic: 2; Professional: unlimited |
| Query Manager (multi-type) | All editions (Collection query type free) | No (My Queries only) | Basic+ for saved queries |
| Collection compare + sync | Pro/Base+ required | N/A | Professional required |
| RBAC dashboard | Via 3T Access platform | N/A | Professional required |
| Audit log | Via 3T Lens platform | N/A | Professional required |
| Schema validation UI | N/A (not supported) | Free | Basic+ |
| Visual ERD designer | N/A | N/A | Basic+ required |
| Atlas Search / Vector Search indexes | N/A | Free (requires Atlas M10+ or MongoDB 7.0+ local) | N/A |

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
