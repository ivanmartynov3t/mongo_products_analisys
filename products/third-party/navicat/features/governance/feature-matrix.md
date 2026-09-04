# Feature Matrix — Navicat / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: Navicat
- Product group: third-party
- Feature ID: F-GOV (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `governance`
- Analysis date: 2026-09-04
- Version/release context: Navicat 17 line

## Source index

- S1: Navicat Competitive Intelligence Analysis (secondary research file), `research/google_research/navicat-competitive-intelligence-analysis/Navicat Competitive Intelligence Analysis.md`

## Capability matrix (low-level)

Navicat's Data Synchronization and Structure Synchronization engines (two of the source's three named synchronization engines — the third, Data Transfer, is covered in [F-TRANSFER](../data-transfer/feature-matrix.md)) are mapped into this feature area as the closest existing dictionary IDs: Structure Synchronization (DDL/schema diffing) to `GOV-collection-compare`, and Data Synchronization (document-level content diffing and reconciliation) to `GOV-collection-sync`. Both engines are also cross-referenced from [F-SCHED](../task-scheduler/feature-matrix.md) for their scheduling/automation angle, since the source describes them as schedulable via the integrated Automation module.

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-rbac-users | RBAC user management | Confirmed | S1: "Navicat provides graphical User and Role Designers across supported database engines, including MongoDB. System administrators can create users, define role-based access control (RBAC) permissions, manage authentication databases..." | — | Unverified | S1 | — |
| GOV-rbac-roles | Custom role creation | Confirmed | Same S1 sentence: "...define role-based access control (RBAC) permissions..." | — | Unverified | S1 | — |
| GOV-rbac-actions | Privilege actions | Confirmed | Same S1 sentence: "...assign granular object-level read, write, or administrative privileges without executing manual shell commands." | — | Unverified | S1 | — |
| GOV-rbac-tree | Privilege tree view | Unverified | Not itemized — S1 confirms graphical User and Role Designers exist but does not describe a hierarchical effective-privilege tree view specifically. | — | Unverified | S1 | — |
| GOV-rbac-inheritance | Role inheritance | Unverified | Not discussed — no mention of inheriting from built-in or custom roles / role chains for Navicat. | — | Unverified | S1 | — |
| GOV-data-masking | Data masking | Not supported (confirmed absent) | S1 (Strengths/Weaknesses table): "Security & Governance | SSH/SSL tunneling, RBAC designers, connection coloring, and Navicat On-Prem Server. | Lacks native field-level data masking and obfuscation (e.g., 3TL Bridge) for compliance." Also: "Data Masking & Compliance | Not available; basic permissions and roles. | Field-level dynamic data obfuscation (3TL Bridge)." (Direct Comparison table) | — | Not planned | S1 | Confirmed-absent by direct, repeated statement across two separate tables in the source — also noted in [product-report.md](../../product-report.md)'s constraints section and in [F-TRANSFER](../data-transfer/feature-matrix.md)'s `TRANSFER-masking-tool` row. |
| GOV-collection-compare | Collection compare | Confirmed | S1: "Structure Synchronization: Compares DDL and schema definitions across database instances. It identifies structural variances across collections, indexes, views, and validation constraints, producing exact alteration scripts to align development, staging, and production environments." | — | Unverified | S1 | Mapped from Structure Synchronization, the DDL/schema-diffing half of Navicat's three-engine synchronization suite. |
| GOV-collection-sync | Collection sync | Confirmed | S1: "Data Synchronization: Performs row-by-row or document-by-document content comparisons between source and target databases. The engine highlights insertions, modifications, and deletions, generating preview scripts or executing direct synchronization to reconcile data drift." | — | Unverified | S1 | Mapped from Data Synchronization, the document-level content-diffing/reconciliation half of the same suite. This engine description ("directed... insert/update/delete between compared collections") is a close match to the dictionary's own `GOV-collection-sync` wording. |
| GOV-audit-log | Audit logging | Unverified | Not discussed — Server Monitor (see [F-IDX](../indexing-performance/feature-matrix.md)) tracks live connection/CPU/memory/lock state, not a queryable history of who ran what query or modification with a timestamp. | — | Unverified | S1 | — |
| GOV-secrets-vault | External secrets manager integration | Unverified | Not discussed for Navicat — no mention of HashiCorp Vault, CyberArk, AWS Secrets Manager, or any external secrets-manager integration. | — | Unverified | S1 | Included as a row because this dictionary ID was added specifically for this cross-product effort (2026-09-04); Navicat's source gives no evidence either way, unlike DBeaver's source which named specific vault products. |
| CONN-color-coding | Connection coloring (cross-referenced) | Confirmed | See [Connectivity feature matrix](../connectivity/feature-matrix.md) for full detail; included here because the source frames it explicitly as a governance/safety control: "To prevent accidental modifications to production environments, Connection Coloring allows administrators to assign distinctive background tags..." | — | Unverified | S1 | Primary row lives in F-CONN; cross-referenced here for governance completeness, mirroring how DBeaver's F-GOV matrix cross-references `CONN-auth-enterprise`. |

## Feature-level conclusion

### Confirmed strengths

- Graphical User and Role Designers spanning create/modify/delete users, RBAC permission definition, authentication-database management, and granular object-level read/write/admin privilege assignment — all without manual shell commands.
- Two distinct, purpose-built synchronization/diffing engines (Structure Synchronization for DDL/schema, Data Synchronization for document content) producing preview scripts or executing direct reconciliation.
- Connection Coloring is a specific, well-described accidental-modification-prevention control, explicitly framed by the source as a governance/safety mechanism.

### Confirmed limitations

- No field-level data masking/obfuscation of any kind — confirmed absent by direct, repeated statement across two separate tables in the source (also tracked in [F-TRANSFER](../data-transfer/feature-matrix.md)).
- No privilege-tree visualization, role-inheritance/role-chain mechanism, audit logging, or external secrets-manager integration is described in the source in either direction — these are silent gaps, not confirmed absences, but they leave Navicat's governance depth thinner than Studio 3T's or 3T Lens/3T Access's platform-tier coverage in this repository's own comparison data.

### Open questions / unknowns

- Whether Navicat's RBAC designer surfaces a hierarchical effective-privilege tree, or only a flat permission list.
- Whether custom roles can inherit from built-in or other custom roles.
- Whether any audit trail of queries/modifications/connections (with timestamp and user) exists anywhere in the product, even outside the Server Monitor tool.
- Whether external secrets-manager integration exists in any form — not discussed in the source in either direction.
