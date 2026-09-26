#!/usr/bin/env bash
# Offline tests for run.sh: arguments, inputs, exit-code mapping and --silo forwarding.
# A stub `uv` stands in for the tools; a throwaway silo repository stands in for the silo.
#
#   tools/silo-sync/test_run.sh
set -uo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)/run.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
fails=0
fail() { echo "FAIL $1"; fails=$((fails + 1)); }
expect() {  # expect <name> <exit code> <command...>
    local name="$1" want="$2"; shift 2
    "$@" >"$TMP/out" 2>&1; local got=$?
    [ "$got" -eq "$want" ] || { fail "$name: exit $got, expected $want"; sed 's/^/    /' "$TMP/out"; }
}

# stub uv: logs its arguments; exits $STUB_CODE when they contain $STUB_MATCH, else 0
mkdir -p "$TMP/bin"
cat > "$TMP/bin/uv" <<'STUB'
#!/usr/bin/env bash
echo "$*" >> "$STUB_LOG"
case "$*" in *"${STUB_MATCH:-<none>}"*) exit "${STUB_CODE:-0}" ;; esac
echo "ok"
STUB
chmod +x "$TMP/bin/uv"

# throwaway silo with origin/main holding the two files taxonomy-reconcile reads
silo="$TMP/silo"
git init -q "$silo"
mkdir -p "$silo/config" "$silo/data"
echo "features: {}" > "$silo/config/taxonomy.yaml"
echo "{}" > "$silo/data/catalog_index.json"
git -C "$silo" add -A
git -C "$silo" -c user.name=t -c user.email=t@t -c commit.gpgsign=false commit -qm init
git -C "$silo" update-ref refs/remotes/origin/main HEAD
git -C "$silo" checkout -q --detach  # a checkout that is not origin/main must not matter

run() { env PATH="$TMP/bin:$PATH" SILO="$silo" STUB_LOG="$TMP/log" "$@" "$RUN" --no-fetch; }

expect "syntax"                 0 bash -n "$RUN"
expect "--help"                 0 "$RUN" --help
expect "unknown argument"       2 "$RUN" --bogus
expect "no silo clone"          2 env SILO="$TMP/none" "$RUN" --no-fetch
mkdir -p "$TMP/notgit/.git"
expect "empty .git is not a clone" 2 env SILO="$TMP/notgit" "$RUN" --no-fetch

: > "$TMP/log"
expect "all quiet"              0 run env
# every tool that reads the silo gets --silo (scope-triggers reads only the snapshot)
grep -v -- "--silo" "$TMP/log" | grep -v "scope-triggers" | grep -q . && fail "every silo tool gets --silo: $(grep -v -- --silo "$TMP/log" | grep -v scope-triggers | head -1)"
grep -q -- "silo-snapshot/snapshot.py apply --silo $silo" "$TMP/log" || fail "SILO forwarded to the snapshot"
grep -q -- "reconcile.py --check --silo " "$TMP/log" || fail "reconcile gets a silo directory"
grep -q -- "reconcile.py --check --silo $silo" "$TMP/log" && fail "reconcile reads a temp copy at origin/main, not the checkout"
expect "a check needs a human"  1 run env STUB_MATCH="pins.py check" STUB_CODE=1
expect "a check errors"         2 run env STUB_MATCH="triggers.py" STUB_CODE=2
expect "a write step fails"     2 run env STUB_MATCH="review.py apply" STUB_CODE=1
: > "$TMP/log"
expect "snapshot fails"         2 run env STUB_MATCH="snapshot.py" STUB_CODE=1
grep -q "triggers.py" "$TMP/log" && fail "triggers are skipped when the snapshot failed"
grep -q "skipped scope triggers" "$TMP/out" || fail "skipped triggers are reported"

if [ "$fails" -ne 0 ]; then echo "FAILED ($fails)"; exit 1; fi
echo "ok: all silo-sync tests passed"
