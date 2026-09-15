# Change detection — updates, moves, renames, deletions

Re-running must be cheap and safe. Cheap, because every Confluence update creates a new page version and
notifies watchers — 360 unconditional writes per run would make the page history useless. Safe, because
the same mechanism decides what gets deleted.

## The digest

Each managed page stores, in its `repo-sync` content property, a SHA-256 over three things:

```
sha256( title \0 parent title \0 rendered storage body )
```

**The digest covers the rendered body, not the source Markdown.** That is not an implementation detail —
it is required for correctness. Because Confluence links resolve by title, retitling page B changes the
*rendered* body of every page that links to B, even though those files' Markdown never changed. Hashing
the source would leave those pages pointing at a title that no longer exists, and Confluence would render
broken-link placeholders. Hashing the rendered output catches them.

## The decision, per page

On each run the script reads every page under the root folder, along with its property, and matches by
`source_path`:

| Situation | Action |
|---|---|
| no page for this source path | **create**, then stamp property and label |
| page exists, digest matches, parent matches | **skip** — no API write whatsoever |
| digest differs | **update** body and title, bump version |
| parent differs | **move** (the same `PUT`, with a new `parentId`) |
| page exists but has no digest | **update** regardless — it was never fully stamped |
| page exists whose source path is gone from the repository | **orphan** |

### Renames and moves preserve the page

Identity is the source path, not the title or the location. So renaming a document's heading retitles the
existing page instead of creating a second one, and moving a file to another directory re-parents the
existing page. Page history, comments and inbound links survive both.

Moving a file to a *different path* is, by that definition, a delete plus a create: the old source path is
orphaned and a new page appears. Treating that as a move would require content-similarity guessing, which
the tool deliberately does not do.

## Deletion

A managed page whose `source_path` no longer exists in the repository is an orphan.

- **By default it is only reported** — the run prints `! orphan (kept, pass --delete to trash)`.
- With `--delete`, it is moved to the **trash**, which is recoverable from the Confluence UI. There is no
  permanent-purge mode, by design.
- A page **without** the `repo-sync` property is never an orphan, however it got there. Anything you write
  by hand inside the sync root is invisible to deletion. `verify` reports such pages so they cannot
  accumulate unnoticed.

Because orphan detection depends on reading the tree correctly, a read failure aborts the run rather than
being treated as "this page is gone" — see [09-confluence-api.md](09-confluence-api.md).

## Why there is no local state file

All state lives on the pages. A local cache would be one more thing to lose, to stale, or to disagree with
reality — and it would make the first run from a fresh clone, or from CI, behave differently from a run on
the machine that last published. The cost is one extra API call per page to read its property; the benefit
is that the tool has no memory to corrupt.
