#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Citation health and staleness queue for this repository, from prod_info_silo (issue #14).

    uv run tools/silo-review/review.py plan      # print the report, write nothing
    uv run tools/silo-review/review.py apply     # write reports/review-queue.md
    uv run tools/silo-review/review.py churn     # measure how often cited pages really change

Read-only by construction: the silo is read from git objects at a pinned ref (never
checked out, never written), and the only file this tool may write is the configured
output. Silo data is a change signal for a human, never evidence for a ✅ or ❌.

A cited URL is compared by the silo's content checksum (`checksum_sha256`, a hash of the
rendered page body), not by "the file was touched in a commit" — pipeline and taxonomy
commits rewrite frontmatter across the corpus without any page changing.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

URL_RE = re.compile(r"https?://[^\s<>()\[\]|`\"']+")
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
REVIEW_DATE_RE = re.compile(r"^- Analysis date:\s*(\d{4}-\d{2}-\d{2})", re.M)
SOURCE_INDEX_RE = re.compile(r"^## Source index\n(.*?)(?=^## |\Z)", re.M | re.S)
SOURCE_LINE_RE = re.compile(r"^[-*]\s*\**`?([A-Z][A-Z0-9_]*)`?\**\s*[:—–-]")


# ---------------------------------------------------------------- write guard


class ReadOnlyViolation(RuntimeError):
    pass


def guarded_write(path: Path, text: str, allowed: Path) -> None:
    """The only write in this tool. Anything but the configured output is refused."""
    if path.resolve() != allowed.resolve():
        raise ReadOnlyViolation(f"refusing to write {path}: only {allowed} may be written")
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- URL handling


def normalize_url(url: str) -> str:
    """Scheme, www., trailing slash, fragment and trailing punctuation do not make a different page."""
    url = url.strip().rstrip(".,;:*_")
    url = re.sub(r"#.*$", "", url)
    url = re.sub(r"^https?://", "", url, flags=re.I)
    host, _, rest = url.partition("/")
    host = host.lower().removeprefix("www.")
    rest = rest.rstrip("/")
    return f"{host}/{rest}" if rest else host


def domain(norm: str) -> str:
    return norm.split("/", 1)[0]


# ---------------------------------------------------------------- git (silo)


def git(silo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(silo), *args], check=True, capture_output=True, text=True).stdout


def cat_batch(silo: Path, specs: list[str]) -> dict[str, str]:
    """Read many `<rev>:<path>` objects in one process. Missing objects map to ''."""
    if not specs:
        return {}
    proc = subprocess.run(
        ["git", "-C", str(silo), "cat-file", "--batch"],
        input=("\n".join(specs) + "\n").encode(), capture_output=True, check=True,
    )
    out, pos, result = proc.stdout, 0, {}
    for spec in specs:
        nl = out.index(b"\n", pos)
        header = out[pos:nl].decode()
        pos = nl + 1
        if header.endswith("missing"):
            result[spec] = ""
            continue
        size = int(header.split()[2])
        result[spec] = out[pos:pos + size].decode("utf-8", "replace")
        pos += size + 1
    return result


def frontmatter(text: str) -> dict[str, str]:
    m = FM_RE.match(text)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if sep and not line.startswith((" ", "-")):
            fm[k.strip()] = v.strip().strip("'\"")
    return fm


MD_IMG = re.compile(r"!\[[^\]]*\]\([^)]*\)")
MIN_WORDS = 6          # shorter lines are menus, buttons and labels
BOILERPLATE_PAGES = 3  # a line on this many pages of one product is site chrome, not content
REMOVED_SHARE = 0.3    # losing this share of a page's lines counts as a content change
BULK_DAY_SHARE = 0.2   # a Last-Modified day shared by this share of a domain's pages is a site rebuild, not an edit


def content_lines(text: str) -> set[str]:
    """Substantive text lines of a silo document, normalised so re-rendering does not count as change."""
    body = FM_RE.sub("", text, count=1)
    out = set()
    for line in body.splitlines():
        if line.startswith(("> **", "# ")):  # silo header (Source / Last Updated / Navigation) and the H1 title it writes
            continue
        line = MD_IMG.sub("", line)
        line = re.sub(r"\]\([^)]*\)", " ", line)   # every link target, including nested/relative ones
        line = URL_RE.sub("", line)
        line = re.sub(r"[^\w]+", " ", line.lower())   # punctuation and markdown syntax are not content
        line = re.sub(r"\s+", " ", line).strip()
        if len(line.split()) >= MIN_WORDS:
            out.add(line)
    return out


