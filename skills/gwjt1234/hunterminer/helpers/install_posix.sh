#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BASE_DIR"
PYTHON_BIN="${PYTHON_BIN:-python3}"
$PYTHON_BIN -m pip install -r requirements.txt
mkdir -p "$HOME/.openclaw/skills"
TARGET="$HOME/.openclaw/skills/hunterminer"
rm -rf "$TARGET"
cp -R "$BASE_DIR" "$TARGET"
echo "Installed to $TARGET"
