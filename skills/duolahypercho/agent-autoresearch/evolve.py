#!/usr/bin/env python3
"""
evolve.py — Execute KEEP or KILL verdict for an agent self-research experiment.

After an experiment's evaluation window closes:
- KEEP:  integrate the change permanently, update champion baseline
- KILL:  revert files to pre-experiment state, discard the change

Usage:
    python3 evolve.py experiments/active.md               # KEEP verdict
    python3 evolve.py experiments/active.md --kill         # KILL verdict
    python3 evolve.py --exp-id EXP-001 --exp-avg 0.85     # explicit args
    python3 evolve.py experiments/active.md --dry-run      # preview changes

The script:
1. Parses the experiment file for the mutation and affected files
2. (KILL only) Reverts affected files from experiments/EXP-XXX/backups/
3. Updates baseline.json (version, strategy, changelog)
4. Resets or increments kill_streak in meta.json
5. Appends result to results.tsv
6. Archives the experiment
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime

EXPERIMENTS_DIR = "experiments"
ARCHIVE_DIR = f"{EXPERIMENTS_DIR}/archive"
BACKUP_DIR = f"{EXPERIMENTS_DIR}/backups"
META_FILE = f"{EXPERIMENTS_DIR}/meta.json"
BASELINE_FILE = "baseline.json"
RESULTS_FILE = "results.tsv"


def parse_experiment_file(filepath: str) -> dict:
    """Parse experiment markdown file for key fields."""
    if not os.path.exists(filepath):
        print(f"Error: Experiment file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(filepath) as f:
        content = f.read()

    exp = {"filepath": filepath, "raw": content}

    # Extract experiment ID from title
    m = re.search(r"#\s+(EXP-\d+)", content)
    exp["id"] = m.group(1) if m else None

    # Extract key fields
    field_patterns = {
        "status": r"\*\*Status:\*\*\s*(.+)",
        "variable": r"\*\*Variable:\*\*\s*(.+)",
        "mutation": r"\*\*Mutation:\*\*\s*(.+)",
        "champion_version": r"\*\*Champion Version:\*\*\s*v?(\d+)",
        "experiment_score": r"\*\*Experiment Score:\*\*\s*([\d.]+)",
        "champion_baseline": r"\*\*Champion Baseline:\*\*\s*([\d.]+)",
        "decision": r"\*\*Decision:\*\*\s*(KEEP|KILL|MODIFY)",
        "created": r"\*\*Created:\*\*\s*(\S+)",
    }
    for key, pattern in field_patterns.items():
        m = re.search(pattern, content)
        if m:
            exp[key] = m.group(1).strip()

    # Extract measurement rows from the metrics table
    measurements = []
    in_table = False
    for line in content.split("\n"):
        if "Experiment Score" in line or "Experiment |" in line:
            in_table = True
            continue
        if in_table and line.startswith("|"):
            if "---" in line:
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 2:
                try:
                    val = float(cells[1])
                    measurements.append(val)
                except (ValueError, IndexError):
                    pass
        elif in_table and not line.startswith("|"):
            in_table = False

    exp["measurements"] = measurements
    if measurements:
        exp["experiment_score"] = sum(measurements) / len(measurements)

    # Extract affected files list
    affected = []
    in_files_section = False
    for line in content.split("\n"):
        if "## What Changes" in line or "## Files Affected" in line:
            in_files_section = True
            continue
        if in_files_section and line.startswith("**Before:**"):
            continue
        if in_files_section and line.startswith("**After:**"):
            continue
        if in_files_section and line.startswith("## "):
            in_files_section = False
        if in_files_section and "- [" in line and "](" in line:
            # Extract file path from markdown checkbox line
            m = re.search(r"\]\(([^)]+)\)", line)
            if m:
                affected.append(m.group(1))

    exp["affected_files"] = affected

    return exp


def load_json(filepath: str) -> dict:
    with open(filepath) as f:
        return json.load(f)


def save_json(filepath: str, data: dict):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def compute_delta_pct(experiment_score: float, baseline_value: float) -> str:
    if baseline_value is None or baseline_value <= 0:
        return "N/A"
    delta = (experiment_score - baseline_value) / baseline_value
    return f"{delta * 100:+.1f}%"


def revert_files(exp: dict):
    """KILL verdict: revert affected files from backups."""
    exp_id = exp.get("id", "UNKNOWN")
    backup_path = os.path.join(BACKUP_DIR, exp_id)

    if not os.path.exists(backup_path):
        print(f"  No backup directory found for {exp_id} — skipping file reversion")
        print(f"  (Change may not have been staged for reversion, or already reverted)")
        return

    reverted = []
    for filename in os.listdir(backup_path):
        src = os.path.join(backup_path, filename)
        dst = filename  # restore to original location (workspace root)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            reverted.append(dst)

    if reverted:
        print(f"  ✓ Reverted {len(reverted)} file(s): {', '.join(reverted)}")
    else:
        print(f"  No files to revert")


def evolve_baseline(exp: dict, dry_run: bool = False):
    """KEEP verdict: update champion baseline with the mutation."""
    bl = load_json(BASELINE_FILE)

    exp_score = float(exp["experiment_score"])
    old_version = bl["version"]
    new_version = old_version + 1
    delta_pct = compute_delta_pct(exp_score, bl["baseline_value"])

    variable = exp.get("variable", "unknown")
    mutation = exp.get("mutation", "unknown")

    # Update strategy (replace the mutated variable)
    updated_strategy = dict(bl.get("strategy", {}))
    updated_strategy[variable] = mutation

    # Build changelog entry
    changelog_entry = (
        f"v{new_version}: {variable}={mutation} "
        f"({delta_pct}, {exp['id']}) ← KEEP"
    )

    # Apply updates
    bl["version"] = new_version
    bl["baseline_value"] = exp_score
    bl["measurements"] = bl.get("measurements", 10) + len(exp.get("measurements", []))
    bl["strategy"] = updated_strategy
    bl["changelog"].append(changelog_entry)
    bl["last_updated"] = datetime.now().isoformat()

    if dry_run:
        print("\n[DRY RUN] Would update baseline.json:")
        print(f"  version:       v{old_version} → v{new_version}")
        print(f"  baseline:      {bl.get('baseline_value', exp_score)} → {exp_score}")
        print(f"  strategy:      {updated_strategy}")
        print(f"  +changelog:   [{changelog_entry}]")
        return

    save_json(BASELINE_FILE, bl)
    print(f"✓ Updated {BASELINE_FILE}: v{old_version} → v{new_version}")
    print(f"  baseline_value: {exp_score}")
    print(f"  strategy:       {updated_strategy}")


def update_meta_kill_streak(reset: bool = False):
    """Reset kill_streak on KEEP, increment on KILL."""
    meta = load_json(META_FILE)
    if reset:
        meta["kill_streak"] = 0
        print(f"✓ Reset kill_streak → 0")
    else:
        meta["kill_streak"] = meta.get("kill_streak", 0) + 1
        streak = meta["kill_streak"]
        print(f"✓ Incremented kill_streak → {streak}")
        if streak >= 3:
            print(f"⚠️  Circuit breaker triggered ({streak} consecutive KILLs)")
            print(f"   Pausing experiment proposal — human review required")
    save_json(META_FILE, meta)


def append_results_tsv(exp: dict, status: str):
    """Append experiment result to results.tsv."""
    exp_id = exp.get("id", "UNKNOWN")
    metric = load_json(BASELINE_FILE).get("primary_metric", "unknown")
    exp_score = float(exp.get("experiment_score", 0))
    baseline = float(exp.get("champion_baseline", load_json(BASELINE_FILE).get("baseline_value", 0)))
    delta_pct = compute_delta_pct(exp_score, baseline) if baseline else "N/A"
    mutation = exp.get("mutation", "unknown")
    date = datetime.now().strftime("%Y-%m-%d")

    row = f"{date}\t{exp_id}\t{metric}\t{exp_score}\t{baseline}\t{delta_pct}\t{status}\t{mutation}"

    with open(RESULTS_FILE, "a") as f:
        f.write(row + "\n")
    print(f"✓ Appended to {RESULTS_FILE}: {status}")


def archive_experiment(filepath: str, exp_id: str, status: str):
    """Archive experiment file to experiments/archive/."""
    dest = f"{ARCHIVE_DIR}/{exp_id}_{status.lower()}.md"
    shutil.copy2(filepath, dest)
    print(f"✓ Archived to {dest}")


def update_meta_next_id():
    """Increment next_exp_id in meta.json."""
    meta = load_json(META_FILE)
    meta["next_exp_id"] = meta.get("next_exp_id", 1) + 1
    meta["active_experiment"] = None
    save_json(META_FILE, meta)
    print(f"✓ Set next_exp_id → {meta['next_exp_id']}")


def main():
    parser = argparse.ArgumentParser(description="Execute KEEP or KILL verdict for an experiment.")
    parser.add_argument("experiment_file", nargs="?", default=None,
                        help="Path to the experiment markdown file (e.g., experiments/EXP-001.md)")
    parser.add_argument("--exp-id", dest="exp_id", type=str, default=None,
                        help="Experiment ID (e.g., EXP-001)")
    parser.add_argument("--exp-score", dest="exp_score", type=float, default=None,
                        help="Experiment score (measured performance)")
    parser.add_argument("--variable", type=str, default=None,
                        help="Variable that was mutated (e.g., behavior, workflow)")
    parser.add_argument("--mutation", type=str, default=None,
                        help="New value for the mutated variable")
    parser.add_argument("--baseline", type=float, default=None,
                        help="Champion baseline at time of experiment")
    parser.add_argument("--status", choices=["KEEP", "KILL", "MODIFY"], default="KEEP",
                        help="Experiment verdict (default: KEEP)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would change without making updates")
    parser.add_argument("--kill", action="store_true",
                        help="Shortcut: run KILL protocol instead of KEEP")
    parser.add_argument("--skip-archive", action="store_true",
                        help="Do not archive the experiment file")

    args = parser.parse_args()

    if args.kill:
        args.status = "KILL"

    # Build exp dict from file or explicit args
    exp = {}
    if args.experiment_file:
        exp = parse_experiment_file(args.experiment_file)

    if args.exp_id:
        exp["id"] = args.exp_id
    if args.exp_score is not None:
        exp["experiment_score"] = args.exp_score
    if args.variable:
        exp["variable"] = args.variable
    if args.mutation:
        exp["mutation"] = args.mutation
    if args.baseline:
        exp["champion_baseline"] = args.baseline

    # Validate
    if not exp.get("id"):
        print("Error: experiment ID required. Pass experiment_file or --exp-id.", file=sys.stderr)
        sys.exit(1)
    if not exp.get("experiment_score"):
        print("Error: experiment score required. Pass experiment_file with filled measurements "
              "or --exp-score.", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print(f"\n[DRY RUN] Would execute {args.status} verdict for {exp['id']}")
        if args.status == "KEEP":
            evolve_baseline(exp, dry_run=True)
        else:
            revert_files(exp)
        return

    # Execute verdict
    print(f"\n{'=' * 50}")
    print(f"AUTORESEARCH VERDICT: {args.status}")
    print(f"Experiment: {exp['id']}")
    print(f"{'=' * 50}")
    print(f"Experiment score: {exp.get('experiment_score')}")
    print(f"Variable:        {exp.get('variable', 'unknown')}")
    print(f"Mutation:        {exp.get('mutation', 'unknown')}")

    if args.status == "KEEP":
        print(f"\n→ Integrating change permanently into agent files")
        evolve_baseline(exp)
        update_meta_kill_streak(reset=True)
    else:
        print(f"\n→ Reverting agent files to pre-experiment state")
        revert_files(exp)
        update_meta_kill_streak(reset=False)

    append_results_tsv(exp, args.status)

    if not args.skip_archive and args.experiment_file:
        archive_experiment(args.experiment_file, exp["id"], args.status)

    update_meta_next_id()

    meta = load_json(META_FILE)
    print(f"\n✓ {args.status} verdict executed for {exp['id']}")
    if meta["kill_streak"] >= 3:
        print(f"⚠️  Experiment loop paused — 3 consecutive KILLs. Human review required.")
    else:
        print(f"  Ready for next experiment.")


if __name__ == "__main__":
    main()
