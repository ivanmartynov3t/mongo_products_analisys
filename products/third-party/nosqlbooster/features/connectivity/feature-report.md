# Feature Report — NoSQLBooster / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Connectivity
- Feature ID: F-CONN (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: NoSQLBooster
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

NoSQLBooster's connectivity surface targets the same breadth of MongoDB deployment topologies as its competitors: standalone instances, replica sets, sharded clusters, and Atlas-hosted deployments. Authentication spans the full standard mechanism set (SCRAM-SHA-1/256, MONGODB-CR, X.509) plus the enterprise set (Kerberos GSSAPI, LDAP PLAIN, AWS IAM, MongoDB OIDC) — though Kerberos and LDAP specifically are excluded from the Free and Personal license tiers per S1's pricing table, unlocking only at Commercial tier and above. Transport security covers TLS/SSL and SSH tunneling; the SSH tunnel's supported key algorithm list was a point of disagreement between the two source files (S1: RSA/DSA/ECDSA/Ed25519; S2: Ed25519/ECDSA/ECDH), resolved in favor of S2's list after this review fetched the vendor's own Feature Tour page, which states the supported formats verbatim as "ECDH, ECDSA, and Ed25519." NoSQLBooster also natively supports Client-Side Field Level Encryption (CSFLE) and Queryable Encryption (QE) configuration, introduced in the v9.0 release (August 2024) per both files' release-history tables.

Also mentioned in the source material, but not mapped to any existing F-CONN sub-feature ID: a "multi-node cluster management" capability (S1) letting users broadcast a shell command across multiple replica-set members simultaneously, with results aggregated into a single JSON response keyed by member. This is closer to a shell/scripting-execution feature than a connection-configuration one, and does not cleanly fit any `CONN-*` or `SHELL-*` dictionary definition — see `features/shell/feature-report.md`'s "Interactions and dependencies" section for where this is instead discussed narratively.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| CONN-auth-enterprise | Kerberos/LDAP support is real but tier-gated below Commercial. | Individual developers on the Personal tier working against Kerberos/LDAP-secured enterprise MongoDB deployments must upgrade tiers or use a different tool. | S1 pricing table |
| CONN-ssh | SSH key-algorithm list corrected from S1's RSA/DSA/ECDSA/Ed25519 claim to the primary-source-confirmed ECDH/ECDSA/Ed25519 list. | Affects only the precise algorithm roster claimed, not the existence of SSH tunneling itself (both files and the primary source agree it exists). | S2 body text; nosqlbooster.com/features (primary, fetched directly) |
| CONN-in-use-enc | CSFLE + Queryable Encryption configuration is a genuine, confirmed capability, not just a marketing claim — it appears in both files' release-history tables (v9.0, August 2024) and the vendor's own edition-comparison page. | Positions NoSQLBooster alongside MongoDB Compass and Studio 3T (both of which also support QE/CSFLE) rather than behind them on this specific dimension. | S1, S2, P2 |

## Constraints and risks

- The Free and Personal tiers exclude Kerberos/LDAP enterprise auth entirely, per S1's own pricing table — a real functional gap for individual developers, not just a soft nudge toward upgrading.
- Neither source file itemizes TLS configuration depth (CA certificate handling, SNI, hostname-validation toggles) or connection-pool/advanced parameters, so those remain unconfirmed rather than assumed comprehensive.

## Interactions and dependencies

- CSFLE/Queryable Encryption connectivity configuration (`CONN-in-use-enc`) is a prerequisite for any query/aggregation work against an encrypted collection, but neither source file describes whether NoSQLBooster's query/aggregation surfaces have any QE-aware UI beyond the connection-level key-vault configuration.
- The multi-node replica-broadcast capability (see "Behavioral walkthrough" above) depends on an already-established replica-set connection and is really a shell-execution-time behavior, not a connection-setup-time one.

## Conclusions

### Strengths

- Full modern MongoDB topology and authentication coverage, including OIDC and native CSFLE/Queryable Encryption configuration — on par with MongoDB Compass and Studio 3T on this specific dimension, ahead of DBeaver's and DataGrip's largely unverified MongoDB-specific connectivity depth.

### Limitations

- Kerberos/LDAP enterprise auth is confirmed excluded below the Commercial license tier.

### Unknowns

- AWS SSO as a distinct, itemized capability (as opposed to a gloss on standard AWS IAM/MONGODB-AWS auth).
- TLS configuration depth and connection-pool/advanced parameters.