@dataclass
class SiloDoc:
    path: str
    checksum: str
    http_last_modified: str
    fetched: str = ""   # date the silo last fetched the page (updated_at)


@dataclass
class Silo:
    root: Path
    ref: str
    sha: str
    commit_date: str
    by_url: dict[str, list[SiloDoc]] = field(default_factory=dict)
    ever_tracked: set[str] = field(default_factory=set)
    boilerplate: dict[str, set[str]] = field(default_factory=dict)
    _chrome: dict[tuple[str, str], set[str]] = field(default_factory=dict)
    bulk_days: dict[str, set[str]] = field(default_factory=dict)  # domain -> Last-Modified days that were site rebuilds

    @classmethod
    def load(cls, root: Path, ref: str, data_dir: str) -> "Silo":
        sha = git(root, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()
        cdate = git(root, "show", "-s", "--format=%cs", sha).strip()
        paths = [p for p in git(root, "ls-tree", "-r", "--name-only", sha, "--", data_dir).splitlines() if p.endswith(".md")]
        texts = cat_batch(root, [f"{sha}:{p}" for p in paths])
        silo = cls(root, ref, sha, cdate)
        freq: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for p in paths:
            for line in content_lines(texts[f"{sha}:{p}"]):
                freq[str(PurePosixPath(p).parent)][line] += 1
        silo.boilerplate = {prod: {l for l, n in lines.items() if n >= BOILERPLATE_PAGES} for prod, lines in freq.items()}
        for p in paths:
            fm = frontmatter(texts[f"{sha}:{p}"])
            if fm.get("source_url") and fm.get("checksum_sha256"):
                silo.by_url.setdefault(normalize_url(fm["source_url"]), []).append(
                    SiloDoc(p, fm["checksum_sha256"], fm.get("http_last_modified", ""), fm.get("updated_at", "")[:10]))
        for docs in silo.by_url.values():
            docs.sort(key=lambda d: d.path)
        per_dom: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for norm, docs in silo.by_url.items():
            for d in docs:
                per_dom[domain(norm)][trusted_last_modified(d) or "-"] += 1
        silo.bulk_days = {dom: {day for day, n in days.items() if day != "-" and n >= BULK_DAY_SHARE * sum(days.values())}
                          for dom, days in per_dom.items()}
        silo._index_history(data_dir)
        return silo

    def _index_history(self, data_dir: str) -> None:
        """One `git log` pass: which commits touched which file, and which files were deleted where."""
        self._commits_of: dict[str, list[tuple[str, str]]] = defaultdict(list)
        self._deleted: list[tuple[str, str]] = []
        out = git(self.root, "log", "--format=@%H %cs", "--name-status", "--no-renames", self.sha, "--", data_dir)
        commit = day = ""
        for line in out.splitlines():
            if line.startswith("@"):
                commit, day = line[1:].split()
            elif line and line.endswith(".md"):
                status, _, path = line.partition("\t")
                if status == "D":
                    self._deleted.append((commit, path))
                else:
                    self._commits_of[path].append((commit, day))

    def history(self, path: str) -> list[tuple[str, str, str, str]]:
        """(commit date, checksum, text, commit) for every commit that touched `path`, oldest first; '' if absent."""
        commits = self._commits_of.get(path, [])[::-1]
        texts = cat_batch(self.root, [f"{c}:{path}" for c, _ in commits])
        out = []
        for c, d in commits:
            t = texts[f"{c}:{path}"]
            out.append((d, frontmatter(t).get("checksum_sha256", ""), t, c))
        return out

    def chrome_at(self, commit: str, product: str) -> set[str]:
        """Lines on BOILERPLATE_PAGES+ pages of one product directory as the silo held it at `commit`.

        Banners the silo has since learned to strip (cookie notices, doc menus) are site chrome
        in the versions that still contain them, even if they no longer appear in the corpus."""
        key = (commit, product)
        if key not in self._chrome:
            paths = [p for p in git(self.root, "ls-tree", "--name-only", commit, "--", product + "/").splitlines() if p.endswith(".md")]
            freq: dict[str, int] = defaultdict(int)
            for text in cat_batch(self.root, [f"{commit}:{p}" for p in paths]).values():
                for line in content_lines(text):
                    freq[line] += 1
            self._chrome[key] = {l for l, n in freq.items() if n >= BOILERPLATE_PAGES}
        return self._chrome[key]

    def first_seen(self, path: str) -> str:
        c = self._commits_of.get(path)
        return c[-1][1] if c else ""

    def load_dropped(self, wanted: set[str]) -> None:
        """URLs the silo tracked at some point but no longer does (candidate dead or moved pages)."""
        texts = cat_batch(self.root, [f"{c}^:{p}" for c, p in self._deleted])
        for text in texts.values():
            u = frontmatter(text).get("source_url")
            if u and normalize_url(u) in wanted and normalize_url(u) not in self.by_url:
                self.ever_tracked.add(normalize_url(u))


# ---------------------------------------------------------------- analysis repo


@dataclass
class Citation:
    url: str           # as written
    norm: str
    file: str          # repo-relative
    source_id: str     # S1 … when cited in a matrix source index, else ''


@dataclass
class Matrix:
    file: str
    review_date: str | None
    citations: list[Citation]


def repo_files(cfg: dict, repo: Path) -> list[Path]:
    out = []
    for pattern in cfg["scan"]:
        out += [p for p in repo.glob(pattern) if p.is_file()]
    excl = cfg.get("exclude", [])
    return sorted({p for p in out if not any(PurePosixPath(p.relative_to(repo).as_posix()).match(e) for e in excl)})


def file_review_date(path: Path, text: str, repo: Path) -> str | None:
    m = REVIEW_DATE_RE.search(text)
    if m:
        return m.group(1)
    d = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%cs", "--", str(path)],
                       capture_output=True, text=True).stdout.strip()
    return d or None


