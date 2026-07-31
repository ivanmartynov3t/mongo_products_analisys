# Feature Report — Studio 3T / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

**Last reviewed:** 2026-07-31 — see [research findings](../../../../../research/studio-3t-desktop-review-2026/01-connectivity-findings.md)

## Scope

This report covers the full connection lifecycle in Studio 3T: topology targeting, connection setup methods, authentication mechanisms (standard and enterprise), TLS/SSL configuration, SSH tunneling, proxy support, advanced driver parameters, connection organization, team sharing, credential storage, and (new in this revision) Session Restore, Git-backed local connection sharing, and 3T Access Manager connection-tree integration.

## Edition names (corrected 2026-07-31)

A source-code audit of `utils/Edition.java` resolves the edition-tier naming that was previously unverified in this report: the five editions and their **display names** are **Free**, **Community Edition** (the `ROBO` enum value), **Professional** (the `PROFESSIONAL`/`CORE`/`PRO` enum values, which are aliases for the same tier and feature set), and **Ultimate** (the `ENTERPRISE` enum value). There is no separately named "Pro/Base" tier. All edition references below use these corrected names.

## Behavioral walkthrough

Studio 3T's Connection Manager is the central hub for all MongoDB connection definitions. Connections can be created by pasting a URI (which auto-populates all tabs), by exporting the current form back out to a URI, by importing from Robo 3T/Robomongo, NoSQLBooster, MongoVue, **or MongoDB Compass** (a fourth import source confirmed by source-code audit, previously undocumented) — including SSH credentials — or by manual tab-by-tab entry. Every connection stores topology type, authentication, TLS, SSH, proxy, and advanced driver options as a named entity.

Authentication spans eight mechanisms split by edition. Free and Community Edition cover SCRAM-SHA-256, SCRAM-SHA-1, X.509, and anonymous access — sufficient for most self-managed and Atlas deployments. Enterprise mechanisms (Kerberos, LDAP, AWS IAM, MongoDB OIDC) are locked to the **Ultimate** edition only — Free, Community Edition, and Professional are all excluded — which aligns with the enterprise IT buyer rather than the individual developer. OIDC adds endpoint-trust and token-type toggles, plus (added within the last 24 months) a nonce parameter for CSRF hardening and a local-callback flow that keeps authentication working in offline environments.

TLS configuration is thorough: multiple CA trust modes, client certificate support, SNI override, and an "allow invalid hostnames" toggle (with the implicit risk that creates). A previously undocumented nuance: hostname validation is **also** implicitly bypassed whenever an SSH tunnel is used, independent of that toggle (see Constraints and risks below).

SSH tunneling supports both password and private-key auth in every edition. **SSH Profiles — the reusable, named credential layer where one profile update propagates to all assigned connections — are gated to Professional and Ultimate editions**, a correction from the previous "all editions" characterization; Free and Community Edition users only get the basic per-connection tunnel, not the profile-management convenience layer. No jump-host/bastion/multi-hop SSH support was found in source.

Proxy configuration is per-connection, supporting HTTP and SOCKS modes alongside a global app-level proxy setting, in all editions. This three-level approach (no proxy / app default / custom) is more granular than most competing tools, and now extends beyond MongoDB/SQL connections to the app's own outbound HTTPS traffic — for example, AI Helper's connection to Anthropic Claude can be routed through the same proxy configuration.

Connection organization has two previously conflated layers: **folder grouping is available in every edition**, but **color-coding per connection (applied to tabs, including shared Team-Sharing connections) is gated to Professional and Ultimate** — a correction from the prior "all editions" description. Shared folders (Team Sharing) with granular permissions (Manage / Edit / View) enable team-level connection sharing without credential distribution, also Professional+.

The read-only connection lock — previously documented as available in all editions — is itself Professional/Ultimate-gated at the user-toggle level. Separately, a **forced read-only lock** exists independent of that per-connection setting: connections governed by 3T Access Manager, and connections shared via Team Sharing at "Viewer" permission, are forced read-only regardless of edition or the user's own toggle. This forced-lock mechanism, along with a broader set of 3T Access Manager restrictions on the connection tree (blocked duplicate/export/edit/drag-drop, disabled coloring and quick-connect for AM-governed connections), is a real, shipped cross-product integration point with no prior documentation in this report.

Two further undocumented capabilities were confirmed by source-code audit:

### Session Restore (Professional+, pending dictionary addition as `CONN-session-restore`)

The app can automatically reopen every connection and tab that was open at last shutdown, on next launch. This is togglable in Behavior preferences, has its own keyboard shortcut, and is gated to Professional and Ultimate editions (`AppFeatures.SESSION_RESTORE`). It shipped as "enabled by default" per the product changelog.

### Git-backed local connection-library sharing (all editions found gating on; pending dictionary addition as `CONN-git-repo-sharing`)

