# VisuaLeaf — Security & Governance Feature Matrix

| ID | Capability | Status | Detail | Source |
|---|---|---|---|---|
| SEC-001 | Credential encryption at rest | **confirmed** | AES-256 encryption; stored locally only; never sent to SozoCode servers | https://visualeaf.com/docs/connection-manager |
| SEC-002 | Air-gapped deployment support | **confirmed** | Fully offline after one-time license activation; no persistent cloud dependency | https://visualeaf.com/docs/connection-manager |
| SEC-003 | RBAC Dashboard: User management | **confirmed** | Professional plan; create, modify, delete MongoDB database users | https://visualeaf.com/features/rbac-dashboard/ |
| SEC-004 | RBAC Dashboard: Custom Role Creation | **confirmed** | Professional plan; granular privileges on specific databases and collections | https://visualeaf.com/features/rbac-dashboard/ |
| SEC-005 | RBAC Dashboard: Role inheritance | **confirmed** | Inherit from built-in or custom roles (role chains) | https://visualeaf.com/features/rbac-dashboard/ |
| SEC-006 | RBAC Dashboard: Hierarchical resource tree | **confirmed** | Shows effective privileges in a hierarchical tree view | https://visualeaf.com/features/rbac-dashboard/ |
| SEC-007 | RBAC Dashboard: Privilege actions | **confirmed** | Supports: read, write, dbAdmin, userAdmin, and all MongoDB privilege actions | https://visualeaf.com/features/rbac-dashboard/ |
| SEC-008 | Audit Logging | **confirmed** | Professional plan; tracks queries, modifications, connections with timestamps, user info, and detailed action logs; for compliance and security monitoring | https://visualeaf.com/features/rbac-dashboard/ |
| SEC-009 | Data Masking | **confirmed** | Basic+ plan; masks sensitive fields in query results | https://visualeaf.com/features/schema-validation/ |
| SEC-010 | Data Masking: implementation details | **unknown/unverified** | No dedicated documentation page found; masking rules, field patterns, and output format not documented | https://visualeaf.com/features/schema-validation/ |
| SEC-011 | Collection Compare & Sync | **confirmed** | Professional plan; compare and sync documents across collections/connections/databases | https://visualeaf.com/docs/collection-compare |
| SEC-012 | Compare: Three-panel layout | **confirmed** | Source (teal), Target (orange), Comparison Links panels | https://visualeaf.com/docs/collection-compare |
| SEC-013 | Compare: Drag-and-drop collection linking | **confirmed** | Link source and target collections across connections and databases | https://visualeaf.com/docs/collection-compare |
| SEC-014 | Compare: Link Configuration — Match Keys | **confirmed** | Default match key: _id; configurable to any field | https://visualeaf.com/docs/collection-compare |
| SEC-015 | Compare: Link Configuration — Source Filter | **confirmed** | MongoDB query syntax filter on source collection | https://visualeaf.com/docs/collection-compare |
| SEC-016 | Compare: Link Configuration — Target Filter | **confirmed** | MongoDB query syntax filter on target collection | https://visualeaf.com/docs/collection-compare |
| SEC-017 | Compare: Session management | **confirmed** | Save and load named comparison configurations | https://visualeaf.com/docs/collection-compare |
| SEC-018 | Compare: Result tabs | **confirmed** | Tabs: Summary, All, Modified, Missing in Source, Missing in Target, Log | https://visualeaf.com/docs/collection-compare |
| SEC-019 | Compare: Field-level diff | **confirmed** | Shows field path, MODIFIED/ADDED/REMOVED badge, source value, target value | https://visualeaf.com/docs/collection-compare |
| SEC-020 | Sync: Direction toggle | **confirmed** | Source→Target or Target→Source | https://visualeaf.com/docs/collection-compare |
| SEC-021 | Sync: Generate Sync Plan | **confirmed** | Preview showing Insert, Update/Replace, Delete operations before execution | https://visualeaf.com/docs/collection-compare |
| SEC-022 | Sync: Execute with progress tracking | **confirmed** | Real-time progress during sync execution | https://visualeaf.com/docs/collection-compare |
| SEC-023 | Sync: Sync Log | **confirmed** | Records each operation: type, status, collection, DB, match key value, timestamp, error | https://visualeaf.com/docs/collection-compare |
| SEC-024 | AI API key masking | **confirmed** | sk-proj-… format AES-masked in Settings UI | https://visualeaf.com/docs/settings |
| SEC-025 | SendGrid API key storage | **confirmed** | User-supplied key for email notifications; stored locally in Settings | https://visualeaf.com/docs/task-manager |

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← AI Assistant Matrix](../ai-assistant/feature-matrix.md)
- [← Connectivity Matrix](../connectivity/feature-matrix.md)
- [← All Feature Matrices](../)
