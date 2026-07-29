# Products Directory

## Navigation

- [Repository README](../README.md)
- [Third-party products](third-party/README.md)
- [3t products](3t/README.md)
- [High-level comparison](../reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](../reports/comparisons/low-level-feature-comparison.md)

Products are split into two groups:

- `third-party/` for external products
- `3t/` for internal 3t products

Each product follows the same hierarchy:

1. `product-report.md`
2. `features/<feature-name>/feature-matrix.md`
3. `features/<feature-name>/feature-report.md`

## Reviewed products

### Studio 3T
- **Type:** Internal (3t)
- **Description:** A MongoDB IDE focused on advanced querying, aggregation, schema exploration, import/export, SQL tools, and automation workflows. Anchors a broader 3T platform organized into three tracks: Build, Pipeline, and Governed Access — see the five products below for the other members of that platform.
- **Website:** https://studio3t.com/

### 3T Explore
- **Type:** Internal (3t)
- **Description:** The browser-based IDE product in the "Build" track (alongside the Studio 3T Desktop IDE and 3T MCP). Bundles Explore (view/query/edit collection data in browser), Visual Query Builder, IntelliShell, Aggregation Editor, an AI Helper, a Workspace Switcher, and Access Control integration with 3T Access Manager.
- **Website:** https://studio3t.com/3t-explore/

### 3T MCP
- **Type:** Internal (3t)
- **Description:** A standalone CLI binary (`stt-cli`) exposing read-only MongoDB access to AI coding agents via the Model Context Protocol over stdio transport — distinct from the Desktop IDE's built-in Local MCP Server (HTTP transport). Part of the "Build" track.
- **Website:** https://studio3t.com/3t-mcp/

### 3T Lens
- **Type:** Internal (3t)
- **Description:** A browser-based governed data workspace: centralized MongoDB connection management, compliance policy templates, PII classification, versioned field history, and MCP tool access governed by 3T Access role policies. Part of the "Governed Access" track.
- **Website:** https://studio3t.com/3t-lens/

### 3T Access
- **Type:** Internal (3t)
- **Description:** The identity and governance plane shared across all 3T products — centralized user/role/permission management and a full audit trail for both human and AI agent access. Part of the "Governed Access" track.
- **Website:** unknown/unverified — described within the 3T Lens product page; no independently confirmed dedicated page.

### 3TL Bridge
- **Type:** Internal (3t)
- **Description:** A real-time Change Data Capture (CDC) pipeline engine (MongoDB/Kafka/Google Pub/Sub/HTTP), with an in-flight Transform Studio, pipeline-layer PII masking, and Kubernetes/Docker Compose deployment. The sole product in the "Pipeline" track.
- **Website:** https://studio3t.com/3tl-bridge/

### MongoDB Compass
- **Type:** Third-party
- **Description:** The official GUI for MongoDB, used for basic querying, schema insights, index analysis, and aggregation workflows.
- **Website:** https://www.mongodb.com/products/tools/compass

### VisuaLeaf
- **Type:** Third-party
- **Description:** A polyglot database GUI aimed at visual data work, query building, and day-to-day database operations. Natively supports MongoDB, Azure Cosmos DB, and Amazon DocumentDB, as well as PostgreSQL, MySQL, MariaDB, Microsoft SQL Server, SQLite, Oracle, CockroachDB, ClickHouse, DuckDB, and TiDB — this repository analyzes its MongoDB-facing capabilities only.
- **Website:** https://visualeaf.com/
