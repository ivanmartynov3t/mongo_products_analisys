# Feature Report — Studio 3T / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T Desktop IDE's AI capabilities across two surfaces: the AI Helper (natural language query generation) and the Local MCP Server (the Desktop IDE acting as an MCP tool server for external AI clients over HTTP). Two related but separate products are documented independently: [3T MCP](../../../3t-mcp/features/ai/feature-report.md) (the standalone `stt-cli` binary, stdio transport) and [3T Explore](../../../3t-explore/features/ai/feature-report.md) (the browser IDE's AI Helper).

## Behavioral walkthrough

Studio 3T's AI Helper is a natural language assistant embedded in the Desktop IDE at three entry points: the Collection Tab query bar, IntelliShell, and the Aggregation Editor. Users type a plain-language question — "find all orders placed in the last 7 days where amount > 100" — and the AI Helper generates the corresponding MongoDB find query, aggregation pipeline stages, or shell script. The user reviews the result in the AI Helper panel, optionally modifies the prompt, and clicks "Change query" / "Change pipeline" / "Change script" to apply it directly to the active editor.

The AI Helper is backend-agnostic and supports three providers: Azure AI, OpenAI GPT-4o, and Anthropic Claude Opus 4.1. All three require external API keys — there is no bundled LLM or Studio 3T-hosted inference. Users bear the per-token cost of their chosen provider. A temperature control allows tuning the creativity vs. determinism trade-off; a global disable toggle provides an opt-out for teams that prefer not to use AI features. Session history with timestamps persists across app restarts, enabling review of prior AI conversations without re-querying.

The Local MCP Server is a fundamentally different capability: it turns Studio 3T itself into an MCP tool server that external AI coding assistants (VS Code + GitHub Copilot, Cursor, Claude Code, Claude Desktop, Cline, Gemini CLI) can call. The server runs on HTTP at `http://127.0.0.1:27117/mcp` (loopback only; no auth required), requires Studio 3T 2026.9+, and exposes 10 tools covering connection management, database/collection listing, find query execution, explain, schema analysis, index listing, collection statistics, and collection health assessment. All 10 tools are read-oriented — the MCP server does not expose write operations, limiting the blast radius of AI agent actions against production data.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| AI-003 | Multi-collection context building with field-level checkbox selection reduces token consumption and focuses AI prompts on relevant schema. | Practical for large schemas where sending all field names would exhaust context windows. |
| AI-007 | Local MCP Server on HTTP loopback (no auth required) is a simple integration path for any MCP-compatible client — no credentials to manage for local use. | Low friction for integrating with VS Code Copilot, Cursor, and Claude Code. |
| AI-008 | The `assess_collection_health` tool (indexing + shape consistency summary) is a high-level diagnostic not present in the lower-level individual tools. | Useful for AI agents performing autonomous MongoDB health checks. |

## Constraints and risks

- All three AI backends require external API keys; Studio 3T does not provide any LLM inference capability — cost and key management are entirely the user's responsibility.
- The Local MCP Server requires Studio 3T 2026.9+ — users on older versions have no Local MCP Server capability.
- The Local MCP Server requires Studio 3T to be running and the toggle enabled; it is not a persistent daemon.
- The Local MCP Server (HTTP) and [3T MCP](../../../3t-mcp/features/ai/feature-report.md) (stdio, separate product) have distinct transports and distinct capabilities; they are not interchangeable.
- AI-generated queries should be reviewed before execution; the AI Helper does not validate generated queries against the actual collection schema before inserting them into the editor.
- [3T Explore's AI Helper](../../../3t-explore/features/ai/feature-report.md) is a separate product; its availability and edition/plan requirements are **unknown/unverified**.

## Conclusion

Studio 3T Desktop IDE's AI features are organized across two distinct models: AI Helper (user-facing NL query generation in the IDE) and the Local MCP Server (machine-facing tool exposure to external AI agents over HTTP). The separation reflects different use cases — IDE productivity for developers vs. AI agent automation for coding environments. The read-only constraint on the Local MCP Server is a reasonable safety boundary. The dependency on external API keys for AI Helper and on Studio 3T 2026.9+ for the Local MCP Server are the main adoption constraints. The related [3T MCP](../../../3t-mcp/features/ai/feature-report.md) standalone binary and [3T Explore](../../../3t-explore/features/ai/feature-report.md) browser IDE AI Helper are separate products, documented in their own product folders.
