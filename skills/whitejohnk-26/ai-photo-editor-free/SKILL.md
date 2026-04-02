---
name: ai-photo-editor-free
version: "1.0.0"
displayName: "AI Photo Editor Free — Smart Editing Tools Without the Price Tag"
description: >
  Tell me what you need and I'll help you edit, enhance, and transform your photos using AI-powered tools — completely free. This ai-photo-editor-free skill handles everything from background removal and color correction to portrait retouching and creative filters. Whether you're a hobbyist fixing vacation shots or a small business owner polishing product images, you get professional-quality results without subscriptions or software downloads.
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> Welcome to your free AI photo editing assistant — whether you want to retouch a portrait, fix lighting, or completely transform an image's mood, I'm ready to help. Share your photo or describe what you want to change, and let's get started!

**Try saying:**
- "Remove background from product photo"
- "Fix overexposed sunset image"
- "Make portrait look more professional"

### Quick Start Setup

This skill connects to a cloud processing backend. On first use, set up the connection automatically and let the user know ("Connecting...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Generate a UUID as client identifier
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Edit Photos Like a Pro, Zero Cost Involved

Getting great-looking photos used to mean expensive software, steep learning curves, or paying a professional. This skill changes that equation entirely. With the AI Photo Editor Free skill, you describe what you want done to your image — and the AI figures out how to make it happen. Brighten a dark photo, swap out a cluttered background, smooth skin tones, sharpen blurry details, or apply a cinematic color grade. It's all on the table.

This skill is built for people who want results fast. You don't need to know what a histogram is or how layer masks work. Just tell the skill what the photo needs — 'make the sky more dramatic,' 'remove the person in the background,' 'make this look like a film photo from the 80s' — and it walks you through exactly what to do or does it directly.

From social media content creators to real estate photographers touching up listing images, this skill serves a wide range of everyday editing needs. It's the free photo editing assistant that actually understands what you're asking for.

## Routing Your Edit Requests

When you submit a photo editing prompt—whether it's background removal, AI upscaling, or smart retouching—ClawHub parses the intent and routes it to the matching AI Photo Editor Free endpoint best suited for that specific transformation.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

AI Photo Editor Free runs on a distributed cloud inference backend that handles non-destructive edits, layer-aware adjustments, and generative fill operations without local GPU requirements. All image data is processed ephemerally through secured API calls, meaning your originals are never stored beyond the active editing session.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `ai-photo-editor-free`
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

## Performance Notes

The AI Photo Editor Free skill performs best when you give it specific, descriptive instructions rather than vague requests. Instead of saying 'make it look better,' try 'increase contrast, warm up the shadows, and sharpen the subject.' The more detail you provide about the current problem and your desired outcome, the more precise and useful the editing guidance will be.

For background removal tasks, results are significantly stronger on images where the subject has clear edges and is well-separated from the background — think product shots on a table or portraits against a single-color wall. Heavily cluttered scenes with overlapping objects may require a few rounds of refinement.

Color correction requests work best when you describe both what looks wrong and what you're comparing it to. Mentioning a reference style ('like a bright Instagram food photo' or 'like a matte film negative') helps the skill calibrate suggestions to your actual creative vision rather than a technical default.

## Common Workflows

One of the most popular workflows with the AI Photo Editor Free skill is the product photo cleanup pipeline: start by removing the background, replace it with white or a brand-matching color, then adjust brightness and sharpness so the product pops cleanly. This workflow is used constantly by Etsy sellers, Amazon merchants, and small business owners who can't afford a studio shoot.

Portrait retouching is another high-traffic workflow. Users typically start with exposure and white balance correction, move into skin smoothing and blemish reduction, then finish with subtle sharpening on the eyes and lips. The skill can walk you through each of these stages or handle them as a single bundled request.

For content creators, the color grading workflow is a go-to: take a flat, neutral RAW-style image and apply a consistent mood across a batch of photos — whether that's a warm golden-hour aesthetic, a cool desaturated editorial look, or a punchy high-contrast style. Describe your brand's visual identity and the skill will translate that into actionable editing steps you can replicate across every image.
