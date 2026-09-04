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
- **Description:** Desktop IDE for MongoDB covering all 11 feature areas: 6-dialect SQL migration & querying toolchain (MySQL, MSSQL, Oracle, PostgreSQL, Sybase, IBM DB2), data masking with 19 field-level operation types across 6 BSON categories, Visual Query Builder with one-way handoff to Aggregation Editor, IntelliShell with Query Assist, 13 task scheduler execution types, cross-connection index copy/paste, built-in Local MCP Server (HTTP port 27117), and opt-in AI Helper. Anchors the broader 3T platform across Build, Pipeline, and Governed Access tracks.
- **Website:** https://studio3t.com/

### 3T Explore
- **Type:** Internal (3t)
- **Description:** The browser-based IDE product in the "Build" track (alongside the Studio 3T Desktop IDE and 3T MCP). Bundles Explore (view/query/edit collection data in browser), Visual Query Builder, IntelliShell, Aggregation Editor, AI Helper, Workspace Switcher, and Access Control integration with 3T Access Manager.
- **Website:** https://studio3t.com/3t-explore/

### 3T MCP
- **Type:** Internal (3t)
- **Description:** Standalone CLI binary (`stt-cli`) in the "Build" track exposing read-only MongoDB access and built-in PII scanning to external AI coding agents via the Model Context Protocol (MCP) over stdio transport.
- **Website:** https://studio3t.com/3t-mcp/

### 3T Lens
- **Type:** Internal (3t)
- **Description:** Browser-based governed data workspace in the "Governed Access" track providing centralized MongoDB connection management, compliance policy templates, PII classification, versioned field history, and 59 MCP tools governed by 3T Access role policies.
- **Website:** https://studio3t.com/3t-lens/

### 3T Access
- **Type:** Internal (3t)
- **Description:** Identity and governance plane in the "Governed Access" track shared across all 3T products, providing centralized identity/role/permission management and a full audit trail for both human users and AI agent access.
- **Website:** unknown/unverified — described within the 3T Lens product page; no independently confirmed dedicated page.

### 3TL Bridge
- **Type:** Internal (3t)
- **Description:** Real-time Change Data Capture (CDC) pipeline engine in the "Pipeline" track (MongoDB ↔ Kafka / Google Pub-Sub / HTTP), featuring an in-flight Transform Studio, pipeline-layer PII masking, and Kubernetes/Docker Compose deployment options.
- **Website:** https://studio3t.com/3tl-bridge/

### MongoDB Compass
- **Type:** Third-party
- **Description:** Official free/open-source GUI for MongoDB by MongoDB Inc. Exclusively provides Queryable Encryption (QE) and CSFLE in-use encryption configuration, real-time live server monitoring (mongostat/mongotop/currentOp), Atlas Search & Vector Search index management, geo schema analysis, enterprise policy enforcement, and human-gated AI natural language query generation.
- **Website:** https://www.mongodb.com/products/tools/compass

### VisuaLeaf
- **Type:** Third-party
- **Description:** Subscription polyglot GUI by SozoCode featuring a visual ERD designer with graph-theory relationship detection, standalone JSON Schema tree editor, 6-step connection test wizard, GridFS file viewer, split-panel workspace layouts, and MongoSync guided cross-server copy. Connects to MongoDB, DocumentDB, Cosmos DB, and relational engines (PostgreSQL/MySQL/SQL Server/Oracle/etc.).
- **Website:** https://visualeaf.com/
