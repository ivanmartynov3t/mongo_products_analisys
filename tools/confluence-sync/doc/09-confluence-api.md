# Confluence API behaviours that shaped the design

Everything here was **measured against the live instance**, not taken from documentation. Each one changed
the design, and each one would be easy to get wrong when modifying the tool.

Endpoints used: `/api/v2/*` for pages, folders and properties; `/rest/api/*` (v1) only for labels, which
v2 does not offer.

## 1. There is no Markdown representation

`POST /api/v2/pages` accepts `body.representation` of **`storage`, `atlas_doc_format` or `wiki`** — that
is the entire enum in the published OpenAPI schema. Markdown is not a body format.

**Consequence:** "publish Markdown" necessarily means converting to storage format (XHTML) locally. The
converter is the bulk of the tool, not the API calls.

## 2. Page links must use `ri:content-title`, not `ri:content-id`

```xml
<!-- renders a broken-link placeholder -->
<ac:link><ri:page ri:content-id="1374552072"/><ac:link-body>…</ac:link-body></ac:link>

<!-- resolves correctly -->
<ac:link><ri:page ri:content-title="Sync probe child"/><ac:link-body>…</ac:link-body></ac:link>
```

The id form produced
`StorageLinkContentTitleNotFoundException: Title must not be null or empty` rendered as an inline error
image. Anchors (`ac:anchor="Heading Text"`) work with the title form, both for another page and for the
current one.

**Consequence:** titles are the link key. They must be unique space-wide and stable, and the change digest
must cover the rendered body so a retitle re-renders every page linking to it. This single fact drives
most of [04-conversion.md](04-conversion.md) and [07-change-detection.md](07-change-detection.md).

## 3. Pages can be created directly under a folder

`parentId` accepts a **folder** id; the response comes back with `parentType: "folder"`. Community reports
suggested otherwise, which is why it was probed first.

This is no longer used — the sync root is a page, for the reason in §7 — but it is worth knowing that
folder-parented pages do work.

## 4. `descendants` truncates at depth 2 by default

`GET /api/v2/folders/{id}/descendants` has a `depth` parameter that **defaults to 2 and is capped at 10**.
Beyond that it returns nothing, with no error and no indication of truncation.

This is a genuine trap: a naive call sees only the top two levels of a deep tree. The tool would then
consider every deeper page missing — recreating it (and failing on duplicate titles) or, with `--delete`,
mistaking live pages for orphans.

**Consequence:** `walk_descendants()` requests `depth=10` and re-queries anything sitting exactly at the
cut-off as a new root, so arbitrarily deep trees are read completely.

## 5. The API intermittently returns 403 and 404 under load, then recovers

During probing, a sequence of requests that had just returned `200` began returning `404 NOT_FOUND` and
`403 "Current user not permitted to use Confluence"` — with `x-cache: Error from cloudfront` — and
recovered unprompted about a minute later. The token and permissions were unchanged throughout.

**Consequence:** `403` and `404` are treated as **retryable**, alongside `429` and `5xx`, with backoff and
`Retry-After` honoured. A read that never succeeds aborts the run rather than being interpreted as "this
page does not exist" — otherwise a transient edge error could cause duplicate pages, or cause live pages
to be trashed as orphans.

## 6. CQL search is eventually consistent

`GET /rest/api/content/search?cql=label="repo-sync"` returned zero results for pages that demonstrably
existed, because the search index lags writes.

**Consequence:** the tool never uses search to find its pages. It walks the folder tree, which is
immediately consistent.

## 7. A folder has no body; only a page can hold content and children

`POST /folders` accepts `spaceId`, `title`, `parentId` — nothing else — and there is no update endpoint
for a folder at all (`/folders/{id}` offers only `get` and `delete`). A folder can list children, but it
can never hold content.

That is why the sync root is a **page**. The repository root is a directory like any other and needs
somewhere to put its own `README.md`; with a folder as the root, that README would have had to appear as
a page called `README.md`. With a page as the root, `README.md` appears nowhere in Confluence.

## 8. An archived page reserves its title; a trashed one does not

Measured directly:

| Attempt | Result |
|---|---|
| create a page titled like an **archived** page | `400 A page already exists with the same TITLE in this space` |
| create a page titled like a **trashed** page | `200` |

Deleting a page's parent leaves its children **archived with no parent** — invisible in the page tree,
still holding their titles. Since titles are the link key, those leftovers silently push live pages into
longer path-qualified names.

The consequence for the design: freeing a title needs only a **trash**, never a permanent purge, so the
recovery is non-destructive. See [12-title-collisions.md](12-title-collisions.md).

## 9. Deleting a page that is already gone answers 500, not 404

The archived-page listing is eventually consistent and can name a page that has already been purged;
`DELETE` on it returns `500 INTERNAL_SERVER_ERROR`. Title-freeing is therefore best-effort: a failed
delete counts as a real failure only if the page is still there afterwards, and a title that genuinely
cannot be freed makes the run re-plan around it rather than abort.

## 10. Miscellaneous

- `PUT /api/v2/pages/{id}` requires `version.number` to be exactly the current version plus one, so each
  update reads the page first.
- Page titles must be unique per **space**, not per branch of the tree.
- Content properties (`/api/v2/pages/{id}/properties`) are ordinary versioned resources: updating one also
  requires the next version number.
- Labels must be written through the v1 endpoint (`POST /rest/api/content/{id}/label`); v2 exposes reads
  only.
- Attachment upload exists only in v1. Not used here — this repository has no images.
- A page cannot be its own parent: sending the root page's own id as its `parentId` returns
  `400 Can not set page as its own parent`. The root page's `parentId` is simply never sent.

## Re-checking these

`PROBE-FINDINGS.md` in the parent directory holds the original raw notes with ids and responses. The
OpenAPI schema used to confirm the body representations and the `depth` default is published at
`https://dac-static.atlassian.com/cloud/confluence/openapi-v2.v3.json`.
