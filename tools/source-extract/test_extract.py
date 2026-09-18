# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Tests for source extract tool (tools/source-extract).

Tests fixture extraction, symbol lookup, deterministic markdown output,
and drift detection on fixture repositories without requiring the external 3t.tools repo.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract  # noqa: E402

failures: list[str] = []


def check(name: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{name}\n     expected: {expected!r}\n     actual:   {actual!r}")


def contains(name: str, haystack: str, needle: str) -> None:
    if needle not in haystack:
        failures.append(f"{name}\n     missing: {needle!r}\n     in:      {haystack[:200]!r}")


# --------------------------------------------------------------------------- fixtures

JAVA_SAMPLE = """package com.example.demo;

/**
 * Top level class javadoc.
 */
public class DemoService {

    /**
     * Secret internal supplier.
     */
    private final String secretSupplier = "internal";

    /**
     * Executes the task operation.
     * Must be called on background thread.
     */
    public void execute(boolean silent) {
        System.out.println("Executing: " + silent);
    }
}
"""

PROPERTIES_SAMPLE = """# Application messages
app.title = Studio 3T Analysis
app.error.timeout = Connection timed out after {0} ms
"""


def test_symbol_extraction():
    # 1. Class javadoc
    sym_class_jd = extract.SymbolTarget(type="javadoc", symbol="DemoService")
    content, line_no = extract.find_symbol_in_java(JAVA_SAMPLE, sym_class_jd)
    contains("class javadoc content", content, "Top level class javadoc")
    check("class javadoc line", line_no, 3)

    # 2. Method block
    sym_method = extract.SymbolTarget(type="method", symbol="execute(boolean)")
    content, line_no = extract.find_symbol_in_java(JAVA_SAMPLE, sym_method)
    contains("method content", content, "public void execute(boolean silent)")
    contains("method body", content, "System.out.println")
    check("method start line", line_no, 17)

    # 3. Method javadoc
    sym_method_jd = extract.SymbolTarget(type="javadoc", symbol="execute(boolean)")
    content, line_no = extract.find_symbol_in_java(JAVA_SAMPLE, sym_method_jd)
    contains("method javadoc content", content, "Executes the task operation")
    contains("method javadoc param/return", content, "Must be called on background thread")

    # 4. Field javadoc by pattern
    sym_field_jd = extract.SymbolTarget(type="field_javadoc", symbol="secretSupplier", pattern="Secret internal")
    content, line_no = extract.find_symbol_in_java(JAVA_SAMPLE, sym_field_jd)
    contains("field javadoc", content, "Secret internal supplier.")


def test_markdown_generation():
    cfg = {
        "source": {
            "repo_url": "https://github.com/testorg/testrepo",
            "pinned_sha": "abc1234",
        }
    }
    file_target = extract.FileTarget(
        target_file="src/com/example/DemoService.java",
        symbols=[extract.SymbolTarget(type="javadoc", symbol="DemoService")],
    )
    extracted = [(file_target.symbols[0], "/** Class doc */", 5)]
    md = extract.generate_markdown(cfg, file_target, extracted, "abc1234999")

    contains("repo url header", md, "https://github.com/testorg/testrepo")
    contains("file path header", md, "src/com/example/DemoService.java")
    contains("pinned sha header", md, "abc1234")
    contains("actual sha header", md, "abc1234999")
    contains("code block", md, "```java\n/** Class doc */\n```")


def test_end_to_end_in_fixture_repo():
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        # Create fake source repo with git
        src_repo = tmp_dir / "fake_src"
        src_repo.mkdir()
        java_file = src_repo / "src/main/java/DemoService.java"
        java_file.parent.mkdir(parents=True)
        java_file.write_text(JAVA_SAMPLE, encoding="utf-8")

        subprocess.run(["git", "init"], cwd=src_repo, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "Tester"], cwd=src_repo, check=True)
        subprocess.run(["git", "config", "user.email", "tester@example.com"], cwd=src_repo, check=True)
        subprocess.run(["git", "add", "."], cwd=src_repo, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=src_repo, check=True)
        sha = extract.get_repo_sha(src_repo)

        # Create config
        out_dir = tmp_dir / "out_extracts"
        cfg_file = tmp_dir / "test-extract.toml"
        cfg_file.write_text(f"""
[source]
repo_path = "{src_repo.as_posix()}"
pinned_sha = "{sha[:7]}"
repo_url = "https://github.com/3tio/3t.tools"

[output]
directory = "{out_dir.as_posix()}"

[[extract]]
target_file = "src/main/java/DemoService.java"
symbols = [
    {{ type = "javadoc", symbol = "DemoService" }},
    {{ type = "method", symbol = "execute(boolean)" }}
]
""", encoding="utf-8")

        # 1. Run extract
        code = extract.run_extract(cfg_file, mode="extract", check_drift=True)
        check("extract returns 0", code, 0)

        out_md = out_dir / "demoservice-extract.md"
        check("output markdown exists", out_md.exists(), True)

        first_content = out_md.read_text(encoding="utf-8")
        contains("symbol heading", first_content, "### Symbol: `DemoService` (javadoc)")
        contains("method heading", first_content, "### Symbol: `execute(boolean)` (method)")

        # 2. Check byte-identical on re-run
        code2 = extract.run_extract(cfg_file, mode="extract", check_drift=True)
        check("second extract returns 0", code2, 0)
        second_content = out_md.read_text(encoding="utf-8")
        check("output is byte-identical", first_content, second_content)

        # 3. Check mode
        code_check = extract.run_extract(cfg_file, mode="check", check_drift=True)
        check("check mode returns 0", code_check, 0)

        # 4. Check drift detection on SHA mismatch
        cfg_drift = tmp_dir / "test-drift.toml"
        cfg_drift.write_text(f"""
[source]
repo_path = "{src_repo.as_posix()}"
pinned_sha = "deadbeef123"
repo_url = "https://github.com/3tio/3t.tools"

[output]
directory = "{out_dir.as_posix()}"

[[extract]]
target_file = "src/main/java/DemoService.java"
symbols = [{{ type = "javadoc", symbol = "DemoService" }}]
""", encoding="utf-8")
        drift_code = extract.run_extract(cfg_drift, mode="check", check_drift=True)
        check("drift detection returns 3 on SHA mismatch", drift_code, 3)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    test_symbol_extraction()
    test_markdown_generation()
    test_end_to_end_in_fixture_repo()

    if failures:
        print(f"{len(failures)} failing check(s):\n")
        for f in failures:
            print("  ✗ " + f)
        sys.exit(1)
    print("all source-extract checks passed")
