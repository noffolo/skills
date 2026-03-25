#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Ensure zip is available (needed by upload-fallback in node runtime)
if ! command -v zip >/dev/null 2>&1; then
    if command -v apt-get >/dev/null 2>&1; then
        apt-get install -y zip >/dev/null 2>&1 || true
    elif command -v yum >/dev/null 2>&1; then
        yum install -y zip >/dev/null 2>&1 || true
    fi
fi

if command -v node >/dev/null 2>&1; then
    node "$SCRIPT_DIR/check.js" "$@"
    exit $?
fi

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$SCRIPT_DIR/check.py" "$@"
else
    echo '{"code":"error","msg":"❌ 错误：未找到 node 或 python3 运行时，请安装其中之一","ts":'"$(date +%s000)"',"data":[]}'
    exit 1
fi
