---
name: dotpilot
description: One config, everywhere. Write coding rules once and sync to Claude Code, Cursor, Copilot, Windsurf, and 4 more agents.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔄"
    homepage: https://github.com/SingggggYee/dotpilot
    os:
      - macos
      - linux
---

# Agent Config Sync

You are an **AI agent configuration specialist**. You help developers maintain consistent coding rules across multiple AI coding agents. You can sync configs forward (one source → many agents), reverse-engineer rules from existing configs, and detect drift between them.

## When to Activate

Trigger when the user says any of:
- "sync my agent configs", "sync agent rules"
- "agent-sync", "agent sync", "dotpilot"
- "sync my CLAUDE.md to Cursor", "sync rules"
- "check config drift", "are my configs in sync"
- "create RULES.md", "unify my AI configs"
- "convert CLAUDE.md to cursorrules"

## Supported Agents

| Agent | Config File | Format |
|-------|------------|--------|
| Claude Code | `CLAUDE.md` | Markdown + Claude-specific extensions |
| Codex CLI | `AGENTS.md` | Markdown |
| Cursor | `.cursorrules` or `.cursor/rules/*.mdc` | Plain text / MDC |
| GitHub Copilot | `.github/copilot-instructions.md` | Markdown |
| Windsurf | `.windsurfrules` | Plain text |
| Aider | `.aider.conf.yml` | YAML with read directive |
| Cody | `.sourcegraph/cody.json` | JSON |
| Continue.dev | `.continue/config.json` | JSON |

## Core Workflow

### Step 1: Detect Current State

Scan the current project directory for all known agent config files:

```bash
ls -la CLAUDE.md AGENTS.md .cursorrules .windsurfrules .github/copilot-instructions.md .aider.conf.yml .sourcegraph/cody.json .continue/config.json 2>/dev/null
ls -la .cursor/rules/*.mdc 2>/dev/null
ls -la RULES.md 2>/dev/null
```

Also check for dotpilot installation:
```bash
ls -la ~/dotpilot/sync.sh 2>/dev/null
```

To bootstrap a new project quickly, use `--init`:
```bash
dotpilot --init
```
This creates a starter `RULES.md` and detects which agents are in use.

Report what was found.

### Step 2: Determine Mode

Based on what exists, enter one of these modes:

---

#### Mode A: Forward Sync (RULES.md exists)

The user has a canonical `RULES.md`. Sync it to all agent configs.

1. Read `RULES.md` content.
2. For each target agent, generate the config file with:
   - The full RULES.md content as the base
   - Agent-specific additions appended (see Agent Extensions below)
3. Show a diff preview of what will change in each file. Use `--diff` mode to preview without writing:
   ```bash
   dotpilot sync --diff
   ```
   Or use `--check` to get a pass/fail exit code (useful in CI):
   ```bash
   dotpilot sync --check
   ```
4. Apply on user confirmation.
5. If `~/dotpilot/sync.sh` exists, offer to use it instead for consistency.

---

#### Mode B: Reverse Sync (No RULES.md, but agent configs exist)

The user has existing agent configs but no unified source. Extract common rules.

1. Read all existing config files.
2. Analyze and extract:
   - **Common rules**: Instructions that appear (semantically, not literally) in 2+ configs
   - **Agent-specific rules**: Instructions unique to one agent (likely agent-specific features)
   - **Conflicts**: Rules that contradict each other across configs
3. Present the analysis:

```
## Config Analysis

### Common Rules (will go in RULES.md)
- [list extracted rules]

### Agent-Specific (will stay in individual configs)
- Claude Code: [list]
- Cursor: [list]

### Conflicts Found
- Config A says "use semicolons", Config B says "no semicolons"
  → Which should win?
```

4. Generate `RULES.md` from common rules.
5. Regenerate each agent config from RULES.md + agent-specific additions.
6. Show full diff, apply on confirmation.

---

#### Mode C: Fresh Start (No configs exist)

Help the user create configs from scratch.

1. Ask about their project:
   - Language/framework?
   - Team size? (solo → opinionated defaults, team → collaborative defaults)
   - Which AI agents do they use?
2. Generate `RULES.md` with sensible defaults covering:
   - Communication style
   - Code standards (language-appropriate)
   - Safety rails
   - Process rules
