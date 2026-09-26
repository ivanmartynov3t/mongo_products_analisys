# silo-pins

Keeps the references to `prod_info_silo` copies machine-readable (issue #38, Plan 08 P6).

```bash
uv run tools/silo-pins/pins.py list            # every pin and its state at the silo ref
uv run tools/silo-pins/pins.py check           # exit 1 if a pin is broken or malformed
uv run tools/silo-pins/pins.py repin plan      # which pins would move to the silo ref (writes nothing)
uv run tools/silo-pins/pins.py repin apply     # move them
uv run tools/silo-pins/test_pins.py            # offline tests
```

Needs a clone of `prod_info_silo` next to this repository; `git -C ../prod_info_silo fetch` before a run. Configuration: [`silo-pins.toml`](silo-pins.toml).

## Pin format

On a Source index line, after the URL (in reports without a Source index, inline where the source is cited):

```markdown
- S2: https://studio3t.com/ — homepage (silo: `data/3t/3t-website-2026/index.md@f1e28e8d`)
```

One silo file at one silo commit (7–40 hex). Text that looks like a pin but does not match (`Silo:`, no space, `@HEAD`, fewer than 7 hex) is reported as a warning, and `check` exits 1. So is a silo file mentioned without `@<commit>` (silo `data/…/page.md`); directory mentions and names such as `prod_info_silo` are not. Prose such as "silo commit `cde319c7`" without a path is not a pin. The rule is in [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md) and the [matrix template](../../templates/feature-matrix-template.md).

## States

| State | Meaning | `repin apply` |
|---|---|---|
| current | pinned at the silo ref already | — |
| unchanged | same content at the silo ref (same `checksum_sha256`, or the same body when there is none) | moves the pin to the ref |
| changed | the content differs at the ref | leaves it: a human re-checks the claim, then updates the pin |
| gone at ref | the file no longer exists at the ref | leaves it |
| broken | the commit is unknown or not on the silo ref's history (unmerged, local-only, or ahead of `--ref`), or the file does not exist at it | leaves it; `check` exits 1 |

## Guarantees

- **Silo read-only.** Read from git objects only; never checked out or written.
- **`list`, `check` and `repin plan` write nothing.**
- **`repin apply` changes only pin commits.** Each rewritten file is compared with the original with every pin commit removed; any other difference aborts the write. Only files holding pins being moved can be written. A second run is a no-op.
- **Pins identify content, not check dates.** `repin apply` moves every *unchanged* pin, so a pin never records when a claim was checked. Write the check date in the prose next to it ("checked 2026-09-25").
- **Not evidence.** A moved pin means the silo holds the same text at a newer commit. It never becomes a ✅ or ❌ in a matrix.
