# Feature Matrix — DBeaver / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: DBeaver
- Product group: third-party
- Feature ID: F-CONN (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `connectivity`
- Analysis date: 2026-09-04
- Version/release context: DBeaver 25.x–26.x line

## Source index

- S1: DBeaver Competitive Intelligence Analysis (secondary research file), `research/google_research/dbeaver-competitive-intelligence-analysis/DBeaver Competitive Intelligence Analysis.md`
- S2: MongoDB authentication | DBeaver Documentation, https://dbeaver.com/docs/dbeaver/Authentication-MongoDB/ (cited in S1's Works Cited #27; not independently fetched for this matrix)
- S3: Connect from DBeaver - SQL Interface - MongoDB Docs, https://www.mongodb.com/docs/sql-interface/dbeaver/connect/ (cited in S1's Works Cited #28; MongoDB's own documentation of the DBeaver integration)
- S4: Security restrictions for database connection | DBeaver Documentation, https://dbeaver.com/docs/dbeaver/Managing-security-restrictions-for-database-connection/ (S1 Works Cited #25)
- S5: License types - DBeaver PRO, https://dbeaver.com/license-types/ (S1 Works Cited #16)
- S6: Differences between license types · dbeaver/dbeaver Wiki - GitHub, https://github.com/dbeaver/dbeaver/wiki/Differences-between-license-types (S1 Works Cited #18, #19)
- S7: MongoDB | DBeaver Documentation, https://dbeaver.com/docs/dbeaver/MongoDB/ (S1 Works Cited #10)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONN-topology | Topology types | Unverified | S1 states DBeaver connects to MongoDB via a JDBC/NoSQL driver layer but does not enumerate standalone/replica-set/sharded/SRV connection support specifically. | MongoDB connectivity itself requires a paid tier (Lite/Enterprise/Ultimate) — confirmed via S1's pricing table. | Unverified | S1, S7 | The existence of a dedicated MongoDB connection type is confirmed (S7); topology-mode granularity is not. |
| CONN-auth-std | Standard auth | Unverified — per secondary source, no primary citation for specific mechanisms (SCRAM/X.509) | S1 does not name specific MongoDB authentication mechanisms; a DBeaver-authored documentation page on MongoDB authentication exists (S2) but its content was not reproduced in S1 and was not independently fetched for this matrix. | — | Unverified | S1, S2 | Do not upgrade to Confirmed without reading S2 directly — this matrix intentionally does not do so per Plan 4's "no independent verification" scope rule. |
| CONN-auth-enterprise | Enterprise auth | Confirmed (existence + edition gating); Unverified (MongoDB-specific applicability) | S1: "Enterprise Identity and Authentication: Authentication protocols including SAML 2.0, Kerberos, SSL/TLS, Microsoft Entra ID (Azure AD), and cloud IAM platforms across AWS, GCP, and Azure." S1 also states Community Edition blocks SSO/SAML/Kerberos/Azure AD, forcing upgrade to a commercial license. | Gated to paid tiers; S1 does not confirm whether these protocols are usable specifically on MongoDB connections vs. only on relational/JDBC connections generally. | Unverified (MongoDB scope) | S1, S5, S6 | Edition-gating claim is corroborated by two independent primary-source citations in S1 (DBeaver's own license page and its GitHub wiki license-differences page). |
| CONN-tls | TLS/SSL config | Confirmed (general existence); Unverified (MongoDB-specific config depth) | S1 lists "SSL/TLS" among supported authentication/security protocols. | MongoDB-specific TLS field set (CA cert, client cert, SNI) not itemized in S1. | Unverified | S1 | — |
| CONN-readonly-lock | Read-only lock | Confirmed | S1: "Connection Security Restrictions: Administrative toggles that enforce client-side constraints on individual connections, including read-only modes, prohibiting data editing, blocking structural DDL alterations, restricting script execution, and blocking external data imports." Backed by a DBeaver-authored documentation page dedicated to exactly this topic (S4). | Per-connection, client-side (UI) restriction — S1 does not state it is a server-enforced control. | Unverified (enforcement depth) | S1, S4 | Strong match: S4's title ("Security restrictions for database connection") directly corresponds to this sub-feature. |
| CONN-cred-storage | Credential storage | Confirmed (general existence) | S1: "Secret Managers and Credential Storage: Master password keystore encryption paired with enterprise secret manager integrations." | Local encrypted keystore is baseline; external secrets-manager integration is a separate, paid capability (see [GOV-secrets-vault](../governance/feature-matrix.md)). | Unverified (depth) | S1 | See F-GOV matrix for the external secrets-manager integration itself. |
| CONN-portability | Import/export configs | Unverified | Not discussed in S1 for MongoDB connections specifically. | — | Unverified | S1 | Omitted from the low-level comparison reports pending evidence. |

## Feature-level conclusion

### Confirmed strengths

- DBeaver has a dedicated, vendor-documented MongoDB connection type (S7) and a dedicated documentation page on MongoDB authentication (S2), confirming the connection surface exists even though this matrix does not independently verify its full mechanism list.
- Per-connection read-only/write-restriction toggles are confirmed via a DBeaver-authored documentation page dedicated to that exact capability (S4).
- Enterprise authentication protocol support (SAML, Kerberos, Azure AD) and its Community-Edition gating are corroborated by two independent primary-source citations in the research file.

### Confirmed limitations

- MongoDB connectivity of any kind requires a paid tier (Lite/Enterprise/Ultimate) — the free Community Edition has none (S1's pricing/edition comparison table).
- The research file does not confirm whether DBeaver's enterprise-auth and secrets-manager integrations apply to MongoDB connections specifically, as opposed to only its relational/JDBC connections generally.

### Open questions / unknowns

- Full list of standard MongoDB auth mechanisms (SCRAM-SHA-256/1, X.509) supported by DBeaver's MongoDB driver.
- Whether DBeaver supports mongodb+srv:// URI paste/auto-fill, replica-set/sharded topology selection, or SSH tunneling specifically for MongoDB connections (CONN-uri-paste, CONN-ssh not evidenced either way in the source and are therefore omitted from this matrix rather than marked absent).
