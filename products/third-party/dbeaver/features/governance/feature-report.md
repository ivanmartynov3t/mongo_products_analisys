# Feature Report — DBeaver / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Governance & Security
- Feature ID: F-GOV (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: DBeaver
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

DBeaver's governance surface, as described in the research file, centers on three pillars: connection-level access restriction, credential/secrets management, and enterprise identity federation. Administrators can apply per-connection security restrictions — read-only mode, blocked DDL/script execution, blocked external data import — documented on a dedicated DBeaver documentation page. Credentials are stored in a local master-password-encrypted keystore by default, with paid tiers additionally able to source credentials from an external secrets manager (HashiCorp Vault, CyberArk, or AWS Secrets Manager) rather than storing them locally. Enterprise identity federation (SAML 2.0, Kerberos, Microsoft Entra ID/Azure AD) is available in paid tiers only — the Community Edition explicitly blocks these, which the research file frames as a deliberate commercial lever forcing enterprise procurement to a paid license even when developers only need basic SQL functionality.

A schema/structure "compare" capability also exists (documented at `dbeaver.com/docs/dbeaver/Schema-compare/`), but it is relational-DDL-oriented; the research file's own (unverified-by-us) assessment is that it struggles with nested BSON arrays and documents when applied to MongoDB structures.

Team Edition and CloudBeaver extend this into browser-based team workspaces with centralized connection sharing and RBAC "tied to corporate directory services," but the source gives no further granularity (no privilege model, no role-inheritance detail, no audit-log description) — this repository's matrix does not manufacture detail the source does not supply.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| GOV-readonly-mode | Per-connection client-side write-restriction toggle, vendor-documented. | Parity point with Studio 3T's own per-connection read-only lock. | DBeaver Docs "Managing security restrictions for database connection" |
| GOV-secrets-vault | External secrets-manager integration (Vault/CyberArk/AWS Secrets Manager) is asserted but not traced to a specific DBeaver documentation page in the source's own Works Cited. | A real enterprise differentiator if true, but held to Unverified pending primary-source confirmation. | Research file narrative only |
| GOV-collection-compare | Schema/structure compare exists (vendor-documented) but is DDL-first and reportedly weak on nested BSON. | Materially different from Studio 3T's field-level collection-to-collection data compare/sync. | DBeaver Docs "Schema compare" + research file's own characterization |

## Constraints and risks

- The secrets-vault integration — arguably DBeaver's most enterprise-relevant governance claim — is the one governance capability in this feature area without a specific matching primary-source citation in the research file's Works Cited list; do not upgrade it to Confirmed in any downstream summary without independent verification.
- RBAC/audit-log depth for Team Edition/CloudBeaver is too vague in the source to support a confident matrix row and is intentionally omitted rather than guessed.

## Interactions and dependencies

- `GOV-readonly-mode` is the same underlying capability tracked as `CONN-readonly-lock` in [F-CONN](../connectivity/feature-report.md) — a per-connection toggle that is simultaneously a connectivity control and a governance control.
- Enterprise auth (`CONN-auth-enterprise`) gates both connectivity and governance posture; see [F-CONN](../connectivity/feature-report.md) for the primary row.

## Conclusions

### Strengths

- Vendor-documented per-connection read-only/write-restriction toggle.
- Enterprise identity protocol breadth (SAML, Kerberos, Azure AD), confirmed via two independent DBeaver licensing-page citations.
- Schema/structure compare tool exists, vendor-documented, even though its MongoDB fit is reportedly weak.

### Limitations

- No primary source backs the external secrets-manager integration claim, despite it being one of the more competitively interesting governance capabilities described.
- No detailed RBAC, audit-logging, or compliance-policy capability is evidenced for MongoDB connections specifically.

### Unknowns

- Exact secrets-manager integration mechanism and which tiers/vault providers are actually supported.
- RBAC/audit-log granularity in Team Edition/CloudBeaver.
- Whether the schema-compare tool's "struggles with nested BSON" characterization is a specific, reproducible finding or a general inference by the secondary source.
