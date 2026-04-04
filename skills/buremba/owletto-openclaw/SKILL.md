---
name: owletto-openclaw
description: Install and configure the Owletto memory plugin for OpenClaw, including OAuth login and MCP health verification.
---

# Owletto OpenClaw Setup

Use this skill when a user wants Owletto long-term memory working in OpenClaw.

For general Owletto usage with Codex, ChatGPT, Claude, Cursor, Gemini, or generic MCP workflows, use `owletto`.

## Setup Flow

1. Ensure CLI prerequisites are available.

```bash
node --version
pnpm --version
owletto --help
```

2. Install the OpenClaw plugin package.

```bash
openclaw plugins install owletto-openclaw-plugin
```

3. Log in to Owletto for MCP access.

```bash
owletto login --mcpUrl <mcp-url>
```

4. Configure OpenClaw plugin settings.

```bash
owletto configure --mcpUrl <mcp-url>
```

5. Verify auth + MCP connectivity.

```bash
owletto health
```

## CLI Fallback

If `owletto` is not on PATH, use the repo-local CLI entrypoint:

```bash
pnpm -C packages/cli exec tsx src/bin.ts login --mcpUrl <mcp-url>
pnpm -C packages/cli exec tsx src/bin.ts configure --mcpUrl <mcp-url>
pnpm -C packages/cli exec tsx src/bin.ts health
```

## Notes

- Replace `<mcp-url>` with the target MCP URL (e.g. the URL shown on the workspace data sources page).
- If `openclaw` is not on PATH, install OpenClaw CLI first, then rerun setup.
- For headless environments without browser access, use `owletto login --device --mcpUrl <mcp-url>`.
