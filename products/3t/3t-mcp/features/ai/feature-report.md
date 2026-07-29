# Feature Report — 3T MCP / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers 3T MCP (stt-cli), the standalone CLI binary providing read-only MongoDB access via stdio MCP transport. It is a separate product from the Studio 3T Desktop IDE's built-in Local MCP Server — see [Studio 3T's AI feature report](../../../studio-3t/features/ai/feature-report.md) — though both are part of the "Build" track per studio3t.com.

## Behavioral walkthrough

The 3T MCP standalone binary (stt-cli) is distributed via GitHub releases. Unlike the Desktop IDE's HTTP MCP server, stt-cli uses stdio transport and is intended to be configured as an MCP server in any stdio-compatible AI coding environment. It requires a 3T account (browser-based OAuth login) and runs entirely locally with no cloud intermediary. Its capability surface partially overlaps with the Desktop IDE's Local MCP Server but adds a PII scanner that identifies fields potentially containing personally identifiable information across collections.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| AI-010 | stdio transport is compatible with a wider range of AI coding environments than HTTP-only MCP servers. | Broader AI tool ecosystem coverage via the standalone binary. | studio3t.com/3t-mcp/ |
| AI-011 | PII scanner provides collection-level PII field identification — a governance-adjacent capability surfaced in a query-oriented tool. | Reduces manual field-by-field review for teams onboarding MongoDB collections to compliance programs. | studio3t.com/3t-mcp/ |

## Constraints and risks

- Requires a 3T account (OAuth login); credentials stored locally.
- stdio-only transport; HTTP-only clients need a bridge adapter.
- PII scanner uses name/pattern heuristics — results require human review and are not an authoritative compliance determination.

## Interactions and dependencies

- Complements, but is architecturally distinct from, the Studio 3T Desktop IDE's Local MCP Server (HTTP transport, AI-007–AI-009) — the two are not interchangeable.

## Conclusions

### Strengths

- Broadest AI-coding-environment compatibility in the 3T MCP ecosystem, via stdio transport.
- Local-only execution with no cloud intermediary for MongoDB data.

### Limitations

- Requires separate account/auth versus the Desktop IDE's Local MCP Server.

### Unknowns

- Pricing/licensing terms for the required 3T account.
