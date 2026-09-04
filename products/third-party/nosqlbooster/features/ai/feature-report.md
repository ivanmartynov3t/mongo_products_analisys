# Feature Report — NoSQLBooster / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: AI Features
- Feature ID: F-AI (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: NoSQLBooster
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

NoSQLBooster's AI Helper, introduced in the v10.0 release (October 2025) and upgraded in v11.0, converts natural-language descriptions into mongosh queries — the vendor's own worked example converts "Find movies directed by Christopher Nolan and released after 2005" into a corresponding `db.movies.find({...})` call. It operates without requiring the user to configure an API key by default (a managed, zero-config cloud backend), and users can selectively opt individual categories of schema metadata (database names, collection names, field names/types, index information) into the prompt to improve generation accuracy — a more granular, itemized privacy control than most other products reviewed in this repository disclose. Since v10.1, enterprise users can override the default managed backend entirely with a custom LLM endpoint (private OpenAI or Azure OpenAI), addressing the class of organizations whose compliance policy prohibits sending database schema to a public third-party API.

A distinct, on-demand "Mongosh script explanation" action is confirmed as a separate capability from query generation itself — both files describe "step-by-step" explanation, and the vendor's own edition-comparison page lists it as its own row under "AI Based Services," alongside a distinct "Auto-execute mongosh readonly script" toggle (an AI-generated script that is read-only can, if the user enables the setting, run automatically; the implication, not explicitly confirmed, is that write-scripts require manual execution — treated here as thin evidence for `AI-safety-guards` rather than the fuller confirmation-dialog-plus-usage-analytics behavior that ID's definition anticipates).

The single most consequential fact about this feature area, confirmed and re-confirmed across both files' pricing tables, user-sentiment sections, and the vendor's own edition-comparison page (whose AI section is headed, verbatim, "Active Software Assurance Required"): every Generative-AI capability is gated behind an active Software Assurance subscription, even on an otherwise-perpetual Personal or Commercial license. Both files independently document user frustration with this — S1 lists "Software Assurance Gating for AI" as a distinct "Negative" sentiment row with "Moderate" discussion frequency, and S2's own "Acknowledged Weaknesses" section names "Gated Free Tier Functionality" and the broader tension between a "perpetual license" marketing pitch and a subscription-gated flagship feature.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| AI-schema-aware | The exact metadata categories a user can opt to share (DB/collection/field names and types/index info) are itemized precisely by the primary source. | A concrete privacy-control granularity claim, stronger evidence than a generic "schema-aware" assertion alone. | S1, S2, P1 |
| AI-plan-gate | Software-Assurance gating of AI features is the single most load-bearing constraint in this entire feature area, confirmed from three independent angles (pricing table, user sentiment, vendor's own page heading). | Materially undercuts the "perpetual license, no subscription" positioning both files otherwise use to frame NoSQLBooster favorably against Studio 3T's subscription model — this review flags the tension explicitly rather than letting the "perpetual licensing" strength claim go unqualified. | S1, S2, P2 |
| AI-safety-guards | Evidence is real but thin — an opt-in auto-execute-for-readonly-scripts toggle, not a documented pre-execution confirmation dialog or token-usage analytics. | Marked Unverified rather than Confirmed to avoid overstating parity with DBeaver's/DataGrip's more explicit, better-evidenced AI guardrail implementations documented elsewhere in this repository. | P1, P2 |

## Constraints and risks

- AI features are entirely unavailable without an active Software Assurance contract — this is not a "reduced capability" tier gate but a full on/off switch for the entire feature area, per S1's explicit statement that "the core desktop IDE remains functional, but managed AI features are disabled until renewal" if Software Assurance lapses.
- No AI-assisted error-correction action, inline AI code completion, or voice input is described in either source file — this review deliberately does not use the `AI-error-fix`, `AI-inline-completion`, or `AI-voice-query` dictionary IDs (all minted during this same five-product effort) for NoSQLBooster, since none has supporting evidence here, unlike Navicat's confirmed "Fix Query with AI" action.

## Interactions and dependencies

- AI schema-awareness draws on the same field/type metadata the Schema Analyzer (F-SCHEMA) computes via document sampling — the two features share an underlying schema-introspection mechanism per both files' descriptions.
- The AI Helper's "cross-language script translation" action is related to, but per this review's reconciliation work (see `product-report.md`) is distinct from, the deterministic 8-target Query Code Generator tracked under F-QUERY's `QUERY-export-lang` — the two should not be conflated when assessing NoSQLBooster's total code-generation language coverage.

## Conclusions

### Strengths

- Zero-config, schema-aware NL-to-query generation with granular, itemized metadata-sharing controls, plus an enterprise-friendly custom LLM endpoint override.

### Limitations

- All AI capabilities are gated behind an active Software Assurance subscription, a defining and user-criticized constraint even on perpetual licenses.
- No confirmed AI-assisted error correction, inline completion, or voice input.

### Unknowns

- Whether the "Auto-execute readonly script" toggle reflects a fuller pre-execution safety-check system than the sources describe.
- The AI Helper's own cross-language script-translation language roster (see F-QUERY's reconciliation notes).
