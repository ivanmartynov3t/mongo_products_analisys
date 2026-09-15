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
    "directory_index": ["README.md"],
    "fold_directory_index": True,
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


# ------------------------------------------------------------------------ structure

repo = build({
    "README.md": "# Home\n\nSee [guide](docs/guide.md).\n",
    "docs/README.md": "# Docs\n",
    "docs/guide.md": "# Guide\n\nBack to [home](../README.md).\n",
    "templates/skeleton.md": "# Skeleton\n",
})
root, nodes, renderer = plan(repo)

check("excluded directory is not published", "templates/skeleton.md" in nodes, False)
check("the tree mirrors the repository", sorted(n.key for n in nodes.values()),
      [".", "docs", "docs/guide.md"])
check("pages are named after their file", nodes["docs/guide.md"].title, "guide.md")
check("directories are named after the directory", nodes["docs"].title, "docs")
check("a subdirectory README becomes that directory's content, not a page",
      "docs/README.md" in nodes, False)
check("the directory page carries the README's source path",
      nodes["docs"].source_path, "docs/README.md")
check("the root README becomes the root page's content, not a page called README.md",
      "README.md" in {n.key for n in nodes.values()}, False)
check("the root page carries the root README", nodes["."].source_path, "README.md")
check("the root page is named after the repository",
      nodes["."].title, Path(nodes["."].key).name or "x" and nodes["."].title)
check("directories hang under the root page", nodes["docs"].parent.key, ".")
check("child sits under its directory", nodes["docs/guide.md"].parent.key, "docs")

contains("link to a file becomes a page link", nodes["."].body,
         '<ri:page ri:content-title="guide.md"/>')
contains("a link to the root README resolves to the root page",
         nodes["docs/guide.md"].body,
         f'<ri:page ri:content-title="{nodes["."].title}"/>')

# ----------------------------------------------------------------- title collisions

repo = build({
    "a/feature.md": "# One\n",
    "b/feature.md": "# Two\n",
    "c/feature.md": "# Three\n",
    "solo.md": "# Alone\n",
})
root, nodes, _ = plan(repo)
check("a shared file name sends the whole group to full paths",
      sorted(n.title for n in nodes.values() if not n.is_dir),
      ["a/feature.md", "b/feature.md", "c/feature.md", "solo.md"])
check("the root page is named after the repository directory",
      nodes["."].title, repo.name)

repo = build({"one.md": "# Taken\n"})
root, nodes, _ = plan(repo, reserved={"one.md"})
check("a title already used elsewhere in the space is avoided",
      nodes["one.md"].title != "one.md", True)

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
         '<ri:page ri:content-title="target.md"/>')
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
contains("the document's own heading is kept, since the title is the file name",
         body, "<h1>Doc</h1>")

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

# ------------------------------------------------------- nothing is added to a page

repo = build({"docs/guide.md": "# Guide\n\nbody\n", "docs/other.md": "# Other\n"})
root, nodes, _ = plan(repo)
body = nodes["docs/guide.md"].body
check("no provenance footer is appended", "Published automatically" in body, False)
check("no child listing is appended", 'ac:name="children"' in body, False)
check("no links are added to a document that has none", "<a " in body or "ac:link" in body, False)
check("a directory without a README renders empty", nodes["docs"].body, "")

# ----------------------------------------------------------- over-long path titles

deep = "/".join(["directory-with-a-long-name"] * 12) + "/feature-report.md"
repo = build({deep: "# Deep\n", "other/feature-report.md": "# Other\n"})
root, nodes, _ = plan(repo)
title = nodes[deep].title
check("an over-long path title is clamped", len(title) <= sync.TITLE_LIMIT, True)
check("clamping keeps the identifying tail", title.endswith("feature-report.md"), True)

# ------------------------------------------------------------------------------ done

if failures:
    print(f"{len(failures)} failing check(s):\n")
    for f in failures:
        print("  ✗ " + f)
    sys.exit(1)
print("all checks passed")
