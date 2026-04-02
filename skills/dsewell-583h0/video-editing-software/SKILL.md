---
name: video-editing-software
version: "1.0.0"
displayName: "Video Editing Software Guide — Master Every Tool, Cut, and Export Like a Pro"
description: >
  Drop a rough cut or describe your project and get expert guidance on video-editing-software in seconds. Whether you're stuck on color grading in DaVinci Resolve, confused by Premiere Pro's timeline, or choosing between CapCut and Final Cut Pro, this skill walks you through it. Get step-by-step editing workflows, software comparisons, export settings, and troubleshooting tips tailored to your specific tool and skill level.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "control"}}
---

## Getting Started

> Welcome to your video editing co-pilot — whether you're wrestling with a timeline, picking the right software, or trying to nail your export settings, I've got you covered. Tell me what you're working on and let's get your project moving.

**Try saying:**
- "I'm using DaVinci Resolve and I can't figure out how to do a smooth J-cut transition between two interview clips — can you walk me through it?"
- "I need to compare Adobe Premiere Pro vs Final Cut Pro for editing YouTube vlogs. I'm on a Mac and upload twice a week. Which one should I use?"
- "My exported video from Premiere Pro looks washed out and pixelated when I upload it to Instagram. What export settings should I be using?"

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Your On-Demand Video Editing Coach Is Here

Editing video is equal parts craft and software literacy — and most people get stuck not because they lack creativity, but because the tools get in the way. This skill bridges that gap by giving you instant, practical guidance across the most popular video-editing-software platforms available today, from beginner-friendly apps like CapCut and iMovie to professional-grade tools like Adobe Premiere Pro, DaVinci Resolve, and Final Cut Pro.

Describe what you're trying to accomplish — cut a talking-head interview down to two minutes, add animated text overlays, sync audio to a beat, fix shaky footage — and get a clear, actionable walkthrough tailored to the software you're actually using. No generic advice. No hunting through YouTube tutorials. Just the exact steps for your exact tool.

Whether you're a content creator editing Reels, a small business owner producing product videos, or a filmmaker working on a short film, this skill adapts to your workflow and experience level. Think of it as having an experienced editor sitting next to you, ready to answer the question you're embarrassed to Google.

## Routing Edits to the Right Tools

When you describe a task — trimming a clip, color grading a sequence, or exporting a final cut — your request is parsed and routed to the specific editing module, effect engine, or export pipeline best suited to handle it.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

All render-heavy operations — including multicam syncing, proxy generation, and codec transcoding — are offloaded to a distributed cloud backend that processes frame data in parallel to keep your timeline responsive. API calls return job IDs you can poll for render status, progress percentage, and output file URIs once encoding completes.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `video-editing-software`
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

## Use Cases

This skill covers the full range of video editing software scenarios that real creators and professionals face daily. Content creators can get help choosing between CapCut, DaVinci Resolve Free, and Premiere Pro based on their platform and upload frequency. Small business owners producing product demos or testimonial videos can learn the fastest path from raw footage to a polished final cut without a steep learning curve.

Filmmakers and video students working on narrative projects can get guidance on advanced techniques — multicam editing, color grading with LUTs, noise reduction in Audition, or visual effects workflows using After Effects alongside Premiere. Educators and course creators can learn how to add captions, zoom effects, and screen recordings efficiently.

Event videographers, wedding editors, and social media managers each have distinct workflows, and this skill adapts its guidance to match — whether that means batch exporting in Final Cut Pro or building a template-based workflow in CapCut for consistent brand output.

## Common Workflows

Some of the most frequently requested workflows include trimming and assembling a rough cut, syncing dual-camera or multi-mic audio, adding and styling lower-third text overlays, applying color correction and LUT-based color grading, and exporting for specific platforms like YouTube, TikTok, LinkedIn, or broadcast.

Users also frequently need help with: removing background noise from dialogue, stabilizing shaky handheld footage, creating smooth slow-motion sequences, building intro and outro animations, and converting horizontal footage to vertical 9:16 format without losing the subject in frame.

For software-specific workflows, this skill handles Premiere Pro sequence settings and proxy editing, DaVinci Resolve's Fusion and Color pages, Final Cut Pro's Magnetic Timeline and Roles system, and CapCut's template and auto-caption features. If your workflow involves multiple tools — say, editing in Premiere but compositing in After Effects — this skill can map out the handoff process step by step.
