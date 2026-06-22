# Feature Matrix — MongoDB Compass / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://www.mongodb.com/docs/compass/connect/
- S2: https://www.mongodb.com/docs/compass/connect/advanced-connection-options/authentication-connection/
- S3: https://www.mongodb.com/docs/compass/connect/advanced-connection-options/tls-ssl-connection/
- S4: https://www.mongodb.com/docs/compass/connect/advanced-connection-options/ssh-connection/
- S5: https://www.mongodb.com/docs/compass/connect/connections/
- S6: https://www.mongodb.com/docs/compass/connect/favorite-connections/import-export/
- S7: https://www.mongodb.com/docs/compass/connect/required-access/
- S8: https://www.mongodb.com/docs/compass/connect/advanced-connection-options/in-use-encryption/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONN-topology | Topology connection support | Supported | Connects to standalone, replica set, and sharded deployments. | Replica-set direct-member connection has staleness/failover caveat. | Unknown | S1 | SRV and replica set options are recommended in docs. |
| CONN-multi-active | Multiple active connections | Supported | Multiple MongoDB instances can be active concurrently with tab separation. | Documented from Compass 1.44.0. | Unknown | S1, S5 | Useful for multi-environment workflows. |
| CONN-auth-std | Standard authentication methods | Supported | Supports None (no credentials), SCRAM-SHA-256, SCRAM-SHA-1, and X.509 certificate authentication. | Method-specific fields and provider setup required. | Unknown | S2 | |
| CONN-auth-enterprise | Enterprise authentication methods | Supported | Supports OIDC (with additional security switches), Kerberos (GSSAPI), LDAP (PLAIN), and AWS IAM. | Provider-specific configuration required. | Unknown | S2 | OIDC includes additional security switches. |
| CONN-tls | TLS/SSL controls | Supported | TLS on/off/default with CA, client cert/key, passphrase, and validation toggles. | Insecure toggles are explicitly warned as security risk. | Unknown | S3 | TLS required for some deployment modes. |
| CONN-ssh | SSH tunnel | Supported | SSH tunnel with password and private-key authentication modes. | Credentials may travel in plaintext in some setups; warnings shown. | Unknown | S4 | Replica set via SSH is supported. |
| CONN-proxy | Proxy | Supported | Socks5 proxy mode supported. | Credentials may travel in plaintext in some proxy setups; warnings shown. | Unknown | S4 | |
| CONN-portability | Saved connection portability | Supported | Saved connections can be exported/imported via UI or CLI, with optional passphrase encryption. | Unencrypted export can include plaintext secrets. | Unknown | S6 | Includes secret-removal option. |
| CONN-sidebar-ops | Connection operations in sidebar | Supported | Connect/disconnect, duplicate, favorite, search, refresh, and error inspection actions. | Some actions depend on active state and permissions. | Unknown | S5 | Also supports performance-view entry. |
| CONN-in-use-enc | In-use encryption connection config | Supported with constraints | Queryable Encryption connection workflow includes key vault namespace and KMS provider config. | Replica set or sharded cluster context required. | Unknown | S8 | Multiple KMS providers documented. |
| CONN-role-docs | Role/privilege mapping docs | Supported | Required access guide maps features to required privileges/roles. | Enforcement depends on server-side auth config. | Unknown | S7 | Supports least-privilege planning. |
