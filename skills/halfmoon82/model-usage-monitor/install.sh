#!/usr/bin/env bash
# OpenClaw Skill — 受保护版本（oc-pay-sdk 加密分发）
# Skill ID: model-usage-monitor
# 核心内容已加密存储于服务端，需授权后在内存中解密执行

SDK_PATH="${OC_PAY_SDK:-$HOME/.openclaw/workspace/.lib/oc-pay-sdk/auth.sh}"
if [ ! -f "$SDK_PATH" ]; then
  echo "❌ oc-pay-sdk 未找到：$SDK_PATH"
  exit 1
fi
source "$SDK_PATH"

IDENTIFIER="${OC_IDENTIFIER:-$(id -u -n 2>/dev/null || echo 'user')@$(hostname -s 2>/dev/null || echo 'host')}"
DRY_RUN="${1:-}"

oc_require_license "model-usage-monitor" "$IDENTIFIER" "$DRY_RUN" || exit 1
oc_execute_skill "model-usage-monitor"
