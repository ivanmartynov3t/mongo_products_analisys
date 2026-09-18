# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "tree-sitter>=0.23",
#     "tree-sitter-java>=0.23",
# ]
# ///
"""Deterministic source extract tool for multi-repository evidence.

Extracts javadocs, docstrings, method declarations, and code snippets from source files
across repositories without publishing whole trees or absolute local paths.
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


@dataclass
class RepoTarget:
    id: str
    repo_path: Path
    repo_url: str
    pinned_sha: str
    extracts: list[FileTarget]


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
    """Walk upwards from start_idx to find preceding javadoc comment block and its start line."""
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
    """Extract full block starting at signature until closing brace."""
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


def find_symbol_in_file(file_content: str, sym: SymbolTarget, file_path: str) -> tuple[str, int]:
    """Locate symbol content and starting line (1-indexed) in Java or Python files."""
    lines = file_content.splitlines()
    is_python = file_path.endswith(".py")

    # If pattern is provided, search by pattern match
    if sym.pattern:
        for idx, line in enumerate(lines):
            if sym.pattern in line:
                if sym.type in ("field_javadoc", "javadoc"):
                    if "/**" in line or line.strip().startswith("*"):
                        start_c = idx
                        while start_c >= 0 and "/**" not in lines[start_c]:
                            start_c -= 1
                        end_c = idx
                        while end_c < len(lines) and "*/" not in lines[end_c]:
                            end_c += 1
                        return "\n".join(lines[start_c : end_c + 1]), start_c + 1
                    jd_res = extract_javadoc_preceding(lines, idx)
                    if jd_res:
                        return jd_res
                return line.strip(), idx + 1

    bare_sym = sym.symbol.split("(")[0].strip()

    for idx, line in enumerate(lines):
        # Class doc / declaration
        if sym.type in ("class_doc", "javadoc") and f"class {bare_sym}" in line:
            if is_python:
                # Look for docstring directly below class definition
                out_lines = [line]
                j = idx + 1
                while j < len(lines) and (not lines[j].strip() or lines[j].strip().startswith("@")):
                    j += 1
                if j < len(lines) and (lines[j].strip().startswith('"""') or lines[j].strip().startswith("'''")):
                    delim = '"""' if '"""' in lines[j] else "'''"
                    start_doc = j
                    out_lines.append(lines[j])
                    if lines[j].count(delim) < 2:
                        j += 1
                        while j < len(lines):
                            out_lines.append(lines[j])
                            if delim in lines[j]:
                                break
                            j += 1
                    return "\n".join(out_lines), idx + 1
                return line.strip(), idx + 1
            else:
                jd_res = extract_javadoc_preceding(lines, idx)
                if jd_res:
                    return jd_res

        # Method / Function
        if (bare_sym in line) and any(kw in line for kw in ("public ", "protected ", "private ", "void ", "def ", "class ", sym.symbol)):
            if sym.type == "javadoc":
                jd_res = extract_javadoc_preceding(lines, idx)
                if jd_res:
                    return jd_res
            elif sym.type == "method":
                return extract_method_block(lines, idx), idx + 1
            elif sym.type == "class_doc":
                return line.strip(), idx + 1

    # Fallback to line_hint if provided
    if sym.line_hint and 0 < sym.line_hint <= len(lines):
        line = lines[sym.line_hint - 1]
        return line.strip(), sym.line_hint

    return f"// Symbol {sym.symbol} not found", 0


