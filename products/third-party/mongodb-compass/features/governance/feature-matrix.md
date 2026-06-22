# Feature Matrix — MongoDB Compass / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://www.mongodb.com/docs/compass/settings/read-only/
- S2: https://www.mongodb.com/docs/compass/settings/protect-connection-strings/
- S3: https://www.mongodb.com/docs/compass/settings/restrict-outgoing-connections/
- S4: https://www.mongodb.com/docs/compass/settings/telemetry/
- S5: https://www.mongodb.com/docs/compass/settings/config-file/
- S6: https://www.mongodb.com/docs/compass/settings/command-line-options/
- S7: https://www.mongodb.com/docs/compass/ai-and-data-usage-information/
- S8: https://www.mongodb.com/docs/compass/query-with-natural-language/compass-ai-assistant/
- S9: https://www.mongodb.com/docs/compass/faq/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-readonly-mode | Read-only mode | Supported with caveat | Hides write/delete UI capabilities. | Does not enforce DB-level read-only permissions; server-side enforcement still required. | Unknown | S1 | Role-based DB enforcement is still required. |
| GOV-cred-protection | Credential protection | Supported | Protect mode masks secrets and blocks direct edit/copy flows in UI. | Must be set in settings/CLI/config to enforce policy. | Unknown | S2, S6 | Reduces accidental credential disclosure. |
| GOV-network-policy | Outbound network restriction | Supported | Network traffic can be restricted to DB-only communication mode. | Disables certain network-backed features (for example maps). | Unknown | S3, S5 | Aligns with hardened environments. |
| GOV-telemetry | Telemetry governance controls | Supported | Telemetry behavior documented and configurable in settings/CLI/config. | Teams must define policy and default state explicitly. | Unknown | S4, S5, S6 | Telemetry fields are documented. |
| GOV-startup-policy | Centralized startup policy via config | Supported | EJSON/YAML config can set immutable startup behavior. | Config location and rollout are OS/deployment dependent. | Unknown | S5 | Useful for enterprise standardization. |
| GOV-cli-policy | CLI policy controls | Supported | Command-line options support enforcement of security/governance settings at launch. | Requires controlled launch process. | Unknown | S6 | Overrides some interactive settings paths. |
| GOV-ai-controls | AI data usage disclosure and controls | Supported with safeguards | AI features document what context is sent and allow disable/approval workflows. Explicit human approval required for assistant tool calls. | AI output is experimental; organizations may require disabling. | Subject to change | S7, S8 | Explicit human approval required for assistant tool calls. |
| GOV-cred-storage-os | OS credential storage model | Supported | Uses OS credential APIs (via Keytar) for secrets storage. | Security profile depends on host OS hardening. | Unknown | S9 | Applies to DB/SSH/TLS secrets. |
| GOV-isolated-edition | Isolated edition network model | Supported in edition variant | Isolated Edition restricts outbound requests to chosen MongoDB server only. | Edition-specific behavior. | Unknown | S9 | Alternative hardening path. |
