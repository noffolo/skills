---
name: model-pilot
description: "Intelligent model routing and token cost optimization. Before every task, classify complexity and recommend the cheapest model that will deliver the same quality. Supports multi-provider model databases (Z.ai, OpenAI, Anthropic, Google) with pricing, benchmarks, and capability tiers. Prevents over-spending on powerful models for simple tasks. Use when: (1) user wants to save tokens or reduce costs, (2) starting any complex or expensive task, (3) switching models based on task type, (4) comparing model capabilities or pricing, (5) setting up cost-efficient model routing, (6) user asks 'is this the right model?', 'can a cheaper model do this?', or 'what model should I use?'. Homepage: https://clawhub.ai/skills/model-pilot"
---

# Model Pilot — Intelligent Model Routing & Cost Optimization

Stop overpaying for intelligence. Match every task to the cheapest model that delivers the quality you need.

**Install:** `clawhub install model-pilot`

## Language

Detect from user's message language. Default: English.

## When This Skill Activates

- User explicitly asks about model choice, cost, or token savings
- User says "save tokens", "cheaper model", "is this the right model?"
- A task is starting that would be expensive on the current model (agent judgment)
- Heartbeat/cron triggers periodic cost review

**This skill does NOT activate for trivial routing** — if the task is clearly simple (format a date, say hello), don't waste tokens analyzing it. Just do it.

---

## How It Works

### The Model Pilot Decision (takes ~5 seconds of thinking)

```
1. What is the task? (classify complexity)
2. What model is currently active?
3. Is there a cheaper model that can handle this task equally well?
4. If yes → recommend the switch with estimated savings
5. If no → proceed with current model, explain why it's warranted
```

**The check itself must be cheap.** Use heuristics (task type, prompt length, keywords), NOT trial runs with multiple models.

---

## Task Complexity Classification

### 🟢 Tier 1: Routine (Use Cheapest Model)

These tasks need basic competence, not brilliance.

**Task types:**
- Formatting (dates, numbers, lists, markdown tables)
- Simple Q&A (facts, definitions, lookups)
- Reminders and scheduling
- Short translations (single sentences, UI strings)
- Greetings and casual conversation
- Reading and summarizing short text (< 500 words)
- File operations (read, move, organize)
- Running pre-defined commands
- Weather lookups
- Simple math or unit conversion

**Appropriate models:** Bottom tier of available models.

**Signal:** Task can be completed in < 1000 output tokens. No creativity or deep reasoning required. Input is well-structured.

### 🟡 Tier 2: Intermediate (Use Mid-Tier Model)

These tasks need understanding and judgment, but not peak intelligence.

**Task types:**
- Email/message drafting and triage
- Code review (small changes, PR comments)
- Summarizing long documents (500-5000 words)
- Data analysis and interpretation
- Multi-step instructions (3-7 steps)
- Moderate translation (paragraphs, technical docs)
- Debugging (common errors, well-defined problems)
- Calendar management and scheduling conflicts
- Research synthesis (combining 2-3 sources)
- Skill writing and editing

**Appropriate models:** Middle tier of available models.

**Signal:** Task requires judgment or synthesis. Output likely 1000-5000 tokens. Multiple considerations to balance.

### 🔴 Tier 3: Complex (Use Best Available Model)

These tasks need peak intelligence. Don't cheap out here.

**Task types:**
- Architectural design (system, software, infrastructure)
- Complex debugging (subtle bugs, race conditions, memory issues)
- Creative writing (long-form, nuanced tone, storytelling)
- Deep research (10+ sources, cross-domain analysis)
- Multi-agent orchestration (sub-agent coordination)
- Complex code generation (new features, refactoring large codebases)
- Strategic planning and decision analysis
- Mathematical proofs or advanced reasoning
- Handling ambiguous requirements that need clarification intelligence
- Any task where a wrong answer is expensive

**Appropriate models:** Top tier of available models.

**Signal:** Task is ambiguous, requires creativity, has high stakes for wrong answers, or needs multi-step reasoning with backtracking. Output likely 5000+ tokens.

---

## Model Database

See `references/model-database.md` for the full provider-agnostic database with pricing, benchmarks, and capability tiers.

### Quick Reference: Recommended Routing

#### Z.ai / GLM Models

| Tier | Model | Input | Output | Best For |
|------|-------|-------|--------|----------|
| 🟢 Routine | GLM-4.7 (`zai/glm-4.7`) | Lowest | Lowest | Formatting, simple Q&A, reminders |
| 🟡 Intermediate | GLM-5 Turbo (`zai/glm-5-turbo`) | Medium | Medium | Code review, emails, analysis |
| 🔴 Complex | GLM-5.1 (`zai/glm-5.1`) | Highest | Highest | Architecture, deep reasoning, creative |

**Cost ratio:** GLM-4.7 → GLM-5 Turbo → GLM-5.1 is roughly **1x → 3x → 5x** in token cost.

**Note:** GLM-4.6V (`zai/glm-4.6v`) is for vision/image tasks — use when images are involved regardless of task complexity.

#### OpenAI Models

| Tier | Model | Best For |
|------|-------|----------|
| 🟢 Routine | GPT-4o-mini | Formatting, simple tasks |
| 🟡 Intermediate | GPT-4o | Analysis, code, general work |
| 🔴 Complex | o3 | Deep reasoning, math, hard problems |

#### Anthropic Models

| Tier | Model | Best For |
|------|-------|----------|
| 🟢 Routine | Claude Haiku | Formatting, simple tasks |
| 🟡 Intermediate | Claude Sonnet | Code, analysis, writing |
| 🔴 Complex | Claude Opus | Complex reasoning, long context |

