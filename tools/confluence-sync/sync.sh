#!/usr/bin/env bash
# Publish this repository's documentation to Confluence.
#
#   ./tools/confluence-sync/sync.sh plan              # show what would change, publish nothing
#   ./tools/confluence-sync/sync.sh apply             # publish, then verify
#   ./tools/confluence-sync/sync.sh apply --delete    # publish, trash pages whose source is gone
#   ./tools/confluence-sync/sync.sh verify            # check Confluence still matches the repo
#
# Credentials come from .env in the repo root (gitignored):
#   CONFLUENCE_BASE_URL, CONFLUENCE_USER_EMAIL, CONFLUENCE_API_TOKEN
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="$(cd "$here/../.." && pwd)"

if [[ -f "$repo/.env" ]]; then
  set -a; . "$repo/.env"; set +a
fi

if [[ -z "${CONFLUENCE_BASE_URL:-}" || -z "${CONFLUENCE_USER_EMAIL:-}" || -z "${CONFLUENCE_API_TOKEN:-}" ]]; then
  echo "error: Confluence credentials missing in environment or $repo/.env (needs CONFLUENCE_BASE_URL, CONFLUENCE_USER_EMAIL, CONFLUENCE_API_TOKEN)" >&2
  exit 2
fi

command -v uv >/dev/null || { echo "error: uv is not installed (brew install uv)" >&2; exit 2; }

# If source extraction tool is present and local source repository is available, extract/refresh references
if [[ -f "$repo/tools/source-extract/extract.sh" ]]; then
  cfg_source_repo="/Users/ivan/Project/3t.tools.intellij/3t.tools"
  if [[ -d "${SOURCE_EXTRACT_REPO_PATH:-$cfg_source_repo}" ]]; then
    echo "Refreshing source code extracts before Confluence publish..."
    "$repo/tools/source-extract/extract.sh" extract
  fi
fi

exec uv run --quiet "$here/sync.py" "${@:-plan}"
