# Limitations — what cannot be published faithfully

Confluence cannot express everything Markdown-on-GitHub can. Where something does not survive the trip,
the tool degrades it to the closest working equivalent and **records it in the report**; it never fails
silently and never guesses.

Counts below are from the first full run of this repository (360 pages).

## Line anchors — 160 occurrences

GitHub links of the form `file.md#L103` address a line number. Confluence has no notion of line numbers
in a page, so there is nothing to point at.

**Result:** the link points at the correct page, the fragment is dropped. Reported as
`line-anchor-dropped`.

## Anchors that no longer match a heading — 12 occurrences

A link such as `#confirmed-absent--no-3t-product-supports-this-13` where the target's heading now reads
`Confirmed absent — no 3T product supports this (9)`.

These are **stale in the repository itself** — the same link is already broken on GitHub. The tool does
not attempt to guess which heading was meant.

**Result:** the link points at the correct page, the fragment is dropped. Reported as
`anchor-unresolved`. Fixing them means fixing the source documents.

## Links to files that are not published — 67 occurrences

Mostly links to `.txt` files that do not exist in the repository (for example, `overview.md` in
`research/google_research/` links to a `.txt` next to each analysis, and those files were never added).
Also covers links to excluded directories and to file types the tool does not publish.

**Result:** the link text is kept as plain text; the link is removed. Reported as `link-unresolved`.
These links are already broken in the repository — publishing them as working links is not possible, and
publishing them as *apparently* working links would be worse.

## Mermaid diagrams — 1 occurrence

A ```` ```mermaid ```` block becomes a code macro showing the diagram source. Confluence Cloud does not
render Mermaid without a marketplace app.

**Result:** readable source, not a picture.

## Titles that had to be qualified — 242 occurrences

Not a loss of fidelity, but longer titles than the file names: where a name is shared — 72 files are
called `feature-report.md` — every page sharing it is titled by its full repository path. Forced by
Confluence's space-wide title uniqueness. See [04-conversion.md](04-conversion.md).

## Structural notes

- **Front matter** is not recognised. This repository has none; if it gains any, it would currently be
  rendered as body text rather than stripped or mapped to page properties.
- **Task lists** (`- [ ] item`) render as literal `[ ]` text — CommonMark has no checkbox construct.
- **Raw HTML** in Markdown is escaped, not passed through.
- **Images and attachments** are not implemented, because this repository contains none. Adding them
  means uploading via the v1 attachment endpoint and emitting `<ac:image><ri:attachment/></ac:image>`.
- **Heading anchors** rely on the heading text. Renaming a heading breaks in-page links to it in exactly
  the way it does on GitHub.

## Things the tool will not do

- It will not edit the repository to fix broken links. The report tells you; the repair is yours.
- It will not permanently delete a page. `--delete` moves pages to the trash, which is recoverable.
- It will not touch a page it did not create, anywhere, ever — including inside the sync root.
