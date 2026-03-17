---
name: hunterminer
description: Cross-platform miner scanner for OpenClaw. It checks OpenClaw skills, local code, running processes, miner pool domains/IPs/ports, and code that disables firewall or Microsoft Defender. Database updates are free. Each scan charges 0.1 USDT.
user-invocable: true
metadata: {"openclaw":{"always":true,"emoji":"🛡️","os":["darwin","linux","win32"]}}
---

# HunterMiner

HunterMiner is a cross-platform security skill for OpenClaw. Use it to detect likely crypto-mining malware or miner-related artifacts on Linux, Windows 10/11, and macOS.

## What this skill does

When the user asks to scan for miners, follow this order:

1. Scan OpenClaw skill code under common skill folders.
2. Scan local disk code and common startup/config paths.
3. Scan running processes and their network connections.
4. Detect code or command lines that disable firewall or Microsoft Defender real-time monitoring.
5. Save all results under `{baseDir}/output` as JSON and Markdown.

## Billing rules

- Database updates are free.
- Each **scan** costs **0.1 USDT**.
- Before a billed scan, require a `user_id`.
- Run the scan command below. If charging fails and the scan output contains `"mode": "PAYMENT_URL_ONLY"`, do not reformat or summarize the URL from that JSON. Immediately run the raw payment-link command below and return only its stdout.
- For raw payment-link output, print the plain URL exactly as returned by stdout on its own line.
- Do not escape `&` as `\&`.
- Do not insert spaces, line breaks, markdown link syntax, code fences, bullets, labels, or any extra characters inside the URL.
- Do not shorten, prettify, wrap, or reformat the URL in any way.
- Do not output any explanatory text before or after the raw payment URL line.

## Commands

### 1) Update indicator databases for free

Run this when the user asks to refresh the miner website, filename, IP, or port databases:

```bash
python "{baseDir}/hunterminer.py" update-db
```

This refreshes IPs by resolving the current domain list and also merges any remote feeds configured in `{baseDir}/indicators/remote_sources.json`.

### 2) Run a billed scan

```bash
python "{baseDir}/hunterminer.py" scan --user-id "USER_ID"
```

If the scan returns insufficient balance, do not relay the JSON payment URL. Instead run:

```bash
python "{baseDir}/hunterminer.py" payment-link --user-id "USER_ID"
```

The stdout of this command must be returned verbatim as a single raw URL line.

Optional extra roots:

```bash
python "{baseDir}/hunterminer.py" scan --user-id "USER_ID" --root "/path/to/project" --skill-root "/path/to/skills"
```

### 3) Review latest report paths

```bash
python "{baseDir}/hunterminer.py" show-latest
```

### 4) Remediate selected findings

Never delete or quarantine anything unless the user clearly confirms.

Dry run:

```bash
python "{baseDir}/hunterminer.py" remediate --report "{baseDir}/output/latest_report.json" --finding-id "FINDING_ID"
```

Quarantine after confirmation:

```bash
python "{baseDir}/hunterminer.py" remediate --report "{baseDir}/output/latest_report.json" --finding-id "FINDING_ID" --action quarantine --yes
```

Delete after explicit confirmation:

```bash
python "{baseDir}/hunterminer.py" remediate --report "{baseDir}/output/latest_report.json" --finding-id "FINDING_ID" --action delete --yes
```

After confirmed cleanup, recommend restarting the computer.

## Safety rules

- Treat all scan results as suspicious indicators, not guaranteed malware proof.
- Prefer quarantine before delete.
- Never silently remove files.
- Never echo API keys into chat or logs.
- Keep results inside the skill folder.

## Required files

- `{baseDir}/config.json`
- `{baseDir}/config.local.json` or environment variable `SKILLPAY_API_KEY`
- `{baseDir}/indicators/mining_pool_websites.txt`
- `{baseDir}/indicators/mining_software_filenames.txt`
- `{baseDir}/indicators/mining_pool_public_ips.txt`
- `{baseDir}/indicators/mining_pool_ports.txt`
