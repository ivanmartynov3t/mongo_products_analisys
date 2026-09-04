# Feature Matrix — DataGrip / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: DataGrip
- Product group: third-party
- Feature ID: F-AI (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `ai`
- Analysis date: 2026-09-04
- Version/release context: DataGrip 2026.1 (AI Agentic Flow introduced)–2026.2 line

## Source index

- S1: DataGrip Competitive Analysis Studio 3T (secondary research file), `research/google_research/datagrip-competitive-analysis/DataGrip Competitive Analysis Studio 3T.md`
- S2: What's New in DataGrip 2026.1, https://www.jetbrains.com/datagrip/whatsnew/2026-1/ (S1 Works Cited #4 — primary source for the AI Agentic Flow / 14-tool MCP server launch)
- S3: Buy DataGrip: Pricing and Licensing, Discounts - JetBrains Toolbox Subscription, https://www.jetbrains.com/datagrip/buy/ (S1 Works Cited #13 — primary source for AI Free / AI Pro Add-on pricing)
- S4: Monthly and yearly plans with JetBrains Toolbox, https://www.jetbrains.com/store/ (S1 Works Cited #15)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-agentic-mode | Agentic tool-calling mode | Confirmed | S1: "DataGrip natively incorporates autonomous AI agents—specifically Anthropic's Claude Agent (built on the Anthropic Agent SDK and powered by Claude 4.5 Sonnet) and OpenAI's Codex—directly into its central AI chat interface." Corroborated by DataGrip's own 2026.1 release notes (S2), which state the release "Introduced AI Agentic Flow with native Claude Agent and OpenAI Codex integration." | Requires an active JetBrains AI Pro subscription, a personal ChatGPT enterprise account, or a BYOK OpenAI/Anthropic API key. | Unverified (exact agent capability boundaries beyond what S1 describes) | S1, S2 | Reused from the dictionary's existing `AI-agentic-mode` ID (originally coined against Studio 3T's LangChain4j-based "AI Helper Plus"); the ID's general concept — an agentic, tool-calling chat mode distinct from single-shot NL-to-query generation — fits DataGrip's Claude Agent/Codex chat cleanly even though the description references a different product's implementation. |
| AI-local-mcp | Local MCP server | Confirmed | S1: "JetBrains extended its internal IDE engine with a database-specific Model Context Protocol (MCP) server," providing 14 tools (listed under `AI-mcp-tools` below). Corroborated by S2's 2026.1 release notes: "released 14 database tools for local MCP server." | Internal to DataGrip's own AI chat pipeline per the source's described flow (agent → DataGrip's internal MCP server → JDBC). | Unverified | S1, S2 | — |
| AI-mcp-tools | MCP tools count | Confirmed | S1 enumerates all 14 tools by name: `list_database_connections`, `create_database_connection`, `edit_database_connection`, `test_database_connection`, `list_database_schemas`, `introspect_schema`, `list_schema_object_kinds`, `list_schema_objects`, `get_database_object_description`, `preview_table_data`, `execute_sql_query`, `fetch_query_result`, `cancel_sql_query`, `list_recent_sql_queries`. | — | Unverified (whether the exact tool count/list has changed since S2's 2026.1 announcement) | S1, S2 | The most granular, itemized MCP tool inventory documented for any product in this repository's comparison set to date. |
| AI-mcp-client | MCP client compatibility | Unverified — source does not describe external client access | S1 describes only an internal flow: DataGrip's own embedded Claude Agent/Codex chat calls DataGrip's internal MCP server. Unlike DBeaver's source (which explicitly names external clients — "Claude Desktop or enterprise LLM agents" — connecting to DBeaver's exposed MCP server), S1 never states that a third-party MCP client (e.g., Claude Desktop, VS Code, Cursor) can connect to DataGrip's MCP server. | — | Unverified | S1 | Do not assume external-client compatibility by analogy to DBeaver or Studio 3T — the source's described architecture reads as internal-only (IDE chat → IDE's own MCP server), and this distinction is explicitly called out rather than silently upgraded. |
| AI-safety-guards | AI execution safety guardrails | Confirmed | S1: "the request passes through an IDE permission layer where the user grants explicit permission for schema reading, data previewing, schema modification, or data modification," across four categories: Schema Access, Data Access, Schema Modification, Data Modification. Also: "any schema modifications trigger automatic background introspection to refresh the database explorer tree instantly." | Consent categories are broader (schema/data read vs. write) than a single "confirm before destructive action" dialog. | Unverified (whether usage/token consumption analytics are also tracked, as the dictionary description's second clause implies — not mentioned in S1 for DataGrip) | S1 | The most granular (4-category) pre-execution AI consent model documented for any product reviewed in this repository to date — more structured than a single blanket approval toggle. |
| AI-inline-completion | Inline AI code completion | Confirmed (existence, pre-agentic baseline); Unverified (implementation depth) | S1's opening AI-strategy sentence: JetBrains "has embedded artificial intelligence deeply into DataGrip's operational model, shifting from basic inline SQL code completion to an open, multi-agent developer architecture" — confirming DataGrip had/has an inline AI code-completion capability distinct from, and predating, its newer agentic chat. | — | Unverified | S1 | Mentioned only in passing as a baseline the newer agentic features built on top of; no further detail (trigger UX, model used, autocomplete scope) is given. |
| AI-providers | Provider support | Confirmed | S1: agents are "Anthropic's Claude Agent... and OpenAI's Codex," authenticated via "an active JetBrains AI Pro subscription, existing personal ChatGPT enterprise accounts, or direct Bring-Your-Own-Key (BYOK) API tokens from OpenAI or Anthropic." | — | Unverified (whether additional providers beyond Anthropic/OpenAI are supported) | S1 | — |
| AI-plan-req / AI-plan-gate | Plan requirement | Confirmed | S1's pricing table: "AI Free tier included; AI Pro Add-on available at $100/yr (Individual) or $200/yr (Organization)." Independently corroborated by JetBrains' own DataGrip buy page (S3) and JetBrains Toolbox store page (S4), both of which document the AI Free/AI Pro tiering. | — | Unverified (exact feature-by-feature gating between AI Free and AI Pro) | S1, S3, S4 | Strongly evidenced via two independent JetBrains primary sources — pricing claims in this matrix are on firmer ground than most of DataGrip's other AI claims. |

## Feature-level conclusion

### Confirmed strengths

- The most granular, fully-enumerated MCP tool inventory (14 named tools) of any product reviewed in this repository, corroborated by a primary JetBrains release-notes citation.
- A structured, 4-category pre-execution consent model (Schema Access / Data Access / Schema Modification / Data Modification) — more granular than a single "AI enabled" toggle or blanket confirmation dialog.
- Multi-agent choice (Claude Agent vs. OpenAI Codex) with BYOK support, and AI pricing that is independently corroborated by two JetBrains primary sources.

### Confirmed limitations

- The source's described architecture is internal-only: DataGrip's own embedded chat talks to DataGrip's own MCP server. There is no confirmed evidence (unlike DBeaver or Studio 3T) that external MCP clients can connect to DataGrip's MCP server — this repository does not assume that capability by analogy.
- The 4-category consent gate's scope, per S1, does not mention usage/token consumption analytics, which the dictionary's `AI-safety-guards` description also covers — that half of the ID's definition is unverified for DataGrip specifically.

### Open questions / unknowns

- Whether DataGrip's MCP server is reachable by external MCP clients (Claude Desktop, VS Code, Cursor) or is wired for internal agentic-chat use only.
- Implementation depth of the pre-agentic inline SQL code-completion capability mentioned only in passing.
- Exact feature gating between the AI Free and AI Pro Add-on tiers.
