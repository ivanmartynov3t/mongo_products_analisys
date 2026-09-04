# Feature Matrix — TablePlus / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: TablePlus
- Product group: third-party
- Feature ID: F-AI (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `ai`
- Analysis date: 2026-09-04
- Version/release context: 2026 release line ("2024–2026: AI Architecture and Protocol Standardization" per the source's own historical-trajectory section)

## Source index

- S1: TablePlus Competitive Intelligence Analysis (secondary research file, no inline per-claim citation markers), `research/google_research/tableplus-competitive-intelligence-analysis/TablePlus Competitive Intelligence Analysis.md`
- S1 Works Cited #28: "AI SQL Completion · Issue #3065 · TablePlus/TablePlus - GitHub" — a GitHub issue thread; not independently fetched for this matrix, and its role (a feature request/discussion thread vs. confirmation of a shipped feature) is not established by S1 alone, so it is not treated as primary-source confirmation of any specific shipped capability.

## Scope note: general AI features, MongoDB applicability largely unconfirmed

Section 8 describes TablePlus's AI/MCP architecture in cross-engine terms — "natural language-to-SQL generation," GitHub Copilot "inline SQL completions," and DeepSeek "tool invocation capabilities that allow the assistant to inspect active schema context and fix invalid query syntax." Every one of these descriptions names SQL specifically, not MQL or MongoDB. Only the MCP server description is stated in engine-agnostic terms ("read database schemas, inspect table structures, and construct queries through TablePlus's execution layer"). This matrix therefore scores general-product AI capability as the best-supported reading, with MongoDB-specific applicability flagged as unconfirmed throughout — consistent with how DataGrip's `dg_cross` federation capability was scored Unverified for MongoDB scope despite general existence being well-described.

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-providers | Provider support | Unverified — per secondary source, no primary citation | S1 (Section 8): "Bring-Your-Own-Key (BYOK) Model: Users input their own API credentials for providers like OpenAI or DeepSeek." | User-supplied API key required; no built-in/bundled AI provider. | Unverified | S1 | — |
| AI-key-storage | API key storage | Unverified — per secondary source, no primary citation | Inferred from the BYOK model description and Section 10's general local-encrypted-credential-storage claim; not stated as a distinct, AI-specific claim. | — | Unverified | S1 | Cross-referenced with `CONN-cred-storage` — the source does not separately confirm API keys are stored the same way as database credentials. |
| AI-nl-query | NL to query | Unverified — MongoDB scope explicitly doubtful | S1 (Section 8): BYOK "enable[s] natural language-to-SQL generation, query optimization, and error troubleshooting directly within the editor workspace." | The source names SQL specifically, not MQL; TablePlus's MongoDB support is elsewhere confirmed to lack any query-translation layer (see product-report.md's omitted-F-SQL note), making NL-to-MQL generation via the same mechanism uncertain rather than assumed. | Unverified (MongoDB scope doubtful) | S1 | Flagged prominently as an open question in product-report.md — do not assume this extends to MongoDB. |
| AI-inline-completion | Inline AI code completion | Unverified — per secondary source, no primary citation; MongoDB scope unconfirmed | S1 (Section 8): "GitHub Copilot Integration: Supports native authorization for GitHub Copilot, allowing inline SQL completions within the query editor." | Named specifically as "inline SQL completions" — MongoDB/MQL completion via the same integration is not stated. | Unverified | S1, S1 Works Cited #28 (unconfirmed relevance) | The GitHub issue in Works Cited #28 ("AI SQL Completion") is consistent with this being a SQL-scoped feature, not confirmation either way of shipped status. |
| AI-error-fix | AI-assisted error correction | Unverified — per secondary source, no primary citation; MongoDB scope unconfirmed | S1 (Section 8): "DeepSeek Integration with Tool Invocation: Recent updates added support for the DeepSeek API, including tool invocation capabilities that allow the assistant to inspect active schema context and fix invalid query syntax." | "Query syntax" is not specified as SQL-only or MQL-inclusive here (unlike the BYOK/Copilot descriptions, which explicitly say SQL) — the closest thing to an engine-agnostic AI capability claim in this section. | Unverified | S1 | Scored slightly more optimistically than `AI-nl-query`/`AI-inline-completion` for MongoDB scope, since this is the one AI capability in Section 8 not explicitly qualified as SQL-only — but still Unverified, not Confirmed. |
| AI-local-mcp | Local MCP server | Unverified — per secondary source, no primary citation | S1 (Section 8): "Model Context Protocol (MCP) Server Support: TablePlus includes native support for the Model Context Protocol (MCP). This allows TablePlus to function as a secure context server for external AI desktop tools (such as Claude Desktop), enabling AI agents to read database schemas, inspect table structures, and construct queries through TablePlus's execution layer." | Positioned as a context-provider server, not a client — the direction is external AI agent → TablePlus, not TablePlus's own chat calling out to an MCP server. | Unverified | S1 | Engine-agnostic wording ("database schemas," "table structures") is the closest this section comes to explicitly including MongoDB; still not itemized by name. |
| AI-mcp-client | MCP client support | Unverified — per secondary source, no primary citation | S1's diagram (Section 8) shows Claude Desktop and "Custom Developer Agents" as the external consumers of TablePlus's MCP server. | Named external clients: Claude Desktop; "custom developer agents" is generic. | Unverified | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- None reach the Confirmed bar (no inline citations in the source for any AI claim).

### Confirmed limitations

- None stated as explicit confirmed-absences specific to F-AI — the source presents TablePlus's AI/MCP posture positively throughout, without naming an absent AI capability the way it does for F-SCHEMA/F-SQL/F-SHELL/F-SCHED.

### Open questions / unknowns

- Whether any of BYOK natural-language generation, Copilot inline completion, or DeepSeek error-fixing actually operates against MongoDB/MQL, given the source's own wording names SQL specifically for two of the three and is ambiguous (not explicitly SQL-only, but not explicitly MongoDB-inclusive either) for the third.
- Whether the native MCP server exposes MongoDB schema/collection metadata specifically, or only relational table/schema metadata — the wording is generic enough to plausibly include MongoDB but does not name it.
- Whether TablePlus's own chat interface (if any) can act as an MCP client consuming external MCP servers, or whether its MCP support is exclusively in the server (context-provider) direction.
