#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Porting validator: checks one /silo-port item's changes before its PR (issue #53, Plan 09 L4).

    uv run tools/silo-candidates/validate.py --item datagrip
    uv run tools/silo-candidates/validate.py --item scope-triggers | cross-product | readme

Compares the working tree (committed, staged, unstaged and untracked files) with its merge-base
with `main`. Only what changed is checked; untouched rows are never judged. For every touched
capability row:
  1. its IDs exist in the dictionary and are not retired;
  2. its status uses the legal labels, with the fields each needs (✅: a cited source with URL
     and date; ❌: a verified quote; ❓: "Checked <URL> on <date>");
  3. the silo pins it cites resolve and are current or unchanged at the silo ref;
  4. every quoted passage appears in a cited source (a pinned silo page or a repository file).
Across the whole diff:
  5. no added line names a non-public host or repository that the base does not already name;
  6. for a product item, no open web-backed candidate is left without a ledger row;
  7. only files in the item's scope changed; reports/silo-candidates.md only as fresh tool output.

Exit 0 clean, 1 findings for a human, 2 error. Output never names a private repository or URL,
so it can be pasted into a PR. Read-only: writes nothing.
"""

from __future__ import annotations

import argparse
import difflib
import fnmatch
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "silo-pins"))
import candidates  # noqa: E402
import pins  # noqa: E402
from review import (SOURCE_LINE_RE, URL_RE, cat_batch, cell_ids, FM_RE, git, host_matches,  # noqa: E402
                    host_of, matrix_table_ids, normalize_url, ID_HEADERS)


class ValidationError(RuntimeError):
    pass


ITEMS_FIXED = ("scope-triggers", "cross-product", "readme")
MATRIX_GLOB = "products/*/*/features/*/feature-matrix.md"
DATE_RE = re.compile(r"(?<![0-9])20[0-9]{2}-[0-9]{2}-[0-9]{2}(?![0-9])")
CHECKED_RE = re.compile(r"Checked\s+\S*https?://\S+\s+on\s+20[0-9]{2}-[0-9]{2}-[0-9]{2}", re.I)
BACKTICK_RE = re.compile(r"`([^`]+)`")
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")


@dataclass
class Finding:
    file: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.file}:{self.line}: {self.message}" if self.line else f"{self.file}: {self.message}"


@dataclass
class Source:
    sid: str
    line: int
    text: str
    urls: list[str] = field(default_factory=list)
    pins: list[tuple[str, str]] = field(default_factory=list)  # (silo path, commit)
    repo_paths: list[str] = field(default_factory=list)


# ---------------------------------------------------------------- git (analysis repo)


def run_git(repo: Path, *args: str, check: bool = True) -> str:
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode != 0:
        raise ValidationError(f"git {' '.join(args)} failed: {r.stderr.strip()[:200]}")
    return r.stdout


def merge_base(repo: Path, base: str) -> str:
    run_git(repo, "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}")
    return run_git(repo, "merge-base", "HEAD", base).strip()


def changed_files(repo: Path, base_sha: str) -> list[str]:
    """Every path that differs from the base in the working tree, including untracked files."""
    tracked = run_git(repo, "diff", "--name-only", "-z", base_sha).split("\0")
    untracked = run_git(repo, "ls-files", "--others", "--exclude-standard", "-z").split("\0")
    return sorted({p for p in tracked + untracked if p})


def base_text(repo: Path, base_sha: str, path: str) -> str:
    return cat_batch(repo, [f"{base_sha}:{path}"])[f"{base_sha}:{path}"]


def added_lines(old: str, new: str) -> list[tuple[int, str]]:
    """(1-based line number, text) of lines inserted or replaced in `new`."""
    a, b = old.splitlines(), new.splitlines()
    out = []
    for tag, _, _, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag in ("insert", "replace"):
            out += [(j + 1, b[j]) for j in range(j1, j2)]
    return out


# ---------------------------------------------------------------- matrices


def split_cells(line: str) -> list[str]:
    return [c.strip() for c in CELL_SPLIT_RE.split(line.strip().strip("|"))]


def capability_rows(text: str) -> list[tuple[int, str, dict[str, str]]]:
    """(line number, raw line, {header: cell}) of every row of every capability table."""
    rows, header = [], None
    for i, line in enumerate(text.splitlines(), 1):
        cells = split_cells(line) if line.startswith("|") else []
        if not cells:
            header = None
        elif cells[0].startswith(ID_HEADERS):
            header = cells if ("Current support" in cells or "Status" in cells) else None
        elif header and not set(cells[0]) <= set("-: "):
            rows.append((i, line, dict(zip(header, cells))))
    return rows


def source_index(text: str, repo: Path) -> dict[str, Source]:
    out: dict[str, Source] = {}
    in_index = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            in_index = line.rstrip() == "## Source index"
            continue
        m = SOURCE_LINE_RE.match(line.strip()) if in_index else None
        if not m:
            continue
        s = Source(m.group(1), i, line, URL_RE.findall(line), [(p.group(1), p.group(2)) for p in pins.PIN_RE.finditer(line)])
        for b in BACKTICK_RE.findall(line):
            if not b.startswith("data/") and "/" in b and (repo / b).is_file():
                s.repo_paths.append(b)
        out[s.sid] = s
    return out


def status_classes(cell: str, vocab: dict[str, list[str]]) -> list[str]:
    text, found = cell.casefold(), []
    for cls, labels in vocab.items():
        for label in sorted(labels, key=len, reverse=True):
            pat = re.escape(label.casefold())
            if label[0].isalnum():
                pat = rf"(?<![a-z]){pat}(?![a-z])"
            text, n = re.subn(pat, " ", text)
            if n and cls not in found:
                found.append(cls)
    return found


_TRANS = str.maketrans({"“": '"', "”": '"', "„": '"', "‘": "'", "’": "'", "–": "-", "—": "-", "‑": "-", " ": " "})


def normalise(text: str) -> str:
    text = text.translate(_TRANS)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)      # markdown links and images -> their text
    text = re.sub(r"[*_`]+", "", text)                           # emphasis and code marks
    text = text.replace("\\|", "|").replace('"', "'")   # a quote inside a quote is often re-quoted with ' when cited
    return " ".join(text.split()).casefold()


def quotes(row: str, min_words: int) -> list[str]:
    """Quoted passages of a row, split at ellipses into the fragments that must be found."""
    out = []
    for q in re.findall(r'"([^"]+)"', row.translate(_TRANS)):
        for frag in re.split(r"\.\.\.|…|\[\.\.\.\]", q):
            frag = frag.strip(" .,;:")
            if len(frag.split()) >= min_words:
                out.append(frag)
    return out


def dictionary_ids(text: str) -> tuple[set[str], set[str]]:
    """(all dictionary IDs, retired IDs)."""
    caps, pointers = matrix_table_ids(text)
    retired = set()
    for line in text.splitlines():
        if line.startswith("|") and "Retired" in line:
            retired.update(cell_ids(split_cells(line)[0]))
    return caps | pointers, retired


# ---------------------------------------------------------------- the checks


def check_matrix(rel: str, new: str, old: str, ctx: dict, findings: list[Finding]) -> None:
    repo, vcfg = ctx["repo"], ctx["vcfg"]
    sources = source_index(new, repo)
    base_lines = set(old.splitlines())
    touched = []
    for n, line, cells in capability_rows(new):
        sid_cell = cells.get("Sources", cells.get("Source", ""))
        cited = [t for t in re.findall(r"[A-Z][A-Z0-9_]*", sid_cell) if t in sources]
        if line not in base_lines or any(sources[c].text not in base_lines for c in cited):
            touched.append((n, line, cells, sid_cell, cited))
    for n, line, cells, sid_cell, cited in touched:
        first = next(iter(cells.values()), "")
        ids = cell_ids(first)
        if not ids:
            findings.append(Finding(rel, n, "no sub-feature ID in the first column"))
        for i in ids:
            if i not in ctx["dict_ids"]:
                findings.append(Finding(rel, n, f"{i} is not in {vcfg['dictionary']}"))
            elif i in ctx["retired"]:
                findings.append(Finding(rel, n, f"{i} is retired; use the ID it is an alias of"))
        status = cells.get("Current support", cells.get("Status", ""))
        classes = status_classes(status, vcfg["status"])
        if not classes:
            findings.append(Finding(rel, n, f"status {status[:40]!r} has no legal label ({', '.join(vcfg['status'])})"))
        if not cited:
            findings.append(Finding(rel, n, f"cites no Source index entry (Sources: {sid_cell[:30]!r})"))
        cited_src = [sources[c] for c in cited]
        if "confirmed" in classes and not any(s.urls and DATE_RE.search(s.text) for s in cited_src):
            findings.append(Finding(rel, n, "confirmed status needs a cited source with a URL and a YYYY-MM-DD date on its Source index line"))
        if "unverified" in classes and not CHECKED_RE.search(line):
            findings.append(Finding(rel, n, 'unverified status needs a note "Checked <URL> on <YYYY-MM-DD>"'))
        # pins on the cited sources
        haystacks = []
        for s in cited_src:
            for path, commit in s.pins:
                state, body = ctx["pin_state"](path, commit)
                if state not in (pins.CURRENT, pins.UNCHANGED):
                    findings.append(Finding(rel, s.line, f"{s.sid}: silo pin is {state} at the silo ref; re-check the claim"))
                if body:
                    haystacks.append(normalise(FM_RE.sub("", body, count=1)))
            for p in s.repo_paths:
                haystacks.append(normalise((repo / p).read_text(encoding="utf-8", errors="replace")))
        if haystacks:
            haystacks.append(ctx["dictionary_text"])   # rows also quote the dictionary's definition of the ID
        qs = quotes(line, int(vcfg["min_quote_words"]))
        if qs and not haystacks:
            findings.append(Finding(rel, n, "quotes a source, but no cited source has a silo pin or a repository file to check it against"))
        elif haystacks:
            for q in qs:
                if not any(normalise(q) in h for h in haystacks):
                    findings.append(Finding(rel, n, f"quote not found in the cited sources ({', '.join(cited)}): {q[:50]!r}"))
        if "absent" in classes and not (qs and haystacks):
            findings.append(Finding(rel, n, "not-supported status needs a quoted, checkable exclusion from a cited source"))


def check_private(rel: str, added: list[tuple[int, str]], ctx: dict, findings: list[Finding]) -> None:
    base_all = ctx["base_all"]
    for n, line in added:
        for url in URL_RE.findall(line):
            norm = normalize_url(url)
            if host_matches(norm, ctx["non_public_hosts"]):
                prefix = "/".join(norm.split("?", 1)[0].split("/")[:3]).casefold()
                if prefix not in base_all:
                    findings.append(Finding(rel, n, f"links a non-public host ({host_of(norm)}) with a repository the "
                                                    "base does not already cite; URL withheld. Confirm it is public"))
        low = line.casefold()
        for name in ctx["private_names"]:
            if re.search(rf"(?<![a-z0-9_.-]){re.escape(name)}(?![a-z0-9_-])", low):
                findings.append(Finding(rel, n, "names a silo repository that this repository does not name yet; "
                                                "name withheld. Remove it, or confirm it is public"))
                break


def private_names(by_product: dict[str, list[dict]], base_all: str) -> list[str]:
    """Silo repository folder names that the base tree never mentions. Kept in memory only."""
    names = set()
    for entries in by_product.values():
        for e in entries:
            parts = PurePosixPath(e.get("path", "")).parts
            if len(parts) > 4 and parts[2] == "repo_docs":
                names.add(parts[3].casefold())
            elif len(parts) > 3:
                names.add(parts[2].casefold())
    tokens = set(re.findall(r"[a-z0-9_.-]+", base_all))
    return sorted(n for n in names if len(n) >= 3 and n not in tokens)


def in_scope(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, p) for p in patterns)


# ---------------------------------------------------------------- run


def validate(vcfg: dict, ccfg: dict, item: str, base: str, silo: Path, ref: str) -> tuple[int, str]:
    repo = vcfg["repo"]
    base_sha = merge_base(repo, base)
    folders = {d.name for d in (repo / "products").glob("*/*") if d.is_dir()}
    if item not in ITEMS_FIXED and item not in folders:
        raise ValidationError(f"unknown item {item!r}: a product folder name or one of {', '.join(ITEMS_FIXED)}")
    kind = item if item in ITEMS_FIXED else "product"
    scope = [p.format(item=item) for p in vcfg["scope"][kind] + vcfg["scope"]["always"]]
    ref_sha = git(silo, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()

    open_web: dict[str, list[str]] = {}
    fresh_report = candidates.build(ccfg, silo, ref, open_web)   # also checks the ledger (exit 2 when malformed)
    _, _, by_product = candidates.load_catalog(silo, ref, ccfg["silo_catalog"], ccfg["silo_data_dir"])

    tree = [p for p in run_git(repo, "ls-tree", "-r", "--name-only", "-z", base_sha).split("\0") if p]
    suffixes = tuple(vcfg["text_suffixes"])
    blobs = cat_batch(repo, [f"{base_sha}:{p}" for p in tree if PurePosixPath(p).suffix in suffixes])
    base_all = "\n".join(blobs.values()).casefold()

    dict_ids, retired = dictionary_ids((repo / vcfg["dictionary"]).read_text(encoding="utf-8"))
    pin_cache: dict[tuple[str, str], tuple[str, str]] = {}

    def pin_state(path: str, commit: str) -> tuple[str, str]:
        if (path, commit) not in pin_cache:
            p = pins.Pin("", 0, "", path, commit)
            pins.evaluate([p], silo, ref_sha)
            body = cat_batch(silo, [f"{p.resolved}:{path}"])[f"{p.resolved}:{path}"] if p.resolved else ""
            pin_cache[(path, commit)] = (p.status, body)
        return pin_cache[(path, commit)]

    ctx = {"repo": repo, "vcfg": vcfg, "dict_ids": dict_ids,
           "dictionary_text": normalise((repo / vcfg["dictionary"]).read_text(encoding="utf-8")), "retired": retired, "pin_state": pin_state,
           "base_all": base_all, "non_public_hosts": list(ccfg.get("non_public_hosts", [])),
           "private_names": private_names(by_product, base_all)}
    findings: list[Finding] = []
    files = changed_files(repo, base_sha)
    for rel in files:
        path = repo / rel
        if not in_scope(rel, scope):
            findings.append(Finding(rel, 0, f"outside the scope of item {item!r}"))
        if rel in vcfg["tool_owned"] and rel != vcfg["candidates_output"] and path.exists():
            findings.append(Finding(rel, 0, "tool-owned report changed; confirm it is unchanged output of its tool"))
        if not path.is_file() or PurePosixPath(rel).suffix not in suffixes:
            continue
        new = path.read_text(encoding="utf-8", errors="replace")
        old = base_text(repo, base_sha, rel)
        added = added_lines(old, new)
        check_private(rel, added, ctx, findings)
        if fnmatch.fnmatchcase(rel, MATRIX_GLOB):
            check_matrix(rel, new, old, ctx, findings)
        if rel == vcfg["triage_ledger"] and kind == "product":
            for n, line in added:
                if line.split("\t", 1)[0] != item:
                    findings.append(Finding(rel, n, f"ledger row for another product than {item!r}"))
    # Checked whether or not it changed: a ledger edit without a regenerated report leaves it stale.
    report = repo / vcfg["candidates_output"]
    if not report.is_file() or report.read_text(encoding="utf-8") != fresh_report:
        findings.append(Finding(vcfg["candidates_output"], 0, "differs from a fresh `candidates.py apply` run at the "
                                "silo ref; regenerate it, never edit it"))
    if kind == "product" and open_web.get(item):
        findings.append(Finding(vcfg["triage_ledger"], 0, f"{len(open_web[item])} open web-backed candidates of {item} "
                                f"have no ledger row: {', '.join(open_web[item])}"))

    head = [f"validate: item {item} · base {base_sha[:10]} · silo {ref_sha[:10]} · {len(files)} changed files"]
    if not findings:
        return 0, "\n".join(head + ["ok: no findings"])
    body = [str(f) for f in sorted(findings, key=lambda f: (f.file, f.line, f.message))]
    return 1, "\n".join(head + body + [f"{len(findings)} findings: fix them, or record them as needs-human in the PR"])


def load_config(path: Path = HERE / "validate.toml", repo: Path = REPO) -> dict:
    cfg = tomllib.loads(path.read_text(encoding="utf-8"))
    cfg["repo"] = repo
    return cfg


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--item", required=True, help="a product folder name, or scope-triggers, cross-product, readme")
    ap.add_argument("--base", default="main", help="compare with the merge-base of HEAD and this ref (default: main)")
    ap.add_argument("--silo", type=Path, help="override silo_path from the candidates config")
    ap.add_argument("--ref", help="override silo_ref from the candidates config")
    a = ap.parse_args(argv)
    try:
        vcfg = load_config()
        ccfg = candidates.load_config(REPO / vcfg["candidates_config"], REPO)
        rc, out = validate(vcfg, ccfg, a.item, a.base, (a.silo.resolve() if a.silo else ccfg["silo_path"]),
                           a.ref or ccfg["silo_ref"])
    except (ValidationError, candidates.CandidatesError, subprocess.CalledProcessError, OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(out)
    return rc


if __name__ == "__main__":
    sys.exit(main())
