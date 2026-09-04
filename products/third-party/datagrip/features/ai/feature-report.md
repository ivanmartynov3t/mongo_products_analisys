# Feature Report — DataGrip / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: AI Features
- Feature ID: F-AI (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: DataGrip
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

DataGrip's AI strategy centers on a central AI chat interface embedding two autonomous agents: Anthropic's Claude Agent (built on the Anthropic Agent SDK, powered by Claude 4.5 Sonnet) and OpenAI's Codex. A developer authenticates one of these agents using an active JetBrains AI Pro subscription, an existing personal ChatGPT enterprise account, or a Bring-Your-Own-Key API token from OpenAI or Anthropic directly. This is a newer, more autonomous layer on top of a pre-existing baseline of inline SQL code completion, which the source mentions only in passing as the starting point DataGrip's AI strategy has since built past.

To let these agents act safely against a live database, JetBrains built a database-specific Model Context Protocol (MCP) server directly into DataGrip's IDE engine. The described operational flow is: a user issues a natural-language prompt in the AI Chat window; the active agent (Claude Agent or Codex) analyzes it and calls into DataGrip's internal MCP server; before anything executes, the request passes through an IDE permission layer requiring the user's explicit consent across one of four categories — Schema Access, Data Access, Schema Modification, or Data Modification; once approved, the MCP server executes the operation against the target database via standard JDBC drivers and streams results back as CSV, optimized for LLM token limits. Schema modifications made this way automatically trigger a background schema-tree refresh, and every AI-issued query is tracked in the same query history a human-typed query would appear in.

The MCP server itself exposes fourteen distinct tools, giving a fully enumerated picture of what the AI agents can do: enumerate connections (`list_database_connections`), provision and edit connections (`create_database_connection`, `edit_database_connection`), test connectivity (`test_database_connection`), walk schema structure (`list_database_schemas`, `introspect_schema`, `list_schema_object_kinds`, `list_schema_objects`, `get_database_object_description`), preview data (`preview_table_data`), and run and manage queries (`execute_sql_query`, `fetch_query_result`, `cancel_sql_query`, `list_recent_sql_queries`). This is a materially more granular, fully-named tool inventory than most competitor sources in this repository provide.

One architectural point is worth calling out explicitly because it is easy to over-read: the source describes this MCP server being used by DataGrip's *own* embedded Claude Agent/Codex chat, not by external MCP clients reaching into DataGrip. Unlike DBeaver's source material, which explicitly names external clients ("Claude Desktop or enterprise LLM agents") as consumers of DBeaver's exposed MCP server, DataGrip's source never makes that claim. This report treats DataGrip's MCP-client compatibility as unverified rather than assuming parity with DBeaver's or Studio 3T's externally-reachable MCP servers.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| AI-agentic-mode, AI-local-mcp, AI-mcp-tools | Native Claude Agent + OpenAI Codex, backed by a 14-tool internal MCP server — both independently confirmed via DataGrip's own 2026.1 release notes. | The deepest, most itemized agentic-AI architecture documented for any product in this repository's comparison set. | JetBrains "What's New in DataGrip 2026.1" (S1 Works Cited #4) |
| AI-mcp-client | The source's described flow is internal-only (IDE chat → IDE's own MCP server); no external-client access is claimed. | Prevents this repository from silently assuming DataGrip has the same "any MCP client can connect" model as DBeaver or Studio 3T. | Absence of any external-client statement in the research file's narrative |
| AI-safety-guards | A 4-category consent gate (Schema Access / Data Access / Schema Modification / Data Modification) is the most granular pre-execution AI approval model documented in this repository. | Meaningfully different UX from a single blanket "enable AI" toggle — worth flagging as a genuine design strength in competitive terms. | Research file narrative |
| AI-plan-req | AI Free / AI Pro Add-on ($100/yr individual, $200/yr organization) pricing independently corroborated by two JetBrains primary sources. | One of the better-evidenced pricing claims in this product's entire entry. | JetBrains DataGrip buy page (S1 Works Cited #13); JetBrains Toolbox store page (S1 Works Cited #15) |

## Constraints and risks

- Do not assume DataGrip's MCP server is reachable by third-party MCP clients (Claude Desktop, VS Code, Cursor) — the source's described architecture is internal-only, unlike DBeaver's or Studio 3T's externally-facing MCP surfaces.
- The 4-category consent model is described narratively but not tied to a dedicated primary source beyond the general 2026.1 "AI Agentic Flow" release-notes line; treat the exact wording/UX of the consent dialogs as the secondary source's own paraphrase.

## Interactions and dependencies

- AI-generated output executes through [F-SQL](../sql-tools/feature-report.md)'s `execute_sql_query` MCP tool — AI agents produce and run SQL text against MongoDB the same way a human user would (SQL-to-JS translation, no native MongoDB filter/pipeline output).
- Depends on [F-CONN](../connectivity/feature-report.md) for the underlying JDBC connection the MCP server's tools operate against.
- Conceptually adjacent to Studio 3T's own `AI-007`/`AI-008`/`AI-009` local MCP server capabilities and to DBeaver's MCP server exposure (see [feature-dictionary.md](../../../../../feature-dictionary.md)) — useful for direct competitive comparison in `reports/comparisons/`.

## Conclusions

### Strengths

- Most granular, fully-enumerated MCP tool inventory (14 named tools) documented for any product in this repository.
- Most structured pre-execution AI consent model documented in this repository (4 distinct categories vs. a single toggle).
- Multi-agent choice (Claude Agent, OpenAI Codex) with BYOK support and primary-source-corroborated pricing.

### Limitations

- AI-generated output is SQL text executed through DataGrip's SQL-to-JS translation layer, not a native MongoDB query/pipeline document.
- No confirmed external-MCP-client compatibility — architecture reads as internal-only per the source.

### Unknowns

- Whether DataGrip's MCP server can be reached by external MCP clients.
- Whether usage/token-consumption analytics accompany the consent gate (part of the dictionary's `AI-safety-guards` definition, not mentioned in the source for DataGrip).
- Implementation depth of the pre-agentic inline SQL code-completion baseline.
