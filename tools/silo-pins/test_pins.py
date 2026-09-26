# /// script
# requires-python = ">=3.11"
# ///
"""Offline tests for silo-pins.

    uv run tools/silo-pins/test_pins.py

Runs on a throwaway silo and a throwaway analysis repository in a temp directory.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pins  # noqa: E402

failures: list[str] = []


def check(name: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{name}\n     expected: {expected!r}\n     actual:   {actual!r}")


def page(title: str, body: str, checksum: str | None) -> str:
    ck = f"checksum_sha256: {checksum}\n" if checksum else ""
    return f"---\ntitle: {title}\n{ck}---\n\n{body}\n"


def commit(root: Path, files: dict[str, str | None], msg: str) -> str:
    for rel, text in files.items():
        p = root / rel
        if text is None:
            p.unlink()
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                    "commit", "-qm", msg], check=True)
    return subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()


def build(tmp: Path) -> tuple[Path, Path, str, str]:
    silo, repo = tmp / "silo", tmp / "repo"
    subprocess.run(["git", "init", "-q", str(silo)], check=True)
    c1 = commit(silo, {
        "data/x/a.md": page("A", "Alpha body.", "aaa"),
        "data/x/b.md": page("B", "Beta body.", "bbb1"),
        "data/x/c.md": page("C", "Gamma body.", None),
        "data/x/d.md": page("D", "Delta body.", "ddd"),
        "data/x/f.md": page("F", "Phi body.", None),
        "data/x/g.md": page("G", "Gimel body.", "ggg"),
        "data/x/h.md": page("H", "Heth body.", "hhh1"),
    }, "c1")
    c2 = commit(silo, {
        "data/x/a.md": page("A retitled", "Alpha body.", "aaa"),   # frontmatter only
        "data/x/b.md": page("B", "Beta body, now longer.", "bbb2"),  # real change
        "data/x/c.md": page("C retitled", "Gamma body.", None),    # no checksum, same body
        "data/x/d.md": None,                                        # removed
        "data/x/f.md": page("F", "Phi body, edited.", None),       # no checksum, body changed
        "data/x/g.md": page("G", "Gimel body, reflowed.", "ggg"),  # same checksum wins over body
        "data/x/h.md": page("H", "Heth body.", "hhh2"),            # checksum changed, same body
    }, "c2")
    subprocess.run(["git", "-C", str(silo), "checkout", "-qb", "side"], check=True)
    side = commit(silo, {"data/x/a.md": page("A side", "Alpha body.", "aaa")}, "side")  # not on the ref
    subprocess.run(["git", "-C", str(silo), "checkout", "-q", "-"], check=True)
    (repo / "products/p/features/f").mkdir(parents=True)
    (repo / "products/p/features/f/feature-matrix.md").write_text(f"""# M

## Source index

- S1: https://a.test/ — page (silo: `data/x/a.md@{c1[:8]}`, captured 2026-09-01)
- S2: https://b.test/ (silo: `data/x/b.md@{c1[:8]}`)
- S3: https://c.test/ (silo: `data/x/c.md@{c1[:8]}`)
- S4: https://d.test/ (silo: `data/x/d.md@{c1[:8]}`)
- S5: https://e.test/ (silo: `data/x/e.md@{c1[:8]}`)
- S6: https://a.test/ (silo: `data/x/a.md@deadbeef`)
- S7: https://a.test/ (silo: `data/x/a.md@{c2[:10]}`)
- S8: https://f.test/ (silo: `data/x/f.md@{c1[:8]}`)
- S9: https://g.test/ (silo: `data/x/g.md@{c1[:8]}`)
- S10: https://h.test/ (silo: `data/x/h.md@{c1[:8]}`)
- S11: two copies (silo: `data/x/a.md@{c1[:8]}`; silo: `data/x/c.md@{c1[:8]}`)
- S12: https://a.test/ (silo: `data/x/a.md@{side[:10]}`)

Prose mention of silo commit `{c1[:8]}` is not a pin.

## Notes

