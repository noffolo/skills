#!/bin/bash
# Copyright (c) 2026 思捷娅科技 (SJYKJ)
# License: MIT
# 入口 wrapper - 加载环境变量

set -euo pipefail

source ~/.openclaw/secrets/gmail.env 2>/dev/null || true
export GMAIL_USER GMAIL_PASS

cd "$(dirname "$0")/.."
python3 scripts/send-email.py "$@"
