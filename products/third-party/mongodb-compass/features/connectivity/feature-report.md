# Feature Report — MongoDB Compass / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers end-to-end connection behavior: deployment targeting, auth, transport security, proxy/tunnel, and connection sharing.

## Behavioral walkthrough

Compass provides both direct connection-string workflows and advanced-tab workflows for transport and authentication controls. It supports connection reuse, favorites, import/export portability, and concurrent active sessions.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| CONN-001 | Topology coverage includes standalone/replica/sharded. | Broad compatibility with common MongoDB deployment types. |
| CONN-003 | Authentication coverage is broad (SCRAM, OIDC, X.509, Kerberos, LDAP, AWS IAM). | Supports enterprise identity patterns. |
| CONN-004 | TLS controls are detailed and include risk-prone bypass flags. | Strong flexibility; requires governance guardrails. |
| CONN-006 | Connection export/import supports encryption and secret stripping. | Enables team portability with manageable secret hygiene. |
| CONN-008 | Queryable Encryption connection setup exists with KMS options. | Supports secure deployments with extra setup complexity. |

## Constraints and risks

- Misconfigured proxy or insecure TLS settings can reduce security posture.
- Unencrypted connection export can leak credentials.
- Effective access control still depends on server-side roles.

## Conclusion

Connectivity is a strong feature area for Compass: broad protocol/auth support, practical ops tooling, and documented security caveats.
