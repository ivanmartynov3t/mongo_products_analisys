# Feature Matrix — NoSQLBooster / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: NoSQLBooster
- Product group: third-party
- Feature ID: F-AI (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `ai`
- Analysis date: 2026-09-04
- Version/release context: v11.0–v11.1 line (AI Helper introduced v10.0, October 2025; custom LLM endpoints added v10.1)

## Source index

- S1: NoSQLBooster Competitive Analysis
- S2: NoSQLBooster Competitive Intelligence Analysis
- P1: nosqlbooster.com/features (primary; fetched directly by this review)
- P2: nosqlbooster.com/compareEditions (primary; fetched directly by this review)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-nl-query | NL to query | Confirmed | S1: "natural language query generation." P1 gives a worked example: `Find movies directed by Christopher Nolan and released after 2005` → a generated `db.movies.find(...)` call. | Requires active Software Assurance — see `AI-plan-gate`. | N/A | S1, S2, P1 | — |
| AI-schema-aware | Schema-aware | Confirmed | S1: "schema-aware query building." S2: "the AI Helper allows users to selectively pass schema metadata—including collection structures, field data types, and index definitions—to the underlying model." P1 itemizes exactly: database names, collection names, field names/types, index information. | User-configurable, per P1 ("Users can configure exactly what schema information to include"). | N/A | S1, S2, P1 | — |
| AI-explanation | Query explanation | Confirmed | S1: "step-by-step logic explanations for complex aggregations." S2: "step-by-step code explanation." P2 lists a distinct "Mongosh script explanation" row under AI Based Services. | — | N/A | S1, S2, P2 | Framed by the sources as a distinct, on-demand action rather than an always-attached explanation on every AI output — `AI-explanation`'s "always included" framing is not confirmed as the behavior here. |
| AI-providers | Provider support | Confirmed | S1: "operates out of the box without requiring external API key configuration" (managed backend). S2: "Enterprise environments requiring strict data governance can override the default cloud backend by configuring custom LLM endpoints, such as private OpenAI or Azure OpenAI instances." P1 corroborates: "Users can also configure their own AI API endpoints for custom deployments." | Custom endpoint override introduced v10.1 per both files' release-history tables. | N/A | S1, S2, P1 | — |
| AI-plan-gate | AI plan gate | Confirmed — a defining characteristic of this product | S1: "cloud-dependent Generative AI capabilities... are gated behind active Software Assurance contracts," repeated across the pricing table for every tier. P2's own AI Based Services table section header reads "(Active Software Assurance Required)." | Applies even to otherwise-perpetual Personal/Commercial licenses. | N/A | S1, S2, P2 | This gating model — perpetual core product, subscription-gated AI — is a recurring theme across both files' pricing and user-sentiment sections and is called out as a specific point of user frustration. |
| AI-safety-guards | AI execution safety guardrails | Unverified (thin) | P2 lists a distinct "Auto-execute mongosh readonly script" row/toggle under AI Based Services, and P1 describes it: "When enabled, read-only mongosh queries will be automatically executed... results displayed." | — | N/A | P2, P1 | Weaker fit than DBeaver's/DataGrip's explicit pre-execution confirmation-dialog guardrails: the evidence here is an opt-in auto-execute behavior scoped specifically to read-only AI-generated scripts (implying write-scripts are not auto-executed), not a documented confirmation dialog. Marked Unverified rather than Confirmed given how much thinner this evidence is than the dictionary ID's "pre-execution safety checks... plus usage/token consumption analytics" definition calls for — no token-analytics claim is made anywhere in the sources reviewed. |

## Feature-level conclusion

### Confirmed strengths

- A zero-configuration AI Helper (no user API key required by default) with schema-aware query generation, itemized to exactly which metadata categories (DB/collection/field/index) the user opts to share — a more granular privacy control than several other products reviewed in this repository disclose.
- Enterprise-friendly custom LLM endpoint override (private OpenAI / Azure OpenAI) for organizations that cannot send schema metadata to a third-party managed backend.

### Confirmed limitations

- Generative-AI features require an active Software Assurance subscription even on an otherwise-perpetual license — confirmed as a defining, recurring theme across both files' pricing tables and user-sentiment sections, not a minor footnote.
- No confirmed AI-assisted error-correction action ("Fix Query with AI"-style), inline AI code completion, or voice input — none of these are described in either source file for NoSQLBooster, unlike Navicat's confirmed "Fix Query with AI" action documented elsewhere in this repository.

### Open questions / unknowns

- The exact target-language roster for the AI Helper's own "cross-language script translation" action, as distinct from the separately-confirmed 8-target deterministic Query Code Generator — see `product-report.md`'s "Two-file reconciliation" point 2 and `features/querying/feature-matrix.md`.
- Whether the "Auto-execute mongosh readonly script" toggle constitutes the kind of pre-execution safety-check-plus-usage-analytics behavior `AI-safety-guards` fully describes, or is a narrower convenience toggle — this matrix treats it as thin, Unverified evidence rather than a confirmed match.
