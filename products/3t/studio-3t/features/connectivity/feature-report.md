# Feature Report — Studio 3T / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers the full connection lifecycle in Studio 3T: topology targeting, connection setup methods, authentication mechanisms (standard and enterprise), TLS/SSL configuration, SSH tunneling, proxy support, advanced driver parameters, connection organization, team sharing, and credential storage.

## Behavioral walkthrough

Studio 3T's Connection Manager is the central hub for all MongoDB connection definitions. Connections can be created by pasting a URI (which auto-populates all tabs), by importing from Robo 3T/Robomongo or NoSQLBooster (including SSH credentials), or by manual tab-by-tab entry. Every connection stores topology type, authentication, TLS, SSH, proxy, and advanced driver options as a named entity.

Authentication spans eight mechanisms split by edition. The Free tier covers SCRAM-SHA-256, SCRAM-SHA-1, X.509, and anonymous access — sufficient for most self-managed and Atlas deployments. Enterprise mechanisms (Kerberos, LDAP, AWS IAM, MongoDB OIDC) are locked to the Ultimate edition, which aligns with the enterprise IT buyer rather than the individual developer. OIDC adds two additional toggles (endpoint trust and token type) that reflect the complexity of OIDC in MongoDB's implementation.

TLS configuration is thorough: multiple CA trust modes, client certificate support, SNI override, and an "allow invalid hostnames" toggle (with the implicit risk that creates). SSH tunneling supports both password and private-key auth. SSH Profiles are a notable productivity feature — a single profile update propagates new credentials to all connections assigned to that profile, avoiding the problem of stale SSH passwords across many saved connections.

Proxy configuration is per-connection, supporting HTTP and SOCKS modes alongside a global app-level proxy setting. This three-level approach (no proxy / app default / custom) is more granular than most competing tools.

Color-coding connections by environment is a low-effort but high-value safety guard — a visually obvious production indicator in every tab header. Shared folders with granular permissions (Manage / Edit / View) enable team-level connection sharing without credential distribution.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| CONN-001 | All four MongoDB topologies (Standalone, Replica Set, Sharded, DNS Seedlist) are fully supported with read preference and tag configuration. | Broad compatibility with Atlas and self-managed deployments. |
| CONN-004 | Robo 3T / Robomongo and NoSQLBooster import (including SSH credentials) reduces onboarding friction for users migrating from those tools. | Lowers migration barrier from competing tools. |
| CONN-006 | Enterprise auth (Kerberos, LDAP, AWS IAM, OIDC) gated to Ultimate edition. | Enterprise auth coverage is complete but carries a hard edition paywall. |
| CONN-008 | SSH Profiles with profile-level password updates propagating to all assigned connections is a significant operational convenience. | Reduces credential hygiene burden in multi-connection SSH environments. |
| CONN-011 | Color-coding per connection is visual-only and does not enforce access policies. | Useful signal but not a security control — read-only lock (CONN-013) is the enforcement layer. |
| CONN-014 | Cryptographic key store (master password mode) provides strong local encryption; previous plaintext files are deleted on migration. | Meaningful improvement over default built-in-key encryption for security-conscious users. |

## Constraints and risks

- Enterprise authentication (Kerberos, LDAP, AWS IAM, OIDC) requires the Ultimate edition — teams on Free or Pro/Base are excluded from enterprise IdP integrations.
- "Accept any certificate" and "Allow invalid hostnames" TLS options, if used in production, create man-in-the-middle exposure.
- Shared folders share connection definitions but credentials must still be managed; permission model (Manage/Edit/View) is UI-level and does not propagate to MongoDB server-side RBAC.
- Read-only connection lock is enforced at the UI layer only — it does not restrict permissions at the MongoDB driver or server level.
- Exact edition tier names are **unknown/unverified** (pricing page returned 404 at analysis time).

## Conclusion

Connectivity is a strong feature area for Studio 3T. The combination of URI-paste onboarding, broad authentication coverage, SSH profile management, granular proxy options, and environment color-coding covers most real-world MongoDB deployment patterns. The edition-gating of enterprise auth mechanisms is the primary friction point for enterprise adoption at non-Ultimate tiers.
