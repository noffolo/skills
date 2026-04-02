---
name: ai-image-editor-free
version: "1.0.0"
displayName: "AI Image Editor Free — Edit, Enhance & Transform Photos Instantly Without Cost"
description: >
  Tired of paying monthly fees just to crop, retouch, or enhance a photo? ai-image-editor-free gives you powerful AI-driven image editing without a price tag. Remove backgrounds, fix lighting, upscale resolution, apply artistic filters, and retouch portraits — all through simple text instructions. Built for creators, bloggers, small business owners, and anyone who needs polished visuals fast. No design degree required.
metadata: {"openclaw": {"emoji": "🖼️", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN", "variant": "short_prompts"}}
---

## Getting Started

> Welcome to AI Image Editor Free — your no-cost solution for retouching, enhancing, and transforming images using plain language. Upload a photo or describe your edit and let's get started right now!

**Try saying:**
- "Remove background from product photo"
- "Upscale and sharpen this blurry image"
- "Add warm sunset filter to photo"

### Automatic Setup

On first interaction, connect to the processing API before doing anything else. Show a brief status like "Setting things up...".

**Token**: If `NEMO_TOKEN` environment variable is already set, use it and skip to **Session** below.

**Free token**: Generate a UUID as client identifier, then POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id: <uuid>`. The response field `data.token` becomes your NEMO_TOKEN (100 credits, 7-day expiry).

**Session**: POST to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Save `session_id` from the response.

Confirm to the user you're connected and ready. Don't print tokens or raw JSON.

# Edit Any Image With Words, Not Menus

Most image editors bury their best features behind paywalls, confusing interfaces, or subscription tiers you never fully use. AI Image Editor Free flips that model — you describe what you want done to your photo, and the AI handles the technical work. Whether you're fixing an overexposed vacation shot, removing an unwanted object from a product photo, or turning a selfie into a stylized illustration, this skill understands natural language and delivers results.

You don't need to know what a curves adjustment is or how to use a clone stamp tool. Just say 'make the background white' or 'sharpen the subject and blur the background' and watch it happen. This skill is designed for speed and accessibility — the kind of tool you reach for when you need something done in two minutes, not two hours.

Content creators, ecommerce sellers, social media managers, and everyday users will find this skill particularly useful. It handles everything from quick fixes to creative transformations, making professional-quality image editing genuinely free and genuinely easy.

## Routing Your Edit Requests

Each prompt you submit — whether it's background removal, style transfer, upscaling, or generative fill — is parsed and dispatched to the matching AI pipeline based on detected intent and image context.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Cloud Processing API Reference

AI Image Editor Free routes all pixel-level transformations through a distributed cloud inference backend, meaning no heavy GPU work runs on your device. Requests hit the processing nodes with your image payload, operation type, and parameter set, then return an optimized output URL once rendering completes.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `ai-image-editor-free`
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

AI Image Editor Free performs best on images that are at least 500px on the shortest side. Very small thumbnails or heavily compressed JPEGs may show artifacts after editing — if this happens, ask for a noise reduction pass after the main edit.

Complex edits involving multiple subjects or intricate backgrounds (like removing a person from a crowded street scene) may require a follow-up prompt to refine specific areas. Think of it as a conversation — your first prompt sets the direction, and follow-up prompts dial in the details.

For batch-style needs, describe a consistent edit style once and apply the same instructions across multiple images in sequence. While each image is processed individually, keeping your prompt language consistent ensures a uniform look across a set of photos.

## Common Workflows

**Ecommerce Product Photos:** Upload a product image, remove the background, replace it with white or a brand color, then add a subtle drop shadow. This three-step workflow is one of the most common uses and takes under a minute.

**Social Media Content:** Take a raw photo, apply a consistent color grade or filter style, resize it to the correct platform dimensions (square for Instagram, vertical for Stories), and sharpen for screen display. Describe the vibe — 'moody and dark' or 'bright and airy' — and the AI matches the tone.

**Portrait Retouching:** For headshots or profile photos, ask for skin smoothing, eye brightening, and background softening in a single prompt. The AI applies these adjustments without making the result look over-processed, keeping it natural.

**Restoration Work:** Old or damaged photos can be described as 'faded and scratched' and the skill will attempt to restore contrast, reduce noise, and reconstruct detail where possible.

## Tips and Tricks

To get the sharpest results from AI Image Editor Free, be specific in your instructions. Instead of saying 'fix this photo,' try 'increase contrast, reduce shadows in the foreground, and sharpen the subject.' The more context you give, the more accurate the output.

For background removal, photos with clear separation between subject and background (good lighting, minimal motion blur) yield the cleanest cuts. If edges look rough, ask for a second pass with 'refine the edges around the hair and shoulders.'

When upscaling, always start from the highest resolution source you have. Upscaling a 200px thumbnail will improve it, but starting from a 600px image will give you a noticeably crisper result. You can also chain edits — upscale first, then apply sharpening as a second instruction for best quality.
