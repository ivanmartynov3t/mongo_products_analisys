# Product Report — Studio 3T

## Navigation

- [Repository README](../../../README.md)
- [Feature dictionary](../../../feature-dictionary.md)
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

Studio 3T is a multi-product MongoDB tooling platform anchored by the Studio 3T Desktop IDE — a full-featured fat client for Windows, macOS, and Linux. Per studio3t.com, the platform is organized into three tracks: **Build** (Studio 3T Desktop IDE, [3T Explore](../3t-explore/product-report.md), [3T MCP](../3t-mcp/product-report.md)), **Pipeline** ([3TL Bridge](../3tl-bridge/product-report.md)), and **Governed Access** ([3T Lens](../3t-lens/product-report.md), [3T Access](../3t-access/product-report.md)). "Build" is the track name, not a product name. The Desktop IDE delivers the deepest feature set and is the primary subject of this analysis and this product folder.

As of 2026-07-29, 3T Explore, 3T MCP, 3TL Bridge, 3T Lens, and 3T Access are each documented in their own product folder under `products/3t/` (linked above) rather than as sub-sections of this report — see [3T products index](../README.md) for the full list. This report previously documented them as sub-sections of the Desktop IDE's AI Features and Governance & Security matrices.

Studio3t.com also states database compatibility with FerretDB, Amazon DocumentDB, and Azure Cosmos DB in addition to MongoDB (see CONN-compat-ferretdb). The vendor's website states ISO 27001 and SOC 2 certification and on-premises deployment options for the governance platform — this is a vendor claim from studio3t.com and has not been independently verified beyond that statement.

The product is tiered across Free, Pro/Base, and Ultimate editions. The Free edition covers core querying, aggregation, import/export, IntelliShell, and the Visual Query Builder. Pro/Base adds SQL tooling, data masking, reschema, team sharing, and the task scheduler. Ultimate unlocks enterprise authentication mechanisms (Kerberos, LDAP, AWS IAM, MongoDB OIDC). Exact edition names are unverified — the pricing page returned 404 at analysis time.

Studio 3T's key differentiators versus MongoDB Compass include: SQL query/migration tooling, a mature task scheduler, IntelliShell (mongosh-based with Query Assist mode), data masking, a full Visual Query Builder with bidirectional sync, and a governance/pipeline platform (3T Lens + 3TL Bridge) aimed at enterprise deployments.

## Feature inventory

Feature IDs and folder names from [feature-dictionary.md](../../../feature-dictionary.md).

| Feature ID | Feature | Matrix | Report | Status |
| --- | --- | --- | --- | --- |
| F-CONN | Connectivity | [feature-matrix.md](features/connectivity/feature-matrix.md) | [feature-report.md](features/connectivity/feature-report.md) | Completed |
| F-QUERY | Querying | [feature-matrix.md](features/querying/feature-matrix.md) | [feature-report.md](features/querying/feature-report.md) | Completed |
| F-AGG | Aggregation | [feature-matrix.md](features/aggregation/feature-matrix.md) | [feature-report.md](features/aggregation/feature-report.md) | Completed |
| F-SCHEMA | Schema | [feature-matrix.md](features/schema/feature-matrix.md) | [feature-report.md](features/schema/feature-report.md) | Completed |
| F-IDX | Indexing & Performance | [feature-matrix.md](features/indexing-performance/feature-matrix.md) | [feature-report.md](features/indexing-performance/feature-report.md) | Completed |
| F-TRANSFER | Data Transfer | [feature-matrix.md](features/data-transfer/feature-matrix.md) | [feature-report.md](features/data-transfer/feature-report.md) | Completed |
| F-SHELL | Shell | [feature-matrix.md](features/shell/feature-matrix.md) | [feature-report.md](features/shell/feature-report.md) | Completed |
| F-AI | AI Features | [feature-matrix.md](features/ai/feature-matrix.md) | [feature-report.md](features/ai/feature-report.md) | Completed |
| F-SQL | SQL Tools | [feature-matrix.md](features/sql-tools/feature-matrix.md) | [feature-report.md](features/sql-tools/feature-report.md) | Completed |
| F-GOV | Governance & Security | [feature-matrix.md](features/governance/feature-matrix.md) | [feature-report.md](features/governance/feature-report.md) | Partial — platform-tier products split to their own folders 2026-07-29 ([3T Lens](../3t-lens/product-report.md), [3T Access](../3t-access/product-report.md), [3TL Bridge](../3tl-bridge/product-report.md), [3T Explore](../3t-explore/product-report.md)); Desktop IDE-native governance (RBAC, audit log, masking, compare/sync) not yet authored |
| F-SCHED | Task Scheduler | [feature-matrix.md](features/task-scheduler/feature-matrix.md) | [feature-report.md](features/task-scheduler/feature-report.md) | Completed |

## Product-level conclusions

### Strategic strengths

- Deepest SQL tooling of any MongoDB GUI: bidirectional SQL↔MongoDB migration with JOIN mapping and schema manipulation.
- IntelliShell's Query Assist mode bridges ad-hoc scripting with structured result editing — a capability absent from Compass.
- Task Scheduler integrates import, export, masking, reschema, compare/sync, and IntelliShell scripts into a single scheduling plane.
- Visual Query Builder with real-time bidirectional sync to the query bar and Aggregation Editor reduces the learning curve for non-developers.
- Data masking is built in at the import, export, and standalone tool layers — not a bolt-on.
- Enterprise auth mechanisms (Kerberos, LDAP, AWS IAM, OIDC) gate at Ultimate tier, aligning with enterprise IT requirements.
- Platform breadth (Desktop IDE + [3T Explore](../3t-explore/product-report.md) + [3T MCP](../3t-mcp/product-report.md) + [3T Lens](../3t-lens/product-report.md)/[3T Access](../3t-access/product-report.md) governance + [3TL Bridge](../3tl-bridge/product-report.md) CDC) enables end-to-end MongoDB lifecycle management.

### Strategic risks / gaps

- Pricing page returned 404 at analysis time — edition tier names and exact pricing are unverified (**unknown/unverified**).
- Some high-value features (SQL tools, task scheduler, data masking, reschema, team sharing) are behind Pro/Base paywall — Free edition users face significant capability gaps.
- Enterprise auth (Kerberos, LDAP, AWS IAM, OIDC) locked to Ultimate only — meaningful edition friction for enterprise self-service.
- [3T Lens](../3t-lens/product-report.md), [3T Access](../3t-access/product-report.md), and [3TL Bridge](../3tl-bridge/product-report.md) governance products are separate deployments; integration maturity with the Desktop IDE is not fully verified.
- The geoHaystack index type is deprecated in MongoDB 4.4 and removed in 5.0; Studio 3T still surfaces it in the UI — could mislead users on newer MongoDB versions.
- AI Helper requires external API keys (Azure/OpenAI/Anthropic) — no bundled LLM; incurs per-token cost and requires user-managed key security.

### Open questions

- Are edition names definitively "Free / Pro / Ultimate" or is "Base" a separate SKU?
- What is the exact pricing for Pro/Base and Ultimate?
- Does [3T Lens](../3t-lens/product-report.md) replace or supplement the Desktop IDE connection manager in practice?
- Is the Local MCP Server available in all editions or only Pro/Ultimate?
- What MongoDB server version range is officially supported (minimum and maximum)?
- What edition/plan is required for [3T Explore](../3t-explore/product-report.md) access, and does it require a separate license from the Desktop IDE?
- Which specific FerretDB versions/features have been validated with Studio 3T (studio3t.com lists compatibility but does not give a version matrix)?
