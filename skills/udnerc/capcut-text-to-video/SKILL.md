---
name: capcut-text-to-video
version: "1.0.0"
displayName: "CapCut Text to Video — Turn Scripts & Prompts Into Polished Videos Instantly"
description: >
  Tell me what you need and I'll transform your written ideas into compelling videos using capcut-text-to-video capabilities. Whether you're turning a blog post into a short-form reel, converting a product description into a promo clip, or building a story from a script, this skill handles the heavy lifting. Supports mp4, mov, avi, webm, and mkv output formats. Built for content creators, marketers, and social media managers who want fast, high-quality video without manual editing.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! I'm here to help you turn your text, scripts, or ideas into real videos using CapCut's text-to-video engine. Drop your script, describe the video you have in mind, or share a prompt — and let's start creating something worth watching.

**Try saying:**
- "Create a 30-second promotional video for a new coffee brand using this product description: 'Rich, bold espresso blends sourced from Colombian highlands.'"
- "Turn this blog post intro into a short Instagram Reel script and generate a video with upbeat pacing and text overlays."
- "Generate a motivational video from this quote: 'Success is built one small decision at a time.' — use cinematic visuals and a calm voiceover tone."

### First-Time Connection

When a user first opens this skill, connect to the NemoVideo backend automatically. Briefly let them know (e.g. "Connecting to NemoVideo...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 3.

1. **Client identifier**: Look for `~/.config/nemovideo/client_id`. If missing, generate a UUID and save it there. This file stores only a UUID for rate-limit tracking.
2. **Obtain a free token**: POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to your identifier. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
3. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# From Words on a Page to Videos That Move People

Writing a script is one thing — turning it into a video that actually holds attention is another challenge entirely. The capcut-text-to-video skill bridges that gap by taking your raw text input and generating structured, visually engaging video content through CapCut's powerful generation engine. You bring the idea; this skill brings it to life.

Whether you're a solo creator working on YouTube Shorts, a brand manager producing product explainers, or a marketer cranking out social content on a deadline, this skill fits naturally into your workflow. Paste in a prompt, a script excerpt, or even a rough outline — and get back a video ready for review, refinement, or direct publishing.

The skill is designed around real creative use cases: promotional storytelling, educational walkthroughs, narrative reels, and announcement clips. It doesn't just stitch together generic stock footage — it interprets your text to build scenes that reflect tone, pacing, and intent. Think of it as your on-demand video production assistant that actually reads what you write.

## Routing Scripts to Video

Every request — whether it's a raw script, a one-line prompt, or a structured storyboard — gets parsed and routed to CapCut's Text to Video pipeline via the NemoVideo backend, matching your input type to the right generation parameters automatically.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo API Reference

NemoVideo acts as the middleware layer that authenticates your session, queues your text-to-video job, and streams the rendered output back once CapCut's engine finishes processing your script into scenes. All generation calls, polling requests, and asset retrieval happen through NemoVideo's endpoints — CapCut's native API is never called directly.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `capcut-text-to-video`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=&task=<task_id>&session=<session_id>&skill_name=capcut-text-to-video&skill_version=1.0.0&skill_source=<platform>`

**Send message (SSE)**: POST `/run_sse` — body `{"app_name":"nemo_agent","user_id":"me","session_id":"<sid>","new_message":{"parts":[{"text":"<msg>"}]}}` with `Accept: text/event-stream`. Max timeout: 15 minutes.

**Upload**: POST `/api/upload-video/nemo_agent/me/<sid>` — file: multipart `-F "files=@/path"`, or URL: `{"urls":["<url>"],"source_type":"url"}`

**Credits**: GET `/api/credits/balance/simple` — returns `available`, `frozen`, `total`

**Session state**: GET `/api/state/nemo_agent/me/<sid>/latest` — key fields: `data.state.draft`, `data.state.video_infos`, `data.state.generated_media`

**Export** (free, no credits): POST `/api/render/proxy/lambda` — body `{"id":"render_<ts>","sessionId":"<sid>","draft":<json>,"output":{"format":"mp4","quality":"high"}}`. Poll GET `/api/render/proxy/lambda/<id>` every 30s until `status` = `completed`. Download URL at `output.url`.

Supported formats: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

### SSE Event Handling

| Event | Action |
|-------|--------|
| Text response | Apply GUI translation (§4), present to user |
| Tool call/result | Process internally, don't forward |
| `heartbeat` / empty `data:` | Keep waiting. Every 2 min: "⏳ Still working..." |
| Stream closes | Process final response |

~30% of editing operations return no text in the SSE stream. When this happens: poll session state to verify the edit was applied, then summarize changes to the user.

### Backend Response Translation

The backend assumes a GUI exists. Translate these into API actions:

| Backend says | You do |
|-------------|--------|
| "click [button]" / "点击" | Execute via API |
| "open [panel]" / "打开" | Query session state |
| "drag/drop" / "拖拽" | Send edit via SSE |
| "preview in timeline" | Show track summary |
| "Export button" / "导出" | Execute export workflow |

**Draft field mapping**: `t`=tracks, `tt`=track type (0=video, 1=audio, 7=text), `sg`=segments, `d`=duration(ms), `m`=metadata.

```
Timeline (3 tracks): 1. Video: city timelapse (0-10s) 2. BGM: Lo-fi (0-10s, 35%) 3. Title: "Urban Dreams" (0-3s)
```

### Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Continue |
| 1001 | Bad/expired token | Re-auth via anonymous-token (tokens expire after 7 days) |
| 1002 | Session not found | New session §3.0 |
| 2001 | No credits | Anonymous: show registration URL with `?bind=<id>` (get `<id>` from create-session or state response when needed). Registered: "Top up at nemovideo.ai" |
| 4001 | Unsupported file | Show supported formats |
| 4002 | File too large | Suggest compress/trim |
| 400 | Missing X-Client-Id | Generate Client-Id and retry (see §1) |
| 402 | Free plan export blocked | Subscription tier issue, NOT credits. "Register at nemovideo.ai to unlock export." |
| 429 | Rate limit (1 token/client/7 days) | Retry in 30s once |

## Integration Guide

Getting started with the capcut-text-to-video skill is straightforward — no complex setup required on your end. Simply provide your text input directly in the chat: this can be a full script, a short prompt, a product description, or a list of key talking points. The skill interprets your input and sends it through CapCut's generation pipeline to produce your video.

Once the video is generated, you'll receive a downloadable file in your preferred format — mp4, mov, avi, webm, or mkv. If you're embedding videos into a website, mp4 is typically the safest choice for browser compatibility. For mobile-first platforms like TikTok or Instagram, mp4 or mov tend to perform best.

If you're working with longer scripts, break them into logical scenes or segments before submitting. This helps the skill maintain visual coherence and pacing across the full video. You can also specify tone, style preferences (cinematic, upbeat, minimal), or target platform in your prompt to fine-tune the output.

## Performance Notes

Generation time for capcut-text-to-video outputs will vary depending on the length and complexity of your input text. Short prompts under 100 words typically resolve quickly, while longer scripts or multi-scene requests may take additional processing time. Plan accordingly if you're working against a publishing deadline.

For best results, write clear and specific prompts. Vague inputs like 'make a cool video' produce less targeted results than structured requests that mention subject matter, tone, duration, and intended platform. The more context you provide, the more aligned the output will be with your creative vision.

If a generated video doesn't match your expectations on the first pass, refine your prompt rather than resubmitting the same input. Small changes — like specifying 'fast-paced editing' or 'minimalist visuals with white background' — can meaningfully shift the final output. Iteration is a natural part of the text-to-video workflow.
