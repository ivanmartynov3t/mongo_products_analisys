# silo-snapshot

Answers one question: **what does `prod_info_silo` hold for each product right now?** (issue #34, Plan 08 P2).

```bash
uv run tools/silo-snapshot/snapshot.py plan      # print the Markdown snapshot, write nothing
uv run tools/silo-snapshot/snapshot.py apply     # write reports/silo-snapshot.md and .json
uv run tools/silo-snapshot/test_snapshot.py      # offline tests
```

Needs a clone of `prod_info_silo` next to this repository; `git -C ../prod_info_silo fetch` before a run. Configuration: [`silo-snapshot.toml`](silo-snapshot.toml).

## Output

[`reports/silo-snapshot.md`](../../reports/silo-snapshot.md) and [`reports/silo-snapshot.json`](../../reports/silo-snapshot.json), regenerated on each run and committed. Use them instead of copying silo numbers by hand, for example in [`docs/coverage-scope.md`](../../docs/coverage-scope.md) or the README dashboard.

Per silo product (every product in the silo's `config/products.yaml`, plus any data folder or catalog product missing from it):

| Field | Source in the silo |
|---|---|
| Name, track, status | `config/products.yaml` (third-party products have no track or status) |
| Web pages | `data/<category>/<slug>/*.md`, generated `README.md`, `DIFF.md` and `repo_source_strings.md` excluded |
| Repo docs | `data/<category>/<slug>/repo_docs/**/*.md` |
| Catalog (source files) | entries for the product in `data/catalog_index.json`; the bracket counts entries that are indexed source files rather than stored documents (a stored document counts wherever it lives: the catalog sometimes files a page under another product's folder) |
| Web written | latest `updated_at` in the web pages' frontmatter: the last time a page was written or changed (the crawler does not rewrite unchanged pages) |
| Repo scraped | `scraped_at` in `repo_symbols_and_strings.json` |
| Seed URLs | `entry_urls` and `sitemap_urls` in `config/products.yaml` (public web entry points) |
| Repos | number of `github_repos` in `config/products.yaml`; **names are not published** |
| Analysis | `products/<category>/<slug>/` in this repository, matched by name only |

Most earlier hand-copied "docs" figures (for example in `docs/coverage-scope.md`) are the **catalog** count; products whose folder held only generated files are an exception. The catalog lists only classified documents, so it can be smaller than web pages plus repo docs.

The silo's `data/baseline_metrics.json` is not used: nothing in the silo regenerates it, and its counts are older than the catalog.

## Guarantees

- **Read-only.** The silo is read from git objects at the pinned `silo_ref` — never checked out, never written, and uncommitted silo changes are ignored. The snapshot records the commit SHA and its date, not the time of the run. The only files the tool can write are the two configured outputs; `guarded_write` refuses anything else.
- **Deterministic.** Same silo commit and same product folders, same bytes out (tested across processes with different hash seeds).
- **Fails loudly.** A missing or malformed `config/products.yaml` or `catalog_index.json` stops the run; it never produces a snapshot of zeros. Outputs must be in `reports/`.
- **Not evidence.** A count says what the silo holds, not what a product can do. It never becomes a ✅ or ❌ in a matrix.
- **No private names.** This repository is public and many silo repositories are private, so GitHub repositories are only counted, never named.
