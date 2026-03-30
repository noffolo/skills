#!/usr/bin/env python3
"""
autoresearch_evolve.py — Update SOUL.md champion block after a KEEP verdict.

Karpathy's autoresearch pattern: when an experiment beats the baseline,
the mutation becomes the new champion. This script atomically updates the
AUTO:CHAMPION block in SOUL.md with the new strategy version.

Usage:
    python3 autoresearch_evolve.py SOUL.md \\
        --version 3 \\
        --change "storytelling hooks" \\
        --experiment EXP-003 \\
        --metric-delta "+18%"

    python3 autoresearch_evolve.py SOUL.md \\
        --version 3 \\
        --variable hook_style \\
        --old-value "Question-based opening" \\
        --new-value "Storytelling opening" \\
        --change "storytelling hooks" \\
        --experiment EXP-003 \\
        --metric-delta "+18%" \\
        --baseline 1450

    python3 autoresearch_evolve.py MEMORY.md \\
        --memory-mode \\
        --learning "Storytelling hooks: +18% views vs question hooks (EXP-003, 2025-01-17)" \\
        --section works

Standalone Python 3, no external dependencies.
Implements atomic read-modify-write with backup.
"""

import argparse
import os
import re
import shutil
import sys
from datetime import datetime


# ── Marker patterns ──────────────────────────────────────────────

CHAMPION_START_RE = re.compile(
    r"(<!-- AUTO:CHAMPION START v?)(\d+)(\s*-->)"
)
CHAMPION_END = "<!-- AUTO:CHAMPION END -->"

MEMORY_START = "<!-- AUTO:MEMORY START -->"
MEMORY_END = "<!-- AUTO:MEMORY END -->"

MAX_CHANGELOG_ENTRIES = 10
MAX_MEMORY_ENTRIES = 20


def read_file(path: str) -> str:
    """Read file content."""
    with open(path, "r") as f:
        return f.read()


def write_file_atomic(path: str, content: str) -> None:
    """
    Write file atomically: write to .tmp, then rename.
    Creates a .bak backup of the original.
    """
    backup_path = path + ".bak"
    tmp_path = path + ".tmp"

    # Backup original
    if os.path.exists(path):
        shutil.copy2(path, backup_path)

    # Write to temp file
    with open(tmp_path, "w") as f:
        f.write(content)

    # Atomic rename
    os.rename(tmp_path, path)


def find_markers(content: str, start_marker: str, end_marker: str) -> tuple:
    """
    Find the start and end positions of a marker block.
    Returns (start_pos, end_pos) of the entire block including markers.
    Returns (None, None) if not found.
    """
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return None, None

    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        return None, None

    return start_idx, end_idx + len(end_marker)


def update_champion_block(
    content: str,
    new_version: int,
    variable: str,
    old_value: str,
    new_value: str,
    change_desc: str,
    experiment_id: str,
    metric_delta: str,
    new_baseline: float = None,
) -> str:
    """
    Update the AUTO:CHAMPION block in SOUL.md content.

    Strategy:
    1. Find the block between markers
    2. Update version number in the start marker
    3. If variable/old_value/new_value provided: swap the strategy line
    4. Add changelog entry
    5. Update baseline if provided
    6. Update version in the title line
    """
    # Find existing champion block
    match = CHAMPION_START_RE.search(content)
    if not match:
        print("Error: AUTO:CHAMPION START marker not found in file.", file=sys.stderr)
        sys.exit(1)

    end_idx = content.find(CHAMPION_END)
    if end_idx == -1:
        print("Error: AUTO:CHAMPION END marker not found in file.", file=sys.stderr)
        sys.exit(1)

    # Extract the block content (between markers)
    block_start = match.end()
    block_content = content[block_start:end_idx]

    # 1. Update version in start marker
    new_start_marker = f"{match.group(1)}{new_version}{match.group(3)}"

    # 2. Update version in the title line (e.g., "## Content Strategy (Champion v2)")
    block_content = re.sub(
        r"(Champion v)\d+",
        f"\\g<1>{new_version}",
        block_content,
    )

    # 3. Swap strategy line if variable details provided
    if old_value and new_value:
        # Replace the old value with new value in the strategy section
        block_content = block_content.replace(old_value, new_value)

    # 4. Update baseline if provided
    if new_baseline is not None:
        block_content = re.sub(
            r"(\*\*Baseline:\*\*\s*)[\d.]+(\s*avg)",
            f"\\g<1>{new_baseline:.0f}\\2",
            block_content,
        )

    # 5. Add changelog entry
    new_entry = f"- v{new_version}: {change_desc} ({metric_delta}, {experiment_id})"

    # Find the changelog section
    changelog_match = re.search(r"\*\*Changelog:\*\*\n", block_content)
    if changelog_match:
        insert_pos = changelog_match.end()
        # Insert new entry at the top of changelog
        block_content = (
            block_content[:insert_pos]
            + new_entry
            + "\n"
            + block_content[insert_pos:]
        )

        # Trim changelog to max entries
        changelog_start = insert_pos
        lines = block_content[changelog_start:].split("\n")
        changelog_lines = []
        other_lines = []
        in_changelog = True
        for line in lines:
            if in_changelog and line.startswith("- v"):
                changelog_lines.append(line)
            else:
                in_changelog = False
                other_lines.append(line)

        if len(changelog_lines) > MAX_CHANGELOG_ENTRIES:
            changelog_lines = changelog_lines[:MAX_CHANGELOG_ENTRIES]

        block_content = (
            block_content[:changelog_start]
            + "\n".join(changelog_lines)
            + "\n"
            + "\n".join(other_lines)
        )
    else:
        # No changelog section — add one before the end
        block_content = block_content.rstrip() + f"\n**Changelog:**\n{new_entry}\n"

    # Reconstruct the full content
    new_content = (
        content[: match.start()]
        + new_start_marker
        + block_content
        + CHAMPION_END
        + content[end_idx + len(CHAMPION_END) :]
    )

    return new_content


