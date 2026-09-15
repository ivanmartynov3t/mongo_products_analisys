# Title collisions

Confluence page titles are unique **per space**, and this tool resolves cross-document links by title
(`ri:content-title` — the id form renders a broken-link placeholder, see
[09-confluence-api.md](09-confluence-api.md)). A title is therefore both a label and an address, and a
collision is not cosmetic: it decides whether a page can be created at all.

Three things can take a title. Each is handled differently, and the difference was measured against the
live API rather than assumed.

## What actually reserves a title

| Page status | Reserves its title? | Measured by |
|---|---|---|
| `current` | **yes** | — |
| `archived` | **yes** | creating a page with an archived page's title → `400 A page already exists with the same TITLE in this space` |
| `trashed` | **no** | create → trash → create again with the same title → `200` |

The archived case is the trap. **Deleting a page's parent leaves its children archived with no parent**:
they vanish from the page tree but keep holding their titles. Trashing the old root folder once left 361
such pages behind, and the next run — seeing every plain name taken — fell back to path-qualified titles
for 360 of 361 pages. Nothing was broken, but every title got longer for an invisible reason.

## The three mechanisms

### 1. Names shared inside the repository → qualify by path

72 files here are called `feature-report.md`. Where a name is shared, **every** page sharing it is titled
by its full repository path, which is unique by construction:

```
feature-dictionary.md                                   unique → keeps the bare name
products/3t/studio-3t/features/ai/feature-report.md     shared → qualified by path
products/3t/3t-explore/features/ai/feature-report.md
```

All-or-nothing per group: one bare `feature-report.md` among 71 qualified ones would be worse than none.
Over-long paths keep their tail, since the end of a path identifies the file and the start repeats.

### 2. Titles held by this tool's own archived leftovers → reclaim them

Before planning, the tool lists archived pages in the space carrying the `repo-sync` property. Those
titles are **not** treated as taken; they are treated as reclaimable. `apply` then moves exactly the
leftovers whose titles it needs to the **trash**, which frees the title — because a trashed page reserves
nothing.

The trash is recoverable, so nothing is permanently destroyed, and only pages this tool created are ever
touched. `plan` reports what it *would* free and changes nothing:

```
303 title(s) held by archived leftovers would be freed (moved to trash, recoverable): …
```

### 3. Titles held by unrelated pages elsewhere in the space → work around them

Pages in the space that the tool did not create keep their titles, always. A document whose name
collides with one is path-qualified instead, and a remaining collision gets a ` (2)` suffix. The root
page is never renamed — it exists already, and its title is yours to choose.

## What this means day to day

- A collision never silently overwrites anything, and never fails a run.
- If titles suddenly get longer, the cause is usually leftovers holding names. `plan` says so explicitly.
- If you delete the root page by hand, its whole subtree becomes archived leftovers. The next `apply`
  reclaims those titles automatically; `purge --yes` is the deliberate way to start clean.
- Renaming or moving a file retitles the existing page rather than creating a second one, so a rename
  cannot create a collision with itself.
