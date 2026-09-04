# Feature Matrix — DBeaver / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: DBeaver
- Product group: third-party
- Feature ID: F-GOV (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `governance`
- Analysis date: 2026-09-04
- Version/release context: DBeaver 25.x–26.x line

## Source index

- S1: DBeaver Competitive Intelligence Analysis (secondary research file), `research/google_research/dbeaver-competitive-intelligence-analysis/DBeaver Competitive Intelligence Analysis.md`
- S2: Security restrictions for database connection | DBeaver Documentation, https://dbeaver.com/docs/dbeaver/Managing-security-restrictions-for-database-connection/ (S1 Works Cited #25)
- S3: Schema compare | DBeaver Documentation, https://dbeaver.com/docs/dbeaver/Schema-compare/ (S1 Works Cited #30)
- S4: License types - DBeaver PRO, https://dbeaver.com/license-types/ (S1 Works Cited #16); Differences between license types · GitHub wiki (S1 Works Cited #18, #19)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-readonly-mode | Read-only mode | Confirmed | S1: "Connection Security Restrictions: Administrative toggles that enforce client-side constraints on individual connections, including read-only modes, prohibiting data editing, blocking structural DDL alterations, restricting script execution, and blocking external data imports." Backed by a dedicated DBeaver documentation page (S2). | Client-side (UI) enforcement — S1 does not claim server-side enforcement. | Unverified | S1, S2 | Also tracked as `CONN-readonly-lock` in the [Connectivity feature matrix](../connectivity/feature-matrix.md) since it is a per-connection toggle; listed here too because it is a governance control in substance. |
| GOV-secrets-vault | External secrets manager integration | Unverified — per secondary source, no primary citation | S1: "Secret Managers and Credential Storage: Master password keystore encryption paired with enterprise secret manager integrations, including HashiCorp Vault, CyberArk, and AWS Secrets Manager." Also listed among 2021–2026 milestones: "Introduced read-only security toggles, updated Kerberos/SSO integration, and added native secret manager connections (HashiCorp Vault, AWS Secrets Manager, CyberArk) to prevent local plaintext credential storage." | No specific DBeaver documentation page for secrets-manager integration is present in S1's Works Cited list. | Unverified | S1 | This is the DBeaver capability that is the direct evidentiary basis for the new dictionary ID `GOV-secrets-vault` added in this same effort (2026-09-04) — its existence in the dictionary does not itself make the claim Confirmed for DBeaver; it remains Unverified per the citation rule. |
| GOV-collection-compare | Collection compare | Confirmed (existence, DDL-oriented); Unverified (BSON-handling assessment) | S1: "Data Comparison and Synchronization | Relational DDL Schema Compare... DBeaver's compare engine struggles with nested BSON arrays/documents." Backed by a dedicated DBeaver documentation page (S3) confirming the compare feature exists. | Relational-DDL-first design; the "struggles with nested BSON" characterization is the secondary source's own assessment, not independently re-verified here. | Unverified (BSON-handling severity) | S1, S3 | Imperfect-fit mapping: DBeaver's compare is structure/DDL-first, while the dictionary's `GOV-collection-compare` description is "field-level diff comparison between collections" (more data-centric). Flagged here as the closest existing ID rather than minting a new one for a single thin data point — see the product-report.md "Open questions" section. |
| CONN-auth-enterprise | Enterprise auth (cross-referenced) | Confirmed (existence + edition gating) | See [Connectivity feature matrix](../connectivity/feature-matrix.md) for full detail; included here because enterprise SSO/identity federation is a governance-relevant control. | Gated to paid tiers. | Unverified (MongoDB-specific scope) | S1, S4 | Primary row lives in F-CONN; cross-referenced here for governance completeness. |

## Feature-level conclusion

### Confirmed strengths

- Per-connection read-only/write-restriction toggle backed by a dedicated DBeaver documentation page.
- Schema/structure compare capability confirmed to exist via a dedicated DBeaver documentation page, even though its BSON-handling quality is only the secondary source's own (unverified) assessment.
- Enterprise auth protocol breadth (SAML, Kerberos, Azure AD) confirmed via two independent primary-source citations in the research file (DBeaver's own licensing pages).

### Confirmed limitations

- No specific primary source backs the external secrets-manager integration (HashiCorp Vault, CyberArk, AWS Secrets Manager) claim — a real, plausible capability, but Unverified per this repository's stricter citation rule.
- No RBAC, audit-log, or platform-governance detail is discussed in the source beyond a brief, unspecific mention of Team Edition/CloudBeaver RBAC "tied to corporate directory services" — too vague to include as its own matrix row with confidence.

### Open questions / unknowns

- Exact secrets-manager integration mechanism (per-connection configuration, supported vault versions/auth modes) — not detailed in the source.
- Whether GOV-collection-compare's "struggles with nested BSON" characterization reflects a specific, reproducible limitation or a general architectural inference by the secondary source's author.
- RBAC/audit-log depth for DBeaver Team Edition/CloudBeaver — mentioned only in passing, not detailed enough for a confident matrix row.
