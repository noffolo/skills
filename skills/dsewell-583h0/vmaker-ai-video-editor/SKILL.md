---
name: vmaker-ai-video-editor
version: "1.0.0"
displayName: "Vmaker AI Video Editor — Edit, Enhance & Export Videos with Smart AI Tools"
description: >
  Turn raw footage into polished, share-ready videos using the vmaker-ai-video-editor skill. This tool brings Vmaker's AI-powered editing suite directly into your workflow — trimming clips, adding captions, applying transitions, and enhancing audio without manual frame-by-frame work. Built for content creators, marketers, and educators who need fast turnarounds. Supports mp4, mov, avi, webm, and mkv formats.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
apiDomain: https://mega-api-prod.nemovideo.ai
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! I'm your Vmaker AI Video Editor assistant — ready to help you trim, caption, enhance, and export your footage into something worth sharing. Drop your video file or describe what you'd like to edit, and let's get started.

**Try saying:**
- "Remove all the silent pauses and filler words from this screen recording and export a clean mp4"
- "Add auto-generated captions to my interview video and highlight the key quotes with text overlays"
- "Trim this 45-minute webinar down to a 3-minute highlight reel with transitions between segments"

### Quick Start Setup

This skill connects to NemoVideo's cloud backend. On first use, set up the connection automatically and let the user know ("Connecting to NemoVideo...").

**Token check**: Look for `NEMO_TOKEN` in the environment. If found, skip to session creation. Otherwise:
- Read `~/.config/nemovideo/client_id` or generate a UUID and save it there
- POST `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with `X-Client-Id` header
- Extract `data.token` from the response — this is your NEMO_TOKEN (100 free credits, 7-day expiry)

**Session**: POST `/api/tasks/me/with-session/nemo_agent` at the same host with Bearer auth and body `{"task_name":"project"}`. Keep the returned `session_id` for all operations.

Let the user know with a brief "Ready!" when setup is complete. Don't expose tokens or raw API output.

# Edit Smarter, Not Harder with Vmaker AI

The vmaker-ai-video-editor skill transforms how you approach video production. Instead of spending hours scrubbing through timelines and manually placing cuts, you describe what you want and the AI handles the heavy lifting — from trimming dead air to syncing captions with spoken words.

Designed with real creators in mind, this skill understands the difference between a rough screen recording and a finished product. Whether you're cleaning up a webinar, packaging a product demo, or turning a long-form interview into a punchy highlight reel, the editor applies intelligent decisions that match your intent.

You're not locked into a rigid template system either. The skill adapts to your footage — identifying natural pause points, flagging filler words in transcripts, and suggesting where B-roll or text overlays could add clarity. The result is a video that feels intentional and professional, even when you started with something completely unscripted.

## Routing Your Vmaker Edit Requests

When you describe a trim, caption drop, background swap, or AI enhancement, ClawHub maps your intent directly to the matching Vmaker AI endpoint so the right tool fires every time.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo Backend API Reference

Vmaker AI's editing pipeline runs on the NemoVideo backend, which handles render queues, AI model calls, and asset processing under the hood. Every clip edit, voiceover sync, or smart cut you trigger passes through NemoVideo's API before the final export lands in your Vmaker project.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `vmaker-ai-video-editor`
- `X-Skill-Version`: from frontmatter `version`
- `X-Skill-Platform`: detect from install path (`~/.clawhub/` → `clawhub`, `~/.cursor/skills/` → `cursor`, else `unknown`)

**All requests** must include: `Authorization: Bearer <NEMO_TOKEN>`, `X-Skill-Source`, `X-Skill-Version`, `X-Skill-Platform`. Missing attribution headers will cause export to fail with 402.

**API base**: `https://mega-api-prod.nemovideo.ai`

**Create session**: POST `/api/tasks/me/with-session/nemo_agent` — body `{"task_name":"project","language":"<lang>"}` — returns `task_id`, `session_id`. After creating a session, give the user a link: `https://nemovideo.com/workspace/claim?token=$TOKEN&task=<task_id>&session=<session_id>&skill_name=vmaker-ai-video-editor&skill_version=1.0.0&skill_source=<platform>`

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

## FAQ

**What video formats does vmaker-ai-video-editor support?** The skill works with mp4, mov, avi, webm, and mkv files, covering the most common formats used by screen recorders, cameras, and mobile devices.

**Can it edit videos with multiple speakers?** Yes. The AI can distinguish between speakers in interview-style footage and apply per-speaker captions when the audio separation is reasonably clear.

**How long can my video be?** The skill handles everything from short social clips to full-length webinars. For very long files, processing time increases — breaking a 2-hour recording into logical chapters before uploading can speed things up significantly.

**Will the AI make creative decisions on its own?** Only when you ask it to. If you request a highlight reel, it will make judgment calls about what to include. For precise edits, give specific instructions like timestamps or spoken phrases to cut around, and the skill will follow your direction closely.

## Tips and Tricks

To get the most out of vmaker-ai-video-editor, start by providing a clear description of your intended audience and purpose. Telling the skill 'this is a product demo for first-time users' versus 'this is an internal training video' changes how it prioritizes pacing and caption density.

When working with longer recordings like webinars or interviews, break your editing request into stages — first ask for a rough cut that removes silences and obvious errors, then refine with caption styling and transitions. This staged approach gives you more control over the final output.

For caption accuracy, mp4 and mov files with clear audio produce the best transcript results. If your footage has background noise, mention it upfront so the skill can apply appropriate audio enhancement before transcription. Always preview the generated captions before finalizing, especially for technical terminology or proper nouns that may need manual correction.
