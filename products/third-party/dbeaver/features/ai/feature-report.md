# Feature Report — DBeaver / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: AI Features
- Feature ID: F-AI (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: DBeaver
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

DBeaver's AI Assistant is built into its SQL editing environment: a user's natural-language prompt is combined with database schema metadata and sent to a configured LLM provider (OpenAI with GPT-5 default, Azure OpenAI, Google Gemini, or GitHub Copilot/Codex), which returns a SQL statement. For a MongoDB connection, this means the AI produces SQL text executed through DBeaver's JDBC/SQL-Console bridge (see [F-SQL](../sql-tools/feature-report.md)) rather than a native MongoDB filter document or aggregation pipeline — a materially different generation target from Compass, VisuaLeaf, or Studio 3T, which all generate MongoDB-native query/pipeline syntax directly.

Beyond text prompts, the source describes two newer input/integration surfaces: speech-to-text voice querying (with audio visualization and pause detection) and file-attachment context, where a user can drop a CSV/JSON/Parquet/XLSX file into an AI Chat session; DBeaver parses its schema, builds a temporary in-memory table, and lets the user query across the combined file-and-database context in one natural-language session.

The most forward-looking capability described is DBeaver exposing its live database connections as Model Context Protocol (MCP) servers, letting external AI agents (the source names Claude Desktop as an example) query connected databases through governed tool interfaces — architecturally similar to Studio 3T's own local MCP server, but for DBeaver's much broader multi-engine connection set. Execution safety is addressed through token-usage tracking, response streaming, cancellation controls, and confirmation dialogs before potentially destructive DDL/DML statements run.

**Important caveat on dates:** the source attributes the voice-querying feature to "version 25.2" and the MCP server integration to "version 26.1.2." Neither exact version string appears among the source's own Works Cited release-note entries (which list 24.2.5, 24.3.5, 25.0, 25.1.5, 25.3.5, and 26.0.5). Per this repository's classification rule — a secondary source's own uncited assertion does not clear the "Confirmed" bar even when phrased with specific-sounding detail — both capabilities are marked Unverified in the feature matrix rather than Confirmed, despite reading confidently in the source narrative.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| AI-nl-query | Generates SQL text via schema-aware LLM prompting, not a native MongoDB query. | Materially different generation target from every other AI-capable product in this repository's comparison set. | Research file narrative |
| AI-sample-context | File-attachment context model (CSV/JSON/Parquet/XLSX parsed into temporary in-memory tables) is unique among the products reviewed here. | A genuinely distinct AI-context mechanism worth flagging in competitive analysis, even though unverified against a primary source. | Research file narrative |
| AI-voice-query, AI-mcp-client | Both cited with specific version numbers not found among the source's own listed release notes. | Demonstrates the value of this repository's stricter "trace to the specific claim" citation rule — a plausible, confidently-worded secondary claim is not automatically Confirmed. | Research file narrative; absence from S1's own Works Cited release-note list |

## Constraints and risks

- Every AI sub-feature in this area is Unverified rather than Confirmed: the research file is a competitive-intelligence narrative, and none of its AI-feature claims is tied to a specific, matching primary source in its own Works Cited list (the general `dbeaver.com/release-notes/` index does not substitute for a dated, version-specific entry).
- Do not treat the version numbers "25.2" and "26.1.2" as confirmed release facts in any downstream document without independently checking DBeaver's actual release notes (out of scope for this plan).

## Interactions and dependencies

- AI-generated SQL output depends on and executes through [F-SQL](../sql-tools/feature-report.md)'s SQL Console for MongoDB connections.
- MCP server exposure is conceptually adjacent to Studio 3T's own `AI-007`/`AI-008`/`AI-009` local MCP server capabilities (see [feature-dictionary.md](../../../../../feature-dictionary.md)) — useful for direct competitive comparison in `reports/comparisons/`.

## Conclusions

### Strengths

- Widest documented LLM provider list among products in this repository (OpenAI, Azure OpenAI, Google Gemini, GitHub Copilot/Codex).
- Unique file-attachment AI context model.
- MCP server exposure of live connections, positioning DBeaver in the same agentic-AI space as Studio 3T's MCP surface.

### Limitations

- AI output is SQL, not native MongoDB query/pipeline syntax.
- Two headline AI capabilities (voice querying, MCP integration) carry specific version claims that cannot be traced to the source's own cited primary sources.

### Unknowns

- Actual (verified) release version for voice querying and MCP integration.
- Per-tier gating of individual AI sub-capabilities.
- Whether AI-generated SQL against a MongoDB connection is further translated into native MongoDB operations, or executed as literal SQL via the JDBC bridge.
