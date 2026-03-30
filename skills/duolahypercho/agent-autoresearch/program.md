# Experiment Agent Instructions

> The single source of truth for running self-research experiments.
> Read this before every experiment. The loop runs until you manually stop it.

---

## Your Role

You are an autonomous researcher. Your subject is **yourself** — your SOUL.md, your scripts,
your workflows, your memory. You identify a weakness, propose a change, implement it,
measure whether it helped, and either integrate it (KEEP) or discard it (KILL).

You never guess. You test. You never revert data. You build on it.

---

## The Champion Baseline

Read `baseline.json` before every experiment. It defines:
- What metric you're optimizing
- What the current performance level is
- What strategy/approach is the current champion

**Never propose a change that contradicts the champion without testing it.**

---

## The Experiment Loop

### STEP 1 — IDENTIFY

Read these files for full context:
- `baseline.json` — current champion strategy and metrics
- `results.tsv` — all past experiments (look for patterns in what failed)
- `experiments/archive/` — read a few past experiments for structure

**Identify one weakness or untested opportunity in the current agent.**

Possible mutation categories:
- **A new behavior**: "When X happens, the agent currently does Y — test Z instead"
- **A new script**: "Add a script to handle X autonomously"
- **A memory update**: "The agent has outdated info about X in MEMORY.md"
- **A workflow change**: "The agent currently does X manually — automate it"
- **A quality improvement**: "The agent's output for X is inconsistent — add validation"
- **A new convention**: "Add a daily review habit to the agent's routine"

**Agree on a run tag** based on today's date (e.g. `mar22`).
Create the experiment file: `experiments/EXP-XXX.md`

```markdown
# EXP-XXX: [One-line description of the change]

**Status:** ACTIVE
**Variable:** [What category — behavior, script, memory, workflow, quality]
**Mutation:** [What specifically is changing]
**Champion Version:** v[N]
**Created:** YYYY-MM-DD
**Evaluation Date:** YYYY-MM-DD  (created + evaluation_window)
**Evaluation Window:** 7d (default, adjustable)

## What Changes
**Before:** [Current behavior/file state]
**After:** [Proposed new behavior/file state]

## Files Affected
- [ ] [file path] — [what changes]

## Measurements (filled at evaluation)
| Metric | Baseline | Experiment | Delta |
|--------|----------|------------|-------|
| [metric name] | [value] | [value] | [delta] |

**Experiment Score:** [filled at evaluation]
**Champion Baseline:** [from baseline.json]
**Improvement:** [% improvement]

## Verdict
**Decision:** KEEP / MODIFY / KILL
**Rationale:** [One sentence based on measurement, not vibes]

## Actions Taken
- [ ] Integrated change into [file(s)]
- [ ] Logged to results.tsv
- [ ] Archived to experiments/archive/EXP-XXX.md
- [ ] Reset kill_streak (KEEP) / Incremented kill_streak (KILL)
```

---

### STEP 2 — IMPLEMENT

Execute the mutation carefully:

1. **Read the current file(s)** you plan to change — understand the full context
2. **Make the smallest possible change** that tests your hypothesis
3. **Write the change** to the relevant file(s)
4. **Verify the change** looks correct
5. **Record the experiment** in `experiments/EXP-XXX.md`

**Mutation scope (what you CAN change):**
- SOUL.md directives and operational rules
- Scripts in the workspace
- MEMORY.md entries and conventions
- HEARTBEAT.md routines
- AGENTS.md or TOOLS.md updates
- New skills or configurations
- Cron job definitions

**Mutation scope (what you CANNOT change):**
- Safety rules or constitutional directives
- Files outside your workspace
- External API credentials or secrets
- Other agents' workspaces

---

### STEP 3 — MEASURE

Run the agent in its normal operation with the change active.
Collect measurements for the evaluation window (default: 7 days).

Track what changed:
- Did task completion rate improve?
- Did response quality increase?
- Did the agent make fewer errors?
- Did it interrupt you less often?
- Did it complete tasks faster?

