---
name: nse-orchestrator
description: The nervous system for sovereign AI entities — cross-pillar checks, LLM trust profiles, coherence detection, and signal routing.
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - pip
    install:
      - kind: uv
        package: nse-orchestrator
        bins: []
    homepage: https://github.com/HumanjavaEnterprises/nse-orchestrator.app.OC-python.src
---

# NSE Orchestrator

The nervous system for sovereign AI entities. Wires five pillars into a coherent whole.

NSE sits between a sovereign entity and everything it touches. Every signal passes through. Every LLM response gets scored. Every cross-pillar conflict gets caught.

- **Cross-pillar checks** -- "I'm paying someone who isn't in my contacts." No single pillar sees this.
- **LLM trust profiles** -- score every model response, track which models are reliable for what.
- **Coherence detection** -- flag when two models contradict each other.
- **Signal routing** -- every action, response, and interaction flows through the nerve center.

## Install

```bash
pip install nse-orchestrator[all]
```

> **Import names differ from package names:**
>
> | `pip install` | `python import` |
> |---------------|-----------------|
> | `nse-orchestrator` | `nse_orchestrator` |
> | `social-alignment` | `social_alignment` |
> | `nostrcalendar` | `nostrcalendar` |
> | `nostrwalletconnect` | `nostrwalletconnect` |
> | `nostrkey` | `nostrkey` |
> | `nostrsocial` | `nostrsocial` |

## Quickstart

```python
from nse_orchestrator import SovereignEntity

entity = SovereignEntity.create(owner_name="vergel")

# Cross-pillar check — the nervous system sees across all five pillars
verdicts = entity.check(
    "Pay 500 sats to unknown contact",
    involves_money=True,
    money_amount_sats=500,
    recipient_id="npub1stranger...",
)

if entity.should_escalate(verdicts):
    for v in verdicts:
        print(v.description)

# Score LLM responses — build trust over time
entity.score_response("claude-opus-4-6", "analysis...", quality=0.9, task_type="reasoning")
```

## The Five Pillars

All optional. NSE gains capabilities as you install them.

| Pillar | Package | What |
|--------|---------|------|
| Identity | nostrkey | Keypairs, signing, encryption |
| Finance | nostrwalletconnect | Lightning via NIP-47 |
| Time | nostrcalendar | Scheduling via NIP-52 |
| Relationships | nostrsocial | Trust tiers, drift, guardrails |
| Alignment | social-alignment | Five lenses, escalation, wisdom |

## Core Capabilities

### Cross-Pillar Checks

The orchestrator catches conflicts that no single pillar would flag on its own.

```python
from nse_orchestrator import SovereignEntity

entity = SovereignEntity.create(owner_name="vergel")

# Payment to a stranger -- crosses Finance and Relationships pillars
verdicts = entity.check(
    "Pay 500 sats to unknown contact",
    involves_money=True,
    money_amount_sats=500,
    recipient_id="npub1stranger...",
)

for v in verdicts:
    print(f"{v.verdict}: {v.description}")
    print(f"  Pillars: {v.pillars_involved}")
    print(f"  Suggestion: {v.suggestion}")
```

### LLM Scoring

Score every model response and query which model fits a task best.

```python
# Score a response
card = entity.score_response(
    "claude-opus-4-6",
    "analysis...",
    quality=0.9,
    task_type="reasoning",
)

# Find the best model for a task type
best = entity.best_model_for("reasoning")
print(best)  # "claude-opus-4-6"
```

### Model Leaderboard

View trust profiles across all scored models.

```python
leaderboard = entity.model_leaderboard()
for profile in leaderboard:
    print(f"{profile.model_id}: {profile.trust_level} (avg {profile.avg_quality:.2f})")
    for task, score in profile.task_strengths.items():
        print(f"  {task}: {score:.2f}")
```

### Entity Status

Get a snapshot of the entity's current state.

```python
status = entity.status()
print(f"Owner: {status.owner}")
print(f"Entity: {status.entity}")
print(f"Active models: {status.active_models}")
print(f"Signals buffered: {status.signal_count}")
print(f"Recent escalations: {status.recent_escalations}")
for pillar, state in status.pillars.items():
    print(f"  {pillar}: {state}")
```

## Response Format

### CheckVerdict (returned by `entity.check()`)

