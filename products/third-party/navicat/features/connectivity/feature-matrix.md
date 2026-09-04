# Feature Matrix — Navicat / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: Navicat
- Product group: third-party
- Feature ID: F-CONN (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `connectivity`
- Analysis date: 2026-09-04
- Version/release context: Navicat 17 line

## Source index

- S1: Navicat Competitive Intelligence Analysis (secondary research file), `research/google_research/navicat-competitive-intelligence-analysis/Navicat Competitive Intelligence Analysis.md`
- S2: Navicat Online Manual, https://www.navicat.com/manual/online_manual/en/navicat_17/win_manual/ (S1 Works Cited #5 — general manual index, not a specific dated section)
- S3: MongoDB Database Administration and Development Tool - Navicat, https://www.navicat.com/en/products/navicat-for-mongodb (S1 Works Cited #7)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONN-topology | Topology types | Unverified | S1 lists MongoDB Atlas among supported cloud-managed targets and describes "concurrent connections to heterogeneous relational, document, and key-value database engines," but does not itemize standalone/replica-set/sharded/SRV topology support for MongoDB specifically. | — | Unverified | S1 | Existence of MongoDB connectivity is Confirmed; topology-type granularity is not discussed. |
| CONN-uri-export | URI export | Confirmed | S1 (Release History): "Navicat 17... URI connection management" and (Security section): "Connection configurations can be represented using standard Navicat URIs for centralized deployment management." | — | Unverified (whether URI paste/auto-fill is also supported, vs. export-only) | S1 | Mapped to URI export since S1's language ("represented using... URIs for centralized deployment management") describes generating/using a URI representation rather than confirming a paste-to-populate-fields workflow. |
| CONN-auth-std | Standard auth | Unverified | Not itemized for MongoDB specifically in S1 beyond general "authentication databases" management under RBAC (see [Governance matrix](../governance/feature-matrix.md)). | — | Unverified | S1 | — |
| CONN-tls | TLS/SSL config | Confirmed | S1: "Navicat secures client-to-database transport via native SSH Tunneling and SSL/TLS encryption, protecting database traffic across public networks or unsegmented enterprise networks." | Depth (CA cert, client cert, SNI, validation toggles) not itemized. | Unverified (configuration depth) | S1 | — |
| CONN-ssh | SSH tunnel | Confirmed | Same S1 sentence as CONN-tls: "native SSH Tunneling... encryption." | Password vs. private-key mode split not itemized. | Unverified (mode depth) | S1 | — |
| CONN-org-folders | Organization & folders | Confirmed | S1 (Feature Inventory): "Workspace Productivity Tools:... virtual grouping of database objects." | — | Unverified | S1 | — |
| CONN-color-coding | Color coding | Confirmed | S1: "To prevent accidental modifications to production environments, Connection Coloring allows administrators to assign distinctive background tags (e.g., red for production, green for development) to connection headers and editor windows." | — | Unverified | S1 | — |
| CONN-team-sharing | Team sharing | Confirmed (existence); Unverified (granularity) | S1 (Product Overview): "Navicat Cloud, a cloud-hosted synchronization software-as-a-service (SaaS), and Navicat On-Prem Server, an enterprise-hosted collaboration platform that stores connections, queries, models, and virtual groups entirely within a customer's internal infrastructure." Navicat Cloud Pro pricing row: "synchronize up to 5,000 units across 500 projects and team members." | Navicat Cloud Pro is a paid add-on ($9.99/mo or $99/yr per user); On-Prem Server is a separately licensed enterprise product. | Unverified | S1 | Per-role permission levels (Manage/Edit/View, as Studio 3T has) are not described — only "synchronize" and "collaboration" language. |
| CONN-cred-storage | Credential storage | Unverified | Not discussed for MongoDB connections specifically; S1 discusses RBAC/authentication database management (see F-GOV) but not a local credential-storage encryption mechanism. | — | Unverified | S1 | — |
| CONN-compat-cosmos | Azure Cosmos DB | Confirmed (as a target infrastructure, connectivity depth unverified) | S1 (Product Overview): "alongside major cloud-managed database infrastructure such as Amazon RDS, Amazon Aurora, Microsoft Azure, Google Cloud, and MongoDB Atlas." | S1 names "Microsoft Azure" and "Google Cloud" generically, not "Azure Cosmos DB (MongoDB API)" by name. | Unverified | S1 | Mapped cautiously — S1 does not use the specific term "Cosmos DB"; included because Azure cloud-managed database support is named, but the exact Cosmos DB MongoDB-API compatibility claim is not explicit. Treat as a weak/partial match. |

## Feature-level conclusion

### Confirmed strengths

- SSH tunneling and SSL/TLS transport encryption are both confirmed for securing database traffic.
- Connection Coloring (background color tags per connection, e.g. red for production) is a specific, well-described productivity/safety feature.
- Two distinct team-collaboration backends exist — Navicat Cloud (SaaS) and Navicat On-Prem Server (self-hosted) — for sharing connections, queries, models, and virtual groups across a team.
- Standard Navicat URI representation for connection configuration, supporting centralized deployment management.

### Confirmed limitations

- The source does not itemize MongoDB-specific topology support (standalone/replica set/sharded/SRV), enterprise authentication protocols (Kerberos/LDAP/AWS IAM/OIDC), or TLS/SSH configuration depth (CA cert options, key modes) — these are silent gaps in the source, not confirmed absences.
- No dedicated credential-storage encryption mechanism (e.g., OS keystore API, AES-256 local vault) is described for Navicat, unlike Compass (OS Keytar API) or VisuaLeaf (AES-256 local).

### Open questions / unknowns

- Whether Navicat supports MongoDB enterprise authentication mechanisms (Kerberos/LDAP/AWS IAM/OIDC) at all — not discussed in the source in either direction.
- Whether connection configurations (beyond the URI representation) can be exported/imported as a portable file format, or duplicated/organized via the sidebar the way Compass/VisuaLeaf/Studio 3T support — not discussed.
- Exact mechanism and encryption strength of Navicat's local credential storage — not discussed.
