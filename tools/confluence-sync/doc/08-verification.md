# Verification

`apply` verifies automatically when publishing finishes; `verify` runs the same checks on their own.
Either way the check reads the tree **back from Confluence** and compares it with a freshly computed plan.
It never trusts what the publish step believed it did.

```bash
./tools/confluence-sync/sync.sh verify
```

Exit code `0` means passed, `1` means failed. Every failure is printed (first 30) and written to the
report.

## What it proves

| Check | Failure message |
|---|---|
| every source file has a page | `missing page for <path>` |
| every managed page still has a source file | `unexpected managed page for <path> (orphan)` |
| no unmanaged pages inside the sync root | `N page(s) under the root are not managed by the sync: …` |
| each page's title matches the plan | `title differs for <path>: 'a' != 'b'` |
| each page's stored digest matches the current source | `stale content for <path>` |
| each page hangs under the right parent | `wrong parent for <path>` |
| the parent page itself exists | `cannot check parent of <path>: <parent> has no page` |
| every published page link names a title that exists | `<path> links to unknown title 'X'` |

The last one is the important one. Because Confluence resolves links by title, a link to a title that does
not exist renders as a broken-link placeholder rather than an error at publish time — so it would
otherwise go unnoticed until a reader clicked it.

Orphans you deliberately kept (by not passing `--delete`) are excused, but only those exact pages. Any
other orphan still fails the run.

## What it deliberately does not do

- **It does not re-fetch each page's rendered HTML.** Verification compares the stored digest against a
  freshly computed one, which is one API call per page rather than two, and catches the same drift.
  Checking the *rendered* output of all 360 pages is a useful occasional audit — see below — but it is not
  part of the routine check.
- **It does not check formatting quality.** That a table rendered as a table, rather than as a wall of
  pipes, is covered by the tests in `test_sync.py`, not by verification.
- **It does not inspect pages outside the sync root**, other than to reserve their titles.

## Auditing the rendered output — `audit.py`

`verify` proves the tree is complete and current. It cannot tell you whether a page *reads* correctly: a
page can be stored exactly as intended and still render a broken link, or show a wall of raw Markdown
because a construct was not converted.

```bash
set -a; . ./.env; set +a
uv run tools/confluence-sync/audit.py              # 25 random pages
uv run tools/confluence-sync/audit.py --all        # every page
uv run tools/confluence-sync/audit.py --sample 60
```

It fetches pages with `body-format=view` — the HTML Confluence actually serves — and checks:

| Check | Catches |
|---|---|
| no broken-link placeholder | a link whose target title does not exist |
| internal links resolve to pages inside the tree | a link escaping the synced subtree |
| a page whose source has links renders some | link rewriting silently dropping everything |
| no raw Markdown in visible text | an unconverted construct: `[text](url)`, `##`, fences, table rules, bullets — code blocks are excluded, since Markdown inside code is not a leak |
| tables, headings and code blocks are real elements | a table rendered as a wall of pipes |
| the source footer is present | a page that cannot be traced to its file |

It also re-checks structure exhaustively: every `.md` file on disk is published, every page maps to a
file, every parent is right.

Exit code `1` on any problem, so it can gate a release as well.

## Using it as a gate

`verify` makes no writes and exits non-zero on mismatch, so it works as a scheduled job or CI step to
catch drift — someone editing a managed page by hand in Confluence, or a document added to the repository
without a publish. It needs the same `.env` credentials as a publish.
