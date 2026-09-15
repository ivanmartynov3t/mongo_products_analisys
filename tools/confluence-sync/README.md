# confluence-sync

Publishes this repository's documentation to Confluence and keeps the page tree identical to the
directory tree, links included.

```bash
./tools/confluence-sync/sync.sh plan              # show what would change, publish nothing
./tools/confluence-sync/sync.sh apply             # publish, then verify
./tools/confluence-sync/sync.sh apply --delete    # also trash pages whose source file is gone
./tools/confluence-sync/sync.sh verify            # check Confluence still matches the repo
./tools/confluence-sync/sync.sh purge --yes       # trash every page under the root, to rebuild
```

`plan` is safe to run at any time — it makes no writes. Every run leaves a full report in
`last-run-report.md`: the planned page tree, what changed, and every link or anchor that could not be
published faithfully.

Step-by-step recipes — including wiping the published tree and rebuilding it from scratch — are in
[doc/13-recipes.md](doc/13-recipes.md). The full documentation set starts at
[doc/01-overview.md](doc/01-overview.md).

## Setup

1. Create an API token at <https://id.atlassian.com/manage-profile/security/api-tokens>.
2. Put it in `.env` in the repository root (gitignored, never committed):

   ```
   CONFLUENCE_BASE_URL=https://3tsoftwarelabs.atlassian.net/wiki
   CONFLUENCE_USER_EMAIL=you@3tsoftwarelabs.com
   CONFLUENCE_API_TOKEN=...
   CONFLUENCE_ROOT_FOLDER_ID=1375076366
   ```

3. `uv` must be installed (`brew install uv`). Python dependencies are declared inline in `sync.py`
   and resolved by `uv` on each run — there is no virtualenv to manage.

Which space and folder to publish into, and what to exclude, live in `confluence-sync.toml`.

## How the mapping works

The page tree mirrors the directory tree one to one — nothing folded, merged or reordered.

| Repository | Confluence |
|---|---|
| the repository root | the configured root **page** — its body is the root `README.md` |
| directory `a/b/` | a page for `b` |
| `a/b/README.md` | the content of the page for `b` — the one permitted deviation |
| `a/b/c.md` | a child page of `b` |

**Page titles** are the file and directory names themselves — `feature-dictionary.md`, `studio-3t`.
Confluence requires titles to be unique across the entire space, and 72 files here are called
`feature-report.md`, so where a name is shared every page sharing it is titled by its full repository
path: `products/3t/studio-3t/features/ai/feature-report.md`.

**Page bodies contain the converted document and nothing else** — no child listings, no footers, no
added links. Confluence's own page tree shows the hierarchy.

**Links** between documents become real Confluence page links, with heading anchors preserved. Links
that cannot be represented are reported rather than silently mangled:

- GitHub line anchors (`#L103`) have no Confluence equivalent — the link points at the page, the
  fragment is dropped.
- Links to files that do not exist, or to file types that are not published, are left as plain text.

## Re-running

Each managed page carries the label `repo-sync` and a content property recording its source path and a
digest of the rendered page. So:

- A page whose content has not changed costs **no API write at all** — no new version, no notification
  to watchers.
- Renaming or moving a file moves the existing page instead of recreating it, so comments and inbound
  links survive.
- A page whose source file no longer exists is an orphan. It is only reported unless `--delete` is
  passed, and even then it is moved to the trash, where it is recoverable. Pages under the root that
  the sync did not create are never touched.

## Verification

`apply` verifies automatically, and `verify` can be run on its own. For a deeper check of what Confluence
actually renders — broken links, unconverted Markdown, tables that did not become tables — run the audit:

```bash
uv run tools/confluence-sync/audit.py --all
```

`verify` re-reads the tree from
Confluence and fails (non-zero exit, so it is usable in CI) if any of the following is true:

- a source file has no page, or a managed page has no source file
- a page's title or parent differs from the plan
- a page's stored digest does not match the current source
- a published link points at a page title that does not exist

## Notes for whoever maintains this

Two behaviours of the Confluence Cloud API shaped the design, both established by probing the live
instance rather than from documentation (see `PROBE-FINDINGS.md`):

- **Links must use `ri:content-title`, not `ri:content-id`** — the id form renders a broken-link
  placeholder. Titles are therefore the link key, which is why title stability matters and why the
  change digest covers the rendered body, title and parent rather than the source markdown.
- **The API intermittently returns 403 and 404 under load** and recovers on its own. Both are treated as
  retryable. A read that never succeeds aborts the run rather than being taken as "no such page" —
  otherwise the sync could duplicate pages, or class a live page as an orphan.
