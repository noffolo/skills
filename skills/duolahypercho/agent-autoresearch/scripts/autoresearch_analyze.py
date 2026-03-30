#!/usr/bin/env python3
"""
autoresearch_analyze.py — Analyze experiment results vs champion baseline.

Karpathy's autoresearch pattern applied to content: read an experiment file,
compare metrics against baseline, output a KEEP/MODIFY/KILL verdict.

Usage:
    python3 autoresearch_analyze.py experiments/active.md --baseline 1200 --threshold 0.10
    python3 autoresearch_analyze.py experiments/active.md --baseline 1200 --threshold 0.10 --metric views_48h
    python3 autoresearch_analyze.py experiments/active.md --auto  # reads baseline from meta.json

The script parses the experiment file for metric values, computes the average,
compares to baseline, and outputs a verdict with rationale.

Standalone Python 3, no external dependencies.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime


def parse_experiment_file(filepath: str) -> dict:
    """
    Parse an experiment markdown file and extract key fields.
    Looks for **Key:** Value patterns and the metrics table.
    """
    with open(filepath, "r") as f:
        content = f.read()

    exp = {
        "raw": content,
        "filepath": filepath,
    }

    # Extract standard fields
    field_patterns = {
        "status": r"\*\*Status:\*\*\s*(.+)",
        "variable": r"\*\*Variable:\*\*\s*(.+)",
        "mutation": r"\*\*Mutation:\*\*\s*(.+)",
        "champion_version": r"\*\*Champion Version:\*\*\s*v?(\d+)",
        "created": r"\*\*Created:\*\*\s*(\S+)",
        "evaluation_date": r"\*\*Evaluation Date:\*\*\s*(\S+)",
        "experiment_avg": r"\*\*Experiment Average:\*\*\s*([\d.]+)",
        "champion_baseline": r"\*\*Champion Baseline:\*\*\s*([\d.]+)",
    }

    for key, pattern in field_patterns.items():
        match = re.search(pattern, content)
        if match:
            exp[key] = match.group(1).strip()

    # Extract experiment ID from title
    title_match = re.search(r"#\s+(EXP-\d+)", content)
    if title_match:
        exp["id"] = title_match.group(1)

    # Extract metric values from the metrics table
    # Pattern: | post_id | metric_value | collected_at |
    metric_values = []
    in_metrics_table = False
    for line in content.split("\n"):
        if "Primary Metric Value" in line:
            in_metrics_table = True
            continue
        if in_metrics_table and line.startswith("|"):
            # Skip separator line
            if "---" in line:
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 2:
                try:
                    val = float(cells[1])
                    metric_values.append(val)
                except (ValueError, IndexError):
                    pass
        elif in_metrics_table and not line.startswith("|"):
            in_metrics_table = False

    exp["metric_values"] = metric_values

    return exp


def load_meta(experiments_dir: str) -> dict:
    """Load experiments/meta.json if it exists."""
    meta_path = os.path.join(experiments_dir, "meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            return json.load(f)
    return {}


def compute_verdict(experiment_avg: float, baseline: float, threshold: float) -> dict:
    """
    Core autoresearch verdict logic.

    improvement = (experiment_avg - baseline) / baseline

    KEEP:   improvement >= threshold
    KILL:   improvement <= -threshold
    MODIFY: otherwise (inconclusive, within noise band)
    """
    if baseline <= 0:
        return {
            "verdict": "ERROR",
            "improvement": 0,
            "rationale": "Baseline is zero or negative. Cannot evaluate.",
        }

    delta = experiment_avg - baseline
    improvement = delta / baseline

    if improvement >= threshold:
        verdict = "KEEP"
        rationale = (
            f"Experiment avg ({experiment_avg:.1f}) beats baseline ({baseline:.1f}) "
            f"by {improvement * 100:+.1f}%, exceeding +{threshold * 100:.0f}% threshold."
        )
    elif improvement <= -threshold:
        verdict = "KILL"
        rationale = (
            f"Experiment avg ({experiment_avg:.1f}) regressed from baseline ({baseline:.1f}) "
            f"by {improvement * 100:+.1f}%, exceeding -{threshold * 100:.0f}% threshold."
        )
    else:
        verdict = "MODIFY"
        rationale = (
            f"Experiment avg ({experiment_avg:.1f}) vs baseline ({baseline:.1f}): "
            f"{improvement * 100:+.1f}% change is within ±{threshold * 100:.0f}% noise band. "
            f"Inconclusive — extend evaluation or treat as KILL."
        )

    return {
        "verdict": verdict,
        "improvement": improvement,
        "improvement_pct": f"{improvement * 100:+.1f}%",
        "delta": delta,
        "experiment_avg": experiment_avg,
        "baseline": baseline,
        "threshold": threshold,
        "rationale": rationale,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze autoresearch experiment results vs baseline."
    )
    parser.add_argument(
        "experiment_file",
        help="Path to the experiment markdown file (e.g., experiments/active.md)",
    )
    parser.add_argument(
        "--baseline",
        type=float,
        default=None,
        help="Champion baseline metric value. Overrides file/meta values.",
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
        default="primary",
        help="Name of the metric being evaluated (for display only).",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Auto-load baseline from experiments/meta.json",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output result as JSON instead of human-readable text.",
    )

    args = parser.parse_args()

    # Parse experiment file
    if not os.path.exists(args.experiment_file):
        print(f"Error: Experiment file not found: {args.experiment_file}", file=sys.stderr)
        sys.exit(1)

    exp = parse_experiment_file(args.experiment_file)

    # Determine baseline
    baseline = args.baseline

    if baseline is None and "champion_baseline" in exp:
        baseline = float(exp["champion_baseline"])

    if baseline is None and args.auto:
        experiments_dir = os.path.dirname(args.experiment_file) or "experiments"
        meta = load_meta(experiments_dir)
        baseline = meta.get("baseline")

    if baseline is None:
        print(
            "Error: No baseline provided. Use --baseline, --auto, or set "
            "**Champion Baseline:** in the experiment file.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Determine experiment average
    if exp["metric_values"]:
        experiment_avg = sum(exp["metric_values"]) / len(exp["metric_values"])
    elif "experiment_avg" in exp:
        experiment_avg = float(exp["experiment_avg"])
    else:
        print(
            "Error: No metric values found in experiment file. Fill in the "
            "metrics table or set **Experiment Average:**.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Compute verdict
    result = compute_verdict(experiment_avg, baseline, args.threshold)
    result["experiment_id"] = exp.get("id", "UNKNOWN")
    result["variable"] = exp.get("variable", "unknown")
    result["mutation"] = exp.get("mutation", "unknown")
    result["metric_name"] = args.metric
    result["n_posts"] = len(exp["metric_values"])
    result["evaluated_at"] = datetime.now().isoformat()

    if args.output_json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        print("=" * 60)
        print(f"AUTORESEARCH VERDICT: {result['verdict']}")
        print("=" * 60)
        print(f"Experiment:    {result['experiment_id']}")
        print(f"Variable:      {result['variable']}")
        print(f"Mutation:      {result['mutation']}")
        print(f"Metric:        {result['metric_name']}")
        print(f"Posts analyzed: {result['n_posts']}")
        print(f"")
        print(f"Experiment avg: {result['experiment_avg']:.1f}")
        print(f"Baseline:       {result['baseline']:.1f}")
        print(f"Delta:          {result['delta']:+.1f}")
        print(f"Improvement:    {result['improvement_pct']}")
        print(f"Threshold:      ±{result['threshold'] * 100:.0f}%")
        print(f"")
        print(f"Rationale: {result['rationale']}")
        print("=" * 60)

        # Action guidance
        if result["verdict"] == "KEEP":
            print("\nNext steps:")
            print("  1. Run: python3 evolve.py experiments/active.md")
            print("     → Updates baseline.json, resets kill_streak, archives experiment")
            print("  2. Propose next experiment immediately")
        elif result["verdict"] == "KILL":
            print("\nNext steps:")
            print("  1. Run: python3 evolve.py experiments/active.md --kill")
            print("     → Increments kill_streak, archives experiment (no baseline change)")
            print("  2. Check kill_streak: if >= 3, pause and wait for human reset")
            print("  3. Propose next experiment")
        elif result["verdict"] == "MODIFY":
            print("\nNext steps:")
            print("  1. If not yet extended: extend evaluation_date by one window, continue posting")
            print("  2. If already extended: run: python3 evolve.py experiments/active.md --kill")
            print("  3. Never extend more than once")


if __name__ == "__main__":
    main()
