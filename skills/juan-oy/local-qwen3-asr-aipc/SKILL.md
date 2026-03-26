---
name: local-qwen3-asr-aipc
description: >
  speech to text, transcribe audio, voice recognition, ASR, speech recognition,
  transcribe recording, convert speech to text, recognize speech, transcribe file,
  audio transcription, local ASR, offline speech recognition, dictation.
  语音识别、转录音频、语音转文字、识别录音、转写、会议录音转文字。
  Runs Qwen3-ASR-0.6B on-device on Windows via Intel OpenVINO.
  Supports 30 languages and 22 Chinese dialects. Accepts WAV, MP3, FLAC.
  Prioritizes Intel iGPU (Xe / Arc), falls back to CPU. INFERENCE is fully offline.
  Requires one-time setup: run setup.py then download_model.py from the skill directory.
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
**SKILL_VERSION**: 'v1.0.0'

> **First time?** Before using this skill, run these two scripts once in a terminal:
> ```
> python setup.py          # creates venv, installs dependencies (~5 min)
> python download_model.py # downloads the model (~2 GB, resumable)
> ```
> Both scripts are in the skill directory alongside this SKILL.md.

---

## ⚠️ Agent instructions

1. **Windows / PowerShell only.** Never use Linux commands (`ls`, `rm`, `cat`). Never use `&&` or `call`.
2. **Every step reads `state.json` itself** — do not pass paths between steps manually.
3. **Use `VENV_PY` from state.json for all python calls** — never use system python for inference.
4. **CRITICAL — Never skip Step 2.** Always run the version check python script to write `transcribe.py`. Never use the Write tool to create or modify `transcribe.py` — a manually written script will be incomplete and will fail.
5. **CRITICAL — If transcribe.py fails**, do NOT rewrite it manually. Delete it and re-run Step 2's python script to regenerate the correct version.
6. **Never diagnose "model issues" without running Step 1's check script first.** The model layout may use a `thinker/` subdirectory — the scripts handle this automatically.
7. **Goal**: transcribe the audio file and send the result to the conversation.

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
Step 1: verify environment  → VENV_PY, ASR_DIR confirmed ready
         ↳ if STATE=MISSING or VENV_BROKEN: auto-run setup.py (3 attempts)
         ↳ if MODEL_STATUS=MISSING: auto-run download_model.py (3 attempts)
Step 2: write transcribe.py → SCRIPT_UPDATE=DONE/SKIPPED  ← NEVER skip this
Step 3: transcribe + send   → [SUCCESS] + [RESULT]
```

---

## Step 0: parse request (LLM only — no tools)

Extract from the user's message:

| Field | Default | Notes |
|-------|---------|-------|
| `AUDIO_PATH` | required | Absolute path to audio file (WAV / MP3 / FLAC) |
| `LANGUAGE` | auto-detect | Optional: `Chinese`, `English`, `Japanese`, etc. |
| `TOPIC` | English snake_case from context | Used for output filename |

If no audio file provided, ask the user before continuing.

---

## Step 1: verify environment and model

> 🔍 Step 1/3: checking environment and model…

```python
python -c "
import json, os, string, subprocess
from pathlib import Path

# Find state.json
state = None
for d in string.ascii_uppercase:
    sf = Path(f'{d}:\\\\') / f'{os.environ.get(\"USERNAME\",\"user\").lower()}_openvino' / 'asr' / 'state.json'
    if sf.exists():
        state = json.loads(sf.read_text(encoding='utf-8'))
        break

if not state:
    print('STATE=MISSING')
    exit(1)

venv_py   = Path(state['VENV_PY'])
asr_dir   = Path(state['ASR_DIR'])
model_dir = asr_dir / 'Qwen3-ASR-0.6B-fp16-ov'
thinker   = model_dir / 'thinker'

# Verify venv python is runnable
r = subprocess.run([str(venv_py), '--version'], capture_output=True, timeout=10)
if r.returncode != 0:
    print('VENV_PY=BROKEN')
    exit(1)

print(f'VENV_PY={venv_py}')
print(f'ASR_DIR={asr_dir}')

# Check model integrity (supports both root and thinker/ layouts)
def ok(lst):
    return all(p.exists() and p.stat().st_size / 1024**2 >= mb for p, mb in lst)

layout_thinker = [(thinker / f, mb) for f, mb in [
    ('openvino_thinker_language_model.bin',      800),
    ('openvino_thinker_audio_encoder_model.bin',  50),
    ('openvino_thinker_audio_model.bin',           0.1),
    ('openvino_thinker_embedding_model.bin',       50),
]] + [(model_dir / 'config.json', 0.001)]

layout_root = [(model_dir / f, mb) for f, mb in [
    ('openvino_language_model.bin',      800),
    ('openvino_audio_encoder_model.bin',  50),
    ('config.json',                       0.001),
]]

