# Outputs — everything the script writes

Three destinations: the console, one local file, and Confluence.

## 1. Console

```
reading the target space …
planned 360 pages from /Users/…/mongo_products_analisys
publishing …
  created 360, updated 0, unchanged 0, moved 0, adopted 0, trashed 0
verifying …
verification PASSED
report: tools/confluence-sync/last-run-report.md  (1111 API calls)
```

The counters are the run's whole story:

| Counter | Meaning |
|---|---|
| `created` | a page that did not exist before |
| `updated` | content, title or both changed |
| `moved` | the page's parent changed (a file moved between directories) |
| `unchanged` | nothing to do — **no API write was made for this page at all** |
| `adopted` | an untracked page with the expected title was re-stamped instead of recreated (see [11-operations.md](11-operations.md)) |
| `trashed` | orphan moved to the trash; only possible with `--delete` |

With `--verbose`, each created page prints `+ Title`, each updated page `~ Title`, and each retried
request prints to stderr.

`plan` prints a create/existing/orphan summary and a count per issue kind instead of the counters.

## 2. `tools/confluence-sync/last-run-report.md`

Rewritten by every run, including `plan`. Not committed — it is a run artefact.

Contents, in order:

1. **Summary** — page counts split into folders and documents; the run's counters; the verification
   verdict with up to 50 failures listed.
2. **Issues**, grouped by kind, each entry naming the source file and the offending link or title:
   - `link-unresolved` — a link that could not be published
   - `line-anchor-dropped` — a `#L123` fragment
   - `anchor-unresolved` — a fragment matching no heading in the target
   - `title-disambiguated` — a page whose title had to be qualified, and what it became
3. **Page tree** — the complete planned hierarchy with final titles, indented. On a first run this is the
   thing to read before publishing: it is exactly what will appear in Confluence.

## 3. Confluence

### Pages

Created under the configured root page, nested to match the repository. A page body is the converted
document and nothing else — no child listing, no footer, no added links. Bodies are Confluence storage
format. Updates bump the page version with the message `repo-sync <source path>`, so the page
history shows which file a change came from.

### A content property on every managed page

Key `repo-sync`:

```json
{
  "source_path": "products/3t/studio-3t/features/ai/feature-report.md",
  "digest": "9f2c…",
  "tool_version": "1.0"
}
```

This is the tool's entire persistent state — there is no local database. It is what makes a page
recognisable on the next run, from any machine. See [07-change-detection.md](07-change-detection.md).

### A label on every managed page

`repo-sync`, so managed pages can be found in the Confluence UI.

## What is never written

- **Nothing outside the root page.** Every operation is scoped to the root page and its descendants, and the root page itself is never created, renamed, re-parented or deleted.
- **No page the tool did not create.** Pages lacking the `repo-sync` property are never updated, moved or
  deleted; `verify` reports them as unmanaged rather than adopting them.
- **No repository files.** The tool only reads the documentation. The one file it writes in the repository
  is its own report.
- **No credentials** in the report, the console, or the page history.
