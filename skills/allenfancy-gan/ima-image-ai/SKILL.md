---
name: "IMA Image Generator"
version: 1.0.8
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, AI image generator, image generator, AI photo generator, product photo, poster generator, thumbnail generator, logo generator, AI art generator, illustration, graphic design, social media image, text to image, image to image
argument-hint: "[text prompt or image URL]"
description: >
  AI image generator and photo generator with SeeDream 4.5, Midjourney, Nano Banana 2, and
  Nano Banana Pro. Generate AI images for posters, thumbnails, logos, art, illustrations,
  product photos, and social media graphic design. Text-to-image and image-to-image AI
  generation with intelligent model selection and knowledge base support. AI poster generator,
  AI thumbnail generator, AI logo generator, AI art generator, AI illustration generator,
  product photo generator, and social media image generator in one unified tool. Supports
  1K/2K/4K resolution and custom aspect ratios. Better alternative to DALL-E, Stable Diffusion,
  or standalone image generation skills. Requires IMA_API_KEY.
requires:
  env:
    - IMA_API_KEY
  runtime:
    - python3
  packages:
    - requests
  primaryCredential: IMA_API_KEY
  credentialNote: "IMA_API_KEY is required at runtime. It is sent to api.imastudio.com and, for local image uploads, to imapi.liveme.com."
metadata:
  openclaw:
    primaryEnv: IMA_API_KEY
    homepage: https://www.imaclaw.ai
    requires:
      bins:
        - python3
      env:
        - IMA_API_KEY
persistence:
  readWrite:
    - ~/.openclaw/memory/ima_prefs.json
    - ~/.openclaw/logs/ima_skills/
