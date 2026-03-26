#!/bin/bash
# Error Monitor - 错误日志监控脚本
# 功能：实时捕获 OpenClaw 运行日志中的 error 类型错误，追加到 error.md

WORKSPACE="${HOME}/.openclaw/workspace"
ERROR_FILE="${WORKSPACE}/error.md"
LOG_FILE="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"

echo "🔍 Error Monitor - 错误日志监控 ($(date +%Y-%m-%d %H:%M))"
echo "================================"

# 检查日志文件是否存在
if [ ! -f "$LOG_FILE" ]; then
    echo "  ℹ️  今日日志文件不存在：$LOG_FILE"
    exit 0
fi

# 检查错误文件，不存在则创建
if [ ! -f "$ERROR_FILE" ]; then
    echo "# OpenClaw Error Log" > "$ERROR_FILE"
    echo "" >> "$ERROR_FILE"
    echo "自动生成的错误日志文件，记录系统运行中的 error 类型错误。" >> "$ERROR_FILE"
    echo "" >> "$ERROR_FILE"
    echo "---" >> "$ERROR_FILE"
    echo "" >> "$ERROR_FILE"
    echo "✅ 已创建 error.md"
fi

# 获取最近 5 分钟的错误日志（排除已处理的）
LAST_CHECK_TIME=$(grep -oP "Last check: \K\d+" "$ERROR_FILE" 2>/dev/null || echo "0")
CURRENT_TIME=$(date +%s)
SINCE_TIME=$((CURRENT_TIME - 300))  # 5 分钟前

# 从日志中提取 error 类型错误
ERRORS=$(grep -iE "\[error\]|\[ERROR\]|error:|Error:|failed|failed to|exception|trace" "$LOG_FILE" 2>/dev/null | tail -20)

if [ -n "$ERRORS" ]; then
    echo "  ⚠️ 检测到错误日志:"
    
    # 追加到 error.md
    echo "### [$(date +%Y-%m-%d %H:%M:%S)] 自动捕获错误" >> "$ERROR_FILE"
    echo "" >> "$ERROR_FILE"
    echo "\`\`\`" >> "$ERROR_FILE"
    echo "$ERRORS" >> "$ERROR_FILE"
    echo "\`\`\`" >> "$ERROR_FILE"
    echo "" >> "$ERROR_FILE"
    echo "状态：待分析" >> "$ERROR_FILE"
    echo "" >> "$ERROR_FILE"
    echo "---" >> "$ERROR_FILE"
    echo "" >> "$ERROR_FILE"
    
    echo "  ✅ 已追加到 error.md"
else
    echo "  ✅ 无新错误"
fi

# 更新最后检查时间
sed -i "s/Last check: [0-9]*/Last check: $CURRENT_TIME/" "$ERROR_FILE" 2>/dev/null || {
    echo "<!-- Last check: $CURRENT_TIME -->" >> "$ERROR_FILE"
}

echo ""
echo "================================"
echo "📊 检查完成"
