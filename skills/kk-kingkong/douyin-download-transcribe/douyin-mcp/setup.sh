#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_ROOT="${CLAWHUB_WORKDIR:-$HOME/.openclaw/workspace}"

echo "=== 抖音视频解析 MCP 服务器安装 ==="

# 1. 安装 Python 依赖
echo "[1/3] 安装 Python 依赖..."
cd "$SCRIPT_DIR"
python3 -m venv .venv
source .venv/bin/activate

# 确保 pip 可用
python3 -m ensurepip --upgrade 2>/dev/null || true
python3 -m pip install --upgrade pip -q

# 安装依赖
pip install -r requirements.txt -q

# 2. 安装 ffmpeg（macOS）
if command -v brew &> /dev/null; then
    echo "[2/3] 安装 ffmpeg..."
    brew install ffmpeg 2>/dev/null || echo "ffmpeg 已安装或跳过"
fi

# 3. 安装 playwright 浏览器
echo "[3/3] 安装 Chromium..."
playwright install chromium 2>/dev/null || echo "playwright 浏览器已安装"

# 4. 配置 mcporter
echo "[+] 配置 mcporter..."
CONFIG_PATH="$WORKSPACE_ROOT/config/mcporter.json"
mkdir -p "$(dirname "$CONFIG_PATH")"

if [ ! -f "$CONFIG_PATH" ]; then
    echo '{}' > "$CONFIG_PATH"
fi

if grep -q '"douyin-analyzer"' "$CONFIG_PATH" 2>/dev/null; then
    echo "[+] douyin-analyzer 已配置，跳过"
else
    echo "[+] 添加 douyin-analyzer 到 mcporter..."
    python3 -c "
import json

config_path = '$CONFIG_PATH'
venv_python = '$SCRIPT_DIR/.venv/bin/python3'

with open(config_path, 'r') as f:
    config = json.load(f)

if 'mcpServers' not in config:
    config['mcpServers'] = {}

config['mcpServers']['douyin-analyzer'] = {
    'command': venv_python,
    'args': ['$SCRIPT_DIR/server.py'],
    'description': '抖音视频解析下载 MCP 服务器'
}

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print('[+] 配置已写入:', config_path)
"
fi

echo ""
echo "=== 安装完成 ==="
echo "运行以下命令验证："
echo "  mcporter list | grep douyin"
echo ""
echo "重启 OpenClaw 后即可使用。"
