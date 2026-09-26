#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""List, check and re-pin `silo: <path>@<commit>` references to prod_info_silo (issue #38).

    uv run tools/silo-pins/pins.py list            # every pin and its state at the silo ref
    uv run tools/silo-pins/pins.py check           # exit 1 if a pin's file is missing at its commit
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
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

sys.path.insert(0, str(HERE.parent / "silo-review"))
from review import FM_RE, ReadOnlyViolation, cat_batch, frontmatter, git  # noqa: E402

PIN_RE = re.compile(r"silo: `(data/[^`@\s]+)@([0-9a-fA-F]{7,40})`")
SOURCE_ID_RE = re.compile(r"^[-*]\s*\**`?([A-Z][A-Z0-9_]*)`?\**\s*[:—–-]")

CURRENT = "current"            # pinned at the silo ref already
UNCHANGED = "unchanged"        # same content at the silo ref: safe to re-pin
CHANGED = "changed"            # content differs at the silo ref: re-check the claim, then re-pin by hand
GONE = "gone at ref"           # the file no longer exists at the silo ref
BROKEN = "broken"              # the file does not exist at the pinned commit, or the commit is unknown
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


def scan_files(cfg: dict, repo: Path) -> list[Path]:
    out: set[Path] = set()
    for pattern in cfg["scan"]:
        out |= {p for p in repo.glob(pattern) if p.is_file()}
    excl = cfg.get("exclude", [])
    return sorted(p for p in out if not any(PurePosixPath(p.relative_to(repo).as_posix()).match(e) for e in excl))


def find_pins(cfg: dict, repo: Path) -> list[Pin]:
    pins = []
    for p in scan_files(cfg, repo):
        rel = p.relative_to(repo).as_posix()
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            sid = SOURCE_ID_RE.match(line.strip())
            for m in PIN_RE.finditer(line):
                pins.append(Pin(rel, i, sid.group(1) if sid else "", m.group(1), m.group(2)))
    return pins


# ---------------------------------------------------------------- silo


def resolve(silo: Path, commit: str) -> str:
    r = subprocess.run(["git", "-C", str(silo), "rev-parse", "--verify", "--quiet", f"{commit}^{{commit}}"],
                       capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip() if r.returncode == 0 else ""


def content_key(text: str) -> str:
    """What "same content" means: the silo's checksum when it has one, else the body."""
    fm = frontmatter(text)
    return "sha:" + fm["checksum_sha256"] if fm.get("checksum_sha256") else "body:" + FM_RE.sub("", text, count=1)


def evaluate(pins: list[Pin], silo: Path, ref_sha: str) -> None:
    for p in pins:
        p.resolved = resolve(silo, p.commit)
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


def render(pins: list[Pin], ref: str, ref_sha: str) -> str:
    counts = {s: sum(p.status == s for p in pins) for s in ORDER}
    out = [f"silo ref {ref} = {ref_sha[:10]} · {len(pins)} pins · " + ", ".join(f"{n} {s}" for s, n in counts.items() if n), ""]
    for p in sorted(pins, key=lambda p: (ORDER.index(p.status), p.file, p.line)):
        sid = f" {p.source_id}" if p.source_id else ""
        out.append(f"{p.status:<12} {p.file}:{p.line}{sid}  {p.path}@{p.commit}")
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
    pins = find_pins(cfg, cfg["repo"])
    evaluate(pins, silo, ref_sha)
    report = render(pins, ref, ref_sha)
    if command == "list":
        return 0, report
    if command == "check":
        broken = [p for p in pins if p.status == BROKEN]
        return (1 if broken else 0), report
    # repin
    new_commit = ref_sha[: int(cfg.get("sha_length", 10))]
    movable = [p for p in pins if p.status == UNCHANGED]
    by_file: dict[str, dict[tuple[str, str], str]] = {}
    for p in movable:
        by_file.setdefault(p.file, {})[(p.path, p.commit)] = new_commit
    summary = f"{len(movable)} pins move to {new_commit} in {len(by_file)} files; " \
              f"{sum(p.status == CHANGED for p in pins)} changed pins need a human re-check first"
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
    ap.add_argument("mode", nargs="?", choices=["plan", "apply"], default="plan", help="for repin only")
    ap.add_argument("--silo", type=Path, help="override silo_path from the config")
    ap.add_argument("--ref", help="override silo_ref from the config")
    a = ap.parse_args(argv)
    code, text = run(load_config(), a.command, a.mode, a.silo.resolve() if a.silo else None, a.ref)
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
