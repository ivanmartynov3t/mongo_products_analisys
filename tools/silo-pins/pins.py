#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""List, check and re-pin `silo: <path>@<commit>` references to prod_info_silo (issue #38).

    uv run tools/silo-pins/pins.py list            # every pin and its state at the silo ref
    uv run tools/silo-pins/pins.py check           # exit 1 if a pin is broken or malformed
    uv run tools/silo-pins/pins.py repin plan      # show which pins would move to the silo ref
    uv run tools/silo-pins/pins.py repin apply     # move them: only pins whose content is unchanged

A pin names one silo file at one silo commit, e.g.
`silo: data/3t/3t-website-2026/index.md@f1e28e8d`. Re-pinning only moves a pin whose file
has the same content at the silo ref as at the pinned commit; a changed page needs a human
to re-check the claim first. The silo is read from git objects only. `repin apply` changes
nothing in a file except the commit part of unchanged pins, and the tool checks that.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

sys.path.insert(0, str(HERE.parent / "silo-review"))
from review import (FM_RE, SOURCE_LINE_RE, ReadOnlyViolation, cat_batch, frontmatter, git,  # noqa: E402
                    repo_files)

PIN_RE = re.compile(r"silo: `(data/[^`@\s]+)@([0-9a-fA-F]{7,40})`")
# Text that looks like a pin but does not match PIN_RE (`Silo:`, no space, short or symbolic commit).
# A silo directory mention ("silo `data/3t/pii-scanner`") names no file and is not a near miss.
NEAR_PIN_RE = re.compile(r"silo:?\s*`data/[^`]*(?:@|\.md)[^`]*`", re.I)

CURRENT = "current"            # pinned at the silo ref already
UNCHANGED = "unchanged"        # same content at the silo ref: safe to re-pin
CHANGED = "changed"            # content differs at the silo ref: re-check the claim, then re-pin by hand
GONE = "gone at ref"           # the file no longer exists at the silo ref
BROKEN = "broken"              # the commit is unknown or not on the silo ref's history, or the file is missing there
ORDER = [BROKEN, GONE, CHANGED, UNCHANGED, CURRENT]


@dataclass
class Pin:
    file: str        # repo-relative
    line: int        # 1-based
    source_id: str   # S1 … when the pin is on a Source index line, else ''
    path: str
    commit: str      # as written
    status: str = ""
    resolved: str = ""  # full SHA of `commit`, '' if unknown


# ---------------------------------------------------------------- repository


def find_pins(cfg: dict, repo: Path) -> tuple[list[Pin], list[str]]:
    """Every pin, plus a warning for each piece of text that looks like a pin but is malformed."""
    pins, warnings = [], []
    for p in repo_files(cfg, repo):
        rel = p.relative_to(repo).as_posix()
        in_index = False
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("## "):
                in_index = line.rstrip() == "## Source index"
            sid = SOURCE_LINE_RE.match(line.strip()) if in_index else None
            for m in PIN_RE.finditer(line):
                pins.append(Pin(rel, i, sid.group(1) if sid else "", m.group(1), m.group(2)))
            for m in NEAR_PIN_RE.finditer(line):
                if not PIN_RE.fullmatch(m.group(0)):
                    warnings.append(f"{rel}:{i}: malformed pin {m.group(0)!r} (expected silo: `data/<path>@<commit>`)")
    return pins, warnings


# ---------------------------------------------------------------- silo


def resolve(silo: Path, commit: str, ref_sha: str) -> str:
    """Full SHA of `commit`, or '' when it is unknown or not an ancestor of the silo ref.

    A pin to a local-only or unmerged commit would pass here and break on other clones, and
    one ahead of the ref would be moved backwards by a re-pin; both count as broken.
    """
    r = subprocess.run(["git", "-C", str(silo), "rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}"],
                       capture_output=True, text=True, encoding="utf-8")
    sha = r.stdout.strip() if r.returncode == 0 else ""
    if sha and subprocess.run(["git", "-C", str(silo), "merge-base", "--is-ancestor", sha, ref_sha],
                              capture_output=True).returncode != 0:
        return ""
    return sha


def content_key(text: str) -> str:
    """What "same content" means: the silo's checksum when it has one, else the body."""
    fm = frontmatter(text)
    return "sha:" + fm["checksum_sha256"] if fm.get("checksum_sha256") else "body:" + FM_RE.sub("", text, count=1)


