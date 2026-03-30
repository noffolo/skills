---
name: skill-drift-guard
description: Trust-then-verify integrity scanner for local repos and OpenClaw skills. Use when you want to scan before trust, save a trusted baseline, compare after updates, review drift since trust, and flag risky capability changes like shell, network, sensitive-path, prompt-injection, obfuscation, symlink, dependency, or install-hook drift.
---

# Skill Drift Guard

**Trust what you review. Compare what changed later.**

Use this skill for **local integrity checks** and **post-update drift detection** on repos or installed skills.

This skill is intentionally narrower than a generic security scanner. Its best use is:
- scan a local skill folder or repo before trust
- save a trusted baseline after review
- compare later to answer **what changed since trust**
- highlight risky new capabilities like shell, network, sensitive file access, symlinks, dependencies, or install hooks

## Quick start

Run the scanner directly from the installed skill folder:

```bash
node ./scripts/cli.js scan <path>
```

Save a trusted baseline after review:

```bash
node ./scripts/cli.js trust <path>
```

Save a trusted baseline to a custom location:

```bash
node ./scripts/cli.js trust <path> --baseline ./reports/skill-baseline.json
```

Compare a skill or repo against a saved baseline:

```bash
node ./scripts/cli.js compare <path> --baseline ./reports/skill-baseline.json
```

## Recommended workflow

### 1. Scan before trust
Review the candidate repo or skill first.

```bash
node ./scripts/cli.js scan /path/to/skill
```

Treat **high** or **critical** output as a stop sign until manually reviewed.

### 2. Trust after review
If the findings are acceptable, save a trusted baseline.

```bash
node ./scripts/cli.js trust /path/to/skill
```

### 3. Compare after updates
After the skill changes or updates, compare it to the saved baseline.

```bash
node ./scripts/cli.js compare /path/to/skill --baseline ./reports/baseline.json
```

Look especially for:
- newly added or changed files
- new shell or network findings
- dependency or install-hook drift
- new symlinks or sensitive file references

## What it checks

- risky shell execution patterns like `curl | bash`, `eval`, `exec`, `subprocess`, `os.system`
- outbound network patterns like `fetch`, `axios`, `requests`, `curl`, webhook usage
- references to sensitive files like `.env`, SSH keys, `SOUL.md`, `MEMORY.md`, OpenClaw config
- prompt injection style content in `SKILL.md`, `SOUL.md`, `MEMORY.md`
- obfuscation hints like base64 helpers and long encoded blobs
- symlink drift without following symlinks
- dependency drift in `package.json`, `requirements.txt`, and `pyproject.toml`
- install-hook changes in `package.json`
- combo risks like:
  - shell + network
  - network + sensitive files
  - shell + prompt-injection signals
  - obfuscation + active capabilities

## Config suppressions

Use a `.driftguard.json` file in the scan root, or pass `--config <file>`.

Example:

```json
{
  "ignorePaths": ["dist/", "fixtures/"],
  "ignoreRules": ["net.fetch", "shell.exec_generic", "shell.*"]
}
```

Use suppressions sparingly. If a rule is noisy, prefer narrowing it later instead of muting the whole category.

## Exit codes

- `0` for low risk and no drift
- `1` for medium risk or drift detected
- `2` for high or critical risk

Use this for CI or install gating.

## Positioning

Use this skill when you want a **transparent, local, deterministic trust workflow**.
Do not use it as the sole authority for safety. It is a heuristic scanner plus drift guard, not a guarantee.
