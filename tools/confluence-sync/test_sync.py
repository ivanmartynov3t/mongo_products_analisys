# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27", "markdown-it-py>=3.0"]
# ///
"""Tests for the parts of confluence-sync that do not touch the network.

    uv run tools/confluence-sync/test_sync.py

Everything here works on a throwaway repository built in a temp directory, so the
tests never read the real documentation and never call Confluence.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sync  # noqa: E402

CFG = {
    "exclude": [".git/**", "templates/**"],
    "directory_index": ["README.md", "index.md", "overview.md"],
    "root_folder_id": "ROOT",
    "repo_url": "https://example.invalid/repo",
    "repo_branch": "main",
    "space_id": "SPACE",
}

failures: list[str] = []


def check(name: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{name}\n     expected: {expected!r}\n     actual:   {actual!r}")


def contains(name: str, haystack: str, needle: str) -> None:
    if needle not in haystack:
        failures.append(f"{name}\n     missing: {needle!r}\n     in:      {haystack[:200]!r}")


def build(files: dict[str, str]) -> Path:
    repo = Path(tempfile.mkdtemp())
    for rel, text in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return repo


def plan(repo: Path, reserved: set[str] | None = None):
    root, nodes = sync.discover(repo, CFG)
    sync.assign_titles(repo, nodes, reserved or set())
    renderer = sync.Renderer(repo, nodes, CFG)
    renderer.index_anchors()
    for node in nodes.values():
        if node.key:
            node.body = renderer.render(node)
    return root, nodes, renderer


# --------------------------------------------------------------------------- slugs

check("slug keeps doubled separators",
      sync.slugify("Stage 8 — 2026-07-31 sync"), "stage-8--2026-07-31-sync")
check("slug strips punctuation", sync.slugify("Confirmed absent (9)"), "confirmed-absent-9")
check("humanize expands known acronyms", sync.humanize("sql-tools"), "SQL Tools")
check("humanize leaves author capitals", sync.humanize("MongoDB Notes"), "MongoDB Notes")
check("titles drop inline code marks",
      sync.plain_text("Repository Structure — `mongo_products_analisys`"),
      "Repository Structure — mongo_products_analisys")
check("titles drop bold, italic and links",
      sync.plain_text("**Bold** and *soft* [link](x.md) and ~~gone~~"),
      "Bold and soft link and gone")
check("titles keep underscores inside words",
      sync.plain_text("overview_of_3t_products"), "overview_of_3t_products")

# ------------------------------------------------------------------------ structure

repo = build({
    "README.md": "# Home\n\nSee [guide](docs/guide.md).\n",
    "docs/README.md": "# Docs\n",
    "docs/guide.md": "# Guide\n\nBack to [home](../README.md).\n",
    "templates/skeleton.md": "# Skeleton\n",
})
root, nodes, renderer = plan(repo)

check("excluded directory is not published", "templates/skeleton.md" in nodes, False)
check("directory index is not a separate page", "docs/README.md" in nodes, False)
check("directory page takes the index title", nodes["docs"].title, "Docs")
check("root index becomes an ordinary page", nodes["README.md"].title, "Home")
check("page count", sorted(n.key for n in nodes.values() if n.key),
      ["README.md", "docs", "docs/guide.md"])
check("child sits under its directory", nodes["docs/guide.md"].parent.key, "docs")

contains("link to a file becomes a page link", nodes["README.md"].body,
         '<ri:page ri:content-title="Guide"/>')
contains("link to a directory index resolves to the directory page",
         nodes["docs/guide.md"].body, '<ri:page ri:content-title="Home"/>')

# ----------------------------------------------------------------- title collisions

repo = build({
    "a/feature.md": "# Feature Report\n",
    "b/feature.md": "# Feature Report\n",
    "c/feature.md": "# Feature Report\n",
})
root, nodes, _ = plan(repo)
titles = sorted(n.title for n in nodes.values() if not n.is_dir)
check("colliding titles are all qualified to the same depth", titles,
      ["A › Feature Report", "B › Feature Report", "C › Feature Report"])

repo = build({"one.md": "# Taken\n"})
root, nodes, _ = plan(repo, reserved={"Taken"})
check("a title already used elsewhere in the space is avoided",
      nodes["one.md"].title != "Taken", True)

# ------------------------------------------------------------------------- rendering

repo = build({
    "target.md": "# Target\n\n## Prereqs\n\ntext\n",
    "doc.md": (
        "# Doc\n\n"
        "[heading anchor](target.md#prereqs)\n\n"
        "[line anchor](target.md#L103)\n\n"
        "[missing](nope.md)\n\n"
        "[external](https://example.com/a?b=1&c=2)\n\n"
        "[`Task.java:L51`](file:///Users/somebody/other-repo/Task.java#L51)\n\n"
        "```python\nprint('hi')\n```\n\n"
        "| a | b |\n|---|---|\n| 1 | 2 |\n\n"
        "A line\\\nbreak\n"
    ),
})
root, nodes, renderer = plan(repo)
body = nodes["doc.md"].body

contains("heading anchor is preserved", body, 'ac:anchor="Prereqs"')
contains("line anchor falls back to a plain page link", body,
         '<ri:page ri:content-title="Target"/>')
check("line anchor is reported",
      any(i.kind == "line-anchor-dropped" for i in renderer.issues), True)
check("broken link is reported",
      any(i.kind == "link-unresolved" and i.detail == "nope.md" for i in renderer.issues), True)
check("broken link keeps its text but drops the link", "<ac:link" in body.split("missing")[0], True)
check("a file:// link never leaks raw markdown into the page", "](file://" in body, False)
contains("a file:// link keeps its text", body, "<code>Task.java:L51</code>")
check("a file:// link is reported as such",
      any(i.kind == "link-to-local-file" for i in renderer.issues), True)
contains("external link is left alone", body, 'href="https://example.com/a?b=1&amp;c=2"')
contains("code fence becomes a code macro", body, '<ac:structured-macro ac:name="code">')
contains("code language is carried over", body, "<ac:parameter ac:name=\"language\">python</ac:parameter>")
contains("table survives", body, "<table>")
contains("void elements are self-closed for XHTML", body, "<br/>")
check("the H1 is not repeated in the body", "<h1>" in body, False)

check("]]> cannot break out of CDATA",
      sync.code_macro("", "a]]>b"), '<ac:structured-macro ac:name="code">'
      "<ac:plain-text-body><![CDATA[a]]]]><![CDATA[>b]]></ac:plain-text-body></ac:structured-macro>")

# ---------------------------------------------------------------------- change digest

repo = build({"a.md": "# A\n\ntext\n", "b.md": "# B\n"})
root, nodes, _ = plan(repo)
before = sync.digest_of(nodes["a.md"], "")
nodes["a.md"].title = "A renamed"
after = sync.digest_of(nodes["a.md"], "")
check("a retitle changes the digest", before != after, True)

# --------------------------------------------------------------------- source footer

repo = build({"docs/guide.md": "# Guide\n\nbody\n"})
root, nodes, _ = plan(repo)
contains("every page names its source file", nodes["docs/guide.md"].body,
         "docs/guide.md")
contains("the source is linked to the repository", nodes["docs/guide.md"].body,
         "https://example.invalid/repo/blob/main/docs/guide.md")
contains("directory pages name their directory", nodes["docs"].body,
         "https://example.invalid/repo/tree/main/docs")

# ------------------------------------------------- H1 removal survives title cleaning

repo = build({"r.md": "# Structure — `repo`\n\nbody\n"})
root, nodes, _ = plan(repo)
check("markdown is stripped from the title", nodes["r.md"].title, "Structure — repo")
check("the cleaned H1 is still removed from the body", "<h1>" in nodes["r.md"].body, False)

# ------------------------------------------------------------------------------ done

if failures:
    print(f"{len(failures)} failing check(s):\n")
    for f in failures:
        print("  ✗ " + f)
    sys.exit(1)
print("all checks passed")