- A — a list line outside the Source index (silo: `data/x/a.md@{c1[:8]}`)
""", encoding="utf-8")
    (repo / "reports").mkdir()
    (repo / "reports/review-queue.md").write_text(f"silo: `data/x/a.md@{c1[:8]}` (generated, excluded)\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    commit(repo, {}, "init")
    return silo, repo, c1, c2


def config(repo: Path, silo: Path) -> dict:
    cfg = pins.load_config(pins.HERE / "silo-pins.toml", repo)
    cfg["silo_path"], cfg["silo_ref"] = silo, "HEAD"
    return cfg


def hashes(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts}


def test_all(tmp: Path) -> None:
    silo, repo, c1, c2 = build(tmp)
    cfg = config(repo, silo)
    found, warnings = pins.find_pins(cfg, repo)
    check("pins found (generated reports excluded, prose ignored, ids only in the Source index)",
          [(p.source_id, p.path) for p in found],
          [("S1", "data/x/a.md"), ("S2", "data/x/b.md"), ("S3", "data/x/c.md"), ("S4", "data/x/d.md"),
           ("S5", "data/x/e.md"), ("S6", "data/x/a.md"), ("S7", "data/x/a.md"), ("S8", "data/x/f.md"),
           ("S9", "data/x/g.md"), ("S10", "data/x/h.md"), ("S11", "data/x/a.md"), ("S11", "data/x/c.md"),
           ("S12", "data/x/a.md"), ("", "data/x/a.md")])
    check("no malformed pins", warnings, [])
    pins.evaluate(found, silo, c2)
    check("statuses", [p.status for p in found], [
        pins.UNCHANGED, pins.CHANGED, pins.UNCHANGED, pins.GONE, pins.BROKEN, pins.BROKEN, pins.CURRENT,
        pins.CHANGED, pins.UNCHANGED, pins.CHANGED, pins.UNCHANGED, pins.UNCHANGED, pins.BROKEN,
        pins.UNCHANGED])

    ahead, _ = pins.find_pins(cfg, repo)
    pins.evaluate(ahead, silo, c1)
    check("a pin ahead of the ref is broken (repin would move it backwards)",
          next(p.status for p in ahead if p.source_id == "S7"), pins.BROKEN)

    matrix = repo / "products/p/features/f/feature-matrix.md"
    before, silo_before = hashes(repo), hashes(silo)
    code, text = pins.run(cfg, "list")
    check("list exits 0", code, 0)
    check("list is deterministic", pins.run(cfg, "list"), (code, text))
    check("check fails on broken pins", pins.run(cfg, "check")[0], 1)
    code, text = pins.run(cfg, "repin", "plan")
    check("repin plan summary", text.splitlines()[-1],
          f"6 pins move to {c2[:10]} in 1 files; need a human first: 3 changed, 1 gone at ref, 3 broken")
    check("list and plan write nothing", hashes(repo), before)

    old = matrix.read_text(encoding="utf-8")
    pins.run(cfg, "repin", "apply")
    new = matrix.read_text(encoding="utf-8")
    changed = [(a, b) for a, b in zip(old.splitlines(), new.splitlines()) if a != b]
    check("only the unchanged pins moved", [b for _, b in changed], [
        f"- S1: https://a.test/ — page (silo: `data/x/a.md@{c2[:10]}`, captured 2026-09-01)",
        f"- S3: https://c.test/ (silo: `data/x/c.md@{c2[:10]}`)",
        f"- S9: https://g.test/ (silo: `data/x/g.md@{c2[:10]}`)",
        f"- S11: two copies (silo: `data/x/a.md@{c2[:10]}`; silo: `data/x/c.md@{c2[:10]}`)",
        f"- A — a list line outside the Source index (silo: `data/x/a.md@{c2[:10]}`)"])
    after = hashes(repo)
    check("apply writes only the matrix", sorted(k for k in after if after[k] != before.get(k)),
          ["products/p/features/f/feature-matrix.md"])
    check("silo untouched", hashes(silo), silo_before)
    pins.run(cfg, "repin", "apply")
    check("second apply is a no-op", hashes(repo), after)


def test_check(tmp: Path) -> None:
    silo, _, c1, c2 = build(tmp / "b")
    repo = tmp / "ok"
    (repo / "docs").mkdir(parents=True)
    note = repo / "docs/note.md"
    note.write_text(f"- S1: x (silo: `data/x/a.md@{c1[:8]}`; folder silo `data/x`)\n", encoding="utf-8")
    cfg = config(repo, silo)
    check("check passes when no pin is broken", pins.run(cfg, "check")[0], 0)
    note.write_text(note.read_text() + "- also prod_info_silo `data/x/a.md` (a repository name, not a pin)\n", encoding="utf-8")
    check("'prod_info_silo' is not 'silo'", pins.run(cfg, "check")[0], 0)
    note.write_text(note.read_text() + f"- _silo: `data/x/a.md@{c1[:8]}`_ (a valid pin in italics)\n"
                    f"- prod_info_silo: `data/x/a.md@{c1[:8]}` (not a pin)\n", encoding="utf-8")
    found, warnings = pins.find_pins(cfg, repo)
    check("valid italic pin is a pin, prod_info_silo is not; no warnings", ([p.line for p in found], warnings), ([1, 3], []))
    note.write_text(note.read_text() + "- S2: y (Silo: `data/x/a.md@HEAD`)\n"
                    f"- S3: y (silo:`data/x/a.md@{c1[:8]}`)\n"
                    "- S4: y (silo: `data/x/a.md@abc12`)\n"
                    f"- S5: y (silo: `data/x@{c1[:8]}`)\n"
                    "- S6: y (silo `data/x/a.md`)\n"
                    "- S7: y _silo: `data/x/a.md@HEAD`_\n", encoding="utf-8")
    code, text = pins.run(cfg, "check")
    check("check fails on a malformed pin", code, 1)
    check("malformed pins are reported (HEAD, no space, short hex, directory)", [l for l in text.splitlines() if l.startswith("warning")], [
        "warning: docs/note.md:5: malformed pin 'Silo: `data/x/a.md@HEAD`' (expected silo: `data/<category>/<product>/<file>.md@<commit>`)",
        f"warning: docs/note.md:6: malformed pin 'silo:`data/x/a.md@{c1[:8]}`' (expected silo: `data/<category>/<product>/<file>.md@<commit>`)",
        "warning: docs/note.md:7: malformed pin 'silo: `data/x/a.md@abc12`' (expected silo: `data/<category>/<product>/<file>.md@<commit>`)",
        f"warning: docs/note.md:8: malformed pin 'silo: `data/x@{c1[:8]}`' (expected silo: `data/<category>/<product>/<file>.md@<commit>`)",
        "warning: docs/note.md:9: malformed pin 'silo `data/x/a.md`' (expected silo: `data/<category>/<product>/<file>.md@<commit>`)",
        "warning: docs/note.md:10: malformed pin 'silo: `data/x/a.md@HEAD`' (expected silo: `data/<category>/<product>/<file>.md@<commit>`)"])
    for cmd in ("list", "check"):
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                pins.main([cmd, "apply"])
            failures.append(f"{cmd} apply accepted")
        except SystemExit as e:
            check(f"a mode is for repin only ({cmd})", e.code, 2)


def test_repin_text_guard() -> None:
    text = "a silo: `data/x/a.md@1234567` b\n"
    check("rewrites the commit only", pins.repin_text(text, {("data/x/a.md", "1234567"): "abcdef0"}),
          "a silo: `data/x/a.md@abcdef0` b\n")
    try:
        pins.repin_text(text, {("data/x/a.md", "1234567"): "abc` injected"})
        failures.append("repin_text accepted a rewrite that changes other text")
    except pins.ReadOnlyViolation:
        pass


def test_write_guard(tmp: Path) -> None:
    try:
        pins.guarded_write(tmp / "x.md", "x", {tmp / "y.md"})
        failures.append("guarded_write accepted a file that is not allowed")
    except pins.ReadOnlyViolation:
        pass


def test_single_write_site() -> None:
    src = (pins.HERE / "pins.py").read_text(encoding="utf-8")
    check("the only write in pins.py is inside guarded_write",
          len(re.findall(r"\.(?:write_text|write_bytes)\(|open\([^)]*['\"][wa]", src)), 1)


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        test_all(tmp)
        test_write_guard(tmp)
        test_check(tmp)
    test_repin_text_guard()
    test_single_write_site()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(" -", f)
        return 1
    print("ok: all silo-pins tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
