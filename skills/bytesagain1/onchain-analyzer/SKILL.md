---
version: "3.0.0"
name: Onchain Analyzer
description: "Analyze wallet on-chain activity with transaction history and behavior profiling. Use when investigating wallets, tracing transfers, profiling activity."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
---

# Onchain Analyzer

An AI and prompt engineering assistant CLI. Despite the name, this tool is focused on helping you craft, optimize, and evaluate prompts for large language models. It provides commands for generating prompts, building prompt chains, comparing AI models, estimating token costs, and following safety guidelines.

All operations are logged with timestamps for auditing and stored locally in flat files.

## Commands

| Command | Description |
|---------|-------------|
| `onchain-analyzer prompt <role> [task] [format]` | Generate a structured prompt with role, task, and output format |
| `onchain-analyzer system <role>` | Generate a system prompt for a given expert role |
| `onchain-analyzer chain` | Display a 4-step prompt chain: Understand → Plan → Execute → Verify |
| `onchain-analyzer template` | List prompt template patterns: Zero-shot, Few-shot, Chain-of-thought, Role-play |
| `onchain-analyzer compare` | Compare major AI models (GPT-4 vs Claude vs Gemini) |
| `onchain-analyzer cost [tokens]` | Estimate cost for a given number of tokens (default: 1000) |
| `onchain-analyzer optimize` | Show prompt optimization tips and best practices |
| `onchain-analyzer evaluate` | Evaluate output quality across accuracy, relevance, completeness, and tone |
| `onchain-analyzer safety` | Display AI safety guidelines (no harmful content, no personal data, cite sources) |
| `onchain-analyzer tools` | List popular AI tools: ChatGPT, Claude, Gemini, Perplexity, Midjourney |
| `onchain-analyzer help` | Show the built-in help message |
| `onchain-analyzer version` | Print the current version |

## Data Storage

All data is stored in the directory defined by the `ONCHAIN_ANALYZER_DIR` environment variable. If not set, it defaults to `~/.local/share/onchain-analyzer/`.

Files created in the data directory:

- **`data.log`** — Main data log file (currently unused but created on init)
- **`history.log`** — Audit trail of every command executed with timestamps

## Requirements

- **bash** 4.0 or later (uses `set -euo pipefail`)
- **python3** — used by the `cost` command for token cost calculation (standard library only, no pip packages)
- **Standard POSIX utilities** — `date`, `cat`, `echo`, `mkdir`
- No external API keys or network access required

## When to Use

1. **Crafting prompts for LLMs** — Use `prompt` and `system` to quickly scaffold well-structured prompts with role assignments and task definitions
2. **Learning prompt engineering patterns** — Use `template` to see common patterns (zero-shot, few-shot, chain-of-thought, role-play) and `chain` for multi-step reasoning workflows
3. **Estimating API costs** — Use `cost` to calculate approximate spend before sending large batches of tokens to an API
4. **Comparing AI models** — Use `compare` to get a quick reference of how GPT-4, Claude, and Gemini stack up in benchmarks
5. **Ensuring responsible AI use** — Use `safety` to review guardrails before deploying prompts in production environments

## Examples

```bash
# Generate a prompt for a data analyst role
onchain-analyzer prompt "data analyst" "summarize sales data" "markdown table"
#=> Role: data analyst
#=>   Task: summarize sales data
#=>   Format: markdown table

# Create a system prompt for an expert role
onchain-analyzer system "cybersecurity researcher"
#=> You are an expert cybersecurity researcher. Be precise, helpful, and concise.

# View prompt chain methodology
onchain-analyzer chain
#=> Step 1: Understand | Step 2: Plan | Step 3: Execute | Step 4: Verify

# Estimate cost for 5000 tokens
onchain-analyzer cost 5000
#=> Tokens: ~5000 | Cost: ~$0.1500

# List available prompt templates
onchain-analyzer template
#=> 1. Zero-shot | 2. Few-shot | 3. Chain-of-thought | 4. Role-play
```

## Configuration

Set the `ONCHAIN_ANALYZER_DIR` environment variable to change the data directory:

```bash
export ONCHAIN_ANALYZER_DIR="/path/to/custom/dir"
```

If unset, the tool respects `XDG_DATA_HOME` (defaulting to `~/.local/share/onchain-analyzer/`).

## How It Works

1. On every invocation, the tool ensures the data directory exists (`mkdir -p`)
2. The first argument selects the command via a `case` dispatch
3. Each command performs its action and appends an entry to `history.log` for auditing
4. The `cost` command uses an inline Python snippet to compute `tokens × $0.00003`
5. All output goes to stdout for easy piping and redirection

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
