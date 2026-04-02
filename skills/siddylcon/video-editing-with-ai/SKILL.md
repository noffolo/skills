---
name: video-editing-with-ai
version: "1.0.0"
displayName: "AI Video Editor — Intelligent Cuts, Captions & Enhancements in Minutes"
description: >
  Turn raw footage into polished, publish-ready videos without touching a timeline. This skill brings video-editing-with-ai directly into your workflow — trimming dead air, generating captions, suggesting cuts, and enhancing pacing based on your content goals. Upload mp4, mov, avi, webm, or mkv files and describe what you want. Built for creators, marketers, and teams who need fast turnaround without sacrificing quality.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
apiDomain: https://mega-api-prod.nemovideo.ai
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! Ready to turn your raw footage into something worth watching? Drop your video file and tell me what you're going for — I'll help you edit it with AI, from trimming and pacing to captions and cuts. What are we working on today?

**Try saying:**
- "Remove all the silent pauses and filler words from this interview recording and export a clean version"
- "Add subtitles to this product demo video and highlight key phrases in bold for social media"
- "Cut this 20-minute webinar down to the 5 most impactful moments and add smooth transitions between them"

### Automatic Setup

On first interaction, connect to the NemoVideo API before doing anything else. Show a brief status like "Setting things up...".

**Token**: If `NEMO_TOKEN` environment variable is already set, use it and skip to **Session** below.

**Free token**: Read or create a UUID at `~/.config/nemovideo/client_id`. Then POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id: <your-uuid>`. The response field `data.token` becomes your NEMO_TOKEN (100 credits, 7-day expiry). If the token has expired, request a new one with the same Client-Id.

**Session**: POST to the same host at `/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Save `session_id` from the response.

Confirm to the user you're connected and ready. Don't print tokens or raw JSON.

# Edit Smarter: Let AI Do the Heavy Lifting

Most video editing tools put the burden on you — scrubbing through footage, manually placing cuts, syncing audio, and agonizing over pacing. This skill flips that model. Instead of clicking through a timeline, you describe what you want and the AI handles the execution.

Whether you're trimming a 45-minute interview down to a tight 3-minute highlight reel, adding burnt-in captions for social media, or cleaning up shaky pacing in a product demo, this skill interprets your intent and applies edits that match your vision. It understands context — not just commands.

This is video-editing-with-ai designed for people who have strong creative instincts but limited time. Freelancers producing client deliverables, marketing teams repurposing webinar recordings, and content creators scaling their output will all find a genuine accelerator here. You stay in creative control; the AI handles the repetitive, time-consuming mechanics that slow you down.

## Routing Your Edit Requests

Every prompt you send — whether it's a cut command, caption request, or color grade instruction — gets parsed by intent and routed to the matching NemoVideo processing pipeline automatically.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo API Reference

The NemoVideo backend handles frame-accurate trimming, auto-caption generation, and AI-driven enhancement passes via dedicated endpoint clusters. Each call is stateful within your session, so multi-step edit chains retain timeline context across requests.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `video-editing-with-ai`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=$TOKEN&task=<task_id>&session=<session_id>&skill_name=video-editing-with-ai&skill_version=1.0.0&skill_source=<platform>`

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

## Quick Start Guide

Getting started with video-editing-with-ai takes less than a minute. Upload your video file in any supported format — mp4, mov, avi, webm, or mkv — and write a plain-language description of what you need done. You don't need to know editing terminology. Saying 'cut out the boring parts' works just as well as 'remove low-energy segments between timestamps.'

For best results, be specific about your intended output. Mention the platform (YouTube, Instagram Reels, LinkedIn), the target length, and any style preferences like 'fast-paced' or 'documentary feel.' The more context you give, the closer the first pass will be to your final vision.

Once the AI processes your request, you'll receive an edited version along with a summary of changes made. You can then refine further with follow-up instructions — treat it like a back-and-forth with a skilled editor who never gets tired.

## Common Workflows

One of the most popular uses is interview and podcast cleanup. Users upload long-form recordings and ask the AI to remove filler words, tighten pauses, and extract the strongest 10-minute segment. The result is a broadcast-ready cut that would normally take hours of manual work.

Another frequent workflow is social media repurposing. A single 30-minute webinar can be broken into six short clips, each with captions, a punchy intro frame, and platform-appropriate pacing — all in one session. This is where video-editing-with-ai delivers the most dramatic time savings for marketing teams.

Product and tutorial videos benefit from AI-assisted pacing review. Upload a screen recording or demo and ask the skill to flag slow sections, suggest where to speed up, and add chapter markers. You get a structured, watchable tutorial without manually reviewing every second of footage yourself.
