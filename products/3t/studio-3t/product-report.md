# Product Report — Studio 3T

## Navigation

- [Repository README](../../../README.md)
- [3T products index](../README.md)
- [High-level comparison](../../../reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](../../../reports/comparisons/low-level-feature-comparison.md)

## Product metadata

- Product name: Studio 3T
- Product group: 3t
- Website: https://studio3t.com
- Maker: 3T Software Labs
- Category: MongoDB IDE / tooling platform
- Analysis date: 2026-06-22

## Product summary

Studio 3T is a multi-product MongoDB tooling platform anchored by the Studio 3T Desktop IDE — a full-featured fat client for Windows, macOS, and Linux. The platform spans six products: the Desktop IDE, 3T Build (browser IDE), 3T MCP (standalone MCP CLI), 3T Lens (governance workspace), 3T Access (identity/governance plane), and 3TL Bridge (CDC pipeline engine). The Desktop IDE delivers the deepest feature set and is the primary subject of this analysis, with platform-wide features noted where applicable.

The product is tiered across Free, Pro/Base, and Ultimate editions. The Free edition covers core querying, aggregation, import/export, IntelliShell, and the Visual Query Builder. Pro/Base adds SQL tooling, data masking, reschema, team sharing, and the task scheduler. Ultimate unlocks enterprise authentication mechanisms (Kerberos, LDAP, AWS IAM, MongoDB OIDC). Exact edition names are unverified — the pricing page returned 404 at analysis time.

Studio 3T's key differentiators versus MongoDB Compass include: SQL query/migration tooling, a mature task scheduler, IntelliShell (mongosh-based with Query Assist mode), data masking, a full Visual Query Builder with bidirectional sync, and a governance/pipeline platform (3T Lens + 3TL Bridge) aimed at enterprise deployments.

## Feature inventory

| Feature | Matrix | Report | Status |
| --- | --- | --- | --- |
| connectivity | [feature-matrix.md](features/connectivity/feature-matrix.md) | [feature-report.md](features/connectivity/feature-report.md) | Completed |
| querying | [feature-matrix.md](features/querying/feature-matrix.md) | [feature-report.md](features/querying/feature-report.md) | Completed |
| aggregation | [feature-matrix.md](features/aggregation/feature-matrix.md) | [feature-report.md](features/aggregation/feature-report.md) | Completed |
| schema-explorer | [feature-matrix.md](features/schema-explorer/feature-matrix.md) | [feature-report.md](features/schema-explorer/feature-report.md) | Completed |
| indexing-performance | [feature-matrix.md](features/indexing-performance/feature-matrix.md) | [feature-report.md](features/indexing-performance/feature-report.md) | Completed |
| data-import-export | [feature-matrix.md](features/data-import-export/feature-matrix.md) | [feature-report.md](features/data-import-export/feature-report.md) | Completed |
| sql-tools | [feature-matrix.md](features/sql-tools/feature-matrix.md) | [feature-report.md](features/sql-tools/feature-report.md) | Completed |
| ai-features | [feature-matrix.md](features/ai-features/feature-matrix.md) | [feature-report.md](features/ai-features/feature-report.md) | Completed |
| governance-platform | [feature-matrix.md](features/governance-platform/feature-matrix.md) | [feature-report.md](features/governance-platform/feature-report.md) | Completed |
| task-scheduler | [feature-matrix.md](features/task-scheduler/feature-matrix.md) | [feature-report.md](features/task-scheduler/feature-report.md) | Completed |

## Product-level conclusions

### Strategic strengths

- Deepest SQL tooling of any MongoDB GUI: bidirectional SQL↔MongoDB migration with JOIN mapping and schema manipulation.
- IntelliShell's Query Assist mode bridges ad-hoc scripting with structured result editing — a capability absent from Compass.
- Task Scheduler integrates import, export, masking, reschema, compare/sync, and IntelliShell scripts into a single scheduling plane.
- Visual Query Builder with real-time bidirectional sync to the query bar and Aggregation Editor reduces the learning curve for non-developers.
- Data masking is built in at the import, export, and standalone tool layers — not a bolt-on.
- Enterprise auth mechanisms (Kerberos, LDAP, AWS IAM, OIDC) gate at Ultimate tier, aligning with enterprise IT requirements.
- Platform breadth (Desktop IDE + Browser IDE + MCP + Governance + CDC) enables end-to-end MongoDB lifecycle management.

### Strategic risks / gaps

- Pricing page returned 404 at analysis time — edition tier names and exact pricing are unverified (**unknown/unverified**).
- Some high-value features (SQL tools, task scheduler, data masking, reschema, team sharing) are behind Pro/Base paywall — Free edition users face significant capability gaps.
- Enterprise auth (Kerberos, LDAP, AWS IAM, OIDC) locked to Ultimate only — meaningful edition friction for enterprise self-service.
- 3T Lens, 3T Access, and 3TL Bridge governance products are separate deployments; integration maturity with the Desktop IDE is not fully verified.
- The geoHaystack index type is deprecated in MongoDB 4.4 and removed in 5.0; Studio 3T still surfaces it in the UI — could mislead users on newer MongoDB versions.
- AI Helper requires external API keys (Azure/OpenAI/Anthropic) — no bundled LLM; incurs per-token cost and requires user-managed key security.

### Open questions

- Are edition names definitively "Free / Pro / Ultimate" or is "Base" a separate SKU?
- What is the exact pricing for Pro/Base and Ultimate?
- Does 3T Lens replace or supplement the Desktop IDE connection manager in practice?
- Is the Local MCP Server available in all editions or only Pro/Ultimate?
- What MongoDB server version range is officially supported (minimum and maximum)?
