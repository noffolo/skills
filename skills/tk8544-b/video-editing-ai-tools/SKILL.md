---
name: video-editing-ai-tools
version: "1.0.0"
displayName: "Video Editing AI Tools — Smart Editing Assistance for Creators and Teams"
description: >
  Turn raw footage into polished, publish-ready content with AI-powered guidance built around video-editing-ai-tools workflows. Get instant recommendations on cuts, transitions, color grading, caption styles, pacing, and export settings — all without digging through tutorials. Whether you're editing short-form social clips, long-form YouTube content, or branded video ads, this skill helps you move faster and make smarter creative decisions at every stage of the edit.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "control"}}
---

## Getting Started

> Welcome to your AI-powered video editing assistant — here to help you cut faster, grade smarter, and publish with confidence. Tell me what you're working on and let's get your edit moving!

**Try saying:**
- "I'm editing a 10-minute YouTube video in DaVinci Resolve and the pacing feels slow in the middle section — how do I tighten it up without losing context?"
- "What's the best workflow for adding auto-captions and styling them for TikTok in CapCut?"
- "I have a talking-head interview with bad room echo — what AI tools or plugins can help clean up the audio inside Premiere Pro?"

### First-Time Connection

When a user first opens this skill, connect to the processing backend automatically. Briefly let them know (e.g. "Setting up...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 2.

1. **Obtain a free token**: Generate a random UUID as client identifier. POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to that UUID. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
2. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Edit Smarter, Not Harder — AI Meets the Timeline

Video editing has never been more accessible — but knowing which tools to use, when to cut, how to color grade, or what export settings actually matter? That's where most editors get stuck. This skill bridges the gap between raw footage and a finished product by giving you real, actionable editing guidance tailored to your specific project.

Whether you're working in Premiere Pro, DaVinci Resolve, CapCut, Final Cut Pro, or any other platform, you can describe what you're trying to achieve and get step-by-step direction, workflow suggestions, and creative input instantly. No more hunting through forums or watching 40-minute tutorials to answer a single question.

From beginner creators posting their first Reels to seasoned video professionals handling multi-camera shoots, this skill adapts to your experience level and editing goals. Ask about B-roll pacing, audio syncing, motion graphics, LUT recommendations, or how to structure a compelling story arc — and get answers that actually fit your timeline.

## Routing Edits to the Right Engine

Each request — whether you're triggering auto-cut, scene detection, color grading suggestions, or voiceover sync — is parsed by intent and routed to the appropriate AI processing pipeline based on task type and media context.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

All video inference tasks run on distributed GPU clusters via the ClawHub backend, handling frame analysis, timeline metadata, and model inference without pushing raw footage through the API. Responses return structured edit suggestions, timecode markers, or rendered preview URLs depending on the endpoint called.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `video-editing-ai-tools`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`.

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
| 2001 | No credits | Anonymous: show registration URL with `?bind=<id>` (get `<id>` from create-session or state response when needed). Registered: "Top up credits in your account" |
| 4001 | Unsupported file | Show supported formats |
| 4002 | File too large | Suggest compress/trim |
| 400 | Missing X-Client-Id | Generate Client-Id and retry (see §1) |
| 402 | Free plan export blocked | Subscription tier issue, NOT credits. "Register or upgrade your plan to unlock export." |
| 429 | Rate limit (1 token/client/7 days) | Retry in 30s once |

## Tips and Tricks

**Be specific about your software and goal.** Instead of asking 'how do I edit better,' tell the skill: 'I'm in Final Cut Pro editing a wedding highlight reel and I want it to feel cinematic at 3 minutes.' The more context you give, the more targeted the advice.

**Describe the problem, not just the task.** If a clip looks washed out, say so. If your audio peaks at -3dB but still sounds thin, mention it. Video editing ai tools guidance works best when it's solving a real problem you're experiencing in your timeline.

**Use it for decision fatigue.** Can't decide between two color grades? Unsure whether to cut on action or on dialogue? Paste both options into your prompt and ask for a recommendation based on your video's tone and audience.

**Ask about AI-native features in your editor.** Tools like Adobe Sensei, DaVinci's Magic Mask, or CapCut's auto-reframe are often underused. Ask this skill how to integrate those features into your specific project type for a real workflow upgrade.

## Use Cases

**Social Media Creators:** Get platform-specific advice on aspect ratios, caption placement, hook timing, and thumbnail-friendly frame selection for TikTok, YouTube Shorts, Instagram, and LinkedIn video.

**Freelance Video Editors:** Speed up client work by getting quick answers on color matching between clips, audio leveling standards, LUT stacking, and multi-cam sync workflows — without interrupting your creative flow.

**Marketing and Brand Teams:** Use this skill to plan video ad structures, choose the right pacing for conversion-focused content, and understand which editing techniques keep viewers watching longer.

**Beginners Learning the Craft:** If you're new to video editing ai tools and don't know where to start, describe your footage and goal and get a clear, jargon-free editing plan that walks you through each step in your chosen software.
