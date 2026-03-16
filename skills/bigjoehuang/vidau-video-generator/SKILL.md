---
name: vidau
version: "1.0.0"
license: MIT
description: Use Vidau Open API to generate short videos with Veo3, Sora2, and other models, or query account credits. Register at superaiglobal.com and configure API Key.
homepage: https://vidau.ai
metadata:
  openclaw:
    requires:
      env: ["VIDAU_API_KEY"]
    primaryEnv: "VIDAU_API_KEY"
    homepage: "https://doc.superaiglobal.com/cn/overview/introduction"
compatibility: Python 3.x required; network access to api.superaiglobal.com
---

# Vidau Video Generator 

**Version:** 1.0.0

## When to use

- User asks to "generate a video", "create a short video with Veo3/Sora", "generate video from this prompt/image", "make a clip from this script", etc.
- User asks "how many credits do I have", "check my Vidau balance", "query Vidau credits", etc.
- User asks to "check my video task status", "has my Vidau task finished", "query task by UUID", etc.

## When NOT to use

- User only wants to edit or process existing local video files (e.g. trim, merge, transcode) without calling any cloud API.
- User asks for a different video API (e.g. Runway, Pika) by name; use that provider’s skill if available.
- User has not mentioned Vidau/Veo/Sora/Seedance or "generate video" / "create video" and is only discussing concepts or other tools.

## Reply language

When returning results (video link, credits, or error message) to the user, use the same language as the user’s question (e.g. Simplified Chinese if they asked in Chinese, English if they asked in English).

## Prerequisites

