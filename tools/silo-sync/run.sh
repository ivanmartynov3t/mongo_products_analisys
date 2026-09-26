#!/usr/bin/env bash
# One weekly command for the silo → analysis refresh (issue #40, Plan 08 P8).
#
#   tools/silo-sync/run.sh            # fetch the silo, regenerate every report, print a summary
#   tools/silo-sync/run.sh --no-fetch # use the silo refs already fetched
#
# Every step writes only through its own tool's guarded write (reports/*). Nothing is
# committed or pushed. Checks (taxonomy, scope triggers, pins) never stop the run; their
# results go into the summary and the exit code: 0 all quiet, 1 something needs a human,
# 2 a step failed.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SILO="${SILO:-$ROOT/../prod_info_silo}"
cd "$ROOT"

FETCH=1
for a in "$@"; do
    case "$a" in
        --no-fetch) FETCH=0 ;;
        -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
        *) echo "unknown argument: $a" >&2; exit 2 ;;
    esac
done

command -v uv >/dev/null 2>&1 || { echo "error: uv not found" >&2; exit 2; }
[ -d "$SILO/.git" ] || { echo "error: no prod_info_silo clone at $SILO" >&2; exit 2; }

if [ "$FETCH" = 1 ]; then
    git -C "$SILO" fetch --quiet origin || { echo "error: git fetch failed in $SILO" >&2; exit 2; }
fi
echo "silo origin/main: $(git -C "$SILO" rev-parse --short=10 origin/main)"

failed=0
attention=0
summary=()

step() {  # step <name> <kind: write|check> <command...>
    local name="$1" kind="$2"; shift 2
    local out rc
    out="$("$@" 2>&1)"; rc=$?
    if [ "$kind" = write ]; then
        if [ $rc -ne 0 ]; then failed=1; summary+=("FAILED  $name (exit $rc)"); printf '%s\n' "$out" | tail -5 >&2
        else summary+=("ok      $name: $(printf '%s\n' "$out" | tail -1)"); fi
    else
        case $rc in
            0) summary+=("quiet   $name") ;;
            1) attention=1; summary+=("ATTEND  $name"); printf '\n--- %s ---\n%s\n' "$name" "$out" ;;
            *) failed=1; summary+=("FAILED  $name (exit $rc)"); printf '%s\n' "$out" | tail -5 >&2 ;;
        esac
    fi
}

# Order matters: the snapshot feeds the trigger and gap checks.
step "silo snapshot"         write uv run -q tools/silo-snapshot/snapshot.py apply
step "review queue (#17)"    write uv run -q tools/silo-review/review.py apply
step "candidate signals"     write uv run -q tools/silo-candidates/candidates.py apply
step "evidence gaps"         write uv run -q tools/evidence-gaps/gaps.py apply
# reconcile.py reads the silo's working tree, not git objects: only run it when the
# checkout is exactly origin/main and clean (this script never changes the silo checkout).
if [ "$(git -C "$SILO" rev-parse HEAD)" = "$(git -C "$SILO" rev-parse origin/main)" ] \
   && [ -z "$(git -C "$SILO" status --porcelain)" ]; then
    step "taxonomy (#18)"    check uv run -q tools/taxonomy-reconcile/reconcile.py --check
else
    failed=1
    summary+=("FAILED  taxonomy (#18): silo checkout is not a clean origin/main (git -C $SILO checkout main && git -C $SILO pull)")
fi
step "scope triggers (#18)"  check uv run -q tools/scope-triggers/triggers.py
step "silo pins"             check uv run -q tools/silo-pins/pins.py check

echo
echo "Summary"
printf '  %s\n' "${summary[@]}"
stale="$(grep -m1 -oE '^[0-9]+ of [0-9]+ feature matrices' reports/review-queue.md 2>/dev/null || true)"
[ -n "$stale" ] && echo "  review queue: $stale cite a page that moved"
echo
echo "Changed files (review, then commit):"
git status --short -- reports/ | sed 's/^/  /'

if [ $failed -ne 0 ]; then exit 2; fi
exit $attention
