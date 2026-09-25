# Plan 08 — Mechanical data porting from prod_info_silo

Research record and improvement plan for the **mechanical** (scripted) part of moving data from `prod_info_silo` into this repository. The LLM-assisted part (interpretation, mapping, clarification) is a separate, later plan.

Measured 2026-09-25 at silo commit `f1e28e8d` and `reports/review-queue.md`.

## Issues

| # | Proposal | Issue | Depends on |
|---|---|---|---|
| P1 | Make GitHub-repo citations checkable | [#33](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/33) | — |
| P2 | Silo snapshot report | [#34](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/34) | — |
| P3 | Automatic scope-trigger check | [#35](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/35) | P2 |
| P4 | Candidate-signal queue | [#36](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/36) | — |
| P5 | Evidence-gap report and seed proposals | [#37](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/37) | — |
| P6 | Machine-readable silo pins | [#38](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/38) | — |
| P7 | Staleness queue for reports and research | [#39](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/39) | — |
| P8 | One weekly command | [#40](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/40) | P2, P3, P4 |
| P9 | Silo clean-up | [prod_info_silo#45](https://github.com/ivanmartynov3t/prod_info_silo/issues/45) | — |

Recommended order: P1, P2, P3, P9 first (small, fix the incoming data); then P4 and P6 (prepare the LLM part); then P5, P7, P8.

## Rule for every proposal

No mechanical tool writes a capability status (✅/🧪/🗺️/❓/❌) into a matrix. Tools produce reports and queues; a human or the LLM step decides. Tools read the silo from git objects at a pinned ref, write only their configured output, and are deterministic and tested — the guarantees `tools/silo-review` already has.

## 1. Summary

- Only two scripts move silo data today, `silo-review` and `taxonomy-reconcile`. Both produce **checks and reports**; neither ports content.
- Everything else from the silo arrives **by hand**: prose citations in matrices and numbers copied into decision records.
- The weekly-maintenance prompts (`.github/prompts/weekly-maintenance/`) do not read the silo at all; they go to vendor websites directly.
- Result: the silo holds a large, classified corpus, but this repository uses little of it, and 72% of its citations cannot be checked against the silo.

## 2. What flows today

| Channel | Silo input | Tool | Output here | Automation |
|---|---|---|---|---|
| Staleness check | `.md` frontmatter (`source_url`, `checksum_sha256`, `http_last_modified`) + git history | `tools/silo-review/review.py` | `reports/review-queue.md` | Scripted, read-only, deterministic |
| Taxonomy match | `config/taxonomy.yaml`, `data/catalog_index.json` | `tools/taxonomy-reconcile/reconcile.py` | `reports/taxonomy-reconciliation.{md,tsv}` | Scripted; decisions entered by hand in `decisions.tsv` |
| Definition probes | silo corpus text | `tools/taxonomy-reconcile/probes.py` | evidence for decisions | Manual trigger |
| Citations in matrices | individual silo files | none | "silo copy … at commit …" in prose | Manual |
| Scope decisions | `products.yaml` status, doc counts | none | `docs/coverage-scope.md` | Manual; already stale (Policy Engine recorded 492 docs, now 529) |
| Weekly maintenance prompts | — | LLM prompts | matrices, reports | Do not use the silo |
| `source-extract` | private repository source | — | — | Reverted (`ac83447`); only an untracked `__pycache__` remains |

## 3. Silo data not used here

| Silo artefact | What it holds | Possible use |
|---|---|---|
| `catalog_index.json` → `by_product` sub-feature tags | classifier output per document | candidate matrix rows (P4) |
| `by_proposed_feature` | 10 `PROP-*` proposed features | the dictionary's Proposed Feature Registry |
| `by_dimension` | personas, deployment and licensing models, compliance standards | product reports, personas research |
| `config/products.yaml` | release status, track, seed URLs | scope decisions, dashboard, revisit triggers (P2, P3) |
| Per-product `README.md` / `DIFF.md` | silo dashboards and change lists | weekly "what changed" signal |
| `baseline_metrics.json` | per-product counts | dashboard (P2) |
| `repo_symbols_and_strings.json` (17 files) | code symbols and strings | source-code evidence for 3T products |

## 4. Effectiveness

**Citation coverage.** 677 distinct URLs are cited across 103 files; **486 (72%) are not checkable**.

| Domain | Not checkable | Why |
|---|---|---|
| mongodb.com | 65 | outside the silo's crawl scope |
| github.com | 55 | repo docs have no checksum in frontmatter, and URLs are SHA-pinned so they never match (P1) |
| reddit.com | 41 | not crawled; excluded by policy (ToS) |
| 3tsoftwarelabs.atlassian.net | 41 | internal Jira/Confluence, not crawled |
| forums, reviews, blogs | rest | not crawled |

**Matrices invisible to the staleness check.** 22 of 73 matrices cite no URL (mostly NoSQLBooster, TablePlus, Navicat); their sources are research files.

**Changes that reach no queue.** 19 cited URLs changed since review, yet the queue shows 0 stale matrices: the changes are cited only by reports and research, which are not queued (P7).

**Silo signals with no matrix row.** For the 13 analysed products that map to a silo slug, the silo tags **456** product × sub-feature signals (≥ 2 docs) that have no matrix row. Govern has no silo slug and is not counted. The classifier is noisy, so these are leads, not facts.

| Product | Silo docs | Silo-only signals | Matrix IDs |
|---|---|---|---|
| 3TL Bridge | 1,709 | 107 | 5 |
| 3T Lens | 533 | 63 | 1 |
| DBeaver | 814 | 61 | 37 |
| DataGrip | 1,033 | 46 | 16 |
| MongoDB Compass | 583 | 35 | 77 |
| Navicat | 15 | 10 | 93 |

3TL Bridge may be inflated by source documents it shares with Studio 3T EE (not verified). Navicat is the reverse case: the analysis goes far beyond what the silo holds.

## 5. Problems found

1. `data/3t/studio-3t/index.md` has held the License Manager page since `c7fd312a` (2026-09-14) — residue of prod_info_silo#44 not repaired by its fix (P9).
2. The silo's master `DIFF.md` reported "No Changes Detected" after the run that removed 4,979 files; cause not found (P9).
3. Repo-only products show `Last Retrieved: N/A` in the silo (P9).
4. Silo pins in matrices are prose, not machine-readable; re-pinning after #44 was manual (P6).
5. Scope triggers in `docs/coverage-scope.md` are checkable by script but are checked by hand (P3).

## 6. Proposals

| # | Proposal | Effect | Effort |
|---|---|---|---|
| P1 | Silo adds checksums to repo docs; `review.py` matches GitHub URLs by repo + path, ignoring the SHA | ~55 URLs become checkable, including Govern's internal sources | S + S |
| P2 | Generated `reports/silo-snapshot.{md,json}`: silo commit, per-product status, doc counts, last retrieved, seed URLs | one source for the README dashboard and scope decisions | S |
| P3 | Scope-trigger check on the snapshot | replaces a manual #18 step | S |
| P4 | Generated `reports/silo-candidates.md`: silo tags per product with no matrix row, filtered by doc count and probability | input queue for the LLM part | M |
| P5 | Evidence-gap report: no-URL matrices, thin products, compliant domains to add as silo seeds | shrinks the 72% | S + silo config |
| P6 | `silo: <path>@<commit>` pins in Source index, plus a bulk re-pin tool | re-pinning becomes one command | M |
| P7 | Staleness queue also covers reports and research | surfaces the 19 hidden changes | S |
| P8 | `tools/silo-sync/run.sh` chaining the steps above | the Monday procedure becomes one local command | S |
| P9 | Silo clean-up (items 1–3 above, plus a filename ↔ `source_url` audit test) | a trustworthy source | S |

## 7. Hand-off to the LLM part

Scripts can surface signals (P4, P5, P7). Deciding whether a signal is a real capability, which sub-feature it maps to, what status it gets and how to word it with a source needs judgement. That is part 2, which should start from the P4 candidate queue.

## Execution log

- 2026-09-25 — research done; plan written; issues #33–#40 and prod_info_silo#45 opened.
