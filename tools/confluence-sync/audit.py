# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27", "markdown-it-py>=3.0"]
# ///
"""Audit what Confluence actually *renders*, not what the sync believes it published.

    uv run tools/confluence-sync/audit.py            # 25 random pages
    uv run tools/confluence-sync/audit.py --all      # every page (slower)
    uv run tools/confluence-sync/audit.py --sample 60

`sync.sh verify` compares stored digests: cheap, and enough to prove the tree is
complete and current. It cannot tell you whether a page *reads* correctly, because a
page can be stored exactly as intended and still render a broken link or a wall of raw
Markdown. This fetches the rendered HTML and looks at it.

Checks per page:
  * no broken-link placeholders (how Confluence renders a link whose target is missing)
  * every internal link resolves to a page inside the synced tree
  * no raw Markdown left in the visible text - outside code blocks, where it belongs
  * block constructs really became blocks: tables as tables, fences as code macros
  * no links beyond the ones the source document itself contains

Structure is checked separately and exhaustively: every source file has exactly one
page, under the right parent.
"""

from __future__ import annotations

import argparse
import html
import os
import random
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync  # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

BROKEN_LINK = re.compile(r"transform-error|placeholder/error")
PAGE_HREF = re.compile(r'href="(/wiki/spaces/[^"]*/pages/(\d+)[^"]*)"')
ANY_LINK = re.compile(r'<a\b[^>]*href="([^"]+)"')
CODEISH = re.compile(r"<(pre|code|ac:plain-text-body)\b.*?</\1>", re.S)
TAG = re.compile(r"<[^>]+>")

# Markdown that should never survive into rendered prose.
#
# Every tag becomes a newline in `visible_text`, so a table cell holding "#" or "*"
# looks like the start of a line. The patterns therefore demand a *horizontal* space
# between the marker and its text — a real heading is "## Title" on one line, whereas
# a "#" column header is followed by a line break.
LEAKS = [
    ("markdown link", re.compile(r"\[[^\]\n]{1,80}\]\((?!\s)[^)\n]{1,200}\)")),
    ("markdown heading", re.compile(r"(?m)^[ \t]{0,3}#{1,6}[ \t]+\S")),
    ("code fence", re.compile(r"```")),
    ("table rule", re.compile(r"(?m)^[ \t]*\|?[ \t]*:?-{3,}:?[ \t]*\|")),
    ("list bullet", re.compile(r"(?m)^[ \t]{0,3}[-*][ \t]{1,3}\S")),
]


SOURCE_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def publishable_links(path: Path) -> int:
    """How many of a document's links the sync is *able* to publish.

    A page with no rendered links is only suspicious if its source had links worth
    rendering. Links to http(s)/mailto survive as-is, and links to another published
    document become page links - but a file:// path to somebody's hard disk, or a link
    to a file that does not exist, is deliberately dropped, so a page built only from
    those is correctly link-free.
    """
    n = 0
    for href in SOURCE_LINK.findall(path.read_text(errors="replace")):
        if href.startswith(("http://", "https://", "mailto:")):
            n += 1
        elif ":" not in href.split("/")[0]:
            target = (path.parent / unquote(href).partition("#")[0]).resolve()
            if target.exists() and (target.is_dir() or target.suffix == ".md"):
                n += 1
    return n


