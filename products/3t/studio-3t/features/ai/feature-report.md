# Feature Report — Studio 3T / AI Features

**Last reviewed:** 2026-07-31 — see [research findings](../../../../../research/studio-3t-desktop-review-2026/08-ai-findings.md)

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

> **⚠️ Behavior-change alert (2026-07-31 review, time-sensitive):** As of release **2026.12.0 (17-Jul-2026)**, AI Helper is now **disabled by default** for all users, requiring explicit opt-in. This reverses the previously documented default-enabled/opt-out behavior described elsewhere in this report and in `feature-matrix.md` (AI-002). Confirmed via public changelog and `t3/utils/properties/v2/AISettingsStore.java` (`applyReconsentResetIfNeeded()`). This likely affects competitive-positioning language elsewhere in the repo (see note at the end of this report).

## Scope

This report covers Studio 3T Desktop IDE's AI capabilities across two surfaces: the AI Helper (natural language query generation) and the Local MCP Server (the Desktop IDE acting as an MCP tool server for external AI clients over HTTP). Two related but separate products are documented independently: [3T MCP](../../../3t-mcp/features/ai/feature-report.md) (the standalone `stt-cli` binary, stdio transport) and [3T Explore](../../../3t-explore/features/ai/feature-report.md) (the browser IDE's AI Helper).

## Behavioral walkthrough

Studio 3T's AI Helper is a natural language assistant embedded in the Desktop IDE at three entry points: the Collection Tab query bar, IntelliShell, and the Aggregation Editor. Users type a plain-language question — "find all orders placed in the last 7 days where amount > 100" — and the AI Helper generates the corresponding MongoDB find query, aggregation pipeline stages, or shell script. The user reviews the result in the AI Helper panel, optionally modifies the prompt, and clicks "Change query" / "Change pipeline" / "Change script" to apply it directly to the active editor.

The AI Helper is backend-agnostic and supports three providers: Azure AI, OpenAI GPT-4o, and Anthropic Claude Opus 4.1 (the underlying model lists also include several additional selectable OpenAI and Claude models beyond the documented defaults, and models can be fetched live from the provider once an API key is entered, since release 2026.5.0). All three require external API keys — there is no bundled LLM or Studio 3T-hosted inference. Users bear the per-token cost of their chosen provider. A temperature control allows tuning the creativity vs. determinism trade-off. **As of release 2026.12.0 (17-Jul-2026), AI Helper is disabled by default and requires explicit opt-in** — this is a reversal of the previously documented default-enabled/opt-out behavior; see the alert at the top of this report. Session history now supports **multiple named conversations** (not a single stream) with rename/delete/switch actions and LLM-generated auto-titling, persisted via Studio 3T's generic tab/workspace-state persistence (Session Restore) rather than a dedicated chat log, surviving app restarts.

