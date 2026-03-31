---
name: context-hawk
description: |
  Context-Hawk 🦅 — AI Context Memory Guardian. Solves AI amnesia: automatically captures what matters, lets noise fade with Weibull decay, recalls the right memory at the right time. Four-tier memory (Working/Short/Long/Archive), 5 compression strategies, 5 injection policies, self-introspection, LanceDB vector search. No database needed, pure-memory fallback. Activates on: memory too big, MEMORY management, context compression, layered memory, lanceDB, importance scoring, context injection, task state, session resume.
---

# Context-Hawk 🦅 — AI Context Memory Guardian

Enterprise-grade context memory management for AI agents. Works with any AI agent — universal, no business logic, open source.

---

## What It Does

Unlike a memory database, Context-Hawk manages **structured memory** that survives sessions:

- **Persistent task state**: `hawk resume` continues from where you left off, even after restart
- **Four-tier memory**: Working → Short-term → Long-term → Archive with Weibull decay
- **Structured JSON memories**: importance, category, tier, L0/L1/L2 layers
- **5 context injection strategies**: dynamically control how much memory enters context
- **5 compression strategies**: summarize / extract / delete / promote / archive
- **Self-introspection**: knows when it's missing information or stuck
- **LanceDB ready**: vector search + BM25 hybrid retrieval (optional)
- **Pure-memory fallback**: works without LanceDB, JSONL persistence

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── Current session (recent 5-10 turns)     │
│       ↓ Weibull decay                                        │
│  Short-term      ←── 24h content, summarized                 │
│       ↓ access_count ≥ 10 + importance ≥ 0.7               │
│  Long-term       ←── Permanent, vector-indexed               │
│       ↓ >90 days or decay_score < 0.15                      │
│  Archive          ←── Historical, loaded on-demand             │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── Persistent across restarts            │
│  - Current task / next steps / progress / outputs            │
├──────────────────────────────────────────────────────────────┤
│  Injection Engine  ←── Strategy A/B/C/D/E decides recall      │
│  Self-Introspection ←── Every answer checks context          │
└──────────────────────────────────────────────────────────────┘
```

---

## Core Capabilities

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Task State Persistence** | `hawk resume` — persist task, resume after restart |
| 2 | **4-Tier Memory** | Working → Short → Long → Archive with Weibull decay |
| 3 | **Structured JSON** | Importance/category/tier/L0/L1/L2 metadata |
| 4 | **AI Importance Scoring** | Auto-score 0-10, discard noise |
| 5 | **5 Injection Strategies** | A(high-imp)/B(task)/C(recent)/D(top5)/E(full) |
| 6 | **5 Compression Strategies** | summarize/extract/delete/promote/archive |
| 7 | **Self-Introspection** | Detects missing info, loops, unclear tasks |
| 8 | **LanceDB Integration** | Optional vector + BM25 hybrid search |
| 9 | **Pure-Memory Fallback** | No database required, JSONL files |
| 10 | **Auto-Dedup** | Duplicate memories merged automatically |

---

## Auto-Trigger: Every N Rounds

Every **10 rounds** (configurable), Context-Hawk automatically:

1. Checks context water level
2. Evaluates memory importance
3. Triggers compression if needed
4. Reports status to user

```bash
# Config (in .hawk-config)
{
  "auto_check_rounds": 10,    # check every N rounds
  "auto_compress_threshold": 70  # compress when > 70%
}
```

---

## Quick Start

```bash
# Install skill
openclaw skills install ./context-hawk.skill

# Auto-link hawk command to ~/bin (one-time)
bash ~/.openclaw/workspace/skills/context-hawk/scripts/install.sh
source ~/.bashrc

# Initialize
hawk init

# Core commands
hawk task "My task"       # create task
hawk resume               # resume after restart (CORE!)
hawk status             # view context usage
hawk compress           # compress memory
hawk strategy B         # switch injection strategy
hawk introspect         # self-introspection report
```

---

## References

| Document | Purpose |
|----------|---------|
| [references/memory-system.md](references/memory-system.md) | 4-tier architecture |
| [references/structured-memory.md](references/structured-memory.md) | Memory format + importance |
| [references/task-state.md](references/task-state.md) | Task state persistence |
| [references/injection-strategies.md](references/injection-strategies.md) | 5 injection strategies |
| [references/compression-strategies.md](references/compression-strategies.md) | 5 compression strategies |
| [references/alerting.md](references/alerting.md) | Alert system |
| [references/self-introspection.md](references/self-introspection.md) | Self-introspection |
| [references/lancedb-integration.md](references/lancedb-integration.md) | LanceDB integration |
| [references/split-patterns.md](references/split-patterns.md) | Memory splitting |
| [references/cli.md](references/cli.md) | CLI reference |
