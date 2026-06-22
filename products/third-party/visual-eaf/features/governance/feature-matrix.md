# Feature Matrix — VisuaLeaf / Governance

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← AI Matrix](../ai/feature-matrix.md)
- [← Connectivity Matrix](../connectivity/feature-matrix.md)
- [→ All Features](../)

## Source index

- S1: https://visualeaf.com/docs/connection-manager
- S2: https://visualeaf.com/features/rbac-dashboard/
- S3: https://visualeaf.com/docs/collection-compare
- S4: https://visualeaf.com/docs/settings
- S5: https://visualeaf.com/features/schema-validation/

## Capability matrix

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| GOV-cred-storage-os | Credential and key storage | confirmed | AES-256 local encryption for all connection credentials; never transmitted to SozoCode servers; air-gapped compatible. AI API keys (sk-proj-… format) are AES-masked in Settings UI and stored locally. SendGrid API key (user-supplied for email notifications) also stored locally. | — | confirmed | S1, S4 |
| GOV-air-gapped | Air-gapped deployment | confirmed | Fully offline after one-time license activation; no persistent cloud dependency for operation. | — | confirmed | S1 |
| GOV-rbac-users | RBAC: user management | confirmed | Create, modify, delete MongoDB database users. | Professional plan | confirmed | S2 |
| GOV-rbac-roles | RBAC: custom role creation | confirmed | Create custom roles with granular privileges on specific databases and collections. | Professional plan | confirmed | S2 |
| GOV-rbac-inheritance | RBAC: role inheritance | confirmed | Roles can inherit from built-in or custom roles (role chains). | Professional plan | confirmed | S2 |
| GOV-rbac-tree | RBAC: hierarchy tree view | confirmed | Shows effective privileges in a hierarchical tree view. | Professional plan | confirmed | S2 |
| GOV-rbac-actions | RBAC: privilege actions | confirmed | Supports all MongoDB privilege actions: read, write, dbAdmin, userAdmin, and all others. | Professional plan | confirmed | S2 |
| GOV-audit-log | Audit logging | confirmed | Tracks queries, modifications, and connections with timestamps, user info, and detailed action logs; for compliance and security monitoring. | Professional plan | confirmed | S2 |
| GOV-data-masking | Data masking | confirmed | Masks sensitive fields in query results for governance. Basic or Professional plan. Implementation details (masking rules, field patterns, output format) are **unknown/unverified** — no dedicated documentation page found. | Basic or Professional plan | confirmed/unknown | S5 |
| GOV-collection-compare | Collection Compare | confirmed | Professional plan. Three-panel layout: Source (teal), Target (orange), Comparison Links. Drag-and-drop collection linking across connections and databases. Match keys configurable (default: _id, any field). Source and target filters (MongoDB query syntax). Session save/load for named comparison configs. Result tabs: Summary, All, Modified, Missing in Source, Missing in Target, Log. Field-level diff: field path, MODIFIED/ADDED/REMOVED badge, source value, target value. | Professional plan | confirmed | S3 |
| GOV-collection-sync | Collection Sync | confirmed | Sync direction toggle: Source→Target or Target→Source. Generate sync plan preview: shows Insert, Update/Replace, Delete operations before execution. Execute with real-time progress tracking. Sync log: records each operation type, status, collection, DB, match key value, timestamp, error. | Professional plan | confirmed | S3 |
