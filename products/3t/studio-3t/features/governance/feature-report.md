# Feature Report — Studio 3T / Governance Platform

**Last reviewed:** 2026-07-31 — see [research findings](../../../../../research/studio-3t-desktop-review-2026/10-governance-findings.md)

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

As of 2026-07-29, this report no longer covers the governance-tier products directly — they have each been split into their own product folder under `products/3t/` with an independent product report and feature report:

- [3T Lens](../../../3t-lens/features/governance/feature-report.md) — governed data workspace (centralized connection management, compliance policy templates, PII classification, versioned field history, MCP integration)
- [3T Access](../../../3t-access/features/governance/feature-report.md) — identity and governance plane (RBAC, audit trail, pre-login access scoping)
- [3TL Bridge](../../../3tl-bridge/features/governance/feature-report.md) — CDC pipeline engine (Transform Studio, PII masking, security/identity, deployment/scaling)
- [3T Explore](../../../3t-explore/features/governance/feature-report.md) — the governance-relevant aspects (Workspace Switcher, Access Control) of the browser IDE product

Previously, this report treated all four as a single "governance platform tier" of Studio 3T. Per studio3t.com, 3T Explore, the Desktop IDE, and 3T MCP make up the "Build" track; 3TL Bridge is the "Pipeline" track; 3T Lens and 3T Access are the "Governed Access" track — three separate tracks, five separate products (excluding the Desktop IDE itself), now documented independently.

This report's remaining scope is the Studio 3T Desktop IDE's own native governance capabilities, now covered below following a 2026-07-31 source-code audit (`product-suite/data-man-mongodb-ent/src/main/java/t3/`, branch `KONG-11077-No-scroll-bar-on-linux-2`, commit `435d6844a3a`) — see the [feature matrix](feature-matrix.md) for the full sub-feature table and the [research findings](../../../../../research/studio-3t-desktop-review-2026/10-governance-findings.md) for the underlying evidence. Comparison reports already reference `GOV-readonly-mode`, `GOV-rbac-users`, `GOV-rbac-roles`, `GOV-audit-log`, `GOV-collection-compare`, `GOV-collection-sync`, `GOV-data-masking`, and `GOV-cred-protection` against this product; those references are unaffected by the 2026-07-29 product split, but several are narrower or materially corrected by this audit (see below).

## Behavioral walkthrough

See the linked per-product reports above for full behavioral detail on 3T Lens, 3T Access, 3TL Bridge, and 3T Explore's governance surface. In summary: 3T Access is the shared identity/permission plane; 3T Lens is the browser-based governed workspace built on top of it (connection governance, compliance, PII classification); 3TL Bridge is the CDC pipeline engine with pipeline-layer PII masking; and 3T Explore extends the same access-scoping model to a browser IDE surface via its Workspace Switcher and 3T Access Manager integration.

For the Desktop IDE itself, the governance surface breaks into: MongoDB server-side RBAC management (users, roles, inheritance, privilege tree — Professional tier and above); a read-only connection lock (Professional tier and above); a rule-based data-masking engine for export (Ultimate edition only, no PII classification); collection compare/sync; and a set of admin-only enterprise controls (network-policy kill switch, telemetry opt-out, AI Helper disable, startup policy) that are Windows registry/Group Policy/installer-manifest driven rather than a cross-platform config file.

### Audit logging — corrected scope

The Desktop IDE's audit-logging capability is real but substantially narrower than previously documented, and is not the "track queries, modifications, and connections" capability the dictionary description implies:

- **Local Connection Manager audit trail (shipped):** `t3.utils.connman.ConnectionManagerLogger` writes a tamper-evident, MD5-chained local `audit.log` file (5MB rotation) recording only Connection Manager actions — creating, editing, deleting, duplicating, or importing a connection or folder — with ISO timestamp, OS username, hostname, and success/failure outcome. It does **not** log queries, aggregations, or document modifications of any kind. It is **off by default** and can only be turned on via Windows Group Policy/registry (`WriteAuditLog` key) or an installer manifest setting — there is no in-app toggle and no macOS/Linux equivalent activation path found in the source.
- **3T Access HTTP audit sender (unshipped scaffolding):** `t3.auditlogging.AuditEventSender`/`AuditEvent`/`AuditRecord`, added 2026-06-03 (KONG-11032), is a fully-built component that would POST a rich audit event (actor identity, resource, action, session, project, source IP) to a 3T Access audit endpoint. A repo-wide search found **zero call sites** for it anywhere in the codebase — it is not invoked from any UI action, menu item, or connection lifecycle event. It also requires the user to be logged into 3T Access to function. This should be read as a **roadmap signal** (the team is building toward centralized audit trails routed through 3T Access) rather than a shipped Desktop IDE capability, and should not be cited as evidence that Studio 3T Desktop currently sends audit events anywhere.

Net effect: any claim that Studio 3T Desktop provides query- or document-modification-level audit logging is not supported by the source. The only shipped mechanism covers Connection Manager housekeeping actions, is disabled out of the box, and is Windows-only to enable centrally.

### Credential storage — corrected mechanism

Previously described (via `GOV-cred-storage-os`) as an "OS-level credential API (Keytar/AES-256)." The actual mechanism, `t3.utils.security.EncryptionManager`, is a **local, file-based BouncyCastle "UBER" keystore**, master-password-protected, storing a 256-bit AES key (current cipher AES/GCM, with legacy AES/CBC and AES/ECB decryption paths kept for backward compatibility). No integration with macOS Keychain, Windows Credential Manager, libsecret, or the `Keytar` library was found anywhere in the source tree. The AES-256 encryption claim is accurate; the "OS-level credential API" framing is not — credentials are protected by an application-managed keystore file, not a platform credential store.

