# HunterMiner

HunterMiner is a cross-platform OpenClaw skill for Linux, Windows 10/11, and macOS. It scans for miner-related indicators by checking OpenClaw skill code, local disk code and common persistence paths, running processes, network endpoints, and code patterns that disable firewall or Microsoft Defender real-time monitoring.

## Release status

This package is prepared as a clean release bundle for distribution and installation.

## Core features

- Cross-platform scanning for Linux, Windows 10/11, and macOS
- Indicator-based detection using four local databases
- Free database updates
- Per-scan billing support through SkillPay
- JSON and Markdown report output
- Optional quarantine or delete actions after user confirmation

## Included indicator databases

- `indicators/mining_pool_websites.txt`
- `indicators/mining_software_filenames.txt`
- `indicators/mining_pool_public_ips.txt`
- `indicators/mining_pool_ports.txt`

## Main commands

### Update indicator databases for free

```bash
python hunterminer.py update-db
```

### Run a billed scan

```bash
python hunterminer.py scan --user-id YOUR_USER_ID
```

### Show latest report paths

```bash
python hunterminer.py show-latest
```

### Remediate a selected finding

```bash
python hunterminer.py remediate --report output/latest_report.json --finding-id FINDING_ID --action quarantine --yes
```

## Billing behavior

- `update-db`: free
- `scan`: `0.1 USDT` per run
- If charging fails, the tool will automatically return a recharge link. It will use the `payment_url` from the charge API first, and if that is missing it will request a new recharge link automatically. It will not direct the user to a website homepage.

## Report output

Reports are written to the local `output/` directory at runtime.

## Installation

Before installation, make sure Python is available:

- Windows 10/11: install Python 3.10 or newer
- Linux: make sure `python3` is installed
- macOS: make sure `python3` is installed

Install dependencies from the skill directory:

### Linux / macOS

```bash
cd hunterminer
python3 -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
cd hunterminer
py -3 -m pip install -r requirements.txt
```

See `INSTALL.md` for full step-by-step installation instructions.

## Support files

- `SKILL.md` — OpenClaw skill definition and usage guide
- `INSTALL.md` — installation steps
- `CHANGELOG.md` — release history
- `LICENSE` — distribution terms

## Notes

- `config.local.json` is included for local configuration convenience.
- You can also provide the billing key through the `SKILLPAY_API_KEY` environment variable.
- Prefer quarantine before delete.


## Raw payment link mode

When a scan fails because the balance is insufficient, you can generate a raw top-up URL without JSON formatting:

```bash
python hunterminer.py payment-link --user-id YOUR_USER_ID
```

This command prints only the plain payment URL on one line.