def visible_text(view_html: str) -> str:
    """Rendered text with code blocks removed - Markdown inside code is not a leak."""
    without_code = CODEISH.sub(" ", view_html)
    return html.unescape(TAG.sub("\n", without_code))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=25)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    cfg = tomllib.loads((HERE / "confluence-sync.toml").read_text())
    api = sync.Confluence(os.environ["CONFLUENCE_BASE_URL"],
                          os.environ["CONFLUENCE_USER_EMAIL"],
                          os.environ["CONFLUENCE_API_TOKEN"])

    print("reading the published tree …")
    remote = sync.read_remote(api, cfg["root_page_id"])
    root, nodes = sync.discover(REPO, cfg)
    sync.assign_titles(REPO, nodes, set(),
                       root_title=remote[cfg["root_page_id"]].title)
    expected = {n.source_path: n for n in nodes.values() if n.key}

    failures: list[str] = []
    warnings: list[str] = []

    # ---------------------------------------------------------------- structure
    by_source = {r.source_path: r for r in remote.values() if r.source_path}
    ids = {r.id for r in remote.values()}
    print(f"\nstructure: {len(expected)} expected, {len(remote)} published")
    for source in sorted(set(expected) - set(by_source)):
        failures.append(f"no page for {source}")
    for source in sorted(set(by_source) - set(expected)):
        failures.append(f"page for {source}, which is not in the repository")
    for r in remote.values():
        if not r.source_path:
            failures.append(f"page not managed by the sync: {r.title!r}")

    for source, node in expected.items():
        page = by_source.get(source)
        if not page:
            continue
        want = (None if node.parent is None
                else (by_source.get(node.parent.source_path).id
                      if by_source.get(node.parent.source_path) else None))
        if want and page.parent_id != want:
            failures.append(f"wrong parent for {source}")

    files_on_disk = {p.relative_to(REPO).as_posix() for p in REPO.rglob("*.md")
                     if not any(part in {".git", ".idea", ".github", "templates", "tools"}
                                for part in p.relative_to(REPO).parts)}
    published_files = {n.source.as_posix() for n in nodes.values() if n.source}
    for missed in sorted(files_on_disk - published_files):
        failures.append(f"markdown file not published at all: {missed}")
    print(f"  markdown files on disk: {len(files_on_disk)}, all published: "
          f"{not (files_on_disk - published_files)}")

    # ------------------------------------------------------------- rendering
    page_ids = sorted(by_source.items())
    if not args.all:
        random.seed(args.seed)
        page_ids = random.sample(page_ids, min(args.sample, len(page_ids)))
    print(f"\nrendering: fetching {len(page_ids)} page(s) as Confluence renders them")

    totals = {"links": 0, "tables": 0, "code": 0, "headings": 0}
    for source, page in page_ids:
        data = api.request("GET", f"/api/v2/pages/{page.id}?body-format=view")
        view = data["body"]["view"]["value"]
        title = data["title"]

        if BROKEN_LINK.search(view):
            failures.append(f"broken-link placeholder rendered in {title!r} ({source})")

        internal = PAGE_HREF.findall(view)
        totals["links"] += len(internal)
        for href, target_id in internal:
            if target_id not in ids:
                failures.append(f"{title!r} links to page {target_id}, "
                                "which is outside the synced tree")
        # Only file-backed pages have a source to compare against; a directory page's
        # source path is a directory, and one without a README is legitimately empty.
        if not source.endswith("/") and not ANY_LINK.search(view):
            if publishable_links(REPO / source):
                failures.append(f"{title!r} has links in its source but none rendered")

        totals["tables"] += view.count("<table")
        totals["code"] += len(re.findall(r'class="[^"]*code', view)) + view.count("<pre")
        totals["headings"] += len(re.findall(r"<h[1-6]\b", view))

        text = visible_text(view)
        for label, pattern in LEAKS:
            m = pattern.search(text)
            if m:
                # A warning, not a failure: these patterns also fire on Markdown the
                # source itself renders oddly (an unescaped "*" inside bold, say),
                # which Confluence reproduces faithfully. Worth a human look, not a
                # reason to fail a release.
                warnings.append(f"raw {label} visible in {title!r} ({source}): "
                                f"{m.group(0)[:60]!r}")

    print(f"  rendered: {totals['links']} internal links, {totals['headings']} headings, "
          f"{totals['tables']} tables, {totals['code']} code blocks")

    # ------------------------------------------------------------------ result
    print()
    if warnings:
        print(f"{len(warnings)} warning(s) — check by eye, usually a quirk of the source document:")
        for w in warnings[:20]:
            print("  ! " + w)
        print()
    if failures:
        print(f"AUDIT FAILED — {len(failures)} problem(s):")
        for f in failures[:40]:
            print("  ✗ " + f)
        if len(failures) > 40:
            print(f"  … and {len(failures) - 40} more")
        return 1
    print("AUDIT PASSED — structure complete, links resolve, pages render as prose")
    return 0


if __name__ == "__main__":
    sys.exit(main())
