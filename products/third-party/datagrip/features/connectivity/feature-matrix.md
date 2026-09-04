# Feature Matrix — DataGrip / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: DataGrip
- Product group: third-party
- Feature ID: F-CONN (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `connectivity`
- Analysis date: 2026-09-04
- Version/release context: DataGrip 2025.3–2026.2 line

## Source index

- S1: DataGrip Competitive Analysis Studio 3T (secondary research file), `research/google_research/datagrip-competitive-analysis/DataGrip Competitive Analysis Studio 3T.md`
- S2: What's New in DataGrip 2026.2, https://www.jetbrains.com/datagrip/whatsnew/ (S1 Works Cited #5)
- S3: What's New in DataGrip 2026.1, https://www.jetbrains.com/datagrip/whatsnew/2026-1/ (S1 Works Cited #4)
- S4: DataGrip: MongoDB IDE - JetBrains, https://www.jetbrains.com/datagrip/features/mongodb/ (S1 Works Cited #2)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONN-topology | Topology types | Confirmed (existence of a MongoDB connection type); Unverified (standalone/replica-set/sharded/SRV granularity) | S1's release table states DataGrip 2026.2 "bundled core JDBC drivers (MongoDB 1.21, MSSQL 13.2, MySQL 9.5, PostgreSQL 42.7.3, Redis 1.6)," and DataGrip's own product page (S4) markets it as a "MongoDB IDE." Neither source itemizes standalone/replica-set/sharded/DNS-SRV connection modes. | — | Unverified (granularity) | S1, S2, S4 | Mirrors the DBeaver matrix's approach: a dedicated MongoDB connection/driver is confirmed to exist via a primary source; topology-mode detail is not. |
| CONN-git-repo-sharing | Git-backed connection sharing | Unverified — per secondary source, no primary citation for this specific mechanism | S1: "Connection structures, subfolder groupings, and query files are serialized into readable XML configuration files (such as `.idea/db-forest-config.xml`). This enables teams to commit query libraries, database folder layouts, and dialect settings directly to Git repositories, establishing continuous integration for database scripts." | Not MongoDB-specific — applies to DataGrip's project-level connection/query-file storage generally. | Unverified | S1 | Imperfect-fit mapping, flagged explicitly (same practice as DBeaver's `GOV-collection-compare` row): the dictionary's `CONN-git-repo-sharing` description is "a local folder of connection files optionally backed by a Git working tree, with in-app push/pull/fetch/reset actions." DataGrip's mechanism is plain, human-readable XML project files that a team's *own* Git tooling can pick up — the source does not describe any in-app git panel or push/pull/fetch/reset actions inside DataGrip itself. Closest existing ID chosen over minting a new one for a single data point. |
| CONN-portability | Import/export configs | Unverified — per secondary source, no primary citation | S1: "DataGrip allows development teams to store Data Source Templates within their JetBrains Accounts... When an engineer logs into any JetBrains IDE on a new machine, these database templates synchronize automatically." | Requires a JetBrains Account; this is automatic cloud sync of templates (stripped of credentials) rather than a manual file export/import action. | Unverified | S1 | Distinct mechanism from the Git-file capability above — automatic per-user cloud sync vs. a version-controllable file on disk — both use the closest-available existing ID rather than a new one. |

## Feature-level conclusion

### Confirmed strengths

- A dedicated MongoDB connection type / bundled JDBC driver (version 1.21 as of 2026.2) is confirmed to exist via DataGrip's own product marketing page and release notes — the baseline claim that MongoDB connectivity exists at all is solidly evidenced.
- Connection and query-file configuration is stored as plain, readable XML in project directories rather than an opaque binary store, which is a genuinely portable and Git-friendly design choice even though DataGrip's own in-app Git integration for this specific artifact type is not described in the source.

### Confirmed limitations

- None of DataGrip's connectivity claims in this matrix are MongoDB-specific in the source; all evidence describes general, engine-agnostic DataGrip connectivity architecture that happens to also apply to its MongoDB connections.
- No MongoDB-specific detail on authentication mechanisms, TLS/SSL configuration, SSH tunneling, or connection pooling is present in the source — these sub-features are omitted from this matrix entirely rather than marked absent, since the source is silent rather than explicit about them.

### Open questions / unknowns

- Full list of MongoDB authentication mechanisms (SCRAM variants, X.509) and topology modes (standalone/replica set/sharded/SRV) supported by DataGrip's bundled MongoDB driver.
- Whether SSH tunneling or a proxy mode is available for MongoDB connections specifically (not discussed in the source in either direction).
- Whether cloud-provider auto-discovery (AWS/Azure/GCP, described in the source only for relational engines like Amazon RDS, Redshift, Azure SQL, and GCP Cloud SQL) extends to discovering MongoDB Atlas clusters — not stated, and therefore not tracked as a sub-feature row here.
