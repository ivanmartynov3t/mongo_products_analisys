# Feature Matrix — TablePlus / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: TablePlus
- Product group: third-party
- Feature ID: F-CONN (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `connectivity`
- Analysis date: 2026-09-04
- Version/release context: 2026 release line

## Source index

- S1: TablePlus Competitive Intelligence Analysis (secondary research file, no inline per-claim citation markers — only an end-of-file Works Cited list), `research/google_research/tableplus-competitive-intelligence-analysis/TablePlus Competitive Intelligence Analysis.md`
- S1 Works Cited #5: TablePlus Documentation: Overview, https://docs.tableplus.com/ (general vendor documentation, not fetched independently for this matrix)
- S1 Works Cited #12: TablePlus pricing, https://tableplus.com/pricing (directly backs Section 2's pricing/licensing table)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONN-uri-paste | URI auto-fill | Unverified — per secondary source, no primary citation | S1: "TablePlus allows developers to establish secure connections to MongoDB clusters using standard URI strings or individual connection parameters." | — | Unverified | S1 | Existence of URI-based connection is stated narratively; the source does not confirm auto-fill/parse behavior specifically. |
| CONN-auth-std | Standard auth | Unverified — per secondary source, no primary citation | Not itemized for MongoDB specifically anywhere in S1 (no mention of SCRAM/X.509 mechanisms). | — | Unverified | S1 | Omitted from confident claims; only generic "individual connection parameters" is mentioned. |
| CONN-ssh | SSH tunnel | Unverified — per secondary source, no primary citation | S1 (Section 10): "Native Network Encryption and Tunneling: Includes native support for SSH Tunneling (supporting password, private key, and SSH Agent authentication)." | Described as a TablePlus-wide capability, not confirmed MongoDB-specific in the source. | Unverified | S1 | Existence is stated with specific auth-mode detail (password/private key/SSH Agent), a stronger claim than a bare mention, but not tied to a Works Cited primary source for this specific detail. |
| CONN-tls | TLS/SSL config | Unverified — per secondary source, no primary citation | S1 (Section 10): "SSL encryption, and TLS 1.3 network transport security." | Not confirmed MongoDB-specific (vs. TablePlus-wide). | Unverified | S1 | — |
| CONN-cred-storage | Credential storage | Unverified — per secondary source, no primary citation | S1 (Section 10): "Local Credential Encrypted Storage: Database credentials, hostnames, and access keys are stored locally on the user's encrypted disk storage. Credentials are never synchronized to TablePlus cloud servers." | Vendor reportedly collects only user email and a one-way hashed hardware ID for license verification (per S1). | Unverified | S1 | A specific, detailed claim, but the source's body text carries no inline citation marker tying it to a specific Works Cited entry. |
| CONN-color-coding | Color coding | Unverified — per secondary source, no primary citation | S1 (Section 4 and Section 10): "Safe Mode and Tagging Controls: Allows database connections to be assigned custom tag colors (e.g., Red for Production)... Environment Tagging and Safe Mode: Connections tagged with high-risk environment colors... automatically enforce Safe Mode." | Tagging a connection as high-risk (e.g., red) is what triggers Safe Mode — see [F-GOV](../governance/feature-matrix.md) for the Safe Mode mechanism itself. | Unverified | S1 | Cross-referenced with `GOV-protect-mode`/`GOV-readonly-mode` in the governance matrix — this ID covers the tagging/coloring UI itself. |
| CONN-portability | Import/export configs | Unverified — per secondary source, no primary citation | S1 (Section 11): "Exportable Workspace Configurations: Developers can export visual connection tags, custom color themes, and metric dashboard layouts to JSON files for team sharing." | Described as workspace/team-sharing configuration export, not confirmed to include full per-connection credential export. | Unverified | S1 | — |
| CONN-multi-active | Multiple active | Unverified — per secondary source, no primary citation | S1 (Section 4): "Multi-Tab Workspace Layouts: Supports horizontal and vertical split screen orientations, allowing developers to execute queries against multiple connections simultaneously." | — | Unverified | S1 | — |
| CONN-sidebar-ops | Sidebar operations | Unverified — per secondary source, no primary citation | S1's UI layout diagram (Section 6) shows a "Connection Pool" sidebar section with database tables, collections, and saved snippets, implying standard connect/browse sidebar operations. | Not itemized feature-by-feature (favorite, duplicate, refresh, etc.) in the source. | Unverified | S1 | Inferred from the UI architecture diagram rather than an explicit feature list entry. |

## Feature-level conclusion

### Confirmed strengths

- None of TablePlus's F-CONN capabilities clear this repository's "Confirmed" bar for MongoDB specifically: the source's body text carries no inline per-claim citation markers, so even detailed, specific-sounding claims (SSH auth modes, local encrypted credential storage) default to Unverified per this plan's stricter-than-usual citation rule. The pricing/licensing terms in the product-report.md (a distinct topic from F-CONN) are the source's one area with a clear, traceable Works Cited match (#12, tableplus.com/pricing).

### Confirmed limitations

- None stated as explicit confirmed-absences for F-CONN specifically — the source does not describe TablePlus's connectivity layer as lacking anything for MongoDB; it simply does not itemize MongoDB-specific auth-mechanism or topology depth.

### Open questions / unknowns

- Full standard-auth mechanism list (SCRAM-SHA-256/1, X.509, Kerberos, LDAP, OIDC) supported for MongoDB connections specifically.
- Whether replica-set/sharded-cluster/DNS-seedlist (`mongodb+srv://`) topology selection is supported as a distinct connection-wizard concept, or only as a raw URI string a user must construct themselves.
- Whether SSH tunneling, TLS 1.3, and local encrypted credential storage — all stated as TablePlus-wide capabilities — apply identically to MongoDB connections, or only to its relational connections.
- TouchID/biometric device-access locks (Section 10) are stated as a TablePlus-wide capability; not itemized elsewhere in the dictionary under F-CONN and not scored here as a separate sub-feature since no existing ID matches "biometric app-level lock" cleanly — noted in the feature report's prose instead.
