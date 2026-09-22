#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
One-shot migration script for Issue #13:
Add '## Feature metadata' section with review dates to all 72 feature-matrix.md files.

Usage:
    python normalize.py --dry-run     # Preview changes without writing
    python normalize.py               # Apply changes in-place

The script detects three format variants:
  A) Studio 3T: has '**Last reviewed:**' line, no '## Feature metadata'
  B) Plan 4 competitors: already has '## Feature metadata' with '- Analysis date:'
  C) Undated: no date, no metadata section (Compass, VisuaLeaf, 3T non-Desktop)
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Git-derived dates for undated files (from: git log -1 --format='%aI' -- <file>)
GIT_DATES: dict[str, str] = {
    # MongoDB Compass
    "products/third-party/mongodb-compass/features/aggregation/feature-matrix.md": "2026-06-22",
    "products/third-party/mongodb-compass/features/ai/feature-matrix.md": "2026-07-28",
    "products/third-party/mongodb-compass/features/connectivity/feature-matrix.md": "2026-06-22",
    "products/third-party/mongodb-compass/features/governance/feature-matrix.md": "2026-06-22",
    "products/third-party/mongodb-compass/features/indexing-performance/feature-matrix.md": "2026-06-22",
    "products/third-party/mongodb-compass/features/querying/feature-matrix.md": "2026-06-22",
    "products/third-party/mongodb-compass/features/schema/feature-matrix.md": "2026-06-22",
    # VisuaLeaf
    "products/third-party/visual-eaf/features/aggregation/feature-matrix.md": "2026-07-28",
    "products/third-party/visual-eaf/features/ai/feature-matrix.md": "2026-06-22",
    "products/third-party/visual-eaf/features/connectivity/feature-matrix.md": "2026-06-22",
    "products/third-party/visual-eaf/features/data-transfer/feature-matrix.md": "2026-07-28",
    "products/third-party/visual-eaf/features/governance/feature-matrix.md": "2026-06-22",
    "products/third-party/visual-eaf/features/indexing-performance/feature-matrix.md": "2026-06-22",
    "products/third-party/visual-eaf/features/querying/feature-matrix.md": "2026-07-28",
    "products/third-party/visual-eaf/features/schema/feature-matrix.md": "2026-06-22",
    "products/third-party/visual-eaf/features/shell/feature-matrix.md": "2026-06-22",
    "products/third-party/visual-eaf/features/sql-tools/feature-matrix.md": "2026-07-28",
    "products/third-party/visual-eaf/features/task-scheduler/feature-matrix.md": "2026-06-22",
    # 3T non-Desktop
    "products/3t/3t-explore/features/ai/feature-matrix.md": "2026-07-29",
    "products/3t/3t-explore/features/governance/feature-matrix.md": "2026-07-29",
    "products/3t/3t-mcp/features/ai/feature-matrix.md": "2026-07-29",
    "products/3t/3tl-bridge/features/governance/feature-matrix.md": "2026-07-29",
    "products/3t/3t-lens/features/governance/feature-matrix.md": "2026-07-29",
    "products/3t/3t-access/features/governance/feature-matrix.md": "2026-07-29",
}

# Product name lookup from directory path
PRODUCT_NAMES: dict[str, str] = {
    "studio-3t": "Studio 3T",
    "3t-explore": "3T Explore",
    "3t-mcp": "3T MCP",
    "3tl-bridge": "3TL Bridge",
    "3t-lens": "3T Lens",
    "3t-access": "3T Access",
    "mongodb-compass": "MongoDB Compass",
    "visual-eaf": "VisuaLeaf",
    "nosqlbooster": "NoSQLBooster",
    "dbeaver": "DBeaver",
    "datagrip": "DataGrip",
    "navicat": "Navicat",
    "tableplus": "TablePlus",
}

# Feature ID lookup from directory name
FEATURE_IDS: dict[str, str] = {
    "connectivity": "F-CONN",
    "querying": "F-QUERY",
    "aggregation": "F-AGG",
    "schema": "F-SCHEMA",
    "indexing-performance": "F-IDX",
    "data-transfer": "F-TRANSFER",
    "shell": "F-SHELL",
    "ai": "F-AI",
    "sql-tools": "F-SQL",
    "governance": "F-GOV",
    "task-scheduler": "F-SCHED",
}


def detect_variant(content: str) -> str:
    """Detect which format variant a file uses."""
    if "## Feature metadata" in content:
        return "plan4"  # Already has metadata section
    if "**Last reviewed:**" in content:
        return "studio3t"
    return "undated"


def extract_product_info(rel_path: str) -> tuple[str, str, str, str]:
    """Extract product name, group, feature ID, and folder from path."""
    parts = Path(rel_path).parts
    # products/<group>/<product>/features/<feature>/feature-matrix.md
    group = parts[1]  # 'third-party' or '3t'
    product_slug = parts[2]
    feature_folder = parts[4]

    product_name = PRODUCT_NAMES.get(product_slug, product_slug)
    product_group = group
    feature_id = FEATURE_IDS.get(feature_folder, f"F-{feature_folder.upper()}")

    return product_name, product_group, feature_id, feature_folder


