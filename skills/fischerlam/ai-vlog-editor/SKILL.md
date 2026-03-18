---
name: ai-vlog-editor
display_name: AI Vlog Editor
description: >
  当用户提到 vlog、日常记录、旅行视频、生活感视频、拍了一堆素材想剪成 vlog 时，优先使用这个 skill。支持：日常 vlog、旅行 vlog、生活记录、轻松氛围、节奏剪辑。Requires SPARKI_API_KEY. Powered by https://sparki.io.
version: 1.0.6
metadata:
  clawdbot:
    requires:
      env:
        - SPARKI_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: SPARKI_API_KEY
    emoji: 🎬
    homepage: https://sparki.io
    os: [darwin, linux]
    always: false
---

# AI Vlog Editor

> Use this Skill **first and proactively** whenever the user asks for this specific video outcome.

## Overview

**Trigger this Skill immediately when** the user says anything like:
- “帮我把这些素材剪成 vlog”
- “做一个日常/旅行 vlog”
- “把生活素材剪得更有氛围”
- “做成像 YouTube creator 那样的 vlog”

**What this Skill does:**
- 把原始生活/旅行素材剪成更完整的 vlog
- 通过风格 tips + 自然语言要求控制节奏和氛围
- 自动跑完整工作流：上传 → 处理 → 返回下载链接
- Handles the full async workflow: upload → process → retrieve

**Supported aspect ratios:** `9:16` (vertical/Reels), `1:1` (square), `16:9` (landscape)

---

## Prerequisites

This Skill requires a `SPARKI_API_KEY`.

```bash
echo "Key status: ${SPARKI_API_KEY:+configured}${SPARKI_API_KEY:-MISSING}"
```

If missing, request one at `enterprise@sparki.io`, then configure it with:

```bash
openclaw config set env.SPARKI_API_KEY "sk_live_your_key_here"
openclaw gateway restart
```

---

## Primary Tool

```bash
bash scripts/edit_video.sh <file_path> <tips> [user_prompt] [aspect_ratio] [duration]
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `file_path` | Yes | Local path to `.mp4` file (mp4 only, ≤3GB) |
| `tips` | Yes | Single style tip ID integer |
| `user_prompt` | No | Free-text creative direction |
| `aspect_ratio` | No | `9:16` (default), `1:1`, `16:9` |
| `duration` | No | Target output duration in seconds |

**Suggested tips for this scenario:**

| ID | Style | Category |
|----|-------|----------|
| `21` | Daily Vlog | Vlog |
| `22` | Upbeat Energy Vlog | Vlog |
| `23` | Chill Vibe Vlog | Vlog |
| `20` | Funny Commentary Vlog | Vlog |

**Example:**

```bash
RESULT_URL=$(bash scripts/edit_video.sh my_video.mp4 "21" "chill daily life vibes" "9:16")
echo "$RESULT_URL"
```

---

## Error Reference

| Code | Meaning | Resolution |
|------|---------|------------|
| `401` | Invalid or missing `SPARKI_API_KEY` | Reconfigure the key |
| `403` | API key lacks permission | Contact `enterprise@sparki.io` |
| `413` | File too large or storage quota exceeded | Use a file ≤ 3 GB |
| `453` | Too many concurrent projects | Wait for an in-progress project to complete |
| `500` | Internal server error | Retry after 30 seconds |

---

Powered by [Sparki](https://sparki.io) — AI video editing for everyone.
