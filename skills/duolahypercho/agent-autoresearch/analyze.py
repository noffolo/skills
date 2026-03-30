#!/usr/bin/env python3
"""
analyze.py — Compute KEEP/KILL/MODIFY verdict from experiment measurements.

Usage:
    python3 analyze.py experiments/active.md --auto
    python3 analyze.py experiments/active.md --baseline 0.75 --threshold 0.10
    python3 analyze.py experiments/active.md --auto --json

Reads the experiment file for measurements, compares to baseline, outputs verdict.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

META_FILE = "experiments/meta.json"
BASELINE_FILE = "baseline.json"


def parse_experiment_file(filepath: str) -> dict:
    """Parse experiment markdown file for key fields and measurements."""
    if not os.path.exists(filepath):
        print(f"Error: Experiment file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    with open(filepath) as f:
        content = f.read()

    exp = {"filepath": filepath, "raw": content}

    # Extract experiment ID
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
        "created": r"\*\*Created:\*\*\s*(\S+)",
        "evaluation_date": r"\*\*Evaluation Date:\*\*\s*(\S+)",
    }
    for key, pattern in field_patterns.items():
        m = re.search(pattern, content)
        if m:
            exp[key] = m.group(1).strip()

    # Extract measurement rows from the metrics table
    measurements = []
    in_table = False
    for line in content.split("\n"):
        if "Experiment Score" in line or ("Metric" in line and "|" in line):
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

    return exp


def load_json(filepath: str) -> dict:
    if os.path.exists(filepath):
        with open(filepath) as f:
            return json.load(f)
    return {}


def compute_verdict(experiment_score: float, baseline: float, threshold: float) -> dict:
    """
    Core verdict logic.
    improvement = (experiment_score - baseline) / baseline
    """
    if baseline is None or baseline <= 0:
        return {
            "verdict": "ERROR",
            "improvement": 0,
            "rationale": "Baseline is zero or negative. Cannot evaluate.",
        }

    delta = experiment_score - baseline
    improvement = delta / baseline

    if improvement >= threshold:
        verdict = "KEEP"
        rationale = (
            f"Experiment score ({experiment_score:.3f}) beats baseline ({baseline:.3f}) "
            f"by {improvement * 100:+.1f}%, exceeding +{threshold * 100:.0f}% threshold."
        )
    elif improvement <= -threshold:
        verdict = "KILL"
        rationale = (
            f"Experiment score ({experiment_score:.3f}) regressed from baseline ({baseline:.3f}) "
            f"by {improvement * 100:+.1f}%, exceeding -{threshold * 100:.0f}% threshold."
        )
    else:
        verdict = "MODIFY"
        rationale = (
            f"Experiment score ({experiment_score:.3f}) vs baseline ({baseline:.3f}): "
            f"{improvement * 100:+.1f}% change is within ±{threshold * 100:.0f}% noise band. "
            f"Inconclusive — extend evaluation window or treat as KILL."
        )

    return {
        "verdict": verdict,
        "improvement": improvement,
        "improvement_pct": f"{improvement * 100:+.1f}%",
        "delta": delta,
        "experiment_score": experiment_score,
        "baseline": baseline,
        "threshold": threshold,
        "rationale": rationale,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze experiment results and compute KEEP/KILL/MODIFY verdict."
    )
    parser.add_argument(
        "experiment_file",
        help="Path to the experiment markdown file (e.g., experiments/active.md)",
    )
    parser.add_argument(
        "--baseline",
        type=float,
        default=None,
        help="Champion baseline score. Overrides file/meta values.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.10,
        help="Improvement threshold for KEEP/KILL (default: 0.10 = 10%%)",
    )
    parser.add_argument(
        "--metric",
        type=str,
        default=None,
        help="Metric name (for display only).",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Auto-load baseline from baseline.json",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output result as JSON.",
    )

    args = parser.parse_args()

    if not os.path.exists(args.experiment_file):
        print(f"Error: Experiment file not found: {args.experiment_file}", file=sys.stderr)
        sys.exit(1)

    exp = parse_experiment_file(args.experiment_file)

    # Resolve baseline
    baseline = args.baseline
    if baseline is None and "champion_baseline" in exp:
        baseline = float(exp["champion_baseline"])
    if baseline is None and args.auto:
        bl = load_json(BASELINE_FILE)
        baseline = bl.get("baseline_value")

    if baseline is None:
        print(
            "Error: No baseline found. Use --baseline, --auto, or set "
            "**Champion Baseline:** in the experiment file.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Resolve experiment score
    if exp.get("measurements"):
        experiment_score = sum(exp["measurements"]) / len(exp["measurements"])
    elif exp.get("experiment_score"):
        experiment_score = float(exp["experiment_score"])
    else:
        print(
            "Error: No measurements found. Fill in the metrics table or set "
            "**Experiment Score:** in the experiment file.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Compute verdict
    result = compute_verdict(experiment_score, baseline, args.threshold)
    result["experiment_id"] = exp.get("id", "UNKNOWN")
    result["variable"] = exp.get("variable", "unknown")
    result["mutation"] = exp.get("mutation", "unknown")
    result["n_measurements"] = len(exp.get("measurements", []))
    result["evaluated_at"] = datetime.now().isoformat()

    if args.output_json:
        print(json.dumps(result, indent=2))
        return

    # Human-readable output
    metric_name = args.metric or load_json(BASELINE_FILE).get("primary_metric", "unknown")

    print("=" * 60)
    print(f"AUTORESEARCH VERDICT: {result['verdict']}")
    print("=" * 60)
    print(f"Experiment:     {result['experiment_id']}")
    print(f"Variable:       {result['variable']}")
    print(f"Mutation:       {result['mutation']}")
    print(f"Metric:         {metric_name}")
    print(f"Measurements:   {result['n_measurements']}")
    print()
    print(f"Experiment:     {result['experiment_score']:.3f}")
    print(f"Baseline:       {result['baseline']:.3f}")
    print(f"Delta:          {result['delta']:+.3f}")
    print(f"Improvement:   {result['improvement_pct']}")
    print(f"Threshold:      ±{result['threshold'] * 100:.0f}%")
    print()
    print(f"Rationale: {result['rationale']}")
    print("=" * 60)

    # Action guidance
    if result["verdict"] == "KEEP":
        print("\nNext steps:")
        print("  1. Run: python3 evolve.py experiments/active.md")
        print("     → Integrates change, updates baseline.json, resets kill_streak")
        print("  2. Propose next experiment immediately")
    elif result["verdict"] == "KILL":
        print("\nNext steps:")
        print("  1. Run: python3 evolve.py experiments/active.md --kill")
        print("     → Reverts files, increments kill_streak, archives experiment")
        print("  2. Check kill_streak: if >= 3, loop is paused until human review")
        print("  3. Propose next experiment")
    elif result["verdict"] == "MODIFY":
        print("\nNext steps:")
        print("  1. If not yet extended: extend evaluation_date by one window, continue")
        print("  2. If already extended: python3 evolve.py experiments/active.md --kill")
        print("  3. Never extend more than once")


if __name__ == "__main__":
    main()
