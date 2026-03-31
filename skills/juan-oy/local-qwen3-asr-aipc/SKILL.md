---
name: local-qwen3-asr-aipc
description: >
  Local offline ASR on Windows — no cloud, no API cost, full privacy.
  Qwen3-ASR 0.6B + Intel OpenVINO, GPU-accelerated inference.
  NETWORK: required for first-time setup (install deps + download 2 GB model); NOT required for inference.
  Auto-extracts audio from video files (mp4, mkv, webm, mov, avi) — just pass the video path.
  Also supports audio: mp3, wav, flac, m4a, ogg, aac, wma, opus.
  Single file, batch folder, or watch-mode continuous transcription with automatic txt/json archive.
  30 languages + 22 Chinese dialects, auto language detection.
  One-line LLM API: from asr_api import transcribe_audio
  Local speech to text, transcribe audio, voice recognition, transcribe video, transcribe recording,
  convert speech to text, audio transcription, local ASR, offline speech recognition, dictation on Windows.
  本地离线语音识别，零云端，支持视频音轨自动提取，支持批量转录和文件夹监听，自动保存转写文档。
  网络说明：仅首次安装环境和下载模型时需要网络，推理转录完全离线。
os: windows
requires:
  - python>=3.10
  - git
network:
  setup: required
  inference: offline
user-invocable: true
allowed-tools: Bash(python *), Bash(powershell *), Read, Write, message
---

# Local Speech Recognition (Windows · Qwen3-ASR · OpenVINO)

**Model**: `snake7gun/Qwen3-ASR-0.6B-fp16-ov` (ModelScope FP16)  
**SKILL_VERSION**: 'v1.0.1'

> **First time?** Before using this skill, run these two scripts once in a terminal:
> ```
> python setup.py          # creates venv, installs dependencies (~5 min)
> python download_model.py # downloads the model (~2 GB, resumable)
> ```
> Both scripts are in the skill directory alongside this SKILL.md.

---

## Agent Routing (When To Call acoustic_pipeline.py)

Use `acoustic_pipeline.py` as the default agent entry when any of these are true:

1. Input is a video file (`.mp4`, `.mkv`, `.webm`, `.mov`, `.avi`, etc.)
2. User requests folder watch (`--watch`) or batch transcription (`--batch`)
3. User requests transcript archiving (`--archive txt|json|both`)
4. Environment may be missing and auto-bootstrap is needed (`--auto-bootstrap`)

Use legacy `transcribe.py` direct flow only for simple single-audio-file requests where no watch/batch/archive/bootstrap behavior is needed.

Recommended defaults:

```powershell
python acoustic_pipeline.py --file "<FILE_PATH>" --language auto --archive json --auto-bootstrap
python acoustic_pipeline.py --watch "<DIR_PATH>" --language auto --archive both --auto-bootstrap
python acoustic_pipeline.py --batch "<DIR_PATH>" --language auto --archive json --auto-bootstrap
```

---

## Skill Contract (Input / Output)

### Accepted Inputs

Any agent should treat this skill as a local audio/video transcription skill.

1. Single file path
- Audio: .wav, .mp3, .flac, .m4a, .ogg, .aac, .wma, .opus
- Video: .mp4, .mkv, .webm, .flv, .mov, .avi, .mts, .m2ts, .ts, .m3u8

2. Folder path
- Watch mode: continuously process new files in folder
- Batch mode: process existing files in folder recursively

3. Runtime options
- language: auto or explicit language name
- archive: none | txt | json | both
- archive_dir: optional output folder for transcript files
- auto_bootstrap: initialize ASR automatically when environment is missing

### Output On Success

The result should be returned as a JSON object (or equivalent dictionary) with:

- text: transcription content
- language: detected or requested language
- source_file: original input path
- source_format: source extension
- confidence: optional confidence value (if available)
- archive_files: optional object containing txt/json output paths

Example shape:

```json
{
    "text": "...",
    "language": "Chinese",
    "source_file": "D:\\demo\\meeting.mp4",
    "source_format": ".mp4",
    "confidence": null,
    "archive_files": {
        "json": "D:\\demo\\transcripts\\meeting_20260326_120000.json"
    }
}
```

### Output On Failure

The agent should return a short structured error summary including:

