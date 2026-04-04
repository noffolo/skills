#!/bin/bash
#===============================================================================
# huo15-memory-evolution: 批量为所有动态 Agent 安装技能
#
# 用法: ./batch-install.sh
#
# 功能:
#   1. 为所有动态 agent 拷贝技能到各自的 skills 目录
#   2. 确保 memory/ 目录结构存在
#   3. 配置每个 agent 的独立 cron 任务（可选）
#===============================================================================

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_NAME="huo15-memory-evolution"
OPENCLAW_DIR="$HOME/.openclaw"
TIMESTAMP=$(date +%Y-%m-%d)

echo "🚀 huo15-memory-evolution 批量安装"
echo "================================"
echo "   时间: ${TIMESTAMP}"
echo ""

#===========================================
# 步骤 1: 发现所有动态 agent
#===========================================
echo "🔍 步骤1: 发现动态 Agent..."

WORKSPACES=$(find "$OPENCLAW_DIR" -maxdepth 1 -type d -name "workspace-wecom-*" 2>/dev/null | sort)
WORKSPACE_COUNT=$(echo "$WORKSPACES" | wc -l | tr -d ' ')
echo "   ✓ 发现 ${WORKSPACE_COUNT} 个动态 Agent"
echo ""

#===========================================
# 步骤 2: 为每个 agent 安装技能和配置
#===========================================
echo "📦 步骤2: 安装技能..."

INSTALLED_COUNT=0
MEMORY_INIT_COUNT=0

for ws in $WORKSPACES; do
    ws_name=$(basename "$ws")
    skills_dir="$ws/skills"
    
    echo "   → $ws_name"
    
    # 1. 确保 skills 目录存在
    mkdir -p "$skills_dir"
    
    # 2. 如果没有 huo15-memory-evolution，安装它
    if [ ! -d "$skills_dir/$SKILL_NAME" ]; then
        # 拷贝技能目录（作为子目录）
        cp -r "$SKILL_DIR" "$skills_dir/$SKILL_NAME"
        echo "     ✅ 技能已安装"
    else
        echo "     ⚠️  技能已存在，更新..."
        rm -rf "$skills_dir/$SKILL_NAME"
        cp -r "$SKILL_DIR" "$skills_dir/$SKILL_NAME"
        echo "     ✅ 技能已更新"
    fi
    INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
    
    # 3. 确保 memory/ 目录结构存在
    memory_dir="$ws/memory"
    if [ ! -d "$memory_dir" ]; then
        mkdir -p "$memory_dir"
        mkdir -p "$memory_dir/user"
        mkdir -p "$memory_dir/feedback"
        mkdir -p "$memory_dir/project"
        mkdir -p "$memory_dir/reference"
        mkdir -p "$memory_dir/archive"
        
        # 创建 index.json
        cat << EOF > "$memory_dir/index.json"
{
  "version": "1.0",
  "installedAt": "${TIMESTAMP}",
  "agentId": "${ws_name}",
  "entries": []
}
EOF
        
        # 创建 MEMORY.md
        cat << EOF > "$ws/MEMORY.md"
# Memory Index

*最后更新: ${TIMESTAMP}*

## user
（用户偏好和习惯）

## feedback
（纠正和确认偏好）

## project
（项目上下文和进展）

## reference
（外部系统指针）

---

*此文件为索引，内容在 memory/{type}/ 目录下*
EOF
        echo "     ✅ memory/ 目录已创建"
        MEMORY_INIT_COUNT=$((MEMORY_INIT_COUNT + 1))
    else
        echo "     ⚠️  memory/ 已存在"
    fi
    
    echo ""
done

#===========================================
# 步骤 3: 统计报告
#===========================================
echo "================================"
echo "📊 安装结果汇总"
echo "================================"
echo "   处理动态 Agent: ${WORKSPACE_COUNT}"
echo "   技能安装: ${INSTALLED_COUNT}"
echo "   记忆目录初始化: ${MEMORY_INIT_COUNT}"
echo ""

#===========================================
# 步骤 4: 验证安装
#===========================================
echo "🔍 步骤3: 验证安装..."

# 检查几个随机 agent
CHECK_AGENTS=(
    "workspace-wecom-default-dm-xun"
    "workspace-wecom-default-dm-panduoduo"
)

for ws_name in "${CHECK_AGENTS[@]}"; do
    ws="$OPENCLAW_DIR/$ws_name"
    if [ -d "$ws" ]; then
        if [ -d "$ws/skills/$SKILL_NAME" ]; then
            echo "   ✅ $ws_name: 技能已安装"
        else
            echo "   ❌ $ws_name: 技能未安装"
        fi
        
        if [ -d "$ws/memory" ]; then
            echo "   ✅ $ws_name: memory/ 已配置"
        else
            echo "   ❌ $ws_name: memory/ 未配置"
        fi
    fi
done

echo ""
echo "✅ 批量安装完成!"
echo ""
echo "📋 下一步:"
echo "   1. 为需要的 agent 配置 cron 任务"
echo "   2. 测试: OC_AGENT_ID=wecom-default-dm-xun ./scripts/verify.sh"