def parse_repo(cfg: dict, repo: Path = REPO) -> tuple[list[Matrix], dict[str, list[Citation]], dict[str, str]]:
    matrices, cites_by_url, dates = [], defaultdict(list), {}
    for p in repo_files(cfg, repo):
        rel = p.relative_to(repo).as_posix()
        text = p.read_text(encoding="utf-8", errors="replace")
        dates[rel] = file_review_date(p, text, repo)
        idx = SOURCE_INDEX_RE.search(text)
        ids: dict[str, str] = {}
        if idx:
            for line in idx.group(1).splitlines():
                m = SOURCE_LINE_RE.match(line.strip())
                if m:
                    for u in URL_RE.findall(line):
                        ids.setdefault(normalize_url(u), m.group(1))
        cites = []
        for u in URL_RE.findall(text):
            n = normalize_url(u)
            c = Citation(u.rstrip(".,;:*_"), n, rel, ids.get(n, ""))
            cites.append(c)
            cites_by_url[n].append(c)
        if p.name == "feature-matrix.md":
            seen, uniq = set(), []
            for c in cites:
                if c.norm not in seen:
                    seen.add(c.norm)
                    uniq.append(c)
            matrices.append(Matrix(rel, REVIEW_DATE_RE.search(text).group(1) if REVIEW_DATE_RE.search(text) else None, uniq))
    return matrices, dict(cites_by_url), dates


# ---------------------------------------------------------------- classification


TRACKED_CHANGED = "changed since review"          # silo saw the content change after the review date
LASTMOD_AFTER = "server reports newer"            # no silo copy from before the review, but Last-Modified is later than it
TRACKED_UNCHANGED = "unchanged since review"      # silo holds a copy from before the review and nothing changed
UNCHANGED_SINCE_CAPTURE = "unchanged since silo capture"  # silo first saw it after the review; no change since then
DROPPED = "dropped by silo"                       # silo tracked it once, no longer: page removed or moved, or silo scope changed
NOT_CHECKABLE = "not checkable"                   # silo never tracked it — never reported as unchanged
ORDER = [TRACKED_CHANGED, LASTMOD_AFTER, TRACKED_UNCHANGED, UNCHANGED_SINCE_CAPTURE, DROPPED, NOT_CHECKABLE]
NEEDS_REVIEW = {TRACKED_CHANGED, LASTMOD_AFTER}


