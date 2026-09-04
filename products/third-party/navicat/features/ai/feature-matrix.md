# Feature Matrix — Navicat / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: Navicat
- Product group: third-party
- Feature ID: F-AI (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `ai`
- Analysis date: 2026-09-04
- Version/release context: Navicat 17 (generative AI capabilities introduced starting with this major version, per the source's Release History section)

## Source index

- S1: Navicat Competitive Intelligence Analysis (secondary research file), `research/google_research/navicat-competitive-intelligence-analysis/Navicat Competitive Intelligence Analysis.md`
- S2: Navicat Premium Price Plan | Navicat Store, https://www.navicat.com/en/store/navicat-premium-plan (S1 Works Cited #9 — backs the "AI Assistant" line item in the pricing table)
- S3: Navicat for MongoDB Price Plan, https://www.navicat.com/en/store/navicat-for-mongodb-plan (S1 Works Cited #16 — backs the "AI Assistant" line item for the MongoDB-only Enterprise tier)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-nl-query | NL to query | Confirmed | S1: "The 'Ask AI' tool provides a natural language interface embedded directly within the query workspace. Developers and analysts can input questions in plain English... and the AI Assistant generates the corresponding SQL statement or MongoDB MQL query." | — | Unverified | S1 | Unlike DBeaver/DataGrip (SQL-only output), the source explicitly names "MongoDB MQL query" as a possible output — a genuine MongoDB-native NL-to-query capability, not merely a SQL-abstraction pass-through. |
| AI-schema-aware | Schema-aware | Confirmed | S1: "The engine incorporates active schema context—including database names, collection definitions, field names, and data types—to ensure generated queries align with the underlying database structure." | — | Unverified | S1 | — |
| AI-sample-context | Sample context | Unverified | Not discussed — S1 describes only schema-metadata context (names/fields/types) feeding the AI, not sample documents from the collection. | — | Unverified | S1 | — |
| AI-explanation | Query explanation | Confirmed | S1 (Feature Inventory): "...code optimization suggestions, query execution explanation, and custom prompt action pinning." Also (Fix Query with AI): "the AI action can be triggered to receive an error explanation alongside corrected code." | — | Unverified | S1 | Two distinct explanation surfaces: execution-plan/query explanation, and error explanation accompanying a fix. |
| AI-error-fix | AI-assisted error correction | Confirmed | S1: "Navicat includes the 'Fix Query with AI' utility for query debugging. When a query fails to execute due to syntax errors, invalid field references, or type mismatches, the AI action can be triggered to receive an error explanation alongside corrected code. The AI engine also offers query tuning recommendations and automated code formatting." | — | Unverified | S1 | This Navicat capability ("Fix Query with AI") is the direct evidentiary basis for the new dictionary ID `AI-error-fix` added in this same effort (2026-09-04) — its description matches this capability's mechanism precisely: takes a failing query, returns a corrected version with explanation, distinct from NL-to-query generation. |
| AI-models / AI-model-chooser | Model selection | Confirmed (existence); Unverified (which specific models/providers) | S1: "The platform also supports multi-model response comparisons, enabling users to evaluate answers generated across different underlying AI models." | No specific model or provider names (OpenAI, Anthropic, Azure, etc.) are given anywhere in the source for Navicat, unlike DBeaver's or DataGrip's itemized provider lists. | Unverified | S1 | — |
| AI-providers | Provider support | Unverified | Implied by "different underlying AI models" (multi-model comparison) but no specific provider integration is named anywhere in the source. | — | Unverified | S1 | Contrast with DBeaver (OpenAI, Azure OpenAI, Google Gemini, GitHub Copilot named explicitly) and DataGrip (Claude Agent, OpenAI Codex named explicitly) — Navicat's source gives no such itemized list. |
| AI-plan-req / AI-plan-gate | Plan requirement | Confirmed | S2 (Navicat Premium 17 Perpetual License row): "...AI Assistant, Cross-Platform activation." S3 (Navicat for MongoDB Perpetual (Enterprise) row): "MongoDB only, Visual Aggregation, Schema Analysis, BI, GridFS, AI Assistant." The Navicat for MongoDB Standard ($299) row does not list "AI Assistant" among its included capabilities. | AI Assistant is listed as an included capability on Navicat Premium (all tiers reviewed) and Navicat for MongoDB Enterprise; it is not listed for Navicat for MongoDB Standard, implying it is Enterprise/Premium-gated. | Unverified (whether Standard tier truly excludes it, vs. the pricing table simply not itemizing it) | S1 (pricing table), S2, S3 | Mapped cautiously: the pricing table's Standard-tier row description is "Excludes advanced capabilities like Structure Sync or Data Modeling," which does not explicitly name AI Assistant as excluded — inferred, not stated. |
| AI-key-storage | API key storage | Unverified | Not discussed — no mention of how (or whether) API keys for the underlying AI models are stored locally. | — | Unverified | S1 | — |
| AI-privacy | Privacy mode | Unverified — per secondary source, no primary citation | The only related statement is in S1's own forward-looking "Strategic Product Opportunities" section, framed as competitive-positioning advice to Studio 3T: "Marketing messaging should emphasize that while Navicat's AI exposes raw schema metadata to third-party endpoints, Studio 3T safely bridges LLMs and enterprise AI agents using field-level masking (3TL Bridge)..." | — | Unverified | S1 | This is the research file's own strategic-recommendation framing, not a factual claim traced to a primary Navicat source — it does not appear in S1's Works Cited as backed by any Navicat documentation. Treated as Unverified rather than Confirmed per the stricter citation rule; included because it is the only AI-privacy-adjacent statement in the source at all. |
| AI-prompt-templates | Custom AI prompt template library | Confirmed | S1: "Users can create, customize, and save tailored AI prompt templates (e.g., 'Convert SQL query to MongoDB Aggregation' or 'Explain Query Execution Plan'). Frequently used actions can be pinned directly to the primary toolbar for quick access." | — | Unverified | S1 | New dictionary ID minted for this capability (see feature-dictionary.md Changelog, 2026-09-04) — no existing F-AI sub-feature ID covers a savable/pinnable custom-prompt-template library; this is a distinct, specifically-described mechanism from NL-to-query generation, model selection, or error-fix. |
| AI-safety-guards | AI execution safety guardrails | Unverified | Not discussed — no pre-execution confirmation dialog, destructive-action guard, or token/usage analytics is described for Navicat's AI features anywhere in the source. | — | Unverified | S1 | Included as a row because this ID was added specifically for this cross-product effort; Navicat's source gives no evidence either way. |
| AI-inline-completion | Inline AI code completion | Unverified | Not discussed — S1 describes only the conversational "Ask AI" / "Fix Query with AI" interaction models, not an autocomplete-style inline suggestion UX. | — | Unverified | S1 | — |
| AI-voice-query | Voice input for AI queries | Unverified | Not discussed anywhere in the source for Navicat. | — | Unverified | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- A genuine MongoDB-native NL-to-query capability ("Ask AI"): the source explicitly names "MongoDB MQL query" as a possible generated output, not merely SQL — a materially different (and stronger, for MongoDB users) claim than DBeaver's or DataGrip's SQL-only AI output.
- "Fix Query with AI" is a well-described, dedicated error-correction workflow (syntax errors, invalid field references, type mismatches) with explanation-plus-corrected-code output, plus separate query tuning recommendations and automated code formatting — the direct evidentiary basis for the new `AI-error-fix` dictionary ID.
- Multi-model response comparison (evaluating answers across different underlying AI models) and a savable/pinnable custom AI prompt template library are both specifically described, distinctive capabilities.
- AI Assistant is confirmed as a named included capability on both Navicat Premium and Navicat for MongoDB Enterprise pricing pages (S2, S3) — a rare case in this Navicat report where a primary source (not just the secondary research file) directly backs the claim.

### Confirmed limitations

- No specific AI provider or model name (OpenAI, Anthropic, Azure, etc.) is given anywhere in the source, unlike DBeaver's and DataGrip's itemized provider lists — Navicat's AI backend composition is entirely unverified.
- No evidence of sample-document context injection (only schema metadata), API key storage mechanism, or pre-execution safety guardrails for destructive AI-generated actions.
- The only "AI privacy" statement in the source is the research file's own competitive-positioning claim ("Navicat's AI exposes raw schema metadata to third-party endpoints") made in service of a Studio 3T marketing recommendation — not traceable to a Navicat primary source, and therefore Unverified rather than Confirmed, despite reading as a factual assertion.

### Open questions / unknowns

- Whether AI Assistant is genuinely excluded from the Navicat for MongoDB Standard tier, or simply not itemized in that row's abbreviated capability list.
- Underlying AI model/provider roster and whether API keys are stored locally, transmitted through a Navicat-operated proxy, or configured directly against a third-party vendor.
- Whether any pre-execution confirmation or safety guardrail exists before an AI-generated query/fix is applied or executed.
- Whether inline/autocomplete-style AI code completion exists as a distinct UX from the conversational "Ask AI"/"Fix Query with AI" interfaces.