### Startup policy — corrected mechanism

Previously described (via `GOV-startup-policy`) as an "EJSON/YAML config setting immutable startup behavior." No EJSON or YAML startup-policy file exists in the source tree. The real mechanism is a **Windows-only, Enterprise("Ultimate")-edition-only** Group Policy/registry scheme (`t3.utils.grouppolicy.EnterpriseGroupPolicyStorage`), falling back to per-machine registry settings, falling back to JAR-manifest attributes. This is a real, enterprise-admin-controlled mechanism, but it is not a portable config-file format — it is Windows-registry/manifest based and does not apply on macOS or Linux.

### Other corrections

- **`GOV-cli-policy`** is absent: the Desktop IDE recognizes exactly one CLI flag (`--log-licenses`), unrelated to governance. This looks like a carry-over from MongoDB Compass, which does have CLI-based enterprise policy enforcement.
- **`GOV-protect-mode`** has no distinct supporting code in the source tree — everything found maps to the same `AppFeatures.READ_ONLY_LOCK` mechanism as `GOV-readonly-mode`. Flagged as a likely duplicate/alias rather than removed, pending confirmation with the original documenter.
- **`GOV-isolated-edition`** is absent for Studio 3T — the only "Isolated Edition" string found is a MongoDB Compass install-path detector used for connection import, not a Studio 3T build variant.
- **`GOV-cred-protection`** is real but is two narrower, separate mechanisms rather than a single "Protect Mode": a `DisableShowPassword` registry flag suppressing the password-reveal toggle, and a 3T-Access-scoped copy/export restriction (`RestrictionLevel`) that only applies to 3T Access-managed connections.

### Confirmed as accurate (kept as-is)

- Ultimate-edition gating of Kerberos/LDAP/AWS IAM/OIDC authentication, with real enforcement (connections can be created/edited/tested on lower tiers but not used to connect).
- `GOV-network-policy` outbound-traffic kill switch (`DisableExternalRequests`), blocking all non-database HTTP traffic when enabled.
- Telemetry controls (admin registry switch plus a user-facing Preferences toggle).
- MongoDB server-side RBAC (`GOV-rbac-users`, `GOV-rbac-roles`, `GOV-rbac-inheritance`, `GOV-rbac-tree`), Professional tier and above (not Ultimate-restricted).
- Data masking: a mature, Ultimate-gated, rule-based field-substitution engine with no PII auto-classification and no compliance-policy-template concept in the Desktop IDE — those concepts remain correctly scoped to 3T Lens and 3TL Bridge.

## Constraints and risks

- 3T Lens, 3T Access, and 3TL Bridge are separate deployable products — not features of the Desktop IDE. They require infrastructure provisioning and are likely separately priced (**unknown/unverified** pricing).
- Integration between 3T Lens centralized connections and the Desktop IDE connection manager is not explicitly documented — it is unverified whether Desktop IDE users can consume 3T Lens-managed connections seamlessly.
- The Desktop IDE's audit-logging capability is materially weaker than "audit logging" typically implies in a governance/compliance context: it is off by default, Windows-GPO-only to enable, covers only Connection Manager housekeeping actions, and has no query- or document-level trail. Enterprise buyers evaluating Studio 3T Desktop against a compliance/audit requirement should not assume query-level audit coverage exists.
- The `AuditEventSender` HTTP audit sender to 3T Access is unwired scaffolding as of this audit — it should not be cited in customer-facing or compliance material as a shipped capability.
- Credential storage is a local encrypted keystore file (BouncyCastle/AES), not an OS-native credential store — relevant to any claim about OS-level secret management.
- Startup/enterprise policy enforcement (network policy, telemetry, startup policy, audit-log enablement, AI Helper disable) is Windows-only (registry/Group Policy/installer manifest) — there is no equivalent centrally-managed enforcement path found for macOS or Linux in this source tree.

## Conclusion

The Studio 3T governance platform is architecturally ambitious: a three-product tier (3T Lens + 3T Access + 3TL Bridge) covering connection governance, identity management, audit trails, schema versioning, PII classification, CDC pipelines, and compliance-aware data movement, plus 3T Explore extending the same access model to a browser IDE. The design principle of applying the same access policies to AI agents and human users is noteworthy and positions the platform for enterprise AI governance use cases. As of 2026-07-29 each of these products is documented in its own folder — see the links in Scope above for full detail.

Within the Desktop IDE itself, a 2026-07-31 source-code audit found the core governance mechanisms (read-only lock, MongoDB server-side RBAC, data masking, network-policy kill switch, telemetry controls) to be real and accurately scoped, but found several previously-documented capabilities to be either narrower than described or not present at all: audit logging covers only Connection Manager housekeeping (not queries or document changes) and is off by default; credential storage is a local encrypted keystore rather than an OS credential API; startup policy is a Windows registry/manifest scheme rather than an EJSON/YAML config file; and CLI-based policy enforcement, a distinct "Protect Mode," and a Studio-3T-specific "Isolated Edition" were not found in the source at all. These corrections should be treated as materially relevant to any downstream claim about Studio 3T Desktop's audit or compliance completeness (see the product report and comparison reports, which are out of scope for this file to edit directly). The main caveat on the platform tier remains that 3T Lens/3T Access/3TL Bridge are separate deployments, not Desktop IDE features — their adoption implies infrastructure investment beyond the Desktop IDE.
