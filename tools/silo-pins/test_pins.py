# /// script
# requires-python = ">=3.11"
# ///
"""Offline tests for silo-pins.

    uv run tools/silo-pins/test_pins.py

Runs on a throwaway silo and a throwaway analysis repository in a temp directory.
"""

from __future__ import annotations

import hashlib
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
    }, "c1")
    c2 = commit(silo, {
        "data/x/a.md": page("A retitled", "Alpha body.", "aaa"),   # frontmatter only
        "data/x/b.md": page("B", "Beta body, now longer.", "bbb2"),  # real change
        "data/x/c.md": page("C retitled", "Gamma body.", None),    # no checksum, same body
        "data/x/d.md": None,                                        # removed
    }, "c2")
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

Prose mention of silo commit `{c1[:8]}` is not a pin.
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
    found = pins.find_pins(cfg, repo)
    check("pins found (generated reports excluded, prose ignored)", [p.source_id for p in found],
          ["S1", "S2", "S3", "S4", "S5", "S6", "S7"])
    pins.evaluate(found, silo, c2)
    check("statuses", {p.source_id: p.status for p in found}, {
        "S1": pins.UNCHANGED, "S2": pins.CHANGED, "S3": pins.UNCHANGED, "S4": pins.GONE,
        "S5": pins.BROKEN, "S6": pins.BROKEN, "S7": pins.CURRENT})

    matrix = repo / "products/p/features/f/feature-matrix.md"
    before, silo_before = hashes(repo), hashes(silo)
    code, text = pins.run(cfg, "list")
    check("list exits 0", code, 0)
    check("list is deterministic", pins.run(cfg, "list"), (code, text))
    check("check fails on broken pins", pins.run(cfg, "check")[0], 1)
    code, text = pins.run(cfg, "repin", "plan")
    check("repin plan summary", text.splitlines()[-1],
          f"2 pins move to {c2[:10]} in 1 files; 1 changed pins need a human re-check first")
    check("list and plan write nothing", hashes(repo), before)

    old = matrix.read_text(encoding="utf-8")
    pins.run(cfg, "repin", "apply")
    new = matrix.read_text(encoding="utf-8")
    changed = [(a, b) for a, b in zip(old.splitlines(), new.splitlines()) if a != b]
    check("only the unchanged pins moved", [b for _, b in changed], [
        f"- S1: https://a.test/ — page (silo: `data/x/a.md@{c2[:10]}`, captured 2026-09-01)",
        f"- S3: https://c.test/ (silo: `data/x/c.md@{c2[:10]}`)"])
    after = hashes(repo)
    check("apply writes only the matrix", sorted(k for k in after if after[k] != before.get(k)),
          ["products/p/features/f/feature-matrix.md"])
    check("silo untouched", hashes(silo), silo_before)
    pins.run(cfg, "repin", "apply")
    check("second apply is a no-op", hashes(repo), after)


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
