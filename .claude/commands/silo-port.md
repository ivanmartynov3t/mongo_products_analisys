---
description: Plan 09 Claude stage — port silo evidence into this repository, one checklist item at a time
argument-hint: "[item] [--once]   (item: a product folder name, scope-triggers, cross-product or readme)"
---

# /silo-port — the Claude stage of Plan 09

You run the **Claude stage** of [Plan 09](../../update-plans/09-silo-porting-llm.md). It loops over the checklist [`update-plans/09-product-loop.md`](../../update-plans/09-product-loop.md), one item at a time. Each item gets its own branch, validator run and pull request. The mechanical stage, `tools/silo-sync/run.sh`, has already refreshed the reports and the local evidence batches.

Arguments: `$ARGUMENTS`
- **No argument:** start at the first unticked item and continue until every item is ticked, or until a stop below.
- **An item name:** work only that item.
- **`--once`:** stop after one item.

## Rules (from Plan 09; never relax them)

1. **You draft; a human approves.**
   - Every change goes through a PR.
   - Never push to `main`, never merge without a passing review, and never force-push.
2. **Silo tags are not evidence.**
   - A tag, its probability or its page count never justifies a status. Evidence is a page's text, quoted word for word.
   - "Matrix IDs the silo never tags" never leads to a ❌ or a row removal.
3. **Status labels and their required fields** (weekly prompt 01). Use the matrix's own wording ("Confirmed", "Partial", "Roadmap", "Unverified", "Not supported"), never a new label.
   - **Confirmed:** a cited source with the URL and a date on its Source index line.
   - **Not supported:** a quoted, explicit exclusion from a cited page. Silence is never absence.
   - **Unverified:** the note `Checked <URL> on <YYYY-MM-DD>; no documentation of capability found.`
   - **Bad captures:** a page captured as navigation, a cookie banner or an empty shell is `needs-human`, never ❌.
4. **Citations.**
   - **Source index line:** `- S<n>: <title>, <URL> (silo: \`data/…/page.md@<sha8>\`, captured <YYYY-MM-DD>)`. Copy the "Cite as" and "Retrieved" columns of the batch. Owner decision 3 (whether a capture date counts as the access date) is still open, so write *captured*, and list every ✅ that rests only on a capture date in the PR.
   - **Quotes:** quote the page in "Detailed behavior" word for word, inside `"…"`. Use `...` for cuts. Never paraphrase inside quotes.
   - **IDs:** prefer an existing dictionary ID. A new ID follows the dictionary's naming rules and is added to `feature-dictionary.md` in the same PR.
5. **This repository is public.**
   - Only the public pages in the batch may be used.
   - Never open, quote or name repository documents, source files, internal systems or private repositories of the silo, and never copy a code-host or internal URL from a page body.
   - The validator withholds names in its output; keep it that way in commits, PR text and comments.
6. **Scope.**
   - Edit only the current item's files (see `tools/silo-candidates/validate.toml`, `[scope]`).
   - Never edit another product's files, never change an existing row's status without a new or changed cited source, never hand-edit a generated report, and never patch `README.md` except in the `readme` item.
   - Never run `pins.py repin apply` inside a product item: it edits every product.

## 0. Preconditions (stop with a message if any fails)

- **Clean state.** `git status --short` is empty, and `main` is up to date with `origin/main`.
- **Fresh reports.** The commit in the header of `reports/silo-candidates.md` equals the first 10 characters of `git -C ../prod_info_silo rev-parse origin/main`. If it differs, the owner runs `tools/silo-sync/run.sh`, reviews and commits the reports, then restarts you.
- **Fresh batches.** `.local/silo-batches/<product>/README.md` names the same commit. If not, run `uv run tools/silo-candidates/batch.py apply`.
- **Checklist.** `update-plans/09-product-loop.md` is on `main`, and the item exists and is unticked.

## 1. Per item

1. `git checkout main && git pull --ff-only && git checkout -b port/<item>-<YYYY-MM-DD>`.
2. Do the item's work (section 2).
3. Regenerate what the tools own and your change affects:
   - `uv run tools/silo-candidates/candidates.py apply`, when the ledger changed;
   - `uv run tools/taxonomy-reconcile/reconcile.py --silo <dir>`, when `decisions.tsv` changed. `<dir>` holds `config/taxonomy.yaml` and `data/catalog_index.json` extracted at `origin/main` with `git -C ../prod_info_silo show`, as `run.sh` does. The validator then asks a human to confirm the regenerated taxonomy report: say so in the PR.
4. Validate: `uv run tools/silo-candidates/validate.py --item <item>`.
   - Fix every finding you can.
   - A finding you cannot fix becomes a `needs-human` ledger row, or a line in the PR's *Needs a human* section. Exit 0 is the goal; exit 2 means stop and report.
5. **Tick the checklist on the branch**, and only for what you did and verified:
   - tick each sub-item as it is done;
   - tick the item's heading box only when all its sub-items are ticked.

   An item with nothing to do gets its heading ticked with "— no changes (<date>)" and no PR of its own. Make that tick on the next item's branch, and say so in that PR. If it is the last item, open a one-line PR for the tick.
6. Commit with a message such as `port(<item>): <summary> (Plan 09)`. Push, and open the PR with the body in section 3.
7. **Review.**
   - Run the repository's `automation-compliance-review` agent on the PR.
   - Check the **content** yourself as well: every new or changed row against its cited page body.
   - Fix the findings, re-validate, and re-review until nothing must be fixed. Record each round on the PR.
