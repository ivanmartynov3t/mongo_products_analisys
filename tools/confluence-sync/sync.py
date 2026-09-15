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
  purge   trash every page below the root page, to rebuild from nothing (needs --yes)

Titles are unique per space and are this tool's link key, so collisions matter. An
archived page still reserves its title (a trashed one does not), and deleting a parent
leaves its children archived - so the tool's own leftovers would otherwise push live
pages into longer path-qualified names. `apply` trashes exactly those leftovers whose
titles it needs; `plan` reports them without touching anything.

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

ROOT_KEY = "."      # the repository root, published as a page of its own
PROPERTY_KEY = "repo-sync"
LABEL = "repo-sync"
TOOL_VERSION = "2.0"


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


def slugify(heading: str) -> str:
    """GitHub-style heading anchor, so in-repo '#some-heading' links can be resolved.

    Each space becomes one hyphen - runs are *not* collapsed, which is why
    'Stage 8 - 2026-07-31' slugs to 'stage-8--2026-07-31' once the dash is stripped.
    """
    s = unicodedata.normalize("NFKD", heading).lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s", "-", s.strip())


def discover(repo: Path, cfg: dict) -> tuple[Node, dict[str, Node]]:
    """Mirror the directory tree: one page per directory, one page per document.

    Nothing is reordered or flattened, so whatever shape the repository takes in
    future, Confluence takes the same shape.

    The single permitted deviation is `fold_directory_index`: a directory's README
    becomes that directory's page content instead of a page of its own, because a
    page with no content of its own is exactly what a README is for. That holds for
    the repository root too, which is why the root is published as a *page* rather
    than mapped onto the configured Confluence folder: a folder has no body (the API
    offers no way to give it one), so a root README would have nowhere to live and
    would have to appear as a page named README.md. The root page carries the root
    README's content and everything else hangs beneath it.
    """
    excludes = cfg["exclude"]
    index_names = cfg["directory_index"] if cfg.get("fold_directory_index") else []

    def excluded(rel: Path) -> bool:
        return any(rel.match(pat) or rel.as_posix().startswith(pat.rstrip("*").rstrip("/") + "/")
                   for pat in excludes)

    files = sorted(
        p for p in repo.rglob("*.md")
        if not excluded(p.relative_to(repo))
    )

    root = Node(key=ROOT_KEY, is_dir=True)
    nodes: dict[str, Node] = {ROOT_KEY: root}

    def container(rel_dir: str) -> Node:
        if not rel_dir:
            return root
        if rel_dir in nodes:
            return nodes[rel_dir]
        parent_key = rel_dir.rpartition("/")[0] if "/" in rel_dir else ""
        parent = container(parent_key)
        node = Node(key=rel_dir, is_dir=True, parent=parent)
        parent.children.append(node)
        nodes[rel_dir] = node
        return node

    # A directory's README becomes that directory's page body rather than a page of
    # its own, so 'docs/README.md' does not sit as a child of 'docs'.
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
        container(dir_key).source = rel

    for f in files:
        rel = f.relative_to(repo)
        d = rel.parent.as_posix()
        d = "" if d == "." else d
        if index_for.get(d) == rel:
            continue  # already the body of its directory
        parent = container(d)
        node = Node(key=rel.as_posix(), is_dir=False, source=rel, parent=parent)
        parent.children.append(node)
        nodes[node.key] = node

    for n in nodes.values():
        n.children.sort(key=lambda c: (not c.is_dir, c.key))
    return root, nodes


def assign_titles(repo: Path, nodes: dict[str, Node], reserved: set[str],
                  root_title: str | None = None) -> list[Issue]:
    """Title every page after the file or directory it mirrors.

    A page is called exactly what the repository calls it - `feature-dictionary.md`,
    `studio-3t` - so the page tree reads like a directory listing.

    Confluence titles must be unique across the whole space, and this repository has 72
    files named `feature-report.md`. Where a name is not unique, every page sharing it
    is titled by its full repository path instead, which is unique by construction:
    `products/3t/studio-3t/features/ai/feature-report.md`.

    The root page is the exception: it already exists and its title is the user's to
    choose, so it is kept as it is rather than renamed to the repository's name.
    """
    issues: list[Issue] = []
    taken = set(reserved)
    ordered = sorted(nodes.values(), key=lambda n: n.key)

    groups: dict[str, list[Node]] = {}
    for node in ordered:
        name = Path(node.key).name or (root_title or repo.name)
        groups.setdefault(name, []).append(node)

    for base, group in groups.items():
        # One page may keep the bare name; a shared name sends the whole group to full
        # paths, so siblings never read inconsistently.
        use_path = len(group) > 1 or base in taken
        for node in group:
            path_title = base if node.key == ROOT_KEY else node.key
            candidate = clamp(path_title if use_path else base)
            n = 2
            while candidate in taken:
                candidate = clamp(path_title if use_path else base, suffix=f" ({n})")
                n += 1
            if candidate != base:
                issues.append(Issue("title-disambiguated", node.source_path, candidate))
            node.title = candidate
            taken.add(candidate)
    return issues


TITLE_LIMIT = 250  # Confluence rejects longer titles


