# VisuaLeaf — Connectivity Feature Matrix

| ID | Capability | Status | Detail | Source |
|---|---|---|---|---|
| CONN-001 | Connection organization hierarchy | **confirmed** | Project → Environment → Connection → Ungrouped; sidebar views: All Connections, By Project, Ungrouped | https://visualeaf.com/features/connection-manager/ |
| CONN-002 | Sidebar search with keyboard navigation | **confirmed** | Search bar with ↑↓ key navigation across connections | https://visualeaf.com/features/connection-manager/ |
| CONN-003 | Import/export connections as JSON | **confirmed** | Passwords excluded from export for security | https://visualeaf.com/features/connection-manager/ |
| CONN-004 | Topology: Standalone | **confirmed** | Fields: Host, Port, Default DB, Read Preference | https://visualeaf.com/docs/connection-manager |
| CONN-005 | Topology: Replica Set | **confirmed** | Fields: RS Name, host:port list, Read From Hidden Nodes toggle, Resolve Cluster Members toggle | https://visualeaf.com/docs/connection-manager |
| CONN-006 | Topology: Sharded Cluster | **confirmed** | Fields: mongos host:port list, Read Preference | https://visualeaf.com/docs/connection-manager |
| CONN-007 | Topology: DNS Seedlist (SRV) | **confirmed** | Fields: connection URI (mongodb+srv://), SRV Service Name override | https://visualeaf.com/docs/connection-manager |
| CONN-008 | Connection string auto-fill | **confirmed** | Paste mongodb:// or mongodb+srv:// URI to auto-populate all form fields | https://visualeaf.com/docs/connection-manager |
| CONN-009 | Export connection to URL | **confirmed** | Generates connection string URI from form fields | https://visualeaf.com/docs/connection-manager |
| CONN-010 | Auth: None | **confirmed** | No authentication required | https://visualeaf.com/docs/connection-manager |
| CONN-011 | Auth: SCRAM-SHA-256 | **confirmed** | Recommended for MongoDB 4.0+; fields: Username, Password, Auth DB | https://visualeaf.com/docs/connection-manager |
| CONN-012 | Auth: SCRAM-SHA-1 | **confirmed** | Legacy SCRAM; fields: Username, Password, Auth DB | https://visualeaf.com/docs/connection-manager |
| CONN-013 | Auth: X.509 | **confirmed** | Uses SSL client certificate; Auth DB = $external; Username derived from Subject DN | https://visualeaf.com/docs/connection-manager |
| CONN-014 | Auth: Kerberos (GSSAPI) | **roadmap/planned** | Planned for Q2 2026; not currently available | https://visualeaf.com/docs/connection-manager |
| CONN-015 | Auth: LDAP (PLAIN) | **confirmed** | Fields: LDAP Username (user@domain.com or CN=… format), Password | https://visualeaf.com/docs/connection-manager |
| CONN-016 | Auth: AWS IAM | **confirmed** | Fields: Access Key ID, Secret Access Key, Session Token (optional for STS AssumeRole) | https://visualeaf.com/docs/connection-manager |
| CONN-017 | Auth: OIDC | **roadmap/planned** | Planned for Q2 2026; not currently available | https://visualeaf.com/docs/connection-manager |
| CONN-018 | SSL/TLS: Custom Root CA (PEM) | **confirmed** | User-supplied CA .pem file; custom certificate authority | https://visualeaf.com/docs/connection-manager |
| CONN-019 | SSL/TLS: OS Trust Store | **confirmed** | Accept OS-trusted certificates via system trust store | https://visualeaf.com/docs/connection-manager |
| CONN-020 | SSL/TLS: Accept any certificates | **confirmed** | Skips validation; for dev/test environments only | https://visualeaf.com/docs/connection-manager |
| CONN-021 | SSL/TLS: Client Certificate (mTLS) | **confirmed** | Certificate: .pem/.crt; Private Key: .pem/.key; optional key passphrase | https://visualeaf.com/docs/connection-manager |
| CONN-022 | SSH Tunnel: Password auth | **confirmed** | Fields: SSH Host, SSH Port (default 22), SSH Username, Password | https://visualeaf.com/docs/connection-manager |
| CONN-023 | SSH Tunnel: Private Key auth | **confirmed** | Private Key file path + optional passphrase | https://visualeaf.com/docs/connection-manager |
| CONN-024 | Advanced: Socket Timeout | **confirmed** | Default 300 seconds; configurable | https://visualeaf.com/docs/connection-manager |
| CONN-025 | Advanced: Connect Timeout | **confirmed** | Default 30 seconds; configurable | https://visualeaf.com/docs/connection-manager |
| CONN-026 | Advanced: Server Selection Timeout | **confirmed** | Default 30 seconds; configurable | https://visualeaf.com/docs/connection-manager |
| CONN-027 | Advanced: Max Pool Size | **confirmed** | Default 100; maximum connection pool size | https://visualeaf.com/docs/connection-manager |
| CONN-028 | Advanced: Min Pool Size | **confirmed** | Default 0; minimum connection pool size | https://visualeaf.com/docs/connection-manager |
| CONN-029 | Advanced: Max Idle Time | **confirmed** | Default 10 minutes; max time a connection can remain idle | https://visualeaf.com/docs/connection-manager |
| CONN-030 | Advanced: Retry Writes | **confirmed** | Enabled by default; retries failed write operations | https://visualeaf.com/docs/connection-manager |
| CONN-031 | Advanced: Retry Reads | **confirmed** | Enabled by default; retries failed read operations | https://visualeaf.com/docs/connection-manager |
| CONN-032 | Advanced: Compress (zlib) | **confirmed** | zlib compression enabled by default | https://visualeaf.com/docs/connection-manager |
| CONN-033 | Advanced: Load Balanced | **confirmed** | Disabled by default; for load balancer topologies | https://visualeaf.com/docs/connection-manager |
| CONN-034 | Advanced: App Name | **confirmed** | Default "VisuaLeaf"; visible in db.currentOp() and MongoDB profiler | https://visualeaf.com/docs/connection-manager |
| CONN-035 | Advanced: Write Concern — W | **confirmed** | Options: majority / 1 / 0 | https://visualeaf.com/docs/connection-manager |
| CONN-036 | Advanced: Write Concern — Timeout (ms) | **confirmed** | Configurable timeout in milliseconds | https://visualeaf.com/docs/connection-manager |
| CONN-037 | Advanced: Write Concern — Journal | **confirmed** | Options: Server Default / true / false | https://visualeaf.com/docs/connection-manager |
| CONN-038 | Test Connection: 6-step validation | **confirmed** | Steps: 1. Network Connectivity, 2. SSH Tunnel, 3. SSL/TLS Handshake, 4. Authentication, 5. Database Access, 6. Permissions Check | https://visualeaf.com/docs/connection-manager |
| CONN-039 | Credential encryption at rest | **confirmed** | AES-256 encrypted; stored locally only; never transmitted to SozoCode servers; air-gapped compatible | https://visualeaf.com/docs/connection-manager |
| CONN-040 | Community plan connection limit | **confirmed** | Maximum 3 connections on Community (free) tier | https://visualeaf.com/features/connection-manager/ |
| CONN-041 | Amazon DocumentDB 8.0+ support | **roadmap/planned** | Coming Soon; version requirement: DocumentDB 8.0+ | https://visualeaf.com/features/connection-manager/ |
| CONN-042 | Azure Cosmos DB (MongoDB API) support | **roadmap/planned** | Coming Soon; version requirement: Cosmos DB 4.2+ MongoDB API | https://visualeaf.com/features/connection-manager/ |
| CONN-043 | Redis 7.0+ support | **roadmap/planned** | Coming Soon; version requirement: Redis 7.0+ | https://visualeaf.com/features/connection-manager/ |

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [→ Querying Matrix](../querying/feature-matrix.md)
- [→ Aggregation Matrix](../aggregation/feature-matrix.md)
- [→ Schema Validation Matrix](../schema-validation/feature-matrix.md)
- [→ Indexing & Performance Matrix](../indexing-performance/feature-matrix.md)
- [→ Data Import/Export Matrix](../data-import-export/feature-matrix.md)
- [→ Visual Schema Matrix](../visual-schema/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Assistant Matrix](../ai-assistant/feature-matrix.md)
- [→ Security & Governance Matrix](../security-governance/feature-matrix.md)
