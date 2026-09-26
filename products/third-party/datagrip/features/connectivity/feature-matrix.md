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
- Analysis date: 2026-09-26
- Review log: 2026-09-25 — weekly re-check (#17): S2 and S3 flagged as emptied in the silo. Both pages render client-side; the silo and a live fetch return only navigation or a cookie banner, which is a capture failure, not evidence of change. The 2026.1 page (S3) still loads its AI/MCP content live. Claims kept. 2026-09-26 — Plan 09 pilot: 12 rows added from the silo's copies of the DataGrip documentation (S5–S11).
- Version/release context: DataGrip 2025.3–2026.2 line

## Source index

- S1: DataGrip Competitive Analysis Studio 3T (secondary research file), `research/google_research/datagrip-competitive-analysis/DataGrip Competitive Analysis Studio 3T.md`
- S2: What's New in DataGrip 2026.2, https://www.jetbrains.com/datagrip/whatsnew/ (S1 Works Cited #5)
- S3: What's New in DataGrip 2026.1, https://www.jetbrains.com/datagrip/whatsnew/2026-1/ (S1 Works Cited #4)
- S4: DataGrip: MongoDB IDE - JetBrains, https://www.jetbrains.com/datagrip/features/mongodb/ (S1 Works Cited #2)
- S5: MongoDB | DataGrip Documentation, https://www.jetbrains.com/help/datagrip/mongodb.html (silo: `data/third-party/datagrip/help_datagrip_mongodb_html.md@55dbb2cb`, captured 2026-09-11)
- S6: Configure SSH and SSL | DataGrip Documentation, https://www.jetbrains.com/help/datagrip/configuring-ssh-and-ssl.html (silo: `data/third-party/datagrip/help_datagrip_configuring-ssh-and-ssl_html.md@55dbb2cb`, captured 2026-09-11)
- S7: Passwords | DataGrip Documentation, https://www.jetbrains.com/help/datagrip/reference-ide-settings-password-safe.html (silo: `data/third-party/datagrip/help_datagrip_reference-ide-settings-password-safe_html.md@55dbb2cb`, captured 2026-09-11)
- S8: HTTP Proxy | DataGrip Documentation, https://www.jetbrains.com/help/datagrip/settings-http-proxy.html (silo: `data/third-party/datagrip/help_datagrip_settings-http-proxy_html.md@55dbb2cb`, captured 2026-09-11)
- S9: Amazon DocumentDB | DataGrip Documentation, https://www.jetbrains.com/help/datagrip/documentdb.html (silo: `data/third-party/datagrip/help_datagrip_documentdb_html.md@55dbb2cb`, captured 2026-09-11)
- S10: Redis | DataGrip Documentation, https://www.jetbrains.com/help/datagrip/redis.html (silo: `data/third-party/datagrip/help_datagrip_redis_html.md@55dbb2cb`, captured 2026-09-11)
- S11: Data Sources and Drivers dialog | DataGrip Documentation, https://www.jetbrains.com/help/datagrip/data-sources-and-drivers-dialog.html (silo: `data/third-party/datagrip/help_datagrip_data-sources-and-drivers-dialog_html.md@55dbb2cb`, captured 2026-09-11)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONN-topology | Topology types | Confirmed (existence of a MongoDB connection type); Unverified (standalone/replica-set/sharded/SRV granularity) | S1's release table states DataGrip 2026.2 "bundled core JDBC drivers (MongoDB 1.21, MSSQL 13.2, MySQL 9.5, PostgreSQL 42.7.3, Redis 1.6)," and DataGrip's own product page (S4) markets it as a "MongoDB IDE." Neither source itemizes standalone/replica-set/sharded/DNS-SRV connection modes. | — | Unverified (granularity) | S1, S2, S4 | Mirrors the DBeaver matrix's approach: a dedicated MongoDB connection/driver is confirmed to exist via a primary source; topology-mode detail is not. |
| CONN-git-repo-sharing | Git-backed connection sharing | Unverified — per secondary source, no primary citation for this specific mechanism | S1: "Connection structures, subfolder groupings, and query files are serialized into readable XML configuration files (such as `.idea/db-forest-config.xml`). This enables teams to commit query libraries, database folder layouts, and dialect settings directly to Git repositories, establishing continuous integration for database scripts." | Not MongoDB-specific — applies to DataGrip's project-level connection/query-file storage generally. | Unverified | S1 | Imperfect-fit mapping, flagged explicitly (same practice as DBeaver's `GOV-collection-compare` row): the dictionary's `CONN-git-repo-sharing` description is "a local folder of connection files optionally backed by a Git working tree, with in-app push/pull/fetch/reset actions." DataGrip's mechanism is plain, human-readable XML project files that a team's *own* Git tooling can pick up — the source does not describe any in-app git panel or push/pull/fetch/reset actions inside DataGrip itself. Closest existing ID chosen over minting a new one for a single data point. |
| CONN-portability | Import/export configs | Unverified — per secondary source, no primary citation | S1: "DataGrip allows development teams to store Data Source Templates within their JetBrains Accounts... When an engineer logs into any JetBrains IDE on a new machine, these database templates synchronize automatically." | Requires a JetBrains Account; this is automatic cloud sync of templates (stripped of credentials) rather than a manual file export/import action. | Unverified | S1 | Distinct mechanism from the Git-file capability above — automatic per-user cloud sync vs. a version-controllable file on disk — both use the closest-available existing ID rather than a new one. |
| CONN-test-steps | Connection test | Confirmed (a single connection test); Unverified (step-by-step diagnosis) | S5: "To do this, click the Test Connection link at the bottom of the connection details section." Checked https://www.jetbrains.com/help/datagrip/mongodb.html on 2026-09-26 (silo copy of 2026-09-11); no step-by-step breakdown (network, SSH, TLS, auth, permissions) documented. | — | — | S5 | Plan 09 pilot (silo candidate). The dictionary asks for step-by-step validation; only a one-shot test is documented, which is silence on the steps, not absence. |
| CONN-auth-std | Standard auth | Confirmed | S5 lists, for MongoDB: "SCRAM-SHA-256: authenticate using User, Password, Authentication database ...", "x.509: use x.509 certificate for authentication." and "No auth: authentication is not required." | — | — | S5 | Plan 09 pilot. S5 also lists SCRAM-SHA-1, but its two SCRAM descriptions name each other's hash function ("SCRAM-SHA-1: authenticate using User, Password, Authentication database and the SHA-256 hashing function"), which looks like a documentation slip. |
| CONN-auth-enterprise | Enterprise auth | Confirmed (AWS IAM, Kerberos, LDAP); Unverified (MongoDB OIDC) | S5 lists, for MongoDB: "AWS IAM: authenticate using AWS access key id, AWS secret access key, and AWS session token", "GSSAPI (Kerberos): use Kerberos for authentication" and "Plain (LDAP): authenticate by proxying the authentication request to a Lightweight Directory Access Protocol (LDAP) service". Checked https://www.jetbrains.com/help/datagrip/mongodb.html on 2026-09-26 (silo copy of 2026-09-11); no documentation of MongoDB OIDC found. | — | — | S5 | Plan 09 pilot. One of the dictionary's four mechanisms (OIDC) is not documented; that is silence, not absence. |
| CONN-ssh | SSH tunnel | Confirmed | S6: "Password: Access the host with a password." and "Key pair (OpenSSH or PuTTY): Use SSH authentication with a key pair." | Data-source setting that applies to all DataGrip data sources; the page does not name MongoDB. | — | S6 | Plan 09 pilot. S6 also documents an "OpenSSH config and authentication agent" option. |
| CONN-tls | TLS/SSL config | Confirmed | S6: "Click the SSH/SSL tab and select the Use SSL checkbox.", "In the CA file field, navigate to the CA certificate file", "In the Client certificate file field, navigate to the client certificate file", and for Full Verification: "Verifies the server host to ensure that it matches the name stored in the server certificate." | Data-source setting that applies to all DataGrip data sources; the page does not name MongoDB. SNI is not mentioned. | — | S6 | Plan 09 pilot. |
| CONN-cred-storage | Credential storage | Confirmed | S7: "DataGrip does not have its own password store. It uses either the native password management system or KeePass." | IDE-wide setting. S5: "For the URL only connection type, the JDBC URL is stored in plain text as is". | — | S7, S5 | Plan 09 pilot. |
| CONN-proxy | Proxy | Partial | S8: "Use this page to customize settings of an HTTP or SOCKS proxy server for DataGrip." For database connections: "For those connections, proxy needs to be specified on the Advanced tab of the dialog according to the driver's manual." | The IDE proxy covers IDE traffic (drivers, plugins, licensing), not database connections; a database proxy is a driver property. | — | S8 | Plan 09 pilot. Partial: no first-class HTTP/SOCKS proxy mode for database connections is documented. |
| CONN-uri-paste | URI auto-fill | Confirmed | S5: "Alternatively, paste the JDBC URL in the URL field." and "For the other connection types, the JDBC URL is broken down into connection details." | For the "URL only" connection type the URL is used as is and stored in plain text (S5). | — | S5 | Plan 09 pilot. |
| CONN-read-pref | Read preference | Confirmed | S5's MongoDB connection options table lists Read preference: "To enable the option, select it from the More Options list on the top right side of the settings area. Refer to the official MongoDB documentation on read preferences" | Enabled from the More Options list of the MongoDB connection settings (S5). Tag sets are not described. | — | S5 | Plan 09 pilot. |
| CONN-compat-docdb | Amazon DocumentDB | Confirmed | S9 describes creating a data source "to your Amazon DocumentDB database in DataGrip, and run a test connection" | — | — | S9 | Plan 09 pilot. |
| CONN-compat-redis | Redis | Confirmed | S10: "Supported DBMS versions: 5-8." and "For Redis, data editing is currently not supported." | Read-only data access for Redis (S10). | — | S10 | Plan 09 pilot. |
| CONN-readonly-lock | Read-only lock | Partial | S11, Read-only option: "Select the checkbox to protect the data source from accidental data modifications." and "Data modifications might be possible in the query console if the driver does not support the read-only status." | Data-source setting for all data sources; S11 does not say whether the MongoDB driver supports the read-only status. | — | S11 | Plan 09 pilot. Partial: the lock is guaranteed only in the data editor. |