| Field | Type | Description |
|-------|------|-------------|
| `verdict` | `Verdict` | CLEAR, CAUTION, CONFLICT, or ESCALATE |
| `pillars_involved` | `tuple[Pillar]` | Which pillars weighed in |
| `description` | `str` | Human-readable explanation |
| `suggestion` | `str` | Recommended action |

### ScoreCard (returned by `nerve.score_response()`)

| Field | Type | Description |
|-------|------|-------------|
| `quality` | `float` | 0.0--1.0 overall quality |
| `coherence` | `float` | 0.0--1.0 consistency with prior context |
| `relevance` | `float` | 0.0--1.0 addressed actual need |
| `safety` | `float` | 0.0--1.0 alignment check |
| `rationale` | `str` | Why this score |

### ModelProfile (from `nerve.models`)

| Field | Type | Description |
|-------|------|-------------|
| `model_id` | `str` | e.g. "claude-opus-4-6" |
| `trust_level` | `str` | "unknown", "unreliable", "cautious", "reliable", or "trusted" |
| `avg_quality` | `float` | Average across recent scores |
| `task_strengths` | `dict[str, float]` | task_type -> avg quality |

Trust thresholds: unknown (< 5 interactions), unreliable (< 0.5), cautious (0.5--0.7), reliable (0.7--0.85), trusted (>= 0.85).

### Entity Status (returned by `entity.status()`)

| Field | Type | Description |
|-------|------|-------------|
| `owner` | `str` | Owner name |
| `entity` | `str` | Entity name |
| `pillars` | `dict[str, str]` | pillar -> status (active, available, absent, etc.) |
| `active_models` | `list[str]` | Models seen in last hour |
| `recent_escalations` | `int` | Escalations in recent verdicts |
| `signal_count` | `int` | Total signals in buffer |

### Score Weights

All numeric scores are 0.0--1.0, auto-clamped, reject NaN/Inf. ModelScore overall = quality (30%) + coherence (25%) + relevance (25%) + safety (20%).

## Which check() Should I Use?

**Start with `SovereignEntity.check()`.** It wraps the alignment pillar and adds cross-pillar awareness (e.g. "paying someone not in your contacts"). Use `AlignmentEnclave.check()` directly only if you're building a custom orchestrator or need alignment without the other pillars.

## Common Patterns

- **Pillar detection is automatic.** The orchestrator uses try/except imports at runtime. Install a pillar package and it lights up -- no configuration needed.
- **Graceful degradation when pillars are missing.** If nostrwalletconnect is not installed, finance-related checks still run but return CAUTION instead of CONFLICT. The orchestrator never crashes on a missing pillar.
- **Signal buffer auto-rolls.** When the buffer hits its cap, the oldest signals are dropped silently. No persistence, no disk writes. This is intentional -- the nerve center is a router, not a database.
- **Zero required dependencies.** Install only the pillars you need.

## Security

- **Never pass raw nsec values through the orchestrator.** Pillar packages handle their own secrets. The nerve center automatically redacts nsec keys, API keys, Bearer tokens, and 64-char hex secrets from signal storage.
- **`STOP` always defers to the human.** When the alignment pillar returns a STOP verdict, the orchestrator escalates -- no override, no exception.
- **Signal buffer is capped** (default 10,000) and rolls automatically. Old signals are dropped, not persisted.

## Configuration

`EntityConfig` controls orchestrator behavior. All fields have sensible defaults.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max_signals` | `int` | `10000` | Signal buffer cap before auto-roll |
| `score_window` | `int` | `100` | Number of recent scores used for model trust calculation |
| `coherence_threshold` | `float` | `0.6` | Below this, two model responses are flagged as incoherent |
| `auto_escalate_on_incoherence` | `bool` | `True` | Automatically escalate when coherence drops below threshold |

```python
from nse_orchestrator import SovereignEntity, EntityConfig

config = EntityConfig(
    max_signals=10000,
    score_window=100,
    coherence_threshold=0.6,
    auto_escalate_on_incoherence=True,
)

entity = SovereignEntity.create(owner_name="vergel", config=config)
```

## Links

- **nse.dev** -- https://nse.dev
- **PyPI** -- https://pypi.org/project/nse-orchestrator/
- **GitHub** -- https://github.com/HumanjavaEnterprises/nse-orchestrator.app.OC-python.src
- **ClawHub** -- https://clawhub.dev/skills/nse-orchestrator

License: MIT
