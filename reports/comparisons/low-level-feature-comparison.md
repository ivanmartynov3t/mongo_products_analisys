# Low-Level Feature Comparison

This report compares normalized capabilities at feature level.

## Navigation

- [Cumulative report index](../cumulative-report.md)
- [High-level comparison](high-level-product-comparison.md)
- [Compass product report](../../products/third-party/mongodb-compass/product-report.md)

## Current baseline coverage

- Third-party product analyzed: MongoDB Compass
- 3t products analyzed: none

## Capability comparison table

| Feature | Capability ID | Capability | MongoDB Compass (third-party) | 3t product behavior | Gap type | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| connectivity | CONN-001 | Multi-instance active connections | Supported (documented in 1.44.0+) | Not assessed | Open | [connectivity matrix](../../products/third-party/mongodb-compass/features/connectivity/feature-matrix.md) |
| connectivity | CONN-002 | Advanced auth methods (SCRAM/OIDC/X.509/Kerberos/LDAP/AWS IAM) | Supported | Not assessed | Open | [connectivity matrix](../../products/third-party/mongodb-compass/features/connectivity/feature-matrix.md) |
| querying | QRY-001 | Query-bar filter/project/sort/skip/limit/collation/maxTimeMS | Supported | Not assessed | Open | [querying matrix](../../products/third-party/mongodb-compass/features/querying/feature-matrix.md) |
| aggregation | AGG-001 | Multi-mode aggregation authoring | Supported | Not assessed | Open | [aggregation matrix](../../products/third-party/mongodb-compass/features/aggregation/feature-matrix.md) |
| schema-validation | SCH-001 | Sampling-based schema profiling | Supported | Not assessed | Open | [schema-validation matrix](../../products/third-party/mongodb-compass/features/schema-validation/feature-matrix.md) |
| indexing-performance | IDX-001 | Index lifecycle and usage insights | Supported | Not assessed | Open | [indexing-performance matrix](../../products/third-party/mongodb-compass/features/indexing-performance/feature-matrix.md) |
| security-governance | SEC-001 | Readonly/protection/network policy controls | Supported with caveats | Not assessed | Open | [security-governance matrix](../../products/third-party/mongodb-compass/features/security-governance/feature-matrix.md) |

## Notes

- As 3t product feature matrices are added, replace `Not assessed` rows with explicit behavior-level entries.