## Feature-level conclusion

### Confirmed strengths

- A dedicated MongoDB connection type / bundled JDBC driver (version 1.21 as of 2026.2) is confirmed to exist via DataGrip's own product marketing page and release notes — the baseline claim that MongoDB connectivity exists at all is solidly evidenced.
- Connection and query-file configuration is stored as plain, readable XML in project directories rather than an opaque binary store, which is a genuinely portable and Git-friendly design choice even though DataGrip's own in-app Git integration for this specific artifact type is not described in the source.

### Confirmed limitations

- SSH, TLS, proxy, credential storage and the read-only lock are documented as generic data-source or IDE settings (S6, S7, S8, S11). Authentication, URL paste, read preference and the connection test are documented on the MongoDB connection page (S5).
- A database proxy is a driver property, not a first-class proxy mode (S8), and the read-only lock holds only in the data editor unless the driver supports it (S11).

### Open questions / unknowns

- Whether MongoDB OIDC is supported (not listed in S5), whether connection pooling is configurable (not described), and whether the MongoDB driver honours the data source's read-only status. S5 confirms an SRV ("MongoDB Atlas (SRV protocol)") connection type and a Replica set option; the CONN-topology row has not been re-checked against it yet.
- Whether the generic SSH/SSL tab (S6) behaves the same for MongoDB data sources; no MongoDB-specific statement was found.
- Whether cloud-provider auto-discovery (AWS/Azure/GCP, described in the source only for relational engines like Amazon RDS, Redshift, Azure SQL, and GCP Cloud SQL) extends to discovering MongoDB Atlas clusters — not stated, and therefore not tracked as a sub-feature row here.
