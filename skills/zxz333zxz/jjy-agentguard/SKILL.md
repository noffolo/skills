---
name: agentguard
description: "AgentGuard security engine — intercept dangerous operations, audit all actions, protect sensitive data. All commands/files/network operations go through ag_* tools for rule-engine review before execution. Use when: (1) setting up agent security guardrails, (2) replacing native exec/read/write/process tools with safe alternatives, (3) auditing agent operations, (4) protecting secrets and sensitive files, or (5) emergency-stopping an agent session."
metadata: { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["agentguard"] }, "primaryEnv": "AGENTGUARD_DAEMON_PORT", "install": [{ "id": "curl-install", "kind": "download", "url": "https://www.agentguard.site/download/install.sh", "label": "Install AgentGuard (curl)" }], "os": ["darwin", "linux"] } }
---

# AgentGuard Security Engine

Integrated **AgentGuard security engine**. All agent operations must pass security review via `ag_*` tools.

## Setup

Run the setup script to install and start AgentGuard:

```bash
scripts/setup.sh
```

Or install manually:

```bash
curl -fsSL https://www.agentguard.site/download/install.sh | sh
agentguard daemon start
```

## Security Architecture

Four-layer protection ensuring agents cannot bypass security:

1. **Gateway Tool Blocking (L1)** — Auto-injects `tools.deny` in `openclaw.json` to physically disable native `exec`/`write`/`edit`/`apply_patch`/`process` tools at the Gateway layer.
2. **Rule Engine (L2)** — All `ag_*` calls go through command blacklist/whitelist, file path controls, and domain whitelists.
3. **Redaction Engine (L3)** — Auto-filters API keys, tokens, SSH keys, and 15+ categories of sensitive data (bidirectional input+output redaction).
4. **Audit Log (L4)** — All operations logged to local SQLite, viewable in Dashboard, tamper-proof.

> ⚠️ Native dangerous tools are blocked at the Gateway layer. Only `ag_*` tools can execute operations.

## Security Tools

### Operation Tools (replace native tools)

| ag_* Tool | Replaces | Security |
|-----------|----------|----------|
| `ag_execute_command` | `exec` / `process` | Command blacklist + dangerous command interception + output redaction |
| `ag_read_file` | `read` | Sensitive path blocking (.ssh/, keychain, browser data) + content redaction |
| `ag_write_file` | `write` / `edit` / `apply_patch` | Path access control + write content redaction check |
| `ag_list_directory` | `read` (directory) | Directory access control |
| `ag_http_request` | `browser` / network tools | Domain whitelist + data exfiltration prevention |

### Inspection Tools

| ag_* Tool | Purpose |
|-----------|---------|
| `ag_skill_check` | Check if a skill/plugin is on the security whitelist |
| `ag_status` | View engine status: mode / audit stats / Panic state |

### Control Tools

| ag_* Tool | Purpose |
|-----------|---------|
| `ag_panic` | 🚨 Emergency stop — immediately reject all subsequent operations |
| `ag_resume` | Resume normal operation |

## Usage Rules

1. **Must use `ag_*` tools** for all command, file, and network operations. Do not use native `exec`, `read`, `write`, `apply_patch`, `process` to bypass security.
2. When `ag_*` returns `🚫 Intercepted`, **do not attempt to bypass** — inform the user the operation was blocked and why.
3. When returning `⏳ Awaiting Approval`, tell the user to approve in the Dashboard.
4. If AgentGuard daemon is not running (connection failed), prompt user:
   - Start: `agentguard daemon start`
   - Install: `curl -fsSL https://www.agentguard.site/download/install.sh | sh`
5. Use `ag_status` anytime to check current security state.
6. Use `ag_panic` for emergency stop when suspicious behavior is detected.

## Security Modes

- **enforce** — Violations are rejected immediately
- **supervised** — Suspicious operations pause for user approval
- **permissive** — Audit logging only, no blocking

## Dashboard

Audit logs viewable at: **http://127.0.0.1:19821**

Features: real-time operation timeline / audit statistics / rule configuration / one-click Panic
