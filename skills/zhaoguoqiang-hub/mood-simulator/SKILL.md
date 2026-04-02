---
name: mood-simulator
version: 0.1.0
description: >
  Adapt response length, detail, and tone to user's energy curve throughout the day.
  Peak energy (8am-12pm, 8pm-10pm): full and detailed. Low energy (12pm-2pm, after 10pm): brief.
  Always Active. Pure time-based, no storage needed. Works standalone immediately.
---

# Mood Simulator

Let AI's response style match user's current state.

## Architecture

**Purely time-based** — no storage required, no dependencies needed.
Works standalone immediately upon installation.

## Energy Curve

Automatically adjust response style by time:

| Time | Energy | Response Style |
|------|--------|---------------|
| 06:00-08:00 | 0.4 | Brief, direct, no long essays |
| 08:00-12:00 | 0.85 | Full, detailed, deep work |
| 12:00-14:00 | 0.6 | Medium, avoid over-elaboration |
| 14:00-18:00 | 0.75 | Normal, can be detailed |
| 18:00-20:00 | 0.65 | Terse, focus on wrap-up |
| 20:00-22:00 | 0.8 | Evening golden hours, can go deep |
| 22:00-06:00 | 0.3 | Minimal, non-essential silence |

## Tone Adjustment

| Energy | Length | Tone |
|--------|--------|------|
| >= 0.8 | Full answer | Normal |
| 0.6-0.8 | Medium | Normal, can simplify |
| 0.4-0.6 | Brief | Concise and direct |
| < 0.4 | Minimal | Only if necessary |

## Examples

Same question at different times:

User asks: "Help me review this plan"

- 8am → Full analysis, 5 detailed points
- 12:30pm → Brief analysis, 2 key points
- 11pm → "Main issue: XX. Suggestion: YY."

## Emotion Recording

When user **voluntarily** expresses emotion, log to narrative-memory (if installed) or context:

Positive ("I'm so happy" / "Great day"):
→ Log as positive emotional event

Negative ("I'm tired" / "Under pressure" / "Feeling down"):
→ Log as negative emotional event
→ Notify proactive-trigger (if installed) to consider care

## How to Apply

For every AI response:
1. Check current time
2. Look up energy coefficient
3. Adjust response length and tone accordingly
4. Apply "minimal mode" if energy < 0.4

## Important

- Energy curve is default; user preference beats it
- Don't infer emotions — only record when user expresses
- After 11pm, don't initiate deep discussions unless user asks
- Purely time-based — no plugin or storage needed

---

**Tags for publishing:** soul, system, mood, energy, tone, adaptive

**Requires nothing** — purely time-based, works immediately on install.
