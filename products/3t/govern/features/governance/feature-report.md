# Feature Report — Govern / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

Govern is the governance track of the 3T platform (studio3t.com, S1). This report covers the policy, alerting, PII, schema-history, performance and MCP-governance capabilities (`GOV-002`–`GOV-009`) that were documented under 3T Lens until 2026-09-25. Source numbers refer to the [feature matrix](feature-matrix.md#source-index).

## Behavioral walkthrough

Publicly, Govern checks delivered data against policy, controls access for humans and AI agents alike, and alerts when something drifts — a schema update, a broken pipeline rule, or a new collection with the wrong permissions (S1). AI agents calling data through MCP follow the same rules as people (S2).

The detail comes from two other places. The removed 3T Lens page (S3, last read 2026-07-29) described six policy-template categories, Slack/email/webhook alerts, PII scanning, versioned field history and document diffs, index recommendations and 59 MCP tools. Internal repository docs (S4–S12) add a compliance score and violations workflow, scheduled policy evaluation, named index checks, a four-bucket PII workspace with export and audit trail, and READ / WRITE / ADMIN gating of MCP tools.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| GOV-002 | Default template count differs between internal docs: 27 (S4) vs 26 (S5); a separate doc lists 21 global-scope policies (S6). | Any published count needs one agreed number. | S4, S5, S6 |
| GOV-003 | Drift alerting is public (S1); the channel list survives only in the removed page (S3) and internal docs (S4). | Channel claims cannot be cited publicly today. | S1, S3, S4 |
| GOV-004 | PII workspace is richer internally than publicly, but is cleared only for a design-partner beta (S9). | Do not present export, audit trail or masking as generally available. | S3, S4, S8, S9, S10 |
| GOV-005 | Only the removed page describes field history and document diffs. | Currently has no public source. | S3 |
| GOV-007 | Four tool counts in circulation: 59 (S3), 60 full, 40 lite, 41 power (S11, S12). | Which build ships with Govern is unknown. | S3, S11, S12 |
| GOV-008 | Compliance score, violations and retention exist only in internal docs. | Internal-only until published. | S4, S7 |
| GOV-009 | Scheduled evaluation ships internally; the blocking policy gate is still planned. | Keep the gate as roadmap. | S4, S5 |

## Constraints and risks

- Most detail rests on a removed page (S3) or on private repositories (S4–S12). Every such claim is marked in the matrix.
- The public site does not say which product delivers Govern (S1). This page may be merged back into 3T Lens or 3T Access once 3T clarifies.

## Interactions and dependencies

- [3T Lens](../../../3t-lens/product-report.md) — read-only governed workspace (S2); the previous home of these rows.
- [3T Access](../../../3t-access/product-report.md) — central roles; MCP agents follow its rules (S2).
- [3TL Bridge](../../../3tl-bridge/product-report.md) — Pipeline track; masking at source (S1) is covered there (`GOV-011`).

## Conclusions

### Strengths

- Public positioning is consistent: policy checks and drift alerts across humans and AI agents (S1, S2).

### Limitations

- Little of the detailed capability set has a current public source.

### Unknowns

- Product ownership of Govern; MCP tool count; default template count. See the matrix open questions.
