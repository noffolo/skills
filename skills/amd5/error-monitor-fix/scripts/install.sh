#!/bin/bash
# Error Monitor Fix - 安装脚本
# 用法：bash skills/error-monitor-fix/scripts/install.sh

set -e

WORKSPACE="${HOME}/.openclaw/workspace"
SKILL_DIR="${WORKSPACE}/skills/error-monitor-fix"

echo "🔧 开始安装 Error Monitor Fix..."
echo ""

# ===== Step 1: 创建错误日志文件 =====
echo "📁 Step 1: 创建错误日志文件..."
ERROR_FILE="${WORKSPACE}/error.md"
if [ ! -f "$ERROR_FILE" ]; then
    cat > "$ERROR_FILE" << 'EOF'
# OpenClaw Error Log

自动生成的错误日志文件，记录系统运行中的 error 类型错误。

---

EOF
    echo "   ✅ 已创建 error.md"
else
    echo "   ✅ error.md 已存在"
fi
echo ""

# ===== Step 2: 注册 Cron 任务 =====
echo "⏰ Step 3: 注册 Cron 任务..."

CRON_LIST=$(openclaw cron list 2>/dev/null | grep -c "错误监控" || echo "0")
CRON_LIST=$(echo "$CRON_LIST" | tr -d '[:space:]')

if ! [[ "$CRON_LIST" =~ ^[0-9]+$ ]]; then
    CRON_LIST=0
fi

if [ "$CRON_LIST" -ge 2 ]; then
    echo "   ✅ Cron 任务已存在（跳过添加）"
else
    echo "   📅 正在添加错误监控 (5 分钟)..."
    openclaw cron add --name "错误监控" \
      --schedule '{"kind":"every","everyMs":300000}' \
      --payload '{"kind":"systemEvent","text":"🔍 错误监控检查"}' \
      --session-target main \
      --delivery '{"mode":"none"}' 2>/dev/null && echo "   ✅ 已添加" || echo "   ⚠️  添加失败"

    echo "   📅 正在添加错误自动修复 (10 分钟)..."
    openclaw cron add --name "错误自动修复" \
      --schedule '{"kind":"every","everyMs":600000}' \
      --payload '{"kind":"systemEvent","text":"🔧 错误自动修复检查"}' \
      --session-target main \
      --delivery '{"mode":"none"}' 2>/dev/null && echo "   ✅ 已添加" || echo "   ⚠️  添加失败"
fi

echo ""

# ===== Step 3: 设置脚本权限 =====
echo "🔧 Step 4: 设置脚本权限..."
chmod +x "${SKILL_DIR}/scripts/monitor-error.sh"
chmod +x "${SKILL_DIR}/scripts/auto-fix.sh"
echo "   ✅ 脚本权限已设置"

echo ""

# ===== 完成 =====
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Error Monitor 安装完成！"
echo ""
echo "   📂 错误日志：~/.openclaw/workspace/error.md"
echo "   🔍 监控脚本：skills/error-monitor-fix/scripts/monitor-error.sh"
echo "   🔧 修复脚本：skills/error-monitor-fix/scripts/auto-fix.sh"
echo "   ⏰ Cron: 2 个定时任务已配置"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
