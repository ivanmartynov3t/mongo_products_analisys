# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx>=0.27", "markdown-it-py>=3.0"]
# ///
"""Publish this repository's documentation to Confluence, keeping the tree identical.

Run it through sync.sh, which loads .env and hands off to uv.

Three phases, each usable on its own:

  plan    walk the repo, resolve titles and links, print what would change (writes nothing)
  apply   plan, then create/update/move/trash pages so Confluence matches the repo
  verify  read the tree back from Confluence and prove it matches the repo

Design notes that are not obvious, all established by probing the live instance
(see PROBE-FINDINGS.md):

  * Page links must use ri:content-title. ri:content-id renders a broken-link
    placeholder. Titles are therefore the link key: unique space-wide, and a retitle
    forces every page that links to it to be re-rendered.
  * Because of that, the change hash covers the *rendered* body plus title and parent,
    not the source markdown. A file whose own text is unchanged still needs a rewrite
    when a page it links to gets retitled.
  * The API intermittently answers 403/404 under burst and recovers by itself. Both are
    retried. A read that never succeeds aborts the run rather than being taken as
    "this page does not exist" - otherwise the sync would duplicate or trash live pages.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import tomllib
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

import httpx
from markdown_it import MarkdownIt

PROPERTY_KEY = "repo-sync"
LABEL = "repo-sync"
TOOL_VERSION = "1.0"
BREADCRUMB = " › "  # "Parent › Child", used to disambiguate colliding titles

# Words that look wrong when naively title-cased.
ACRONYMS = {
    "ai": "AI", "sql": "SQL", "mcp": "MCP", "ui": "UI", "api": "API", "cli": "CLI",
    "3t": "3T", "3tl": "3TL", "eaf": "EAF", "gui": "GUI", "poc": "POC", "voc": "VoC",
    "mongodb": "MongoDB", "dbeaver": "DBeaver", "nosqlbooster": "NoSQLBooster",
    "tableplus": "TablePlus", "datagrip": "DataGrip", "json": "JSON", "erd": "ERD",
}


# --------------------------------------------------------------------------- model


@dataclass(eq=False)
class Node:  # not frozen, but identity-hashed so nodes can key dicts
    """One page-to-be: either a directory (container) or a markdown file."""

    key: str                      # repo-relative path, posix, "" for the root folder
    is_dir: bool
    source: Path | None = None    # the markdown file supplying the body
    parent: "Node | None" = None
    children: list["Node"] = field(default_factory=list)
    title: str = ""
    body: str = ""                # rendered storage format
    digest: str = ""

    @property
    def source_path(self) -> str:
        """What gets recorded on the page, and what identifies it across runs."""
        return self.source.as_posix() if self.source else self.key + "/"


@dataclass
class Issue:
    kind: str
    source: str
    detail: str


# ----------------------------------------------------------------------- discovery


def humanize(name: str) -> str:
    words = re.split(r"[-_\s]+", name.strip())
    out = []
    for w in words:
        if not w:
            continue
        low = w.lower()
        if low in ACRONYMS:
            out.append(ACRONYMS[low])
        elif w[:1].isupper():
            out.append(w)  # already capitalised by the author, leave it alone
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def first_heading(text: str) -> str | None:
    m = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    return plain_text(m.group(1)) if m else None


def plain_text(heading: str) -> str:
    """Strip inline Markdown, since a Confluence title is plain text.

    Without this, '# Repository Structure — `mongo_products_analisys`' becomes a page
    titled with literal backticks.
    """
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)   # [text](url) -> text
    s = re.sub(r"`+([^`]*)`+", r"\1", s)                   # `code` -> code
    s = re.sub(r"(\*\*|__)(.+?)\1", r"\2", s)              # bold
    s = re.sub(r"(?<!\w)([*_])(.+?)\1(?!\w)", r"\2", s)    # italic
    s = re.sub(r"~~(.+?)~~", r"\1", s)                     # strikethrough
    return s.strip()


def slugify(heading: str) -> str:
    """GitHub-style heading anchor, so in-repo '#some-heading' links can be resolved.

    Each space becomes one hyphen - runs are *not* collapsed, which is why
    'Stage 8 - 2026-07-31' slugs to 'stage-8--2026-07-31' once the dash is stripped.
    """
    s = unicodedata.normalize("NFKD", heading).lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s", "-", s.strip())


def discover(repo: Path, cfg: dict) -> tuple[Node, dict[str, Node]]:
    excludes = cfg["exclude"]
    index_names = cfg["directory_index"]

    def excluded(rel: Path) -> bool:
        return any(rel.match(pat) or rel.as_posix().startswith(pat.rstrip("*").rstrip("/") + "/")
                   for pat in excludes)

    files = sorted(
        p for p in repo.rglob("*.md")
        if not excluded(p.relative_to(repo))
    )

    root = Node(key="", is_dir=True, title="<root folder>")
    nodes: dict[str, Node] = {"": root}

    def container(rel_dir: str) -> Node:
        if rel_dir in nodes:
            return nodes[rel_dir]
        parent_key = rel_dir.rpartition("/")[0] if "/" in rel_dir else ""
        parent = container(parent_key)
        node = Node(key=rel_dir, is_dir=True, parent=parent)
        parent.children.append(node)
        nodes[rel_dir] = node
        return node

    # A directory's index file becomes that directory's page body rather than a page
    # of its own, so 'docs/README.md' does not sit as a child of 'docs'.
    index_for: dict[str, Path] = {}
    for f in files:
        rel = f.relative_to(repo)
        d = rel.parent.as_posix()
        d = "" if d == "." else d
        if rel.name in index_names and d not in index_for:
            index_for[d] = rel
        elif rel.name in index_names:
            current = index_for[d]
            if index_names.index(rel.name) < index_names.index(current.name):
                index_for[d] = rel

    for dir_key, rel in index_for.items():
        node = container(dir_key) if dir_key else root
        node.source = rel

    for f in files:
        rel = f.relative_to(repo)
        d = rel.parent.as_posix()
        d = "" if d == "." else d
        if index_for.get(d) == rel:
            continue  # already the body of its directory
        parent = container(d) if d else root
        node = Node(key=rel.as_posix(), is_dir=False, source=rel, parent=parent)
        parent.children.append(node)
        nodes[node.key] = node

    # The repo root's own index (README.md) has nowhere to live: the sync root is a
    # Confluence folder, and folders hold no body. It becomes an ordinary page.
    if root.source is not None:
        rel = root.source
        node = Node(key=rel.as_posix(), is_dir=False, source=rel, parent=root)
        root.children.append(node)
        nodes[node.key] = node
        root.source = None

    for n in nodes.values():
        n.children.sort(key=lambda c: (not c.is_dir, c.key))
    return root, nodes


def assign_titles(repo: Path, nodes: dict[str, Node], reserved: set[str]) -> list[Issue]:
    """Give every node a space-unique title.

    Preferred title is the document's own H1 (or a humanized directory name). On
    collision the parent path is prepended one segment at a time, which is stable as
    long as the file stays where it is - and a move rewrites the links anyway.
    """
    issues: list[Issue] = []
    taken = set(reserved)
    ordered = sorted((n for n in nodes.values() if n.key != ""), key=lambda n: n.key)

    bases: dict[Node, str] = {}
    for node in ordered:
        if node.source is not None:
            text = (repo / node.source).read_text(encoding="utf-8", errors="replace")
            base = first_heading(text) or humanize(node.source.stem)
        else:
            base = humanize(Path(node.key).name)
        bases[node] = re.sub(r"\s+", " ", base).strip()[:240]

    # Every node sharing a base name is disambiguated to the *same* depth, so the ten
    # "Governance" folders all read "<Product> › Features › Governance" rather than one
    # of them keeping the bare name because it happened to be walked first.
    groups: dict[str, list[Node]] = {}
    for node, base in bases.items():
        groups.setdefault(base, []).append(node)

    for base, group in groups.items():
        depth = 0
        if len(group) > 1 or base in taken:
            limit = max(len(list(iter_ancestors(n))) for n in group)
            while depth < limit:
                depth += 1
                labels = {qualified(n, base, depth) for n in group}
                if len(labels) == len(group) and not (labels & taken):
                    break
        for node in sorted(group, key=lambda n: n.key):
            candidate = qualified(node, base, depth)
            n = 2
            while candidate in taken:
                candidate = f"{qualified(node, base, depth)} ({n})"
                n += 1
            if candidate != base:
                issues.append(Issue("title-disambiguated", node.source_path, candidate))
            node.title = candidate
            taken.add(candidate)
    return issues


def qualified(node: Node, base: str, depth: int) -> str:
    """`base` prefixed with the `depth` nearest ancestor directory names."""
    if depth == 0:
        return base
    ancestors = [a for a in iter_ancestors(node)][::-1]
    prefix = BREADCRUMB.join(humanize(Path(a.key).name) for a in ancestors[-depth:])
    return f"{prefix}{BREADCRUMB}{base}" if prefix else base


def iter_ancestors(node: Node):
    p = node.parent
    while p is not None and p.key != "":
        yield p
        p = p.parent


# ------------------------------------------------------------------------ rendering


def build_renderer() -> MarkdownIt:
    md = MarkdownIt("commonmark").enable(["table", "strikethrough"])
    # markdown-it refuses to parse file:, data: and javascript: URLs, which leaves the
    # raw "[text](file:///…)" in the output. We want those links *parsed* so the link
    # classifier can drop them deliberately and report them; nothing unsafe reaches the
    # page, because only http(s)/mailto/ftp are ever emitted as an href.
    md.validateLink = lambda url: True
    return md


def cdata(text: str) -> str:
    # "]]>" cannot appear inside a CDATA section; split it across two sections.
    return "<![CDATA[" + text.replace("]]>", "]]]]><![CDATA[>") + "]]>"


def code_macro(language: str, content: str) -> str:
    lang = (language or "").strip().lower()
    param = f'<ac:parameter ac:name="language">{lang}</ac:parameter>' if lang else ""
    return ('<ac:structured-macro ac:name="code">' + param
            + "<ac:plain-text-body>" + cdata(content) + "</ac:plain-text-body>"
            + "</ac:structured-macro>")


class Renderer:
    """Markdown -> Confluence storage format, with repo links turned into page links."""

    def __init__(self, repo: Path, nodes: dict[str, Node], cfg: dict | None = None):
        self.repo = repo
        self.nodes = nodes
        self.cfg = cfg or {}
        self.md = build_renderer()
        self.anchors: dict[str, dict[str, str]] = {}  # source path -> slug -> heading text
        self.issues: list[Issue] = []
        self._install_rules()

    def index_anchors(self) -> None:
        for node in self.nodes.values():
            if node.source is None:
                continue
            text = (self.repo / node.source).read_text(encoding="utf-8", errors="replace")
            table = {}
            for m in re.finditer(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
                heading = m.group(1).strip()
                table.setdefault(slugify(heading), heading)
            self.anchors[node.source.as_posix()] = table

    # -- link resolution ---------------------------------------------------

    def _node_for(self, target: Path) -> Node | None:
        rel = target.as_posix()
        if rel in self.nodes:
            return self.nodes[rel]
        # A link to a directory, or to a directory's index file, means that
        # directory's container page.
        for key, node in self.nodes.items():
            if node.source is not None and node.source.as_posix() == rel:
                return node
        return None

    def _resolve(self, href: str, node: Node) -> tuple[str, str] | None:
        """(title, anchor) for an internal link, or None when it cannot be published."""
        path_part, _, frag = unquote(href).partition("#")
        if not path_part:
            return (node.title, self._anchor(node, frag)) if frag else (node.title, "")

        base = (self.repo / node.source).parent if node.source else self.repo / node.key
        try:
            target = (base / path_part).resolve().relative_to(self.repo.resolve())
        except ValueError:
            return None
        target_node = self._node_for(target)
        if target_node is None:
            return None
        return target_node.title, self._anchor(target_node, frag)

    def _anchor(self, target: Node, frag: str) -> str:
        if not frag:
            return ""
        if re.fullmatch(r"L\d+(-L\d+)?", frag):
            # A GitHub line anchor. Confluence has no equivalent; link to the page.
            self.issues.append(Issue("line-anchor-dropped", target.source_path, f"#{frag}"))
            return ""
        table = self.anchors.get(target.source.as_posix() if target.source else "", {})
        heading = table.get(frag.lower())
        if heading is None:
            self.issues.append(Issue("anchor-unresolved", target.source_path, f"#{frag}"))
            return ""
        return heading

    # -- markdown-it rules -------------------------------------------------

    def _install_rules(self) -> None:
        rules = self.md.renderer.rules

        def link_open(tokens, idx, options, env):
            href = tokens[idx].attrGet("href") or ""
            node: Node = env["node"]
            if href.startswith(("http://", "https://", "mailto:", "ftp://")):
                env["stack"].append("</a>")
                safe = href.replace("&", "&amp;").replace('"', "&quot;")
                return f'<a href="{safe}">'
            resolved = None if ":" in href.split("/")[0] else self._resolve(href, node)
            if resolved is None:
                kind = ("link-to-local-file" if href.startswith("file:")
                        else "link-unresolved")
                self.issues.append(Issue(kind, node.source_path, href))
                env["stack"].append("")  # keep the text, drop the link
                return ""
            title, anchor = resolved
            attr = f' ac:anchor="{escape_attr(anchor)}"' if anchor else ""
            if title == node.title and anchor:
                env["stack"].append("</ac:link-body></ac:link>")
                return f"<ac:link{attr}><ac:link-body>"
            env["stack"].append("</ac:link-body></ac:link>")
            return (f"<ac:link{attr}>"
                    f'<ri:page ri:content-title="{escape_attr(title)}"/>'
                    f"<ac:link-body>")

        def link_close(tokens, idx, options, env):
            return env["stack"].pop() if env["stack"] else ""

        def fence(tokens, idx, options, env):
            return code_macro(tokens[idx].info, tokens[idx].content)

        rules["link_open"] = link_open
        rules["link_close"] = link_close
        rules["fence"] = fence
        rules["code_block"] = fence

    # -- entry point -------------------------------------------------------

    def render(self, node: Node) -> str:
        if node.source is None:
            body = ('<p>This page mirrors a folder of the repository. Its contents:</p>'
                    '<ac:structured-macro ac:name="children">'
                    '<ac:parameter ac:name="all">true</ac:parameter>'
                    "</ac:structured-macro>")
            return body + self.footer(node)
        text = (self.repo / node.source).read_text(encoding="utf-8", errors="replace")
        text = strip_title_heading(text, node.title)
        html = self.md.render(text, {"node": node, "stack": []})
        children = ('<p><ac:structured-macro ac:name="children">'
                    '<ac:parameter ac:name="all">true</ac:parameter>'
                    "</ac:structured-macro></p>" if node.children else "")
        return to_xhtml(html) + children + self.footer(node)

    def footer(self, node: Node) -> str:
        """Name the file this page was generated from.

        Page titles come from each document's own heading, so a reader cannot otherwise
        tell which repository file they are looking at - and two documents may share a
        heading. This line makes every page traceable, and searchable by path.
        """
        path = node.source_path
        url = self.cfg.get("repo_url", "")
        if url:
            branch = self.cfg.get("repo_branch", "main")
            kind = "tree" if node.source is None else "blob"
            href = f"{url.rstrip('/')}/{kind}/{branch}/{path.rstrip('/')}"
            where = f'<a href="{escape_attr(href)}">{escape_attr(path)}</a>'
        else:
            where = f"<code>{escape_attr(path)}</code>"
        return ("<hr/><p><em>Source: " + where
                + ". Published automatically from the repository - "
                  "edits made here are overwritten on the next sync.</em></p>")


def strip_title_heading(text: str, title: str) -> str:
    """Drop the leading H1 when Confluence already shows it as the page title."""
    m = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    if m and plain_text(m.group(1)) == title:
        return text[: m.start()] + text[m.end():]
    return text


def escape_attr(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


VOID_TAG = re.compile(r"<(br|hr|img|col)([^>]*?)\s*/?>", re.I)


def to_xhtml(html: str) -> str:
    """Storage format is XHTML: void elements must be self-closed."""
    return VOID_TAG.sub(lambda m: f"<{m.group(1)}{m.group(2)}/>", html)


# -------------------------------------------------------------------------- client


class Confluence:
    RETRYABLE = {403, 404, 429, 500, 502, 503, 504}

    def __init__(self, base: str, email: str, token: str, verbose: bool = False):
        self.http = httpx.Client(base_url=base, auth=(email, token), timeout=60)
        self.verbose = verbose
        self.calls = 0

    def request(self, method: str, path: str, body=None, tries: int = 6):
        """Retry 403/404 as well as the usual suspects - see the module docstring."""
        last = ""
        for attempt in range(tries):
            self.calls += 1
            try:
                r = self.http.request(method, path, json=body)
            except httpx.HTTPError as exc:
                last = str(exc)
                time.sleep(1.5 * (attempt + 1))
                continue
            if r.status_code < 400:
                return r.json() if r.content else None
            last = f"{r.status_code} {r.text[:300]}"
            if r.status_code in self.RETRYABLE and attempt < tries - 1:
                delay = float(r.headers.get("Retry-After", 0)) or 1.5 * (attempt + 1)
                if self.verbose:
                    print(f"    retry {method} {path}: {last[:80]}", file=sys.stderr)
                time.sleep(delay)
                continue
            break
        raise RuntimeError(f"{method} {path} failed after {tries} attempts: {last}")

    def paged(self, path: str):
        while path:
            data = self.request("GET", path)
            yield from data.get("results", [])
            nxt = data.get("_links", {}).get("next", "")
            path = nxt.replace("/wiki", "", 1) if nxt else ""


# ---------------------------------------------------------------------- remote side


@dataclass
class RemotePage:
    id: str
    title: str
    parent_id: str
    source_path: str | None
    digest: str | None
    property_id: str | None
    version: int = 0


MAX_DEPTH = 10  # the API's ceiling for one descendants call


def walk_descendants(api: Confluence, kind: str, content_id: str):
    """Every page below `content_id`, however deep.

    `depth` on the descendants endpoints defaults to 2 and is capped at 10, so a
    single call silently truncates a deep tree. Anything sitting at the cut-off is
    re-queried as its own root.
    """
    seen: set[str] = set()
    frontier = [(kind, content_id)]
    while frontier:
        parent_kind, parent_id = frontier.pop()
        deepest = []
        for item in api.paged(
            f"/api/v2/{parent_kind}/{parent_id}/descendants?limit=250&depth={MAX_DEPTH}"
        ):
            if item["id"] in seen:
                continue
            seen.add(item["id"])
            yield item
            if item.get("depth") == MAX_DEPTH and item.get("type") == "page":
                deepest.append(("pages", item["id"]))
        frontier.extend(deepest)


def read_remote(api: Confluence, folder_id: str) -> dict[str, RemotePage]:
    pages: dict[str, RemotePage] = {}
    for item in walk_descendants(api, "folders", folder_id):
        if item.get("type") != "page":
            continue
        pid = item["id"]
        prop = None
        for p in api.paged(f"/api/v2/pages/{pid}/properties?limit=50"):
            if p["key"] == PROPERTY_KEY:
                prop = p
                break
        value = (prop or {}).get("value") or {}
        pages[pid] = RemotePage(
            id=pid,
            title=item["title"],
            parent_id=str(item.get("parentId") or ""),
            source_path=value.get("source_path"),
            digest=value.get("digest"),
            property_id=(prop or {}).get("id"),
        )
    return pages


# ------------------------------------------------------------------------- planning


def digest_of(node: Node, parent_title: str) -> str:
    h = hashlib.sha256()
    h.update(node.title.encode())
    h.update(b"\x00")
    h.update(parent_title.encode())
    h.update(b"\x00")
    h.update(node.body.encode())
    return h.hexdigest()


def plan(repo: Path, cfg: dict, api: Confluence | None, reserved: set[str]):
    root, nodes = discover(repo, cfg)
    issues = assign_titles(repo, nodes, reserved)

    renderer = Renderer(repo, nodes, cfg)
    renderer.index_anchors()
    for node in nodes.values():
        if node.key == "":
            continue
        node.body = renderer.render(node)
    for node in nodes.values():
        if node.key != "":
            node.digest = digest_of(node, node.parent.title if node.parent else "")
    issues.extend(renderer.issues)
    return root, nodes, issues


def bfs(root: Node):
    queue = list(root.children)
    while queue:
        node = queue.pop(0)
        yield node
        queue.extend(node.children)


# -------------------------------------------------------------------------- applying


def apply_tree(api: Confluence, cfg: dict, root: Node, nodes: dict[str, Node],
               remote: dict[str, RemotePage], delete: bool, verbose: bool):
    by_source = {r.source_path: r for r in remote.values() if r.source_path}
    # A run interrupted between creating a page and stamping its property leaves a page
    # with no source path. Adopting it by title repairs that on the next run; creating a
    # second page instead would fail anyway, since Confluence forbids duplicate titles.
    by_title = {r.title: r for r in remote.values() if not r.source_path}
    stats = {"created": 0, "updated": 0, "unchanged": 0, "moved": 0,
             "adopted": 0, "trashed": 0}
    page_ids: dict[str, str] = {}

    for node in bfs(root):  # parents before children
        parent_id = (cfg["root_folder_id"] if node.parent is None or node.parent.key == ""
                     else page_ids[node.parent.key])
        existing = by_source.get(node.source_path)
        if existing is None and node.title in by_title:
            existing = by_title.pop(node.title)
            stats["adopted"] += 1

        if existing is None:
            created = api.request("POST", "/api/v2/pages", {
                "spaceId": cfg["space_id"], "status": "current", "title": node.title,
                "parentId": parent_id,
                "body": {"representation": "storage", "value": node.body},
            })
            page_ids[node.key] = created["id"]
            write_state(api, created["id"], node, is_new=True)
            stats["created"] += 1
            if verbose:
                print(f"  + {node.title}")
            continue

        page_ids[node.key] = existing.id
        moved = existing.parent_id != parent_id
        # A missing digest means the page was never fully stamped, so it cannot be
        # trusted as up to date however its content looks.
        if existing.digest is not None and existing.digest == node.digest and not moved:
            stats["unchanged"] += 1
            continue

        current = api.request("GET", f"/api/v2/pages/{existing.id}")
        api.request("PUT", f"/api/v2/pages/{existing.id}", {
            "id": existing.id, "status": "current", "title": node.title,
            "parentId": parent_id,
            "body": {"representation": "storage", "value": node.body},
            "version": {"number": current["version"]["number"] + 1,
                        "message": f"repo-sync {node.source_path}"},
        })
        write_state(api, existing.id, node)
        stats["moved" if moved else "updated"] += 1
        if verbose:
            print(f"  ~ {node.title}")

    wanted = {n.source_path for n in nodes.values() if n.key != ""}
    orphans = [r for r in remote.values() if r.source_path and r.source_path not in wanted]
    for orphan in orphans:
        if not delete:
            print(f"  ! orphan (kept, pass --delete to trash): {orphan.title}")
            continue
        api.request("DELETE", f"/api/v2/pages/{orphan.id}")
        stats["trashed"] += 1
        print(f"  - trashed {orphan.title}")
    return stats, page_ids, orphans


def write_state(api: Confluence, page_id: str, node: Node, is_new: bool = False) -> None:
    """Stamp the page so later runs can recognise, update and orphan-check it."""
    value = {"source_path": node.source_path, "digest": node.digest,
             "tool_version": TOOL_VERSION}
    existing = None
    if not is_new:
        for p in api.paged(f"/api/v2/pages/{page_id}/properties?limit=50"):
            if p["key"] == PROPERTY_KEY:
                existing = p
                break
    if existing is None:
        api.request("POST", f"/api/v2/pages/{page_id}/properties",
                    {"key": PROPERTY_KEY, "value": value})
    else:
        api.request("PUT", f"/api/v2/pages/{page_id}/properties/{existing['id']}",
                    {"key": PROPERTY_KEY, "value": value,
                     "version": {"number": existing["version"]["number"] + 1}})
    api.request("POST", f"/rest/api/content/{page_id}/label",
                [{"prefix": "global", "name": LABEL}])


# --------------------------------------------------------------------- verification


def verify(api: Confluence, cfg: dict, root: Node, nodes: dict[str, Node]) -> list[str]:
    failures: list[str] = []
    remote = read_remote(api, cfg["root_folder_id"])
    by_source = {r.source_path: r for r in remote.values() if r.source_path}
    expected = {n.source_path: n for n in nodes.values() if n.key != ""}

    missing = sorted(set(expected) - set(by_source))
    failures += [f"missing page for {m}" for m in missing]
    extra = sorted(set(by_source) - set(expected))
    failures += [f"unexpected managed page for {e} (orphan)" for e in extra]

    unmanaged = [r for r in remote.values() if not r.source_path]
    if unmanaged:
        failures.append(f"{len(unmanaged)} page(s) under the root are not managed by the sync: "
                        + ", ".join(sorted(r.title for r in unmanaged)[:5]))

    titles = {}
    for source, node in expected.items():
        remote_page = by_source.get(source)
        if remote_page is None:
            continue
        titles[node.title] = source
        if remote_page.title != node.title:
            failures.append(f"title differs for {source}: {remote_page.title!r} != {node.title!r}")
        if remote_page.digest != node.digest:
            failures.append(f"stale content for {source}")
        if node.parent is None or node.parent.key == "":
            parent_id = cfg["root_folder_id"]
        else:
            parent = by_source.get(node.parent.source_path)
            # The parent page's own absence is reported by the `missing` check above;
            # say so here too rather than quietly passing the assertion.
            parent_id = parent.id if parent else None
            if parent is None:
                failures.append(f"cannot check parent of {source}: "
                                f"{node.parent.source_path} has no page")
        if parent_id and remote_page.parent_id != parent_id:
            failures.append(f"wrong parent for {source}")

    # Every page link we published must point at a title that exists in the space,
    # otherwise Confluence will render a broken-link placeholder.
    link_re = re.compile(r'<ri:page ri:content-title="([^"]+)"/>')
    for node in expected.values():
        for m in link_re.finditer(node.body):
            target = (m.group(1).replace("&amp;", "&").replace("&lt;", "<")
                      .replace("&gt;", ">").replace("&quot;", '"'))
            if target not in titles:
                failures.append(f"{node.source_path} links to unknown title {target!r}")
    return failures


# -------------------------------------------------------------------------- reporting


def write_report(path: Path, root: Node, nodes: dict[str, Node], issues: list[Issue],
                 stats: dict | None, failures: list[str] | None) -> None:
    lines = [f"# confluence-sync report", "",
             f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')}", "",
             f"- pages planned: **{len(nodes) - 1}** "
             f"({sum(1 for n in nodes.values() if n.is_dir and n.key)} folders, "
             f"{sum(1 for n in nodes.values() if not n.is_dir)} documents)"]
    if stats:
        lines.append("- result: " + ", ".join(f"{k} {v}" for k, v in stats.items()))
    if failures is not None:
        lines.append(f"- verification: **{'PASSED' if not failures else 'FAILED'}**")
        lines += [f"  - {f}" for f in failures[:50]]
    lines += ["", "## Issues", ""]
    by_kind: dict[str, list[Issue]] = {}
    for i in issues:
        by_kind.setdefault(i.kind, []).append(i)
    if not by_kind:
        lines.append("None.")
    for kind, items in sorted(by_kind.items()):
        lines.append(f"### {kind} ({len(items)})")
        lines += [f"- `{i.source}` — {i.detail}" for i in items[:100]]
        if len(items) > 100:
            lines.append(f"- … and {len(items) - 100} more")
        lines.append("")
    lines += ["## Page tree", "", "```"]

    def walk(node: Node, depth: int):
        for child in node.children:
            lines.append("  " * depth + child.title + ("/" if child.is_dir else ""))
            walk(child, depth + 1)

    walk(root, 0)
    lines.append("```")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------ main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["plan", "apply", "verify"])
    ap.add_argument("--delete", action="store_true",
                    help="trash pages whose source file no longer exists (recoverable)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    repo = here.parent.parent
    cfg = tomllib.loads((here / "confluence-sync.toml").read_text())

    try:
        api = Confluence(os.environ["CONFLUENCE_BASE_URL"],
                         os.environ["CONFLUENCE_USER_EMAIL"],
                         os.environ["CONFLUENCE_API_TOKEN"], args.verbose)
    except KeyError as exc:
        print(f"missing environment variable {exc} - see .env", file=sys.stderr)
        return 2

    # Titles must be unique across the whole space, not just our subtree, so pages
    # that already exist elsewhere in the space reserve their titles.
    print("reading the target space …")
    remote = read_remote(api, cfg["root_folder_id"])
    managed_titles = {r.title for r in remote.values()}
    reserved = {p["title"] for p in api.paged(f"/api/v2/spaces/{cfg['space_id']}/pages?limit=250")}
    reserved -= managed_titles

    root, nodes, issues = plan(repo, cfg, api, reserved)
    print(f"planned {len(nodes) - 1} pages from {repo}")

    report = here / "last-run-report.md"
    if args.command == "plan":
        write_report(report, root, nodes, issues, None, None)
        summarise(nodes, remote, issues)
        print(f"\nwrote {report.relative_to(repo)} — nothing was published")
        return 0

    if args.command == "verify":
        failures = verify(api, cfg, root, nodes)
        write_report(report, root, nodes, issues, None, failures)
        print("verification " + ("PASSED" if not failures else "FAILED"))
        for f in failures[:30]:
            print("  ✗ " + f)
        return 0 if not failures else 1

    print("publishing …")
    stats, _, orphans = apply_tree(api, cfg, root, nodes, remote, args.delete, args.verbose)
    print("  " + ", ".join(f"{k} {v}" for k, v in stats.items()))
    print("verifying …")
    failures = verify(api, cfg, root, nodes)
    # Orphans deliberately left in place are not verification failures. Only those
    # exact pages are excused - any other orphan still fails the run.
    kept = {f"unexpected managed page for {o.source_path} (orphan)"
            for o in orphans} if not args.delete else set()
    failures = [f for f in failures if f not in kept]
    write_report(report, root, nodes, issues, stats, failures)
    print("verification " + ("PASSED" if not failures else "FAILED"))
    for f in failures[:30]:
        print("  ✗ " + f)
    print(f"report: {report.relative_to(repo)}  ({api.calls} API calls)")
    return 0 if not failures else 1


def summarise(nodes, remote, issues) -> None:
    by_source = {r.source_path for r in remote.values() if r.source_path}
    wanted = {n.source_path for n in nodes.values() if n.key != ""}
    print(f"  create {len(wanted - by_source)}, "
          f"existing {len(wanted & by_source)}, orphan {len(by_source - wanted)}")
    kinds: dict[str, int] = {}
    for i in issues:
        kinds[i.kind] = kinds.get(i.kind, 0) + 1
    for kind, n in sorted(kinds.items()):
        print(f"  {kind}: {n}")


if __name__ == "__main__":
    sys.exit(main())