def evaluate(pins: list[Pin], silo: Path, ref_sha: str) -> None:
    for p in pins:
        p.resolved = resolve(silo, p.commit, ref_sha)
    specs = sorted({f"{p.resolved}:{p.path}" for p in pins if p.resolved} | {f"{ref_sha}:{p.path}" for p in pins})
    blobs = cat_batch(silo, specs)
    for p in pins:
        old = blobs.get(f"{p.resolved}:{p.path}", "") if p.resolved else ""
        new = blobs.get(f"{ref_sha}:{p.path}", "")
        if not old:
            p.status = BROKEN
        elif p.resolved == ref_sha:
            p.status = CURRENT
        elif not new:
            p.status = GONE
        else:
            p.status = UNCHANGED if content_key(old) == content_key(new) else CHANGED


# ---------------------------------------------------------------- output


def render(pins: list[Pin], warnings: list[str], ref: str, ref_sha: str) -> str:
    counts = {s: sum(p.status == s for p in pins) for s in ORDER}
    out = [f"silo ref {ref} = {ref_sha[:10]} · {len(pins)} pins · " + ", ".join(f"{n} {s}" for s, n in counts.items() if n), ""]
    for p in sorted(pins, key=lambda p: (ORDER.index(p.status), p.file, p.line)):
        sid = f" {p.source_id}" if p.source_id else ""
        out.append(f"{p.status:<12} {p.file}:{p.line}{sid}  {p.path}@{p.commit}")
    if warnings:
        out += ["", *(f"warning: {w}" for w in warnings)]
    return "\n".join(out)


def repin_text(text: str, moves: dict[tuple[str, str], str]) -> str:
    """Rewrite the commit of each pin in `moves` ((path, old commit) -> new commit); nothing else."""
    new = PIN_RE.sub(lambda m: f"silo: `{m.group(1)}@{moves.get((m.group(1), m.group(2)), m.group(2))}`", text)
    strip = lambda s: PIN_RE.sub(lambda m: f"silo: `{m.group(1)}@`", s)  # noqa: E731
    if strip(new) != strip(text):
        raise ReadOnlyViolation("re-pinning would change text other than pin commits")
    return new


def guarded_write(path: Path, text: str, allowed: set[Path]) -> None:
    """The only write in this tool: files that hold pins being moved, and nothing else."""
    if path.resolve() not in {a.resolve() for a in allowed}:
        raise ReadOnlyViolation(f"refusing to write {path}: not a file with pins to move")
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- main


def load_config(path: Path = HERE / "silo-pins.toml", repo: Path = REPO) -> dict:
    cfg = tomllib.loads(path.read_text(encoding="utf-8"))
    cfg["repo"] = repo
    cfg["silo_path"] = (repo / cfg["silo_path"]).resolve()
    return cfg


def run(cfg: dict, command: str, mode: str = "plan", silo_root: Path | None = None, ref: str | None = None) -> tuple[int, str]:
    """Execute one command; returns (exit code, text to print)."""
    silo, ref = silo_root or cfg["silo_path"], ref or cfg["silo_ref"]
    ref_sha = git(silo, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()
    pins, warnings = find_pins(cfg, cfg["repo"])
    evaluate(pins, silo, ref_sha)
    report = render(pins, warnings, ref, ref_sha)
    if command == "list":
        return 0, report
    if command == "check":
        return (1 if warnings or any(p.status == BROKEN for p in pins) else 0), report
    # repin
    new_commit = ref_sha[: int(cfg.get("sha_length", 10))]
    movable = [p for p in pins if p.status == UNCHANGED]
    by_file: dict[str, dict[tuple[str, str], str]] = {}
    for p in movable:
        by_file.setdefault(p.file, {})[(p.path, p.commit)] = new_commit
    human = ", ".join(f"{sum(p.status == s for p in pins)} {s}" for s in (CHANGED, GONE, BROKEN))
    summary = f"{len(movable)} pins move to {new_commit} in {len(by_file)} files; " \
              f"need a human first: {human}"
    if mode == "plan":
        return 0, report + "\n\n" + summary
    allowed = {cfg["repo"] / f for f in by_file}
    for f, moves in sorted(by_file.items()):
        path = cfg["repo"] / f
        guarded_write(path, repin_text(path.read_text(encoding="utf-8"), moves), allowed)
    return 0, "applied: " + summary


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["list", "check", "repin"])
    ap.add_argument("mode", nargs="?", choices=["plan", "apply"], help="for repin only (default: plan)")
    ap.add_argument("--silo", type=Path, help="override silo_path from the config")
    ap.add_argument("--ref", help="override silo_ref from the config")
    a = ap.parse_args(argv)
    if a.mode and a.command != "repin":
        ap.error(f"{a.command} takes no mode; plan/apply is for repin only")
    code, text = run(load_config(), a.command, a.mode or "plan", a.silo.resolve() if a.silo else None, a.ref)
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
