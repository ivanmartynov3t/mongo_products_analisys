# confluence-sync — overview

`confluence-sync` publishes this repository's documentation to Confluence Cloud and keeps the published
page tree identical to the directory tree, with cross-document links preserved as real Confluence page
links.

It is a one-way mirror: the repository is the source of truth, Confluence is a rendering of it. Nothing
is ever read back from Confluence into the repository.

## What it guarantees

- **Identical structure.** Every published directory is a page; every published document is a page under
  the page for its directory. A `README.md` supplies the body of its own directory's page rather than
  appearing as a separate child.
- **Working links.** A relative link between two documents becomes a Confluence page link pointing at the
  page the target document was published as, heading anchors included.
- **Idempotence.** Re-running changes only what actually changed. A page whose rendered content, title and
  parent are unchanged costs no write at all — no new version, no notification to watchers.
- **Honest reporting.** Anything that cannot be represented faithfully in Confluence (see
  [05-limitations.md](05-limitations.md)) is written to a report, never silently altered or dropped.
- **Safe deletion.** Deleting a page requires an explicit flag, only ever touches pages this tool created,
  and moves them to the trash rather than destroying them.

## What it is not

- Not bidirectional. Edits made in Confluence to a managed page are overwritten on the next run that sees
  a content change, and are not merged back into the repository.
- Not a Confluence backup or export tool.
- Not a general-purpose Markdown→Confluence converter: the conversion covers the constructs this
  repository actually uses (see [04-conversion.md](04-conversion.md)).

## Document map

| Document | Covers |
|---|---|
| [02-usage.md](02-usage.md) | commands, flags, exit codes, a first run end to end |
| [03-inputs.md](03-inputs.md) | every input: credentials, configuration, which files are read |
| [04-conversion.md](04-conversion.md) | how a directory tree and Markdown become pages, titles and links |
| [05-limitations.md](05-limitations.md) | what cannot be represented faithfully, and what happens instead |
| [06-outputs.md](06-outputs.md) | everything written — locally, in Confluence, and to the console |
| [07-change-detection.md](07-change-detection.md) | how updates, moves, renames and deletions are decided |
| [08-verification.md](08-verification.md) | what `verify` proves, and what it deliberately does not |
| [09-confluence-api.md](09-confluence-api.md) | API behaviours that shaped the design, each one measured |
| [10-development.md](10-development.md) | code layout, tests, how to extend it safely |
| [11-operations.md](11-operations.md) | runbook: interrupted runs, failures, recovery, performance |

## Where the code lives

```
tools/confluence-sync/
├── sync.sh                  entry point: loads .env, hands off to uv
├── sync.py                  the whole implementation (single file)
├── confluence-sync.toml     what to publish and where
├── audit.py                 checks what Confluence renders (links, prose, structure)
├── test_sync.py             offline tests, no network
├── last-run-report.md       written by every run (not committed)
├── README.md                short usage summary
├── PROBE-FINDINGS.md        raw notes from probing the live API
└── doc/                     this documentation
```

`tools/` is excluded from publishing, so this documentation describes the tool without being pushed to
Confluence by it.
