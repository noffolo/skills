# WebChat Enhancer

A lightweight Tampermonkey script that adds a sleek, hover-expandable navigation panel to your OpenClaw WebChat interface.

![Version](https://img.shields.io/badge/version-4.5.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

🖱️ **Hover to Expand** — A slim tab stays hidden on the right edge of the screen. Slide your mouse near it and the panel smoothly slides out. Move your mouse away and it hides again. No clicks needed.

🎨 **Auto Theme Sync** — Automatically detects whether your WebChat is in Dark or Light mode and instantly switches the navigator to matching Lobster-inspired colors. No manual switching, no settings panel — it just works.

📜 **Chat Navigator** — Scans your entire conversation and generates a list of clickable message cards. Click any card to smoothly scroll and jump to that exact message.

🔄 **Auto-Updating** — Detects new messages automatically as they appear. The message list stays fresh without any action from you.

⚡ **Lightweight** — Pure vanilla JavaScript. No external dependencies. No settings or configuration needed.

---

## Screenshots

**Dark Mode**
![Dark Mode](screenshot-dark.png)

**Light Mode**
![Light Mode](screenshot-light.png)

---

## What Changed in 4.5.0

- ❌ Removed language switching — English only, keeping it simple
- ❌ Removed theme selector — theme is now fully automatic
- ❌ Removed settings panel — works out of the box
- 🆕 Hover-expandable navigation — panel hides when not in use
- 🆕 Auto theme detection — syncs with WebChat Dark/Light mode instantly

---

## Requirements

- **OpenClaw WebChat** running at `http://127.0.0.1:18789` (or `http://localhost:18789`)
- **Tampermonkey** browser extension ([Chrome](https://chrome.google.com/webstore/detail/tampermonkey) · [Firefox](https://addons.mozilla.org/firefox/addon/tampermonkey/) · [Edge](https://microsoftedge.microsoft.com/addons/detail/tampermonkey))

---

## Installation

### Option 1: GreasyFork (Recommended)

[![Install on GreasyFork](https://img.shields.io/badge/Install-GreasyFork-orange)](https://greasyfork.org/scripts/571337-webchat-enhancer)

1. Click the green **Install** button on GreasyFork
2. Open WebChat at `http://127.0.0.1:18789`
3. The navigator appears automatically ✨

### Option 2: Manual

1. Install [Tampermonkey](https://www.tampermonkey.net/) for your browser
2. Open Tampermonkey Dashboard → **Create new script**
3. Paste the contents of `enhancer.user.js` and save
4. Open WebChat at `http://127.0.0.1:18789`

---

## Usage

| Action | Result |
|--------|--------|
| Mouse enters right edge tab | Navigator slides out |
| Mouse leaves navigator area | Navigator slides back in |
| Click any message card | Smooth scroll to that message |
| Click **Refresh** | Rescan conversation |
| Switch WebChat theme | Navigator auto-adapts colors |

---

## Technical Details

- **Version:** 4.5.0
- **Author:** Boss
- **License:** MIT
- **Namespace:** `https://clawhub.ai/skills/webchat-enhancer`
- **Match URLs:** `http://127.0.0.1:18789/*`, `http://localhost:18789/*`
- **No external dependencies** — runs 100% client-side

---

## Links

- 🌐 [ClawHub](https://clawhub.com/skills/webchat-enhancer)
- 📦 [GreasyFork](https://greasyfork.org/scripts/571337-webchat-enhancer)
- 💻 [GitHub](https://github.com/yjin94606-art/webchat-enhancer)

---

## Changelog

### 4.5.0
- 🆕 Hover-expandable navigation — panel hides until mouse approaches
- 🎨 Auto theme sync — detects WebChat Dark/Light mode automatically
- 🦐 Lobster-inspired colors (crimson red accent)
- ⚡ Faster theme detection (300ms polling + MutationObserver)
- 🔧 Removed settings/language/theme panels — fully automatic
- 🐛 Fixed hover flicker at panel edges

### 4.x (Previous)
- Click-to-expand/fold navigation
- Manual language and theme selection
- Fixed chat bubble detection
