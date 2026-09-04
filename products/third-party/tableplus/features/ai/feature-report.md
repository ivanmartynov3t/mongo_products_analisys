# Feature Report — TablePlus / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: AI Features
- Feature ID: F-AI (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: TablePlus
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

TablePlus takes a bring-your-own-key (BYOK), vendor-neutral approach to AI rather than shipping a single proprietary assistant. A user supplies their own OpenAI or DeepSeek API credentials to enable natural-language-to-SQL generation, query optimization, and error troubleshooting inside the editor. Separately, native GitHub Copilot authorization provides inline SQL autocomplete-style suggestions while typing. A more recent DeepSeek integration adds tool-invocation capability, letting the assistant inspect the active schema context and propose fixes for invalid query syntax.

The most architecturally distinctive piece is native Model Context Protocol (MCP) server support: TablePlus can act as a context provider for external AI desktop agents (the source names Claude Desktop specifically), letting those agents read database schemas, inspect table structures, and construct queries through TablePlus's own execution layer. This is the reverse integration direction from a typical "AI chat inside the app" feature — TablePlus positions itself as infrastructure other AI tools can plug into, not primarily as a chat interface itself.

Every specific AI capability description in the source names SQL explicitly, except the DeepSeek "fix invalid query syntax" claim and the MCP server's engine-agnostic "database schemas"/"table structures" wording, which are ambiguous rather than confirmed MongoDB-inclusive. Given that TablePlus's MongoDB support is independently confirmed elsewhere in the source to lack a query-translation layer, a shell, and schema profiling, it would be a significant, unstated leap to assume the AI layer alone bridges the SQL/MongoDB gap that every other feature area does not.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| AI-providers | BYOK model supporting OpenAI and DeepSeek. | User controls cost and provider choice; no proprietary AI subscription lock-in. | S1 Section 8 |
| AI-inline-completion | GitHub Copilot authorization for inline SQL completions. | A real, named integration with a widely-used completion tool — but named as SQL-specific. | S1 Section 8 |
| AI-error-fix | DeepSeek tool invocation inspects schema context and fixes invalid query syntax. | The one AI description in the source not explicitly qualified as SQL-only, making it the most plausible (if still unconfirmed) candidate for MongoDB applicability. | S1 Section 8 |
| AI-local-mcp / AI-mcp-client | Native MCP server positions TablePlus as a schema/query context provider for external AI agents like Claude Desktop. | A structurally different AI integration than a built-in chat assistant — positions TablePlus as AI infrastructure, which the product-report.md's strategic-recommendations section (in the original research) explicitly cites as a competitive idea worth Studio 3T adopting. | S1 Section 8 |

## Constraints and risks

- No claim in this area traces to a primary-source citation; all findings are Unverified per this plan's classification rule.
- The BYOK NL-to-query and Copilot inline-completion claims name SQL explicitly — treating either as extending to MongoDB/MQL without further evidence would be an unsupported assumption.
- The MCP server's context-provider role has not been confirmed to expose MongoDB-specific schema metadata (as opposed to relational table/schema metadata only).

## Interactions and dependencies

- If AI-assisted query generation does extend to MongoDB, it would interact with the same generic query window used for MQL filters and aggregation pipelines (see [F-QUERY](../querying/feature-report.md) and [F-AGG](../aggregation/feature-report.md)).
- The MCP server's "construct queries through TablePlus's execution layer" wording implies it can trigger the same staged-commit review workflow documented under [F-GOV](../governance/feature-report.md), though this is not stated explicitly for AI-originated writes.

## Conclusions

### Strengths

- An open, multi-provider BYOK AI model plus a distinctive, forward-looking native MCP server positioning TablePlus as AI infrastructure rather than only an AI consumer.

### Limitations

- Every specific, named AI capability in the source is SQL-scoped; none is confirmed to generate, complete, or fix native MongoDB queries.

### Unknowns

- Whether any AI capability (NL generation, inline completion, or error-fixing) operates against MongoDB/MQL.
- Whether the MCP server's schema/table metadata includes MongoDB collections and BSON field types.
- Whether TablePlus enforces any AI-specific safety guardrail (confirmation before an AI-generated destructive action runs, usage/token analytics) — not discussed in the source, so `AI-safety-guards` is not scored in this matrix.