def clamp(title: str, suffix: str = "") -> str:
    """Keep the tail of an over-long path - the end identifies a file, the start repeats."""
    room = TITLE_LIMIT - len(suffix)
    if len(title) > room:
        title = "…" + title[-(room - 1):]
    return title + suffix


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
        """The converted file, and nothing else.

        No child listing, no provenance footer, no navigation: a page carries exactly
        what its file carries, so the only links on it are the ones the author wrote.
        Confluence's own page tree already shows the hierarchy. A directory with no
        README therefore renders as an empty page.
        """
        if node.source is None:
            return ""
        # The document's own H1 is kept: the page is titled after the file, so the
        # heading is not a duplicate of the title.
        text = (self.repo / node.source).read_text(encoding="utf-8", errors="replace")
        return to_xhtml(self.md.render(text, {"node": node, "stack": []}))


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


def read_remote(api: Confluence, root_page_id: str) -> dict[str, RemotePage]:
    """The root page and everything beneath it."""
    pages: dict[str, RemotePage] = {}
    root = api.request("GET", f"/api/v2/pages/{root_page_id}")
    items = [{"id": root["id"], "title": root["title"], "type": "page",
              "parentId": root.get("parentId"), "root": True}]
    items += list(walk_descendants(api, "pages", root_page_id))
    for item in items:
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
            parent_id="" if item.get("root") else str(item.get("parentId") or ""),
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


def plan(repo: Path, cfg: dict, api: Confluence | None, reserved: set[str],
         root_title: str | None = None):
    root, nodes = discover(repo, cfg)
    issues = assign_titles(repo, nodes, reserved, root_title)

    renderer = Renderer(repo, nodes, cfg)
    renderer.index_anchors()
    for node in nodes.values():
        node.body = renderer.render(node)
    for node in nodes.values():
        node.digest = digest_of(node, node.parent.title if node.parent else "")
    issues.extend(renderer.issues)
    return root, nodes, issues


def bfs(root: Node):
    queue = [root]
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
        # The root page already exists and sits wherever the user put it, so it is
        # never created and never re-parented - only its content is ours to write.
        is_root = node.parent is None
        parent_id = None if is_root else page_ids[node.parent.key]
        existing = (remote.get(cfg["root_page_id"]) if is_root
                    else by_source.get(node.source_path))
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
        moved = not is_root and existing.parent_id != parent_id
        # A missing digest means the page was never fully stamped, so it cannot be
        # trusted as up to date however its content looks.
        if existing.digest is not None and existing.digest == node.digest and not moved:
            stats["unchanged"] += 1
            continue

        current = api.request("GET", f"/api/v2/pages/{existing.id}")
        update = {
            "id": existing.id, "status": "current", "title": node.title,
            "body": {"representation": "storage", "value": node.body},
            "version": {"number": current["version"]["number"] + 1,
                        "message": f"repo-sync {node.source_path}"},
        }
        if parent_id is not None:
            update["parentId"] = parent_id
        api.request("PUT", f"/api/v2/pages/{existing.id}", update)
        write_state(api, existing.id, node)
        stats["moved" if moved else "updated"] += 1
        if verbose:
            print(f"  ~ {node.title}")

    wanted = {n.source_path for n in nodes.values()}
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
    remote = read_remote(api, cfg["root_page_id"])
    by_source = {r.source_path: r for r in remote.values() if r.source_path}
    expected = {n.source_path: n for n in nodes.values()}

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
        if node.parent is None:
            parent_id = None  # the root page hangs wherever the user put it
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


# ----------------------------------------------------------------------------- purge


def purge(api: Confluence, cfg: dict, confirmed: bool) -> int:
    """Trash every page beneath the sync root, so the next publish rebuilds from nothing.

    Unlike orphan deletion, this does not spare unmanaged pages: everything below the
    root belongs to the sync, and a half-finished run can leave pages carrying no
    property. The root page itself is never deleted - it is not ours - and everything
    goes to the trash, where it stays recoverable.
    """
    pages = [(item.get("depth", 0), item["id"], item["title"])
             for item in walk_descendants(api, "pages", cfg["root_page_id"])
             if item.get("type") == "page"]
    if not pages:
        print("the folder is already empty")
        return 0
    print(f"{len(pages)} page(s) under the root folder:")
    for _, _, title in sorted(pages, key=lambda p: p[2])[:10]:
        print(f"    {title}")
    if len(pages) > 10:
        print(f"    … and {len(pages) - 10} more")
    if not confirmed:
        print("\nnothing deleted — re-run with --yes to move all of these to the trash")
        return 1
    for _, page_id, _ in sorted(pages, reverse=True):  # children before their parents
        api.request("DELETE", f"/api/v2/pages/{page_id}")
    print(f"\ntrashed {len(pages)} page(s) — recoverable from the space's trash")
    return 0


