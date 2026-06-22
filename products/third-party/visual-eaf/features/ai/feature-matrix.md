# Feature Matrix — VisuaLeaf / AI Features

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Shell Matrix](../shell/feature-matrix.md)
- [→ Governance Matrix](../governance/feature-matrix.md)

## Source index

- S1: https://visualeaf.com/docs/mongo-query
- S2: https://visualeaf.com/docs/settings

## Capability matrix

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| AI-nl-query | Natural language → MongoDB query | confirmed | Converts natural language input to find()-style query filter. | — | confirmed | S1 |
| AI-nl-pipeline | Natural language → aggregation pipeline | confirmed | Generates full multi-stage pipeline with correct operators from natural language. | — | confirmed | S1 |
| AI-explanation | Query explanation | confirmed | Every AI-generated query includes a plain-English explanation of what it does. | — | confirmed | S1 |
| AI-schema-aware | Schema-aware suggestions | confirmed | Uses collection field names and BSON types from live schema. | — | confirmed | S1 |
| AI-sample-context | Sample document context | confirmed | Optionally includes sample documents alongside schema for higher AI accuracy. | — | confirmed | S1 |
| AI-conversation | Conversation context | confirmed | Prior conversation turns used for iterative query refinements. | — | confirmed | S1 |
| AI-models | Model selection | confirmed | 11 OpenAI models: ChatGPT4o (recommended/gpt-4o), ChatGPT4oMini (gpt-4o-mini), ChatGPTo3Mini (o3-mini), ChatGPTo1 (o1), ChatGPTo1Mini (o1-mini), ChatGPTo1Preview (o1-preview), ChatGPT41 (gpt-4.1), ChatGPT41Mini (gpt-4.1-mini), ChatGPT4Turbo (gpt-4-turbo), ChatGPT4 (gpt-4), ChatGPT35Turbo (gpt-3.5-turbo). | Active config selected in Settings → AI Configuration. | confirmed | S2 |
| AI-providers | Provider support | confirmed/unknown | OpenAI confirmed in Settings documentation. Anthropic mentioned in product FAQ but absent from Settings docs; status unclear. | Anthropic support unverified. | unknown/unverified (Anthropic) | S2 |
| AI-privacy | Privacy mode | confirmed | "Send Sample Data ON" (schema + sample docs, labeled "Better Accuracy", green badge) vs "Send Sample Data OFF" (schema only, labeled "More Private", blue badge + yellow accuracy warning). | — | confirmed | S2 |
| AI-key-storage | API key storage | confirmed | sk-proj-… format; AES-masked in Settings UI; stored locally; never transmitted to SozoCode. | — | confirmed | S2 |
| AI-multi-config | Multiple AI configurations | confirmed | Multiple named AI configs supported (e.g., dev vs prod); enable/disable per config without deleting; active config selector in Settings. | — | confirmed | S2 |
| AI-plan-req | Plan requirement | confirmed | AI Assistant requires Professional plan ($149/year). | — | confirmed | S2 |
