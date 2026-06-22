# Feature Matrix — VisuaLeaf / Connectivity

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [→ Querying Matrix](../querying/feature-matrix.md)
- [→ Aggregation Matrix](../aggregation/feature-matrix.md)
- [→ Schema Matrix](../schema/feature-matrix.md)
- [→ Indexing & Performance Matrix](../indexing-performance/feature-matrix.md)
- [→ Data Transfer Matrix](../data-transfer/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Matrix](../ai/feature-matrix.md)
- [→ Governance Matrix](../governance/feature-matrix.md)
- [→ Task Scheduler Matrix](../task-scheduler/feature-matrix.md)

## Source index

- S1: https://visualeaf.com/features/connection-manager/
- S2: https://visualeaf.com/docs/connection-manager

## Capability matrix

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| CONN-org-folders | Connection organization hierarchy | confirmed | Project → Environment → Connection → Ungrouped structure; sidebar views: All Connections, By Project, Ungrouped. Community plan is limited to a maximum of 3 connections. | Community plan: max 3 connections | confirmed | S1 |
| CONN-search-nav | Sidebar search with keyboard navigation | confirmed | Search bar with ↑↓ key navigation across connections. | — | confirmed | S1 |
| CONN-portability | Import/export connections as JSON | confirmed | Export all connection configs as JSON file; passwords excluded from export for security. | — | confirmed | S1 |
| CONN-topology | Supported topologies | confirmed | Standalone: Host, Port, Default DB, Read Preference. Replica Set: RS Name, host:port list, Read From Hidden Nodes toggle, Resolve Cluster Members toggle. Sharded Cluster: mongos host:port list, Read Preference. DNS Seedlist (SRV): connection URI (mongodb+srv://), SRV Service Name override. | — | confirmed | S2 |
| CONN-read-pref | Read preference configuration | confirmed | Read Preference configurable for Standalone and Sharded topologies. Replica Set additionally supports Read From Hidden Nodes toggle. | — | confirmed | S2 |
| CONN-uri-paste | Connection string auto-fill | confirmed | Paste mongodb:// or mongodb+srv:// URI to auto-populate all form fields. | — | confirmed | S2 |
| CONN-uri-export | Export connection to URI | confirmed | Generates connection string URI from form fields. | — | confirmed | S2 |
| CONN-auth-std | Standard authentication mechanisms | confirmed | None (no auth required); SCRAM-SHA-256 (recommended for MongoDB 4.0+, fields: Username, Password, Auth DB); SCRAM-SHA-1 (legacy SCRAM, fields: Username, Password, Auth DB); X.509 (uses SSL client certificate, Auth DB=$external, Username derived from Subject DN). | — | confirmed | S2 |
| CONN-auth-enterprise | Enterprise authentication mechanisms | confirmed/roadmap | LDAP (PLAIN): confirmed; fields: LDAP Username (user@domain.com or CN=… format), Password. AWS IAM: confirmed; fields: Access Key ID, Secret Access Key, Session Token (optional for STS AssumeRole). Kerberos (GSSAPI): roadmap/planned Q2 2026. OIDC: roadmap/planned Q2 2026. | Kerberos and OIDC not yet available | roadmap/planned (Kerberos, OIDC) | S2 |
| CONN-tls | SSL/TLS options | confirmed | Custom Root CA (PEM): user-supplied CA .pem file for custom certificate authority. OS Trust Store: accept OS-trusted certificates via system trust store. Accept Any Certificates: skips validation; for dev/test only. Client Certificate (mTLS): Certificate .pem/.crt + Private Key .pem/.key + optional key passphrase. | — | confirmed | S2 |
| CONN-ssh | SSH tunnel | confirmed | Password auth: SSH Host, SSH Port (default 22), SSH Username, Password. Private Key auth: Private Key file path + optional passphrase. | — | confirmed | S2 |
| CONN-pool-params | Advanced connection parameters | confirmed | Socket Timeout: default 300s; Connect Timeout: default 30s; Server Selection Timeout: default 30s; Max Pool Size: default 100; Min Pool Size: default 0; Max Idle Time: default 10 min; Retry Writes: on by default; Retry Reads: on by default; Compress (zlib): on by default; Load Balanced: off by default; App Name: default "VisuaLeaf" (visible in db.currentOp() and MongoDB profiler); Write Concern W: majority/1/0; Write Concern Timeout: configurable ms; Write Concern Journal: Server Default/true/false. | — | confirmed | S2 |
| CONN-test-steps | Test connection: 6-step validation | confirmed | Steps: 1. Network Connectivity; 2. SSH Tunnel; 3. SSL/TLS Handshake; 4. Authentication; 5. Database Access; 6. Permissions Check. | — | confirmed | S2 |
| CONN-cred-storage | Credential encryption at rest | confirmed | AES-256 encrypted; stored locally only; never transmitted to SozoCode servers; air-gapped compatible. AI API keys (sk-proj-… format) are also AES-masked in Settings UI. | — | confirmed | S2 |
| CONN-compat-docdb | Amazon DocumentDB support | roadmap/planned | Coming Soon; version requirement: DocumentDB 8.0+. | — | roadmap/planned | S1 |
| CONN-compat-cosmos | Azure Cosmos DB support | roadmap/planned | Coming Soon; version requirement: Cosmos DB 4.2+ MongoDB API. | — | roadmap/planned | S1 |
| CONN-compat-redis | Redis support | roadmap/planned | Coming Soon; version requirement: Redis 7.0+. | — | roadmap/planned | S1 |