def stale_titles(api: Confluence, cfg: dict) -> dict[str, str]:
    """Titles held by archived pages this tool created: {title: page id}.

    Deleting a page's parent leaves its children *archived* with no parent. They are
    invisible in the page tree, but - measured against the live API - an archived page
    still reserves its title, while a trashed one does not:

        create a page titled like an archived one  -> 400, "A page already exists
                                                       with the same TITLE in this space"
        create a page titled like a trashed one    -> 200

    Titles are this tool's link key, so a leftover silently pushes the live page into a
    longer path-qualified name. Moving the leftover to the trash frees the title and is
    recoverable, which is why nothing here is ever purged permanently.
    """
    held: dict[str, str] = {}
    for page in api.paged(f"/api/v2/spaces/{cfg['space_id']}/pages?status=archived&limit=250"):
        props = [pr for pr in api.paged(f"/api/v2/pages/{page['id']}/properties?limit=50")
                 if pr["key"] == PROPERTY_KEY]
        if props:
            held[page["title"]] = page["id"]
    return held


def free_titles(api: Confluence, held: dict[str, str],
                wanted: set[str]) -> tuple[list[str], list[str]]:
    """Trash the archived leftovers whose titles are needed: (freed, still held).

    Best-effort by design. The archived listing is eventually consistent and can name a
    page that has already gone, for which Confluence answers 500 rather than 404 - so a
    failed delete is only a real failure if the page is still there afterwards. A title
    that genuinely cannot be freed is handed back, and the caller re-plans with it
    treated as taken rather than failing the run.
    """
    freed, stuck = [], []
    for title, page_id in held.items():
        if title not in wanted:
            continue
        try:
            api.request("DELETE", f"/api/v2/pages/{page_id}", tries=3)  # archived -> trashed
            freed.append(title)
            continue
        except RuntimeError:
            pass
        try:
            api.request("GET", f"/api/v2/pages/{page_id}", tries=1)
            stuck.append(title)
        except RuntimeError:
            freed.append(title)  # already gone, so the title is free regardless
    return freed, stuck


# -------------------------------------------------------------------------- reporting


def write_report(path: Path, root: Node, nodes: dict[str, Node], issues: list[Issue],
                 stats: dict | None, failures: list[str] | None) -> None:
    lines = [f"# confluence-sync report", "",
             f"Generated {time.strftime('%Y-%m-%d %H:%M:%S')}", "",
             f"- pages planned: **{len(nodes)}** "
             f"({sum(1 for n in nodes.values() if n.is_dir)} directories, "
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
        lines.append("  " * depth + node.title + ("/" if node.is_dir else ""))
        for child in node.children:
            walk(child, depth + 1)

    walk(root, 0)
    lines.append("```")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------ main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["plan", "apply", "verify", "purge"])
    ap.add_argument("--delete", action="store_true",
                    help="trash pages whose source file no longer exists (recoverable)")
    ap.add_argument("--yes", action="store_true",
                    help="confirm `purge`, which trashes every page under the root")
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

    if args.command == "purge":
        return purge(api, cfg, args.yes)

    # Titles must be unique across the whole space, not just our subtree, so pages
    # that already exist elsewhere in the space reserve their titles.
    print("reading the target space …")
    remote = read_remote(api, cfg["root_page_id"])
    managed_titles = {r.title for r in remote.values()}
    root_page = remote.get(cfg["root_page_id"])

    # Titles are unique per space, so anything else in the space reserves its name -
    # archived pages included, which is measured, not assumed (see stale_titles).
    # Leftovers this tool archived are the exception: their titles can be reclaimed,
    # so they are planned around rather than treated as permanently taken.
    held = stale_titles(api, cfg)
    reserved = {p["title"] for p in api.paged(f"/api/v2/spaces/{cfg['space_id']}/pages?limit=250")}
    reserved -= managed_titles
    reserved -= set(held)

    root, nodes, issues = plan(repo, cfg, api, reserved,
                               root_page.title if root_page else None)
    print(f"planned {len(nodes)} pages from {repo}")

    wanted_titles = {n.title for n in nodes.values()}
    reclaimable = sorted(set(held) & wanted_titles)
    if reclaimable:
        verb = "will be freed" if args.command == "apply" else "would be freed"
        print(f"  {len(reclaimable)} title(s) held by archived leftovers {verb} "
              f"(moved to trash, recoverable): e.g. {', '.join(reclaimable[:3])}")

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

    if reclaimable:
        freed, stuck = free_titles(api, held, wanted_titles)
        print(f"freed {len(freed)} title(s) from archived leftovers")
        if stuck:
            # Whatever could not be freed is genuinely taken, so plan around it
            # instead of failing: those pages fall back to path-qualified titles.
            print(f"  {len(stuck)} could not be freed; re-planning around them")
            root, nodes, issues = plan(repo, cfg, api, reserved | set(stuck),
                                       root_page.title if root_page else None)

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
    wanted = {n.source_path for n in nodes.values()}
    print(f"  create {len(wanted - by_source)}, "
          f"existing {len(wanted & by_source)}, orphan {len(by_source - wanted)}")
    kinds: dict[str, int] = {}
    for i in issues:
        kinds[i.kind] = kinds.get(i.kind, 0) + 1
    for kind, n in sorted(kinds.items()):
        print(f"  {kind}: {n}")


if __name__ == "__main__":
    sys.exit(main())
