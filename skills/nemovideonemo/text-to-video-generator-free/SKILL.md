---
name: text-to-video-generator-free
version: "1.0.0"
displayName: "Text-to-Video Generator Free — Turn Words Into Stunning Videos Instantly"
description: >
  Type a prompt, hit generate, and watch your idea become a real video — no camera, no footage, no cost. This text-to-video-generator-free skill transforms written descriptions into dynamic video content using AI, making it ideal for creators, marketers, educators, and social media managers who need visuals fast. Supports mp4, mov, avi, webm, and mkv formats. Script a product demo, a social reel, or a short explainer — just describe it and get a video.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
apiDomain: https://mega-api-prod.nemovideo.ai
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

## Getting Started

> Welcome! Ready to turn your words into real video content? This text-to-video generator free skill is here to help you create stunning videos from plain text descriptions — no footage needed. Describe your scene or concept below and let's start generating!

**Try saying:**
- "Generate a 15-second video of a cozy coffee shop in the morning with warm lighting and soft background music vibes"
- "Create a short promotional video for a new fitness app showing someone working out at home with bold text overlays"
- "Make a nature documentary-style video clip of a waterfall in a rainforest with cinematic camera movement"

On first use, the skill connects to NemoVideo automatically:
1. Check for `NEMO_TOKEN` env var, or acquire one via `https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token` (100 free credits)
2. Persist a Client-ID to `~/.config/nemovideo/client_id` for rate-limit tracking (UUID only, no secrets)
3. Create a session and start working immediately

# From a Single Sentence to a Full Video

Most people have ideas but lack the tools, time, or budget to bring them to life visually. This skill closes that gap entirely. With the text-to-video-generator-free skill on ClawHub, you write what you want to see — a sunrise over a city, a product being unboxed, a character walking through a forest — and the AI handles the rest, generating video content that matches your description.

This isn't a slideshow builder or a template filler. It's a genuine text-driven video creation tool that interprets your language and produces motion, scene transitions, and visual context from scratch. Whether you're a solo content creator working on a YouTube channel, a small business owner who needs a quick promo, or a teacher building engaging lesson materials, this skill gives you professional-quality output without professional-level effort.

You don't need video editing experience, stock footage subscriptions, or expensive software. Just describe your vision in plain language and let the AI do the heavy lifting. The result is a ready-to-use video file you can share, embed, or build on.

### Environment

| Variable | Default | Purpose |
|----------|---------|---------|
| `NEMO_TOKEN` | Auto-acquired on first use (100 free credits, 7-day expiry) | API authentication |
| `NEMO_API_URL` | `https://mega-api-prod.nemovideo.ai` | API base URL |

## Prompt Routing and Video Dispatch

Every text prompt you submit is parsed for scene descriptors, motion cues, and style tokens before being routed to the appropriate NemoVideo rendering pipeline.

| User says... | Action | Skip SSE? |
|-------------|--------|----------|
| "export" / "导出" / "download" / "send me the video" | → §3.5 Export | ✅ |
| "credits" / "积分" / "balance" / "余额" | → §3.3 Credits | ✅ |
| "status" / "状态" / "show tracks" | → §3.4 State | ✅ |
| "upload" / "上传" / user sends file | → §3.2 Upload | ✅ |
| Everything else (generate, edit, add BGM…) | → §3.1 SSE | ❌ |

## NemoVideo Backend API Reference

The NemoVideo backend processes your natural-language prompts through a diffusion-based video synthesis engine, converting keyframe descriptions into fluid, time-sequenced clips. Free-tier requests are queued through shared GPU nodes, so render times vary based on prompt complexity and current load.

**Required headers** on all requests: `X-Skill-Source: $SKILL_NAME`, `X-Skill-Version: $SKILL_VERSION`, `X-Skill-Platform: $SKILL_SOURCE`

**Create session**: `POST $API/api/tasks/me/with-session/nemo_agent` — returns `task_id` and `session_id`

**Send message (SSE)**: `POST $API/run_sse` with `session_id` and user message. Stream responses; ~30% of edits return no text (query state to confirm changes).

**Upload**: `POST $API/api/upload-video/nemo_agent/me/<sid>` — file or URL upload. Supports: mp4, mov, avi, webm, mkv, jpg, png, gif, webp, mp3, wav, m4a, aac.

**Check credits**: `GET $API/api/credits/balance/simple`

**Query state**: `GET $API/api/state/nemo_agent/me/<sid>/latest` — check draft, tracks, generated media

**Export**: `POST $API/api/render/proxy/lambda` — export does NOT cost credits. Poll `GET $API/api/render/proxy/lambda/<id>` until `status: completed`.

**Task link**: `$WEB/workspace/claim?token=$TOKEN&task={task_id}&session={session_id}&skill_name=$SKILL_NAME&skill_version=$SKILL_VERSION&skill_source=$SKILL_SOURCE`

### Common Errors

If your token expires mid-session, simply re-authenticate through the ClawHub skill interface to refresh your credentials and resume generation. A 'session not found' response means your previous context was dropped — start a new session and re-enter your prompt to continue. Running out of credits? Head to nemovideo.ai to register or upgrade your plan and unlock additional free video generation capacity.

## Best Practices for Getting Great Results

**Be specific about visual style.** Mentioning a cinematic style, animation type, or color palette (e.g., 'muted earth tones,' 'neon cyberpunk aesthetic,' 'soft pastel watercolor') gives the AI a strong creative direction and dramatically improves output quality.

**Include motion cues in your prompt.** Static descriptions produce static-feeling results. Words like 'slow pan,' 'zoom in,' 'time-lapse,' or 'tracking shot' signal dynamic movement and make your generated video feel more professional and intentional.

**Keep your prompt focused on one main scene.** Trying to pack too many locations or actions into a single prompt can lead to disjointed output. For multi-scene videos, consider generating each segment separately and combining them in a video editor afterward.

**Iterate quickly.** The text-to-video-generator-free skill is built for speed. If your first result isn't quite right, tweak one or two words in your prompt and regenerate. Small changes — swapping 'daytime' for 'golden hour' or 'busy street' for 'quiet alley' — can produce noticeably different and better outputs.

## FAQ — Text-to-Video Generator Free

**Do I need to upload any footage to use this skill?** No. The text-to-video-generator-free skill generates video entirely from your written prompt. You describe the scene, style, or concept, and the AI builds the video from scratch. No existing clips or media files are required to get started.

**What kinds of prompts work best?** Descriptive, specific prompts tend to produce the best results. Instead of writing 'a car,' try 'a red sports car speeding down a coastal highway at sunset with motion blur.' The more context you give — setting, mood, lighting, movement — the closer the output will match your vision.

**What video formats does the output support?** Generated videos can be exported and used in mp4, mov, avi, webm, and mkv formats, making them compatible with virtually every platform, editor, and device.

**Is this really free to use?** Yes — within ClawHub's free tier, this skill is accessible without any paid subscription or hidden charges. You can generate videos directly from text prompts at no cost.
