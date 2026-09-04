# Product Report — DataGrip

## Navigation

- [Repository README](../../../README.md)
- [Feature dictionary](../../../feature-dictionary.md)
- [Products index](../../README.md)
- [Third-party index](../README.md)
- [High-level comparison](../../../reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](../../../reports/comparisons/low-level-feature-comparison.md)

## Product metadata

- Product name: DataGrip
- Product group: third-party
- Website: https://www.jetbrains.com/datagrip/
- Category: Polyglot (multi-database) SQL/NoSQL IDE, built on the IntelliJ platform
- Analysis date: 2026-09-04
- Version/release context: DataGrip 2025.3–2026.2 line; MongoDB driver 1.21 bundled as of 2026.2

## Product summary

- **Primary use cases:** Unified, code-first IDE for software engineers, DBAs, and data engineers who work across many relational engines (PostgreSQL, MySQL, SQL Server, Oracle, ClickHouse, Snowflake) and treat MongoDB as one additional data source, reached through SQL rather than a document-native workspace.
- **Target users:** Polyglot developers and full-stack engineers already inside the JetBrains IDE ecosystem (IntelliJ IDEA, PyCharm, WebStorm) who want one client for all their databases, trading MongoDB-specific depth for breadth and code intelligence (AST-based refactoring, autocompletion, cross-file reference tracking).
- **Notable strengths:** A native agentic AI chat backed by Anthropic's Claude Agent and OpenAI Codex, driving a 14-tool database-specific MCP server behind a granular 4-category consent gate (Schema Access / Data Access / Schema Modification / Data Modification); a DuckDB-backed cross-database federated JOIN engine (`dg_cross`); Data Source Templates stored as human-readable, Git-committable XML; a free non-commercial license tier (introduced late 2025) and a materially lower-cost individual commercial tier than Studio 3T ($109/yr year 1, down to $65/yr by year 3, vs. Studio 3T Professional's flat $499/yr).
- **Notable constraints:** MongoDB access is explicitly SQL-to-JS translation with **no native document workspace** — there is no MongoDB-native filter bar, tree view, or visual query builder. The SQL engine supports only SELECT-family syntax (WHERE, GROUP BY, HAVING, ORDER BY, LIMIT, OFFSET, single-equality INNER/LEFT JOIN); **INSERT, UPDATE, and DELETE are not supported via SQL** and must be authored in native MongoDB shell syntax or edited cell-by-cell in the data grid. There is **no visual, stage-by-stage aggregation pipeline builder** (multi-stage pipelines are hand-coded as JSON in a text console) and **no code generation to application languages** (Java, Python, C#, Node.js, PHP) comparable to Studio 3T's Aggregations-to-Code. Document schema profiling is limited to basic tabular/tree rendering — no field-probability, type-probability, or histogram analytics.

## Feature inventory

Feature IDs and folder names from [feature-dictionary.md](../../../feature-dictionary.md).

| Feature ID | Feature | Matrix | Report | Status |
| --- | --- | --- | --- | --- |
| F-CONN | Connectivity | [feature-matrix.md](features/connectivity/feature-matrix.md) | [feature-report.md](features/connectivity/feature-report.md) | Completed |
| F-AI | AI Features | [feature-matrix.md](features/ai/feature-matrix.md) | [feature-report.md](features/ai/feature-report.md) | Completed |
| F-SQL | SQL Tools (primary MongoDB query surface) | [feature-matrix.md](features/sql-tools/feature-matrix.md) | [feature-report.md](features/sql-tools/feature-report.md) | Completed |

### Feature areas omitted (no folder created)

Per [feature-dictionary.md](../../../feature-dictionary.md) naming rule #5, a feature area with no real evidence in the source material gets no placeholder folder. The source is `research/google_research/datagrip-competitive-analysis/DataGrip Competitive Analysis Studio 3T.md`.

- **F-QUERY (Querying):** Following the same reasoning already applied to DBeaver (see [DBeaver's product report](../dbeaver/product-report.md)), DataGrip has no MongoDB-native filter-bar/tree-view query surface. Its own source is explicit and even more categorical than DBeaver's: "its architectural implementation relies on translating queries into standard SQL rather than offering a native document workspace." A user writes standard SQL (`SELECT name, email, status FROM users WHERE age > 25...`) and DataGrip transpiles it into MongoDB shell syntax (`db.users.find(...)`) behind the scenes, confirmed by JetBrains' own "SQL for MongoDB" documentation page (Works Cited #22 in the source). This capability is tracked entirely under **F-SQL** instead, exactly as DBeaver's was.
- **F-AGG (Aggregation):** The source states plainly that DataGrip "lacks a visual stage-by-stage pipeline builder. Developers constructing complex multi-stage aggregations ($unwind, $lookup, $facet, $bucket) must manually hand-code JSON documents inside text consoles." This is a confirmed-absent capability (direct statement, not silence), so per this repository's convention it is described here in prose rather than given a matrix with rows of "Not supported."
- **F-SCHEMA (Schema):** The source confirms absence directly: "DataGrip renders documents in standard tabular grids or basic tree views but lacks comprehensive schema structural analysis, field type probability distribution charts, or document structure drift detection." No sampling, field-probability, or type-probability surface exists to build a matrix from.
- **F-IDX (Indexing & Performance):** DataGrip's Explain Plan / diagnostic engine section names PostgreSQL, Redshift, MySQL, MariaDB, Oracle, SQL Server, and Snowflake as supported output formats — MongoDB is never mentioned as a target of this engine, and no MongoDB index-management capability is discussed anywhere in the source. Omitted for lack of evidence, not confirmed absence.
- **F-TRANSFER (Data Transfer):** No MongoDB import/export, migration, or masking capability is discussed for DataGrip in the source.
- **F-SHELL (Shell):** No MongoDB shell / mongosh-equivalent scripting environment is described for DataGrip; its only MongoDB-facing surface is the SQL-to-JS translation console (tracked under F-SQL).
- **F-GOV (Governance & Security):** The one governance-adjacent mechanism the source describes for DataGrip — the 4-category consent/approval gate (Schema Access / Data Access / Schema Modification / Data Modification) that an AI agent's actions must pass through — is a pre-execution safety confirmation specific to the AI agent, not a product-wide RBAC/audit-log/policy surface. Following the same judgment DBeaver's entry applied to its AI "execution safety guards" (mapped to `AI-safety-guards` in F-AI, not to F-GOV), this consent gate is tracked under **F-AI** (see [feature-matrix.md](features/ai/feature-matrix.md)) rather than creating a thin F-GOV folder for a single AI-scoped data point. No RBAC, audit logging, data masking, or platform-governance capability is discussed for DataGrip anywhere in the source.
- **F-SCHED (Task Scheduler):** The source's release-history table lists "added CLI data source management" under DataGrip 2026.2. This is **not** task scheduling: it is command-line creation/editing of connection configurations (a connectivity-management capability), not running, scheduling, or monitoring recurring jobs/scripts — the dictionary's `SCHED-cli-headless` is specifically defined as CLI automation that "can run/trigger scheduled tasks or scripts," which this is not. It also does not cleanly match any existing `CONN-*` sub-feature ID (none describes CLI-driven connection management). Per this plan's instruction to avoid forcing a sub-feature ID onto a capability that doesn't fit one, this is described here in prose only, with no F-SCHED (or F-CONN) matrix row: DataGrip 2026.2 added a command-line interface for creating/editing/listing data source connections outside the GUI, useful for scripted environment setup — unverified in exact scope (source: release-timeline table, no dedicated primary citation for this specific line item).

## Product-level conclusions

### Strategic strengths

- The deepest agentic-AI integration reviewed in this repository to date: native Claude Agent (Claude 4.5 Sonnet via the Anthropic Agent SDK) and OpenAI Codex, driving a purpose-built 14-tool database MCP server, gated by a granular 4-category user-consent model — a materially more structured safety model than a single blanket "AI enabled" toggle.
- `dg_cross`, a DuckDB-backed engine letting one SQL query join tables/collections across multiple, independently-configured data sources (e.g., `$postgresql_production` joined to `$sqlserver_warehouse`) without a pre-flight migration — a real architectural investment, though the source's own technical description names only relational engines (PostgreSQL, MySQL, SQL Server) as example join targets, not MongoDB.
- Materially lower total cost of ownership for individual and JetBrains-ecosystem developers: a free non-commercial tier (since late 2025), a $109→$65/yr commercial tier with a perpetual fallback license, and inclusion in the JetBrains All Products Pack — a fundamentally different pricing posture from Studio 3T's flat $499–$699/yr annual-only model.
- Data Source Templates stored as human-readable XML (`.idea/db-forest-config.xml`) that a team can commit to its existing Git repository, plus JetBrains Account cloud sync of the same templates across a developer's own machines.

### Strategic risks / gaps

- MongoDB support is explicitly SQL-to-JS translation only: no native document workspace, no visual aggregation pipeline builder, no INSERT/UPDATE/DELETE via SQL, no code generation to application languages, and only basic (non-analytical) document schema rendering — a categorically narrower MongoDB surface than Compass, VisuaLeaf, or Studio 3T.
- JOIN support against MongoDB is restricted to a single equality condition in the ON clause; subqueries and USING syntax are unsupported, and SQL aggregate functions cannot be nested or used outside GROUP BY blocks.
- The source is a secondary competitive-intelligence write-up. Several claims (Data Source Template Git-sharing mechanics, cloud-provider auto-discovery scope, `dg_cross`'s applicability to MongoDB specifically, the 2026.2 CLI data-source-management feature) are not tied to a primary source in its own Works Cited list for that specific detail and are labeled Unverified in the feature matrices below rather than Confirmed.

### Open questions

- Whether `dg_cross`'s DuckDB-backed federation engine can actually include a MongoDB collection as a join target — the source's only worked technical example joins two relational engines (PostgreSQL, SQL Server); MongoDB is mentioned only in the source's own forward-looking recommendation for Studio 3T to build an equivalent capability, not confirmed as already working for DataGrip's MongoDB connections today.
- Whether DataGrip's 14-tool MCP server can be reached by external MCP clients (e.g., Claude Desktop, VS Code) the way DBeaver's or Studio 3T's can, or whether it is wired for internal use only by DataGrip's own embedded Claude Agent/Codex chat — the source describes only the internal flow (IDE chat → internal MCP server → JDBC), never an externally-facing client scenario.
- Exact scope and edition requirement of the 2026.2 "CLI data source management" feature.
- Cloud-provider auto-discovery (AWS/Azure/GCP) is described only for relational engines (Amazon RDS, Redshift, Azure SQL, GCP Cloud SQL) in the source — whether it extends to MongoDB Atlas discovery is not stated, and is not tracked here for that reason.
