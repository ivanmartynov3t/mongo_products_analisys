# VisuaLeaf — Security & Governance Feature Report

## Summary

VisuaLeaf's Security & Governance capabilities span three tiers. All plans benefit from AES-256 local credential encryption and full air-gapped support. Basic+ adds Data Masking (implementation details unknown/unverified). Professional adds an RBAC Dashboard (user management, custom roles, role inheritance, privilege tree), Audit Logging (full operation tracking for compliance), and Collection Compare & Sync (field-level document diff and directional sync between any two collections across connections and databases).

---

## Strengths

- **AES-256 local credential storage:** Credentials never leave the user's machine; no SozoCode cloud transmission — confirmed and critical for enterprise security policies.
- **Air-gapped support:** Fully offline after license activation; compatible with high-security network-isolated environments.
- **RBAC Dashboard with custom roles:** Granular privilege configuration on specific databases/collections; role inheritance — covers MongoDB's full role-based model.
- **Privilege hierarchy tree:** Visual hierarchical effective-privilege view — aids least-privilege audits.
- **Audit Logging:** Tracks queries, modifications, and connections with timestamps and user context — suitable for SOC2/compliance requirements.
- **Collection Compare & Sync:** Field-level diff with MODIFIED/ADDED/REMOVED badges across connections and databases; directional sync with Generate Sync Plan (preview before execute) — a powerful data migration/reconciliation tool.
- **Sync Log with per-operation detail:** Records type, status, collection, DB, match key value, timestamp, error — full traceability.

---

## Limitations / Gaps

- **Data Masking details unknown/unverified:** Basic+ plan pricing page lists Data Masking but no documentation page exists; masking rules, field patterns, reversibility, and output format are all **unknown/unverified**.
- **RBAC Dashboard requires Professional:** MongoDB users cannot be managed without the $149/year plan.
- **Audit Logging destination undocumented:** Whether audit logs export to file, syslog, SIEM, or are only viewable in UI is **unknown/unverified**.
- **Collection Compare: cross-database only or same-connection too?** Documentation confirms cross-connection/cross-DB but same-connection same-DB constraints are not specified.
- **Sync conflict resolution:** How the Sync Plan handles concurrent modifications during sync execution is **unknown/unverified**.
- **No MFA or SSO for VisuaLeaf application access:** No application-level authentication (MFA, SSO) documented; only MongoDB-level RBAC.

---

## Comparison Notes (vs MongoDB Compass baseline)

| Aspect | VisuaLeaf | MongoDB Compass |
|---|---|---|
| Credential encryption | **confirmed** (AES-256, local) | **confirmed** (local) |
| Air-gapped support | **confirmed** | **confirmed** |
| RBAC User management | **confirmed** (Professional) | not available |
| Custom role creation | **confirmed** (Professional) | not available |
| Privilege hierarchy visualization | **confirmed** (Professional) | not available |
| Audit logging | **confirmed** (Professional) | not available |
| Data Masking | **confirmed** (Basic+, details unknown) | not available |
| Collection Compare | **confirmed** (Professional, field-level diff) | not available |
| Collection Sync | **confirmed** (Professional, directional with plan+log) | not available |
| App-level MFA/SSO | not available | not available |

---

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [← AI Assistant](../ai/feature-report.md)
- [← Connectivity](../connectivity/feature-report.md)
- [← Querying](../querying/feature-report.md)
- [← Aggregation](../aggregation/feature-report.md)
- [← Schema Validation](../schema/feature-report.md)
- [← Indexing & Performance](../indexing-performance/feature-report.md)
- [← Data Import/Export](../data-transfer/feature-report.md)
- [← Schema Designer](../schema/feature-report.md)
- [← MongoDB Shell](../shell/feature-report.md)