if ok(layout_thinker) or ok(layout_root):
    total = sum(f.stat().st_size for f in model_dir.rglob('*') if f.is_file()) / 1024**3
    print(f'MODEL_STATUS=READY  ({total:.2f} GB)')
else:
    print('MODEL_STATUS=MISSING')
    exit(1)
"
```

**On success**: record `VENV_PY` and `ASR_DIR` from output, proceed to Step 2.

**On failure — auto-recovery (try before asking user):**

### If STATE=MISSING or VENV_PY=BROKEN → auto-run setup.py

First find the script path:
```python
python -c "
import os, string
from pathlib import Path
skill_dir = Path(r'{baseDir}')
p = skill_dir / 'setup.py'
print(f'SETUP_PY={p}') if p.exists() else print('SETUP_PY=NOT_FOUND')
"
```

Then announce and run (up to 3 attempts):
```
⚙️ 环境未初始化，正在自动安装（第 1/3 次尝试）…
```
```powershell
python "<SETUP_PY path>"
```

After each attempt, re-run Step 1's check script to verify. If all 3 attempts fail, show manual fallback below.

### If MODEL_STATUS=MISSING → auto-run download_model.py

First find the script path:
```python
python -c "
import os, string
from pathlib import Path
skill_dir = Path(r'{baseDir}')
p = skill_dir / 'download_model.py'
print(f'DOWNLOAD_PY={p}') if p.exists() else print('DOWNLOAD_PY=NOT_FOUND')
"
```

Then announce and run (up to 3 attempts, stop if a single attempt exceeds 8 minutes):
```
📥 模型未找到，正在自动下载（第 1/3 次尝试）…
   预计耗时：100Mbps 约 3 分钟 · 50Mbps 约 5 分钟
   下载支持断点续传，中断后重新运行可继续。
```
```powershell
python "<DOWNLOAD_PY path>"
```

After each attempt, re-run Step 1's check script to verify. If all 3 attempts fail, show manual fallback below.

### Manual fallback (only if all 3 auto-attempts fail)

```python
python -c "
import os, string
from pathlib import Path
skill_dir = Path(r'{baseDir}')
for script in ['setup.py', 'download_model.py']:
    p = skill_dir / script
    if p.exists(): print(f'{script}={p}')
"
```

Show user this message with the actual paths filled in:
```
⚠️ 自动安装失败，需要手动操作。

请打开 Windows 终端（PowerShell 或命令提示符），依次运行：

① 安装环境（如果还未安装）：
   python "<SETUP_PY 的完整路径>"
   预计耗时约 5 分钟，全程自动完成。

② 下载模型（约 2 GB）：
   python "<DOWNLOAD_PY 的完整路径>"
   下载支持断点续传，中断后重新运行可继续。
   预计耗时：100 Mbps → 约 3 分钟 · 50 Mbps → 约 5 分钟

完成后回到这里重新发送请求。
```

---

## Step 2: write transcribe.py

> ✍️ Step 2/3: writing inference script…

```python
python -c "
import json, os, string, re
from pathlib import Path

state = None
for d in string.ascii_uppercase:
    sf = Path(f'{d}:\\\\') / f'{os.environ.get(\"USERNAME\",\"user\").lower()}_openvino' / 'asr' / 'state.json'
    if sf.exists():
        state = json.loads(sf.read_text(encoding='utf-8'))
        break

if not state:
    print('[ERROR] state.json not found — re-run Step 1')
    exit(1)

asr_dir = Path(state['ASR_DIR'])
CURRENT_VERSION = 'v2.0'
script = asr_dir / 'transcribe.py'