def update_memory_block(
    content: str,
    learning: str,
    section: str = "works",
) -> str:
    """
    Update the AUTO:MEMORY block in MEMORY.md content.

    Adds a learning entry to the appropriate section:
    - "works": ### What Works
    - "fails": ### What Doesn't Work
    - "observation": ### Observations
    """
    start_idx = content.find(MEMORY_START)
    end_idx = content.find(MEMORY_END)

    if start_idx == -1 or end_idx == -1:
        # Create the block if it doesn't exist
        memory_block = f"""
{MEMORY_START}
## Autoresearch Learnings

### What Works

### What Doesn't Work

### Observations (not yet tested)

**Stats:** 0 experiments | 0 keeps | 0 kills | 0 modifies | Champion v1
{MEMORY_END}
"""
        content = content.rstrip() + "\n" + memory_block
        start_idx = content.find(MEMORY_START)
        end_idx = content.find(MEMORY_END)

    block_start = start_idx + len(MEMORY_START)
    block_content = content[block_start:end_idx]

    # Determine target section header
    section_headers = {
        "works": "### What Works",
        "fails": "### What Doesn't Work",
        "observation": "### Observations",
    }
    target_header = section_headers.get(section, "### What Works")

    # Find the target section and insert the learning after its header
    header_idx = block_content.find(target_header)
    if header_idx == -1:
        # Section doesn't exist, add it
        block_content = block_content.rstrip() + f"\n\n{target_header}\n- {learning}\n"
    else:
        insert_pos = header_idx + len(target_header)
        # Skip any trailing whitespace/newline after header
        while insert_pos < len(block_content) and block_content[insert_pos] in "\r\n":
            insert_pos += 1
        block_content = (
            block_content[:insert_pos]
            + f"- {learning}\n"
            + block_content[insert_pos:]
        )

    # Count total entries and prune if needed
    entry_lines = [l for l in block_content.split("\n") if l.strip().startswith("- ") and not l.strip().startswith("- **")]
    if len(entry_lines) > MAX_MEMORY_ENTRIES:
        print(
            f"Warning: {len(entry_lines)} entries exceed max {MAX_MEMORY_ENTRIES}. "
            f"Consider archiving oldest entries.",
            file=sys.stderr,
        )

    # Reconstruct
    new_content = (
        content[:block_start]
        + block_content
        + content[end_idx:]
    )

    return new_content


def main():
    parser = argparse.ArgumentParser(
        description="Update SOUL.md champion block or MEMORY.md after autoresearch verdict."
    )
    parser.add_argument(
        "file",
        help="Path to SOUL.md or MEMORY.md to update",
    )

    # Champion mode args
    parser.add_argument(
        "--version",
        type=int,
        help="New champion version number",
    )
    parser.add_argument(
        "--variable",
        type=str,
        help="Strategy variable that changed (e.g., hook_style)",
    )
    parser.add_argument(
        "--old-value",
        type=str,
        help="Old value to replace in strategy",
    )
    parser.add_argument(
        "--new-value",
        type=str,
        help="New value to insert in strategy",
    )
    parser.add_argument(
        "--change",
        type=str,
        help="Short description of the change for changelog",
    )
    parser.add_argument(
        "--experiment",
        type=str,
        help="Experiment ID (e.g., EXP-003)",
    )
    parser.add_argument(
        "--metric-delta",
        type=str,
        help='Metric improvement string (e.g., "+18%%")',
    )
    parser.add_argument(
        "--baseline",
        type=float,
        default=None,
        help="New baseline value to set",
    )

    # Memory mode args
    parser.add_argument(
        "--memory-mode",
        action="store_true",
        help="Operate on AUTO:MEMORY block instead of AUTO:CHAMPION",
    )
    parser.add_argument(
        "--learning",
        type=str,
        help="Learning entry to add to memory",
    )
    parser.add_argument(
        "--section",
        type=str,
        choices=["works", "fails", "observation"],
        default="works",
        help="Memory section to add learning to",
    )

    # General args
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the updated content without writing to file",
    )

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    content = read_file(args.file)

    if args.memory_mode:
        # Memory mode
        if not args.learning:
            print("Error: --learning is required in memory mode.", file=sys.stderr)
            sys.exit(1)

        new_content = update_memory_block(content, args.learning, args.section)
        action_desc = f"Added learning to {args.section} section"

    else:
        # Champion mode
        if not all([args.version, args.change, args.experiment, args.metric_delta]):
            print(
                "Error: --version, --change, --experiment, and --metric-delta "
                "are required for champion mode.",
                file=sys.stderr,
            )
            sys.exit(1)

        new_content = update_champion_block(
            content=content,
            new_version=args.version,
            variable=args.variable or "",
            old_value=args.old_value or "",
            new_value=args.new_value or "",
            change_desc=args.change,
            experiment_id=args.experiment,
            metric_delta=args.metric_delta,
            new_baseline=args.baseline,
        )
        action_desc = f"Updated champion to v{args.version}"

    if args.dry_run:
        print("=== DRY RUN — would write: ===")
        print(new_content)
    else:
        write_file_atomic(args.file, new_content)
        print(f"✓ {action_desc}")
        print(f"  File: {args.file}")
        if not args.memory_mode:
            print(f"  Version: v{args.version}")
            print(f"  Change: {args.change} ({args.metric_delta}, {args.experiment})")
        else:
            print(f"  Section: {args.section}")
            print(f"  Learning: {args.learning}")
        print(f"  Backup: {args.file}.bak")


if __name__ == "__main__":
    main()
