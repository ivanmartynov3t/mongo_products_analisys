# VisuaLeaf — AI Assistant Feature Report

## Summary

VisuaLeaf's AI Assistant (Professional plan only) integrates OpenAI models directly into the query and aggregation workflow. It converts natural language to find()-style queries and full multi-stage aggregation pipelines, provides plain-English explanations for every generated query, uses the live collection schema for context, and supports follow-up refinements through conversation history. 11 OpenAI models are configurable (from gpt-3.5-turbo to o1, o3-mini, and gpt-4.1), with a privacy toggle controlling whether sample documents are sent alongside the schema.

---

## Strengths

- **11 OpenAI model options:** From gpt-3.5-turbo to o1, o3-mini, gpt-4.1, and gpt-4o — users can balance cost vs. accuracy per use case.
- **Schema-aware generation:** Collection field names and BSON types ground the AI in the actual data model, reducing hallucinated field names.
- **Explicit privacy toggle with labeled modes:** Green "Better Accuracy" badge vs. blue "More Private" badge with yellow accuracy warning — makes the data/privacy trade-off visible and auditable.
- **Multiple named AI configurations:** Named configs (dev key / prod key, different models) with per-config enable/disable; Active Config selector supports environment switching.
- **Local API key storage:** Keys stored AES-masked locally; never transmitted to SozoCode servers.
- **Plain-English explanation on every generated query:** Forces understanding over blind copy-paste; reduces risky unreviewed query execution.
- **Aggregation pipeline generation:** Generates complete multi-stage pipelines — not just simple find() filters.

---

## Limitations / Gaps

- **Professional plan only:** $149/year barrier; no AI features on Community or Basic.
- **OpenAI only (confirmed):** No Anthropic, Azure OpenAI, Google Gemini, Ollama, or local model support confirmed.
- **Anthropic status unknown/unverified:** Mentioned in product FAQ but absent from Settings documentation — **unknown/unverified**.
- **No air-gapped AI:** AI features require outbound OpenAI API calls; breaks fully air-gapped deployments.
- **No AI for index creation or schema generation:** AI scope limited to queries and aggregation pipelines.
- **No feedback loop:** No thumbs-up/down mechanism to improve generation accuracy over time.
- **User pays OpenAI API costs:** No bundled AI call quota; users bear all OpenAI usage costs.
- **No self-hosted LLM support:** No Ollama, LM Studio, or OpenAI-compatible endpoint override documented.

---

## Comparison Notes (vs MongoDB Compass baseline)

| Aspect | VisuaLeaf | MongoDB Compass |
|---|---|---|
| AI query generation | **confirmed** (Professional) | not available |
| AI aggregation generation | **confirmed** (Professional) | not available |
| Query explanation | **confirmed** (every result) | not available |
| Schema-aware AI | **confirmed** | not available |
| Privacy control for AI data | **confirmed** (schema-only vs. schema+docs) | not available |
| Model selection | **confirmed** (11 OpenAI models) | not available |
| Multiple AI configs | **confirmed** | not available |
| Plan required | Professional ($149/year) | N/A |

---

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [← MongoDB Shell](../shell/feature-report.md)
- [→ Security & Governance](../governance/feature-report.md)
