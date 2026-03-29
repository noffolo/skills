---
name: install-founderclaw
description: >
  Install FounderClaw — a complete multi-agent system for OpenClaw.
  Adds 6 agents (CEO + 5 departments), 29 skills, structured workspace,
  tool policies, and model configuration. This modifies openclaw.json and
  restarts the gateway. Requires user permission.
  Triggered by: "install founderclaw", "setup founderclaw", "get founderclaw",
  "add founderclaw", "install the engineering team".
---

# Install FounderClaw

This is a SYSTEM install. It adds 6 agents to OpenClaw. Follow every step. Do not skip the config step — it is required.

## Step 1: Explain

Tell the user:

> **FounderClaw** adds a 6-agent engineering team to your OpenClaw:
> - 🎯 **CEO** — orchestrates everything, talks to you
> - 📐 **Strategy** — product thinking, design, architecture
> - 🚀 **Shipper** — code review, deployment, releases
> - 🔍 **Tester** — QA, browser testing, bug detection
> - 🛡️ **Safety** — security audits, guardrails
> - 📊 **Observer** — debugging, retrospectives, second opinions
>
> 29 skills. Structured workspace. Each agent has its own personality and tools.
>
> **This will modify your OpenClaw config** and restart the gateway. Your existing agents are NOT affected.

Wait for "yes" or "proceed".

## Step 2: Clone and install files

Run:

```bash
git clone --single-branch --depth 1 https://github.com/ashish797/FounderClaw.git ~/.agents/skills/founderclaw 2>&1 && cd ~/.agents/skills/founderclaw && INSTALLED=0 && for skill_dir in */; do [ ! -f "$skill_dir/SKILL.md" ] && continue; skill_name=$(basename "$skill_dir"); target=~/.agents/skills/"$skill_name"; [ -e "$target" ] && continue; ln -sf "$(pwd)/$skill_dir" "$target"; INSTALLED=$((INSTALLED + 1)); done && if [ ! -d ~/.openclaw/founderclaw ]; then cp -r workspace-template ~/.openclaw/founderclaw; echo "WORKSPACE_CREATED"; else echo "WORKSPACE_EXISTS"; fi && echo "FILES_DONE:$INSTALLED"
```

Report: "✅ X skills installed. ✅ Workspace created."

## Step 3: Apply multi-agent config (REQUIRED — DO NOT SKIP)

Tell the user:

> Now applying the multi-agent config. This adds 6 agents to your openclaw.json and restarts the gateway.

Apply this config patch using `gateway config.patch`:

```json
{
  "agents": {
    "list": [
      {
        "id": "founderclaw-main",
        "name": "FounderClaw CEO",
        "workspace": "~/.openclaw/founderclaw/ceo"
      },
      {
        "id": "fc-strategy",
        "name": "Strategy",
        "workspace": "~/.openclaw/founderclaw/strategy-dept",
        "skills": ["office-hours", "plan-ceo-review", "plan-eng-review", "plan-design-review", "design-consultation", "design-review", "design-shotgun", "autoplan"]
      },
      {
        "id": "fc-shipper",
        "name": "Shipper",
        "workspace": "~/.openclaw/founderclaw/shipping-dept",
        "skills": ["review", "ship", "land-and-deploy", "canary", "benchmark", "document-release"]
      },
      {
        "id": "fc-tester",
        "name": "Tester",
        "workspace": "~/.openclaw/founderclaw/testing-dept",
        "skills": ["qa", "qa-only", "browse", "setup-browser-cookies", "connect-chrome"]
      },
      {
        "id": "fc-safety",
        "name": "Safety",
        "workspace": "~/.openclaw/founderclaw/security-dept",
        "skills": ["cso", "careful", "freeze", "guard", "unfreeze"]
      },
      {
        "id": "fc-observer",
        "name": "Observer",
        "workspace": "~/.openclaw/founderclaw/history-dept",
        "skills": ["investigate", "retro", "codex"]
      }
    ]
  }
}
```

If the config.patch fails (e.g., tool not available, permission denied), tell the user:

> ⚠️ Config could not be applied automatically. You need to add the agents manually:
>
> Open `~/.openclaw/openclaw.json` and add these 6 entries to `agents.list`.
> See the config template at `~/.agents/skills/founderclaw/install-founderclaw/agents-config.json`

Also write the config to a file for manual application:

```bash
cat > ~/.agents/skills/founderclaw/install-founderclaw/agents-config.json << 'EOF'
[
  {"id":"founderclaw-main","name":"FounderClaw CEO","workspace":"~/.openclaw/founderclaw/ceo"},
  {"id":"fc-strategy","name":"Strategy","workspace":"~/.openclaw/founderclaw/strategy-dept","skills":["office-hours","plan-ceo-review","plan-eng-review","plan-design-review","design-consultation","design-review","design-shotgun","autoplan"]},
  {"id":"fc-shipper","name":"Shipper","workspace":"~/.openclaw/founderclaw/shipping-dept","skills":["review","ship","land-and-deploy","canary","benchmark","document-release"]},
  {"id":"fc-tester","name":"Tester","workspace":"~/.openclaw/founderclaw/testing-dept","skills":["qa","qa-only","browse","setup-browser-cookies","connect-chrome"]},
  {"id":"fc-safety","name":"Safety","workspace":"~/.openclaw/founderclaw/security-dept","skills":["cso","careful","freeze","guard","unfreeze"]},
  {"id":"fc-observer","name":"Observer","workspace":"~/.openclaw/founderclaw/history-dept","skills":["investigate","retro","codex"]}
]
EOF
```

## Step 4: VERIFY agents exist in config (MANDATORY CHECK)

After Step 3, verify the agents were actually added. Run `agents_list` to check:

```
Use the agents_list tool to check if founderclaw-main, fc-strategy, fc-shipper, fc-tester, fc-safety, fc-observer exist.
```

If any of the 6 agents are MISSING from the config:
- The config.patch did NOT work
- You MUST apply it again or provide manual instructions
- Do NOT report "installed" until all 6 agents are confirmed

If agents_list tool is not available:
- Read the config file: check if the agents exist
- If not, provide the manual instructions from Step 3

**This check is mandatory. Do not skip it.**

## Step 5: Report ONLY after verification

Tell the user ONLY after confirming all 6 agents exist:

> **FounderClaw installed!**
>
> ✅ 29 skills in ~/.agents/skills/
> ✅ 6 agents configured (CEO + 5 departments)
> ✅ Workspace at ~/.openclaw/founderclaw/
>
> **Gateway will restart to apply the new agents.**

If agents were NOT added:

> ⚠️ Skills installed but agents were NOT configured.
> You need to add 6 agents to your openclaw.json manually.
> Run: `cat ~/.agents/skills/founderclaw/install-founderclaw/agents-config.json`
> Copy the contents into your `agents.list` array in openclaw.json.

## Uninstall

When user says "uninstall founderclaw":

```bash
for link in ~/.agents/skills/*; do [ -L "$link" ] || continue; target=$(readlink "$link"); echo "$target" | grep -q "founderclaw" && rm "$link"; done
rm -rf ~/.agents/skills/founderclaw
echo "Skills removed. Workspace kept at ~/.openclaw/founderclaw/"
```

Then remove the 6 agents from config via `gateway config.patch` (remove the founderclaw entries from agents.list).
