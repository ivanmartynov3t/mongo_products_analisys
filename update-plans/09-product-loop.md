# Plan 09 — product loop

Checklist for [`/silo-port`](../.claude/commands/silo-port.md) ([Plan 09](09-silo-porting-llm.md#flow)). The command takes the first unticked item, works it on its own branch, opens one PR, and ticks it. Sub-items are ticked on the branch, only when done and verified.

Cycle started: 2026-09-26 · silo ref: `55dbb2cb` · counts from `reports/silo-candidates.md` (web-backed / all candidates).

For each product the sub-items are:
- **candidates** — triage the web-backed candidates; one ledger row each;
- **review queue** — re-check the rows and reports whose cited page changed;
- **pins** — apply unchanged re-pins; re-check the rows behind changed ones;
- **evidence gaps** — add a public source to matrices that cite no URL, where the silo has one;
- **cascade** — update the product's feature and product reports;
- **validator** — `validate.py` exits 0, or the remaining findings are listed in the PR;
- **PR** — opened and reviewed. The merge lands the item's ticks on `main`, so an item with an open PR is not started again.

An item with nothing to do is ticked "no changes" on the next item's branch and gets no PR of its own.

## First

- [ ] **Scope triggers** — `uv run tools/scope-triggers/triggers.py`; update `docs/coverage-scope.md` when a trigger fires
  - [ ] validator · [ ] PR

## Third-party products

- [ ] **DataGrip** (`third-party/datagrip`) — 33 / 33 · pilot, go/no-go gate after this item
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **DBeaver** (`third-party/dbeaver`) — 34 / 34
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **MongoDB Compass** (`third-party/mongodb-compass`) — 14 / 18
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **NoSQLBooster** (`third-party/nosqlbooster`) — 14 / 14
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **TablePlus** (`third-party/tableplus`) — 8 / 8
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **VisuaLeaf** (`third-party/visual-eaf`) — 8 / 8
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **Navicat** (`third-party/navicat`) — 7 / 7 · thin silo coverage (15 documents for 95 matrix IDs)
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR

## 3T products

Only web-backed candidates are in scope; candidates backed only by repository or source documents wait for owner decision 3.

- [ ] **Studio 3T** (`3t/studio-3t`) — 10 / 10 · 6 mostly shared
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **3T Explore** (`3t/3t-explore`) — 3 / 7
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **3T Access** (`3t/3t-access`) — 2 / 8
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **3T MCP** (`3t/3t-mcp`) — 1 / 4
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **3TL Bridge** (`3t/3tl-bridge`) — 1 / 61
  - [ ] candidates · [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **3T Lens** (`3t/3t-lens`) — 0 / 27
  - [ ] review queue · [ ] pins · [ ] evidence gaps · [ ] cascade · [ ] validator · [ ] PR
- [ ] **Govern** (`3t/govern`) — no silo product; review queue and pins only
  - [ ] review queue · [ ] pins · [ ] cascade · [ ] validator · [ ] PR

## Last

- [ ] **Cross-product reports** — low-level comparison and gap analysis (prompt 03), after every product above is merged
  - [ ] cascade · [ ] validator · [ ] PR
- [ ] **README dashboard** — rebuild `README.md` with [`update-readme-dashboard.prompt.md`](../.github/prompts/update-readme-dashboard.prompt.md), after the cross-product reports are merged
  - [ ] README rebuilt · [ ] fixed skeleton kept · [ ] PR
