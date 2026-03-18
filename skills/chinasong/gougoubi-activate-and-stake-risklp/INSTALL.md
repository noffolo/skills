# Install

## Local install

```bash
cp -R skills/gougoubi-activate-and-stake-risklp "$CODEX_HOME/skills/"
```

## GitHub install

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/gougoubi-activate-and-stake-risklp
```

## Verify

```bash
ls -la "$CODEX_HOME/skills/gougoubi-activate-and-stake-risklp"
```

Restart the agent runtime after installation.
