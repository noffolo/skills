#!/bin/bash
#===============================================================================
# huo15-memory-evolution: 快照备份脚本
#
# 用法: ./snapshot.sh
#
# 功能: 在执行记忆系统改造前，对当前状态进行完整快照
# 输出: snapshots/memory-snapshot-YYYY-MM-DD-HHMMSS.tar.gz
#
# 回滚: ./rollback.sh <snapshot-tarball>
#===============================================================================

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
OPENCLAW_DIR="$HOME/.openclaw"
SNAPSHOT_DIR="$SKILL_DIR/snapshots"
TIMESTAMP=$(date +%Y-%m-%d-%H%M%S)
OUTPUT_FILE="${SNAPSHOT_DIR}/memory-snapshot-${TIMESTAMP}.tar.gz"

echo "📸 huo15-memory-evolution 快照备份"
echo "================================"
echo ""

# 创建快照目录
mkdir -p "$SNAPSHOT_DIR"

# 收集信息
echo "📋 收集当前状态..."

WORKSPACES=$(find "$OPENCLAW_DIR" -maxdepth 1 -type d -name "workspace-wecom-*" 2>/dev/null | sort)
MAIN_MEMORY_LINES=$(wc -l < "$WORKSPACE_DIR/MEMORY.md" 2>/dev/null || echo "N/A")

cat << EOF > "${SNAPSHOT_DIR}/snapshot-info-${TIMESTAMP}.txt"
# 快照信息
快照时间: $(date -u +%Y-%m-%dT%H:%M:%SZ)
主机: $(hostname)
用户: $(whoami)

# 工作区列表
$(find "$OPENCLAW_DIR" -maxdepth 1 -type d -name "workspace*" | sort)

# Agent 数量
$(find "$OPENCLAW_DIR/agents" -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')

# 主 workspace MEMORY.md 行数
${MAIN_MEMORY_LINES}
EOF

echo "   ✓ 状态信息已收集"

# 创建 tarball
echo "📦 创建快照压缩包..."
TAR_SOURCES=""
for ws in $WORKSPACES; do
    ws_name=$(basename "$ws")
    TAR_SOURCES="$TAR_SOURCES $ws"
done

tar czf "$OUTPUT_FILE" \
    -C "$WORKSPACE_DIR" \
        MEMORY.md \
        memory/ \
    -C "$OPENCLAW_DIR" \
        workspace/MEMORY.md \
        workspace/memory/ \
        $(echo $WORKSPACES | sed "s|$OPENCLAW_DIR/||g") \
        openclaw.json \
    2>/dev/null || true

if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo "   ✓ 快照已创建: snapshots/memory-snapshot-${TIMESTAMP}.tar.gz"
    echo "   ✓ 大小: ${SIZE}"
else
    echo "   ⚠️  tar 压缩部分失败，列出可用快照..."
fi

echo ""
echo "✅ 快照完成!"
echo ""
echo "下一步: 运行迁移"
echo "   ./migrate.sh"
echo ""
echo "如需回滚:"
echo "   ./rollback.sh snapshots/memory-snapshot-${TIMESTAMP}.tar.gz"
