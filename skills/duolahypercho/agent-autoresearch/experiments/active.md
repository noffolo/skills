# EXP-001: [One-line description of the change]

**Status:** ACTIVE
**Variable:** [Category — behavior, script, memory, workflow, quality, identity]
**Mutation:** [What specifically is changing]
**Champion Version:** v[N]
**Created:** YYYY-MM-DD
**Evaluation Date:** YYYY-MM-DD  (created + evaluation_window)
**Evaluation Window:** 7d (default, adjustable)

## What Changes
**Before:** [Current behavior / file state]
**After:** [Proposed new behavior / file state]

## Hypothesis
[One sentence: why might this change improve the metric?]

## Files to Modify
List the files this experiment changes:
- [ ] [file path] — [what changes]

## Measurement Log
Record measurements during the evaluation window:

| Date | Metric Value | Notes |
|------|-------------|-------|
| | | |

**Experiment Score:** [mean of all measurements]
**Champion Baseline:** [from baseline.json → baseline_value]
**Improvement:** [% improvement vs baseline]

## Verdict
**Decision:** KEEP / MODIFY / KILL
**Rationale:** [One sentence based on measurement, not vibes]

## Actions Taken
- [ ] Ran `python3 evolve.py experiments/active.md` (KEEP) or `--kill` (KILL)
- [ ] Integrated / reverted change in [file(s)]
- [ ] Logged to results.tsv
- [ ] Archived to experiments/archive/EXP-XXX_KEEP.md or _KILL.md
- [ ] Reset kill_streak (KEEP) / Incremented kill_streak (KILL)

---

### Verdict Thresholds
```
improvement = (experiment_score - baseline) / baseline

≥ +10%  → KEEP  (integrate the change)
≤ -10%  → KILL  (revert to previous state)
-10% to +10% → MODIFY (extend once or treat as KILL)
```

### File Backup for Reversion
Before making changes, back up originals to:
```
experiments/backups/EXP-XXX/
  SOUL.md       # original
  scripts/x.py  # original
```
If KILL: `evolve.py` restores these files automatically.
