#!/usr/bin/env bash
# Offline checks for run.sh's argument and input handling (no silo needed).
#
#   tools/silo-sync/test_run.sh
set -uo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)/run.sh"
fails=0
expect() {  # expect <name> <exit code> <command...>
    local name="$1" want="$2"; shift 2
    "$@" >/dev/null 2>&1; local got=$?
    if [ "$got" -ne "$want" ]; then echo "FAIL $name: exit $got, expected $want"; fails=$((fails + 1)); fi
}
expect "syntax"             0 bash -n "$RUN"
expect "--help"             0 "$RUN" --help
expect "unknown argument"   2 "$RUN" --bogus
expect "no silo clone"      2 env SILO=/nonexistent/prod_info_silo "$RUN" --no-fetch
if [ "$fails" -ne 0 ]; then echo "FAILED ($fails)"; exit 1; fi
echo "ok: all silo-sync tests passed"
