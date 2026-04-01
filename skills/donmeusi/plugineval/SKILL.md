---
name: plugineval
version: 1.2.0
description: PluginEval Quality Evaluation for AI agent skills. Measures 6 dimensions, detects anti-patterns, and assigns quality badges. Read-only by default - auto-fix requires explicit --allow-write flag.
---

# PluginEval 🔬

Quality evaluation framework for AI agent skills. Measures skill quality across 6 dimensions and detects common anti-patterns. **Read-only by default** - file modifications require explicit opt-in.

## Use When

- Evaluating skill quality before installation
- Checking installed skills for quality issues
- Improving skills to meet quality standards
- Publishing skills to ClawHub with quality badges

## Security Model

| Mode | Command | File Access |
|------|---------|-------------|
| **Read-Only** (default) | `--layer1`, `--layer2`, `--anti-patterns` | READ ONLY |
| **Preview** | `--auto-fix --dry-run` | READ ONLY (shows what would change) |
| **Write** | `--auto-fix --allow-write` | Creates backup, modifies SKILL.md only |

**Safeguards:**
- Only modifies `SKILL.md` (never other files)
- Creates `.backup-YYYYMMDD-HHMMSS.md` before any change
- Requires `--allow-write` flag (never auto-executes)
- Maximum 3 backups per skill (auto-cleanup)

## Quality Dimensions

| Dimension | Weight | What it Measures |
|-----------|--------|------------------|
| **Frontmatter Quality** | 35% | Name, description, trigger phrase |
| **Orchestration Wiring** | 25% | Input/Output documentation, examples |
| **Progressive Disclosure** | 15% | Conciseness, layered information |
| **Structural Completeness** | 10% | Headings, troubleshooting, examples |
| **Token Efficiency** | 6% | Directive count, duplication |
| **Ecosystem Coherence** | 2% | Cross-references to related skills |

## Quality Badges

| Badge | Score | Grade | Meaning |
|-------|-------|-------|---------|
| Platinum ★★★★★ | ≥90 | A | Reference Quality - install freely |
| Gold ★★★★ | ≥80 | B | Production Ready - minor polish needed |
| Silver ★★★ | ≥70 | C | Functional - improvements recommended |
| Bronze ★★ | ≥60 | D | Minimum Viable - review before install |
| Needs Improvement ★ | <60 | F | Requires Work - do not install |

## Anti-Patterns

| Pattern | Penalty | Description |
|---------|---------|-------------|
| OVER_CONSTRAINED | 10% | >15 MUST/ALWAYS/NEVER directives |
| EMPTY_DESCRIPTION | 10-50% | Description <20 chars |
| MISSING_TRIGGER | 15% | No "Use when..." trigger phrase |
| BLOATED_SKILL | 10% | >800 lines without references/ |
| ORPHAN_REFERENCE | 5% | Empty reference file |
| DEAD_CROSS_REF | 5% | Reference to non-existent skill |

## Input / Output

**Input:** Skill directory containing SKILL.md

**Output:** Quality score, badge, grade, anti-patterns

## Quick Start

```bash
# Layer 1: Static Analysis
skill-eval.py --layer1 ~/.openclaw/skills/weather-pollen

# Anti-Pattern Detection
skill-eval.py --anti-patterns ~/.openclaw/skills/weather-pollen

# Deep Evaluation (Layer 1 + LLM Judge)
skill-eval.py --deep ~/.openclaw/skills/weather-pollen

# Combined Security + Quality
vet-skill.sh weather-pollen
```

## Examples

### Evaluate a Skill

```bash
skill-eval.py --layer1 ~/.openclaw/skills/openai-whisper

# Output:
# [1/6] Frontmatter Quality (35%)
#   ✓ Has name/title: openai-whisper...
#   ✓ Description adequate (159 chars)
#   ✓ Has trigger phrase
#   Score: 100/100
# 
# [2/6] Orchestration Wiring (25%)
#   ✓ Documents output
#   ✓ Documents input
#   ✓ Has code examples
#   Score: 100/100
# ...
# 
# === Final Score ===
# Weighted: 91.5
# Penalty: 100.0%
# Final: 92
# Badge: Platinum ★★★★★
# Grade: A-
```

### Improve a Skill

1. Run evaluation: `skill-eval.py --layer1 <skill-dir>`
2. Check anti-patterns: `skill-eval.py --anti-patterns <skill-dir>`
3. Fix issues identified
4. Re-run until score ≥70

### Auto-Fix Anti-Patterns

```bash
# Preview fixes (dry run - read only)
skill-eval.py --auto-fix --dry-run <skill-dir>

# Apply safe fixes (requires explicit opt-in)
skill-eval.py --auto-fix --allow-write <skill-dir>

# Apply all fixes including unsafe
skill-eval.py --auto-fix --allow-write --unsafe <skill-dir>
```

**Safe Auto-Fixes:**
- `EMPTY_DESCRIPTION` — Generates description from skill content
- `MISSING_TRIGGER` — Adds "Use when..." trigger phrase
- `ORPHAN_REFERENCE` — Removes empty reference files

**Requires `--unsafe`:**
- `OVER_CONSTRAINED` — Too many MUST/NEVER/ALWAYS directives (needs review)
- `BLOATED_SKILL` — Skill too large (needs manual splitting)
- `DEAD_CROSS_REF` — References to non-existent skills (needs verification)

**Safeguards:**
- `--allow-write` required (never auto-executes)
- Only modifies `SKILL.md` (no other files)
- Creates timestamped backup before changes
- Maximum 3 backups per skill (auto-cleanup)

### Combined Workflow

```bash
# Security + Quality in one call
vet-skill.sh weather-pollen

# [1/3] Security Scan (ClawDefender)
#   ✓ Clean
# [2/3] Quality Evaluation (PluginEval)
#   Final: 81 | Badge: Gold ★★★★
# [3/3] Anti-Pattern Detection
#   ✓ No anti-patterns detected
```

## Integration

### Before Publishing

```bash
# Check quality before publishing to ClawHub
skill-eval.py --layer1 <skill-dir>
# Score should be ≥70 before publishing
```

## Related Skills

- `skill-vetter` — Security vetting before skill installation
- `clawdefender` — Security scanning for malicious patterns

## Changelog

### v1.1.0 (2026-03-31)
- Added Layer 3: Auto-Fix for anti-patterns
- `--auto-fix`: Automatically fix issues
- `--dry-run`: Preview without changes
- `--safe-only`: Only safe fixes (default)
- `--unsafe`: Allow all fixes
- Auto-backup before changes

### v1.0.1 (2026-03-31)
- Removed automation-specific section (universally usable)
- Cleaner documentation

### v1.0.0 (2026-03-31)
- Initial release
- 6 Quality Dimensions (Frontmatter, Orchestration, Progressive Disclosure, Structural Completeness, Token Efficiency, Ecosystem Coherence)
- 6 Anti-Patterns detection
- Quality Badges (Platinum/Gold/Silver/Bronze/Needs Improvement)

---

*Based on wshobson/agents PluginEval specification.*
