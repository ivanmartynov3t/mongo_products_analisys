# VisuaLeaf — AI Assistant Feature Matrix

| ID | Capability | Status | Detail | Source |
|---|---|---|---|---|
| AI-001 | Natural language → MongoDB query | **confirmed** | Converts natural language input to find()-style query filter | https://visualeaf.com/docs/mongo-query |
| AI-002 | Natural language → aggregation pipeline | **confirmed** | Generates full multi-stage pipeline with correct operators | https://visualeaf.com/docs/mongo-query |
| AI-003 | Plain-English query explanation | **confirmed** | Every AI-generated query includes an explanation of what it does | https://visualeaf.com/docs/mongo-query |
| AI-004 | Schema-aware suggestions | **confirmed** | Uses collection field names and BSON types from schema | https://visualeaf.com/docs/mongo-query |
| AI-005 | Sample document context (optional) | **confirmed** | Optionally includes sample documents alongside schema for higher accuracy | https://visualeaf.com/docs/mongo-query |
| AI-006 | Conversation context for follow-up | **confirmed** | Prior conversation turns used for iterative query refinements | https://visualeaf.com/docs/mongo-query |
| AI-007 | Model: ChatGPT4o (recommended) | **confirmed** | gpt-4o; recommended default model | https://visualeaf.com/docs/settings |
| AI-008 | Model: ChatGPT4oMini | **confirmed** | gpt-4o-mini | https://visualeaf.com/docs/settings |
| AI-009 | Model: ChatGPTo3Mini | **confirmed** | o3-mini | https://visualeaf.com/docs/settings |
| AI-010 | Model: ChatGPTo1 | **confirmed** | o1 | https://visualeaf.com/docs/settings |
| AI-011 | Model: ChatGPTo1Mini | **confirmed** | o1-mini | https://visualeaf.com/docs/settings |
| AI-012 | Model: ChatGPTo1Preview | **confirmed** | o1-preview | https://visualeaf.com/docs/settings |
| AI-013 | Model: ChatGPT41 | **confirmed** | gpt-4.1 | https://visualeaf.com/docs/settings |
| AI-014 | Model: ChatGPT41Mini | **confirmed** | gpt-4.1-mini | https://visualeaf.com/docs/settings |
| AI-015 | Model: ChatGPT4Turbo | **confirmed** | gpt-4-turbo | https://visualeaf.com/docs/settings |
| AI-016 | Model: ChatGPT4 | **confirmed** | gpt-4 | https://visualeaf.com/docs/settings |
| AI-017 | Model: ChatGPT35Turbo | **confirmed** | gpt-3.5-turbo | https://visualeaf.com/docs/settings |
| AI-018 | API Key storage | **confirmed** | sk-proj-… format; AES-masked in UI; stored locally; never sent to SozoCode | https://visualeaf.com/docs/settings |
| AI-019 | Multiple AI configurations | **confirmed** | Multiple named AI configs supported (e.g., dev vs. prod); enable/disable per config without deleting | https://visualeaf.com/docs/settings |
| AI-020 | Active AI Config selector | **confirmed** | Settings → AI Configuration; select which enabled config is active | https://visualeaf.com/docs/settings |
| AI-021 | Privacy Mode: Send Sample Data ON | **confirmed** | Sends schema (field names + BSON types) + sample documents to OpenAI; labeled "Better Accuracy" (green badge) | https://visualeaf.com/docs/settings |
| AI-022 | Privacy Mode: Send Sample Data OFF | **confirmed** | Sends schema only (field names + BSON types); labeled "More Private" (blue badge + yellow accuracy warning) | https://visualeaf.com/docs/settings |
| AI-023 | AI Provider: OpenAI | **confirmed** | Confirmed in Settings documentation | https://visualeaf.com/docs/settings |
| AI-024 | AI Provider: Anthropic | **unknown/unverified** | Mentioned in product FAQ but absent from Settings documentation; status unclear | https://visualeaf.com/docs/settings |
| AI-025 | Plan requirement | **confirmed** | AI Assistant requires Professional plan ($149/year) | https://visualeaf.com/docs/settings |

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Shell Matrix](../shell/feature-matrix.md)
- [→ Security & Governance Matrix](../security-governance/feature-matrix.md)
