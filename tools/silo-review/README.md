# silo-review

Answers one question each week: **which parts of this analysis rest on evidence that has since moved?** (issue #14, feeds the weekly review #17).

```bash
uv run tools/silo-review/review.py plan      # print the report, write nothing
uv run tools/silo-review/review.py apply     # write reports/review-queue.md
uv run tools/silo-review/review.py churn     # weekly rate of real content change on cited pages
uv run tools/silo-review/test_review.py      # offline tests
```

Needs a full (not shallow) clone of `prod_info_silo` next to this repository; `git -C ../prod_info_silo fetch` before a run. Configuration: [`silo-review.toml`](silo-review.toml).

## Output

[`reports/review-queue.md`](../../reports/review-queue.md), regenerated on each run and committed, so every change to the queue is reviewable in a PR.

1. **Staleness queue** — per feature matrix, the cited pages that moved after its `Analysis date`, most-changed first, with source ID, change dates, the new text and the silo file.
2. **Citation health** — every distinct URL cited anywhere in the repository, classified:

| Status | Meaning |
|---|---|
| changed since review | the page's content changed after the review date |
| server reports newer | no silo copy from before the review, but a trustworthy `Last-Modified` is later |
| unchanged since review | the silo holds a copy from before the review; nothing changed |
| unchanged since silo capture | the silo first saw it after the review; nothing changed since |
| dropped by silo | tracked once, no longer (removed, moved, or out of the silo's scope) |
| not checkable | never tracked by the silo — never reported as unchanged |

How "changed" is decided, and why it is not the silo's checksum: [CHURN.md](CHURN.md).

## Guarantees

- **Read-only.** The silo is read from git objects at the pinned `silo_ref` — never checked out or written — and the report records the commit SHA. The only file the tool can write is the configured output; `guarded_write` refuses anything else and the tests check both that and that no other file in either tree changes.
- **Deterministic.** Same silo commit and same repository content, same bytes out (tested).
- **Not evidence.** A flag is a prompt for a human to re-check a source. It never becomes a ✅ or ❌ in a matrix.
