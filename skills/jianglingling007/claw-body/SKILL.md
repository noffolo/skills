---
name: claw-body
description: "Give your Claw a body! Turn your AI lobster into a real-time digital avatar with face, voice, and expressions. Talk face-to-face with your lobster — not just text. Powered by NuwaAI. Usage: /claw-body"
user-invocable: true
metadata:
  openclaw:
    emoji: "🦞"
    requires:
      bins:
        - node
---

# 🦞 Claw Body — Give Your Claw a Body

![Claw Body Preview](https://raw.githubusercontent.com/jianglingling007/nuwa-digital-human/main/poster.png)

**Every lobster deserves a body.**

Turn your OpenClaw AI into a real-time digital avatar — with a face, a voice, and expressions. Talk to your lobster face-to-face, not just through cold text.

Free 5-minute trial included. Sign up at [nuwaai.com](https://nuwaai.com) to create your own custom avatar for free.

## For Every Lobster Fan

- 🎨 **Design your dream lobster** — cute, anime, realistic, handsome, beautiful, or buff — your call
- 🗣️ **Voice chat** — speak to your lobster and hear it talk back with lip-sync
- 📺 **Real-time video** — see your lobster's expressions as it responds
- 🧠 **Same brain** — it's your OpenClaw agent, just with a face. Same memory, same personality
- 🌐 **中文 / English** — bilingual interface with language toggle

## Quick Start

When user runs `/claw-body`:

1. **Start the server**:
   ```bash
   node <skill-dir>/server.mjs
   ```

2. **Tell the user**:
   > 🦞 Claw Body is live: http://localhost:3099
   >
   > Two options:
   > - **Free trial** — chat with the demo lobster for 5 minutes
   > - **Your own avatar** — sign up at [nuwaai.com](https://nuwaai.com) (free), create your dream look, then enter your API Key + Avatar ID + User ID

## How It Works

```
You speak → ASR transcribes → OpenClaw agent replies → Avatar speaks with lip-sync
```

This skill uses NuwaAI's **humanctrl** mode with ASR:
- Your voice → NuwaAI speech recognition → text
- Text → OpenClaw Gateway → agent generates reply
- Reply → drives the avatar's voice and lip movements

**Same agent, new interface.** The avatar is just another channel — like iMessage or Telegram, but with a face.

## Features

- 🎤 Real-time voice input (ASR)
- 🗣️ Lip-synced avatar speech
- 🧠 Same OpenClaw agent — not a separate bot
- 📺 WebRTC real-time video stream
- 💬 Text input fallback
- 📱 Auto-adapts to portrait / landscape / square avatars
- 🔧 In-browser config — zero env vars needed
- 🎁 Free 5-min trial with demo avatar
- 🌐 Chinese / English bilingual UI
- 🔄 Disconnect / reconnect controls

## Create Your Own Avatar

1. Go to [nuwaai.com](https://nuwaai.com) — sign up is free
2. Create your avatar — first one is free!
3. Get your **API Key**, **Avatar ID**, and **User ID**
4. Enter them in the Claw Body interface
5. Done — your lobster now has a body 🦞

## Requirements

- OpenClaw Gateway running
- NuwaAI account (free sign-up)
- Modern browser (WebRTC + microphone)
- Node.js 18+

## ⚠️ First-Time Setup (Important!)

Claw Body talks to your OpenClaw agent via the Gateway's chat API. This endpoint is **disabled by default** and must be enabled once.

When user runs `/claw-body`:

1. Read `~/.openclaw/openclaw.json`
2. If `gateway.http.endpoints.chatCompletions.enabled` is not `true`, tell the user to enable it manually:
   > ⚠️ 首次使用需要启用 AI 对话接口，在 `~/.openclaw/openclaw.json` 中添加以下配置，然后重启 Gateway：
   > ```
   > openclaw gateway restart
   > ```
   > 重启后刷新页面即可。以后不需要再操作了。

Add this to `~/.openclaw/openclaw.json`:

```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true }
      }
    }
  }
}
```