instructionScope:
  crossSkillReadOptional:
    - ~/.openclaw/skills/ima-knowledge-ai/references/*
---

# IMA Image AI — Image Generator

**For complete API documentation, security details, all parameters, and Python examples, read `SKILL-DETAIL.md`.**

## Model ID Reference (CRITICAL)

Use **exact model_id** from this table. Do NOT infer from friendly names.


| Friendly Name   | model_id                 | Notes                             |
| --------------- | ------------------------ | --------------------------------- |
| SeeDream 4.5    | `doubao-seedream-4.5`    | ✅ Recommended default, 5 pts      |
| Nano Banana2    | `gemini-3.1-flash-image` | ⚠️ NOT nano-banana-2, 4-13 pts    |
| Nano Banana Pro | `gemini-3-pro-image`     | ⚠️ NOT nano-banana-pro, 10-18 pts |
| Midjourney      | `midjourney`             | ✅ Same as friendly name, 8-10 pts |


**User input aliases:** 香蕉/Banana → `gemini-3.1-flash-image` · 香蕉Pro → `gemini-3-pro-image` · 可梦/SeeDream → `doubao-seedream-4.5` · MJ/Midjourney → `midjourney`

## Image Generation Modes


| User intent              | task_type        | When to use                        |
| ------------------------ | ---------------- | ---------------------------------- |
| Text only, no image      | `text_to_image`  | "画一张…" / "生成图片" / "text to image"  |
| Image as reference/input | `image_to_image` | "把这张图…" / "参考这张图" / "图生图" / "风格迁移" |


## Visual Consistency (IMPORTANT)

If user mentions "same character", "series", "multi-shot", or continues from a previous generation:

- **Do NOT use text_to_image** (will produce different-looking results)
- Use `image_to_image` with previous result as reference
- Read `ima-knowledge-ai/references/visual-consistency.md` if available

## Pre-Check: Knowledge Base

**If ima-knowledge-ai is installed**, read before generating:

1. `ima-knowledge-ai/references/visual-consistency.md` — if multi-shot or character continuity needed

**If not installed:** use this SKILL's model table and defaults.

## Model Selection Priority

1. **User preference** (if explicitly stated) → highest priority
2. **ima-knowledge-ai recommendation** (if installed)
3. **Fallback defaults:**


| Task                     | Default Model   | model_id                 | Cost      |
| ------------------------ | --------------- | ------------------------ | --------- |
| text_to_image            | SeeDream 4.5    | `doubao-seedream-4.5`    | 5 pts     |
| text_to_image (budget)   | Nano Banana2    | `gemini-3.1-flash-image` | 4 pts     |
| text_to_image (premium)  | Nano Banana Pro | `gemini-3-pro-image`     | 10-18 pts |
| text_to_image (artistic) | Midjourney 🎨   | `midjourney`             | 8-10 pts  |
| image_to_image           | SeeDream 4.5    | `doubao-seedream-4.5`    | 5 pts     |


## User Input Parsing

**Size/Resolution:** 512/1K/2K/4K → via attribute_id for Nano Banana series
**Aspect ratio:** 16:9/9:16/4:3/3:4/1:1 → SeeDream 4.5 or Nano Banana series (Midjourney only 1:1)
**Budget:** 最便宜→Nano Banana2 (4pts) · 最好→Nano Banana Pro (4K) or SeeDream 4.5

## Script Usage

```bash
# Text to image
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key $IMA_API_KEY \
  --task-type text_to_image \
  --model-id doubao-seedream-4.5 \
  --prompt "a cute puppy running on grass" \
  --user-id {user_id} \
  --output-json

# Image to image (accepts URLs and local file paths)
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key $IMA_API_KEY \
  --task-type image_to_image \
  --model-id doubao-seedream-4.5 \
  --prompt "turn into oil painting style" \
  --input-images https://example.com/photo.jpg \
  --user-id {user_id} \
  --output-json

# With aspect ratio (SeeDream 4.5 or Nano Banana)
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key $IMA_API_KEY \
  --task-type text_to_image \
  --model-id doubao-seedream-4.5 \
  --prompt "beautiful landscape" \
  --extra-params '{"aspect_ratio": "16:9"}' \
  --user-id {user_id} \
  --output-json
```

## Sending Results to User

```python
# ✅ CORRECT: Use remote URL directly for inline image display
message(action="send", media=image_url, caption="✅ 图片生成成功！\n• 模型：[Name]\n• 耗时：[X]s\n• 积分：[N pts]\n\n🔗 原始链接：[url]")

# ❌ WRONG: Never download to local file (shows as attachment, not rendered)
```

## UX Protocol (Brief)

1. **Pre-generation:** "🎨 开始生成图片… 模型：[Name]，预计[X~Y]秒，消耗[N]积分"
2. **Progress:** Every 15-30s: "⏳ 正在生成中… [P]%" (cap at 95% until API returns success)
3. **Success:** Send image via `media=image_url` + include link in caption for sharing
4. **Failure:** Natural language error + suggest alternative models. **Never show technical errors to users.** See SKILL-DETAIL.md for full error translation table.

**Never say to users:** script names, API endpoints, attribute_id, technical parameter names. Only: model name · time · credits · result · status.

## Midjourney Limitations

Midjourney has **fixed 1:1 aspect ratio** (1024×1024 only). If user asks for 16:9 etc. with "MJ", recommend SeeDream 4.5 or Nano Banana series instead.

## Environment

Base URL: `https://api.imastudio.com`
Headers: `Authorization: Bearer $IMA_API_KEY` · `x-app-source: ima_skills` · `x_app_language: en`

## Core Flow

1. `GET /open/v1/product/list?app=ima&platform=web&category=<task_type>` → get `attribute_id`, `credit`, `model_version`, `form_config`
2. [image_to_image only] Upload images or pass local paths to script
3. `POST /open/v1/tasks/create` → get `task_id`
4. `POST /open/v1/tasks/detail` → poll every 3-5s until `resource_status==1`

**MANDATORY:** Always query product list first. `attribute_id` is required — if 0 or missing, task fails.

## User Preference Memory

Storage: `~/.openclaw/memory/ima_prefs.json`

- **Save** when user explicitly says "用XXX" / "默认用XXX" / "always use XXX"
- **Clear** when user says "用最好的" / "推荐一个" / "自动选择"
- **Never save** auto-selected or fallback models as preferences

## Model Capabilities


| Model           | Custom Aspect Ratio | Max Resolution | Notes                                            |
| --------------- | ------------------- | -------------- | ------------------------------------------------ |
| SeeDream 4.5    | ✅ (8 ratios)        | 4K             | 1:1, 16:9, 9:16, 4:3, 3:4, 2:3, 3:2, 21:9        |
| Nano Banana2    | ✅ (5 ratios)        | 4K             | 1:1, 16:9, 9:16, 4:3, 3:4; size via attribute_id |
| Nano Banana Pro | ✅ (5 ratios)        | 4K             | 1:1, 16:9, 9:16, 4:3, 3:4; size via attribute_id |
| Midjourney 🎨   | ❌ (1:1 only)        | 1024px         | Fixed square, artistic style focus               |


