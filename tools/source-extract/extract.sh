#!/usr/bin/env bash
# Extract comments and code snippets from 3t.tools source repository.
#
#   ./tools/source-extract/extract.sh plan      # show what would be extracted
#   ./tools/source-extract/extract.sh extract   # extract and write markdown files
#   ./tools/source-extract/extract.sh check     # verify committed extracts match source (fails on drift)
#
# Environment variables:
#   SOURCE_EXTRACT_REPO_PATH: override path to local 3t.tools clone

set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="$(cd "$here/../.." && pwd)"

command -v uv >/dev/null || { echo "error: uv is not installed (brew install uv)" >&2; exit 2; }

exec uv run --quiet "$here/extract.py" "${@:-extract}"