8. **Merge.**
   - **Standing approval recorded.** If the Plan 09 execution log records the owner's standing approval for the loop after the pilot gate, squash-merge after a passing review, delete the branch, and continue.
   - **No standing approval.** Stop after the review, report the PR link, and wait for the owner. This is always the case during the pilot (Plan 09 step 5).

## 2. The work, by item

### Product items (a product folder name)

Read `.local/silo-batches/<product>/README.md`, the product's matrices and product report, and the product's rows in `reports/review-queue.md`, `reports/evidence-gaps.md` and the `pins.py repin plan` output.

**candidates.** Decide every candidate in the batch. For each one:
1. Read its dictionary definition, then the page bodies (`pages/…`), best probability first, until the question is settled. Read at least the top 3 pages, or every page if there are fewer.
2. Choose exactly one outcome:

   | Outcome | When | What you write |
   |---|---|---|
   | `add-row` | a page shows the capability, a limitation, or an explicit absence | a row in the matching matrix (see below) |
   | `existing-row` | an existing row already covers it under another ID | a mapping in `tools/taxonomy-reconcile/decisions.tsv`, only if the mapping holds for the dictionary in general; otherwise a `needs-human` row with the reason |
   | `other-product` | the pages describe another product (see "Shared") | ledger row only |
   | `noise` | the pages do not describe this capability for this product | ledger row only |
   | `needs-human` | ambiguous, a bad capture, or a private source would be needed | ledger row with the reason |

3. **Where rows go.** The matrix is chosen by the ID prefix:

   | Prefix | Folder |
   |---|---|
   | CONN | `connectivity` |
   | QUERY | `querying` |
   | AGG | `aggregation` |
   | SCHEMA | `schema` |
   | IDX | `indexing-performance` |
   | TRANSFER | `data-transfer` |
   | SHELL | `shell` |
   | AI | `ai` |
   | SQL | `sql-tools` |
   | GOV | `governance` |
   | SCHED | `task-scheduler` |

   - **Missing folder.** If the folder does not exist and at least one `add-row` is evidenced for it, create it from `templates/feature-matrix-template.md` and `templates/feature-report-template.md`. Add it to the product report's feature inventory, and remove it from "Feature areas omitted" if listed there. Never create a folder without evidence (dictionary naming rule 5).
   - **Source index.** Add the page as the next `S<n>`, and reuse an existing entry for the same URL.
4. **Ledger.** Append one row to `tools/silo-candidates/triage.tsv`:
   - product, tag, outcome;
   - today's date;
   - the silo commit (10 characters);
   - `web_docs` (the batch's Web count);
   - a one-line public reason (e.g. `row added in querying`, `noise: pages cover Snowflake SSO`).

   Never name a private repository or document in it.

**review queue.** For each of the product's matrices or reports listed as changed, re-read the rows that cite the moved page against its current silo copy:
- **Claim still holds:** add a dated `Review log:` line to the matrix metadata saying so.
- **Claim changed:** update the row and its citation, following rule 3.

**pins.** For pins in this product's files that the re-pin plan lists as *unchanged*, move them by hand: same path, new commit. For *changed* or *gone* pins, re-check the claim first, as in the review queue.

**evidence gaps.** For the product's matrices that cite no URL, add a public page from the batch as an extra source to rows it directly supports. Leave the status alone unless rule 3 allows a change.

**cascade.** Update the product's `features/*/feature-report.md` and `product-report.md` for every row you added or changed: summary bullets, feature inventory, and analysis date. Cross-product reports wait for the `cross-product` item.

### `scope-triggers`

Run `uv run tools/scope-triggers/triggers.py`.
- **Nothing fired:** tick "no changes". Copy its "Check by hand" list under *Needs a human* in the next PR.
- **A trigger fired:** update `docs/coverage-scope.md` as its revisit-trigger table says, and never beyond it. List the trigger and the change in the PR.

### `cross-product`

After every product item is merged, cascade the cycle's changes with [weekly prompt 03](../../.github/prompts/weekly-maintenance/03-sync-downstream-reports.prompt.md), steps 1–4:
- the low-level comparison;
- the high-level comparison;
- both gap analyses;
- the cumulative report.

The cycle's changes are the rows the merged `port/*` PRs added or changed since the cycle started. Log the result in Plan 09's execution log, not Plan 03's.

### `readme`

Rebuild `README.md` with [`update-readme-dashboard.prompt.md`](../../.github/prompts/update-readme-dashboard.prompt.md), unchanged, keeping its fixed skeleton. This is the last item.

## 3. PR body

```markdown
Plan 09 · checklist item **<item>** · silo `<sha10>`

## Candidates (<n> in batch)
| Outcome | Count | Tags |
|---|---|---|
| add-row | … | … |
| existing-row | … | … |
| other-product | … | … |
| noise | … | … |
| needs-human | … | … |

## Other work
- Review queue: …
- Pins: …
- Evidence gaps: …
- Cascade: … (cross-product reports wait for the `cross-product` item)

## Rows resting only on a silo capture date (owner decision 3)
- …

## Needs a human
- …

## Validator
`uv run tools/silo-candidates/validate.py --item <item>` → exit <code>, <n> findings (listed above if any)

## Merge checklist
- [ ] Only files in the item's scope changed
- [ ] Validator exit 0, or every remaining finding listed under *Needs a human*
- [ ] Every new or changed row checked against its cited page
- [ ] Code review done; every *must fix* fixed
- [ ] No secrets, personal data or private-repository text
- [ ] Owner approved the merge

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## 4. When you stop

Report:
- the items done, with PR links;
- per item, the outcome counts and the validator result;
- anything that needs a human;
- the next unticked item.

Never claim a check passed that you did not run.
