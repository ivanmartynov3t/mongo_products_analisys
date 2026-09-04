# Weekly Maintenance Prompts Guide

This directory contains executable prompt instructions designed for an AI agent performing recurring weekly maintenance on the MongoDB products competitive analysis repository.

## Directory Layout
- [`00-orchestrator.prompt.md`](00-orchestrator.prompt.md): The master entry point executing the three steps in sequence.
- [`01-verify-subfeatures.prompt.md`](01-verify-subfeatures.prompt.md): Step 1 — Verify 5–10 unverified sub-feature IDs against whitelisted primary vendor documentation.
- [`02-competitor-releases.prompt.md`](02-competitor-releases.prompt.md): Step 2 — Scan official competitor changelog and release endpoints across all published releases (no 30-day limit).
- [`03-sync-downstream-reports.prompt.md`](03-sync-downstream-reports.prompt.md): Step 3 — Cascade all matrix changes to low-level comparison, high-level comparison, gap analyses, and cumulative reports.

## How a Human Triggers Weekly Maintenance
Feed the following command/prompt to the agent:
> *"Run weekly maintenance using the instructions in `.github/prompts/weekly-maintenance/00-orchestrator.prompt.md`."*