existing = None
if script.exists():
    m = re.search(r\"SKILL_VERSION\s*=\s*[\\\"'](.*?)[\\\"']\", script.read_text(encoding='utf-8', errors='ignore'))
    if m: existing = m.group(1)

if existing == CURRENT_VERSION:
    print('SCRIPT_UPDATE=SKIPPED')
else:
    code = r\'\'\'
SKILL_VERSION = \"v2.0\"
import sys, io, os, json, string, argparse, re
from datetime import datetime
from pathlib import Path

def get_state():
    for d in string.ascii_uppercase:
        sf = Path(f\"{d}:\\\\\") / f\"{os.environ.get('USERNAME','user').lower()}_openvino\" / \"asr\" / \"state.json\"
        if sf.exists():
            return json.loads(sf.read_text(encoding='utf-8'))
    return None

def get_device():
    import openvino as ov
    core = ov.Core()
    devs = core.available_devices
    print(f\"[INFO] Devices: {devs}\")
    for d in devs:
        if \"GPU\" in d:
            print(f\"[INFO] Using {d}\")
            return d
    print(\"[INFO] Using CPU\")
    return \"CPU\"

def transcribe(audio_path, language=None, topic='', output_path=None):
    state = get_state()
    if not state:
        print(\"[ERROR] state.json not found — run setup.py\")
        sys.exit(1)

    asr_dir   = Path(state['ASR_DIR'])
    sys.path.insert(0, str(asr_dir))
    out_dir   = asr_dir / \"outputs\"
    out_dir.mkdir(parents=True, exist_ok=True)

    model_dir = asr_dir / \"Qwen3-ASR-0.6B-fp16-ov\"
    thinker   = model_dir / \"thinker\"

    def ok(lst):
        return all(p.exists() and p.stat().st_size / 1024**2 >= mb for p, mb in lst)

    layout_thinker = [(thinker/f, mb) for f, mb in [
        ('openvino_thinker_language_model.bin',      800),
        ('openvino_thinker_audio_encoder_model.bin',  50),
        ('openvino_thinker_audio_model.bin',           0.1),
        ('openvino_thinker_embedding_model.bin',       50),
    ]] + [(model_dir/'config.json', 0.001)]

    layout_root = [(model_dir/f, mb) for f, mb in [
        ('openvino_language_model.bin',      800),
        ('openvino_audio_encoder_model.bin',  50),
        ('config.json',                       0.001),
    ]]

    if not ok(layout_thinker) and not ok(layout_root):
        print(\"[ERROR] Model incomplete — run download_model.py\")
        sys.exit(1)

    if not Path(audio_path).exists():
        print(f\"[ERROR] Audio not found: {audio_path}\")
        sys.exit(1)

    device = get_device()
    print(f\"[INFO] Loading model: {model_dir}\")

    from asr_engine import OVQwen3ASRModel
    model = OVQwen3ASRModel.from_pretrained(str(model_dir), device=device)

    import time
    t0 = time.time()
    results = model.transcribe(audio=audio_path, language=language)
    elapsed = time.time() - t0

    if not results:
        print(\"[ERROR] Empty transcription result\")
        sys.exit(1)

    text = results[0].text
    lang = results[0].language
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe = re.sub(r'[^\\w]', '_', (topic or 'asr').strip())[:30].strip('_')
    if output_path is None:
        output_path = str(out_dir / f\"{date_str}_{safe}.txt\")

    Path(output_path).write_text(
        f\"Language: {lang}\\nTime: {elapsed:.2f}s\\n\\n{text}\\n\",
        encoding='utf-8'
    )
    print(f\"[SUCCESS] {output_path}\")
    print(f\"[INFO] Language: {lang} | Time: {elapsed:.2f}s\")
    print(f\"[RESULT] {text}\")
    return output_path

if __name__ == \"__main__\":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    try:
        p = argparse.ArgumentParser()
        p.add_argument(\"--audio\",    required=True)
        p.add_argument(\"--language\", default=None)
        p.add_argument(\"--topic\",    default='')
        p.add_argument(\"--output\",   default=None)
        args = p.parse_args()
        lang = None if args.language in (None, '', 'None', 'none', 'null') else args.language
        print(transcribe(args.audio, lang, args.topic, args.output))
        sys.stdout.flush()
    except Exception as e:
        import traceback
        print(f\"[FATAL] {type(e).__name__}: {e}\", flush=True)
        traceback.print_exc()
        sys.exit(1)
\'\'\'
    script.write_text(code.strip(), encoding='utf-8')
    print('SCRIPT_UPDATE=DONE')

print(f'EXISTS={script.exists()}')
"
```

| Output | Action |
|--------|--------|
| `SCRIPT_UPDATE=SKIPPED` | ✅ Already up to date, proceed to Step 3 |
| `SCRIPT_UPDATE=DONE` | ✅ Script written, proceed to Step 3 |
| `EXISTS=False` | ⛔ Write failed — check directory permissions on `ASR_DIR` |

---

## Step 3: transcribe and send result

> 🎤 Step 3/3: transcribing…

Run these two commands separately:

```powershell
$env:PYTHONUTF8 = "1"
```

**With language hint:**
```powershell
& "<VENV_PY>" "<ASR_DIR>\transcribe.py" --audio "AUDIO_PATH" --language "LANGUAGE" --topic "TOPIC"
```

**Auto-detect (no language hint):**
```powershell
& "<VENV_PY>" "<ASR_DIR>\transcribe.py" --audio "AUDIO_PATH" --topic "TOPIC"
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
| `STATE=MISSING` | Run `python setup.py` from the skill directory |
| `VENV_PY=BROKEN` | Re-run `python setup.py` — it will rebuild the venv automatically |
| `MODEL_STATUS=MISSING` | Run `python download_model.py` from the skill directory in a terminal |
| `[ERROR] Audio not found` | Verify the file path is correct and the file exists |
| `[ERROR] Model incomplete` | Re-run `python download_model.py` — it will resume automatically |
| `[ERROR] state.json not found` | Re-run Step 1 |
| `RuntimeError` on GPU | Edit `transcribe.py` — change `get_device()` to always `return "CPU"` |
