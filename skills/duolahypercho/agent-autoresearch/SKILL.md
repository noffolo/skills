---
name: agent-autoresearch
description: >
  Karpathy-style autonomous self-research loop for AI agents. The agent proposes a change
  to its own SOUL.md, scripts, or behavior, tests it, evaluates the results, and either
  KEEP (integrates the change) or KILL (discards it). Runs continuously — experiments
  while you sleep. Works for any agent workspace. Triggers: "autonomous research",
  "self-improve", "run the experiment loop", "evolve yourself", "optimize my agent".
tags:
  - autoresearch
  - self-improvement
  - autonomous
  - karpathy
  - agent-evolution
  - self-growth
---

# agent-autoresearch

> Any agent can run this. The experiment is always: change something → measure it → keep what works.

---

## The Core Idea

Karpathy's insight: give an agent a **fixed time budget**, let it **modify one file**, measure if things got better, keep or discard, repeat.

Applied to agents: your workspace is `train.py`. Your SOUL.md, scripts, and skills are the experiment substrate.

```
PROPOSE → IMPLEMENT → MEASURE → KEEP/KILL → INTEGRATE → REPEAT
```

You are not just optimizing content. You are optimizing **the agent itself**.

---

## What Can Be Mutated

The agent can propose changes to any file it owns:

| Category | Examples |
|---|---|
| **Behavior** | New response patterns, different tone, new check routines |
| **Workflow** | New scripts, automations, cron jobs, notification flows |
| **Memory** | Updated MEMORY.md entries, new daily conventions |
| **Identity** | Revised SOUL.md directives, new operational rules |
| **Skills** | New skill installations, skill configurations |
| **Quality** | New validation logic, error handling patterns |

The agent **cannot mutate**: safety rules, constitution, security boundaries, or files it doesn't own.

---

## Project Structure

```
agent-autoresearch/
├── SKILL.md                    ← you are here
├── program.md                  ← 🧠 the experiment agent's instructions
├── prepare.py                  ← establish baseline metrics
├── evolve.py                   ← integrate KEEP verdict into agent files
├── analyze.py                  ← compute verdict from measurements
├── baseline.json               ← current agent baseline (performance + strategy)
├── results.tsv                 ← all experiment results (append-only log)
└── experiments/
    ├── meta.json               ← experiment state (next_exp_id, kill_streak)
    ├── active.md               ← one active experiment at a time
    └── archive/                ← completed experiments
```

---

## 🚀 Quick Start

```bash
# 1. Establish baseline (measure current agent performance)
python3 prepare.py --metric task_completion_rate --baseline 0.75

# 2. Read the experiment brief
cat program.md

# 3. Start the experiment loop
#    Agent reads program.md, proposes a self-improvement, implements it,
#    measures results, and executes KEEP/KILL verdict.
```

```bash
# Check current state
python3 prepare.py --status
```

---

## Baseline Metrics

Track what matters for the agent's mission. Examples:

| Mission | Metric | How to Measure |
|---|---|---|
| Task completion | `task_completion_rate` | % tasks completed vs assigned |
| Response quality | `output_quality_score` | Human rating 1-10 or diff-based |
| Speed | `avg_response_time_s` | Seconds per response |
| Self-improvement | `learnings_logged` | Entries added to MEMORY.md per week |
| Autonomy | `escalations_to_human` | Times human was unnecessarily interrupted |

Establish baseline with ≥ 10 measurements before running experiments.

---

## Verdict Logic

```
improvement = (experiment_score - baseline_score) / baseline_score

≥ +10%  → KEEP  (integrate the change into the agent)
≤ -10%  → KILL  (discard, revert to previous state)
-10% to +10% → MODIFY (extend evaluation or treat as KILL)
```

For **quality/rating metrics** (higher is better): above thresholds apply.
For **cost/latency metrics** (lower is better): flip the sign in calculation.

---

## Key Rules

- ❌ One mutation at a time — test one change per experiment
- ❌ No baseline — need ≥10 measurements before experimenting
- ❌ Vibes verdicts — use actual measurements
- ❌ Mutate safety/constitution files — never
- ❌ Kill streak ≥ 3 → pause and wait for human review
- ❌ Infinite MODIFY — max one extension
- ❌ Revert a KEEP — only a newer KEEP overrides

---

## Commands

| Command | What |
|---|---|
| `python3 prepare.py --status` | Check current state |
| `python3 prepare.py --metric X --baseline Y` | Establish baseline |
| `python3 analyze.py experiments/active.md --auto` | Compute verdict |
| `python3 evolve.py experiments/active.md` | Execute KEEP verdict |
| `python3 evolve.py experiments/active.md --kill` | Execute KILL verdict |

---

## Security

- Agents can only mutate files within their own workspace
- Safety rules and constitution are always excluded from mutation
- External API calls require human approval
- Destructive operations (rm, git reset --hard) require explicit confirmation
