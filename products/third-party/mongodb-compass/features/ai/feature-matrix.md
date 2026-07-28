# Feature Matrix — MongoDB Compass / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://www.mongodb.com/products/tools/compass

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| AI-nl-query | Natural language querying | Supported | Product page lists "Natural language query generation" as a core capability, alongside the query bar's "intuitive query operators." | Exact requirements (e.g., Atlas sign-in, MongoDB version, Compass version) are not stated on the source page. | confirmed | S1 |
| AI-nl-pipeline | Natural language → aggregation pipeline | Unknown | Not mentioned on the product page; the page describes the aggregation builder (stage-by-stage, automatic preview) without reference to natural-language pipeline generation. | — | unknown/unverified | S1 |
| AI-explanation | Query explanation | Unknown | Not mentioned on the product page. | — | unknown/unverified | S1 |
| AI-schema-aware | Schema-aware suggestions | Unknown | Not mentioned on the product page. | — | unknown/unverified | S1 |
| AI-sample-context | Sample document context | Unknown | Not mentioned on the product page. | — | unknown/unverified | S1 |
| AI-conversation | Conversation context | Unknown | Not mentioned on the product page. | — | unknown/unverified | S1 |
| AI-models | Model selection | Unknown | Not mentioned on the product page. | — | unknown/unverified | S1 |
| AI-providers | Provider support | Unknown | Not mentioned on the product page. | — | unknown/unverified | S1 |
| AI-privacy | Privacy mode | Unknown | Not mentioned on the product page. | — | unknown/unverified | S1 |
| AI-key-storage | API key storage | Unknown | Not mentioned on the product page. | — | unknown/unverified | S1 |
| AI-multi-config | Multiple configurations | Unknown | Not mentioned on the product page. | — | unknown/unverified | S1 |
| AI-plan-req | Plan requirement | Unknown | Not stated whether natural language querying requires MongoDB Atlas (vs. local/self-managed/Community Edition deployments). | — | unknown/unverified | S1 |

## Feature-level conclusion

### Confirmed strengths

- MongoDB Compass now offers natural language query generation (AI-nl-query) directly from its official product page — previously undocumented in this repository, which listed Compass as having no AI features at all.

### Confirmed limitations

- Only the existence of natural language querying is confirmed; depth of implementation (schema awareness, explanation text, model/provider choice, pipeline generation, privacy controls) is not detailed on the source page.

### Open questions / unknowns

- Does natural language querying require an Atlas connection/sign-in, or does it also work against local/self-managed MongoDB deployments?
- Which MongoDB Compass version introduced this capability?
- Is this feature available in all Compass distributions (including any offline/enterprise-restricted builds covered in the Governance report)?
