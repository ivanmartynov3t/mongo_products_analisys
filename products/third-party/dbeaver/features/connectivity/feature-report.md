# Feature Report — DBeaver / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Connectivity
- Feature ID: F-CONN (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: DBeaver
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

DBeaver connects to MongoDB through a dedicated NoSQL driver entry in its Driver Manager, available only in paid editions (Lite, Enterprise, Ultimate). The connection wizard for MongoDB is one instance of DBeaver's generic, engine-agnostic connection UI (shared across its 100+ supported engines), rather than a MongoDB-purpose-built wizard. Once connected, MongoDB collections surface in DBeaver's Database Navigator tree alongside relational schemas/tables from any other connected engines, and are queried through the generic SQL Console (see the [SQL Tools feature report](../sql-tools/feature-report.md)) rather than a document-native filter bar.

Enterprise-tier connections can additionally authenticate via SAML 2.0, Kerberos, or Microsoft Entra ID (Azure AD), and can source credentials from an external secrets manager (HashiCorp Vault, CyberArk, AWS Secrets Manager) instead of DBeaver's local encrypted keystore — see the [Governance & Security feature report](../governance/feature-report.md) for the secrets-manager integration itself. Administrators can also apply per-connection security restrictions (read-only mode, blocking DDL/script execution/data import) documented in DBeaver's own "Managing security restrictions for database connection" page.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| CONN-auth-enterprise | SAML/Kerberos/Azure AD auth exist as a DBeaver-wide capability, gated out of the free Community Edition. | Enterprise buyers needing SSO must upgrade to a commercial tier even for basic MongoDB access. | Research file narrative + S1 Works Cited #16, #18, #19 |
| CONN-readonly-lock | Per-connection client-side write-restriction toggle, with a dedicated vendor documentation page. | Matches Studio 3T's own per-connection read-only lock concept; a real, evidenced parity point rather than a marketing claim. | Research file narrative + S1 Works Cited #25 |
| CONN-cred-storage | Local master-password keystore is the baseline credential store; external secrets-manager integration is a separate, higher-tier capability. | Two-tier credential model (local vs. externally managed) — see F-GOV for the secrets-vault capability itself. | Research file narrative |

## Constraints and risks

- MongoDB connectivity requires a paid DBeaver tier — this is a structural gate on the entire F-CONN surface for MongoDB users, unlike Compass or Studio 3T Community, which both offer some free MongoDB connectivity.
- The research file does not confirm whether DBeaver's enterprise-auth and secrets-manager features work against MongoDB connections specifically (as opposed to relational connections only) — treat any claim to the contrary as unverified.

## Interactions and dependencies

- Shares the underlying JDBC/NoSQL driver architecture with [F-SQL](../sql-tools/feature-report.md) — MongoDB collections reached via a DBeaver connection are queried through the SQL Console, not a separate document browser.
- Credential handling connects to [F-GOV's external secrets-manager integration](../governance/feature-report.md) (GOV-secrets-vault).

## Conclusions

### Strengths

- Enterprise identity protocol breadth (SAML, Kerberos, Azure AD, cloud IAM) is real and independently corroborated by DBeaver's own licensing documentation.
- A dedicated, per-connection read-only/write-restriction toggle is confirmed via DBeaver's own documentation.

### Limitations

- No MongoDB-specific connection wizard; MongoDB is one of 100+ generic engine types in the same UI.
- Free Community Edition has zero MongoDB connectivity — a materially different starting point than Compass (fully free) or Studio 3T (free Community tier with limited MongoDB access).

### Unknowns

- Exact standard-auth mechanism list (SCRAM variants, X.509) for MongoDB connections specifically.
- Whether SSH tunneling, proxy support, or mongodb+srv:// URI paste are available for MongoDB connections (not discussed in the source material).
