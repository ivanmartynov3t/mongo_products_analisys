# Feature Matrix — NoSQLBooster / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: NoSQLBooster
- Product group: third-party
- Feature ID: F-CONN (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `connectivity`
- Analysis date: 2026-09-04
- Version/release context: v11.0–v11.1 line

## Source index

- S1: NoSQLBooster Competitive Analysis, `research/google_research/nosqlbooster-competitive-analysis/NoSQLBooster Competitive Analysis.md`
- S2: NoSQLBooster Competitive Intelligence Analysis, `research/google_research/nosqlbooster-competitive-intelligence-analysis/NoSQLBooster Competitive Intelligence Analysis.md`
- P1: nosqlbooster.com/features (primary source; cited as S1 Works Cited #1/#9 and S2 Works Cited #2/#10; fetched directly by this review 2026-09-04 to adjudicate the SSH-key-list discrepancy between S1 and S2)
- P2: nosqlbooster.com/compareEditions (primary source; cited as S1 Works Cited #7 and S2 Works Cited #9; fetched directly by this review 2026-09-04)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONN-topology | Topology types | Confirmed | S2: "standalone instances, replica sets, sharded clusters, and cloud-hosted MongoDB Atlas deployments." P2's edition-comparison table lists Direct Connection, Replica Set, and Sharded Cluster as distinct rows present across all tiers. | — | N/A | S2, P2 | — |
| CONN-auth-std | Standard auth | Confirmed | S2: "Supported authentication mechanisms encompass SCRAM-SHA-1/256, MONGODB-CR, X.509 certificates..." P2 lists matching rows. | — | N/A | S2, P2 | — |
| CONN-auth-enterprise | Enterprise auth | Confirmed, tier-gated | S1 & S2 both confirm Kerberos (GSSAPI), LDAP (PLAIN), AWS IAM, and OIDC support. P2 lists matching auth rows (Kerberos, LDAP, MONGODB-AWS, MONGODB-OIDC). | S1's own pricing table: "Personal License... Restricted: Lacks Kerberos (GSSAPI) and LDAP (PLAIN) auth"; unlocked at Commercial tier and above. | N/A | S1, S2, P2 | AWS SSO specifically (named in S1's prose and S2's "AWS IAM (including credential process integration and SSO)" phrasing) is Unverified as a distinct itemized capability — P2's edition-comparison table lists only one generic "MONGODB-AWS Authentication" row, not an SSO-specific one. |
| CONN-tls | TLS/SSL config | Confirmed | S2: "Security infrastructure covers transport encryption via SSL/TLS..." P2 lists an "SSL Support" row. | — | N/A | S2, P2 | Config depth (CA cert, SNI, validation toggles) not itemized in either source file. |
| CONN-ssh | SSH tunnel | Confirmed, list corrected via primary source | S2: "SSH tunneling supporting Ed25519, ECDSA, and ECDH host keys." P1's Feature Tour page states verbatim: "SSH tunneling for MongoDB connections, support SSH key format: ECDH, ECDSA, and Ed25519" — matching S2's list exactly. | — | N/A | S2, P1 | **Reconciliation:** S1 instead lists "RSA, DSA, ECDSA, and Ed25519" (Product overview section). P1, the primary source both files cite, corroborates S2's list (ECDH/ECDSA/Ed25519) and does not corroborate S1's RSA/DSA claim — S1's specific key-list claim is not carried forward as confirmed. |
| CONN-in-use-enc | In-use encryption | Confirmed | S1: "native Queryable Encryption management." S2: "NoSQLBooster provides configuration interfaces for Client-Side Field Level Encryption (CSFLE) and Queryable Encryption (QE)." P2 lists an "In-Use Encryption (CSFLE & QE)" row. | — | N/A | S1, S2, P2 | Introduced per S1's/S2's own release-history tables in v9.0 (August 2024). |

## Feature-level conclusion

### Confirmed strengths

- A full modern-MongoDB connectivity surface: all standard topologies including Atlas, the complete standard and enterprise MongoDB auth mechanism roster (including OIDC), TLS, SSH tunneling, and native CSFLE/Queryable Encryption configuration — evidenced consistently across both source files and corroborated by the vendor's own edition-comparison page.

### Confirmed limitations

- Enterprise authentication (Kerberos, LDAP) is confirmed excluded from the Free and Personal license tiers by S1's own pricing table — a real adoption friction point for individual developers working against enterprise-secured MongoDB deployments, called out explicitly in S1's own "Product weaknesses" section.

### Open questions / unknowns

- Connection organization/UX capabilities (folders, color coding, credential-storage mechanism, session restore, portability/export-import of connection configs) are not discussed in either source file's body text and are left out of this matrix rather than asserted from an out-of-scope primary-source glance — see `product-report.md`'s reconciliation note on this review's narrow, targeted use of primary-source verification.
- Exact TLS configuration depth (CA cert handling, SNI, hostname-validation toggles) is unconfirmed.
