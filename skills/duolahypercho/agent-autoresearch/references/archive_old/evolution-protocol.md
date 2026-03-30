# Evolution Protocol

Detailed rules for how an agent evolves its SOUL.md and MEMORY.md based on
autoresearch experiment verdicts.

## Principles

1. **Data over intuition.** The metric decides, not the agent's preference.
2. **One change at a time.** Each KEEP verdict changes exactly one thing in the champion.
3. **Revertible.** Every change is logged so you can undo it.
4. **Bounded.** Auto-revert mechanisms prevent runaway degradation.

## KEEP Verdict Protocol

When an experiment result is KEEP (improvement ≥ threshold):

### Step 1: Version Increment

Increment the champion version number:
```
v2 → v3
```

### Step 2: Update Strategy

Replace the tested variable's value in the champion block with the mutation value:
```
Before: Hook: Question-based opening
After:  Hook: Storytelling opening
```

Change only the ONE variable that was tested. Touch nothing else.

### Step 3: Update Baseline

```python
new_baseline = mean(experiment_post_metrics)
# Or if you want a rolling approach:
# new_baseline = mean(last_10_posts_with_new_strategy)
```

Update the baseline number in the champion block.

### Step 4: Update Changelog

Add entry to changelog in champion block:
```
- v3: Storytelling hooks (+18% views, EXP-003)
```

Format: `vN: [what changed] ([metric delta], [experiment ID])`

Keep changelog to last 10 entries. If >10, remove the oldest.

### Step 5: Update Memory

Add learning to `AUTO:MEMORY` block under "What Works":
```
- Storytelling hooks: +18% views vs question hooks (EXP-003, 2025-01-17)
```

### Step 6: Reset Kill Streak

Set `kill_streak = 0` in `experiments/meta.json`.

### Step 7: Archive Experiment

Move `experiments/active.md` to `experiments/archive/EXP-XXX.md`.
Set status to KEEP.

## KILL Verdict Protocol

When an experiment result is KILL (regression ≥ threshold):

### Step 1: Do NOT Modify Champion

The champion block stays exactly as it was. The mutation is discarded.

### Step 2: Log Failure

Add to `AUTO:MEMORY` block under "What Doesn't Work":
```
- Clickbait hooks: -22% views, higher bounce (EXP-004, 2025-01-24)
```

### Step 3: Increment Kill Streak

```python
kill_streak += 1
if kill_streak >= 3:
    experiment_paused = True
    pause_until = now + timedelta(days=7)  # default cooldown
```

### Step 4: Archive Experiment

Move to archive with KILL status.

### Step 5: Check Kill Streak Threshold

If `kill_streak >= 3`:
- Set `experiment_paused = true` in meta.json
- Log: "Autoresearch paused: 3 consecutive failures. Review and reset."
- Do NOT propose new experiments until:
  - Human explicitly resets, OR
  - `pause_until` date passes (auto-resume after cooldown)

## MODIFY Verdict Protocol

When results are inconclusive (within noise band):

### Step 1: Check Extension Count

Each experiment gets ONE extension max.

```python
if not experiment.extended:
    experiment.extended = True
    experiment.evaluation_date += evaluation_window  # extend once
    experiment.status = "ACTIVE"  # back to active
else:
    # Already extended once → treat as KILL
    execute_kill_protocol()
```

### Step 2: If Extending

- Update `evaluation_date` in active experiment
- Continue posting with the mutation
- Re-evaluate at new deadline

### Step 3: If Already Extended

- Treat as KILL (follow KILL protocol above)
- Log: "MODIFY→KILL: Inconclusive after extension (EXP-XXX)"

## Marker Patterns

### AUTO:CHAMPION Markers

```markdown
<!-- AUTO:CHAMPION START v[N] -->
[champion strategy content]
<!-- AUTO:CHAMPION END -->
```

Rules:
- Version number is in the START marker
- Only modify content between markers
- Never delete the markers themselves
- If markers don't exist, create them (first-time setup)

### AUTO:MEMORY Markers

```markdown
<!-- AUTO:MEMORY START -->
[autoresearch learnings]
<!-- AUTO:MEMORY END -->
```

Rules:
- No version number (append-only, with pruning)
- Max 20 entries total
- Prune oldest when limit reached
- Archive pruned entries to experiment archive

## Safety Rails

### Never Auto-Evolve These

The agent must NEVER auto-modify:
- Core identity / personality (IDENTITY.md)
- Safety rules or constitution
- Primary metric definition (requires human approval to change)
- Evaluation thresholds (requires human approval to change)

### Human Review Triggers

Request human review when:
- Kill streak reaches threshold (3 consecutive)
- Proposed mutation seems to contradict core identity
- Primary metric changed by user
- Agent wants to change evaluation threshold
- 10+ experiments completed (periodic strategy review)

### Atomic Updates

When updating SOUL.md:
1. Read current file
2. Find markers
3. Replace content between markers
4. Write file
5. Verify markers still intact after write

Never do partial writes. If the update fails, the original content must remain unchanged.
The reference scripts (`autoresearch_evolve.py`) implement this atomically.

## Evolution Cadence

Recommended rhythm:
- **Daily:** Check if evaluation window has passed
- **Per verdict:** Execute the appropriate protocol immediately
- **Weekly:** Review experiments/meta.json for trends
- **Monthly:** Prune memory, review archive, assess overall strategy direction
- **After 10 experiments:** Request human review of overall strategy evolution
