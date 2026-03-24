---
name: agent-cost-strategy
description: Tiered model selection and cost optimization for multi-agent AI workflows. Use this skill whenever you are choosing a model for a task, spinning up a sub-agent, setting up cron jobs or heartbeats, or trying to reduce API spend. Also use when the user says "save costs", "which model should I use", "optimize model usage", "this is getting expensive", or when delegating any task to a sub-agent. Works with any AI provider.
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

# Agent Cost Strategy

Use the cheapest model that can reliably do the job. Most tasks don't need your most powerful model.

## The Three Tiers

| Tier | When to Use | Examples |
|------|-------------|---------|
| **Fast/Cheap** | Sub-agents, background tasks, automated fixes, simple lookups, short replies | Claude Haiku, GPT-4o-mini, Gemini Flash |
| **Mid-tier** | Main session dialogue, moderate reasoning, multi-step tasks | Claude Sonnet, GPT-4o, Gemini Pro |
| **Powerful** | Architecture decisions, deep reviews, hard problems, after cheaper models fail twice | Claude Opus, GPT-4.5, Gemini Ultra |

## Task → Tier Routing

```
Fix failing tests          → Fast/Cheap
Write boilerplate          → Fast/Cheap
Research / search          → Fast/Cheap
Cron / scheduled tasks     → Fast/Cheap (always)
Short replies (hi, ok)     → Fast/Cheap (always)
Background monitoring      → Fast/Cheap (always)
Build new feature          → Mid-tier
Review a PR                → Mid-tier
Main assistant dialogue    → Mid-tier (default)
Architecture decisions     → Powerful
Deep code review           → Powerful
Stuck after 2 attempts     → Escalate one tier up
```

## Heartbeat / Cron Model Rule

Always specify the cheapest model for scheduled and background tasks — they run frequently and costs add up fast. Check your platform's config for how to set a model per cron/heartbeat job.

For heartbeat intervals: set them just under your provider's cache TTL to keep the prompt cache warm and pay cache-read rates instead of full input rates. Check your provider's docs for the exact TTL.

## Communication Pattern Rule

One-word and short conversational messages (hi, thanks, ok, sure, yes, no) should always route to Fast/Cheap. Never burn a mid-tier or powerful model on an acknowledgment.

## Cache Optimization

Prompt caching cuts costs 50-90% on repeated context. See `references/cache-optimization.md` for patterns.

## Signs You're Over-Spending

- Running powerful models on tasks Fast/Cheap can handle
- No caching on repeated system prompts
- Heartbeat/cron jobs using the default (expensive) model
- Spawning sub-agents without specifying a model tier

## Session & Cache Management

**Never delete or end sessions to "save money" — it backfires.**

Anthropic's prompt cache builds from repeated context within a live session. When a session starts fresh, all context (system prompt, workspace files, skills) loads cold — typically 400-600k tokens at full cost. Once cached, subsequent messages cost ~10% of that.

**The math:**
- Cold session start: 600k tokens × full price = expensive
- After cache warms up: 600k tokens × 10% cache price = ~90% cheaper per message
- Deleting a session destroys the cache and forces a full cold reload next time

**Rules:**
- Let sessions run as long as possible
- Only start a new session (`/new`) when context is genuinely full (>80%)
- Never tell a user to delete conversations — it spikes costs
- The longer a session runs, the cheaper each message gets

**Delegation rule (keep main agent lean):**
- Main agent (Sonnet/mid-tier) = conversational only: planning, coordination, reviewing results
- Sub-agents (Haiku/fast-cheap) = all actual doing: file edits, research, builds, data tasks
- Keeping the main agent conversational reduces its context growth and keeps cache hits high
