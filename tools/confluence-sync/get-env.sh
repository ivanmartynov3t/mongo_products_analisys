#!/usr/bin/env bash
# Resolves Confluence credentials from all available sources:
# 1. Existing environment variables (e.g. CI/CD secrets, active terminal exports)
# 2. Local .env file (in current directory or git root)

set -euo pipefail

find_env_file() {
  local dir="${1:-$PWD}"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/.env" ]]; then
      echo "$dir/.env"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}

SOURCE="environment variables"
ENV_FILE="$(find_env_file "$PWD" 2>/dev/null || true)"

# 1. Fallback / supplement with .env if found
if [[ -n "$ENV_FILE" && -f "$ENV_FILE" ]]; then
  while IFS='=' read -r key value || [[ -n "$key" ]]; do
    # Skip comments and empty lines
    [[ "$key" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$key" ]] && continue
    key="$(echo "$key" | xargs)"
    value="$(echo "$value" | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//")"
    # Do not overwrite if already set in environment
    if [[ -z "${!key:-}" ]]; then
      export "$key"="$value"
    fi
  done < "$ENV_FILE"
  SOURCE=".env ($ENV_FILE) + environment"
fi

# 2. Validation
MISSING=()
[[ -z "${CONFLUENCE_BASE_URL:-}" ]] && MISSING+=("CONFLUENCE_BASE_URL")
[[ -z "${CONFLUENCE_USER_EMAIL:-}" ]] && MISSING+=("CONFLUENCE_USER_EMAIL")
[[ -z "${CONFLUENCE_API_TOKEN:-}" ]] && MISSING+=("CONFLUENCE_API_TOKEN")

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo "Error: Missing required Confluence credentials: ${MISSING[*]}" >&2
  echo "Source checked: $SOURCE" >&2
  exit 1
fi

echo "Successfully resolved Confluence credentials from: $SOURCE"
echo "CONFLUENCE_BASE_URL=$CONFLUENCE_BASE_URL"
echo "CONFLUENCE_USER_EMAIL=$CONFLUENCE_USER_EMAIL"
MASKED_TOKEN="${CONFLUENCE_API_TOKEN:0:4}****${CONFLUENCE_API_TOKEN: -4}"
echo "CONFLUENCE_API_TOKEN=$MASKED_TOKEN"
