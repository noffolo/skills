---
name: Phantom Browser
slug: phantom-browser
version: 0.1.0
description: Undetectable browser automation for AI agents. 31/31 stealth tests passed. WindMouse physics, per-profile fingerprinting, residential IP routing. Runs headless on a $6/mo VPS.
author: ClawAgents
license: MIT
tags:
  - browser
  - automation
  - stealth
  - anti-detect
  - scraping
  - social-media
  - ai-agents
requires:
  - python>=3.10
---

# Phantom Browser

Undetectable browser automation built for AI agents. Not Playwright. Not a manual anti-detect tool.

Your agents log into platforms, interact with sites, and browse the web without getting flagged, throttled, or banned.

## What It Does

Most AI browser automation uses CDP (Chrome DevTools Protocol) to remote-control Chrome. Every major platform detects it. Facebook, LinkedIn, Instagram, X, Google. The second they see CDP automation, you are flagged, throttled, or banned.

Phantom Browser does not work that way.

### Tool Layer (Not Remote Control)

The AI agent describes what it wants to do. "Click this button." "Type in this field." "Scroll down." A tool layer translates that into actions that look exactly like a real person using a real computer. The agent never sends raw browser commands.

### Human-Like Input Physics

- **Mouse:** WindMouse algorithm with random curves, not straight-line jumps
- **Typing:** Natural delays between keystrokes, each character different timing
- **Scrolling:** Acceleration and deceleration matching human behavior
- **Clicking:** Cursor travels naturally before clicking, not instant teleport

### Per-Profile Fingerprinting

Each browser session runs with a unique identity. Screen resolution, installed fonts, timezone, language, WebGL signature (reports a real consumer GPU like GTX 1650, not SwiftShader), canvas fingerprint, user agent, plugin list.

To the platform, each profile looks like a completely separate person on a completely separate computer.

### Residential IP Routing

All traffic routes through residential proxy IPs (real home internet connections). The platform sees a normal ISP from a real location, not a datacenter IP.

### Headless on VPS

Runs on a cheap VPS ($6/month). No desktop app. No screen. No GUI. Agents browse 24/7. Uses Xvfb so Chrome extensions work without a physical display.

### System-Level Access Control

Only agents explicitly approved for browser access can open one. Not a prompt instruction. System-level lockout. Unapproved agents genuinely cannot access the browser.

## Proof

- **31/31** stealth tests passed (bot.sannysoft.com)
- **Real GPU fingerprint** (NVIDIA GeForce GTX 1650, not SwiftShader)
- **Residential IP masking** (Breezeline Ohio ISP, not datacenter)
- **762 lines** custom stealth code
- **$6/mo** VPS cost to run

## Status: Early Access

Phantom Browser is in limited early access. Run `setup.sh` to register your interest and be first in line when we open spots.

```bash
bash setup.sh
```

## Quick Start (After Access)

```bash
bash setup.sh
source .venv/bin/activate
python3 phantom_browser.py --status
```

## vs. Everything Else

| Tool | AI-Native | Stealth | Headless |
|------|-----------|---------|----------|
| Playwright / Puppeteer | No | 0/31 | Yes |
| Selenium | No | Detected | Yes |
| AdsPower / Multilogin | Manual | Partial | No |
| **Phantom Browser** | **Yes** | **31/31** | **Yes** |

## Requirements

- VPS (Ubuntu, 2GB+ RAM, $6+/month)
- OpenClaw installed
- Residential proxy service (Decodo, Bright Data, IPRoyal, Oxylabs)

## Links

- Product page: https://clawagents.dev/phantom-browser/
- Demo video: 67s proof-of-concept showing all stealth tests
