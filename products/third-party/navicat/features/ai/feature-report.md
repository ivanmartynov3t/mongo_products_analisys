# Feature Report — Navicat / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: AI Features
- Feature ID: F-AI (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: Navicat
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

Navicat's generative AI capabilities were introduced starting with Version 17, and are organized around two named tools embedded in the query workspace: "Ask AI" and "Fix Query with AI."

"Ask AI" is a natural-language interface: a user types a plain-English request (the source's own example: "Find all customers who made purchases above $500 in Q3 and group them by region"), and the AI Assistant generates the corresponding query — the source explicitly states this can be "the corresponding SQL statement or MongoDB MQL query," meaning that for a MongoDB connection the generated output is native MQL, not a SQL string requiring further translation. This distinguishes Navicat from DBeaver and DataGrip, both of which (per this repository's own entries for those products) generate only SQL text regardless of the target engine. The engine incorporates "active schema context — including database names, collection definitions, field names, and data types" to keep generated queries aligned with the live schema; there is no mention of sample-document context (as opposed to schema-only context) being used.

"Fix Query with AI" targets query debugging: when a query fails due to syntax errors, invalid field references, or type mismatches, triggering the action returns an error explanation alongside corrected code. The same engine also offers query tuning recommendations and automated code formatting. This maps directly and specifically to the newly-added `AI-error-fix` dictionary ID, whose description — "takes a failing/erroring query or script and returns a corrected version with an explanation of the fix, distinct from generating new queries from natural language" — matches this Navicat mechanism precisely.

Beyond the two named tools, the source describes a savable, pinnable custom AI prompt template library: "Users can create, customize, and save tailored AI prompt templates (e.g., 'Convert SQL query to MongoDB Aggregation' or 'Explain Query Execution Plan'). Frequently used actions can be pinned directly to the primary toolbar for quick access." No existing dictionary ID captured this specific mechanism (a user-curated, toolbar-pinnable library of reusable AI prompts, distinct from model selection, NL-to-query generation, or error-fix), so a new ID — `AI-prompt-templates` — was minted for it in this same effort, per the dictionary's naming rules. The source also names multi-model response comparison ("the platform also supports multi-model response comparisons, enabling users to evaluate answers generated across different underlying AI models") as a distinct capability, though it does not name any specific underlying model or provider anywhere.

On plan-gating: Navicat's own pricing pages (Works Cited #9 for Navicat Premium, #16 for Navicat for MongoDB) list "AI Assistant" as an included capability on the Navicat Premium 17 Perpetual License and the Navicat for MongoDB Perpetual (Enterprise) tier, but the Navicat for MongoDB Standard ($299) row's abbreviated capability description ("Excludes advanced capabilities like Structure Sync or Data Modeling") does not explicitly name AI Assistant as excluded — so the Standard-tier exclusion is inferred from the row's silence, not stated outright.

The only statement in the source bearing on AI data-privacy handling is not a factual claim about Navicat at all: it appears in the research file's own forward-looking "Strategic Product Opportunities" section, framed as marketing advice to Studio 3T ("Marketing messaging should emphasize that while Navicat's AI exposes raw schema metadata to third-party endpoints, Studio 3T safely bridges LLMs..."). This is the secondary research file's own competitive-positioning language, not something traceable to a Navicat primary source in its own Works Cited — it is treated as Unverified accordingly, despite its confident phrasing.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| AI-nl-query | Generates native MongoDB MQL (not just SQL) from plain-English input, with schema-context injection. | A genuinely MongoDB-native NL-to-query capability, stronger than DBeaver's/DataGrip's SQL-only AI output for MongoDB users specifically. | Research file's AI Features and Assistance Ecosystem section |
| AI-error-fix | "Fix Query with AI" — dedicated failing-query diagnosis and correction workflow with explanation. | Direct evidentiary basis for the new `AI-error-fix` dictionary ID; a genuinely useful developer-debugging workflow distinct from NL-to-query generation. | Same section |
| AI-prompt-templates | Savable, toolbar-pinnable custom AI prompt template library. | New dictionary ID minted specifically for this Navicat capability — no prior ID covered a curated reusable-prompt library. | Same section |
| AI-plan-req / AI-plan-gate | AI Assistant is a named included capability on Navicat Premium and Navicat for MongoDB Enterprise pricing pages; not itemized for the Standard tier. | A rare case in this report where a primary source (Navicat's own store pages) directly backs the claim, rather than resting solely on the secondary research file. | Navicat Premium Price Plan, Navicat for MongoDB Price Plan (S2, S3) |
| AI-privacy | Only source statement is the research file's own competitive-marketing framing about Navicat's third-party data exposure, not a primary-sourced factual claim. | Cannot be scored Confirmed under this repository's stricter citation rule; a genuinely open question about Navicat's actual AI data-handling practices. | Research file's Strategic Product Opportunities section |

## Constraints and risks

- No AI provider or underlying model is named anywhere in the source for Navicat — a materially thinner disclosure than DBeaver's (OpenAI, Azure OpenAI, Google Gemini, GitHub Copilot) or DataGrip's (Claude Agent, OpenAI Codex) explicit provider lists.
- The Navicat for MongoDB Standard tier's AI Assistant availability is inferred (not stated) to be excluded; treat this as an open question, not a confirmed edition boundary.
- The AI-privacy claim sourced from the research file's own marketing-recommendation language should not be repeated as fact in any customer-facing comparison without independent verification against a Navicat primary source.

## Interactions and dependencies

- "Ask AI" and "Fix Query with AI" both operate against the same active-schema-context mechanism described for the Data Editor and query workspace (see [F-QUERY](../querying/feature-report.md)).
- Multi-model response comparison and the prompt-template library are both workspace productivity features layered on top of the same underlying AI Assistant capability gated by edition (see Constraints above).

## Conclusions

### Strengths

- Genuine MongoDB-native NL-to-query generation (MQL output, not SQL-only), schema-context-aware.
- A dedicated, well-described AI error-correction workflow ("Fix Query with AI") — the direct basis for the new `AI-error-fix` dictionary ID.
- A distinctive, specifically-described savable/pinnable custom AI prompt template library — the direct basis for the new `AI-prompt-templates` dictionary ID.
- AI Assistant availability is confirmed via primary-sourced Navicat pricing pages for Premium and MongoDB Enterprise tiers.

### Limitations

- No AI provider/model roster, API key storage mechanism, sample-document context, or pre-execution safety guardrail is described anywhere in the source.
- The only AI-privacy-adjacent statement traces to the research file's own marketing framing, not a Navicat primary source — Unverified, not Confirmed.

### Unknowns

- Whether AI Assistant is genuinely excluded from the Navicat for MongoDB Standard tier.
- Underlying AI model/provider composition and API key handling.
- Whether inline/autocomplete-style AI code completion exists as a distinct UX from the two named conversational tools.
