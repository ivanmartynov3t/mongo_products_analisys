# Feature Matrix — TablePlus / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: TablePlus
- Product group: third-party
- Feature ID: F-GOV (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `governance`
- Analysis date: 2026-09-04
- Version/release context: 2026 release line

## Source index

- S1: TablePlus Competitive Intelligence Analysis (secondary research file, no inline per-claim citation markers), `research/google_research/tableplus-competitive-intelligence-analysis/TablePlus Competitive Intelligence Analysis.md`

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-staged-commit | Staged pending-changes review | Unverified — per secondary source, no primary citation, but a detailed and specific description | S1 (Sections 4, 6, 7): "Staged Commit Model: Visual edits made within the data grid are queued as staged changes. Users must explicitly review pending DML/DDL statements (⌘+Shift+P / Ctrl+Shift+P) before committing them to the host server." Modified cells are highlighted yellow, deleted rows red, new entries green. | Applies to grid-based edits; whether it applies identically to any programmatic/scripted MongoDB write is not stated (TablePlus has no shell — see product-report.md). | Unverified | S1 | This is the direct evidentiary basis for `GOV-staged-commit` being minted in this dictionary during this five-product effort — one of the clearest, most specific, and most consistently-repeated capability descriptions anywhere in the source (named in four separate sections). |
| GOV-protect-mode | Protect mode | Unverified — per secondary source, no primary citation | S1 (Sections 4, 10): "Safe Mode and Tagging Controls: ...Flagging a connection enforces Safe Mode, which disables auto-commits and prompts for manual confirmation before executing destructive operations." / "Environment Tagging and Safe Mode: Connections tagged with high-risk environment colors... automatically enforce Safe Mode, requiring manual user verification before running destructive DROP, TRUNCATE, or DELETE statements." | Triggered by connection color-tagging (see [F-CONN](../connectivity/feature-matrix.md), `CONN-color-coding`); DROP/TRUNCATE/DELETE are named as example relational operations — MongoDB-equivalent destructive operations (e.g., `dropCollection`, `deleteMany`) are not explicitly named. | Unverified | S1 | — |
| GOV-readonly-mode | Read-only mode | Unverified — per secondary source, no primary citation | Implied by the same Safe Mode description above ("disables auto-commits"); not described as a separate, standalone read-only toggle independent of Safe Mode. | — | Unverified | S1 | Treated as the same mechanism as `GOV-protect-mode` rather than a distinct, separately-triggerable read-only lock — the source does not describe a per-connection read-only toggle independent of the color-tag/Safe-Mode pairing. |
| GOV-rbac-users / GOV-rbac-roles | RBAC user/role management | Confirmed absent | S1 (Section 11): "Lack of Enterprise Governance: TablePlus does not provide real-time co-authoring, centralized cloud connection vaults, role-based access control (RBAC), or enterprise audit logging." | — | Confirmed absent | S1 | Direct, explicit statement. |
| GOV-audit-log | Audit logging | Confirmed absent | Same citation as above — "enterprise audit logging" named explicitly as absent. | — | Confirmed absent | S1 | — |
| GOV-secrets-vault | External secrets manager integration | Confirmed absent | Same citation as above — "centralized cloud connection vaults" named explicitly as absent; Section 10 separately confirms credentials are stored only locally, never synced to any TablePlus-operated cloud service. | — | Confirmed absent | S1 | — |
| GOV-data-masking | Data masking | Confirmed absent | S1 (Section 18, "Missing Functionality"): "No Dynamic Data Masking: Lacks native data obfuscation capabilities to sanitize sensitive production records during export or viewing." | — | Confirmed absent | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- None reach the Confirmed bar (no inline citations in the source), but `GOV-staged-commit` and `GOV-protect-mode` are described with unusual specificity and internal consistency (repeated, matching detail across multiple independent sections of the same document), which is the strongest secondary-source signal available in this review without a primary citation.

### Confirmed limitations

- No RBAC, no enterprise audit logging, no centralized cloud connection vault, and no dynamic data masking (all confirmed absent by direct statement).

### Open questions / unknowns

- Whether Safe Mode's destructive-operation detection recognizes MongoDB-native destructive operations (`dropCollection`, `dropDatabase`, `deleteMany`) given the source's own examples are all relational (DROP, TRUNCATE, DELETE statements).
- Whether the staged-commit review mechanism generates and displays actual MQL for a MongoDB write the way it displays SQL DML/DDL for relational writes — the source's own wording ("pending DML/DDL statements... generated SQL or MQL statements") suggests both are shown, but does not show a worked MongoDB example.
- Whether any per-connection read-only lock exists independent of the color-tag/Safe-Mode pairing.
