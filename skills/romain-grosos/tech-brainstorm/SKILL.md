---
name: tech-brainstorm
version: "1.0.0"
description: "Multi-source technical research + contextual brainstorm for architecture and stack decisions. Use when: the user asks to brainstorm a technical topic, compare technologies, evaluate architecture options, or explore a tech subject with a specific context. Produces a structured report (state of the art + concrete options with pros/cons/effort) and dispatches to Telegram/Nextcloud/email. Enhanced by mail-client (email output) and nextcloud-files (cloud storage)."
homepage: https://github.com/Rwx-G/openclaw-skill-tech-brainstorm
compatibility: Python 3.9+ - no external dependencies (stdlib only) - network access for LLM API
metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "requires": { "env": [] },
      "suggests": ["mail-client", "nextcloud-files"]
    }
  }
ontology:
  reads: [web_content]
  writes: [local_data_files]
  enhancedBy: [mail-client, nextcloud-files]
---

# Skill Tech-Brainstorm

Multi-source technical research + contextual brainstorm for architecture and stack decisions.
Gathers web research, synthesizes state of the art, and produces context-aware recommendations
with pros/cons/effort for each option.

No external dependencies: stdlib Python only (urllib, json).
LLM API required (OpenAI-compatible, configurable).

---

## Trigger phrases

- "brainstorm [sujet technique]"
- "compare [techno A] vs [techno B] dans mon contexte"
- "quelle stack pour [besoin] ?"
- "etat de l'art [sujet]"
- "analyse technique [sujet]"
- "aide-moi a choisir entre [options]"
- "tech brainstorm [sujet]"
- "explore [sujet technique] pour moi"

---

## How it works

### Agent workflow (recommended)

When the user sends a brainstorm request (e.g., via Telegram), the agent should:

