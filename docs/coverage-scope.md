# Coverage scope: 3T products tracked by the silo but not analysed

**Status: DECIDED — approved by the owner on 2026-09-25 (issue #16).**

`prod_info_silo` tracks 12 3T products that this repository does not analyse. This record decides each one, so the weekly triage (#18) can skip excluded products without re-raising them.

Evidence per product: release status, track and description from `prod_info_silo/config/products.yaml`; document counts and feature tags from `prod_info_silo/data/catalog_index.json` (silo commit `cde319c742`).

The *Docs* column records the silo's catalog count at the decision (silo `cde319c742`). Current counts: [silo snapshot](../reports/silo-snapshot.md).

**Revisit triggers are machine-checked.** The *Revisit trigger* column is encoded in [`coverage-triggers.toml`](coverage-triggers.toml) and checked by [`tools/scope-triggers`](../tools/scope-triggers/README.md) (`uv run tools/scope-triggers/triggers.py`, exit 1 if any fired). Out-of-scope rows fire only when the entry itself goes stale (the product leaves the snapshot, stops being a 3T product, or gains an analysis folder); a status change that is not a trigger is listed as *noted, no action*. A new 3T silo product with no decision also fires. Change the table and the TOML together; a test checks they match.

## Decision rule

A product is **in scope** when it is (a) *shipped* and (b) exposes MongoDB-facing capabilities that map onto our Feature IDs. When a shipped component only exists **inside** a product already analysed here, it is covered on that product's pages rather than getting its own product folder. Anything not shipped is **revisit later**, with an explicit trigger. Infrastructure and websites are **out of scope**.

## Decisions

| Product | Silo status | Docs | Decision | Reason | Revisit trigger |
|---|---|---|---|---|---|
| `policy-engine` | Shipped | 492 | **In scope — inside 3T Lens** | Governance engine "embedded in Lens / proxy"; its capabilities (policy templates, alert channels, index suggestions) are already rows `GOV-002`, `GOV-003`, `GOV-006` (Supported) in the 3T Lens governance matrix | If it ships as a standalone product |
| `pii-scanner` | Shipped | 23 | **In scope — inside 3T Lens and 3T MCP** | Ships as `scan-pii` in 3T MCP and as the Lens PII Detector; already covered on the 3T Lens governance matrix (`GOV-004`, Supported) and the 3T MCP pages | If it ships as a standalone product |
| `studio-3t-ee` | Alpha | 1,779 | **Revisit later** — then inside Studio 3T | An edition of Studio 3T Desktop (central auth via Access Manager), not a separate product; 50 of its 94 source URLs are Studio 3T/website pages | Status reaches GA → add edition notes to the Studio 3T pages |
| `interceptor-proxy` | Working PoC | 202 | **Revisit later** | Capability-bearing (F-GOV, F-CONN) but not shipped | Status becomes Shipped |
| `studio-3t-ai-chat` | Internal demo only | 38 | **Revisit later** | Not released to users | Released → assess against Studio 3T `F-AI` |
| `enterprise-data-suite` | Planned | 2 | **Revisit later** | Not built yet; 2 documents | Status becomes Shipped, or silo holds ≥ 20 documents |
| `cassandra-ui` | PoC | 15 | **Out of scope** | Apache Cassandra viewer — not MongoDB-facing | If this repository widens beyond MongoDB tools |
| `license-manager` | Live | 57 | **Out of scope** | Licensing and user management; no MongoDB-facing capability | — |
| `3t-cognito` | Live | 3 | **Out of scope** | Identity service | — |
| `3t-login-page` | Live | 10 | **Out of scope** | Hosted login UI | — |
| `3t-website-2026` | Live | 216 | **Out of scope as a product** | The marketing site. Its pages remain a *citation source* (studio3t.com) checked by `tools/silo-review` | — |
| `3t-internal-tools` | Live | 41 | **Out of scope** | Internal utilities, not a product | — |

## Amendment 2026-09-25

By owner decision, the rows these components map to (`GOV-002`–`GOV-009`) moved from 3T Lens to a new [Govern](../products/3t/govern/product-report.md) folder. Reason: studio3t.com/3t-lens/ returned 404 and the public site describes policy checks, drift alerts and governed agent access as the Govern track. Read "inside 3T Lens" below as "inside Govern"; the Govern matrix keeps 3T Lens as an alternative attribution. This is the one new product folder; the "no new product folders" consequence below is superseded for it.

## Consequences

- **No new product folders now.** The two in-scope components are covered on existing product pages (3T Lens, 3T MCP), so the cost is edits to existing matrices, not new analysis sets.
- **Follow-up for the in-scope components:** check the 3T Lens and 3T MCP pages actually cover the Policy Engine and PII Scanner capabilities the silo documents; any new claim enters as ❓ until a human verifies a source. Done in #30: [Policy Engine / PII Scanner coverage](../reports/policy-engine-pii-coverage.md) (3 contradictions, 16 gaps to verify).
- **Weekly triage (#18):** skip every *out of scope* product; for *revisit later*, check only the trigger column.

## Navigation

- [Products index](../products/README.md) · [3T products](../products/3t/README.md)
- [Feature dictionary](../feature-dictionary.md)
- [Policy Engine / PII coverage](../reports/policy-engine-pii-coverage.md) · [Taxonomy reconciliation](../reports/taxonomy-reconciliation.md) · [Review queue](../reports/review-queue.md)