The Local MCP Server is a fundamentally different capability: it turns Studio 3T itself into an MCP tool server that external AI coding assistants (VS Code + GitHub Copilot, Cursor, Claude Code, Claude Desktop, Cline, Gemini CLI — compatibility with these specific clients is a protocol-conformance claim from the vendor's own documentation, not independently verifiable from source) can call. The server runs on HTTP at `http://127.0.0.1:27117/mcp` (loopback only; no auth required, single-session — only one connected MCP client at a time), requires Studio 3T 2026.9+, is gated to the Ultimate edition (or trial), and exposes 10 read-oriented tools including `find_documents` (previously documented as `query`) and `get_collection_stats` (previously documented as `get_collection_statistics`) — corrected tool names per the 2026-07-31 source-code audit. All 10 tools are read-oriented — the MCP server does not expose write operations, limiting the blast radius of AI agent actions against production data.

A separate, newer agentic mode ("AI Helper Plus") and a set of previously undocumented capabilities were also found in the 2026-07-31 source-code audit; see the new subsections below.

## New capabilities found in the 2026-07-31 source-code audit

The following six capabilities were not present in the prior version of this report. Candidate dictionary IDs are proposed in `feature-matrix.md` (marked "PENDING DICTIONARY ADDITION") pending addition to `feature-dictionary.md`.

### AI Helper Plus — agentic tool-calling mode

A distinct, more advanced chat mode alongside the plain NL-to-query flow (AI-003), gated by `FeatureFlags.AI_HELPER_PLUS` (observed default **false** — feature-flagged off, not yet confirmed GA) and an `AppFeatures.AI_HELPER_PLUS` license entry. Backed by LangChain4j (`AiHelperPlusClientImpl.java`) rather than the raw provider SDKs used by the standard AI Helper. It reviews the entire conversation history each turn via a dedicated system prompt, uses a bounded chat memory (`MessageWindowChatMemory.withMaxMessages(10)`), calls tools against Studio 3T's own internal tool set plus an externally-installed official MongoDB MCP server (see below), supports parallel tool execution, and supports mid-execution tool cancellation. **Roadmap status: in-progress/pre-release as of the commits examined; treat as roadmap, not shipped-and-GA, until confirmed in a release build.**

### Bundled/offline official `mongodb-mcp-server` as an internal tool source

`t3/mcpserversupport/**` (not related to the in-process Local MCP Server despite the similar package area) installs and runs MongoDB Inc.'s own official `mongodb-mcp-server` npm package offline — a bundled Node runtime (win-x64/darwin-arm64 only) launching it as a stdio MCP client subprocess consumed by the AI Helper Plus agent, always forced read-only (`MDB_MCP_READ_ONLY=true`, pinned to version 1.2.0). This means the AI Helper Plus agent can draw on two separate MongoDB tool sources at once: Studio 3T's own native tool set and the official community MCP server. The integration is one-directional — Studio 3T consumes this external tool, it does not register itself with other MCP clients' configuration files. Gated by the same `FeatureFlags.AI_HELPER_PLUS` flag as AI Helper Plus above (observed default **false**). **Roadmap status: same as AI Helper Plus — in-progress/pre-release, no public changelog entry found; not confirmed GA.**

### Live tab-context-awareness registry

An internal-only tool (`list_connected_tabs`, annotated `@InternalTool` and explicitly excluded from the external MCP tool listing documented under AI-008) gives the in-app AI agent live awareness of which Studio 3T tabs are currently open — deliberately scoped to IntelliShell, Aggregation, and Collection View tabs — including the database/collection each tab is pointed at, kept in sync as tabs are renamed or closed. This lets the AI Helper know "the user is currently looking at collection X" without the user restating it, extending beyond what AI-003's "schema-aware" description previously conveyed. **Status: found in code (`KONG-10894` series) with no corresponding public changelog entry as of this review — treat as in-progress/roadmap or very-recently-shipped-but-unannounced, not confirmed GA.**

### AI-response chart rendering

AI Helper responses can now include rendered charts — pie, bar, horizontal-bar, and stacked-bar — drawn via an embedded JavaFX canvas inside the SWT chat view (`AiHelperChartRenderer.java`). The model is instructed via a prompt fragment to emit `chart`-fenced JSON blocks, capped at 4 charts per response, and this pairs naturally with schema-analysis/reporting requests (e.g., alongside the `analyze_schema` tool). This is a materially new output modality: the AI Helper was previously documented as a pure text/query generator. **Status: found in code with no corresponding public changelog entry as of this review — treat as in-progress/roadmap or very-recently-shipped-but-unannounced, not confirmed GA**, consistent with the corresponding row in `feature-matrix.md`.

### Multi-conversation support with delete and auto-titling

The Global AI Helper now supports multiple named conversations rather than one history stream, with rename/delete/switch actions, a cap of 10 sessions with oldest-session eviction, and LLM-generated automatic conversation titles (with retry/fallback) after the first user message. Shipped in release **2026.12.0 (17-Jul-2026)** per the public changelog ("Multiple conversations are now available"; "Added an option to Delete Conversation"). This materially extends the session-history description under AI-005 — persistence is confirmed to ride on Studio 3T's generic tab/workspace-state persistence mechanism (versioned state schema, currently v6, with a migration path from v5) rather than a dedicated chat-log store.

### Mismatch/guard-rail apply layer

A real safety layer sits between AI-generated output and the active editor when the user applies a result (AI-004): type-compatibility routing decides whether to open a new tab, show a blocking mismatch-confirmation dialog (when the generated code type doesn't match the active tab), or apply in place; a source-collection-mismatch check prompts for confirmation when the AI targeted a different collection than the one open; unsaved-changes protection prompts before an in-place overwrite; and generated find-query text is syntactically parsed and validated before being applied, with parse failures blocked behind an error dialog. This corrects the previous "no validation" framing under AI-004 — it is not schema-level (live field-type) validation, but it is a materially real guard-rail layer, not an absence of one.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| AI-002 | AI Helper is now **disabled by default** as of release 2026.12.0 (17-Jul-2026), reversing the previously documented default-enabled/opt-out behavior; a one-time forced re-consent reset runs on upgrade. | Adoption impact: existing users upgrading past 2026.12.0 will see AI Helper turned off until they explicitly re-opt-in; new users start with AI features off. Likely affects competitive-positioning language elsewhere in the repo — see note in Conclusion. |
| AI-003 | Multi-collection context building with field-level checkbox selection reduces token consumption and focuses AI prompts on relevant schema. | Practical for large schemas where sending all field names would exhaust context windows. |
| AI-004 | A real mismatch/guard-rail layer exists on the apply-to-editor path (type-routing, collection-mismatch and unsaved-changes prompts, query parse validation) — see subsection above. | Corrects the prior "no validation" framing; materially reduces (but does not eliminate) the risk of blindly overwriting editor content with AI output. |
| AI-005 | Session history has grown into multiple named conversations with delete and auto-titling (2026.12.0) — see "Multi-conversation support" subsection above. | Corrects the previously vague "local storage" framing; persistence is confirmed to ride on generic tab/workspace-state persistence (v6 schema), not a dedicated chat-log store. |
| AI-006 | The documented "Ctrl+Enter to send" shortcut is unverified and code suggests it may be backwards (plain Enter sends, Ctrl+Enter inserts a newline). | Recommend a manual UI check before publishing a corrected shortcut in user-facing docs. |
| AI-007 | Local MCP Server on HTTP loopback (no auth required, single-session) is a simple integration path for any MCP-compatible client — no credentials to manage for local use. Edition gate confirmed: Ultimate edition (or trial) only, not all editions. | Low friction for integrating with VS Code Copilot, Cursor, and Claude Code, but restricted to Ultimate-tier customers. |
| AI-008 | The `assess_collection_health` tool (indexing + shape consistency summary) is a high-level diagnostic not present in the lower-level individual tools. Tool names corrected: `find_documents` (not `query`), `get_collection_stats` (not `get_collection_statistics`). | Useful for AI agents performing autonomous MongoDB health checks; naming corrections matter for anyone scripting against the MCP tool names directly. |

## Constraints and risks

- All three AI backends require external API keys; Studio 3T does not provide any LLM inference capability — cost and key management are entirely the user's responsibility.
- **AI Helper is disabled by default as of release 2026.12.0 (17-Jul-2026)** — this is a reversal of previously documented behavior and is a material adoption constraint going forward: users must actively discover and enable the opt-in toggle.
- The Local MCP Server requires Studio 3T 2026.9+ and Ultimate edition (or trial) — users on older versions or lower editions have no Local MCP Server capability.
- The Local MCP Server requires Studio 3T to be running and the toggle enabled; it is not a persistent daemon; only one MCP client can be connected at a time (single-session).
- The Local MCP Server (HTTP) and [3T MCP](../../../3t-mcp/features/ai/feature-report.md) (stdio, separate product) have distinct transports and distinct capabilities; they are not interchangeable.
- AI-generated queries should still be reviewed before execution; while a real mismatch/guard-rail layer exists on the apply path (see subsection above), it does not perform schema-level (live field-type) validation against the actual collection schema.
- AI Helper Plus (agentic mode) and the bundled official MongoDB MCP server client are feature-flagged off by default and should be treated as roadmap/in-progress, not GA, pending confirmation in a shipping release.
- [3T Explore's AI Helper](../../../3t-explore/features/ai/feature-report.md) is a separate product; its availability and edition/plan requirements are **unknown/unverified**.

## Conclusion

Studio 3T Desktop IDE's AI features are organized across two distinct models: AI Helper (user-facing NL query generation in the IDE) and the Local MCP Server (machine-facing tool exposure to external AI agents over HTTP). The separation reflects different use cases — IDE productivity for developers vs. AI agent automation for coding environments. The read-only constraint on the Local MCP Server is a reasonable safety boundary. The dependency on external API keys for AI Helper and on Studio 3T 2026.9+ for the Local MCP Server are the main adoption constraints, now joined by the new **default-disabled** state of AI Helper since release 2026.12.0. The 2026-07-31 source-code audit also surfaced a materially more capable and more actively developed AI surface than previously documented — an agentic "AI Helper Plus" mode, a second internal MongoDB MCP tool source, live tab-context awareness, chart rendering in AI responses, multi-conversation support, and a real apply-time guard-rail layer — none of which were previously captured in this report. The related [3T MCP](../../../3t-mcp/features/ai/feature-report.md) standalone binary and [3T Explore](../../../3t-explore/features/ai/feature-report.md) browser IDE AI Helper are separate products, documented in their own product folders.

> **Note for central synthesis:** the AI Helper default-enabled → default-disabled reversal (2026.12.0, 17-Jul-2026) likely affects competitive-positioning language in `products/3t/studio-3t/product-report.md` and possibly `reports/comparisons/*` (e.g., any framing that credits Studio 3T with AI features being "on by default" or lower-friction to adopt than competitors). This report and `feature-matrix.md` have been corrected per the audit scope, but the product-report and comparison-report files were out of scope for this pass and were not modified — flagging here for a follow-up pass.
