# Feature Report — DataGrip / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Connectivity
- Feature ID: F-CONN (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: DataGrip
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

DataGrip's MongoDB connectivity is one instance of its generic, engine-agnostic Data Source and Drivers architecture, shared with every relational engine it supports (PostgreSQL, MySQL, SQL Server, Oracle, ClickHouse, Snowflake, and others). A bundled MongoDB JDBC driver (version 1.21 as of the 2026.2 release) provides the underlying connection, and DataGrip markets MongoDB support directly on its own product pages — confirming the connection type exists, even though the source material never itemizes MongoDB-specific topology modes (standalone/replica set/sharded/SRV) or authentication mechanisms the way it does for some relational engines.

What is distinctive about DataGrip's connectivity model — described generically, not as a MongoDB-specific capability — is how connection and query configuration is stored and shared. Rather than an opaque binary connection store, DataGrip serializes connection structures, folder groupings, and query files into human-readable XML project files (for example, `.idea/db-forest-config.xml`). Because these are plain text files inside a project directory, a team can commit them to its own Git repository using its existing Git workflow — DataGrip does not appear (per the source) to provide a dedicated in-app Git panel with push/pull/fetch/reset actions for this specific artifact, unlike Studio 3T's dedicated git-backed connection-sharing feature. Separately, DataGrip also offers automatic cloud sync of Data Source Templates through a developer's own JetBrains Account: templates (with personal credentials stripped out) follow the developer automatically to any machine where they sign into a JetBrains IDE.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| CONN-topology | MongoDB connection type/driver existence is confirmed via a primary source (DataGrip's own "MongoDB IDE" product page); topology-mode granularity is not itemized. | Establishes the floor of DataGrip's MongoDB connectivity claim without overstating its depth. | JetBrains "DataGrip: MongoDB IDE" product page (S1 Works Cited #2); "What's New in DataGrip 2026.2" (S1 Works Cited #5) |
| CONN-git-repo-sharing | Closest existing ID for DataGrip's Git-committable XML connection/query files, but an imperfect fit — no in-app Git actions are described. | Prevents overstating DataGrip's Git integration as equivalent to Studio 3T's dedicated push/pull/fetch/reset connection-sharing UI. | Research file narrative |
| CONN-portability | JetBrains Account cloud sync of Data Source Templates across a developer's own machines, credentials stripped. | A convenience feature for individual developers working across multiple machines, distinct from team-level connection sharing. | Research file narrative |

## Constraints and risks

- Every connectivity claim traced in this matrix describes DataGrip's general, engine-agnostic architecture rather than a MongoDB-specific mechanism — treat any inference that these behaviors are MongoDB-tuned as unverified.
- No primary source in the research file's own Works Cited list documents the Git-file-sharing or JetBrains Account template-sync mechanisms in detail; both remain Unverified despite reading as confident claims in the source narrative.

## Interactions and dependencies

- The MongoDB connection established here is the foundation for [F-SQL](../sql-tools/feature-report.md)'s SQL-to-JS translation engine — DataGrip has no separate MongoDB-native query surface.
- AI agent tool calls (see [F-AI](../ai/feature-report.md)) operate against the same underlying JDBC connection via DataGrip's internal MCP server.

## Conclusions

### Strengths

- Confirmed, vendor-marketed MongoDB connection type with a bundled, versioned JDBC driver.
- Human-readable, Git-committable XML connection/query-file storage — a materially different (and arguably more transparent) design than an opaque binary connection store.

### Limitations

- No MongoDB-specific detail on authentication, TLS, SSH tunneling, or topology modes anywhere in the source.
- No in-app Git panel or push/pull/fetch/reset UI is described for the XML connection files, unlike Studio 3T's dedicated git-backed connection-sharing feature.

### Unknowns

- Whether cloud-provider auto-discovery (confirmed only for relational engines: Amazon RDS, Redshift, Azure SQL, GCP Cloud SQL) extends to MongoDB Atlas.
- Full MongoDB authentication-mechanism and topology-mode support list.
