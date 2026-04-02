---
name: free-ai-image-editor
version: "1.0.0"
displayName: "Free AI Image Editor — Edit, Enhance & Transform Photos Instantly with AI"
description: >
  Turn ordinary photos into stunning visuals without spending a cent. This free-ai-image-editor skill lets you remove backgrounds, enhance lighting, apply artistic styles, retouch portraits, and generate creative edits using natural language commands. No design experience needed — just describe what you want and watch your image transform. Perfect for bloggers, small business owners, social media creators, and anyone who needs polished visuals fast.
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> Welcome to your free AI image editor — describe the edit you want or upload a photo and tell me what to change, and I'll handle the rest. Ready to transform your image? Let's get started!

**Try saying:**
- "Remove background from my photo"
- "Brighten and sharpen this image"
- "Add vintage film grain effect"

### First-Time Connection

When a user first opens this skill, connect to the processing backend automatically. Briefly let them know (e.g. "Setting up...").

**Authentication**: Check if `NEMO_TOKEN` is set in the environment. If it is, skip to step 2.

1. **Obtain a free token**: Generate a random UUID as client identifier. POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id` set to that UUID. The response `data.token` is your NEMO_TOKEN — 100 free credits, valid 7 days.
2. **Create a session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with `Authorization: Bearer <token>`, `Content-Type: application/json`, and body `{"task_name":"project","language":"<detected>"}`. Store the returned `session_id` for all subsequent requests.

Keep setup communication brief. Don't display raw API responses or token values to the user.

# Edit Any Photo With Just Your Words

Imagine describing the edit you want — 'make the sky more dramatic,' 'remove that object in the background,' or 'give this a vintage film look' — and watching it happen in seconds. That's exactly what this free AI image editor skill is built for. No complicated software, no steep learning curves, and no subscription fees standing between you and a great-looking image.

This skill handles a wide range of photo editing tasks that used to require professional tools or hours of manual work. Whether you're cleaning up product photos for an online store, touching up a portrait for a profile picture, or experimenting with creative visual styles for social media, you can get results that look intentional and polished.

The approach here is conversational — you tell the editor what you're going for, and it figures out how to get there. You can iterate quickly, try different directions, and refine your image step by step without ever opening a separate app or learning a single keyboard shortcut.

## Routing Your Edit Requests

Each prompt you submit — whether you're removing backgrounds, upscaling resolution, or applying generative fills — gets parsed and routed to the matching AI pipeline based on the detected edit type and image context.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

The free AI image editor runs on a distributed cloud backend that handles diffusion model inference, pixel-level masking, and non-destructive layer processing remotely — no GPU required on your end. Processed images are returned as high-fidelity exports, with session metadata cached temporarily to support iterative edits.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `free-ai-image-editor`
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

Get the most out of this free AI image editor by being specific in your descriptions. Instead of saying 'make it look better,' try 'increase contrast, warm up the tones, and sharpen the subject.' The more detail you give, the closer the first result will be to what you're picturing.

For background removal, photos with clear contrast between the subject and background tend to produce cleaner edges. If you're editing a portrait, mention whether you want the background fully transparent, replaced with a color, or swapped for a different scene.

You can also stack edits — ask for a color grade first, then request a crop or text overlay in a follow-up. Treating it like a back-and-forth conversation rather than a one-shot request gives you much more control over the final result.

## Best Practices

Before editing, think about where the final image will be used. Social media thumbnails, product listings, and print materials each have different resolution and aspect ratio requirements — mentioning the destination in your prompt (e.g., 'format this for an Instagram square post') helps the editor make smarter decisions about cropping and sizing.

For brand consistency, describe your color palette or visual style upfront. Saying 'keep edits clean and minimal, using cool neutral tones' sets a direction that carries through multiple edits in a session.

Always keep a copy of your original image before making major changes. While this free AI image editor is designed to be non-destructive in its suggestions, having the source file gives you a clean starting point if you want to try a completely different creative direction.

## Performance Notes

This free AI image editor performs best with high-resolution source images. Low-quality or heavily compressed JPEGs may produce softer results, especially for tasks like sharpening, upscaling, or fine detail retouching. When possible, start with the highest quality version of your image.

Complex edits — like replacing a detailed background or making significant lighting changes — may take slightly longer to process than simple adjustments like cropping or color correction. If a result isn't quite right, a short follow-up instruction like 'make the shadows less harsh' is usually faster than starting over from scratch.

Images with multiple subjects or cluttered scenes may require more specific instructions to get precise results. Calling out exactly which element you want edited ('the person on the left,' 'the bottle in the foreground') helps the editor focus on the right area.