- error: human-readable failure reason
- stage: bootstrap | extract_audio | transcribe | archive
- source_file: input path (if known)
- recoverable: true if retry is reasonable

---

## ⚠️ Agent instructions

1. **Windows / PowerShell only.** Never use Linux commands (`ls`, `rm`, `cat`). Never use `&&` or `call`.
2. **Every step reads `state.json` itself** — do not pass paths between steps manually.
3. **Use `VENV_PY` from state.json for inference calls** — never use system python for inference. Exception: `check_env.py` uses only standard library and can be run with system python.
4. `transcribe.py` is automatically deployed to `ASR_DIR` when `setup.py` runs. If it is missing, re-run `setup.py`.
5. **If `transcribe.py` fails at runtime**, do NOT edit it manually. Re-run `setup.py` to redeploy the original from the repository.
6. **Never diagnose "model issues" without running Step 1's check script first.** The model layout may use a `thinker/` subdirectory — the scripts handle this automatically.
7. **Do not generate helper scripts in agent workspace directories.** Use repository-managed `check_env.py` instead.
8. **Goal**: transcribe the audio file and send the result to the conversation.

**Auto-recovery policy — try before asking user:**
⚠️ Network handling (proxy-aware)

When running setup.py or download_model.py:
1. Try to read system proxy settings:
   - Environment variables: HTTP_PROXY / HTTPS_PROXY
   - Windows WinHTTP proxy (netsh winhttp show proxy)
2. If proxy is detected:
   - Automatically apply it
   - Continue installation / download
3. If no proxy is detected:
   - Continue normally (direct connection)
4. If download/setup fails:
   - Inform the user whether a proxy was detected
   - If no proxy was detected, suggest configuring one
   - Then retry
IMPORTANT:
- Many networks (corporate / China mainland / campus) require proxy
- Download supports resume — safe to retry after fixing network

- If `STATE=MISSING` or `VENV_PY=BROKEN`: automatically run `setup.py` (up to 3 attempts). Only ask user to run it manually if all 3 attempts fail.
- If `MODEL_STATUS=MISSING`: automatically run `download_model.py` (up to 3 attempts). Only ask user to run it manually if all 3 attempts fail or if a single attempt runs longer than 8 minutes without completing (likely a slow connection — download_model.py supports resume so partial progress is not lost).
- Always announce what you are doing before each attempt: "⚙️ 正在自动安装环境（第 N/3 次尝试）…"

**Pipeline — follow exactly in order, no skipping:**
```
Step 0: parse request       → AUDIO_PATH, LANGUAGE, TOPIC
Step 1: verify environment  → run check_env.py → VENV_PY, ASR_DIR confirmed ready
         ↳ if STATE=MISSING or VENV_BROKEN: auto-run setup.py (3 attempts)
         ↳ if MODEL_STATUS=MISSING: auto-run download_model.py (3 attempts)
Step 2: transcribe + send   → prefer acoustic_pipeline.py; fallback to runtime transcribe.py
         (transcribe.py is auto-deployed by setup.py — no separate agent step needed)
```

---

## Step 0: parse request (LLM only — no tools)

Extract from the user's message:

| Field | Default | Notes |
|-------|---------|-------|
| `AUDIO_PATH` | required | Absolute path to audio/video file (wav/mp3/flac/m4a/ogg/aac/wma/opus/mp4/mkv/webm/flv/mov/avi/mts/m2ts/ts/m3u8) |
| `LANGUAGE` | auto-detect | Optional: `Chinese`, `English`, `Japanese`, etc. |
| `TOPIC` | English snake_case from context | Used for output filename |

If no audio file provided, ask the user before continuing.

---

## Step 1: verify environment and model

> 🔍 Step 1/3: checking environment and model…

```powershell
python "<skill_dir>\check_env.py"
```

**On success**: record `VENV_PY` and `ASR_DIR` from output, proceed to Step 2.

**On failure — auto-recovery (try before asking user):**

### If STATE=MISSING or VENV_PY=BROKEN → auto-run setup.py

Announce and run (up to 3 attempts):
```
⚙️ 环境未初始化，正在自动安装（第 1/3 次尝试）…
```
```powershell
python "<skill_dir>\setup.py"
```

After each attempt, re-run `check_env.py` to verify. If all 3 attempts fail, show manual fallback below.