1. **Parse** the request to extract topic and context
2. **Research** the topic using web_search and web_fetch (agent's native tools)
3. **Feed** the gathered sources to the skill:
   ```bash
   echo '[{"url":"...","title":"...","content":"..."}]' \
     | python3 scripts/tech_brainstorm.py brainstorm \
       --topic "k8s on-prem" \
       --context "AWX + Terraform, 10 apps, 3 personnes"
   ```
4. **Dispatch** the report to configured outputs:
   ```bash
   echo '<report_json>' | python3 scripts/tech_brainstorm.py send
   ```

Or use the `run` command for brainstorm + dispatch in one step:
```bash
echo '[sources_json]' | python3 scripts/tech_brainstorm.py run \
  --topic "..." --context "..."
```

### Direct CLI usage (without agent research)

The skill works without web sources - the LLM produces the brainstorm
from its training data:

```bash
python3 scripts/tech_brainstorm.py brainstorm \
  --topic "migration PostgreSQL vers CockroachDB" \
  --context "20 microservices, 500GB data, equipe 4 devs, SLA 99.9%"
```

---

## Quick Start

```bash
# 1. Setup
python3 scripts/setup.py

# 2. Validate
python3 scripts/init.py

# 3. Brainstorm (LLM only, no web sources)
python3 scripts/tech_brainstorm.py brainstorm \
  --topic "k8s on-prem" \
  --context "AWX + Terraform, 10 applis hebergees, equipe 3 personnes"

# 4. Full pipeline with dispatch
python3 scripts/tech_brainstorm.py run \
  --topic "k8s on-prem" \
  --context "AWX + Terraform, 10 applis hebergees, equipe 3 personnes"
```

---

## Setup

### Requirements

- Python 3.9+
- LLM API access (OpenAI, or any OpenAI-compatible endpoint)
- No pip installs needed

### Installation

```bash
# From the skill directory
python3 scripts/setup.py

# Validate
python3 scripts/init.py

# Test LLM connectivity
python3 scripts/init.py --test-llm
```

The wizard creates:
- `~/.openclaw/config/tech-brainstorm/config.json` (settings + outputs)
- `~/.openclaw/data/tech-brainstorm/` (reports storage)
- `~/.openclaw/secrets/openai_api_key` (API key, if not already present)

---

## Storage and credentials

### Files written by this skill

| Path | Written by | Purpose | Contains secrets |
|------|-----------|---------|-----------------|
| `~/.openclaw/config/tech-brainstorm/config.json` | `setup.py` | Settings + outputs | NO |
| `~/.openclaw/data/tech-brainstorm/reports/*.json` | `tech_brainstorm.py` | Saved reports | NO |

### Files read from outside the skill

| Path | Read by | Key accessed | When |
|------|---------|-------------|------|
| `~/.openclaw/secrets/openai_api_key` | `_llm.py` | API key (read-only) | Every LLM call |
| `~/.openclaw/openclaw.json` | `_dispatch.py` | `channels.telegram.botToken` (read-only) | When telegram_bot output is enabled without explicit bot_token |

### Cleanup on uninstall

```bash
python3 scripts/setup.py --cleanup
```

---

## Security model

### Credential isolation
- API keys are read from dedicated files (`~/.openclaw/secrets/`), never from config.json.
- The skill warns if key files have overly permissive permissions.

### Subprocess boundaries
- Dispatch delegates to other skills via `subprocess.run()` (never `shell=True`).
- Script paths are validated to reside under `~/.openclaw/workspace/skills/`.

### File output safety
- The `file` output type validates paths (allowlist + blocklist) and content before writing.
- Only `~/.openclaw/` is allowed by default. Additional directories can be whitelisted via `config.security.allowed_output_dirs`.
- Sensitive paths and suspicious content patterns are always blocked.

### Cross-config reads
- `~/.openclaw/openclaw.json` for Telegram bot token (only when needed, logged to stderr).
- `~/.openclaw/secrets/openai_api_key` for LLM API access.

---

## CLI reference

### `brainstorm`

```
python3 tech_brainstorm.py brainstorm --topic "..." [--context "..."]
```

Generates a brainstorm report. Optionally reads web research from stdin as JSON:
```json
[
  {"url": "https://...", "title": "...", "content": "extracted text..."},
  {"url": "https://...", "title": "...", "content": "..."}
]
```

Output (JSON on stdout):
```json
{
  "topic": "k8s on-prem",
  "context": "AWX + Terraform, 10 apps, 3 personnes",
  "report": "# Etat de l'art\n...\n# Pistes\n...\n# Recommandation\n...",
  "recap": "🧠 *Brainstorm: k8s on-prem*\n...",
  "sources_count": 5,
  "sources": [{"url": "...", "title": "..."}],
  "model": "gpt-4o-mini",
  "timestamp": "2026-03-28T10:00:00+00:00"
}
```

### `run`

```
python3 tech_brainstorm.py run --topic "..." [--context "..."] [--profile NAME]
```

Full pipeline: brainstorm + dispatch to configured outputs.
Same as `brainstorm` but also saves the report locally and dispatches.

### `send`

```
python3 tech_brainstorm.py send [--profile NAME]
```

Reads a report JSON from stdin and dispatches to all enabled outputs.

### `config`

```
python3 tech_brainstorm.py config
```

Shows the active configuration (API keys masked).

---

## Output report structure

The brainstorm report is structured in 3 sections:

### 1. Etat de l'art
- State of the art on the topic (technologies, trends, adoption levels)
- Known friction points and community feedback
- Recent trends and evolutions
- Sources cited with links

### 2. Pistes concretes (3-5 options)
For each option:
- **Description**: what it concretely involves
- **Avantages**: expected benefits in your context
- **Risques**: what can go wrong, tech debt, limitations
- **Effort**: estimate in person-days or T-shirt sizing (S/M/L/XL)
- **Sources**: links or references

### 3. Recommandation
- Options ranked by relevance/effort ratio
- Recommended option with justification
- Identifiable quick wins
- Critical attention points

---

## LLM configuration

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

| Key | Default | Description |
|-----|---------|-------------|
| `enabled` | `true` | Enable LLM (required for this skill) |
| `base_url` | `https://api.openai.com/v1` | OpenAI-compatible endpoint |
| `api_key_file` | `~/.openclaw/secrets/openai_api_key` | Path to API key file |
| `model` | `gpt-4o-mini` | Model for synthesis + brainstorm |
| `max_tokens` | `4096` | Max output tokens |
| `temperature` | `0.7` | Creativity (0.0-1.0, higher = more creative) |

Compatible endpoints: OpenAI, Azure OpenAI, Ollama, LM Studio, vLLM, any OpenAI-compatible API.

---

## Dispatch configuration

Outputs are configured in `config.json` under the `outputs` array.

Available types:
- `telegram_bot`: short recap via Telegram Bot API
- `mail-client`: full HTML report via mail-client skill or SMTP fallback
- `nextcloud`: full Markdown report via nextcloud skill (append or overwrite)
- `file`: full Markdown report to local file

Content types:
- `recap`: short summary (5-8 lines, suitable for Telegram)
- `full_report`: complete Markdown report

Configure outputs:
```bash
python3 scripts/setup.py --manage-outputs
```

---

## Templates (agent usage)

### Basic brainstorm (no web research)

```python
result = exec("python3 scripts/tech_brainstorm.py brainstorm "
              "--topic 'k8s on-prem' "
              "--context 'AWX + Terraform, 10 apps, 3 personnes'")
data = json.loads(result.stdout)
# data["report"] = full Markdown report
# data["recap"] = short Telegram-ready recap
```

### With web research

```python
# 1. Agent gathers sources via web_search + web_fetch
sources = [
    {"url": "https://...", "title": "K8s on-prem guide", "content": "..."},
    {"url": "https://...", "title": "K3s vs K8s comparison", "content": "..."},
]

# 2. Feed to skill via stdin
result = exec(
    "python3 scripts/tech_brainstorm.py run "
    "--topic 'k8s on-prem' "
    "--context 'AWX + Terraform, 10 apps, 3 personnes'",
    stdin=json.dumps(sources)
)
```

### Agent workflow

```
1. Parse user request: extract topic + context
2. web_search: 3-5 queries related to topic
3. web_fetch: top results (docs, comparisons, community posts)
4. Structure sources as JSON array
5. Pipe to tech_brainstorm.py run (brainstorm + dispatch)
6. Return recap to user conversation
```

---

## Combine with

- **mail-client** : send the full report by email
- **nextcloud** : archive reports as Markdown files
- **veille** : combine tech watch insights with brainstorm context

---

## Troubleshooting

See `references/troubleshooting.md` for detailed troubleshooting steps.

Common issues:

- **API key not found**: create `~/.openclaw/secrets/openai_api_key` with your key
- **LLM timeout**: increase timeout or use a faster model
- **Empty report**: check that `llm.enabled` is `true` in config
- **Dispatch failed**: run `setup.py --manage-outputs` to configure outputs
