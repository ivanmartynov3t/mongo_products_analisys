# Feature Report — DataGrip / SQL Tools

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: SQL Tools
- Feature ID: F-SQL (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: DataGrip
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

Where Compass, VisuaLeaf, and Studio 3T all offer a MongoDB-native filter bar as the primary query surface, DataGrip's *only* MongoDB query surface is SQL text, transpiled by a custom JavaScript-SQL translation layer into native MongoDB shell syntax. A developer writes a standard SQL statement — for example `SELECT name, email, status FROM users WHERE age > 25 AND status = 'active' ORDER BY created_at DESC LIMIT 10;` — and DataGrip automatically converts it into `db.users.find({"age": {"$gt": 25}, "status": "active"}, {"name": 1, "email": 1, "status": 1, "_id": 0}).sort({"created_at": -1}).limit(10);`, viewable via a "Show JS Script" context action. This is not a secondary or experimental feature: it was announced as far back as the DataGrip 2020.3 EAP and remains documented today on JetBrains' own "SQL for MongoDB" help page — two independent primary sources corroborating both the feature's existence and its longevity.

The translation engine is deliberately narrow. Only SELECT-family syntax is supported (WHERE, GROUP BY, HAVING, ORDER BY, LIMIT, OFFSET, INNER JOIN, LEFT JOIN); INSERT, UPDATE, and DELETE must be authored directly in MongoDB shell syntax or performed cell-by-cell in the data grid. JOINs are restricted to a single equality condition in the ON clause — compound conditions, subqueries inside JOIN clauses, and USING syntax are all explicitly unsupported. SQL aggregate functions (AVG, SUM, MIN, MAX) cannot be used outside an explicit GROUP BY block, and nested aggregate calls are prohibited. There is no SQL migration wizard and no SQL-to-MongoDB-driver-language code generator — the source's own side-by-side comparison table credits Studio 3T alone with a "Full SQL query translation engine with bi-directional SQL-to-MongoDB data migration tools," explicitly contrasting it with DataGrip's narrower translation-only engine.

The most architecturally significant SQL capability described for DataGrip overall is `dg_cross`, a DuckDB-backed cross-database federation engine introduced in the 2026.2 release. It lets a single SQL query join tables qualified by different `$data_source` names — the source's worked example joins `$postgresql_production.public.products` with `$sqlserver_warehouse.dbo.orders` — with DataGrip transparently transpiling the qualified syntax into DuckDB `dg_cross` function calls, handling remote connections, type mapping, and streaming automatically. This is confirmed as a real, shipped feature via DataGrip's own 2026.2 release notes and a JetBrains-internal design discussion on its console/UX. **Important scope caveat:** the source's own technical walkthrough and code example name only relational engines as join targets; MongoDB is never shown as a `dg_cross` participant in that section. MongoDB appears only in the source's separate strategic-recommendations section, which proposes that Studio 3T build an *equivalent* federation capability to close this gap — that framing implies DataGrip's own federation reach into MongoDB is not itself confirmed, only aspirational-by-analogy. This distinction matters enough to call out explicitly rather than let the general "DataGrip has federated querying" claim imply MongoDB coverage it may not have.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| SQL-expressions, SQL-code-gen | SQL-to-MongoDB-shell translation is DataGrip's entire MongoDB query mechanism, independently confirmed by two JetBrains primary sources spanning six years (2020 announcement, current help page). | The single strongest-evidenced MongoDB capability in this entire product entry. | JetBrains "SQL for MongoDB" help page (S1 Works Cited #22); "DataGrip 2020.3 EAP 3: SQL for MongoDB" blog post (S1 Works Cited #23) |
| SQL-join-mapping, SQL-migration | No visual JOIN editor (single equality condition only, text-authored); no migration wizard or driver-language code-gen — both confirmed absent by direct statement/contrast in the source. | Materially narrower MongoDB toolchain than Studio 3T for both query authoring beyond simple filters and any relational-to-document migration scenario. | Research file narrative and its own MongoDB capability comparison table |
| SQL-federated-query | `dg_cross` is a confirmed, shipped, primary-sourced feature, but its applicability to MongoDB specifically is not confirmed — only relational engines appear in the source's worked technical example. | Prevents overstating DataGrip's federation capability as already MongoDB-inclusive when the evidence doesn't support that specific claim. | DataGrip 2026.2 release notes (S1 Works Cited #5); YouTrack design issue DBE-26268 (S1 Works Cited #6) |

## Constraints and risks

- DataGrip's entire MongoDB "querying" capability lives inside F-SQL — there is no fallback native query surface if a user needs something the SQL translator cannot express (e.g., a multi-stage aggregation, a compound-condition JOIN, or a write operation), other than dropping to raw MongoDB shell syntax.
- Do not conflate `dg_cross`'s confirmed relational-database federation capability with a confirmed MongoDB-inclusive federation capability — the source does not make that specific claim.

## Interactions and dependencies

- Depends on [F-CONN](../connectivity/feature-report.md)'s MongoDB connection (bundled JDBC driver 1.21 as of 2026.2).
- AI-generated SQL from [F-AI](../ai/feature-report.md)'s Claude Agent/Codex chat is executed through this same SQL-to-JS translation engine and the internal MCP server's `execute_sql_query` tool.

## Conclusions

### Strengths

- Independently confirmed (by two JetBrains primary sources spanning six years) SQL-to-MongoDB-shell translation engine — the most solidly evidenced MongoDB capability for DataGrip in this repository.
- `dg_cross` is a genuine, shipped architectural differentiator among the products compared here, even setting aside its unconfirmed MongoDB scope.

### Limitations

- No visual pipeline builder, no SQL migration wizard, no driver-language code generation, no INSERT/UPDATE/DELETE via SQL, and JOINs limited to a single equality condition with no visual mapping editor.

### Unknowns

- Whether `dg_cross` can join in a MongoDB collection specifically (only relational engines are shown in the source's technical example).
- Whether the SELECT-clause support list has expanded in versions released after the source's own citations.
