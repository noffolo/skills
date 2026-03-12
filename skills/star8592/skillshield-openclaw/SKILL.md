---
name: skillshield
version: 2.1.5
description: Sandboxed command runner for AI agents — Rust daemon with Linux user-namespace isolation via Bubblewrap.
metadata: {"openclaw":{"emoji":"🛡️"}}
---

# skillshield

**Sandboxed command runner for AI agents — Rust daemon with Linux user-namespace isolation via Bubblewrap.**

SkillShield provides a safe execution layer for AI-driven workflows. Instead of running shell commands directly on the host, every command goes through a bundled Rust daemon that applies a policy check and then runs the command inside a [Bubblewrap](https://github.com/containers/bubblewrap) user namespace with a minimal, read-only root filesystem.

## How it works

1. The wrapper script (`skillshield-exec.sh`) builds the bundled Rust daemon on first use and communicates with it over a local Unix socket.
2. The daemon evaluates a lightweight policy (safe-by-default — blocks destructive patterns and limits filesystem scope).
3. Approved commands run inside `bwrap --unshare-all` with `/usr` mounted read-only and only the current working directory writable.

## Features

- **Minimal root filesystem** — only `/usr`, `/dev`, `/proc`, and `/tmp` are available; no access to home directories, cloud credential paths, or sensitive host files.
- **Policy evaluation** — the Rust policy engine categorises each action (shell, file-read, file-write, network) by risk level and decides Allow / Confirm / Deny / Sandbox.
- **Unix socket IPC** — the wrapper talks to the daemon over a local socket, never over the network.
- **Incremental build** — the Rust binary is compiled once and cached; subsequent calls start in sub-second time.

## Usage

```bash
# Run a simple command
./skillshield-exec.sh "echo hello world"

# Cleanup a temporary directory
./skillshield-exec.sh "rm -rf tmp_dir/"
```

## Requirements

| Dependency | Purpose |
|---|---|
| Linux | User-namespace support |
| `bwrap` | Bubblewrap sandbox runtime |
| `cargo` | Builds the Rust daemon on first run |
| `curl` | Health-check the daemon |
| `python3` | JSON formatting in the wrapper |

## Links

- Homepage: https://coinwin.info
- Marketplace: https://clawhub.ai/star8592/skillshield-openclaw
