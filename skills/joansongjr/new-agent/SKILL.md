---
name: new-agent
description: Create a new OpenClaw agent and connect it to a messaging channel (Telegram, Discord, Slack, Feishu, WhatsApp, Signal, Google Chat). Includes workspace scaffolding and channel configuration guide.
---

# New Agent

Add a new agent to your OpenClaw gateway with a dedicated workspace and messaging channel.

## When to Use

- User wants to add a new AI agent or bot
- User wants to connect a bot to a messaging platform
- User provides an agent name and channel credentials

## Overview

Adding a new agent involves three parts:
1. **Workspace** — Create identity, personality, and memory files
2. **Registration** — Add the agent to the gateway configuration
3. **Channel** — Connect a messaging account and set up routing

See `scripts/setup-agent.sh` for automated workspace creation, or follow the steps below.

## Required Information

| Field | Example |
|-------|---------|
| Agent name | "Luna" |
| Channel | telegram / discord / slack / feishu / whatsapp / signal |
| Credentials | Bot token, app secret, or QR scan |

## Step 1: Workspace

Run the helper script or create manually:

```bash
./scripts/setup-agent.sh {name} {channel}
```

This creates a workspace at `workspace-groups/{name}/` with standard files:
- `IDENTITY.md` — Name, role, emoji
- `SOUL.md` — Personality and behavior
- `AGENTS.md` — Startup instructions
- `USER.md` — Owner info
- `HEARTBEAT.md`, `TOOLS.md`

## Step 2: Registration

Use the CLI to register the agent:

```bash
openclaw agents add {name}-agent
```

Or add manually to `agents.list` in the gateway config:

```json
{
  "id": "{name}-agent",
  "workspace": "~/.openclaw/workspace-groups/{name}"
}
```

## Step 3: Channel Configuration

Each channel requires an account entry and a routing rule (binding).

### Channel Reference

| Channel | Account Key | Required Fields |
|---------|------------|-----------------|
| Telegram | `channels.telegram.accounts` | `botToken` |
| Discord | `channels.discord.accounts` | `token` |
| Slack | `channels.slack.accounts` | `mode`, `appToken`, `botToken` |
| Feishu | `channels.feishu.accounts` | `appId`, `appSecret` |
| WhatsApp | `channels.whatsapp.accounts` | QR scan via CLI |
| Signal | `channels.signal.accounts` | QR scan via CLI |
| Google Chat | `channels.googlechat.accounts` | `serviceAccountPath` |

### Binding Format

```json
{
  "agentId": "{name}-agent",
  "match": {
    "channel": "{channel}",
    "accountId": "{name}"
  }
}
```

> Use `accountId` in the match block — not `account`.

### WhatsApp / Signal

These require interactive login:
```bash
openclaw channels login --channel whatsapp --account {name}
openclaw channels login --channel signal --account {name}
```

### Feishu / Lark

For Lark (global), add `"domain": "lark"` to the account entry.

## Step 4: Verify

```bash
openclaw agents list --bindings
openclaw channels status --probe
```

## Step 5: Pairing

For DM-based channels, the owner sends `/start` to the bot, then approves:

```bash
openclaw pairing approve {channel} {CODE}
```

## Notes

- All agents share existing model credentials — no extra API keys needed
- One channel is enough to bring an agent online
- Add more channels later by repeating Step 3