def build_metadata_block(
    product_name: str,
    product_group: str,
    feature_id: str,
    feature_folder: str,
    analysis_date: str,
    version_context: str = "—",
) -> str:
    """Build a ## Feature metadata section."""
    return (
        f"## Feature metadata\n"
        f"\n"
        f"- Product name: {product_name}\n"
        f"- Product group: {product_group}\n"
        f"- Feature ID: {feature_id} (see [feature-dictionary.md](../../../../../feature-dictionary.md))\n"
        f"- Feature folder: `{feature_folder}`\n"
        f"- Analysis date: {analysis_date}\n"
        f"- Version/release context: {version_context}\n"
    )


def migrate_studio3t(content: str, rel_path: str) -> str:
    """Migrate Studio 3T variant: extract date from **Last reviewed:** and insert metadata."""
    product_name, product_group, feature_id, feature_folder = extract_product_info(rel_path)

    # Extract date from **Last reviewed:** line
    date_match = re.search(r"\*\*Last reviewed:\*\*\s+(\d{4}-\d{2}-\d{2})", content)
    if not date_match:
        print(f"  WARNING: Could not extract date from {rel_path}", file=sys.stderr)
        return content
    analysis_date = date_match.group(1)

    # Extract version context from the **Last reviewed:** line if present
    reviewed_line_match = re.search(r"^\*\*Last reviewed:\*\*.*$", content, re.MULTILINE)
    reviewed_line = reviewed_line_match.group(0) if reviewed_line_match else ""

    # Build metadata block
    metadata = build_metadata_block(
        product_name, product_group, feature_id, feature_folder, analysis_date
    )

    # Remove the **Last reviewed:** line (and surrounding blank lines)
    content = re.sub(
        r"\n*\*\*Last reviewed:\*\*[^\n]*\n*",
        "\n\n",
        content,
    )

    # Insert metadata section before ## Source index
    content = content.replace(
        "## Source index",
        f"{metadata}\n## Source index",
    )

    return content


def migrate_undated(content: str, rel_path: str) -> str:
    """Migrate undated variant: insert metadata with git-derived date."""
    product_name, product_group, feature_id, feature_folder = extract_product_info(rel_path)

    analysis_date = GIT_DATES.get(rel_path)
    if not analysis_date:
        print(f"  WARNING: No git date for {rel_path}", file=sys.stderr)
        return content

    metadata = build_metadata_block(
        product_name, product_group, feature_id, feature_folder, analysis_date
    )

    # Insert metadata section before ## Source index
    content = content.replace(
        "## Source index",
        f"{metadata}\n## Source index",
    )

    return content


def find_all_matrices() -> list[Path]:
    """Find all feature-matrix.md files."""
    patterns = [
        REPO_ROOT / "products" / "*" / "features" / "*" / "feature-matrix.md",
        REPO_ROOT / "products" / "*" / "*" / "features" / "*" / "feature-matrix.md",
    ]
    results = []
    for pattern in patterns:
        import glob
        results.extend(Path(p) for p in sorted(glob.glob(str(pattern))))
    return results


def main():
    parser = argparse.ArgumentParser(description="Normalize feature-matrix.md metadata")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    args = parser.parse_args()

    matrices = find_all_matrices()
    print(f"Found {len(matrices)} feature-matrix.md files\n")

    stats = {"plan4": 0, "studio3t": 0, "undated": 0, "modified": 0, "skipped": 0}

    for matrix_path in matrices:
        rel_path = str(matrix_path.relative_to(REPO_ROOT))
        content = matrix_path.read_text()
        variant = detect_variant(content)
        stats[variant] += 1

        if variant == "plan4":
            # Already normalized
            if args.dry_run:
                print(f"  SKIP (already has metadata): {rel_path}")
            stats["skipped"] += 1
            continue

        if variant == "studio3t":
            new_content = migrate_studio3t(content, rel_path)
        elif variant == "undated":
            new_content = migrate_undated(content, rel_path)
        else:
            continue

        if new_content == content:
            print(f"  SKIP (no changes): {rel_path}")
            stats["skipped"] += 1
            continue

        if args.dry_run:
            print(f"  WOULD MODIFY: {rel_path}")
            # Show the metadata section that would be inserted
            meta_match = re.search(r"## Feature metadata\n.*?(?=\n## )", new_content, re.DOTALL)
            if meta_match:
                print(f"    + {meta_match.group(0).strip()}")
            print()
        else:
            matrix_path.write_text(new_content)
            print(f"  MODIFIED: {rel_path}")
            stats["modified"] += 1

    print(f"\n--- Summary ---")
    print(f"Total files:     {len(matrices)}")
    print(f"  plan4 (ok):    {stats['plan4']}")
    print(f"  studio3t:      {stats['studio3t']}")
    print(f"  undated:       {stats['undated']}")
    print(f"  modified:      {stats['modified']}")
    print(f"  skipped:       {stats['skipped']}")

    if args.dry_run:
        print("\n(Dry run — no files were modified)")


if __name__ == "__main__":
    main()
