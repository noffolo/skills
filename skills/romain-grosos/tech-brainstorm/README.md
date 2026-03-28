# 🧠 openclaw-skill-tech-brainstorm

> OpenClaw skill - Multi-source technical research + contextual brainstorm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-blue)](https://openclaw.ai)
[![Python](https://img.shields.io/badge/Python-3.9%2B-brightgreen)](https://python.org)
[![Zero deps](https://img.shields.io/badge/deps-zero%20(stdlib%20only)-success)]()

Research technical topics, synthesize state of the art, and produce context-aware architecture recommendations with pros/cons/effort. Conversational - triggered from Telegram or CLI. Sources cited with links, not a black-box synthesis.

## Install

```bash
clawhub install tech-brainstorm
```

Or manually:

```bash
git clone https://github.com/Rwx-G/openclaw-skill-tech-brainstorm \
  ~/.openclaw/workspace/skills/tech-brainstorm
```

## Setup

```bash
python3 scripts/setup.py             # configure LLM + settings
python3 scripts/setup.py --manage-outputs  # configure dispatch (Telegram, Nextcloud, email)
python3 scripts/init.py              # validate config + API key
python3 scripts/init.py --test-llm   # test LLM connectivity
```

Requires an LLM API key (OpenAI or compatible). No other credentials needed for core functionality.

## Quick start

```bash
# Simple brainstorm (LLM only)
python3 scripts/tech_brainstorm.py brainstorm \
  --topic "k8s on-prem" \
  --context "AWX + Terraform, 10 applis hebergees, equipe 3 personnes"

# Full pipeline with dispatch
python3 scripts/tech_brainstorm.py run \
  --topic "k8s on-prem" \
  --context "AWX + Terraform, 10 applis hebergees, equipe 3 personnes"

# With web research on stdin
echo '[{"url":"https://...","title":"...","content":"..."}]' \
  | python3 scripts/tech_brainstorm.py brainstorm \
    --topic "k8s on-prem" --context "..."
```

## What it does

| Step | Details |
|------|---------|
| Research | Agent gathers web sources (docs, comparisons, community posts) |
| Synthesis | State of the art: technologies, trends, friction points, sources cited |
| Brainstorm | 3-5 concrete options crossed with your context: pros/cons/effort each |
| Dispatch | Telegram recap + Nextcloud/email/file full report |

## What makes it different

- **Conversational** - no CLI required, trigger from Telegram
- **Context-aware** - your stack, team size, and constraints shape the recommendations
- **Sources cited** - links included, not a generic synthesis
- **Adaptive output** - short recap for Telegram, full report for cloud/email

## CLI reference

```bash
# Generate brainstorm (optional: sources JSON on stdin)
python3 scripts/tech_brainstorm.py brainstorm --topic "..." [--context "..."]

# Full pipeline: brainstorm + dispatch
python3 scripts/tech_brainstorm.py run --topic "..." [--context "..."] [--profile NAME]

# Dispatch report (stdin JSON) to configured outputs
python3 scripts/tech_brainstorm.py send [--profile NAME]

# Show active config
python3 scripts/tech_brainstorm.py config
```

## Output format

```json
{
  "topic": "k8s on-prem",
  "context": "AWX + Terraform, 10 apps, 3 personnes",
  "report": "# Etat de l'art\n...\n# Pistes concretes\n...\n# Recommandation\n...",
  "recap": "🧠 *Brainstorm: k8s on-prem*\n3 pistes analysees...",
  "sources_count": 5,
  "model": "gpt-4o-mini",
  "timestamp": "2026-03-28T10:00:00+00:00"
}
```

## Configuration

Config file: `~/.openclaw/config/tech-brainstorm/config.json`

### LLM

```json
{
  "llm": {
    "enabled": true,
    "base_url": "https://api.openai.com/v1",
    "api_key_file": "~/.openclaw/secrets/openai_api_key",
    "model": "gpt-4o-mini",
    "max_tokens": 4096,
    "temperature": 0.7
  }
}
```

Compatible: OpenAI, Azure OpenAI, Ollama, LM Studio, vLLM, any OpenAI-compatible API.

### Outputs

```bash
python3 scripts/setup.py --manage-outputs
```

Types: `telegram_bot` (recap), `mail-client` (HTML report), `nextcloud` (Markdown), `file` (local).

## File structure

```
openclaw-skill-tech-brainstorm/
  SKILL.md                   # OpenClaw skill descriptor
  README.md                  # This file
  config.example.json        # Example config
  .gitignore
  references/
    troubleshooting.md
  scripts/
    tech_brainstorm.py       # Main CLI (brainstorm, run, send, config)
    _llm.py                  # LLM API client (OpenAI-compatible)
    _dispatch.py             # Output dispatcher (Telegram, email, Nextcloud, file)
    _retry.py                # Network retry utility
    setup.py                 # Interactive setup wizard
    init.py                  # Validation
```

## Storage & credentials

| Path | Purpose |
|------|---------|
| `~/.openclaw/config/tech-brainstorm/config.json` | Settings + outputs |
| `~/.openclaw/data/tech-brainstorm/reports/*.json` | Saved reports |
| `~/.openclaw/secrets/openai_api_key` | LLM API key (shared with other skills) |

## Security

- **API keys** read from dedicated files, never from config.json
- **Subprocess isolation** for skill-to-skill calls (no `shell=True`)
- **File output safety**: path validation + content pattern detection
- **Cross-config reads**: only `openclaw.json` for Telegram token (logged)

## Uninstall

```bash
clawhub remove tech-brainstorm
rm -rf ~/.openclaw/config/tech-brainstorm
rm -rf ~/.openclaw/data/tech-brainstorm
```

## License

MIT
