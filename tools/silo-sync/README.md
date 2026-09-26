# silo-sync

One local command for the weekly silo → analysis refresh (issue #40, Plan 08 P8). No CI needed.

```bash
tools/silo-sync/run.sh              # fetch the silo, regenerate every report, print a summary
tools/silo-sync/run.sh --no-fetch   # use the silo refs already fetched
SILO=/path/to/prod_info_silo tools/silo-sync/run.sh
```

## Steps

| # | Step | Tool | Writes | Weekly issue |
|---|---|---|---|---|
| 1 | fetch `prod_info_silo` | `git fetch` in the silo | silo refs only | — |
| 2 | silo snapshot | [`silo-snapshot`](../silo-snapshot/README.md) | `reports/silo-snapshot.{md,json}` | #18 |
| 3 | staleness queue | [`silo-review`](../silo-review/README.md) | `reports/review-queue.md` | #17 |
| 4 | candidate signals | [`silo-candidates`](../silo-candidates/README.md) | `reports/silo-candidates.md` | LLM part |
| 5 | taxonomy check | [`taxonomy-reconcile`](../taxonomy-reconcile/README.md) `--check` | nothing | #18 |
| 6 | scope triggers | [`scope-triggers`](../scope-triggers/README.md) | nothing | #18 |
| 7 | pin check | [`silo-pins`](../silo-pins/README.md) `check` | nothing | — |
| 8 | re-pin plan | [`silo-pins`](../silo-pins/README.md) `repin plan` | nothing: shows which unchanged pins could move; run `repin apply` yourself | — |

Steps 2–4, 7 and 8 read the silo from git objects at `origin/main`. Step 5 reads the silo's working tree, so it runs only when the silo checkout is a clean `origin/main`; otherwise it is reported as failed with the command to fix it. The script never changes the silo checkout.

## Result

A summary line per step, the full output of any check that needs attention, and the changed report files. Nothing is committed or pushed: review the diff, then commit.

| Exit code | Meaning |
|---|---|
| 0 | every report regenerated; no check needs attention |
| 1 | a check needs a human (new taxonomy signal, fired scope trigger, broken pin) |
| 2 | a step failed |

The evidence-gap report (P5, #37) is added as a step when that tool merges.

Every write goes through the guarded write of the tool that owns the file. No step writes a ✅ or ❌ into a matrix.
