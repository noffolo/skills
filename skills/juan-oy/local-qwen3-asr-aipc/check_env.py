#!/usr/bin/env python
"""Check runtime environment and model availability for the ASR skill."""

import json
import os
import string
import subprocess
import sys
from pathlib import Path


def find_state() -> dict | None:
    username = os.environ.get("USERNAME", "user").lower()
    for drive in string.ascii_uppercase:
        state_file = Path(f"{drive}:\\") / f"{username}_openvino" / "asr" / "state.json"
        if state_file.exists():
            return json.loads(state_file.read_text(encoding="utf-8"))
    return None


def model_layout_ready(model_dir: Path) -> bool:
    thinker = model_dir / "thinker"

    def ok(items: list[tuple[Path, float]]) -> bool:
        return all(path.exists() and path.stat().st_size / 1024**2 >= min_mb for path, min_mb in items)

    thinker_layout = [(thinker / name, min_mb) for name, min_mb in [
        ("openvino_thinker_language_model.bin", 800),
        ("openvino_thinker_audio_encoder_model.bin", 50),
        ("openvino_thinker_audio_model.bin", 0.1),
        ("openvino_thinker_embedding_model.bin", 50),
    ]] + [(model_dir / "config.json", 0.001)]

    root_layout = [(model_dir / name, min_mb) for name, min_mb in [
        ("openvino_language_model.bin", 800),
        ("openvino_audio_encoder_model.bin", 50),
        ("config.json", 0.001),
    ]]

    return ok(thinker_layout) or ok(root_layout)


def main() -> int:
    state = find_state()
    if not state:
        print("STATE=MISSING")
        return 1

    venv_py = Path(state["VENV_PY"])
    asr_dir = Path(state["ASR_DIR"])
    model_dir = asr_dir / "Qwen3-ASR-0.6B-fp16-ov"

    result = subprocess.run([str(venv_py), "--version"], capture_output=True, timeout=10)
    if result.returncode != 0:
        print("VENV_PY=BROKEN")
        return 1

    print(f"VENV_PY={venv_py}")
    print(f"ASR_DIR={asr_dir}")

    if model_layout_ready(model_dir):
        total_size_gb = sum(path.stat().st_size for path in model_dir.rglob("*") if path.is_file()) / 1024**3
        print(f"MODEL_STATUS=READY ({total_size_gb:.2f} GB)")
        return 0

    print("MODEL_STATUS=MISSING")
    return 1


if __name__ == "__main__":
    sys.exit(main())