def generate_markdown(
    repo_url: str,
    pinned_sha: str,
    actual_sha: str,
    file_target: FileTarget,
    extracted_symbols: list[tuple[SymbolTarget, str, int]],
) -> str:
    target_path = file_target.target_file
    lang = "python" if target_path.endswith(".py") else "java"

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
        lines.append(f"```{lang}")
        lines.append(content.rstrip())
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def load_config(config_path: Path) -> tuple[Path, list[RepoTarget]]:
    with open(config_path, "rb") as f:
        cfg = tomllib.load(f)

    repo_root = config_path.resolve().parent.parent.parent
    out_dir_val = cfg.get("output", {}).get("directory", "research/source-extracts")
    output_dir = Path(out_dir_val)
    if not output_dir.is_absolute():
        output_dir = repo_root / output_dir

    repos: list[RepoTarget] = []

    # Check for multi-repository format ([[repositories]])
    if "repositories" in cfg:
        for r in cfg["repositories"]:
            repo_id = r.get("id", "default")
            path_val = r.get("repo_path", "")
            # Allow environment override per repo if needed, e.g. SOURCE_EXTRACT_REPO_PATH_3T_TOOLS
            env_var = f"SOURCE_EXTRACT_REPO_PATH_{repo_id.upper().replace('.', '_').replace('-', '_')}"
            path_str = os.environ.get(env_var, os.environ.get("SOURCE_EXTRACT_REPO_PATH", path_val))
            repo_p = Path(path_str).resolve()
            pinned = r.get("pinned_sha", "")
            url = r.get("repo_url", "")
            extracts = []
            for t in r.get("extract", []):
                symbols = [SymbolTarget(**s) for s in t.get("symbols", [])]
                extracts.append(FileTarget(target_file=t["target_file"], symbols=symbols))
            repos.append(RepoTarget(id=repo_id, repo_path=repo_p, repo_url=url, pinned_sha=pinned, extracts=extracts))
    else:
        # Legacy single repo format ([source] and [[extract]])
        src = cfg.get("source", {})
        repo_p = Path(os.environ.get("SOURCE_EXTRACT_REPO_PATH", src.get("repo_path", ""))).resolve()
        pinned = src.get("pinned_sha", "")
        url = src.get("repo_url", "")
        extracts = []
        for t in cfg.get("extract", []):
            symbols = [SymbolTarget(**s) for s in t.get("symbols", [])]
            extracts.append(FileTarget(target_file=t["target_file"], symbols=symbols))
        repos.append(RepoTarget(id="default", repo_path=repo_p, repo_url=url, pinned_sha=pinned, extracts=extracts))

    return output_dir, repos


def run_extract(config_path: Path, mode: str = "extract", check_drift: bool = False) -> int:
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        return 1

    output_dir, repos = load_config(config_path)
    drift_found = False
    missing_repo_found = False

    for repo in repos:
        print(f"\n--- Processing repository: {repo.id} ({repo.repo_path}) ---")
        if not repo.repo_path.exists() or not (repo.repo_path / ".git").exists():
            print(f"Warning: Repository path not found or not a git checkout: {repo.repo_path}", file=sys.stderr)
            missing_repo_found = True
            continue

        actual_sha = get_repo_sha(repo.repo_path)
        print(f"Current SHA: {actual_sha}")
        print(f"Pinned SHA:  {repo.pinned_sha}")

        if check_drift and repo.pinned_sha:
            if not actual_sha.startswith(repo.pinned_sha) and not repo.pinned_sha.startswith(actual_sha):
                print(
                    f"DRIFT DETECTED in {repo.id}: HEAD ({actual_sha}) does not match pinned SHA ({repo.pinned_sha})!",
                    file=sys.stderr,
                )
                drift_found = True

        for target in repo.extracts:
            full_src = repo.repo_path / target.target_file
            if not full_src.exists():
                print(f"Warning: Target file not found: {full_src}", file=sys.stderr)
                continue

            file_content = full_src.read_text(encoding="utf-8", errors="replace")
            extracted_symbols = []
            for sym in target.symbols:
                content, line_no = find_symbol_in_file(file_content, sym, target.target_file)
                extracted_symbols.append((sym, content, line_no))

            md_content = generate_markdown(
                repo.repo_url, repo.pinned_sha, actual_sha, target, extracted_symbols
            )

            # Distinguish output filenames by repo prefix if multiple repos
            prefix = f"{repo.id.replace('.', '-').replace('_', '-')}-" if len(repos) > 1 else ""
            slug = Path(target.target_file).stem.lower().replace("_", "-")
            out_file = output_dir / f"{prefix}{slug}-extract.md"

            if mode == "plan":
                print(f"[plan] Would write {out_file.name} ({len(extracted_symbols)} symbols)")
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

    if check_drift and drift_found:
        return 3
    if mode == "check" and drift_found:
        return 4
    if missing_repo_found and mode == "check":
        return 2

    print("\nSource extraction completed successfully across all repositories.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Extract source comments and symbols across repositories")
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
