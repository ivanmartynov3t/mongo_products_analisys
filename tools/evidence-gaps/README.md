# evidence-gaps

Shows **where the silo cannot check this repository's sources** (issue #37, Plan 08 P5).

```bash
uv run tools/evidence-gaps/gaps.py plan      # print the report, write nothing
uv run tools/evidence-gaps/gaps.py apply     # write reports/evidence-gaps.md
uv run tools/evidence-gaps/test_gaps.py      # offline tests
```

Needs a clone of `prod_info_silo` next to this repository and a current [`reports/silo-snapshot.json`](../../reports/silo-snapshot.json) (`tools/silo-snapshot`). Configuration: [`evidence-gaps.toml`](evidence-gaps.toml).

## Output

[`reports/evidence-gaps.md`](../../reports/evidence-gaps.md):

1. **Matrices that cite no URL**, which the staleness check cannot cover.
2. **Thin silo coverage:** products whose silo holds fewer documents (web pages + repo docs, from the snapshot) than their matrices have IDs, and analysed products with no silo product.
3. **Cited URLs the silo does not track** (*not checkable* or *dropped by silo*, as classified by `tools/silo-review`), counted per domain in four groups:
   - crawlable and compliant: candidate silo seeds;
   - excluded by policy (terms of service, review sites, forums);
   - internal systems;
   - GitHub pages that are not files.

   The groups are set in the config; anything not listed counts as crawlable.

Adding seed URLs to the silo is out of scope: that is [prod_info_silo#47](https://github.com/ivanmartynov3t/prod_info_silo/issues/47), which takes this report as input.

## Guarantees

- **Read-only.** Uses `tools/silo-review` for citation parsing, silo reads (git objects at the pinned ref) and classification; the only file it can write is the configured output in `reports/`.
- **Deterministic** for the same silo commit, snapshot and repository content (tested).
- **Domains, not URLs.** The report counts URLs per domain and lists none.
- **Not evidence.** A gap is a prompt for a human; it never changes a ✅ or ❌.
