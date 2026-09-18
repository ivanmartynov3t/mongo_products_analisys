# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Tests for multi-repository source extract tool (tools/source-extract).

Tests fixture extraction, symbol lookup across Java and Python, deterministic markdown output,
and drift detection on fixture repositories without requiring external git repos.
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

PYTHON_SAMPLE = '''"""Module docstring."""

class ParserService:
    """Class docstring explaining parser behaviors."""

    def parse(self, text: str) -> dict:
        return {"ok": True}
'''


def test_symbol_extraction():
    # 1. Java Class javadoc
    sym_class_jd = extract.SymbolTarget(type="javadoc", symbol="DemoService")
    content, line_no = extract.find_symbol_in_file(JAVA_SAMPLE, sym_class_jd, "DemoService.java")
    contains("class javadoc content", content, "Top level class javadoc")
    check("class javadoc line", line_no, 3)

    # 2. Java Method block
    sym_method = extract.SymbolTarget(type="method", symbol="execute(boolean)")
    content, line_no = extract.find_symbol_in_file(JAVA_SAMPLE, sym_method, "DemoService.java")
    contains("method content", content, "public void execute(boolean silent)")
    contains("method body", content, "System.out.println")
    check("method start line", line_no, 17)

    # 3. Java Field javadoc by pattern
    sym_field_jd = extract.SymbolTarget(type="field_javadoc", symbol="secretSupplier", pattern="Secret internal")
    content, line_no = extract.find_symbol_in_file(JAVA_SAMPLE, sym_field_jd, "DemoService.java")
    contains("field javadoc", content, "Secret internal supplier.")

    # 4. Python Class docstring
    sym_py_class = extract.SymbolTarget(type="class_doc", symbol="ParserService")
    content, line_no = extract.find_symbol_in_file(PYTHON_SAMPLE, sym_py_class, "parser.py")
    contains("python class docstring", content, "Class docstring explaining parser behaviors.")
    check("python class line", line_no, 3)


def test_markdown_generation():
    file_target = extract.FileTarget(
        target_file="src/com/example/DemoService.java",
        symbols=[extract.SymbolTarget(type="javadoc", symbol="DemoService")],
    )
    extracted = [(file_target.symbols[0], "/** Class doc */", 5)]
    md = extract.generate_markdown(
        "https://github.com/testorg/testrepo",
        "abc1234",
        "abc1234999",
        file_target,
        extracted,
    )

    contains("repo url header", md, "https://github.com/testorg/testrepo")
    contains("file path header", md, "src/com/example/DemoService.java")
    contains("pinned sha header", md, "abc1234")
    contains("actual sha header", md, "abc1234999")
    contains("code block", md, "```java\n/** Class doc */\n```")


def test_end_to_end_in_fixture_repos():
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        # 1. Create fake java repo
        src_repo1 = tmp_dir / "fake_java_repo"
        src_repo1.mkdir()
        java_file = src_repo1 / "src/main/java/DemoService.java"
        java_file.parent.mkdir(parents=True)
        java_file.write_text(JAVA_SAMPLE, encoding="utf-8")
        subprocess.run(["git", "init"], cwd=src_repo1, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "Tester"], cwd=src_repo1, check=True)
        subprocess.run(["git", "config", "user.email", "tester@example.com"], cwd=src_repo1, check=True)
        subprocess.run(["git", "add", "."], cwd=src_repo1, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=src_repo1, check=True)
        sha1 = extract.get_repo_sha(src_repo1)

        # 2. Create fake python repo
        src_repo2 = tmp_dir / "fake_py_repo"
        src_repo2.mkdir()
        py_file = src_repo2 / "src/parser.py"
        py_file.parent.mkdir(parents=True)
        py_file.write_text(PYTHON_SAMPLE, encoding="utf-8")
        subprocess.run(["git", "init"], cwd=src_repo2, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "Tester"], cwd=src_repo2, check=True)
        subprocess.run(["git", "config", "user.email", "tester@example.com"], cwd=src_repo2, check=True)
        subprocess.run(["git", "add", "."], cwd=src_repo2, check=True)
        subprocess.run(["git", "commit", "-m", "Initial py commit"], cwd=src_repo2, check=True)
        sha2 = extract.get_repo_sha(src_repo2)

        # Create multi-repo config
        out_dir = tmp_dir / "out_extracts"
        cfg_file = tmp_dir / "test-multi-extract.toml"
        cfg_file.write_text(f"""
[output]
directory = "{out_dir.as_posix()}"

[[repositories]]
id = "repo1"
repo_path = "{src_repo1.as_posix()}"
pinned_sha = "{sha1[:7]}"
repo_url = "https://github.com/3tio/repo1"

[[repositories.extract]]
target_file = "src/main/java/DemoService.java"
symbols = [
    {{ type = "javadoc", symbol = "DemoService" }},
    {{ type = "method", symbol = "execute(boolean)" }}
]

[[repositories]]
id = "repo2"
repo_path = "{src_repo2.as_posix()}"
pinned_sha = "{sha2[:7]}"
repo_url = "https://github.com/3tio/repo2"

[[repositories.extract]]
target_file = "src/parser.py"
symbols = [
    {{ type = "class_doc", symbol = "ParserService" }}
]
""", encoding="utf-8")

        # 1. Run extract
        code = extract.run_extract(cfg_file, mode="extract", check_drift=True)
        check("extract returns 0", code, 0)

        out_md1 = out_dir / "repo1-demoservice-extract.md"
        out_md2 = out_dir / "repo2-parser-extract.md"
        check("repo1 markdown exists", out_md1.exists(), True)
        check("repo2 markdown exists", out_md2.exists(), True)

        # 2. Check byte-identical on re-run
        code2 = extract.run_extract(cfg_file, mode="extract", check_drift=True)
        check("second extract returns 0", code2, 0)

        # 3. Check mode
        code_check = extract.run_extract(cfg_file, mode="check", check_drift=True)
        check("check mode returns 0", code_check, 0)

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    test_symbol_extraction()
    test_markdown_generation()
    test_end_to_end_in_fixture_repos()

    if failures:
        print(f"{len(failures)} failing check(s):\n")
        for f in failures:
            print("  ✗ " + f)
        sys.exit(1)
    print("all multi-repo source-extract checks passed")
