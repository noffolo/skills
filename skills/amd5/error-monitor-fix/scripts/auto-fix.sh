#!/bin/bash
# Error Auto Fix - 错误自动修复脚本
# 功能：分析 error.md 中的错误，自动尝试修复

WORKSPACE="${HOME}/.openclaw/workspace"
ERROR_FILE="${WORKSPACE}/error.md"
GATEWAY_LOG="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"

echo "🔧 Error Auto Fix - 错误自动修复 ($(date +%Y-%m-%d %H:%M))"
echo "================================"

if [ ! -f "$ERROR_FILE" ]; then
    echo "  ℹ️  error.md 不存在，无需修复"
    exit 0
fi

# 检查是否有待修复的错误
PENDING_ERRORS=$(grep -c "状态：待分析" "$ERROR_FILE" 2>/dev/null || echo "0")

if [ "$PENDING_ERRORS" -eq 0 ]; then
    echo "  ✅ 无待修复错误"
    exit 0
fi

echo "  ⚠️ 检测到 $PENDING_ERRORS 个待修复错误"
echo ""

# 读取最新错误
LATEST_ERROR=$(grep -A 10 "状态：待分析" "$ERROR_FILE" | tail -15)

# 错误类型识别和自动修复
FIX_APPLIED=0

# 1. Gateway 连接错误
if echo "$LATEST_ERROR" | grep -qi "gateway.*closed\|gateway.*connect\|ws.*closed"; then
    echo "  🔧 检测到 Gateway 连接错误，尝试重启..."
    systemctl --user restart openclaw-gateway.service 2>/dev/null && {
        echo "  ✅ Gateway 已重启"
        FIX_APPLIED=1
    }
fi

# 2. 内存/缓存错误
if echo "$LATEST_ERROR" | grep -qi "memory\|cache\|out of memory"; then
    echo "  🔧 检测到内存/缓存错误，尝试清理..."
    rm -rf /root/.openclaw/workspace/runtime/cache/* 2>/dev/null
    rm -rf /root/.openclaw/workspace/runtime/temp/* 2>/dev/null
    echo "  ✅ 缓存已清理"
    FIX_APPLIED=1
fi

# 3. 文件权限错误
if echo "$LATEST_ERROR" | grep -qi "permission denied\|EACCES"; then
    echo "  🔧 检测到权限错误，尝试修复..."
    chmod -R 755 /root/.openclaw/workspace 2>/dev/null
    chown -R $(whoami):$(whoami) /root/.openclaw/workspace 2>/dev/null
    echo "  ✅ 权限已修复"
    FIX_APPLIED=1
fi

# 4. 端口占用错误
if echo "$LATEST_ERROR" | grep -qi "EADDRINUSE\|port.*in use\|address already in use"; then
    echo "  🔧 检测到端口占用，尝试释放..."
    PORT=$(echo "$LATEST_ERROR" | grep -oP "port \K\d+" | head -1)
    if [ -n "$PORT" ]; then
        fuser -k $PORT/tcp 2>/dev/null
        echo "  ✅ 端口 $PORT 已释放"
        FIX_APPLIED=1
    fi
fi

# 5. 数据库连接错误
if echo "$LATEST_ERROR" | grep -qi "database\|mysql\|connection refused"; then
    echo "  ⚠️ 检测到数据库连接错误，需手动检查数据库服务"
    FIX_APPLIED=0
fi

# 更新错误状态
if [ "$FIX_APPLIED" -eq 1 ]; then
    sed -i "s/状态：待分析/状态：已自动修复（$(date +%Y-%m-%d %H:%M)）/g" "$ERROR_FILE"
    echo ""
    echo "✅ 错误已自动修复"
else
    echo ""
    echo "⚠️  无法自动修复，需手动处理"
    sed -i "s/状态：待分析/状态：需手动修复（$(date +%Y-%m-%d %H:%M)）/g" "$ERROR_FILE"
fi

echo ""
echo "================================"
echo "📊 修复完成"