@dataclass
class Verdict:
    status: str
    changes: list[str]      # dates of real content changes after the review date
    docs: list[SiloDoc]
    first_seen: str = ""
    last_modified: str = ""  # ISO date of the latest server Last-Modified among the silo copies
    sample: list[str] = field(default_factory=list)  # up to two added lines, for the reviewer
    delta: tuple[int, int, int] = (0, 0, 0)          # (lines added, lines removed, baseline lines)


def http_date(value: str) -> str:
    try:
        return datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %Z").date().isoformat()
    except ValueError:
        return ""


def trusted_last_modified(d: SiloDoc) -> str:
    """Last-Modified as an ISO date, or '' when the server just stamps the request time (as some sites do)."""
    lm = http_date(d.http_last_modified)
    return lm if lm and d.fetched and lm < d.fetched else ""


def content_change(old: str, new: str, chrome: set[str]) -> tuple[bool, list[str], int, int]:
    """Net content change between two versions, ignoring site chrome.

    Returns (changed, added lines, removed line count, baseline line count)."""
    o, n = content_lines(old) - chrome, content_lines(new) - chrome
    added = sorted(n - o)
    removed = len(o - n)
    return bool(added) or (bool(o) and removed / len(o) >= REMOVED_SHARE), added, removed, len(o)


def classify(norm: str, review_date: str | None, silo: Silo, hist_cache: dict) -> Verdict:
    docs = silo.by_url.get(norm)
    if not docs:
        return Verdict(DROPPED if norm in silo.ever_tracked else NOT_CHECKABLE, [], [])
    first = min((silo.first_seen(d.path) for d in docs if silo.first_seen(d.path)), default="")
    bulk = silo.bulk_days.get(domain(norm), set())
    lastmod = max((lm for d in docs if (lm := trusted_last_modified(d)) and lm not in bulk), default="")
    if not review_date:
        return Verdict(UNCHANGED_SINCE_CAPTURE, [], docs, first, lastmod)
    changed_days, added_lines, baseline_seen, delta = set(), [], False, [0, 0, 0]
    for d in docs:
        if d.path not in hist_cache:
            hist_cache[d.path] = silo.history(d.path)
        versions = [v for v in hist_cache[d.path] if v[1]]
        if not versions:
            continue
        before = [v for v in versions if v[0] <= review_date]
        baseline_seen |= bool(before)
        base = before[-1] if before else versions[0]
        product = str(PurePosixPath(d.path).parent)
        chrome = silo.boilerplate.get(product, set()) | silo.chrome_at(base[3], product)
        changed, added, removed, total = content_change(base[2], versions[-1][2], chrome)
        if changed:
            added_lines += added
            delta = [delta[0] + len(added), delta[1] + removed, delta[2] + total]
            # dates on which the checksum moved after the baseline (when it happened, not whether)
            prev = base[1]
            for day, ck, _, _ in versions[versions.index(base) + 1:]:
                if ck != prev:
                    changed_days.add(day)
                prev = ck
    if changed_days:
        return Verdict(TRACKED_CHANGED, sorted(changed_days), docs, first, lastmod, sorted(set(added_lines))[:2], tuple(delta))
    if not baseline_seen and lastmod and lastmod > review_date:
        return Verdict(LASTMOD_AFTER, [], docs, first, lastmod)
    return Verdict(TRACKED_UNCHANGED if baseline_seen else UNCHANGED_SINCE_CAPTURE, [], docs, first, lastmod)


# ---------------------------------------------------------------- report


def _link(file: str) -> str:
    return f"[{file}](../{file})"


