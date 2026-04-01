---
name: chenyu-aigc
description: >
  Generate AI videos and images via Chenyu Studio AIGC API.
  Supports text-to-video, image-to-video, video extension, style transfer, and AI image generation.
  Trigger when: generate video, create AI video, text to video, image to video,
  AI image generation, video generation, 生成视频, AI视频, 文生视频, 图生视频, 生成图片.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - CHENYU_API_KEY
        - CHENYU_BASE_URL
      bins:
        - curl
    primaryEnv: CHENYU_API_KEY
    emoji: "\U0001F3AC"
    os:
      - darwin
      - linux
---

# Chenyu AIGC - AI Video & Image Generation

Generate videos and images using AI models through the Chenyu Studio AIGC orchestration API.

## When to Use

- User wants to generate a video from text prompt
- User wants to generate a video from an image (first/last frame)
- User wants to extend or remix a video
- User wants to generate AI images
- User wants to check status of a generation task
- User wants to list available AI models

## When NOT to Use

- User wants to analyze or understand existing videos (use video-analysis skill)
- User wants to download videos from social platforms (use video-fetch skill)
- User wants to manage digital humans or clone voices (use chenyu-core skill)

## Authentication

All requests use API Key authentication:

```
Authorization: Bearer $CHENYU_API_KEY
```

Base URL: `$CHENYU_BASE_URL` (default: `https://chenyu.pro`)

## Core Workflow

The typical workflow is: **discover recipes -> get schema -> execute -> poll status -> get output**.

### 1. List Available Recipes (AI Models)

```bash
curl -s "$CHENYU_BASE_URL/api/v1/aigc/recipes" \
  -H "Authorization: Bearer $CHENYU_API_KEY" | jq '.data[] | {recipe_id, name, slug, description, output_type, status}'
```

Each recipe represents an AI model capability (e.g. text-to-video, image generation).
Key fields in the response:
- `recipe_id` - Use this ID when executing
- `slug` - Human-readable identifier (e.g. `volcengine-seedance-v1-pro`)
- `output_type` - What it produces: `video`, `image`, `audio`
- `typed_inputs_schema` - What inputs the model accepts
- `parameters_schema` - Tunable parameters (duration, ratio, etc.)

### 2. Get Recipe Schema

Before executing, check what inputs and parameters a recipe needs:

```bash
curl -s "$CHENYU_BASE_URL/api/v1/aigc/recipes/{recipe_id}/schema" \
  -H "Authorization: Bearer $CHENYU_API_KEY" | jq '.data'
```

The schema tells you:
- `typed_inputs_schema.definitions` - What input types are accepted and their fields
- `parameters_schema` - Available parameters with constraints (min/max/enum)
- `credit_cost` / `credit_cost_rules` - How many credits it costs

### 3. Execute a Recipe

Submit a generation task:

```bash
curl -s -X POST "$CHENYU_BASE_URL/api/v1/aigc/recipes/{recipe_id}/execute" \
  -H "Authorization: Bearer $CHENYU_API_KEY" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [...],
    "parameters": {...}
  }'
```

**Required headers:**
- `Authorization: Bearer $CHENYU_API_KEY`
- `Idempotency-Key` - Unique key per request (prevents duplicate submissions, 24h TTL)
- `Content-Type: application/json`

**Request body:**

```json
{
  "inputs": [
    {
      "type": "text",
      "text": { "prompt": "A cat running through sunlit grass", "role": "prompt" }
    }
  ],
  "parameters": {
    "duration": 5,
    "ratio": "16:9"
  }
}
```

**Input types and their fields:**

| type | payload field | key fields |
|------|--------------|------------|
| `text` | `text` | `prompt` (string, required), `role` (`prompt` or `negative_prompt`) |
| `image` | `image` | `uri` (string, required), `role` (`first_frame`, `last_frame`, `reference_image`) |
| `video` | `video` | `uri` (string, required), `role` (`source`, `extend`, `pose`) |
| `audio` | `audio` | `uri` (string, required), `role` (`background_music`, `speech`, `sound_effect`) |
| `reference` | `reference` | `uri` (string, required), `kind` (`style`, `element`), `weight` (0.0-1.0) |

**URI formats supported:** HTTPS URLs, data URIs (`data:image/jpeg;base64,...`), or S3 Asset IDs (26-char ULID).

