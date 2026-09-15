# Operations — running it, and what to do when something goes wrong

## Routine use

After editing documentation:

```bash
./tools/confluence-sync/sync.sh apply
```

After deleting or moving documents, add `--delete` so the pages left behind go to the trash:

```bash
./tools/confluence-sync/sync.sh apply --delete
```

When unsure what a run would do, run `plan` first — it never writes.

## Measured performance

From the first full publish of this repository (360 pages):

| Run | Time | API calls |
|---|---|---|
| full publish from empty | ~7 min | 1 111 |
| no-op re-run (nothing changed) | ~90 s | 727 |

A publish costs 3 calls per page (create, property, label). A no-op run costs 2 per page (read the tree,
read each property) and is paid twice, since verification re-reads independently. Requests are sequential;
see [10-development.md](10-development.md) for how to parallelise safely.

## Failure modes

### `missing environment variable …` (exit 2)

`.env` is absent or incomplete. See [03-inputs.md](03-inputs.md).

### `… failed after 6 attempts: 401`

The token is wrong, expired, or revoked. Create a new one and update `.env`. Note that a *transient* 403
retries and usually succeeds; a persistent 401/403 is a real credential problem.

### The run aborts mid-publish with a traceback

An API error survived all retries. Pages already created remain. **Just run `apply` again** — it is
resumable: existing pages are recognised by their `source_path` property and skipped or updated, not
duplicated.

The one gap that resume has to handle: a run killed *between* creating a page and stamping its property
leaves a page the next run cannot recognise. Because Confluence rejects duplicate titles, creating it
again would fail. So a page with no property whose title exactly matches a planned page is **adopted** —
re-stamped rather than recreated — and counted as `adopted`. If you see a non-zero `adopted` count, a
previous run was interrupted.

### `verification FAILED` with many `missing page for …`

Every source file appearing to lack a page usually means the tree was read incompletely rather than that
the pages are gone. Check that `walk_descendants` is being used with `depth=10` and its re-query loop
intact — a plain `descendants` call truncates at depth 2 and produces exactly this symptom.

### `N page(s) under the root are not managed by the sync`

Someone created a page by hand inside the sync root, or a previous interrupted run left an unstamped page.
The tool will not touch it. Either move it out of the root, or let the next `apply` adopt it if its title
matches a planned page.

### A page shows a broken-link image

A link points at a title that no longer exists. `verify` catches this as `links to unknown title`. The
usual cause is a title change that did not propagate — re-running `apply` re-renders every page whose
rendered body changed, which fixes it.

## Recovering from a bad publish

- **Trashed the wrong pages.** They are in the space's trash and can be restored from the Confluence UI.
  Nothing is ever permanently deleted by this tool.
- **Want to start over.** Delete the managed pages (they carry the `repo-sync` label, so they are easy to
  find), then run `apply` again. The tool holds no local state, so there is nothing else to clean up.
- **Want to move the whole tree elsewhere.** Change `root_folder_id` in `confluence-sync.toml` and run
  `apply`: the new location is empty, so everything is created there. The old pages become orphans of a
  root the tool no longer looks at — delete them by hand, or point the config back and run
  `apply --delete` first.

## Keeping it honest over time

`verify` makes no writes and exits non-zero on drift, so it is worth running on a schedule or in CI. It
catches documents added to the repository without a publish, and managed pages edited by hand in
Confluence — both of which are otherwise invisible until someone notices the wiki and the repository
disagree.
