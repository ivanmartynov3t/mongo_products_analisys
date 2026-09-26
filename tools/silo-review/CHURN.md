# How trustworthy is the silo's change signal?

Measured 2026-09-25 against `prod_info_silo` at `cde319c742` (history since 2026-09-08, 133 commits), for the **174 cited URLs the silo tracks** — the true review load, not the 8,000-document corpus. Re-run with `uv run tools/silo-review/review.py churn`.

## Result

| ISO week | File touched | Checksum changed | Content really changed |
|---|---|---|---|
| 2026-W37 | 172 | 136 | 20 |
| 2026-W38 | 168 | 43 | 5 |
| 2026-W39 | 120 | 49 | 6 |

- **"File touched" is useless as a signal**: pipeline and taxonomy commits rewrite frontmatter on nearly every page every week.
- **The silo's own `checksum_sha256` is ~8× too noisy.** It hashes the rendered page body, so it moves whenever the silo changes how it renders a page, not only when the page changes. Week 37 is the silo's first week (its crawler was still evolving); on one day (2026-09-11) it stripped documentation menus and banners from 131 of the 174 cited pages at once.
- **Real content change in steady state: 5–6 cited pages per week (~3%).** That is the expected weekly review load for #17.

## What counts as "content really changed"

Compared: the page as the silo holds it now against its **baseline** — the silo's copy from the matrix's review date, or its first copy when the silo is younger than the review. Comparing endpoints, not every intermediate version, cancels pages that oscillate (rotating tips, A/B banners).

Both versions are reduced to **substantive lines**: silo header and H1 title removed, image and link targets removed, punctuation and markdown syntax removed, lower-cased, at least 6 words. Lines that appear on 3 or more pages of the same product directory — at the baseline commit or now — are **site chrome** (cookie notices, "Docs Menu", "Found this useful?", geo banners) and ignored.

A page **changed** if it gained at least one substantive line, or lost ≥ 30% of them. The report quotes up to two added lines, shows `+added / −removed of baseline` and flags pages whose text disappeared entirely (emptied, moved or failed to render).

## The second signal: server `Last-Modified`

Used only where the silo has no copy from before the review date. Measured per domain on cited pages:

| Domain | Real dates | Equal to the fetch day | Missing |
|---|---|---|---|
| studio3t.com | 91 | 5 | 6 |
| visualeaf.com | 1 | 21 | 1 |
| navicat.com | 0 | 7 | 0 |
| mongodb.com, nosqlbooster.com, dbeaver.com | 0 | 0 | all |

- A value **on or after the day the silo fetched the page** is the server stamping the request time (VisuaLeaf, Navicat) and is ignored.
- A day shared by **≥ 20% of a domain's pages** is a site rebuild, not an edit: 688 of ~760 studio3t.com pages carry 2026-09-07 or 2026-09-08. Those days are ignored.
- What remains (8 URLs on the first run) are individual page edits.

## Known limits

- The silo's history starts 2026-09-08; every matrix reviewed earlier is compared against the silo's first copy, so edits between the review and 2026-09-08 are invisible unless `Last-Modified` reports them.
- 472 of 660 cited URLs (forums, issue trackers, Reddit, GitHub) were not tracked by the silo on 2026-09-25 and are reported as *not checkable* — never as unchanged. Since #33, GitHub file permalinks are matched by repository and path (12 of 55 cited GitHub URLs at silo `55dbb2cb`); GitHub issue, release, wiki and repository pages remain not checkable.
- Marketing banners unique to one page (e.g. a MongoDB promo line) still register as change; a reviewer dismisses them in seconds.
- A full run takes ~2–4 minutes (history of every cited page is read from git objects).
