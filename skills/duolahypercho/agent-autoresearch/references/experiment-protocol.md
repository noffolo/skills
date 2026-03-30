# Experiment Protocol — agent-autoresearch

## State Machine

```
PROPOSED → ACTIVE → EVALUATING → KEEP / KILL / MODIFY
                                     ↓
                                  MODIFY → EVALUATING (max 1 extension)
                                     ↓
                               KEEP or KILL (final)
```

## Status Definitions

| Status | Meaning |
|--------|---------|
| `PROPOSED` | Experiment designed, not yet implemented |
| `ACTIVE` | Change implemented, evaluation window started |
| `EVALUATING` | Evaluation date reached, analyzing measurements |
| `KEEP` | Improvement ≥ +10% — change integrated permanently |
| `KILL` | Regression ≤ -10% — change reverted |
| `MODIFY` | Within ±10% noise band — extend or kill |

## Verdict Logic

```python
improvement = (experiment_score - baseline) / baseline

if improvement >= 0.10:        verdict = "KEEP"
elif improvement <= -0.10:      verdict = "KILL"
else:                           verdict = "MODIFY"
```

## KEEP Protocol

1. Run `python3 evolve.py experiments/active.md`
2. Champion version increments in `baseline.json`
3. `baseline_value` updated to experiment_score
4. `strategy` dict updated with the mutated variable
5. `kill_streak` reset to 0
6. Result appended to `results.tsv`
7. Experiment archived to `experiments/archive/EXP-XXX_KEEP.md`
8. `meta.json` → `next_exp_id` incremented

## KILL Protocol

1. Run `python3 evolve.py experiments/active.md --kill`
2. Affected files reverted from `experiments/backups/EXP-XXX/`
3. `baseline.json` unchanged
4. `kill_streak` incremented
5. Result appended to `results.tsv`
6. Experiment archived to `experiments/archive/EXP-XXX_KILL.md`
7. `meta.json` → `next_exp_id` incremented

## Kill Streak Circuit Breaker

If `kill_streak >= 3`:
- Pause automated experiment proposal
- Log: "Autoresearch paused: 3 consecutive failures"
- Do NOT propose new experiments until human explicitly resets

## MODIFY Protocol

1. If not yet extended: extend `evaluation_date` by one evaluation window
2. If already extended once: treat as KILL
3. Never extend more than once

## Evaluation Windows

| Experiment Type | Default Window |
|---|---|
| Behavior changes | 7d |
| Script additions | 3d (verify it runs without errors) |
| Memory updates | 14d (long-term retention) |
| Workflow changes | 7d |
| Quality improvements | 7d |

## Simplification Criterion

When evaluating whether to keep a change:
- A small improvement that adds 50 lines of complexity? Not worth it.
- Removing 100 lines with equal/better results? Always take it.
- Equal results but much simpler approach? Keep simpler.

## Anti-Patterns

- ❌ Stacking mutations (test one at a time)
- ❌ No baseline (need ≥10 measurements)
- ❌ Vibes verdicts (data only)
- ❌ Mutating safety/constitution files
- ❌ Reverting a KEEP (only newer KEEP overrides)
- ❌ Infinite MODIFY (max one extension)
- ❌ Kill streak ≥ 3 without pausing
