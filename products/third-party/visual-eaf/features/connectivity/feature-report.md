# VisuaLeaf — Connectivity Feature Report

## Summary

VisuaLeaf's Connection Manager provides enterprise-grade connection lifecycle management. It organizes connections in a three-tier Project → Environment → Connection hierarchy, supports all major MongoDB topology types, and covers the full spectrum of authentication mechanisms: SCRAM-SHA-256/1, X.509, LDAP, and AWS IAM are all confirmed. SSL/TLS with mTLS, SSH tunneling (password and private key), and granular driver-level options (pool sizing, write concern, compression) are confirmed. A 6-step validation wizard provides per-step pass/fail feedback. Kerberos and OIDC are on the Q2 2026 roadmap. Credentials are AES-256 encrypted and stored locally, supporting fully air-gapped deployments.

---

## Strengths

- **Structured hierarchy:** Project → Environment → Connection is more structured than typical favorites/recents patterns; supports teams managing many connections cleanly across environments.
- **Comprehensive auth coverage:** SCRAM-SHA-256/1, X.509, LDAP, AWS IAM — 6 of 8 mechanisms confirmed; only Kerberos and OIDC are pending (both Q2 2026).
- **6-step granular test validation:** Each of Network, SSH, TLS, Auth, DB Access, and Permissions is individually surfaced — debugging partial failures is straightforward vs. a single-step pass/fail.
- **Connection string bidirectional conversion:** URI → form (auto-fill on paste) and form → URI (Export to URL) both confirmed.
- **Full Write Concern control per connection:** W (majority/1/0), timeout (ms), journal — unusual granularity in GUI tools.
- **Air-gapped / offline:** AES-256 local encryption; no external server calls to SozoCode after license activation.
- **Driver-level pool and timeout controls:** Max/Min Pool Size, Max Idle Time, Socket/Connect/Server Selection timeouts all individually configurable — useful for tuning against slow networks or large Atlas clusters.

---

## Limitations / Gaps

- **Kerberos (GSSAPI) absent:** Enterprise environments using Active Directory Kerberos-backed MongoDB must wait until Q2 2026 or use a workaround.
- **OIDC absent:** MongoDB 7.0+ OIDC auth (Workforce Identity, Workload Identity Federation) not yet supported.
- **Community plan: 3-connection cap:** Limits usefulness for developers managing multiple environments on the free tier.
- **Connection import excludes passwords:** Security-justified but requires manual re-entry; no import-time password prompt documented.
- **DocumentDB / Cosmos DB / Redis:** Planned but unscheduled; users of those backends cannot connect yet.
- **snappy/zstd compression not mentioned:** Only zlib documented; MongoDB 4.2+ added snappy and zstd — unknown/unverified whether they are silently supported via URI or simply absent.

---

## Comparison Notes (vs MongoDB Compass baseline)

| Aspect | VisuaLeaf | MongoDB Compass |
|---|---|---|
| Connection grouping | Project → Environment → Connection hierarchy | Favorites + Recent only; no hierarchy |
| Topology: Sharded Cluster | **confirmed** (explicit mongos config) | **confirmed** |
| Auth: Kerberos | **roadmap/planned** (Q2 2026) | **confirmed** |
| Auth: OIDC | **roadmap/planned** (Q2 2026) | **confirmed** (Compass 1.40+) |
| Auth: LDAP | **confirmed** | **confirmed** |
| Auth: AWS IAM | **confirmed** | **confirmed** |
| SSH Tunnel | **confirmed** (password + private key) | **confirmed** |
| mTLS client certificate | **confirmed** | **confirmed** |
| Test connection granularity | 6-step (Network, SSH, TLS, Auth, DB, Permissions) | Single-step |
| Write Concern per connection | **confirmed** (W, timeout, journal) | not documented in UI |
| Connection pool settings | **confirmed** (Max/Min pool size, idle time) | not exposed in UI |
| Air-gapped support | **confirmed** | **confirmed** |
| App Name in profiler | "VisuaLeaf" (visible in currentOp/profiler) | "MongoDB Compass" |
| Connection import/export | JSON (passwords excluded) | not natively available |

---

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [→ Querying](../querying/feature-report.md)
- [→ Aggregation](../aggregation/feature-report.md)
- [→ Schema Validation](../schema/feature-report.md)
- [→ Indexing & Performance](../indexing-performance/feature-report.md)
- [→ Data Import/Export](../data-transfer/feature-report.md)
- [→ Schema Designer](../schema/feature-report.md)
- [→ MongoDB Shell](../shell/feature-report.md)
- [→ AI Assistant](../ai/feature-report.md)
- [→ Security & Governance](../governance/feature-report.md)
