#!/usr/bin/env bash
# One weekly command for the silo → analysis refresh (issue #40, Plan 08 P8).
#
#   tools/silo-sync/run.sh            # fetch the silo, regenerate every report, print a summary
#   tools/silo-sync/run.sh --no-fetch # use the silo refs already fetched
#
# Every tool reads the silo from git objects at origin/main (never its working tree) and
# writes only through its own guarded write (reports/*, and the gitignored .local/silo-batches/).
# Nothing is committed or pushed.
# Checks never stop the run; exit code: 0 all quiet, 1 something needs a human, 2 a step failed.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SILO="${SILO:-$ROOT/../prod_info_silo}"
REF=origin/main
cd "$ROOT"

FETCH=1
for a in "$@"; do
    case "$a" in
        --no-fetch) FETCH=0 ;;
        -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
        *) echo "unknown argument: $a" >&2; exit 2 ;;
    esac
done

command -v uv >/dev/null 2>&1 || { echo "error: uv not found" >&2; exit 2; }
git -C "$SILO" rev-parse --git-dir >/dev/null 2>&1 || { echo "error: no prod_info_silo clone at $SILO" >&2; exit 2; }
if [ "$FETCH" = 1 ]; then
    git -C "$SILO" fetch --quiet origin || { echo "error: git fetch failed in $SILO" >&2; exit 2; }
fi
SHA="$(git -C "$SILO" rev-parse --verify --quiet "$REF^{commit}")" || { echo "error: $REF not found in $SILO" >&2; exit 2; }
echo "silo $REF: ${SHA:0:10}"

# taxonomy-reconcile reads two files from a silo directory: give it exactly those files at
# $REF in a temp directory, so no step depends on the silo checkout.
# Both files exist in every prod_info_silo commit, so a missing one also means SILO points at
# some other repository: stop before any report is written.
TAX="$(mktemp -d)"
trap 'rm -rf "$TAX"' EXIT
for f in config/taxonomy.yaml data/catalog_index.json; do
    mkdir -p "$TAX/$(dirname "$f")"
    git -C "$SILO" show "$SHA:$f" > "$TAX/$f" 2>/dev/null \
        || { echo "error: $f missing at $REF in $SILO (is SILO a prod_info_silo clone?)" >&2; exit 2; }
done

failed=0
attention=0
summary=()

step() {  # step <name> <kind: write|check> <command...>
    local name="$1" kind="$2"; shift 2
    local out rc
    out="$("$@" 2>&1)"; rc=$?
    if [ "$kind" = write ]; then
        if [ $rc -ne 0 ]; then failed=1; summary+=("FAILED  $name (exit $rc)"); printf '%s\n' "$out" | tail -5 >&2; return 1
        else summary+=("ok      $name: $(printf '%s\n' "$out" | tail -1)"); fi
    else
        case $rc in
            0) summary+=("quiet   $name") ;;
            1) attention=1; summary+=("ATTEND  $name"); printf '\n--- %s ---\n%s\n' "$name" "$out" ;;
            *) failed=1; summary+=("FAILED  $name (exit $rc)"); printf '%s\n' "$out" | tail -5 >&2 ;;
        esac
    fi
}

S=(--silo "$SILO" --ref "$REF")  # every tool reads the same commit the header prints
# Order matters: the scope-trigger check reads the snapshot.
if step "silo snapshot"      write uv run -q tools/silo-snapshot/snapshot.py apply "${S[@]}"; then
    step "scope triggers (#18)" check uv run -q tools/scope-triggers/triggers.py
else
    summary+=("skipped scope triggers (#18): needs a fresh snapshot")
fi
step "review queue (#17)"    write uv run -q tools/silo-review/review.py apply "${S[@]}"
step "candidate signals"     write uv run -q tools/silo-candidates/candidates.py apply "${S[@]}"
step "evidence batches"      write uv run -q tools/silo-candidates/batch.py apply "${S[@]}"   # gitignored, for /silo-port
step "evidence gaps"         write uv run -q tools/evidence-gaps/gaps.py apply "${S[@]}"
step "taxonomy (#18)"        check uv run -q tools/taxonomy-reconcile/reconcile.py --check --silo "$TAX"
step "silo pins"             check uv run -q tools/silo-pins/pins.py check "${S[@]}"
# Re-pinning edits matrices, so the script only shows the plan; `pins.py repin apply` is a human step.
if step "silo pins re-pin plan" write uv run -q tools/silo-pins/pins.py repin plan "${S[@]}" \
   && ! printf '%s\n' "${summary[@]}" | grep -q "need a human first: 0 changed, 0 gone at ref"; then
    attention=1; summary+=("ATTEND  silo pins: a pinned page changed or is gone; re-check the claim, then re-pin by hand")
fi

echo
echo "Summary"
printf '  %s\n' "${summary[@]}"
stale="$(grep -m1 -oE '^[0-9]+ of [0-9]+ feature matrices' reports/review-queue.md 2>/dev/null || true)"
[ -n "$stale" ] && echo "  review queue: $stale cite a page that moved"
echo
echo "Changed files (review, then commit; anything outside reports/ is unexpected):"
git status --short | sed 's/^/  /'

if [ $failed -ne 0 ]; then exit 2; fi
exit $attention