def build_report(cfg: dict, silo: Silo, matrices: list[Matrix], cites: dict[str, list[Citation]], dates: dict[str, str]) -> str:
    cache: dict = {}
    L = [
        "# Review queue — evidence that moved since review",
        "",
        "Generated by [`tools/silo-review`](../tools/silo-review/README.md) (issue #14). **Do not edit by hand.**",
        "",
        f"- Silo: `prod_info_silo` at `{silo.sha}` ({silo.commit_date}, ref `{silo.ref}`)",
        "- *Changed since review*: the page gained new text (or lost ≥ 30% of it) after the matrix's review date, compared against the silo's copy from the review date — or, when the silo is younger than the review, its first copy. Menus, site-wide banners and silo re-rendering are ignored (see [`CHURN.md`](../tools/silo-review/CHURN.md)).",
        "- *Server reports newer*: the silo holds no copy from before the review, but the page's `Last-Modified` header is later than the review date. Ignored where a server stamps the request time, and on days when a site republished ≥ 20% of its pages at once.",
        "- This is a prompt to re-review, not evidence. Silo data never becomes a ✅ or ❌; a claim changes only after a human checks the source.",
        "",
        "## Navigation",
        "",
        "- [Feature dictionary](../feature-dictionary.md) · [Low-level comparison](comparisons/low-level-feature-comparison.md) · [High-level comparison](comparisons/high-level-product-comparison.md)",
        "- Weekly routine: issue #17 · Signal reliability: [`tools/silo-review/CHURN.md`](../tools/silo-review/CHURN.md)",
        "",
    ]

    # 1. staleness queue
    rows = []
    for m in matrices:
        flagged, other = [], defaultdict(int)
        for c in m.citations:
            v = classify(c.norm, m.review_date, silo, cache)
            if v.status in NEEDS_REVIEW:
                flagged.append((c, v))
            else:
                other[v.status] += 1
        n_changed = sum(v.status == TRACKED_CHANGED for _, v in flagged)
        rows.append((m, flagged, other, n_changed))
    rows.sort(key=lambda r: (-r[3], -len(r[1]), r[0].file))
    stale = [r for r in rows if r[1]]
    L += ["## 1. Staleness queue", "",
          f"{len(stale)} of {len(matrices)} feature matrices cite at least one page that moved after the matrix's review date. "
          "Ordered by confirmed content changes, then by server-reported changes.", ""]
    if stale:
        L += ["| Matrix | Reviewed | Changed since review | Server reports newer | Other cited URLs |", "|---|---|---|---|---|"]
        for m, flagged, other, n_changed in stale:
            o = ", ".join(f"{n} {s}" for s, n in sorted(other.items(), key=lambda kv: ORDER.index(kv[0])))
            L.append(f"| {_link(m.file)} | {m.review_date} | {n_changed} | {len(flagged) - n_changed} | {o or '—'} |")
        L.append("")
        for m, flagged, _, _ in stale:
            L += [f"### {m.file}", "", f"Reviewed {m.review_date}.", ""]
            for c, v in sorted(flagged, key=lambda cv: (ORDER.index(cv[1].status), cv[0].source_id, cv[0].norm)):
                sid = f"**{c.source_id}** " if c.source_id else ""
                if v.status == TRACKED_CHANGED:
                    a, rm, tot = v.delta
                    what = f"content changed ({', '.join(v.changes)}; +{a} / −{rm} of {tot} lines)"
                    if tot and rm == tot and not a:
                        what += " — all text gone: page emptied, moved or failed to render"
                    if v.sample:
                        what += "; new text: " + " / ".join(f"“{x[:120]}”" for x in v.sample)
                else:
                    what = f"server `Last-Modified` {v.last_modified}; silo first captured it {v.first_seen}"
                L.append(f"- {sid}<{c.url}> — {what} (silo: `{v.docs[0].path}`)")
            L.append("")
    no_date = [r[0].file for r in rows if not r[0].review_date]
    no_src = [r[0].file for r in rows if r[0].review_date and not r[0].citations]
    if no_date or no_src:
        L += ["### Matrices this check cannot cover", ""]
        L += [f"- {_link(f)} — no `Analysis date` in `## Feature metadata`" for f in no_date]
        L += [f"- {_link(f)} — cites no URL (sources are research files or source-code audits)" for f in no_src]
        L.append("")

    # 2. citation health
    status_of: dict[str, str] = {}
    for norm, cl in cites.items():
        # a URL cited in several files is judged against the oldest review date that cites it
        rds = [dates[c.file] for c in cl if dates.get(c.file)]
        status_of[norm] = classify(norm, min(rds) if rds else None, silo, cache).status
    counts = defaultdict(int)
    by_dom = defaultdict(lambda: defaultdict(int))
    for norm, st in status_of.items():
        counts[st] += 1
        by_dom[domain(norm)][st] += 1
    files = {c.file for cl in cites.values() for c in cl}
    L += ["## 2. Citation health", "",
          f"{len(status_of)} distinct URLs cited across {len(files)} files. A URL cited in several files is judged against the oldest review date that cites it "
          "(a matrix's `Analysis date`, otherwise the file's last commit date).", "",
          "| Status | URLs |", "|---|---|"]
    L += [f"| {st} | {counts.get(st, 0)} |" for st in ORDER]
    L += ["", "*Not checkable* means the silo has never tracked the page (forums, issue trackers, sites it does not crawl). It is never reported as unchanged.", "",
          "### By domain", "", "| Domain | " + " | ".join(ORDER) + " |", "|---|" + "---|" * len(ORDER)]
    for d in sorted(by_dom, key=lambda d: (-sum(by_dom[d].values()), d)):
        L.append(f"| {d} | " + " | ".join(str(by_dom[d].get(st, 0)) for st in ORDER) + " |")
    dropped = sorted(n for n, st in status_of.items() if st == DROPPED)
    if dropped:
        L += ["", "### Dropped by the silo", "",
              "The silo tracked these pages once and no longer does: the page was removed or moved, or the silo stopped crawling it. Check the link before relying on it.", ""]
        L += [f"- <https://{n}> — cited in {', '.join(_link(f) for f in sorted({c.file for c in cites[n]}))}" for n in dropped]
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- churn


