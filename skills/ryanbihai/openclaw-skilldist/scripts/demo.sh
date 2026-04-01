#!/bin/bash
# demo.sh - 演示模式（不实际发布）
# 用法: ./demo.sh <slug>
# 
# 显示发布流程，但不执行任何实际操作

WORKSPACE="/home/node/.openclaw/workspace/skills"
SKILL="${1:?用法: $0 <slug>}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Skill Publisher - 演示模式${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📦 Skill: $SKILL"
echo "📂 目录: $WORKSPACE/$SKILL"
echo ""
echo "此模式仅显示发布流程，不执行实际操作"
echo ""

# 检查目录
if [ ! -d "$WORKSPACE/$SKILL" ]; then
    echo -e "${RED}❌ Skill 目录不存在${NC}"
    exit 1
fi

# 显示元数据
if [ -f "$WORKSPACE/$SKILL/_meta.json" ]; then
    echo -e "${GREEN}✓ 找到 _meta.json${NC}"
    cat "$WORKSPACE/$SKILL/_meta.json" | python3 -m json.tool 2>/dev/null | head -10
else
    echo -e "${YELLOW}⚠ 未找到 _meta.json${NC}"
fi

echo ""
echo -e "${GREEN}━━━ 演示：发布步骤 ━━━${NC}"
echo ""
echo "1️⃣  加载 .env 中的 Token"
echo "    → 检查 CLAWHUB_TOKEN, GITHUB_TOKEN"
echo ""
echo "2️⃣  发布到 ClawHub"
echo "    → npx clawhub publish . --slug $SKILL"
echo "    → 如果未配置 CLAWHUB_TOKEN → 跳过"
echo ""
echo "3️⃣  发布到 GitHub"
echo "    → git push 到仓库"
echo "    → 如果未配置 GITHUB_TOKEN → 跳过"
echo ""
echo "4️⃣  生成手动平台提交文本"
echo "    → COZE / 腾讯元器 / 阿里百炼 / SkillzWave"
echo ""

# 检查 Token 状态
ENV_FILE="$(dirname "$0")/../.env"
if [ -f "$ENV_FILE" ]; then
    echo -e "${GREEN}━━━ 当前 Token 状态 ━━━${NC}"
    source "$ENV_FILE"
    
    if [ -n "$CLAWHUB_TOKEN" ]; then
        echo -e "   🌐 ClawHub:  ✅ 已配置"
    else
        echo -e "   🌐 ClawHub:  ❌ 未配置"
    fi
    
    if [ -n "$GITHUB_TOKEN" ]; then
        echo -e "   💻 GitHub:   ✅ 已配置"
    else
        echo -e "   💻 GitHub:   ❌ 未配置"
    fi
    
    if [ -n "$COZE_TOKEN" ]; then
        echo -e "   🤖 COZE:     ✅ 已配置"
    else
        echo -e "   🤖 COZE:     ❌ 未配置"
    fi
else
    echo -e "${YELLOW}⚠ 未找到 .env 文件（首次使用？）${NC}"
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "💡 实际发布: python scripts/publish.sh $SKILL"
echo "💡 配置 Token: python scripts/setup_tokens.py"
echo ""
