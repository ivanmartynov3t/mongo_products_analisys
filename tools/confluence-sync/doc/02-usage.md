# Usage

## Commands

```bash
./tools/confluence-sync/sync.sh plan       # work out what would change; write nothing
./tools/confluence-sync/sync.sh apply      # publish, then verify
./tools/confluence-sync/sync.sh verify     # check Confluence still matches the repository
```

Running `sync.sh` with no argument is the same as `plan`. **This is deliberate: the default does not
publish anything.** If you run the script bare and nothing appears in Confluence, that is the safe
default, not a failure.

### `plan`

Walks the repository, resolves titles, converts every document and rewrites every link, then reports what
it would do. It reads from Confluence (to learn which pages already exist and which titles are already
taken) but writes nothing to it. Safe to run at any time.

### `apply`

Does everything `plan` does, then creates, updates and moves pages so Confluence matches the repository.
Finishes by running the same checks as `verify` and reports the result.

### `verify`

Re-reads the published tree from Confluence and checks it against a freshly computed plan. Makes no
writes. Exits non-zero on any mismatch, so it can be used as a CI gate.

## Flags

| Flag | Effect |
|---|---|
| `--delete` | Move pages whose source file no longer exists to the trash. Without it, such pages are only reported. Only meaningful with `apply`. |
| `--verbose` | Print a line per created (`+`) and updated (`~`) page, and a line per retried request. |

## Exit codes

| Code | Meaning |
|---|---|
| `0` | success — for `apply` and `verify`, this also means verification passed |
| `1` | verification failed; the report lists every mismatch |
| `2` | setup problem: `.env` missing, a required variable unset, or `uv` not installed |

A failure *during* publishing (an API error that survives all retries) raises and aborts the run with a
non-zero exit and a traceback naming the failing request. Pages already published stay published; the run
is resumable (see [11-operations.md](11-operations.md)).

## A first run, end to end

```bash
# 1. See what would happen. Nothing is published.
./tools/confluence-sync/sync.sh plan

# 2. Read the report: the full page tree, and every link that cannot be published faithfully.
less tools/confluence-sync/last-run-report.md

# 3. Publish. Verification runs automatically at the end.
./tools/confluence-sync/sync.sh apply --verbose

# 4. Later, after editing documentation, re-run. Unchanged pages cost nothing.
./tools/confluence-sync/sync.sh apply

# 5. After deleting or renaming documents, let it clean up the pages left behind.
./tools/confluence-sync/sync.sh apply --delete
```

Step 2 matters most on a first run: the report contains the planned title of all 360 pages, and titles are
what links resolve against. Reviewing them before publishing is much cheaper than retitling afterwards.

## Requirements

- `uv` on the PATH (`brew install uv`). Python dependencies are declared inline in `sync.py` and resolved
  by `uv` per run; there is no virtualenv to create or activate.
- A `.env` file in the repository root — see [03-inputs.md](03-inputs.md).
- Permission to create pages in the target space, which for a personal space means being its owner.