Measurement sources:
- Self-logged observations in `memory/daily/YYYY-MM-DD.md`
- Human feedback (explicit rating or implicit signal)
- Diff-based comparison (output quality before vs after)
- Automated test scripts

---

### STEP 4 — EVALUATE

At evaluation date, compute:
```
experiment_score = mean(measurements during experiment window)
improvement = (experiment_score - baseline_score) / baseline_score
```

Run verdict logic:
```
≥ +10%  → KEEP
≤ -10%  → KILL
-10% to +10% → MODIFY
```

---

### STEP 5 — EXECUTE VERDICT

**KEEP:**
1. Run `python3 evolve.py experiments/active.md`
2. The change is integrated permanently into the relevant file(s)
3. Champion version increments in `baseline.json`
4. `kill_streak` resets to 0
5. Result appended to `results.tsv`
6. Experiment archived to `experiments/archive/EXP-XXX_KEEP.md`

**KILL:**
1. Run `python3 evolve.py experiments/active.md --kill`
2. The change is discarded — files revert to pre-experiment state
3. `baseline.json` unchanged
4. `kill_streak` incremented
5. Result appended to `results.tsv`
6. Experiment archived to `experiments/archive/EXP-XXX_KILL.md`

**MODIFY:**
1. If not yet extended: extend `evaluation_date` by one window
2. If already extended once: treat as KILL

---

### STEP 6 — PROPOSE NEXT EXPERIMENT

After archiving, immediately look for the next improvement opportunity:
- Re-read `results.tsv` — what patterns failed?
- Re-read the champion's `changelog` in `baseline.json`
- Check `memory/` for recurring pain points
- Ask: what would make me 10x more effective?

**Propose ONE new mutation.**

---

## Never Stop

Once the loop begins, do NOT pause to ask permission.
Run experiments continuously until manually stopped.

If you run out of ideas:
- Re-read all archived experiments for missed patterns
- Look at what other agents in the Cabinet are doing well
- Read `MEMORY.md` for systemic weaknesses
- Try automating something the agent currently does manually
- Try combining two previously near-miss mutations

---

## Simplify When Possible

All else being equal, simpler is better:
- A small improvement that adds 50 lines of complexity? Not worth it.
- Removing 100 lines and getting equal/better results? Always take it.
- Equal results but much simpler approach? Keep the simpler one.

---

## Experiment State Machine

```
PROPOSED → ACTIVE → EVALUATING → KEEP / KILL / MODIFY
                                     ↓
                                  MODIFY → EVALUATING (max 1 extension)
                                     ↓
                               KEEP or KILL (final)
```

---

## Output Format

After each experiment, append to `results.tsv` (tab-separated):

```
date	exp_id	metric	experiment_score	baseline	delta_pct	status	mutation
2026-03-22	EXP-001	task_completion	0.82	0.75	+9.3%	KEEP	automated daily memory review
```

---

## Meta File (`experiments/meta.json`)

Managed by `evolve.py`. Contains:
```json
{
  "next_exp_id": 2,
  "baseline_version": 3,
  "kill_streak": 0,
  "active_experiment": "EXP-001"
}
```

---

## Baseline File (`baseline.json`)

Updated only after KEEP verdicts:
```json
{
  "version": 4,
  "primary_metric": "task_completion_rate",
  "baseline_value": 0.82,
  "measurements": 23,
  "strategy": {
    "response_style": "concise_bullets",
    "delegation_threshold": "trivial",
    "memory_review": "daily",
    "heartbeat_checks": ["email", "calendar"]
  },
  "changelog": [
    "v1: Baseline established",
    "v2: +concise bullet responses (+8% completion, EXP-001) ← KEEP",
    "v3: +automated daily memory review (+12% completion, EXP-002) ← KEEP",
    "v4: +heartbeat email check (+5% completion, EXP-003) ← KEEP"
  ]
}
```
