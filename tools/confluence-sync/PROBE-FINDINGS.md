# Probe findings — 2026-09-15 (verified against the live instance, not documentation)

Space `~712020e5…` = spaceId **11436034**. Root folder `1375076366` = "Product compare",
itself a child of page `11436238`.

## Works

| Primitive | Result |
|---|---|
| Create page with `parentId` = **folder id** | ✅ 200, response shows `parentType: "folder"` — no manual root page needed |
| Nested child pages (page → page) | ✅ arbitrary depth |
| `GET /api/v2/folders/{id}/descendants` | ✅ returns the whole subtree with `parentId` + `depth` — this is how verification and orphan detection read the tree |
| Content property `repo-sync` on a page (v2) | ✅ — sync state lives on the page |
| Label write (v1 `/rest/api/content/{id}/label`) | ✅ |
| `PUT` update with `version.number = current + 1` | ✅ |
| `code` macro with language, tables, headings | ✅ render correctly |

## Two findings that change the design

**1. Page links must use `ri:content-title`, not `ri:content-id`.**
`<ac:link><ri:page ri:content-id="1374552072"/></ac:link>` renders as a *broken-link placeholder*:
`StorageLinkContentTitleNotFoundException: Title must not be null or empty`.
With `ri:content-title="Sync probe child"` the same link resolves correctly, including
`ac:anchor="Prereqs"` for heading anchors and bare `<ac:link ac:anchor="…">` for same-page anchors.

Consequences:
- **Titles are the link key.** They must be unique across the *whole space* and deterministic.
- A title change must trigger re-render of every page linking to it → the change-detection hash must be
  over the **rendered storage body**, not the source markdown.

**2. The API intermittently returns 403/404 under burst.** During probing, a series of calls that had just
returned 200 started returning `404 NOT_FOUND` and `403 "Current user not permitted to use Confluence"`
(with `x-cache: Error from cloudfront`), then recovered on their own a minute later. So 403 and 404 must be
treated as **retryable** with backoff, not as "page does not exist" — otherwise the sync would wrongly
conclude a page is missing and create a duplicate, or wrongly call a page an orphan and trash it.

## Title inventory (measured)

- 231 markdown files to publish (excluding `templates/`, `.github/`, `tools/`) + **119 directory container pages** = 350 pages.
- Markdown H1 titles: only **2 internal collisions**.
- **0 collisions with the 175 pages that already exist in the space.**
- But **directory names collide badly**: `ai` ×10, `governance` ×10, `connectivity` ×8, `aggregation` ×7 …
  → container page titles must be path-qualified (e.g. `Studio 3T › Features › AI`), and the qualifier must
  be deterministic so links stay stable.

## Probe artefacts left in Confluence

`Sync probe — mongo_products_analisys` (id 1375895554) and its child `Sync probe child` (id 1374552072),
inside the "Product compare" folder. Safe to delete.
