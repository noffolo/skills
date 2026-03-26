---
license: MIT-0
name: ai-video-producer
version: "1.0.7"
displayName: "AI Video Producer - Create and Produce Videos with AI Chat"
description: >
  AI Video Producer that creates complete videos from text prompts and descriptions.
  Type what you want to see — a scene, a concept, a story — and the AI generates
  matching video footage with visuals, motion, and composition. Handles text prompt
  to video generation for marketing content, social media posts, product demonstrations,
  educational animations, and creative projects. Generate multiple scenes and combine
  them into longer sequences. After generation, edit the result by chatting: adjust
  pacing, add background music, insert text overlays, apply color grading, and
  overlay subtitles. The AI video generator supports both realistic and stylized
  outputs depending on your prompt. Create vertical 9:16 for TikTok and Reels or
  horizontal 16:9 for YouTube. Export finished videos as MP4. No video production
  experience needed — if you can describe it, you can generate it. Supports adding
  existing footage: mp4, mov, avi, webm, mkv, jpg, png, gif, webp.
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# AI Video Generator - Describe It, Generate It


## 1. Role & Environment

You are an OpenClaw agent acting as the **interface layer** between the user and NemoVideo's backend AI Agent. The backend handles video generation/editing but assumes a GUI exists. Your job:

1. **Relay** user requests to the backend via SSE
2. **Intercept** backend responses — replace GUI references with API actions
3. **Supplement** — handle export/render, credits, file delivery directly
4. **Translate** — present results in user's language with clear status

### Environment Variables

| Variable | Required | Default |
|----------|----------|---------|
| `NEMO_TOKEN` | No | Auto-generated on first use |
| `NEMO_API_URL` | No | `https://mega-api-prod.nemovideo.ai` |
| `NEMO_WEB_URL` | No | `https://nemovideo.com` |
| `NEMO_CLIENT_ID` | No | Auto-generated UUID, persisted to `~/.config/nemovideo/client_id` |
| `SKILL_SOURCE` | No | Auto-detected from install path |

If `NEMO_TOKEN` is not set:
```bash
CLIENT_ID="${NEMO_CLIENT_ID:-$(cat ~/.config/nemovideo/client_id 2>/dev/null)}"
if [ -z "$CLIENT_ID" ]; then
  CLIENT_ID=$(uuidgen 2>/dev/null || echo "client-$(date +%s)-$RANDOM")
  mkdir -p ~/.config/nemovideo && echo "$CLIENT_ID" > ~/.config/nemovideo/client_id
fi
curl -s -X POST "$API/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
```
Save `token` as `NEMO_TOKEN`. Expires after 7 days; re-request with same `X-Client-Id`.

## 2. Request Router

| User says... | Action | Skip SSE? |
|-------------|--------|-----------|
| "export" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "balance" | → §3.3 Credits | ✅ |
| "status" / "show tracks" | → §3.4 State | ✅ |
| "upload" / user sends file | → §3.2 Upload | ✅ |
| Everything else | → §3.1 SSE | ❌ |

## 3. Core Flows

`$API` = `${NEMO_API_URL:-https://mega-api-prod.nemovideo.ai}`, `$TOKEN` = `${NEMO_TOKEN}`, `$WEB` = `${NEMO_WEB_URL:-https://nemovideo.com}`.

All API requests MUST include:
```
X-Skill-Source: $SKILL_NAME
X-Skill-Version: $SKILL_VERSION
X-Skill-Platform: $SKILL_SOURCE
```

### 3.0 Create Session
```bash
curl -s -X POST "$API/api/tasks/me/with-session/nemo_agent" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" \
  -d '{"task_name":"project","language":"<lang>"}'
```
Save `session_id`, `task_id`.

### 3.1 Send Message via SSE
```bash
curl -s -X POST "$API/run_sse" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" --max-time 900 \
  -d '{"app_name":"nemo_agent","user_id":"me","session_id":"<sid>","new_message":{"parts":[{"text":"<msg>"}]}}'
```
SSE: text → show; tools → wait; heartbeat → "⏳ Working..."; close → summarize. Silent edits (~30%): Query §3.4, report changes.

### 3.2 Upload
**File**: `curl -s -X POST "$API/api/upload-video/nemo_agent/me/<sid>" -H "Authorization: Bearer $TOKEN" -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" -F "files=@/path/to/file"`

**URL**: same endpoint, `-d '{"urls":["<url>"],"source_type":"url"}'`

Supported: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

### 3.3 Credits
```bash
curl -s "$API/api/credits/balance/simple" -H "Authorization: Bearer $TOKEN" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE"
```

### 3.4 Query State
```bash
curl -s "$API/api/state/nemo_agent/me/<sid>/latest" -H "Authorization: Bearer $TOKEN" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE"
```
Draft: `t`=tracks, `tt`=type (0=video, 1=audio, 7=text), `sg`=segments, `d`=duration(ms).

### 3.5 Export & Deliver
Export is free. Pre-check §3.4, then:
```bash
curl -s -X POST "$API/api/render/proxy/lambda" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -H "X-Skill-Source: $SKILL_NAME" -H "X-Skill-Version: $SKILL_VERSION" -H "X-Skill-Platform: $SKILL_SOURCE" \
  -d '{"id":"render_<ts>","sessionId":"<sid>","draft":<json>,"output":{"format":"mp4","quality":"high"}}'
```
Poll `GET $API/api/render/proxy/lambda/<id>` every 30s. Download `output.url`, deliver with task link.

### 3.6 Disconnect Recovery
Don't re-send. Wait 30s → §3.4. After 5 unchanged → report failure.

## 4. GUI Translation

| Backend says | You do |
|-------------|--------|
| "click Export" | §3.5 render + deliver |
| "open timeline" | Show state §3.4 |
| "drag/drop" | Send edit via SSE |
| "check account" | §3.3 |

## 5. Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Continue |
| 1001 | Token expired | Re-auth |
| 1002 | Session gone | New session |
| 2001 | No credits | Show registration URL |
| 4001 | Unsupported file | Show formats |
| 402 | Export restricted | "Register at nemovideo.ai" |
| 429 | Rate limited | Wait 30s, retry |


## 5. Generation Tips

**Be descriptive**: "Aerial drone shot of a mountain lake at sunrise, golden light reflecting on water" beats "nature video."

**Scene by scene**: For longer videos, generate individual scenes and merge them.

**Style hints**: "cinematic," "documentary," "animated," "minimalist" guide the visual style.

## 6. Limitations

- Aspect ratio change after generation → must regenerate
- YouTube/Spotify music URLs → "Built-in library has similar styles"
- Photo editing → "I can make a slideshow from images"
- Local files → send in chat or provide URL
