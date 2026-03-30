# Security Compliance — Tracebit Canaries Skill

This document covers safety posture, credential handling rules, messaging constraints, and full removal instructions for the Tracebit Canaries skill.

---

## Safety Posture

This skill operates under a **human-gated-deployment** model:

1. **Upfront consent** — Before starting setup, the agent confirms with the human that they want to proceed. The agent summarizes what will be installed and where canaries will be placed.
2. **Confirmation before sensitive writes** — The agent confirms with the human before writing canary credentials to standard credential locations on disk.
3. **Confirmation before remediation** — After an incident, the agent waits for human acknowledgement before rotating canaries or taking corrective action.

### Red Lines

The agent will **never**:
- Use canary credentials for real workloads or authentication
- Expose canary credential values in conversation output or logs
- Send notifications to channels other than the user's own configured messaging channel
- Execute remediation or canary rotation without human acknowledgement
- Read or modify real credentials on disk (only canary-specific files are touched)

### Runtime Constraints

| Constraint | Enforced |
|---|---|
| Human confirmation before deployment | Yes |
| Human confirmation before remediation | Yes |
| Investigation phase is read-only | Yes |

---

## Credential & Secret Handling

- **Generated passwords** must be written to a temp file with restrictive permissions (`chmod 600`), never included in conversation output.
- Tell the human the file path and instruct them to:
  1. Save the password to their password manager
  2. Change the password in Tracebit account settings
  3. Delete the temp file
- **Canary credential values** (fake AWS keys, SSH keys, cookies, passwords) must never appear in conversation output or logs. They are written to standard credential locations by the Tracebit CLI.
- **CLI authentication tokens** are stored at the standard Tracebit config location. Do not expose in logs or shared contexts.

---

## Messaging Scope

- Notifications are sent only to the **user's own configured messaging channel** (the one they set up in OpenClaw before activating this skill).
- The skill never lists specific messaging providers or sends to any other channel or recipient.
- Constrain all messaging to the user's own channel only.

---

## Local Footprint & Full Removal

### What this skill installs

| Component | Location | Installed by |
|---|---|---|
| Tracebit CLI binary | System PATH (e.g., `/usr/local/bin/tracebit`) | `scripts/install-tracebit.sh` |
| CLI auth token | Standard Tracebit config directory | `tracebit auth` |
| Canary state cache | Standard Tracebit config directory | `tracebit deploy` |
| AWS canary profile | Standard AWS credentials location (named `[canary]` profile) | `tracebit deploy aws` |
| SSH canary key | Standard SSH directory (named `tracebit-canary`) | `tracebit deploy ssh` |
| Background daemon | launchd (macOS) / systemd (Linux) | `tracebit deploy` |
| Heartbeat check | `HEARTBEAT.md` entry | Manual (Step 6) |
| Temp credentials file | `/tmp/tracebit-setup-creds` | Skill setup (Step 1) |

### Full removal script

Run this to completely remove all Tracebit canary components:

```bash
#!/usr/bin/env bash
# remove-tracebit.sh — Full removal of Tracebit canary skill footprint
set -euo pipefail

echo "Removing Tracebit canary components..."

# 1. Stop and remove background daemon
# macOS
launchctl stop com.tracebit.daemon 2>/dev/null || true
launchctl remove com.tracebit.daemon 2>/dev/null || true
# Linux
systemctl --user stop tracebit 2>/dev/null || true
systemctl --user disable tracebit 2>/dev/null || true

# 2. Remove canary credentials from standard locations
# AWS canary profile
if [ -f "$HOME/.aws/credentials" ]; then
  python3 -c "
import configparser, os
p = os.path.expanduser('~/.aws/credentials')
c = configparser.ConfigParser()
c.read(p)
if 'canary' in c:
    c.remove_section('canary')
    with open(p, 'w') as f:
        c.write(f)
    print('Removed [canary] profile from AWS credentials')
else:
    print('No [canary] profile found')
" 2>/dev/null || echo "Could not clean AWS credentials — check manually"
fi

# SSH canary key
rm -f "$HOME/.ssh/tracebit-canary" && echo "Removed SSH canary key" || true

# 3. Remove Tracebit config directory
rm -rf "$HOME/.config/tracebit" && echo "Removed Tracebit config directory" || true

# 4. Remove CLI binary
if command -v tracebit >/dev/null 2>&1; then
  TRACEBIT_PATH=$(which tracebit)
  sudo rm -f "$TRACEBIT_PATH" && echo "Removed CLI: $TRACEBIT_PATH" || echo "Could not remove CLI — run: sudo rm $TRACEBIT_PATH"
fi

# 5. Remove temp credentials file
rm -f /tmp/tracebit-setup-creds && echo "Removed temp credentials file" || true

# 6. Reminder
echo ""
echo "Done. Manual steps remaining:"
echo "  - Remove the Tracebit heartbeat entry from HEARTBEAT.md"
echo "  - Delete your Tracebit account at https://community.tracebit.com if desired"
```

### Manual removal (if script is unavailable)

1. Stop the background daemon (see `references/troubleshooting.md`)
2. Remove the `[canary]` profile from your AWS credentials file
3. Delete the SSH canary key from your SSH directory
4. Delete the Tracebit config directory
5. Remove the `tracebit` binary from your PATH
6. Delete `/tmp/tracebit-setup-creds` if it exists
7. Remove the heartbeat entry from `HEARTBEAT.md`
