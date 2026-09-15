# Development

## Layout

`sync.py` is a single file, ordered as a pipeline. Section banners mark the boundaries.

| Section | Contents |
|---|---|
| model | `Node` (one page-to-be), `Issue` (one reportable problem) |
| discovery | `discover()` builds the tree; `assign_titles()` + `qualified()` resolve titles; `humanize()`, `slugify()` |
| rendering | `Renderer` — Markdown to storage format, link rewriting; `code_macro()`, `to_xhtml()` |
| client | `Confluence` — retry policy, pagination |
| remote side | `RemotePage`, `walk_descendants()`, `read_remote()` |
| planning | `plan()` ties discovery and rendering together; `digest_of()` |
| applying | `apply_tree()` — the diff engine; `write_state()` |
| verification | `verify()` |
| reporting | `write_report()` |
| main | argument parsing, wiring |

Dependencies are declared inline (PEP 723) at the top of the file, so `uv run` resolves them per run with
no virtualenv to manage. They are `httpx` and `markdown-it-py`; keeping the list this short is deliberate.

## The one ordering constraint

Titles must be final before any body is rendered, because links are rewritten to titles. So:

```
discover()  →  assign_titles()  →  render every node  →  digest every node
```

Anything that changes a title after rendering silently invalidates every link pointing at it. If you add a
feature that adjusts titles, adjust them in `assign_titles()`, never later.

Within `apply_tree()`, pages are walked breadth-first so a parent always exists before its children are
created.

## Tests

```bash
uv run tools/confluence-sync/test_sync.py
```

Plain asserts, no test framework, no network, no fixtures on disk. Each test builds a throwaway repository
in a temp directory and runs the real `discover` / `assign_titles` / `Renderer` code over it. Covered:
slug rules, exclusion, index files, parenting, collision qualification, reserved titles, anchors, dropped
line anchors, broken links, external links, code macros, tables, XHTML self-closing, CDATA escaping, and
the digest reacting to a retitle.

Not covered by tests, because it needs a live instance: the client's retry policy, `read_remote`,
`apply_tree` and `verify`. Those are exercised by running `plan` (which is read-only) against the real
space.

## Extending it

**Adding a Markdown construct.** Add a rule to `Renderer._install_rules()` keyed by the markdown-it token
type, and a test. Rules receive `(tokens, idx, options, env)`; `env["node"]` is the page being rendered,
`env["stack"]` carries closing tags between `*_open` and `*_close`.

**Adding images/attachments.** Upload through v1 (`POST /rest/api/content/{id}/child/attachment`), then
emit `<ac:image><ri:attachment ri:filename="…"/></ac:image>`. The link classifier in `Renderer._resolve`
is where a non-`.md` target would be routed to an attachment instead of being reported as unresolvable.

**Making it faster.** The current run is sequential: ~360 pages in about 7 minutes for a full publish,
90 seconds for a no-op re-run. The safe parallelisation is per depth level — siblings concurrently,
levels in order, since a parent id must exist before its children are created. Read phases
(`read_remote`'s property fetches, which dominate a no-op run) parallelise without ordering constraints.
Do not add concurrency until you have deliberately tested the resume path, because a resume bug and a
concurrency bug together are very hard to separate.

**Changing what is published.** Prefer `confluence-sync.toml` over code. Run `plan` and read the tree in
the report before applying.

## Things to be careful about

- **Do not switch links back to `ri:content-id`.** It renders a broken-link placeholder — see
  [09-confluence-api.md](09-confluence-api.md).
- **Do not hash the source Markdown** instead of the rendered body. Retitles would stop propagating and
  links would silently break.
- **Do not treat a 404 as absence.** The API returns transient 403/404s. Absence is only proven by a
  successful read that does not contain the page.
- **Do not widen deletion.** Only pages carrying the `repo-sync` property may be trashed, and only with
  `--delete`.
- **Do not call `descendants` without `depth`.** It defaults to 2 and truncates silently.
