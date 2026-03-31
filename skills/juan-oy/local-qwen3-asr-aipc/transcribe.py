SKILL_VERSION = "v1.1.0"
import sys, io, os, json, string, argparse, re
from datetime import datetime
from pathlib import Path


def get_state():
    for d in string.ascii_uppercase:
        sf = Path(f"{d}:\\") / f"{os.environ.get('USERNAME', 'user').lower()}_openvino" / "asr" / "state.json"
        if sf.exists():
            return json.loads(sf.read_text(encoding='utf-8'))
    return None


def get_device():
    import openvino as ov
    core = ov.Core()
    devs = core.available_devices
    print(f"[INFO] Devices: {devs}")
    for d in devs:
        if "GPU" in d:
            print(f"[INFO] Using {d}")
            return d
    print("[INFO] Using CPU")
    return "CPU"


def transcribe(audio_path, language=None, topic='', output_path=None):
    state = get_state()
    if not state:
        print("[ERROR] state.json not found — run setup.py")
        sys.exit(1)

    asr_dir = Path(state['ASR_DIR'])
    sys.path.insert(0, str(asr_dir))
    out_dir = asr_dir / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    model_dir = asr_dir / "Qwen3-ASR-0.6B-fp16-ov"
    thinker = model_dir / "thinker"

    def ok(items):
        return all(path.exists() and path.stat().st_size / 1024**2 >= min_mb for path, min_mb in items)

    thinker_layout = [(thinker / name, min_mb) for name, min_mb in [
        ('openvino_thinker_language_model.bin', 800),
        ('openvino_thinker_audio_encoder_model.bin', 50),
        ('openvino_thinker_audio_model.bin', 0.1),
        ('openvino_thinker_embedding_model.bin', 50),
    ]] + [(model_dir / 'config.json', 0.001)]

    root_layout = [(model_dir / name, min_mb) for name, min_mb in [
        ('openvino_language_model.bin', 800),
        ('openvino_audio_encoder_model.bin', 50),
        ('config.json', 0.001),
    ]]

    if not ok(thinker_layout) and not ok(root_layout):
        print("[ERROR] Model incomplete — run download_model.py")
        sys.exit(1)

    if not Path(audio_path).exists():
        print(f"[ERROR] Audio not found: {audio_path}")
        sys.exit(1)

    device = get_device()
    print(f"[INFO] Loading model: {model_dir}")

    from asr_engine import OVQwen3ASRModel
    model = OVQwen3ASRModel.from_pretrained(str(model_dir), device=device)

    import time
    t0 = time.time()
    results = model.transcribe(audio=audio_path, language=language)
    elapsed = time.time() - t0

    if not results:
        print("[ERROR] Empty transcription result")
        sys.exit(1)

    text = results[0].text
    lang = results[0].language
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe = re.sub(r'[^\w]', '_', (topic or 'asr').strip())[:30].strip('_')
    if output_path is None:
        output_path = str(out_dir / f"{date_str}_{safe}.txt")

    Path(output_path).write_text(
        f"Language: {lang}\nTime: {elapsed:.2f}s\n\n{text}\n",
        encoding='utf-8'
    )
    print(f"[SUCCESS] {output_path}")
    print(f"[INFO] Language: {lang} | Time: {elapsed:.2f}s")
    print(f"[RESULT] {text}")
    return output_path


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--audio", required=True)
        parser.add_argument("--language", default=None)
        parser.add_argument("--topic", default='')
        parser.add_argument("--output", default=None)
        args = parser.parse_args()
        language = None if args.language in (None, '', 'None', 'none', 'null') else args.language
        print(transcribe(args.audio, language, args.topic, args.output))
        sys.stdout.flush()
    except Exception as exc:
        import traceback
        print(f"[FATAL] {type(exc).__name__}: {exc}", flush=True)
        traceback.print_exc()
        sys.exit(1)
