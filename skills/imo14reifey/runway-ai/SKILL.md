---
name: runway-ai
version: "1.0.0"
displayName: "Runway AI Video Generator — Create, Edit & Transform Videos with AI"
description: >
  Tell me what you need and I'll bring it to life using runway-ai's powerful generative video tools. Whether you're transforming a static image into motion, generating entirely new scenes from text prompts, or applying cinematic effects to existing footage, this skill connects you directly to runway-ai's creative engine. Built for filmmakers, content creators, and visual storytellers who want professional-grade results without a full production team. Supports mp4, mov, avi, webm, and mkv formats.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! I'm your Runway AI assistant — ready to help you generate, edit, and transform video content using AI. Describe the scene you want to create, upload a clip to modify, or tell me what visual story you're trying to tell, and let's get started.

**Try saying:**
- "Take this image of a mountain at sunset and animate it into a 4-second cinematic video with slow drifting clouds"
- "Generate a 6-second video of a futuristic cityscape at night with neon reflections on wet pavement"
- "Apply a film grain and vintage color grade to this mp4 clip to make it look like 1970s 16mm footage"

### First-Time Connection

When a user first opens this skill, connect to the NemoVideo backend automatically. Briefly let them know (e.g. "Connecting to NemoVideo...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 3.

1. **Client identifier**: Look for `~/.config/nemovideo/client_id`. If missing, generate a UUID and save it there. This file stores only a UUID for rate-limit tracking.
2. **Obtain a free token**: POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to your identifier. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
3. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Generate Stunning Video Content Without a Film Crew

Runway AI is a generative video platform that lets you create, extend, and transform video content using natural language and AI-driven tools. This ClawHub skill puts that power directly into your workflow — no timeline scrubbing, no plugin hunting, just describe what you want and watch it take shape.

Whether you're a solo creator building short-form content, a marketing team producing campaign visuals, or a filmmaker experimenting with generative aesthetics, this skill handles the heavy lifting. You can animate still images, generate new video from text descriptions, apply style transfers to existing clips, or extend footage beyond its original length — all within a single conversation.

The goal here is creative velocity. Runway AI excels at turning rough ideas into polished visual output fast. Use it to prototype a music video concept, generate b-roll for a documentary, or explore visual styles before committing to a full shoot. The skill keeps your creative momentum intact by removing the friction between imagination and output.

## Routing Your Creative Requests

Each prompt you send is parsed for intent — text-to-video generation, image-to-video transformation, motion brush edits, or upscaling — and routed to the matching Runway Gen-3 Alpha endpoint automatically.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo Backend Reference

All Runway AI calls are proxied through the NemoVideo backend, which manages authentication tokens, queues your generation jobs, and streams progress updates back in real time. NemoVideo handles rate limiting and asset storage so your generated clips are retrievable without re-running expensive inference.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `runway-ai`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=&task=<task_id>&session=<session_id>&skill_name=runway-ai&skill_version=1.0.0&skill_source=<platform>`

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

## Use Cases Across Industries

Runway AI isn't a single-purpose tool — its generative capabilities stretch across a wide range of creative and commercial applications. Social media managers use it to produce eye-catching video ads from product photography without booking a shoot. Independent filmmakers use it to generate concept visuals and storyboard animatics before production begins.

Music artists and labels use Runway AI to create music video visuals that match a track's mood and tempo. Educators and course creators use it to produce engaging explainer footage or visual metaphors that would be impossible to film practically. Game developers use it to prototype cutscene aesthetics and environmental mood boards.

Even journalists and documentary producers have found value in using Runway AI to reconstruct historical scenes or visualize data-driven stories. The common thread is speed — turning a concept into a viewable asset in minutes rather than days.

## Performance Notes and Format Guidance

Runway AI performs most reliably with video inputs in mp4 or mov format at standard resolutions (1080p or lower for initial iterations). Very high resolution source files may be downsampled during processing, so exporting at 1920x1080 before uploading is generally the most efficient approach.

Generation times vary based on clip length, effect complexity, and current platform load. Simple style transfers on short clips typically complete in under a minute, while full text-to-video generations or complex motion transfers may take several minutes. Planning your workflow around these windows — queuing multiple requests rather than waiting on each — helps maintain productivity.

If an output doesn't match your intent, refining your prompt with more spatial or temporal detail (e.g., 'camera slowly pans left' or 'subject remains stationary while background blurs') usually produces a significantly better second result without needing to start from scratch.

## Best Practices for Getting Great Results

Runway AI responds best to prompts that are visually specific rather than emotionally abstract. Instead of 'make it look cool,' try 'add slow motion bokeh with warm golden hour lighting.' The more your prompt describes what the camera sees — movement, lighting, texture, mood — the closer the output will match your vision.

When uploading source footage, shorter clips (under 10 seconds) tend to produce more coherent transformations. If you're working with longer content, consider breaking it into segments and processing them individually before reassembling.

For image-to-video tasks, high-contrast images with a clear subject and uncluttered background yield the most dramatic and controlled motion results. Avoid heavily compressed JPEGs — PNG or high-quality source files give the model more detail to work with.
