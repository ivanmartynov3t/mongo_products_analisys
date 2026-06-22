# High-Level Product Comparison

## Navigation

- [Cumulative report index](../cumulative-report.md)
- [Low-level comparison](low-level-feature-comparison.md)
- [Feature dictionary](../../feature-dictionary.md)
- [Studio 3T product report](../../products/3t/studio-3t/product-report.md)
- [MongoDB Compass product report](../../products/third-party/mongodb-compass/product-report.md)
- [VisuaLeaf product report](../../products/third-party/visual-eaf/product-report.md)

## Compared products

- Third-party:
  - MongoDB Compass
  - VisuaLeaf
- 3t:
  - Studio 3T

## Product-level comparison

| Product | Group | Positioning | Core feature coverage | Main strengths | Main gaps |
| --- | --- | --- | --- | --- | --- |
| [MongoDB Compass](../../products/third-party/mongodb-compass/product-report.md) | third-party | General-purpose MongoDB GUI for developers and operators | Broad (F-CONN, F-QUERY, F-AGG, F-SCHEMA, F-IDX, F-GOV) | Deep aggregation tooling; broad connection and security options | No shell, no AI, no import/export, no task scheduler |
| [VisuaLeaf](../../products/third-party/visual-eaf/product-report.md) | third-party | Desktop MongoDB IDE with visual tools and AI | Broad (F-CONN, F-QUERY, F-AGG, F-SCHEMA, F-IDX, F-TRANSFER, F-SHELL, F-AI, F-GOV, F-SCHED) | Strong visual tools, AI query builder, task scheduler; tiered pricing | No SQL tools; no enterprise CDC pipeline; Kerberos/OIDC roadmap |
| [Studio 3T](../../products/3t/studio-3t/product-report.md) | 3t | Full-featured MongoDB IDE platform with SQL, governance, and CDC | Full (F-CONN, F-QUERY, F-AGG, F-SCHEMA, F-IDX, F-TRANSFER, F-SHELL, F-AI, F-SQL, F-GOV, F-SCHED) | Deepest SQL tooling; IntelliShell; mature task scheduler; governance platform | Some features require Pro/Ultimate; pricing page unverified |

## Feature-group comparison

Feature IDs reference the [unified feature dictionary](../../feature-dictionary.md).

| Feature ID | Feature | MongoDB Compass | VisuaLeaf | Studio 3T | Gap assessment |
| --- | --- | --- | --- | --- | --- |
| F-CONN | Connectivity | Strong — all topology types, all auth methods, TLS/SSH/proxy | Strong — all topology types, most auth methods (Kerberos/OIDC roadmap), rich advanced params | Strong — all topology types, all auth methods incl. enterprise (Ultimate), SSH profiles | Compass: no connection test steps UI; VisuaLeaf: Kerberos/OIDC pending; Studio 3T: enterprise auth Ultimate-only |
| F-QUERY | Querying | Solid — filter bar, projections, sort, collation, history, saved queries | Deep — VQB, AI query builder, 4 view modes, batch edit, execution timer | Deep — VQB with bidirectional sync, IntelliShell, date tags, query manager | Compass: no VQB, no AI query builder; VisuaLeaf: AI requires Professional plan |
| F-AGG | Aggregation | Strong — stage builder, multi-mode, save/load, explain, code gen | Strong — 37+ stages, visual/JSON mode per stage, preview, code tab, 4 export formats | Strong — pipeline editor, options, code gen, create view, VQB sync | All products cover core pipeline authoring; Studio 3T adds date tags; VisuaLeaf adds chart builder |
| F-SCHEMA | Schema | Sampling, field analysis, geo analysis, validation rules, UI workflows | JSON schema editor, deploy validator, visual ERD canvas, import from DB | Sampling, field analysis, histograms, view editor, documentation export | Compass: no visual ERD designer; Studio 3T: no JSON schema editor or deploy validator |
| F-IDX | Indexing & Performance | Index lifecycle, Atlas/Vector Search indexes, explain, perf insights, real-time perf | Full index type coverage, collation/text/geo opts, profiler with percentiles, live monitoring | Full index type coverage, Visual Explain (brief/full), Query Profiler, profiler drill-down | Compass: Atlas/Vector Search unique; VisuaLeaf: strongest profiler analytics; Studio 3T: has haystack (deprecated) |
| F-TRANSFER | Data Transfer | — (not available) | JSON/CSV/BSON/SQL INSERT, field mapping, JS transforms, pipeline pre-export | JSON/CSV/BSON/Excel/SQL, SQL source import, incremental export, data masking | Studio 3T: most complete with masking and SQL source; VisuaLeaf: no SQL DB source/target |
| F-SHELL | Shell | — (not available) | Monaco editor, mongosh runtime, run all/select/cursor, sessions, history | IntelliShell (mongosh), Shell + Query Assist modes, editable result tabs | Compass: no shell; both Studio 3T and VisuaLeaf have strong shell capabilities |
| F-AI | AI Features | — (not available) | NL→query and NL→pipeline, 11 OpenAI models, schema-aware, privacy mode, Professional-only | AI Helper (Azure/OpenAI/Anthropic), NL→query, NL→code, Pro/Base+ | Compass: no AI; both require user-managed API keys |
| F-SQL | SQL Tools | — (not available) | — (not available) | SQL query, JOIN mapping, SQL↔MongoDB migration, reschema; Pro/Base+ | Studio 3T unique differentiator |
| F-GOV | Governance & Security | Readonly, cred protection, network policy, telemetry, startup/CLI policy, AI controls | RBAC dashboard, audit logging, data masking, collection compare/sync, air-gapped, Professional | Governance platform (3T Lens, 3T Access, 3TL Bridge), CDC, data masking, compare/sync, Ultimate | Compass: no RBAC dashboard; Studio 3T: unique CDC pipeline; VisuaLeaf: strongest RBAC UI |
| F-SCHED | Task Scheduler | — (not available) | 6 schedule types, cron, timezone, 5 task states, notifications, Basic+ | Multi-type task scheduler (import/export/masking/reschema/script), Pro/Base+ | Both use per-user API key setup; Studio 3T has broader task types |

## Conclusions

- Studio 3T has the broadest feature coverage across all 11 feature areas.
- VisuaLeaf is the strongest third-party competitor: visual tools, AI, task scheduler, RBAC, air-gapped.
- MongoDB Compass is focused on core developer/operator workflows without automation, AI, or SQL.
- F-SQL is a unique Studio 3T differentiator with no third-party equivalent.
- F-GOV (3T Lens + 3TL Bridge) is a unique Studio 3T enterprise platform — no third-party equivalent.
- Kerberos/OIDC auth is a gap in VisuaLeaf (roadmap Q2 2026) vs Studio 3T (confirmed Ultimate) and Compass (confirmed).