Distinct from cloud-based Team Sharing, Studio 3T also supports a local folder of connection XML files that can optionally be a Git working tree, with in-app Git actions (add remote, fetch, push, pull, reset-and-sync) and a UI badge showing fetched-but-unmerged commit count. This gives teams an ongoing, version-controlled, syncable storage backend for shared connections as an alternative to the cloud-mediated Team Sharing folder model, without requiring a hosted service.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| CONN-topology | All four MongoDB topologies (Standalone, Replica Set, Sharded, DNS Seedlist) are fully supported with read preference and tag configuration. | Broad compatibility with Atlas and self-managed deployments. |
| CONN-import-clients | Robo 3T / Robomongo, NoSQLBooster, MongoVue, **and MongoDB Compass** import (including SSH credentials) reduces onboarding friction for users migrating from those tools. | Lowers migration barrier from competing tools; broader than previously documented (Compass added). |
| CONN-auth-enterprise | Enterprise auth (Kerberos, LDAP, AWS IAM, OIDC) gated to the **Ultimate** edition only. | Enterprise auth coverage is complete but carries a hard edition paywall reaching all the way down through Professional. |
| CONN-ssh | Basic SSH tunneling is available in every edition; **SSH Profiles (reusable credentials with propagating password updates) are gated to Professional+**, a correction from the prior undifferentiated "all editions" claim. | Free/Community Edition users get tunnel connectivity but not the credential-hygiene convenience layer. |
| CONN-color-coding | Color-coding is **gated to Professional+**, not "all editions" as previously stated; folder grouping itself remains available to all editions. | Free/Community Edition users lose the visual production/test safety cue; still get organizational folders. |
| CONN-readonly-lock | The user-toggled read-only lock is Professional+-gated; a separate, edition-independent **force-lock** applies to Access-Manager-governed and Team-Sharing "Viewer" connections. | The most consequential correction in this revision — the enforcement layer is more complex than a single "all editions" toggle. |
| CONN-cred-storage | Cryptographic key store (master password mode) provides strong local encryption via a three-generation AES fallback chain (GCM primary, CBC/ECB legacy decrypt paths); previous plaintext files are deleted on migration. No OS-native credential store (Keychain/Credential Manager/libsecret) is used for connection passwords specifically. | Meaningful improvement over default built-in-key encryption for security-conscious users; the OS-credential-store gap should be weighed against competitors that use native OS secret storage. |
| CONN-compat-ferretdb | studio3t.com lists FerretDB as a compatible database alongside MongoDB, DocumentDB, and Cosmos DB; corroborated by a third-party FerretDB blog post. Source-code audit found **no FerretDB-specific code** — compatibility is a byproduct of generic MongoDB-wire-protocol support, not a dedicated integration. | Widens Studio 3T's addressable use cases, but readers should not infer first-class/dedicated FerretDB support. |
| CONN-compat-redis | **Correction 2026-07-31:** no Redis-specific compatibility code, detection, or special-casing exists anywhere in the source. This capability should be treated as unverified/likely-erroneous pending re-check of its original source. | Any customer-facing claim of Redis compatibility should not be repeated until re-verified; it is not corroborated by the codebase. |

## Constraints and risks

- Enterprise authentication (Kerberos, LDAP, AWS IAM, OIDC) requires the **Ultimate** edition — teams on Free, Community Edition, or Professional are excluded from enterprise IdP integrations.
- "Accept any certificate" and "Allow invalid hostnames" TLS options, if used in production, create man-in-the-middle exposure. **Additionally, hostname validation is implicitly bypassed whenever an SSH tunnel is used, regardless of the "Allow invalid hostnames" toggle** — this is undocumented behavior surfaced by the source-code audit and should be called out explicitly in customer-facing security guidance.
- Shared folders share connection definitions but credentials must still be managed; permission model (Manage/Edit/View) is UI-level and does not propagate to MongoDB server-side RBAC.
- Read-only connection lock (the user-toggled variant) is enforced at the UI layer only — it does not restrict permissions at the MongoDB driver or server level. A separate forced-lock path (Access-Manager-governed and Team-Sharing "Viewer" connections) is also UI-level only.
- No OS-native credential store (Keychain, Windows Credential Manager, libsecret) is used for connection passwords — only the app's own AES-GCM/master-password keystore. (Cross-reference: if F-GOV's `GOV-cred-storage-os` entry is asserted for Studio 3T Desktop's connection credentials specifically, that would conflict with this finding and should be reconciled with the F-GOV team.)
- Whether a stored-connection-count limit is still enforced for Free-tier users is **unknown/unverified** — the `AppFeatures.MANAGE_UNRESTRICTED_NUMBER_OF_CONNECTIONS` flag exists in every edition's flag set with no located enforcement call site in the current codebase, despite a historical Free-tier limit having been added (`ROBO-110`).
- Edition tier names, previously flagged as unknown/unverified pending a working pricing page, are now resolved from source (`Edition.java`): **Free / Community Edition / Professional / Ultimate**. There is no separate "Pro/Base" display name.

## Conclusion

Connectivity is a strong feature area for Studio 3T. The combination of URI-paste onboarding, broad authentication coverage, SSH tunneling and profile management, granular proxy options, environment color-coding, Session Restore, and Git-backed connection sharing covers most real-world MongoDB deployment patterns. The edition-gating of enterprise auth mechanisms to Ultimate only is the primary friction point for enterprise adoption at non-Ultimate tiers, and this revision surfaces several previously undocumented Professional-tier gates (SSH Profiles, color-coding, the read-only lock toggle) that materially narrow what Free and Community Edition users actually get relative to the prior "all editions" characterization. The 3T Access Manager connection-tree integration (forced read-only lock, restricted duplicate/export/edit/drag-drop for AM-governed connections) is a newly documented cross-product integration point that should be tracked jointly with F-GOV.
