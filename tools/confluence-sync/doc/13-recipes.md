# Recipes — how to do each thing

Every command is run from the repository root, and every one of them loads `.env` itself.

| I want to… | Do this |
|---|---|
| see what would change, safely | `./tools/confluence-sync/sync.sh plan` |
| publish my documentation edits | `./tools/confluence-sync/sync.sh apply` |
| publish after deleting or renaming files | `./tools/confluence-sync/sync.sh apply --delete` |
| check Confluence still matches the repo | `./tools/confluence-sync/sync.sh verify` |
| check how the pages actually *read* | `uv run tools/confluence-sync/audit.py --all` |
| wipe everything and rebuild | see [Rebuild from scratch](#rebuild-from-scratch) |
| publish somewhere else | see [Move the whole tree](#move-the-whole-tree) |
| change what gets published | see [Change what is published](#change-what-is-published) |

---

## Everyday: publish your changes

```bash
./tools/confluence-sync/sync.sh plan     # optional: see what would change
./tools/confluence-sync/sync.sh apply
```

`apply` verifies itself at the end and exits non-zero if anything does not match. Pages whose content is
unchanged cost **no API write at all**, so re-running is cheap and creates no page-history noise.

If you deleted or moved documents, add `--delete` so the pages left behind go to the trash:

```bash
./tools/confluence-sync/sync.sh apply --delete
```

Without `--delete` those pages are only reported, never removed.

---

## Rebuild from scratch

Wipes the published tree and republishes everything. Useful after changing the title scheme, the
structure rules, or when you simply want a clean slate.

```bash
# 1. See exactly what would be deleted. Deletes nothing.
./tools/confluence-sync/sync.sh purge

# 2. Trash it all. Recoverable from the space's trash.
./tools/confluence-sync/sync.sh purge --yes

# 3. Rebuild. ~360 pages takes roughly 7 minutes.
./tools/confluence-sync/sync.sh apply

# 4. Prove it.
./tools/confluence-sync/sync.sh verify
uv run tools/confluence-sync/audit.py --all
```

What `purge` does and does not touch:

- It trashes **everything beneath the root page**, whether or not this tool created it — below the root
  belongs to the sync.
- It **never deletes the root page**. That page is yours: the sync writes its body and nothing else.
- Everything goes to the **trash**, which is recoverable in Confluence. Nothing is destroyed permanently.

After a rebuild, the pages you just trashed become leftovers holding their old titles. That resolves
itself — see the next recipe.

---

## Titles came out longer than expected

Symptom: pages titled `products/3t/studio-3t/features/ai/feature-report.md` where you expected
`feature-report.md`.

Two causes, and `plan` tells you which:

1. **The name is genuinely shared in the repository.** 72 files here are called `feature-report.md`, so
   every one of them is titled by its full path. Nothing to fix — see
   [12-title-collisions.md](12-title-collisions.md).
2. **Leftovers are holding the plain names.** Deleting a page's parent leaves its children *archived*,
   invisible in the tree but still reserving their titles. `plan` reports this:

   ```
   303 title(s) held by archived leftovers would be freed (moved to trash, recoverable)
   ```

   `apply` frees exactly those it needs, automatically. Just run it:

   ```bash
   ./tools/confluence-sync/sync.sh apply
   ```

---

## Move the whole tree

```bash
# 1. Create the new root page in Confluence by hand, and copy its page id from the URL.
# 2. Point the config at it.
$EDITOR tools/confluence-sync/confluence-sync.toml    # root_page_id = "…"
# 3. Publish into the new location.
./tools/confluence-sync/sync.sh apply
```

The new root is empty, so everything is created there. The old tree is left where it is — the tool only
ever looks below its configured root. To remove the old copy, point the config back at the old id, run
`purge --yes`, then point it at the new one again.

Note the root page's **title is never changed**, so name it whatever you like.

---

## Change what is published

Edit `exclude` in `confluence-sync.toml`, then:

```bash
./tools/confluence-sync/sync.sh plan              # read the page tree in the report
./tools/confluence-sync/sync.sh apply --delete    # --delete removes pages you just excluded
```

Without `--delete`, newly excluded documents keep their pages and are reported as orphans.

To have a directory's `README.md` become a page of its own instead of its directory's content, set
`fold_directory_index = false`. That makes the page tree stop matching the directory tree, which is why
it is on.

---

## Recover from trouble

| Situation | What to do |
|---|---|
| a run died with a traceback | just run `apply` again — it resumes; existing pages are recognised, not duplicated |
| `adopted` count was non-zero | a previous run was interrupted; the tool repaired it, nothing more to do |
| you trashed pages by mistake | restore them from the space's trash in the Confluence UI |
| someone edited a managed page in Confluence | the next `apply` overwrites it; `verify` reports the drift beforehand |
| you want to start completely over | [Rebuild from scratch](#rebuild-from-scratch) |
| a page shows a broken-link image | run `apply` — it re-renders every page whose links changed; `audit.py` finds them |

Nothing in this tool deletes permanently. The worst case is a page in the trash.

---

## Use it as a gate

`verify` and `audit.py` make no writes and exit non-zero on a problem, so either can run on a schedule or
in CI to catch drift — documents added to the repository without a publish, or managed pages edited by
hand in Confluence:

```bash
./tools/confluence-sync/sync.sh verify        # fast: structure and freshness
uv run tools/confluence-sync/audit.py --all   # thorough: what Confluence actually renders
```

Both need the same `.env` credentials as a publish.
