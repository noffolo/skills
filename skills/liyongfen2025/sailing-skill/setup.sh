#!/bin/bash
# Setup script for Sailing Sports MCP Skill

set -e

echo "🚀 设置 Sailing Sports MCP Skill..."
echo ""

# 检查 mcporter
if ! command -v mcporter &> /dev/null; then
    echo "⚠️  未找到 mcporter（MCP 服务管理工具）。"
    echo "   需要执行全局安装：npm install -g mcporter"
    echo "   这将向系统全局 npm 目录写入文件。"
    echo ""
    read -r -p "是否继续安装 mcporter？(y/N): " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        npm install -g mcporter
        echo "✅ mcporter 安装完成"
    else
        echo "❌ 已取消安装。请手动安装 mcporter 后重新运行此脚本："
        echo "   npm install -g mcporter"
        exit 1
    fi
fi

# 检查 SAILING_TAI_IT_TOKEN 环境变量
echo "🔍 检查 Sailing Sports Token 环境变量..."
if [ -z "$SAILING_TAI_IT_TOKEN" ]; then
    echo "❌ 错误：未检测到 SAILING_TAI_IT_TOKEN 环境变量！"
    echo "请先执行以下步骤："
    echo "  第1步：📌 前往申请 Token：https://sailing.sports.qq.com/open/token-apply"
    echo "  第2步：设置环境变量："
    echo "    export SAILING_TAI_IT_TOKEN=\"your_actual_token_here\""
    echo "  或在执行脚本时直接传入："
    echo "    SAILING_TAI_IT_TOKEN=\"your_actual_token_here\" bash setup.sh"
    exit 1
else
    echo "✅ SAILING_TAI_IT_TOKEN 环境变量已配置"
fi
echo ""

# 安全提示：告知用户 Token 将被持久化存储
echo "⚠️  安全提示：您的 SAILING_TAI_IT_TOKEN 将以明文形式保存到"
echo "   mcporter 本地配置文件中（通常位于 ~/.mcporter/ 目录）。"
echo "   请确保该目录仅限您本人访问，不要提交到版本控制系统。"
echo "   如需撤销，可运行：mcporter config remove sailing-sports-mcp"
echo ""
read -r -p "是否继续配置？(y/N): " confirm_config
if [[ ! "$confirm_config" =~ ^[Yy]$ ]]; then
    echo "❌ 已取消配置。"
    exit 1
fi

# 添加 MCP 配置
echo "🔧 配置 mcporter..."

mcporter config add sailing-sports-mcp https://sailing.sports.qq.com/api/tteagent/sport_pub/mcp \
    --header "Authorization=Bearer ${SAILING_TAI_IT_TOKEN}" \
    --header "Content-Type=application/json" \
    --scope global

echo "✅ 配置完成！"

# 验证配置
echo "🧪 验证配置..."
if mcporter list 2>&1 | grep -q "sailing-sports-mcp"; then
    echo "✅ 配置验证成功！"
    echo ""
    mcporter list | grep -A 1 "sailing-sports-mcp" || true
else
    echo "⚠️  配置验证失败，请检查网络或 Token 是否有效"
    echo ""
    echo "如有问题，请前往 https://sailing.sports.qq.com/open/token-apply 重新获取 Token"
fi

echo ""
echo "─────────────────────────────────────"
echo "🎉 设置完成！"
