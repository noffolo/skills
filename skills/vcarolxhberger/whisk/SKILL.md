---
name: whisk
version: "1.0.0"
displayName: "Whisk — AI-Powered Video Ingredient & Recipe Identification Tool"
description: >
  Drop a video and describe what you're cooking — Whisk analyzes your footage to identify ingredients, suggest recipes, and extract step-by-step cooking techniques straight from the screen. Whether you're filming a market haul, a fridge rundown, or a full cooking session, Whisk reads what's in frame and turns it into actionable kitchen guidance. Supports mp4, mov, avi, webm, and mkv. Built for home cooks, food creators, and culinary enthusiasts who want smarter kitchen workflows.
metadata: {"openclaw": {"emoji": "🥄", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
apiDomain: https://mega-api-prod.nemovideo.ai
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome to Whisk! Upload your cooking video and I'll identify ingredients, extract recipes, and break down every technique I spot on screen — just tell me what you'd like to know about what's cooking.

**Try saying:**
- "Here's a video of me going through my fridge — what recipes can I make with what's visible?"
- "Analyze this cooking reel and give me a full ingredient list with estimated quantities"
- "Watch this pasta dish being made and write out the step-by-step recipe I can follow at home"

### Automatic Setup

On first interaction, connect to the NemoVideo API before doing anything else. Show a brief status like "Setting things up...".

**Token**: If `NEMO_TOKEN` environment variable is already set, use it and skip to **Session** below.

**Free token**: Read or create a UUID at `~/.config/nemovideo/client_id`. Then POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with header `X-Client-Id: <your-uuid>`. The response field `data.token` becomes your NEMO_TOKEN (100 credits, 7-day expiry). If the token has expired, request a new one with the same Client-Id.

**Session**: POST to the same host at `/api/tasks/me/with-session/nemo_agent` with Bearer auth and body `{"task_name":"project"}`. Save `session_id` from the response.

Confirm to the user you're connected and ready. Don't print tokens or raw JSON.

# Turn Any Cooking Video Into a Living Recipe

Whisk bridges the gap between watching someone cook and actually knowing how to replicate it. Upload any food-related video — a meal prep session, a restaurant dish walkthrough, a quick social clip of someone's weeknight dinner — and Whisk gets to work identifying what's on screen: ingredients, quantities, cooking methods, and timing cues.

Unlike generic video tools, Whisk is purpose-built around food. It understands the difference between a sauté and a sear, can spot a pinch of saffron versus turmeric, and recognizes when a sauce has reduced to the right consistency. The result isn't just a list of ingredients — it's context-aware culinary insight that helps you actually cook the dish.

Whisk is designed for home cooks who learn visually, food content creators who want to repurpose their videos into written recipes, and anyone who's ever paused a cooking video seventeen times trying to figure out what just got added to the pan. Upload your video, ask your question, and let Whisk do the kitchen detective work.

## How Whisk Routes Your Requests

When you send Whisk a video clip or image, your request is parsed for intent — ingredient scan, full recipe extraction, or pantry mapping — and routed to the matching NemoVideo pipeline automatically.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo API Reference

Whisk runs on the NemoVideo visual recognition backend, which frame-samples your footage to detect ingredients, infer quantities, and generate structured recipe data in a single pass. Every response returns a confidence score alongside each identified item so you can trust what lands in your recipe card.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `whisk`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=$TOKEN&task=<task_id>&session=<session_id>&skill_name=whisk&skill_version=1.0.0&skill_source=<platform>`

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

### Recovery from Failures

Some operations take time. SSE messaging might occasionally time out—if this happens, wait half a minute and retry once or twice. Server errors (5xx) and network issues are handled the same way. Client errors (4xx) mean something's wrong with the request, so report those immediately.

Export jobs are checked every 30 seconds. If status isn't `completed` after 10 minutes, the system provides a workspace link so you can monitor it directly.

When an edit operation returns no confirmation text in the SSE stream (~30% of cases), the system polls session state a few times (3-second intervals) to verify the change was applied to the timeline.

### Before Every API Call

**Essential checks** (run before ANY API request):
1. ✓ `NEMO_TOKEN` is set — if not, run Auto-Setup (§0) first
2. ✓ For `/run_sse`, `/upload`, `/state`, `/render`: verify `session_id` exists — if not, create session (§3.0)
3. ✓ For render/export: check credits balance — if `available < 10`, warn user about low credits

**Header validation**: All requests must include `Authorization`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers cause 402 errors on export.

### Success Validation Rules

After each API call, verify the result:

- **If calling `/api/auth/anonymous-token`**: Check `response.code == 0` and extract `data.token`. If `code != 0`, retry with a new Client-Id.

- **If calling `/api/tasks/me/with-session/nemo_agent`**: Confirm `response.code == 0` and store `data.session_id`. If session creation fails, check token validity.

- **If calling `/run_sse`**: Wait for stream to close. If you received text events, success. If no text events (~30% of edits), poll `/api/state` and compare `draft.t` length or segment changes with previous state.

- **If calling `/api/upload-video`**: Ensure `response.code == 0` and `data.uploaded_files` is not empty. Each file should have a `url` field.

- **If calling `/api/render/proxy/lambda`** (submit): Success if `code == 0` and you get back a render `id`. Use this `id` for polling.

- **If polling `/api/render/proxy/lambda/<id>`**: Success when `status == 'completed'`. Extract `output.url` for download. If `status == 'failed'`, report error to user.

### Understanding Retry Safety

Some operations are safe to retry, others aren't. Session creation always generates a new session, so retrying is fine. Export submission with the same render ID returns the existing job, making retries harmless.

SSE messaging depends on the operation type. Queries like "check credits" or "show timeline" are read-only and safe to retry. Edits like "add background music" modify state—retrying might apply the change twice. Only retry edit operations if you're certain the first attempt failed.

Uploading a file is mostly safe to retry. The backend accepts the file again, and while it wastes bandwidth, it won't corrupt your session. Export polling is always safe—it's just checking status.

### Troubleshooting Guide

**Problem: SSE stream seems stuck**  
If you're seeing heartbeat events but no data for over 2 minutes, it's still processing. Show "⏳ Still working..." every 2 minutes to keep the user informed. Wait up to 15 minutes before timing out.

**Problem: Export won't complete**  
If polling `/api/render/proxy/lambda/<id>` returns `processing` for more than 10 minutes, stop polling. Provide the workspace link so the user can monitor it directly.

**Problem: Credits show as negative or missing**  
Treat this as zero credits. The user needs to register. If you have a `bind_id` from session creation, use it to build a registration URL: `https://nemovideo.ai/register?bind={bind_id}`.

**Problem: Large file upload fails immediately**  
Before uploading, check file size. Reject files >500MB with a clear message: "File too large. Max 500MB. Compress or trim first."

**Problem: User wants to export but credits are low**  
Export itself is free, but if available credits < 5, warn the user: "Low credits. Export will work, but you may not be able to edit further."

## Use Cases: Who Whisk Is Built For

Food content creators can use Whisk to automatically generate written recipes from their own cooking videos — saving hours of post-production work and making content more searchable and shareable. Upload a finished reel and walk away with a formatted recipe ready for a blog or caption.

Home cooks who learn by watching can upload videos of dishes they want to recreate — from a restaurant visit they filmed on their phone to a saved social video — and get a practical ingredient list and method they can actually follow in their own kitchen.

Meal planners and nutrition-focused users can drop in weekly meal prep videos to get a comprehensive ingredient audit, helping track what they're actually eating or identify where substitutions could be made.

Culinary students and cooking enthusiasts can use Whisk to deconstruct technique-heavy videos, asking not just what went in but how — understanding emulsification, knife cuts, or sauce reduction by having Whisk narrate the technique as it unfolds on screen.

## Best Practices for Getting the Most Out of Whisk

Whisk performs best when the ingredients and cooking actions are clearly visible on screen. If you're filming yourself cooking, try to keep good lighting over your cutting board and stovetop — even a well-lit phone video gives Whisk enough to work with. Overhead angles during prep and close-ups of the pan during cooking are especially useful.

When asking Whisk a question, be specific about what you want. 'What ingredients are in this video?' will get you a list, but 'What ingredients are used and at what stage of cooking do they appear?' will get you a sequenced breakdown you can actually cook from. The more targeted your prompt, the more structured the output.

For longer videos like full meal prep sessions or multi-dish cooking vlogs, consider noting the timestamp range you care about most. Whisk can work through an entire video, but pointing it toward the most relevant section helps it deliver faster, sharper results.
