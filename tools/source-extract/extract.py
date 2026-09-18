# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "tree-sitter>=0.23",
#     "tree-sitter-java>=0.23",
# ]
# ///
"""Deterministic source extract tool for 3t.tools source references.

Extracts javadocs, method declarations, and code snippets from Java and properties files
without publishing whole trees or absolute local paths.
Outputs committed markdown files under research/source-extracts/ stamped with commit SHA.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SymbolTarget:
    type: str
    symbol: str
    line_hint: int | None = None
    pattern: str | None = None


@dataclass
class FileTarget:
    target_file: str
    symbols: list[SymbolTarget]


def get_repo_sha(repo_path: Path) -> str:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        return res.stdout.strip()
    except Exception as exc:
        raise RuntimeError(f"Failed to read git HEAD from {repo_path}: {exc}") from exc


def extract_javadoc_preceding(lines: list[str], start_idx: int) -> tuple[str, int] | None:
    """Walk upwards from start_idx to find the preceding javadoc comment block and start line."""
    idx = start_idx - 1
    # Skip annotations and blank lines
    while idx >= 0:
        line = lines[idx].strip()
        if not line or line.startswith("@"):
            idx -= 1
            continue
        break

    if idx >= 0 and lines[idx].strip().endswith("*/"):
        end_comment_idx = idx
        while idx >= 0:
            if "/**" in lines[idx]:
                return "\n".join(lines[idx : end_comment_idx + 1]), idx + 1
            idx -= 1
    return None


def extract_method_block(lines: list[str], start_idx: int) -> str:
    """Extract full method block starting at signature until closing brace."""
    out = []
    brace_depth = 0
    started = False
    for line in lines[start_idx:]:
        out.append(line)
        for char in line:
            if char == "{":
                brace_depth += 1
                started = True
            elif char == "}":
                brace_depth -= 1
                if started and brace_depth == 0:
                    return "\n".join(out)
    return "\n".join(out)


def find_symbol_in_java(file_content: str, sym: SymbolTarget) -> tuple[str, int]:
    """Locate symbol content and starting line (1-indexed)."""
    lines = file_content.splitlines()

    # If pattern is provided, search by pattern match
    if sym.pattern:
        for idx, line in enumerate(lines):
            if sym.pattern in line:
                if sym.type == "field_javadoc" or sym.type == "javadoc":
                    # If pattern matched inside the comment
                    if "/**" in line or line.strip().startswith("*"):
                        # Find start /**
                        start_c = idx
                        while start_c >= 0 and "/**" not in lines[start_c]:
                            start_c -= 1
                        # Find end */
                        end_c = idx
                        while end_c < len(lines) and "*/" not in lines[end_c]:
                            end_c += 1
                        return "\n".join(lines[start_c : end_c + 1]), start_c + 1
                    jd_res = extract_javadoc_preceding(lines, idx)
                    if jd_res:
                        return jd_res
                return line.strip(), idx + 1

    # Search by symbol name
    bare_sym = sym.symbol.split("(")[0].strip()
    for idx, line in enumerate(lines):
        # Class javadoc
        if sym.type == "javadoc" and f"class {sym.symbol}" in line:
            jd_res = extract_javadoc_preceding(lines, idx)
            if jd_res:
                return jd_res
        # Method declaration or method javadoc
        if (bare_sym in line) and any(kw in line for kw in ("public ", "protected ", "private ", "void ", sym.symbol)):
            if sym.type == "javadoc":
                jd_res = extract_javadoc_preceding(lines, idx)
                if jd_res:
                    return jd_res
            elif sym.type == "method":
                return extract_method_block(lines, idx), idx + 1

    # Fallback to line_hint if provided
    if sym.line_hint and 0 < sym.line_hint <= len(lines):
        line = lines[sym.line_hint - 1]
        return line.strip(), sym.line_hint

    return f"// Symbol {sym.symbol} not found", 0


def generate_markdown(
    cfg: dict,
    file_target: FileTarget,
    extracted_symbols: list[tuple[SymbolTarget, str, int]],
    actual_sha: str,
) -> str:
    source_cfg = cfg.get("source", {})
    repo_url = source_cfg.get("repo_url", "https://github.com/3tio/3t.tools")
    pinned_sha = source_cfg.get("pinned_sha", actual_sha[:11])
    target_path = file_target.target_file

    lines = [
        f"# Source Extract: `{Path(target_path).name}`",
        "",
        "| Attribute | Value |",
        "| --- | --- |",
        f"| **Source Repository** | `{repo_url}` |",
        f"| **File Path** | `{target_path}` |",
        f"| **Pinned Revision** | `{pinned_sha}` |",
        f"| **Extracted At SHA** | `{actual_sha}` |",
        "",
        "## Extracted Symbols & Citations",
        "",
    ]

    for sym, content, line_no in extracted_symbols:
        lines.append(f"### Symbol: `{sym.symbol}` ({sym.type})")
        if line_no > 0:
            lines.append(f"**Origin Line (Audited Baseline):** `{line_no}`")
        lines.append("")
        lines.append("```java")
        lines.append(content.rstrip())
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def run_extract(config_path: Path, mode: str = "extract", check_drift: bool = False) -> int:
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        return 1

    with open(config_path, "rb") as f:
        cfg = tomllib.load(f)

    source_cfg = cfg.get("source", {})
    repo_path_env = os.environ.get("SOURCE_EXTRACT_REPO_PATH")
    repo_path = Path(repo_path_env or source_cfg.get("repo_path", "")).resolve()

    if not repo_path.exists() or not (repo_path / ".git").exists():
        print(f"Error: Source repository path not found: {repo_path}", file=sys.stderr)
        return 2

    actual_sha = get_repo_sha(repo_path)
    pinned_sha = source_cfg.get("pinned_sha", "")

    print(f"Source repository: {repo_path}")
    print(f"Current SHA:       {actual_sha}")
    print(f"Pinned SHA:        {pinned_sha}")

    if check_drift and pinned_sha:
        if not actual_sha.startswith(pinned_sha) and not pinned_sha.startswith(actual_sha):
            print(
                f"DRIFT DETECTED: Target repository HEAD ({actual_sha}) does not match pinned SHA ({pinned_sha})!",
                file=sys.stderr,
            )
            return 3

    output_dir = Path(cfg.get("output", {}).get("directory", "research/source-extracts"))
    if not output_dir.is_absolute():
        repo_root = config_path.resolve().parent.parent.parent
        output_dir = repo_root / output_dir

    targets = []
    for t in cfg.get("extract", []):
        symbols = [SymbolTarget(**s) for s in t.get("symbols", [])]
        targets.append(FileTarget(target_file=t["target_file"], symbols=symbols))

    drift_found = False

    for target in targets:
        full_src = repo_path / target.target_file
        if not full_src.exists():
            print(f"Warning: Source file not found: {full_src}", file=sys.stderr)
            continue

        file_content = full_src.read_text(encoding="utf-8", errors="replace")
        extracted_symbols = []
        for sym in target.symbols:
            content, line_no = find_symbol_in_java(file_content, sym)
            extracted_symbols.append((sym, content, line_no))

        md_content = generate_markdown(cfg, target, extracted_symbols, actual_sha)

        slug = Path(target.target_file).stem.lower().replace("_", "-")
        out_file = output_dir / f"{slug}-extract.md"

        if mode == "plan":
            print(f"[plan] Would write {out_file.relative_to(output_dir.parent.parent)} ({len(extracted_symbols)} symbols)")
        elif mode == "extract":
            output_dir.mkdir(parents=True, exist_ok=True)
            existing = out_file.read_text(encoding="utf-8") if out_file.exists() else None
            if existing != md_content:
                out_file.write_text(md_content, encoding="utf-8")
                print(f"[updated] Wrote {out_file}")
            else:
                print(f"[unchanged] {out_file}")
        elif mode == "check":
            if not out_file.exists():
                print(f"Missing extract file: {out_file}", file=sys.stderr)
                drift_found = True
            else:
                existing = out_file.read_text(encoding="utf-8")
                if existing != md_content:
                    print(f"Extract drift detected in {out_file}!", file=sys.stderr)
                    drift_found = True

    if mode == "check" and drift_found:
        return 4

    print("Source extraction completed successfully.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Extract source comments and symbols from 3t.tools")
    parser.add_argument("mode", choices=["plan", "extract", "check"], default="extract", nargs="?")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parent / "source-extract.toml",
        help="Path to source-extract.toml",
    )
    parser.add_argument("--check-drift", action="store_true", help="Fail if current commit SHA differs from pinned SHA")
    args = parser.parse_args()

    sys.exit(run_extract(args.config, mode=args.mode, check_drift=args.check_drift))


if __name__ == "__main__":
    main()
