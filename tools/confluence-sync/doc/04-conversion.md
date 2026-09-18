# Conversion — repository to pages

Three separate decisions turn a repository into a page tree: **structure** (what becomes a page and where
it hangs), **titles** (what each page is called), and **content** (Markdown to Confluence storage format,
links included). They happen in that order, because links can only be rewritten once every title is known.

## 1. Structure

The page tree mirrors the directory tree **one to one**. Nothing is folded, merged, reordered or
flattened, so when the repository is restructured, Confluence takes the new shape exactly.

| Repository | Confluence |
|---|---|
| the repository root | the configured root **page** — its content is the root `README.md` |
| directory `a/b/` | a page for `b`, under the page for `a` |
| `a/b/README.md` | the **content of the page for `b`** — the one permitted deviation |
| `a/b/c.md` | a child page of `b` |
| a file at the repository root | a page directly under the root page |

A directory's `README.md` supplies that directory's page content rather than becoming a page of its
own — a folder page with no content of its own is exactly what a README is for. This applies to
`README.md` only: an `overview.md` or `index.md` stays an ordinary page like any other document. A
directory without a README gets an empty page; its children show in Confluence's page tree.

This holds for the repository root too, which is why the sync root is a **page** and not a Confluence
folder: a folder has no body at all (the API offers no way to give it one), so a root `README.md` would
have nowhere to go and would have to appear as a page called `README.md`. With a page as the root,
`README.md` appears nowhere in Confluence — at any level — and the root page's title is left alone,
since that page is yours to name.

Only directories that contain at least one publishable document (at any depth) become pages. Siblings are
ordered directories first, then documents, each alphabetically by path.

## 2. Titles

Titles carry more weight here than they might appear to, because **Confluence resolves page links by
title** (see [09-confluence-api.md](09-confluence-api.md)). A title is therefore both a label and an
address.

Confluence requires titles to be unique **across the whole space**, not just within a branch. This
repository would otherwise be unpublishable: it contains 72 files named `feature-report.md`, 72 named
`feature-matrix.md` and 13 named `product-report.md`.

The rule:

1. **Base title** is the document's first `# ` heading. Falling back to a humanized filename if there is
   none, and for a directory page with no index file, the humanized directory name. Whitespace is
   collapsed and the result truncated to 240 characters.
2. Titles already used by pages **elsewhere in the space** are reserved up front, so the sync never
   collides with unrelated pages. (Pages it manages itself are excluded from that reservation, or it
   would collide with its own previous run.)
3. Where several pages share a base title, **all of them** are qualified with their parent directories,
   joined by `›` — and all to the *same* depth, the shallowest depth that makes the whole group unique.
4. A remaining collision appends ` (2)`, ` (3)`, and so on.

Step 3 is what keeps the result readable. Qualifying only the ones that "lost" would leave one bare
`Governance` page and nine `… › Governance` pages, which reads like an inconsistency. Instead:

```
3T Access  › Features › Governance
3T Explore › Features › Governance
3T Lens    › Features › Governance
```

Humanizing expands known acronyms (`sql-tools` → `SQL Tools`, `mongodb-compass` → `MongoDB Compass`) and
leaves words the author already capitalised alone. The list lives in `ACRONYMS` in `sync.py`.

In practice, for this repository, the documents' own H1 headings are descriptive enough that only two
collide; almost all qualification falls on directory pages.

## 3. Content

Markdown is parsed with `markdown-it-py` in CommonMark mode, plus tables and strikethrough, and rendered
to **Confluence storage format** — an XHTML dialect. Storage format is the only representation that
accepts macros, and the API does not accept Markdown at all.

| Markdown | Becomes |
|---|---|
| headings, paragraphs, lists, blockquotes, emphasis | the corresponding XHTML |
| tables | `<table>` |
| fenced code | a `code` macro, with the fence's language as a parameter |
| `<br>`, `<hr>` and other void elements | self-closed, as XHTML requires |
| the document's own `# ` heading | **kept** — the page is titled after the file, so it is not a duplicate |


Raw HTML embedded in Markdown is passed through by the CommonMark parser (`html=True`), while Confluence's storage format renderer sanitizes and strips tags it does not support while preserving their inner text. Void elements like `<br>` are self-closed to `<br/>` for XHTML compliance. Content inside a code macro is wrapped in CDATA, and a literal `]]>` in the code is split across two CDATA sections so it cannot terminate the block early.

### Links

Every link is classified and rewritten:

| Link | Result |
|---|---|
| `../product-report.md` | `<ac:link><ri:page ri:content-title="…"/></ac:link>` — a real page link |
| `guide.md#prereqs` | the same, plus `ac:anchor="Prereqs"` resolved from the target's headings |
| `#section` (same page) | `<ac:link ac:anchor="Section">` |
| `guide.md#L103` | a page link, **fragment dropped** — see [05-limitations.md](05-limitations.md) |
| `https://…`, `mailto:` | left as an ordinary `<a href>` |
| anything unresolvable | the link text is kept, the link is dropped, and it is reported |

Link targets are URL-decoded before resolution, so `%20` in a path to a file whose name contains spaces
resolves correctly — this repository has 22 such files. A link to a directory, or to a directory's index
file, resolves to that directory's page.

Anchors are resolved through a table built from the target document's headings, using GitHub's slug rules
(lowercase, punctuation stripped, **each** space becoming one hyphen — so runs of whitespace produce runs
of hyphens). If the slug in the link matches no heading in the target, the link still points at the page,
and the unresolved anchor is reported.

## Nothing is added

A page carries exactly what its file carries. No child listing, no provenance footer, no navigation, no
"generated by" note. The only links on a page are the ones the author wrote — converted, never invented.
Confluence's own page tree already shows the hierarchy, so the body does not repeat it.
