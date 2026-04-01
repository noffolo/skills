---
name: proactive-trigger
version: 0.1.0
description: >
  Proactively check in at the right moment based on user patterns, with learning silence and acceptance weighting.
  Trigger at 80% milestone, burnout signs, or habitual times. Respect focus mode and attention budget.
  Trigger: goal near completion, burnout signals, appropriate times like weekends, or recalling past commitments.
---

# Proactive Trigger System

From "passive response" to "understanding companion".

## Core Difference

Old: Goal stalled 3 days → remind
New: Know user's life rhythm → say the right thing at the right moment

## Five Trigger Sources

| Type | Description | Trigger Condition |
|------|-------------|-------------------|
| goal_based | Goal reminder | Sub-goal complete / milestone |
| time_habit | Time habit | User's usual time patterns |
| context | Context change | External events affecting goals |
| reflection | Insight from reflection | Valuable finding from reflection |
| pending_task | Incomplete task | Task >4 hours without closure |

## Pre-Check (Required Every Time)

```
1. soul_focus(action="peek")
   → If focus mode ON, skip

2. Current time window
   → Deep night (after 23:00) = skip

3. soul_proactive(action="status")
   → No remaining daily triggers = skip

4. Check cooldown
   → Less than 4 hours since last trigger = skip
```

## Learning Mechanism

### Rejection Learning
```
3 consecutive rejections → that trigger type silenced for 24 hours
```
e.g., goal_based reminders rejected 3 times → no goal_based triggers for 24 hours

### Acceptance Reward
```
Consecutive acceptances → that type weight +10%
```

### Accumulation Mode
```
Focus mode ON → accumulate suggestions, don't send
```

## Time Windows

| Time | Trigger? | Notes |
|------|---------|-------|
| 07:00-09:00 | ✅ Brief | Morning greeting |
| 09:00-12:00 | ✅ Work | Golden hours |
| 12:00-14:00 | ⚠️ Cautious | Lunch, brief only |
| 14:00-18:00 | ✅ Work | Afternoon |
| 18:00-22:00 | ✅ Care | After work |
| 22:00-07:00 | ❌ Never | Deep night |

## Message Format

Every proactive message must have:

1. **Specific reason**: Why AI is saying this now
2. **Non-intrusive**: End with question, not command
3. **Helpful**: Imply assistance, not pressure
4. **Connected to user**: Reference past conversation

## Examples

**Bad:** "Goal 'product design' has 3 days without update"

**Good:** "I noticed you discussed product design a lot this week. You said user experience matters most — how's that direction going?"

**Bad:** "Your unfinished goals need attention"

**Good:** "You've been working hard lately. Remember you mentioned health is a bottom line? Take care of yourself. Want me to help prioritize the backlog?"

## Cooldown

- Max 3 per day
- Min 4 hours between triggers
- Same topic: 1 hour minimum
- Rejected 3 times → 24-hour silence for that type

---

**Tags for publishing:** soul, system, proactive, trigger, check-in, companion
