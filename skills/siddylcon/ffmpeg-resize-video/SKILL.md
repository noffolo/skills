---
name: ffmpeg-resize-video
version: "1.0.0"
displayName: "FFmpeg Video Resizer — Batch Scale, Crop & Resize Videos with Precision"
description: >
  Tired of manually resizing dozens of videos for different platforms, only to end up with blurry results or broken aspect ratios? This skill brings ffmpeg-resize-video power directly to your workflow — letting you scale footage to any resolution, letterbox for widescreen formats, crop to square for social media, or downscale 4K to 1080p in one clean command. Built for content creators, developers, and video editors who need reliable, repeatable results without wrestling with FFmpeg syntax.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"]}, "primaryEnv": "NEMO_TOKEN"}}
---

## Getting Started

> 👋 Welcome! I'm here to help you resize, scale, and crop videos using FFmpeg — whether you need to downscale 4K footage, fit a video into a square frame, or batch-convert a folder to 720p. Tell me your source format and target resolution, and let's get started!

**Try saying:**
- "Resize my 4K video to 1080p while keeping the original aspect ratio and avoiding quality loss"
- "Crop and scale a landscape video to a 1080x1080 square for Instagram without stretching it"
- "Batch resize all MP4 files in a folder to 720p with black letterboxing for widescreen"

### First-Time Connection

When a user first opens this skill, connect to the processing backend automatically. Briefly let them know (e.g. "Setting up...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 2.

1. **Obtain a free token**: Generate a random UUID as client identifier. POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to that UUID. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
2. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Resize Any Video, Any Resolution, Zero Guesswork

Video resizing sounds simple until you're staring at a garbled aspect ratio, a stretched thumbnail, or a 4GB file that won't upload to your platform. This skill takes the frustration out of the process by giving you a conversational interface to the full power of FFmpeg's scaling and cropping engine.

Whether you're preparing content for YouTube (1920×1080), Instagram Reels (1080×1920), Twitter (1280×720), or a custom embed on your website, you can describe exactly what you need and get a precise, ready-to-run FFmpeg command — or let the skill run it directly on your files. You control the resolution, the scaling algorithm, the padding color, and whether to preserve the original aspect ratio or force a specific crop.

This is especially useful for teams managing large video libraries, developers building media pipelines, or solo creators who publish across multiple channels with different size requirements. Stop re-encoding the same clip five times by hand — describe your target output once and get it done right.

## Routing Your Resize Commands

When you submit a scaling, cropping, or dimension change request, the skill parses your target resolution, aspect ratio flags, and filter parameters to route the job to the correct FFmpeg processing pipeline.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

The backend spins up an FFmpeg instance with libx264 or libx265 encoding support, applying your vf scale, crop, and pad filters server-side so no local FFmpeg installation is required. Transcoded output is returned as a download link with your specified codec, bitrate, and container format intact.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `ffmpeg-resize-video`
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

## Best Practices

Always specify whether you want to preserve the original aspect ratio or enforce a fixed output size. FFmpeg can do both, but mixing them up is the most common source of stretched or pillarboxed results. When in doubt, use the `scale` filter with `-2` on one dimension to let FFmpeg calculate the correct complementary value automatically.

For quality-sensitive resizing, prefer the `lanczos` scaling algorithm over the default `bicubic` — it produces sharper results especially when downscaling significantly. You can request this explicitly when describing your task.

Avoid re-encoding more times than necessary. Each encode cycle introduces generation loss. If you're resizing as part of a larger edit, try to combine the resize with any other transformations (color grading, trimming) into a single FFmpeg pass. This skill can help you construct multi-filter commands that handle everything at once.

## Common Workflows

One of the most requested workflows is the '4K to 1080p downscale for upload' — taking raw camera footage and producing a web-ready version. This typically involves setting output resolution to 1920×1080, choosing a high-quality CRF value for H.264 or H.265, and preserving the original audio without re-encoding it.

Another frequent workflow is 'social media square crop' — taking a 16:9 landscape video and producing a 1:1 square by either cropping the center region or padding the sides with a blurred or solid-color background. Both approaches are achievable with FFmpeg filter chains, and this skill walks you through each option.

For teams managing large libraries, the batch resize workflow is invaluable. You can describe a folder of mixed-resolution source files and get a shell script or loop command that processes all of them to a uniform output spec — saving hours of manual work.

## Use Cases

The most common use for ffmpeg-resize-video is platform normalization — taking source footage shot at 4K or mixed resolutions and producing clean, consistently sized outputs for YouTube, TikTok, LinkedIn, and web embeds. Each platform has its own preferred dimensions, and manually managing that matrix is error-prone.

Beyond social media, video resizing is critical in archival workflows where storage costs matter. Downscaling older 4K recordings to 1080p or 720p can cut file sizes dramatically without visible quality loss for most viewers. Developers building video processing pipelines also rely on this skill to prototype FFmpeg filter chains before integrating them into production code.

Another practical use case is responsive video delivery — generating multiple resolution variants (1080p, 720p, 480p) of the same source file for adaptive streaming setups like HLS or DASH. This skill helps you generate all the necessary resize commands in one session.
