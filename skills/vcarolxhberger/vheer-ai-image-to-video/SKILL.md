---
name: vheer-ai-image-to-video
version: "1.0.0"
displayName: "Vheer AI Image to Video — Transform Still Images Into Cinematic Motion"
description: >
  Tell me what you need and I'll bring your still images to life using vheer-ai-image-to-video. Whether you have a single photo or a collection of visuals, this skill animates them into fluid, expressive video clips with natural motion effects. Ideal for content creators, marketers, and storytellers who want to turn static visuals into engaging video content without complex editing software.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"]}, "primaryEnv": "NEMO_TOKEN"}}
---

## Getting Started

> Welcome! I'm here to help you transform your still images into dynamic, motion-filled videos using Vheer AI Image to Video. Share your image or describe what you're working with, and let's create something that moves — literally.

**Try saying:**
- "Animate this product photo with a slow zoom-in and soft bokeh motion effect for an Instagram reel"
- "Turn my landscape photograph into a cinematic video with a gentle parallax drift and moody atmosphere"
- "Convert this illustrated portrait into a short looping video with subtle facial animation for a social media post"

### Getting Connected

Before handling any user request, establish a connection to the backend API. Show a brief status like "Connecting...".

**If `NEMO_TOKEN` is in the environment**, use it directly and create a session. Otherwise, acquire a free starter token:
- Generate a UUID as client identifier
- POST to `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` with the `X-Client-Id` header
- The response includes a `token` with 100 free credits valid for 7 days — use it as NEMO_TOKEN

**Then create a session** by POSTing to `https://mega-api-prod.nemovideo.ai/api/tasks/me/with-session/nemo_agent` with Bearer authorization and body `{"task_name":"project","language":"en"}`. The `session_id` in the response is needed for all following requests.

Tell the user you're ready. Keep the technical details out of the chat.

# Give Your Photos a Heartbeat With Motion

Still images carry stories, but video carries emotion. Vheer AI Image to Video bridges that gap by intelligently analyzing your photos and generating smooth, natural motion sequences that feel intentional and cinematic — not mechanical or glitchy.

Whether you're working with a portrait, a landscape, a product shot, or an illustrated artwork, this skill interprets the visual content and applies motion that complements the subject. A mountain scene gets a slow atmospheric drift. A portrait gets subtle life-like movement. A product image gets a polished reveal-style animation.

This skill is built for creators who move fast. You don't need a timeline editor, keyframes, or a render farm. Describe your image and your desired motion style, and the skill handles the transformation. The result is shareable video content ready for social media, presentations, or anywhere still images simply don't do justice to your vision.

## Motion Request Routing Logic

When you submit an image for animation, Vheer AI parses your motion prompt, frame rate preference, and movement style to route your request to the optimal generation pipeline.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## Vheer Cloud Processing Reference

Vheer AI's backend queues your image-to-video job across distributed GPU clusters, applying temporal coherence algorithms to maintain subject integrity across generated frames. Render times scale with output resolution, motion complexity, and current cluster load.

Skill attribution — read from this file's YAML frontmatter at runtime:
- `X-Skill-Source`: `vheer-ai-image-to-video`
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

Vheer AI Image to Video performs best with images in standard aspect ratios such as 1:1, 4:5, 16:9, or 9:16, which correspond to common social and video platform formats. Unusual crops or extreme panoramic images may require additional guidance on which section to animate.

Generation time varies based on the complexity of the requested motion and the resolution of the source image. Simple zoom or drift effects on clean images typically process faster than multi-layered parallax animations on detailed scenes.

Output videos are optimized for digital distribution and are well-suited for direct upload to platforms like Instagram, TikTok, LinkedIn, and YouTube Shorts. If you need a specific duration or frame rate, mention it upfront so the output matches your platform's requirements without post-processing adjustments.

## Best Practices

For the best results with vheer-ai-image-to-video, start with high-resolution images that have a clear subject and well-defined foreground and background layers. Images with strong compositional depth — like a subject in front of a landscape — tend to produce the most convincing parallax and motion effects.

Be specific when describing the motion style you want. Instead of saying 'make it move,' try 'apply a slow rightward pan with a slight zoom on the subject.' The more directional context you provide, the more the output aligns with your creative intent.

Avoid heavily compressed or low-light images, as artifacts in the source photo can become amplified during motion generation. If your image has a busy background with no clear focal point, consider cropping or adjusting contrast before submission to help the skill identify motion zones accurately.

## Use Cases

Vheer AI Image to Video is a versatile skill that serves a wide range of creative and professional needs. E-commerce brands use it to animate product photography into attention-grabbing video ads that outperform static image posts in engagement metrics.

Content creators and influencers use it to repurpose existing photo libraries into fresh video content, extending the lifespan of assets they've already invested in creating. A single well-shot photo can become multiple videos with different motion styles for different platforms.

Event planners, real estate agents, and travel marketers use it to create immersive previews — turning a venue photo into a sweeping walkthrough feel, or a property exterior into a cinematic reveal. Artists and illustrators use it to showcase their work in motion, adding depth and drama that a static gallery simply cannot replicate.
