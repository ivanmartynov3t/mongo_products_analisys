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

1. **Matrices that cite no URL**, which the staleness check cannot cover. Every such matrix is listed; `tools/silo-review` lists only those that also have an `Analysis date` (the rest it reports as undated).
2. **Thin silo coverage:** products whose silo holds fewer documents (web pages + repo docs, from the snapshot) than their matrices have IDs, and analysed products with no silo product.
3. **Cited URLs the silo does not track** (*not checkable* or *dropped by silo*, as classified by `tools/silo-review`), counted per domain in four groups:
   - crawlable and compliant: candidate silo seeds;
   - excluded by policy (terms of service, review and comparison sites, forums and issue trackers, paywalled sites);
   - internal systems;
   - other GitHub pages (organisation pages, trees, links without a file).

   Domains are matched with their subdomains, ignoring any port. The domain groups are set in the config; anything not listed counts as crawlable. GitHub URLs that are not file permalinks are grouped by path: repository, release, tag and wiki pages are crawlable (issue #37); issues, pull requests and discussions are excluded, like other issue trackers.

   Section 2 uses the snapshot; sections 1 and 3 read the silo at its ref. When the two commits differ, the report says so at the top.

Adding seed URLs to the silo is out of scope: that is [prod_info_silo#47](https://github.com/ivanmartynov3t/prod_info_silo/issues/47), which takes this report as input.

## Guarantees

- **Read-only.** Uses `tools/silo-review` for citation parsing, silo reads (git objects at the pinned ref) and classification; the only file it can write is `reports/evidence-gaps*.md`.
- **Deterministic** for the same silo commit, snapshot and repository content (tested).
- **Domains, not URLs.** The report counts URLs per domain and lists none.
- **Not evidence.** A gap is a prompt for a human; it never changes a ✅ or ❌.
