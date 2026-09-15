# Inputs — every piece of data the script consumes

There are exactly three inputs: credentials from the environment, settings from a TOML file, and the
Markdown files in the repository.

## 1. Credentials — `.env` in the repository root

`sync.sh` sources `.env` and exports its contents before starting Python. `.env` is gitignored and must
never be committed.

| Variable | Required | Meaning |
|---|---|---|
| `CONFLUENCE_BASE_URL` | yes | Wiki base URL, e.g. `https://3tsoftwarelabs.atlassian.net/wiki`. **The base, not a page URL** — every API path is appended to it. |
| `CONFLUENCE_USER_EMAIL` | yes | Atlassian account email; the username half of HTTP Basic auth. |
| `CONFLUENCE_API_TOKEN` | yes | API token from <https://id.atlassian.com/manage-profile/security/api-tokens>. |
| `CONFLUENCE_ROOT_FOLDER_ID` | no | Not read by `sync.py` — the root is configured in the TOML file. Handy for ad-hoc `curl`. |

A missing variable exits with code `2` and names the variable. The token value is never printed, never
logged and never written to the report.

Authentication is HTTP Basic with `email:token`. An unscoped ("classic") token inherits the account's own
Confluence permissions, which is what this tool expects.

## 2. Settings — `confluence-sync.toml`

Sits next to `sync.py` and is read on every run. This file is committed; it contains no secrets.

```toml
root_folder_id = "1375076366"   # the Confluence folder everything is published under
space_id = "11436034"           # numeric id of the space that folder lives in

exclude = [                     # paths not published
    ".git/**",
    ".idea/**",
    ".github/**",
    "templates/**",
    "tools/**",
]

directory_index = ["README.md", "index.md", "overview.md"]
```

| Key | Meaning |
|---|---|
| `root_folder_id` | The Confluence folder (or page) everything is created under. It is never modified itself, and nothing outside it is ever touched. |
| `space_id` | Numeric space id — **not** the space key. Required when creating a page. Find it in any page's API response as `spaceId`. |
| `exclude` | Glob patterns, matched against the repository-relative path. A path matches if `Path.match` matches it or if it starts with the pattern's directory prefix. |
| `directory_index` | File names that supply the body of their own directory's page instead of becoming a separate child page. Earlier entries win when a directory contains more than one. |

### What is deliberately excluded

Only human-readable documentation is published:

- `.github/` — Copilot instructions and prompt files: development tooling, not documentation.
- `templates/` — skeleton documents whose placeholder links intentionally point nowhere.
- `tools/` — this script and its own documentation.
- `.git/`, `.idea/` — repository and IDE internals.

To change what is published, edit `exclude` and re-run `plan`; the report shows the resulting tree before
anything is written.

## 3. The repository content

Every `*.md` file under the repository root that is not excluded, found recursively. Nothing else is read:
no images, no `.txt`, no source files. This repository happens to contain no images or binaries at all.

Per file, the script reads:

| What | Used for |
|---|---|
| the whole file text | conversion to Confluence storage format |
| the first `# ` heading | the page title |
| every `#`–`######` heading | building the anchor table so `#fragment` links can be resolved |
| every Markdown link | rewriting into page links |

The file's location determines its place in the page tree. Nothing else about the file — timestamps,
git history, permissions — is consulted.

## Inputs the script does *not* use

- No local state or cache file. All sync state lives on the Confluence pages themselves
  (see [07-change-detection.md](07-change-detection.md)), so the tool works identically from a fresh
  clone, from another machine, or from CI.
- No git metadata. A file is published because it exists and is not excluded, whether or not it is
  committed.
- No YAML front matter. This repository has none; front matter would currently be rendered as body text.
