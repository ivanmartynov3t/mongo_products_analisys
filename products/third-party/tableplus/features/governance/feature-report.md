# Feature Report — TablePlus / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Governance & Security
- Feature ID: F-GOV (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: TablePlus
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

TablePlus's governance model is built around two connected, connection-scoped mechanisms rather than a centralized platform: a staged "pending changes" review workflow, and Safe Mode triggered by connection color tagging. Every grid edit — a cell change, a row deletion, a new row insert — is first queued locally as a pending change, visually flagged (yellow for modified, red for deleted, green for new), and only actually applied to the database once the user reviews and explicitly commits the generated write statement via a dedicated preview window (⌘+Shift+P / Ctrl+Shift+P). This staged-commit model is described consistently across four separate sections of the source (product positioning, feature inventory, UX architecture, and productivity shortcuts), making it the single most repeated and specific capability claim in the entire document — the direct evidentiary basis for this dictionary's `GOV-staged-commit` sub-feature ID, minted during this five-product effort.

Separately, tagging a connection with a high-risk color (conventionally red for production) automatically enforces Safe Mode: auto-commit is disabled, and destructive operations require manual confirmation before running. The source's own worked examples for "destructive" operations (DROP, TRUNCATE, DELETE) are all relational-SQL statements — it does not explicitly confirm that MongoDB-native destructive operations (dropping a collection or database, a broad `deleteMany`) trigger the same confirmation gate, though the general framing ("destructive operations," "before executing destructive operations") reads as intended to be engine-agnostic.

Beyond these two connection-level mechanisms, the source is explicit that TablePlus has no centralized enterprise governance layer at all: no RBAC, no audit logging, no cloud-hosted connection vault, and (separately, under "Missing Functionality") no dynamic data masking for sanitizing sensitive records during export or viewing.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| GOV-staged-commit | Grid edits queue as color-coded pending changes; the generated write statement is shown for review before commit. | A genuine, structural safeguard against accidental writes — distinct from a simple "are you sure?" dialog, since the actual statement is inspectable before it runs. | S1 Sections 4, 6, 7 |
| GOV-protect-mode | Color-tagged connections (e.g., red = production) auto-enable Safe Mode, disabling auto-commit and requiring manual confirmation for destructive operations. | Reduces the risk of an accidental destructive action against a flagged environment; a real, if connection-scoped, mitigation. | S1 Sections 4, 10 |
| GOV-rbac-users | No RBAC of any kind. | TablePlus is unsuitable as a shared, permission-differentiated team access point; all governance is per-user, local, and connection-scoped. | S1 Section 11 |
| GOV-data-masking | No dynamic data masking. | Exporting or viewing production data through TablePlus carries the same sensitive-data exposure risk as any unmasked client. | S1 Section 18 |

## Constraints and risks

- All governance is connection-scoped and local — there is no centralized policy, audit trail, or team-wide enforcement mechanism a security team could rely on across multiple developers' TablePlus installs.
- Safe Mode's destructive-operation detection is described only with relational examples (DROP/TRUNCATE/DELETE); MongoDB-specific destructive-operation coverage is inferred, not confirmed.
- No audit log means there is no record of what was changed, when, or by whom — a materially different governance posture than Studio 3T's, Navicat's, or DBeaver's Enterprise-tier audit logging.

## Interactions and dependencies

- Safe Mode's trigger condition is [F-CONN](../connectivity/feature-report.md)'s connection color tagging (`CONN-color-coding`).
- The staged-commit review surface is shared across all query/edit surfaces — [F-QUERY](../querying/feature-report.md)'s inline grid edits and any relational DML alike.

## Conclusions

### Strengths

- A genuinely distinctive staged-commit model, repeated and detailed consistently across the source, that structurally reduces accidental-write risk beyond a typical confirmation dialog.
- Safe Mode plus color tagging is a lightweight but real per-connection safety net for flagging high-risk (e.g., production) environments.

### Limitations

- No RBAC, audit logging, cloud connection vault, or data masking of any kind — TablePlus is confirmed to have none of the centralized governance surface enterprise buyers expect, by the source's own direct statement.

### Unknowns

- Whether MongoDB-native destructive operations are recognized by Safe Mode's confirmation gate the same way relational DROP/TRUNCATE/DELETE statements are.
- Whether a per-connection read-only lock exists independent of the color-tag/Safe-Mode pairing.
