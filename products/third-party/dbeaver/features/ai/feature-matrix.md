# Feature Matrix — DBeaver / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: DBeaver
- Product group: third-party
- Feature ID: F-AI (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `ai`
- Analysis date: 2026-09-04
- Version/release context: DBeaver 25.x–26.x line (source claims features added in "v25.2" and "v26.1.2" — see Notes on why these are marked Unverified despite specific version numbers)

## Source index

- S1: DBeaver Competitive Intelligence Analysis (secondary research file), `research/google_research/dbeaver-competitive-intelligence-analysis/DBeaver Competitive Intelligence Analysis.md`
- S2: DBeaver Enterprise Release notes, https://dbeaver.com/release-notes/ (S1 Works Cited #2 — general index, not a specific dated entry)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-nl-query | NL to query | Confirmed (as NL-to-SQL, not NL-to-MongoDB-filter) | S1: "Natural Language to SQL Generation: Translates plain-language user prompts into SQL statements by passing database schema metadata into the configured LLM." | Generates SQL, not a native MongoDB filter document — consistent with DBeaver's SQL-first MongoDB architecture (see [F-SQL](../sql-tools/feature-report.md)). | Unverified | S1 | Mapped to AI-nl-query as the dictionary's closest concept; the output is SQL text, which for a MongoDB connection is then translated by DBeaver's JDBC bridge, not a native filter document. |
| AI-schema-aware | Schema-aware | Confirmed | Same S1 sentence: "passing database schema metadata into the configured LLM." | — | Unverified | S1 | — |
| AI-providers | Provider support | Confirmed | S1: "Supported LLM integrations include OpenAI (with GPT-5 as the default model), Azure OpenAI Service, Google Gemini, and GitHub Copilot (incorporating Codex models for enterprise environments)." | Provider selection likely tier-gated (not itemized per-provider in S1). | Unverified | S1 | Broadest documented provider list among the products reviewed in this repository. |
| AI-sample-context | Sample context | Confirmed | S1: "Context-Aware File Attachments: Allows users to attach external structured files (CSV, JSON, Parquet, XLSX) directly into an AI Chat session. The AI parses the file schema, builds temporary in-memory tables, and executes natural language queries across the combined file and database context." | File-attachment context, not sampled documents from the live collection. | Unverified | S1 | Distinct mechanism from Compass/VisuaLeaf/Studio 3T's "sample documents from the query result" context model. |
| AI-voice-query | Voice input for AI queries | Unverified — per secondary source, no primary citation for the specific version | S1: "Speech-to-Text Voice Querying: Added in version 25.2, this feature includes speech recognition with audio visualization, pause detection, and transcription customization." | — | Unverified | S1 | S1's own Works Cited list of release notes (items #20–26) covers versions 24.2.5, 24.3.5, 25.0, 25.1.5, 25.3.5, 26.0.5 — none of which is exactly "25.2." The specific version claim cannot be traced to a listed primary source and is marked Unverified per this repository's stricter citation rule, even though the capability itself is plausible. |
| AI-mcp-client / AI-local-mcp | MCP server/client support | Unverified — per secondary source, no primary citation for the specific version | S1: "Model Context Protocol (MCP) Server Integration: Introduced in version 26.1.2, DBeaver can expose active database connections as Model Context Protocol (MCP) servers. This allows external AI agents (such as Claude Desktop or enterprise LLM agents) to query connected databases through governed tool interfaces." | — | Unverified | S1 | Same issue as AI-voice-query: "26.1.2" does not match any release-note entry in S1's own Works Cited (#20–26 top out at 26.0.5). |
| AI-safety-guards | AI execution safety guardrails | Unverified — per secondary source, no primary citation | S1: "Execution Safety Guards and Token Analytics: Provides real-time token tracking, response streaming, query cancellation controls, and prompt execution confirmation dialogs to prevent accidental execution of destructive DDL or DML statements." | — | Unverified | S1 | This DBeaver capability is the direct evidentiary basis for the new dictionary ID `AI-safety-guards` added in this same effort (2026-09-04). |
| AI-inline-completion | Inline AI code completion | Unverified | S1 mentions "GitHub Copilot (incorporating Codex models for enterprise environments)" as a supported LLM integration, which plausibly implies inline/autocomplete-style suggestions distinct from the conversational AI Chat, but S1 does not explicitly describe an inline-completion UX separate from the NL-to-SQL chat interface. | — | Unverified | S1 | Included because GitHub Copilot integration is named explicitly; not upgraded to Confirmed because S1 never describes the interaction model. |
| AI-plan-req / AI-plan-gate | Plan requirement | Confirmed | S1's pricing/edition table and licensing narrative state that AI assistance is one of several capabilities ("natural language AI assistance") used as a monetization catalyst for paid tiers, alongside NoSQL support and enterprise identity protocols. | — | Unverified (which specific tier gates which specific AI sub-capability) | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- Broadest documented LLM provider list among the products in this repository's comparison set (OpenAI, Azure OpenAI, Google Gemini, GitHub Copilot/Codex).
- Distinctive context-attachment model (CSV/JSON/Parquet/XLSX files parsed into temporary in-memory tables for combined file+database querying) not described for any other product in this repository.
- MCP server exposure of live connections is a real architectural investment in the same agentic-AI space Studio 3T's own MCP surface competes in — though the specific version number introducing it is unverified.

### Confirmed limitations

- AI-generated output is SQL, not a native MongoDB filter/pipeline document — consistent with DBeaver's SQL-first architecture, but a materially different mechanism from Compass/VisuaLeaf/Studio 3T's direct-to-MongoDB-query generation.
- Two headline 2026-era AI capabilities (speech-to-text voice querying, MCP server integration) are asserted with specific version numbers ("25.2," "26.1.2") that do not match any release-note entry in the research file's own Works Cited list — per this repository's classification rule, these are Unverified rather than Confirmed, despite reading as confident, specific claims in the source narrative.

### Open questions / unknowns

- Which AI sub-capabilities require which specific paid tier (Lite vs. Enterprise vs. Ultimate vs. Team).
- Whether inline/autocomplete-style AI code completion is a distinct UX from the conversational AI Chat, or just an implication of the GitHub Copilot integration.
- Whether AI-generated NL-to-SQL output is then further translated by DBeaver into a native MongoDB query, or executed as literal SQL against the JDBC bridge (source does not specify the execution path).