### If MODEL_STATUS=MISSING → auto-run download_model.py

Announce and run (up to 3 attempts, stop if a single attempt exceeds 8 minutes):
```
📥 模型未找到，正在自动下载（第 1/3 次尝试）…
   预计耗时：100Mbps 约 3 分钟 · 50Mbps 约 5 分钟
   下载支持断点续传，中断后重新运行可继续。
```
```powershell
python "<skill_dir>\download_model.py"
```

After each attempt, re-run `check_env.py` to verify. If all 3 attempts fail, show manual fallback below.

### Manual fallback (only if all 3 auto-attempts fail)

Show user this message:
```
⚠️ 自动安装失败，需要手动操作。

请打开 Windows 终端（PowerShell 或命令提示符），依次运行：

① 安装环境（如果还未安装）：
   python "<skill_dir>\setup.py"
   预计耗时约 5 分钟，全程自动完成。

② 下载模型（约 2 GB）：
   python "<skill_dir>\download_model.py"
   下载支持断点续传，中断后重新运行可继续。
   预计耗时：100 Mbps → 约 3 分钟 · 50 Mbps → 约 5 分钟

完成后回到这里重新发送请求。
```

---

## Step 2: transcribe and send result

> 🎤 Step 2/2: transcribing…

**Preferred path** — use `acoustic_pipeline.py` for all standard requests:

```powershell
python "<skill_dir>\acoustic_pipeline.py" --file "AUDIO_PATH" --language auto --archive json --auto-bootstrap
```

If the user specified a language:

```powershell
python "<skill_dir>\acoustic_pipeline.py" --file "AUDIO_PATH" --language "LANGUAGE" --archive json --auto-bootstrap
```

Return the JSON result directly to the conversation and include any `archive_files` paths.

**Fallback** — only when direct low-level runtime behavior is explicitly required:

```powershell
$env:PYTHONUTF8 = "1"
& "<VENV_PY>" "<ASR_DIR>\transcribe.py" --audio "AUDIO_PATH" --language "LANGUAGE" --topic "TOPIC"
```

**Pass**: stdout contains `[SUCCESS]` and `[RESULT]`. Record:
- `OUTPUT_PATH` — path from `[SUCCESS]` line
- `TRANSCRIPT` — text after `[RESULT]`
- `LANG` — language from `[INFO]` line

Send via `message` tool:
```
action: "send"  filePath: "OUTPUT_PATH"  message: "✅ TOPIC | LANG\n\nTRANSCRIPT"
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `STATE=MISSING` | Run `python "<skill_dir>\setup.py"` |
| `VENV_PY=BROKEN` | Re-run `python "<skill_dir>\setup.py"` — it will rebuild the venv |
| `MODEL_STATUS=MISSING` | Run `python "<skill_dir>\download_model.py"` |
| `[ERROR] Audio not found` | Verify the file path is correct and the file exists |
| `[ERROR] Model incomplete` | Re-run `python "<skill_dir>\download_model.py"` — supports resume |
| `[ERROR] state.json not found` | Re-run Step 1 (`check_env.py`) |
| `RuntimeError` on GPU | Run `check_env.py` first to confirm model is READY. If model is OK, try adding `--language auto` to remove language mismatch. If still failing, re-run `setup.py` to upgrade OpenVINO and redeploy runtime files. |

---

## LLM API Usage

For agents that prefer a Python import interface over shell commands:

```python
from asr_api import transcribe_audio

# Basic usage — auto language detection
result = transcribe_audio("C:\\meeting.mp4")
print(result["text"])

# With options
result = transcribe_audio(
    file_path="C:\\lecture.mp4",
    language="Chinese",
    archive_mode="json",       # save transcript to file
    auto_bootstrap=True,       # auto-install env if missing
)
print(result["text"])
print(result.get("archive_files"))  # path to saved json
```

`asr_api.py` is in the skill directory and wraps `acoustic_pipeline.py` internally.

---

## Workspace Hygiene

- Do not generate helper scripts in agent workspace directories (e.g. `.openclaw\workspace\check_asr_env.ps1`).
- Use repository-managed `check_env.py` — it is versioned, auditable, and repeatable.
- If the execution environment forces a temporary file, treat it as disposable and remove it after the command completes.

