---
name: lucid-dreamer
description: "Nightly AI memory reasoning system. Lucid runs every night while you sleep — it reads your daily notes and memory files, detects stale facts, unresolved todos, recurring problems, and forgotten decisions, then generates a review report for your approval. Zero dependencies, no database, no embeddings. Just a cron job and markdown files. Use when you want your AI agent to automatically maintain and improve its long-term memory over time. Triggers on \"memory dreamer\", \"nightly memory review\", \"lucid\", \"auto memory\", \"memory cleanup\", \"memory hygiene\"."
metadata:
  openclaw:
    requires:
      bins:
        - git
        - date
      env:
        CLAWD_DIR: "required — workspace path (e.g. /home/user/clawd)"
    always: false
---

# Lucid Dreamer 🧠

> *Your AI sleeps. Lucid dreams.*

Lucid keeps your AI's memory clean. Every night, it reads what happened, checks what your AI already knows, and suggests what's outdated, missing, or forgotten.

See `README.md` for full setup, `ARCHITECTURE.md` for internals, and `config/` for configuration.

## Quick Setup

1. Set your workspace path in the config:
   ```bash
   export CLAWD_DIR=/path/to/your/workspace
   ```

2. Create a nightly cron job using OpenClaw's cron tool — run the prompt in `prompts/nightly-review.md` at 3 AM.

3. Wake up to a review report in `memory/review/YYYY-MM-DD.md`.

4. Approve or reject suggestions — Lucid tracks state in `memory/review/state.json`.

## Files

- `prompts/nightly-review.md` — the main nightly review prompt
- `config/` — thresholds and behavior settings
- `examples/` — sample review output and state file

## Security

**Files read at runtime:**
- `MEMORY.md` — long-term agent memory summary
- `USER.md` — user profile and preferences
- Last 7 daily notes (`memory/YYYY-MM-DD.md`)

**Files written at runtime:**
- `memory/review/YYYY-MM-DD.md` — the generated review report
- `memory/review/state.json` — approval/rejection tracking state

**What this skill never does:**
- Never reads or outputs API keys, tokens, or credentials
- Never accesses files outside the configured workspace directory
- Never pushes to remote git automatically — all commits are local only, and no `git push` is performed unless you explicitly run it
- Announce/notification delivery is opt-in and off by default — no messages are sent without explicit configuration

**Recommendations:**
- Set `CLAWD_DIR` explicitly in your environment to ensure the skill operates on the correct workspace
- Review generated reports before approving suggestions — Lucid proposes changes, but you remain in control