**Response:**

```json
{
  "code": 200,
  "data": {
    "task_id": "01HXY...",
    "status": "queued",
    "created_at": "2026-03-07T10:30:00Z"
  }
}
```

### 4. Poll Task Status

```bash
curl -s "$CHENYU_BASE_URL/api/v1/aigc/executions/{task_id}" \
  -H "Authorization: Bearer $CHENYU_API_KEY" | jq '.data | {status, progress, progress_message, outputs, error}'
```

**Task statuses:** `queued` -> `running` -> `succeeded` / `failed` / `canceled` / `expired`

When `status` is `succeeded`, the `outputs` field contains the result (e.g. `video_url`, `image_url`).
When `status` is `failed`, check `error.code` and `error.message`.

**Polling strategy:** Wait 3-5 seconds between polls. Most video tasks complete in 30-120 seconds.

### 5. Cancel a Task

```bash
curl -s -X POST "$CHENYU_BASE_URL/api/v1/aigc/executions/{task_id}/cancel" \
  -H "Authorization: Bearer $CHENYU_API_KEY"
```

Only `queued` or `running` tasks can be canceled.

### 6. List Tasks

```bash
curl -s "$CHENYU_BASE_URL/api/v1/aigc/executions?status=running&page=1&page_size=10" \
  -H "Authorization: Bearer $CHENYU_API_KEY"
```

Query parameters: `status`, `recipe_slug`, `page`, `page_size` (max 100).

### 7. Delete a Completed Task

```bash
curl -s -X DELETE "$CHENYU_BASE_URL/api/v1/aigc/executions/{task_id}" \
  -H "Authorization: Bearer $CHENYU_API_KEY"
```

Only terminal-state tasks (`succeeded`, `failed`, `canceled`, `expired`) can be deleted.

## Common Examples

### Text-to-Video

```bash
curl -s -X POST "$CHENYU_BASE_URL/api/v1/aigc/recipes/{recipe_id}/execute" \
  -H "Authorization: Bearer $CHENYU_API_KEY" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {"type": "text", "text": {"prompt": "A golden retriever playing in snow, cinematic lighting"}}
    ],
    "parameters": {"duration": 5, "ratio": "16:9"}
  }'
```

### Image-to-Video (First Frame)

```bash
curl -s -X POST "$CHENYU_BASE_URL/api/v1/aigc/recipes/{recipe_id}/execute" \
  -H "Authorization: Bearer $CHENYU_API_KEY" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {"type": "text", "text": {"prompt": "Camera slowly zooms in"}},
      {"type": "image", "image": {"uri": "https://example.com/photo.jpg", "role": "first_frame"}}
    ],
    "parameters": {"duration": 5}
  }'
```

### Image-to-Video (First + Last Frame)

```bash
curl -s -X POST "$CHENYU_BASE_URL/api/v1/aigc/recipes/{recipe_id}/execute" \
  -H "Authorization: Bearer $CHENYU_API_KEY" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {"type": "text", "text": {"prompt": "Smooth transition between two scenes"}},
      {"type": "image", "image": {"uri": "https://example.com/start.jpg", "role": "first_frame"}},
      {"type": "image", "image": {"uri": "https://example.com/end.jpg", "role": "last_frame"}}
    ],
    "parameters": {"duration": 5}
  }'
```

### Style Transfer with Reference

```bash
curl -s -X POST "$CHENYU_BASE_URL/api/v1/aigc/recipes/{recipe_id}/execute" \
  -H "Authorization: Bearer $CHENYU_API_KEY" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {"type": "text", "text": {"prompt": "A city street at sunset"}},
      {"type": "reference", "reference": {"uri": "https://example.com/style.jpg", "kind": "style", "weight": 0.8}}
    ],
    "parameters": {"duration": 5}
  }'
```

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 400 | Invalid inputs or parameters | Check request body against recipe schema |
| 402 | Insufficient credits | Top up account balance |
| 404 | Recipe or task not found | Verify the ID |
| 409 | Idempotency conflict | Use a different Idempotency-Key |

Task-level error codes (in `error.code` field):
- `MODEL_ERROR` - AI model failed, retry with different inputs
- `TASK_TIMEOUT` - Task exceeded timeout, retry
- `QUEUE_EXPIRED` - Task expired in queue before processing
