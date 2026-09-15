# Conversion — repository to pages

Three separate decisions turn a repository into a page tree: **structure** (what becomes a page and where
it hangs), **titles** (what each page is called), and **content** (Markdown to Confluence storage format,
links included). They happen in that order, because links can only be rewritten once every title is known.

## 1. Structure

The page tree mirrors the directory tree **one to one**. Nothing is folded, merged, reordered or
flattened, so when the repository is restructured, Confluence takes the new shape exactly.

| Repository | Confluence |
|---|---|
| the configured root folder | the sync root; never modified |
| directory `a/b/` | a page for `b`, under the page for `a` |
| `a/b/README.md` | a child page of `b`, like any other document |
| `a/b/c.md` | a child page of `b` |
| a file at the repository root | a page directly under the root folder |

A directory's page body is a list of its children; the documents inside it, `README.md` included, are
pages in their own right. `confluence-sync.toml` has a `fold_directory_index` switch that would instead
merge a README into its directory's page — it is **off**, because it makes the page tree stop matching
the directory tree.

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
| the leading `# ` heading | **removed** — Confluence already displays it as the page title |
| a page with children | a `children` macro appended, listing them |

Raw HTML embedded in Markdown is escaped rather than passed through, so a stray tag cannot produce a
document Confluence refuses to store. Content inside a code macro is wrapped in CDATA, and a literal
`]]>` in the code is split across two CDATA sections so it cannot terminate the block early.

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
