# Feature Report — Navicat / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Connectivity
- Feature ID: F-CONN (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: Navicat
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

Navicat connects to MongoDB alongside a broad set of other engines (MySQL, MariaDB, SQL Server, Oracle, PostgreSQL, SQLite, Redis, Snowflake) and cloud-managed infrastructure (Amazon RDS, Amazon Aurora, Microsoft Azure, Google Cloud, MongoDB Atlas) within Navicat Premium, or as a MongoDB-only client in Navicat for MongoDB. Transport security is provided via native SSH tunneling and SSL/TLS encryption. Connections can be represented as standard Navicat URIs for centralized deployment management, and administrators can tag connections with distinctive background colors (e.g., red for production, green for development) to reduce the risk of accidental modifications to the wrong environment.

Team-level connection sharing is handled by one of two backends: Navicat Cloud (a cloud-hosted SaaS, with a paid "Cloud Pro" tier supporting up to 5,000 synchronized units across 500 projects/team members) or Navicat On-Prem Server (a self-hosted enterprise collaboration platform storing connections, queries, models, and virtual groups entirely within the customer's own infrastructure).

Beyond these points, the source material does not go deep on connectivity mechanics: it does not itemize MongoDB topology support (standalone/replica set/sharded/DNS SRV), specific TLS configuration options (CA certificates, client certs, SNI), SSH tunnel modes (password vs. private key), or enterprise authentication protocols (Kerberos, LDAP, AWS IAM, OIDC) for MongoDB connections specifically.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| CONN-tls / CONN-ssh | Both confirmed to exist as a paired transport-security capability, but with no configuration depth described. | Cannot assess parity with Compass/VisuaLeaf/Studio 3T's fuller SSH/TLS option sets from this source alone. | Research file narrative |
| CONN-color-coding | Well-described, specific safety feature (production/development color tagging on connection headers and editor windows). | A genuine productivity/safety differentiator worth noting even though most other connectivity dimensions are thin. | Research file narrative |
| CONN-team-sharing | Two distinct collaboration backends (Navicat Cloud, Navicat On-Prem Server) exist, but per-role permission granularity (à la Studio 3T's Manage/Edit/View) is not described. | Team-sharing existence is Confirmed; whether it supports Studio 3T-style granular permissions is Unverified. | Research file narrative + pricing table |

## Constraints and risks

- This is one of the thinner feature areas for Navicat despite a strong overall product — the source's Product Overview and Security sections give existence-level confirmation for several capabilities but rarely configuration-level detail.
- Silence on a sub-feature (e.g., topology types, enterprise auth) means "not evidenced either way" per this repository's unverified-by-default rule, not "confirmed absent."

## Interactions and dependencies

- Connection Coloring and URI-based configuration both interact with Navicat's broader "prevent accidental production modification" theme, which also appears in [F-GOV](../governance/feature-report.md) (RBAC) and [F-TRANSFER](../data-transfer/feature-report.md) (no data-masking capability, a related but distinct safety gap).
- Navicat Cloud / On-Prem Server team-sharing is licensed and priced separately from the core desktop client — see [product-report.md](../../product-report.md) for the full pricing table.

## Conclusions

### Strengths

- Confirmed SSH tunneling, SSL/TLS transport encryption, connection coloring, and two distinct team-collaboration backends (cloud SaaS and self-hosted enterprise).
- Standard URI representation for centralized connection deployment management.

### Limitations

- No itemized detail on MongoDB topology support, TLS/SSH configuration depth, or enterprise authentication protocols — a materially thinner connectivity picture than Compass, VisuaLeaf, or Studio 3T provide in their own sources.
- No described local credential-storage encryption mechanism.

### Unknowns

- MongoDB-specific topology support (standalone/replica set/sharded/SRV).
- Enterprise auth protocol support (Kerberos/LDAP/AWS IAM/OIDC) for MongoDB connections.
- Connection portability (export/import as a file), sidebar search/duplicate/favorite operations, and credential-storage mechanism.
