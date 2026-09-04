# Feature Report — TablePlus / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Connectivity
- Feature ID: F-CONN (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: TablePlus
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

TablePlus establishes MongoDB connections using either a full connection URI or individually entered connection parameters, alongside its 15+ other supported engines in the same connection UI (per the source's own framing, TablePlus is a single interface across relational and select NoSQL engines, not a MongoDB-purpose-built client). Once connected, MongoDB collections appear in a left-sidebar "Connection Pool" alongside database tables from any other connected engines, next to a "Saved Snippets" section (per the source's UI-architecture diagram).

Connections can be tagged with a custom color (e.g., red for a production environment). Tagging a connection this way is what triggers Safe Mode — a write-protection behavior documented in the [Governance & Security feature report](../governance/feature-report.md) rather than here, since the color tag is the UI/connectivity-layer mechanism while Safe Mode's enforcement (blocking destructive statements, requiring manual confirmation) is the governance behavior it activates.

The source describes SSH tunneling (password, private key, and SSH Agent authentication modes), SSL encryption, TLS 1.3 transport security, local encrypted credential storage, and biometric (macOS TouchID) device-access locks as TablePlus-wide security capabilities. None of these are stated as MongoDB-specific or MongoDB-excluded — they are described once, in a general "Security, Encryption, & Connection Governance" section covering the whole product, so this report treats their MongoDB applicability as presumed-but-unconfirmed rather than independently verified for the MongoDB connection type.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| CONN-uri-paste | MongoDB connections can be made via URI string or individual parameters. | Standard, low-friction connection setup consistent with most modern MongoDB GUIs. | S1 Section 5 narrative |
| CONN-ssh | SSH tunneling with password/private-key/SSH-Agent modes is described as a product-wide capability. | If it extends to MongoDB (unconfirmed), matches the SSH tunnel depth of specialized MongoDB tools. | S1 Section 10 |
| CONN-color-coding | Connections can be assigned custom tag colors, with red conventionally used for production. | Directly enables the Safe Mode trigger mechanism documented under F-GOV; a real, specific UI behavior, not just a generic "environment label." | S1 Sections 4, 10 |
| CONN-cred-storage | Credentials, hostnames, and access keys are stored locally on encrypted disk storage and never synced to TablePlus's own cloud servers. | A privacy-favorable local-only credential model, consistent with a lightweight, non-cloud-first client architecture. | S1 Section 10 |

## Constraints and risks

- The source's body text has no inline citation markers tying any specific F-CONN claim to a specific Works Cited primary source — every claim above is Unverified rather than Confirmed under this plan's stricter citation discipline, even where the claim is detailed and specific-sounding (e.g., naming three distinct SSH auth modes).
- No claim in the source confirms these connectivity capabilities apply identically to MongoDB as to TablePlus's relational connections; the source's security/connectivity sections are written generically across the whole product.
- Biometric (TouchID) device-access locks are mentioned once, with no existing dictionary sub-feature ID matching "biometric app-level lock" cleanly (closest concept, `CONN-cred-storage`, is about at-rest storage encryption, not an in-app unlock gate) — described here in prose rather than forced into a matrix row, consistent with this plan's guidance to avoid stretching an ID to cover a materially different capability.

## Interactions and dependencies

- Connection color tagging (`CONN-color-coding`) is the trigger mechanism for Safe Mode, documented under [F-GOV](../governance/feature-report.md) (`GOV-protect-mode` / `GOV-readonly-mode`).
- Credential storage interacts with TablePlus's hardware-hash-based device licensing model (documented in `product-report.md`'s pricing/commercial-terms narrative, not itself an F-CONN capability).

## Conclusions

### Strengths

- A real, if not primary-source-confirmed, SSH tunneling, TLS, and local-encrypted-credential-storage story consistent with a security-conscious desktop client.
- Connection color tagging is a specific, real UI mechanism (not just a marketing claim) that feeds directly into an operational-safety behavior (Safe Mode).

### Limitations

- No MongoDB-specific connection wizard is described — MongoDB is one of 15+ generic engine types in the same connection UI, similar in spirit to DBeaver's and DataGrip's generic multi-engine connection surfaces.
- No enterprise authentication (SAML, Kerberos, OIDC), no read-preference or topology-mode controls, and no proxy support are discussed anywhere in the source for TablePlus.

### Unknowns

- Whether SSH tunneling, TLS 1.3, and local credential encryption apply identically to MongoDB connections as to relational connections.
- Full standard-auth mechanism coverage (SCRAM variants, X.509) for MongoDB specifically.
- Whether TablePlus's iOS companion app shares the same connection store/credentials as the desktop client for MongoDB connections specifically.
