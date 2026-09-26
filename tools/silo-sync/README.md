# silo-sync

One local command for the weekly silo → analysis refresh (issue #40, Plan 08 P8). No CI needed.

```bash
tools/silo-sync/run.sh              # fetch the silo, regenerate every report, print a summary
tools/silo-sync/run.sh --no-fetch   # use the silo refs already fetched
SILO=/path/to/prod_info_silo tools/silo-sync/run.sh
tools/silo-sync/test_run.sh         # offline tests: arguments, inputs, exit codes, --silo forwarding
```

## Steps

| # | Step | Tool | Writes | Weekly issue |
|---|---|---|---|---|
| 1 | fetch `prod_info_silo` | `git fetch` in the silo | silo refs only | — |
| 2 | silo snapshot | [`silo-snapshot`](../silo-snapshot/README.md) | `reports/silo-snapshot.{md,json}` | #18 |
| 3 | scope triggers | [`scope-triggers`](../scope-triggers/README.md) (reads the new snapshot; skipped if step 2 failed) | nothing | #18 |
| 4 | staleness queue | [`silo-review`](../silo-review/README.md) | `reports/review-queue.md` | #17 |
| 5 | candidate signals | [`silo-candidates`](../silo-candidates/README.md) | `reports/silo-candidates.md` | Plan 09 |
| 6 | evidence batches | [`silo-candidates/batch.py`](../silo-candidates/README.md#evidence-batches) | `.local/silo-batches/` (gitignored; input for `/silo-port`) | Plan 09 |
| 7 | evidence gaps | [`evidence-gaps`](../evidence-gaps/README.md) (section 2 reads the new snapshot) | `reports/evidence-gaps.md` | prod_info_silo#47 |
| 8 | taxonomy check | [`taxonomy-reconcile`](../taxonomy-reconcile/README.md) `--check` | nothing | #18 |
| 9 | pin check | [`silo-pins`](../silo-pins/README.md) `check` | nothing | — |
| 10 | re-pin plan | [`silo-pins`](../silo-pins/README.md) `repin plan` | nothing: shows which unchanged pins could move; run `repin apply` yourself | — |

Every step reads the silo at `origin/main` from git objects; `SILO` and the ref are passed to each silo tool as `--silo` and `--ref`, so every tool reads the commit the header prints. If `SILO` does not hold `config/taxonomy.yaml` and `data/catalog_index.json` at `origin/main`, the script stops with exit 2 before writing anything. The taxonomy check reads two files from a directory, so the script extracts `config/taxonomy.yaml` and `data/catalog_index.json` at `origin/main` into a temporary directory for it. The silo checkout is never read or changed, so a fetch without a pull is enough.

The order differs from issue #40's list: the snapshot runs first because the trigger check reads it, and the two pin steps (P6) were added.

## After the run: the Claude stage

Commit the regenerated reports, then run `/silo-port` in Claude Code ([Plan 09](../../update-plans/09-silo-porting-llm.md), [command](../../.claude/commands/silo-port.md)). It works through [`update-plans/09-product-loop.md`](../../update-plans/09-product-loop.md) one item at a time:
- it reads the evidence batches written by step 6;
- it opens one PR per item, checked by `tools/silo-candidates/validate.py`.

The Claude stage is not part of this script, because it is not deterministic.

## Result

A summary line per step, the full output of any check that needs attention, and every changed file (anything outside `reports/` is unexpected; `.local/` is gitignored and never listed). Nothing is committed or pushed: review the diff, then commit.

| Exit code | Meaning |
|---|---|
| 0 | every report regenerated; no check needs attention |
| 1 | a check needs a human (new taxonomy signal, fired scope trigger, broken, malformed or near-miss pin, or a pinned page that changed or is gone) |
| 2 | a step failed: a write step exited non-zero, or a check exited 2. Pins, taxonomy and triggers exit 2 on the errors they handle; an unhandled Python exception exits 1 and its traceback is shown under ATTEND |

Every write goes through the guarded write of the tool that owns the file. No step writes a ✅ or ❌ into a matrix.