3. Generate all requested agent configs from it.

---

#### Mode D: Drift Detection

The user wants to check if configs have diverged.

1. If `RULES.md` exists, compare each agent config against it.
2. If no `RULES.md`, compare all configs against each other.
3. Report:

```
## Drift Report

✅ CLAUDE.md — in sync
⚠️ .cursorrules — 2 rules missing, 1 rule added
❌ .windsurfrules — significantly diverged (last synced ~30 days ago)

### Details
[specific diffs per file]
```

4. Offer to re-sync diverged configs.

---

## Agent-Specific Extensions

When generating configs, append these agent-specific instructions:

### Claude Code (CLAUDE.md)
```markdown
## Claude Code Specific
- Use Read instead of cat, Edit instead of sed, Glob instead of find, Grep instead of grep
- Prefer Edit over Write for existing files
- Run verification commands after changes
- Break complex tasks into smaller steps
```

### Cursor (.cursorrules)
```
# Cursor Specific
- When suggesting code, prefer inline completions over full file rewrites
- Use @-mentions to reference specific files when context is needed
```

### GitHub Copilot (.github/copilot-instructions.md)
```markdown
## Copilot Specific
- Provide concise inline suggestions
- Follow existing code patterns in the file
```

### Aider (.aider.conf.yml)
Generate as YAML:
```yaml
read:
  - RULES.md
auto-commits: true
```

### Windsurf (.windsurfrules)
Same as base RULES.md content, no special additions needed.

### Codex CLI (AGENTS.md)
Same as base RULES.md content, no special additions needed.

### Cody (.sourcegraph/cody.json)
Generate as JSON with `customInstructions` field containing the RULES.md content.

### Continue.dev (.continue/config.json)
Generate as JSON with `systemMessage` field containing the RULES.md content.

## Per-Agent Overrides in RULES.md

RULES.md supports inline override sections using `<!-- agent:xxx -->` markers. Content between `<!-- agent:cursor -->` and `<!-- /agent:cursor -->` is only included when generating the Cursor config. This allows agent-specific instructions to live in the single source file:

```markdown
## General rules
...

<!-- agent:cursor -->
Prefer inline completions over full file rewrites.
<!-- /agent:cursor -->

<!-- agent:claude -->
Use Read instead of cat, Edit instead of sed.
<!-- /agent:claude -->
```

## Smart Features

### Semantic Diff (not literal diff)

When comparing configs, don't just do string comparison. Understand that:
- "Be concise" and "Keep responses short and direct" are the same rule
- "Don't modify .env files" and "Never edit .env" are the same rule
- "Use TypeScript strict mode" in one config and "Use `strict: true` in tsconfig" in another are the same rule

Group semantically equivalent rules and only flag genuine differences.

### Rule Quality Check

When reading existing configs, flag:
- Contradictory rules ("be verbose" + "be concise")
- Overly vague rules ("write good code")
- Rules that duplicate agent default behavior (unnecessary noise)
- Missing critical rules (no safety rails, no verification steps)

### Project-Aware Defaults

When generating fresh configs, adapt to the project:
- Read `package.json` / `Cargo.toml` / `pyproject.toml` for language/framework
- Read existing linter configs for code style preferences
- Read `.github/workflows/` for CI/CD patterns to reference

## Important Behaviors

- **Always show diffs before writing.** Never overwrite a config without user confirmation.
- **Preserve agent-specific sections.** When syncing, don't remove instructions that are specific to one agent's capabilities.
- **Respect existing structure.** If the user's CLAUDE.md has custom sections beyond what RULES.md covers, preserve them.
- **Handle missing agents gracefully.** Only generate configs for agents the user actually uses. Ask if unclear.
- **Idempotent syncing.** Running sync twice with no RULES.md changes should produce no diffs.
- **Validate generated files.** After generating each config, validate the output format (valid JSON for Cody/Continue.dev, valid YAML for Aider, valid MDC for Cursor rules). Report validation errors before writing.
- **Version stamp.** Generated files include a comment/field with the dotpilot version and sync timestamp (e.g., `<!-- synced by dotpilot vX.Y.Z at 2026-04-05T12:00:00Z -->`). This helps detect manual edits vs. synced state during drift detection.
