---
name: ai-text-to-video-generator-free
version: "1.0.0"
displayName: "AI Text to Video Generator Free — Turn Words Into Stunning Videos Instantly"
description: >
  Type a scene, a story, or a script — and watch it come to life. This ai-text-to-video-generator-free skill transforms written prompts into fully rendered video content without any cost barrier. Whether you're drafting a product explainer, a social media reel, or a narrative short, simply describe what you want and let the AI handle the visuals. Accepts mp4, mov, avi, webm, and mkv formats. Built for creators, marketers, educators, and storytellers who want professional-quality video output from plain text — no studio required.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! Ready to turn your words into real video content using our free AI text-to-video generator? Describe your scene, story, or message below and we'll start building your video right now.

**Try saying:**
- "Create a 30-second promotional video for a handmade candle brand with warm lighting, cozy home scenes, and upbeat background music"
- "Generate an educational video explaining how photosynthesis works, suitable for middle school students, with simple animations and clear narration"
- "Make a social media reel for a new coffee shop opening downtown — include street shots, latte art close-ups, and a welcoming vibe with text overlays"

### Quick Start Setup

This skill connects to NemoVideo's cloud backend. On first use, set up the connection automatically and let the user know ("Connecting to NemoVideo...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Read `~/.config/nemovideo/client_id` or generate a UUID and save it there
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `/api/tasks/me/with-session/nemo_agent` at the same host with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# From Blank Page to Bold Video in Seconds

Most people have ideas but lack the tools — or the budget — to bring them to screen. This skill closes that gap entirely. Describe your vision in plain language: a product launch, a travel montage, an educational walkthrough, or a brand story. The AI reads your words and builds a video that matches your intent, tone, and structure.

The ai-text-to-video-generator-free skill is designed for people who think in words but want to communicate in visuals. You don't need editing software, stock footage subscriptions, or design experience. Your prompt is the script, the storyboard, and the creative brief all at once.

Whether you're a solo content creator posting to YouTube, a small business owner building a product page, or a teacher crafting engaging lesson materials, this tool meets you where you are. Write naturally, refine your prompt, and generate polished video content that would otherwise take hours — or hundreds of dollars — to produce.

## Prompt Routing and Video Dispatch

When you submit a text prompt, the skill parses your scene description, style preferences, and duration cues, then routes the request directly to the NemoVideo rendering pipeline for free-tier video synthesis.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo API Reference Guide

The NemoVideo backend ingests your natural-language prompt and converts it into frame-by-frame video sequences using diffusion-based text-to-video models, supporting aspect ratios, motion intensity, and style tokens out of the box. Free-tier generation slots are allocated per session, so render queue times may vary based on platform load.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `ai-text-to-video-generator-free`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=&task=<task_id>&session=<session_id>&skill_name=ai-text-to-video-generator-free&skill_version=1.0.0&skill_source=<platform>`

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

## Use Cases

The ai-text-to-video-generator-free skill covers a wide range of real-world applications. Marketing teams use it to prototype ad concepts before committing to full production budgets. Educators build explainer videos for online courses without hiring animators. Podcasters repurpose episode summaries into shareable video clips for social distribution.

Small business owners find it especially useful for generating product showcase videos, seasonal promotions, and event announcements on a tight budget. Bloggers and journalists use it to add visual context to written stories. Even game developers and indie filmmakers use it to storyboard sequences or visualize concept scenes before production begins.

Because it's free to access, there's no risk in experimenting — try different prompt styles, genres, and formats until you find what resonates with your audience.

## Performance Notes

For best results with the ai-text-to-video-generator-free skill, write prompts that are specific rather than vague. Instead of 'make a video about nature,' try 'create a 20-second video featuring a misty forest at dawn with birds chirping and soft golden light filtering through the trees.' The more detail you provide — mood, pacing, visual style, subject matter — the closer the output will match your vision.

Video length and complexity affect generation time. Short clips under 60 seconds typically process faster. If you're uploading an existing video file (mp4, mov, avi, webm, or mkv) to use as a reference or base, keep file sizes reasonable to avoid delays. The skill handles most standard resolutions and aspect ratios, including vertical formats for mobile-first platforms like TikTok and Instagram Reels.

## Quick Start Guide

Getting started with the ai-text-to-video-generator-free skill takes less than a minute. First, decide what your video is about — write a one to three sentence description of the scene, subject, or story you want to tell. Include details like tone (energetic, calm, professional), setting (urban, nature, studio), and any specific visual elements you want included.

Paste your description into the prompt field and hit generate. Review the output and refine your prompt if needed — small tweaks like adding 'cinematic lighting' or 'fast-paced cuts' can significantly change the result. If you have an existing video file you'd like to enhance or use as a reference, upload it in mp4, mov, avi, webm, or mkv format alongside your prompt.

Once satisfied, download your video and use it directly on any platform — no watermarks, no paywalls, no complicated export settings.
