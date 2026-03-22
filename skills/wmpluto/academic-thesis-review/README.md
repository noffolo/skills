# Academic Thesis Review Skill

[简体中文](README.zh-CN.md)

Reusable agent skill for reviewing Chinese management-oriented master's theses in multiple rounds.

## Overview

This repository packages a reusable thesis-review skill for agent frameworks such as:

- OpenCode
- OpenClaw
- Claude Code
- Other markdown-based prompt/skill loaders

The skill focuses primarily on **Chinese management-oriented master's theses** — especially programs such as **MBA**, **MEM**, and **MPA** — and also works well for other similar professional or applied research master's theses.

It uses a **3-round review strategy**:

1. Macro structure review
2. Per-chapter deep review
3. Inter-chapter consistency review

It is designed to generate **strict but actionable** revision feedback in Chinese.

## Multi-round Review Support

Yes — this skill explicitly supports **multi-round review workflows**.

- **Round 1:** macro structure and overall logic
- **Round 2:** chapter-by-chapter deep review
- **Round 3:** inter-chapter consistency review
- **Iterative re-review:** if an existing `review_results.md` is present, the skill can verify whether previously flagged issues were fixed, partially fixed, or left unchanged

This makes it suitable not only for a first-pass review, but also for **revision follow-up and repeated review cycles**.

## Files

- `SKILL.md` — canonical cross-platform skill entry with metadata frontmatter
- `skill.json` — repository-level metadata for publishing and later automation
- `.gitignore` — recommended ignore rules for local temp outputs

## Supported Agent Use Cases

This skill is intended for agent systems that can load or reference a markdown instruction file as a reusable skill, command, prompt, or workflow definition.

Recommended scope:

- MBA theses
- MEM theses
- MPA theses
- Other management, public administration, engineering management, and similarly structured applied master's theses

Typical use cases:

- Review a `.docx` thesis draft
- Re-review a revised thesis against prior comments
- Produce a structured `review_results.md`

## Installation

Because different agent frameworks organize skills differently, use one of these approaches:

### Option 1: Direct file use

Point your agent system to `SKILL.md` directly.

### Option 2: Copy into your skill directory

Copy this folder into the target framework's local skills/prompts directory and register it according to that framework's conventions.

#### Claude Code

Personal install:

```bash
mkdir -p ~/.claude/skills/academic-thesis-review
cp -r . ~/.claude/skills/academic-thesis-review
```

Project install:

```bash
mkdir -p .claude/skills/academic-thesis-review
cp -r . .claude/skills/academic-thesis-review
```

#### OpenClaw

Suggested global install:

```bash
mkdir -p ~/.openclaw/skills/academic-thesis-review
cp -r . ~/.openclaw/skills/academic-thesis-review
```

#### OpenCode / compatible prompt loaders

Use `SKILL.md` as the imported markdown asset.

### Option 3: Reference this GitHub repository

Upload this folder to GitHub, then use the raw markdown or repository contents wherever your agent platform accepts remote or synced prompt assets.

## Suggested Trigger Phrases

- 审阅论文
- review thesis
- 论文评审
- 帮我看看论文
- 修改后再看看

## Inputs Expected by the Skill

- Thesis file in `.docx` format
- Python available for text extraction
- Optional existing `review_results.md` for iterative review mode

## Output

- Markdown review report
- Recommended filename: `review_results.md`

## Repository Metadata

- Author GitHub: https://github.com/wmpluto
- Repository URL: `https://github.com/wmpluto/academic-thesis-review-skill`
- Homepage / docs URL: `https://github.com/wmpluto/academic-thesis-review-skill`

## Publishing Notes

- `SKILL.md` is the canonical file for ecosystems following the Agent Skills style convention.
- On Windows, case-only duplicate filenames such as `SKILL.md` and `skill.md` cannot reliably coexist, so this package standardizes on `SKILL.md`.
- `skill.json` is a generic metadata file for publishing convenience. It is not assumed to be required by every agent framework.
- Replace remaining placeholder values only if you later add a separate homepage or documentation site.

## Notes

- If you later decide to target a specific platform with a strict manifest format, add that platform-specific file separately instead of replacing `SKILL.md`.