Environment variable `VIDAU_API_KEY` must be set (injected by OpenClaw from `skills.entries.vidau.apiKey` or `env`). If the user has no API key, they must register at [https://www.superaiglobal.com/](https://www.superaiglobal.com/) to get one. Do not trigger this skill if it is not configured.

## Environment check

Before running any script, ensure Python 3 is available:

1. Run `python3 --version` or `python --version`. If either succeeds, use that command when invoking the scripts below.
2. If both fail, try to install Python for the current platform:
   - **macOS**: `brew install python3` (requires Homebrew).
   - **Linux (Debian/Ubuntu)**: `sudo apt-get update && sudo apt-get install -y python3`.
   - **Windows**: `winget install Python.Python.3.12` if available; otherwise tell the user to download and run the installer from [python.org](https://www.python.org/downloads/).
3. If install fails (e.g. no permission or unsupported OS), reply with a short message that Python 3 is required and link to [python.org/downloads](https://www.python.org/downloads/), then stop. Do not run the Vidau scripts until Python is available.

The scripts use only the standard library; no pip packages are required.

## Available scripts

- **`scripts/query_credit.py`** — Query current available credits; no args; outputs JSON with `data.availableCredit`, `data.userId`.
- **`scripts/create_task.py`** — Create video task; required `--prompt`, optional `--model`, etc.; outputs JSON with `data.taskUUID`.
- **`scripts/query_task.py`** — Query task status and result once; required `--task-uuid`; outputs JSON with `taskStatus`, and on success also prints `[VIDAU_VIDEO_URL]` / `[/VIDAU_VIDEO_URL]` and `[VIDAU_THUMB_PATH]` / `[/VIDAU_THUMB_PATH]` blocks containing the raw URLs. When presenting succeeded results to the user, **copy the video and thumbnail URLs verbatim from these blocks** (do not rewrite or shorten). When the task has reached `succeeded` or `failed`, the script prints `[OPENCLAW] DELETE_SCHEDULED_TASK task_uuid=<uuid>` to stderr so the platform can remove the corresponding scheduled poll task.
- **`scripts/wait_task.py`** — Poll until task succeeds or fails (or timeout); required `--task-uuid`; optional `--interval` (default 10s), `--timeout` (default 600s = 10 min). On success outputs same JSON as query_task and the same `[VIDAU_VIDEO_URL]` / `[VIDAU_THUMB_PATH]` blocks. Exit code 0 = succeeded, 1 = failed, 2 = timeout.

## Workflow (generate video)

1. **Optional**: Call `scripts/query_credit.py` to check `availableCredit` before creating a task to avoid failures due to insufficient credits.
2. Call `scripts/create_task.py` with `--prompt` (required), `--resolution` (required), `--model` (default `veo@3:normal`), and optional args (see parameter table below).
3. Read `data.taskUUID` from the script’s stdout JSON.
4. **Option A** (recommended): Call `scripts/wait_task.py --task-uuid <taskUUID>` to poll until done (default: 10s interval, 10 min timeout). **Option B**: Manually poll `scripts/query_task.py --task-uuid <taskUUID>` every 5–10s until `data.taskStatus` is `succeeded` or `failed`; cap total wait at 3–5 minutes.
5. **Success**: Return the video and thumbnail links to the user. **Copy verbatim from the script output blocks**: the video and thumbnail URLs shown to the user must be copied exactly from the content between `[VIDAU_VIDEO_URL]` and `[/VIDAU_VIDEO_URL]`, and between `[VIDAU_THUMB_PATH]` and `[/VIDAU_THUMB_PATH]` in the script stdout—do not rewrite, truncate, or replace; present links in a code block so the user can copy. **Failure**: Explain using the API `message` or error code (e.g. insufficient credits, policy violation).
6. **When task reaches a final state** (succeeded or failed): If a scheduled task was created to poll this taskUUID, cancel/delete that scheduled task so the platform stops re-running the query. `query_task.py` prints `[OPENCLAW] DELETE_SCHEDULED_TASK task_uuid=<uuid>` to stderr on final state for platform integration.

## Workflow (query credits)

When the user asks for balance, call `scripts/query_credit.py` (no args), read `data.availableCredit` from stdout JSON and reply; optionally include `data.userId`.

## Parameters (create_task.py)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--prompt` | Yes | Text description, up to 2000 characters |
| `--model` | No | Default `veo@3:normal`; see model list below |
| `--negative-prompt` | No | Negative prompt, up to 2000 characters |
| `--image-url` | No | First-frame image URL |
| `--last-image-url` | No | Last-frame image URL |
| `--duration` | No | Video duration in seconds |
| `--generate-audio` | No | Whether to generate audio; true/false |
| `--seed` | No | Random seed |
| `--resolution` | Yes | Resolution, e.g. `720p`, `1080p` |
| `--ratio` | No | Aspect ratio, e.g. `16:9`, `9:16` |

Valid values: `resolution` commonly `720p` or `1080p`; `ratio` e.g. `16:9`, `9:16`. See [references/parameters.md](references/parameters.md) for more detail. Run `python scripts/create_task.py --help` for full parameters.

## Model list

Common model IDs (aligned with API):

- **Veo 3**: `veo@3:normal`
- **Veo 3.1**: `veo@3.1:normal`, `veo@3.1:fast`
- **Sora 2**: `sora@2:normal`, `sora@2:pro`
- **Seedance**: `seedance@1:pro`, `seedance@1:pro_fast`
- **Wan 2.5**: `wan@2.5:preview`
- **Vidu Q2**: `vidu@q2:turbo`, `vidu@q2:pro`

See [references/models.md](references/models.md) for more models and use cases.

## Error handling

- If `VIDAU_API_KEY` is not set, scripts exit with an error; tell the user to register at [https://www.superaiglobal.com/](https://www.superaiglobal.com/) to get an API key, then configure it in OpenClaw.
- Common API 400 errors: `CreditInsufficient`, `TaskPromptPolicyViolation`, `ImageDownloadFailure`. Relay the API `message` to the user in the user’s language. See [references/errors.md](references/errors.md) for error codes and suggested user-facing messages.

## Example usage

- **Generate video**: User says e.g. "Generate an 8s video with Veo3 from this script" or "Generate a 10s sunset beach clip with Sora2". Agent: (optional) `query_credit.py` → `create_task.py --prompt "..." --resolution 720p --duration 8 --model veo@3:normal` → read `taskUUID` → `wait_task.py --task-uuid <uuid>` → return video URL from output blocks or explain failure.
- **Query credits**: User says e.g. "How many Vidau credits do I have?" or "Check my Vidau balance". Agent: `query_credit.py` → reply with `data.availableCredit` (and optionally `data.userId`).
- **Check task**: User says e.g. "Is my video task done? UUID is xxx". Agent: `wait_task.py --task-uuid xxx` or `query_task.py --task-uuid xxx` → return status or video link. When the result is succeeded or failed, cancel any scheduled task that was polling this taskUUID.
