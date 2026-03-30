#!/usr/bin/env python3
"""
prepare.py — Establish baseline metrics for the agent self-research experiment loop.

DO NOT MODIFY THIS FILE. It is read-only.

This script:
1. Creates the experiments/ directory structure
2. Initializes baseline.json (agent's current performance baseline)
3. Initializes results.tsv (header only)
4. Validates the experiment environment

Run once at setup:
    python3 prepare.py

Or with explicit baseline:
    python3 prepare.py --metric task_completion_rate --baseline 0.75 --measurements 20
"""

import argparse
import json
import os
import sys
from datetime import datetime

EXPERIMENTS_DIR = "experiments"
ARCHIVE_DIR = f"{EXPERIMENTS_DIR}/archive"
META_FILE = f"{EXPERIMENTS_DIR}/meta.json"
BASELINE_FILE = "baseline.json"
RESULTS_FILE = "results.tsv"


def create_directories():
    """Create required directory structure."""
    os.makedirs(EXPERIMENTS_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    print(f"✓ Created {EXPERIMENTS_DIR}/ and {ARCHIVE_DIR}/")


def init_results_tsv():
    """Initialize results.tsv with header row."""
    if os.path.exists(RESULTS_FILE):
        print(f"✓ {RESULTS_FILE} already exists (not overwriting)")
        return

    header = "date\texp_id\tmetric\texperiment_score\tbaseline\tdelta_pct\tstatus\tmutation"
    with open(RESULTS_FILE, "w") as f:
        f.write(header + "\n")
    print(f"✓ Created {RESULTS_FILE}")


def init_meta():
    """Initialize meta.json with default state."""
    if os.path.exists(META_FILE):
        print(f"✓ {META_FILE} already exists (not overwriting)")
        return

    meta = {
        "next_exp_id": 1,
        "baseline_version": 1,
        "kill_streak": 0,
        "active_experiment": None,
        "setup_date": datetime.now().isoformat(),
    }
    with open(META_FILE, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"✓ Created {META_FILE}")


def init_baseline(metric: str, baseline_value: float, measurements: int, strategy: dict = None):
    """Initialize baseline.json with the agent's current champion strategy."""
    if os.path.exists(BASELINE_FILE):
        print(f"✓ {BASELINE_FILE} already exists (not overwriting)")
        print("  To reset: delete baseline.json and re-run prepare.py")
        return

    baseline = {
        "version": 1,
        "primary_metric": metric,
        "baseline_value": baseline_value,
        "measurements": measurements,
        "strategy": strategy or {},
        "changelog": [
            f"v1: Baseline established, {measurements} measurements avg {baseline_value} {metric}"
        ],
        "established_date": datetime.now().isoformat(),
    }
    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=2)
    print(f"✓ Created {BASELINE_FILE} with {metric}={baseline_value} ({measurements} measurements)")


def validate_environment():
    """Check that required files exist for running experiments."""
    errors = []
    warnings = []

    if not os.path.exists(BASELINE_FILE):
        errors.append(f"{BASELINE_FILE} not found — run setup first")

    if not os.path.exists(RESULTS_FILE):
        errors.append(f"{RESULTS_FILE} not found — run setup first")

    if not os.path.exists(META_FILE):
        warnings.append(f"{META_FILE} not found — run setup first")

    return errors, warnings


def print_status():
    """Print current experiment state."""
    print("\n" + "=" * 50)
    print("AGENT AUTORESEARCH STATUS")
    print("=" * 50)

    errors, warnings = validate_environment()

    if errors:
        print("\n❌ Setup incomplete:")
        for e in errors:
            print(f"   {e}")
        print("\n→ Run: python3 prepare.py --metric <name> --baseline <value> --measurements <count>")
        return False

    # Load and display baseline
    with open(BASELINE_FILE) as f:
        bl = json.load(f)
    print(f"\n📊 Champion (v{bl['version']})")
    print(f"   Metric:        {bl.get('primary_metric') or 'not set'}")
    print(f"   Baseline:      {bl.get('baseline_value') or 'not set'}")
    print(f"   Measurements: {bl.get('measurements', bl.get('posts_measured', 'N/A'))}")
    if bl.get("strategy"):
        print(f"   Strategy:      {bl['strategy']}")

    # Load meta
    if os.path.exists(META_FILE):
        with open(META_FILE) as f:
            meta = json.load(f)
        print(f"\n📈 Experiment State")
        print(f"   Next ID:       EXP-{meta['next_exp_id']:03d}")
        print(f"   Kill streak:   {meta['kill_streak']}")

        if meta["kill_streak"] >= 3:
            print(f"   ⚠️  Circuit breaker active — 3 consecutive KILLs")

        if meta["active_experiment"]:
            print(f"   Active:        {meta['active_experiment']}")
        else:
            print(f"   Active:        None (ready for new experiment)")

    # Load results
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            lines = f.readlines()
        completed = len(lines) - 1
        keeps = sum(1 for l in lines[1:] if "\tKEEP\t" in l)
        kills = sum(1 for l in lines[1:] if "\tKILL\t" in l)
        print(f"   Completed:     {completed} experiments")
        print(f"   KEEP:          {keeps} | KILL: {kills}")

    if warnings:
        print("\n⚠️  Warnings:")
        for w in warnings:
            print(f"   {w}")

    print("\n✓ Setup complete. Ready to run experiments.")
    print("=" * 50)
    return True


def main():
    parser = argparse.ArgumentParser(description="Prepare the agent self-research experiment environment.")
    parser.add_argument("--metric", type=str, default="task_completion_rate",
                        help="Primary metric name (default: task_completion_rate)")
    parser.add_argument("--baseline", type=float, default=None,
                        help="Baseline metric value (required for first-time setup)")
    parser.add_argument("--measurements", type=int, default=10,
                        help="Number of measurements used to establish baseline (default: 10)")
    parser.add_argument("--strategy", type=str, default=None,
                        help='JSON string for initial strategy, e.g. \'{"behavior":"concise","delegation":"all"}\'')
    parser.add_argument("--status", action="store_true",
                        help="Print current experiment state and exit")
    parser.add_argument("--reset", action="store_true",
                        help="⚠️  Delete existing baseline.json and meta.json to start fresh")

    args = parser.parse_args()

    if args.status:
        ok = print_status()
        sys.exit(0 if ok else 1)

    if args.reset:
        print("⚠️  Resetting experiment state...")
        for f in [BASELINE_FILE, META_FILE, RESULTS_FILE]:
            if os.path.exists(f):
                os.remove(f)
                print(f"   Deleted {f}")
        create_directories()

    if args.baseline is None:
        if not print_status():
            print("\n→ First-time setup: python3 prepare.py --metric <name> --baseline <value> --measurements <count>")
        return

    strategy = None
    if args.strategy:
        try:
            strategy = json.loads(args.strategy)
        except json.JSONDecodeError as e:
            print(f"Error: --strategy must be valid JSON: {e}")
            sys.exit(1)

    create_directories()
    init_results_tsv()
    init_meta()
    init_baseline(args.metric, args.baseline, args.measurements, strategy)
    print_status()


if __name__ == "__main__":
    main()