def churn(cfg: dict, silo: Silo, cites: dict[str, list[Citation]]) -> str:
    """Per ISO week, for cited pages the silo tracks: files touched, checksum changes, real content changes."""
    touched: dict[str, set[str]] = defaultdict(set)
    checksum: dict[str, set[str]] = defaultdict(set)
    real: dict[str, set[str]] = defaultdict(set)
    tracked = sorted(n for n in cites if n in silo.by_url)
    cache: dict = {}
    for n in tracked:
        for d in silo.by_url[n]:
            product = str(PurePosixPath(d.path).parent)
            prev = None
            for day, ck, text, commit in cache.setdefault(d.path, silo.history(d.path)):
                wk = "%d-W%02d" % date.fromisoformat(day).isocalendar()[:2]
                touched[wk].add(n)
                if not ck:
                    continue
                if prev is not None and ck != prev[0]:
                    checksum[wk].add(n)
                    chrome = silo.boilerplate.get(product, set()) | silo.chrome_at(prev[2], product)
                    if content_change(prev[1], text, chrome)[0]:
                        real[wk].add(n)
                prev = (ck, text, commit)
    L = [f"Silo `{silo.sha[:10]}` ({silo.commit_date}); {len(tracked)} cited URLs tracked by the silo.", "",
         "| ISO week | File touched | Checksum changed | Content really changed |", "|---|---|---|---|"]
    for wk in sorted(touched):
        L.append(f"| {wk} | {len(touched[wk])} | {len(checksum[wk])} | {len(real[wk])} |")
    return "\n".join(L)


# ---------------------------------------------------------------- main


def load_config(path: Path = HERE / "silo-review.toml", repo: Path = REPO) -> dict:
    cfg = tomllib.loads(path.read_text(encoding="utf-8"))
    cfg["repo"] = repo
    cfg["silo_path"] = (repo / cfg["silo_path"]).resolve()
    cfg["output_path"] = (repo / cfg["output"]).resolve()
    return cfg


def run(cfg: dict, command: str, silo_root: Path | None = None, ref: str | None = None) -> str:
    """Execute one command against a loaded config; returns what `main` prints."""
    silo = Silo.load(silo_root or cfg["silo_path"], ref or cfg["silo_ref"], cfg.get("silo_data_dir", "data"))
    matrices, cites, dates = parse_repo(cfg, cfg["repo"])
    silo.load_dropped(set(cites))
    if command == "churn":
        return churn(cfg, silo, cites)
    report = build_report(cfg, silo, matrices, cites, dates)
    if command == "plan":
        return report
    guarded_write(cfg["output_path"], report, cfg["output_path"])
    return f"wrote {cfg['output']} (silo {silo.sha[:10]})"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["plan", "apply", "churn"])
    ap.add_argument("--silo", type=Path, help="override silo_path from the config")
    ap.add_argument("--ref", help="override silo_ref from the config")
    a = ap.parse_args(argv)
    cfg = load_config()
    print(run(cfg, a.command, a.silo.resolve() if a.silo else None, a.ref))
    return 0

if __name__ == "__main__":
    sys.exit(main())