#### Google Models

| Tier | Model | Best For |
|------|-------|----------|
| 🟢 Routine | Gemini Flash | Formatting, simple tasks |
| 🟡 Intermediate | Gemini Pro | Analysis, code |
| 🔴 Complex | Gemini Ultra | Complex reasoning, multimodal |

---

## Decision Flowchart

```
INCOMING TASK
     │
     ├─ Is it clearly routine? (formatting, simple Q&A, reminder)
     │    YES → 🟢 Recommend cheapest model
     │    "This is a routine task. [Cheapest model] will handle it fine
     │     and save you ~X% in token costs."
     │
     ├─ Does it involve images/vision?
     │    YES → Use vision-capable model (GLM-4.6V, GPT-4o, Claude Sonnet)
     │
     ├─ Is it complex? (architecture, creative, ambiguous, high-stakes)
     │    YES → 🔴 Current model is appropriate (if it's top-tier)
     │    "This task needs peak capability. Staying with [current model]
     │     is warranted."
     │
     └─ Is it intermediate? (most tasks fall here)
          YES → 🟡 Check if a mid-tier model is active
          If top-tier is active → recommend downgrade with savings estimate
          If mid-tier is active → proceed
```

---

## Presenting Recommendations

### When recommending a cheaper model:

```
💡 Model Pilot: This task looks like [tier] complexity.

Current model: [name] — [cost tier]
Recommended: [name] — [cost tier] (saves ~X% tokens)

I can switch for this task, or you can change it in settings.
What I'd lose: [specific capability gap, if any]
```

**Rules:**
- Always explain WHY the recommended model is sufficient
- Always mention what capability you'd lose (if anything)
- Never switch without user awareness (but can switch back without asking)
- Respect explicit model overrides — if user set a specific model, don't second-guess it for that session unless they ask

### When staying with current model:

```
✅ Model Pilot: [Current model] is the right choice for this.

This task requires [specific capability]. A cheaper model would
likely produce lower quality results for [specific reason].
```

---

## Cost Estimation

### Quick Math

```
Estimated tokens = input_tokens + estimated_output_tokens
Cost = (input_tokens × input_price + output_tokens × output_price) / 1,000,000
```

### Approximate Output Token Estimates by Task Type

| Task Type | Typical Output |
|-----------|---------------|
| Formatting | 50-200 tokens |
| Short answer | 100-500 tokens |
| Email draft | 500-1500 tokens |
| Code review | 500-2000 tokens |
| Analysis/summary | 1000-3000 tokens |
| Long-form writing | 2000-8000 tokens |
| Architecture/design | 3000-10000 tokens |
| Complex reasoning | 5000-15000 tokens |

### Savings Examples (Z.ai)

| Scenario | GLM-5.1 | GLM-5 Turbo | GLM-4.7 | Savings vs 5.1 |
|----------|---------|-------------|---------|-----------------|
| Format date (100 out) | ~$0.001 | ~$0.0005 | ~$0.0002 | ~80% |
| Draft email (1000 out) | ~$0.005 | ~$0.003 | ~$0.001 | ~80% |
| Code review (2000 out) | ~$0.010 | ~$0.006 | ~$0.002 | ~80% |
| Architecture (8000 out) | ~$0.030 | ~$0.015 | ~$0.008 | ~73% |

**Key insight:** For routine tasks, using GLM-4.7 instead of GLM-5.1 saves ~80% per task with negligible quality difference.

---

## Integration with OpenClaw

### Per-Session Model Override

OpenClaw supports per-session model overrides. The agent can use `session_status` with the model parameter to switch models for specific tasks.

### Configuring Available Models

Model Pilot works with whatever models the user has configured in their OpenClaw config. Check `agents.defaults.model` and model aliases to know what's available.

### Cron-Based Cost Review

Optional: Set up a weekly review that estimates token spend and recommends model adjustments:

```
Schedule: Weekly
Message: "Review this week's tasks and estimate token costs.
Were there tasks that used expensive models unnecessarily?
Suggest any model routing improvements."
```

---

## Edge Cases

### "I specifically chose this model"
→ Respect it. Don't recommend switching. The user knows what they want.

### "This is a test, accuracy matters more than cost"
→ Always recommend the best model regardless of task complexity.

### "I'm on a tight budget"
→ Default to recommending the cheapest model for everything. Only suggest upgrades when the task genuinely needs it.

### Mixed-complexity conversations
→ Some conversations start simple and become complex. Re-evaluate when the task shifts. Don't switch models mid-conversation unless the user asks.

### Sub-agent tasks
→ When spawning sub-agents, consider if they need the main session's model or a cheaper one. Coding agents might need top-tier, but research/analysis agents could use mid-tier.

---

## Anti-Patterns: When NOT to Optimize

**Don't recommend model switches when:**
- The task is already in progress
- The user has explicitly set a model override
- The cost difference is negligible (< $0.001)
- You're uncertain about the task complexity
- The user is debugging model behavior (they need consistency)

**Don't over-analyze:** The cost of analyzing which model to use should never exceed the savings. If unsure, just proceed with the current model.

---

## File Structure

```
model-pilot/
├── SKILL.md                      — This file
└── references/
    └── model-database.md         — Full model database with pricing & benchmarks
```

## More by TommoT2

- **tommo-skill-guard** — Security scanner + ClawHub Security Gate
- **setup-doctor** — Diagnose and fix OpenClaw setup issues
- **context-brief** — Optimize context window for longer conversations
- **skill-analytics** — Monitor ClawHub skill performance and adoption trends

Install the full efficiency suite:
```bash
clawhub install model-pilot tommo-skill-guard setup-doctor context-brief
```
