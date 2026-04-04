#!/bin/bash
#===============================================================================
# huo15-memory-evolution: 从零安装脚本
#
# 用法: ./install.sh
#
# 功能: 在全新的 OpenClaw 上初始化记忆系统
#       不需要快照，不需要迁移，直接创建干净的目录结构
#
# 适用场景:
#   - 新安装的 OpenClaw
#   - 新的工作机器
#   - 其他 OpenClaw 实例
#
#===============================================================================

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE_DIR="$HOME/.openclaw/workspace"
OPENCLAW_DIR="$HOME/.openclaw"
TIMESTAMP=$(date +%Y-%m-%d)

echo "🚀 huo15-memory-evolution 从零安装"
echo "================================"
echo "   时间: ${TIMESTAMP}"
echo ""

#===========================================
# 步骤 1: 检查环境
#===========================================
echo "🔍 步骤1: 检查环境..."

# 检查 OpenClaw workspace 是否存在
if [ ! -d "$WORKSPACE_DIR" ]; then
    echo "❌ OpenClaw workspace 不存在: $WORKSPACE_DIR"
    echo "   请先安装 OpenClaw"
    exit 1
fi

# 检查 OC_AGENT_ID 环境变量
CURRENT_AGENT="${OC_AGENT_ID:-main}"
echo "   ✓ OpenClaw workspace 存在"
echo "   ✓ 当前 Agent: ${CURRENT_AGENT}"

# 检查企微插件是否安装
WECOM_PLUGIN=""
if [ -d "$OPENCLAW_DIR/extensions/wecom" ]; then
    WECOM_PLUGIN="installed"
    echo "   ✓ 企微插件: 已安装（动态 Agent 隔离功能可用）"
elif [ -d "$OPENCLAW_DIR/plugins/wecom" ]; then
    WECOM_PLUGIN="installed"
    echo "   ✓ 企微插件: 已安装（动态 Agent 隔离功能可用）"
else
    echo "   ⚠️  企微插件: 未安装"
    echo "   ⚠️  提示: 本技能的记忆隔离功能依赖 @huo15/wecom 插件"
    echo "   ⚠️  如需完整功能，请先安装企微插件"
fi

echo ""

#===========================================
# 步骤 2: 创建主 workspace 记忆目录
#===========================================
echo "📁 步骤2: 创建主 workspace 记忆目录..."

mkdir -p "$WORKSPACE_DIR/memory"
mkdir -p "$WORKSPACE_DIR/memory/user"
mkdir -p "$WORKSPACE_DIR/memory/feedback"
mkdir -p "$WORKSPACE_DIR/memory/project"
mkdir -p "$WORKSPACE_DIR/memory/reference"
mkdir -p "$WORKSPACE_DIR/memory/archive"
mkdir -p "$WORKSPACE_DIR/memory/activity"  # 保留原架构兼容

echo "   ✓ memory/{user,feedback,project,reference,archive,activity}/ 已创建"
echo ""

#===========================================
# 步骤 3: 创建 index.json
#===========================================
echo "📋 步骤3: 创建结构化索引..."

cat << EOF > "$WORKSPACE_DIR/memory/index.json"
{
  "version": "1.0",
  "installedAt": "${TIMESTAMP}",
  "migrationFrom": "none (fresh install)",
  "entries": []
}
EOF

echo "   ✓ memory/index.json 已创建"
echo ""

#===========================================
# 步骤 4: 创建 MEMORY.md 索引
#===========================================
echo "📝 步骤4: 创建 MEMORY.md 索引..."

cat << EOF > "$WORKSPACE_DIR/MEMORY.md"
# Memory Index

*最后更新: ${TIMESTAMP} | 最多 200 行*

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

## 记忆写入规范

**两步写入（强制）：**
1. 将记忆写入 memory/{type}/<name>.md
2. 在上方索引中添加一行指针

**禁止：**
- 禁止将记忆内容直接写入 MEMORY.md
- 禁止写入可从代码/配置推导的信息
- 禁止记录实际凭证值（只记录位置）

---

*技能: huo15-memory-evolution v1.0.0*
EOF

echo "   ✓ MEMORY.md 索引已创建"
echo ""

#===========================================
# 步骤 5: 为已有动态 agent 创建记忆目录
#===========================================
echo "🔒 步骤5: 为动态 Agent 创建独立记忆空间..."

WORKSPACES=$(find "$OPENCLAW_DIR" -maxdepth 1 -type d -name "workspace-wecom-*" 2>/dev/null | sort)
AGENT_COUNT=0

for ws in $WORKSPACES; do
    ws_name=$(basename "$ws")
    AGENT_COUNT=$((AGENT_COUNT + 1))
    
    echo "   → $ws_name"
    
    # 创建 memory 目录结构
    mkdir -p "$ws/memory"
    mkdir -p "$ws/memory/user"
    mkdir -p "$ws/memory/feedback"
    mkdir -p "$ws/memory/project"
    mkdir -p "$ws/memory/reference"
    mkdir -p "$ws/memory/archive"
    
    # 创建 index.json
    cat << EOF > "$ws/memory/index.json"
{
  "version": "1.0",
  "installedAt": "${TIMESTAMP}",
  "agentId": "${ws_name}",
  "entries": []
}
EOF
    
    # 创建干净的 MEMORY.md
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
    
    echo "   ✓ $ws_name 记忆空间已创建"
done

echo "   ✓ 共处理 ${AGENT_COUNT} 个动态 Agent"
echo ""

#===========================================
# 步骤 6: 生成安装报告
#===========================================
echo "📊 步骤6: 生成安装报告..."

REPORT_FILE="$SKILL_DIR/INSTALL-REPORT-${TIMESTAMP}.md"

cat << EOF > "$REPORT_FILE"
# huo15-memory-evolution 安装报告
安装时间: ${TIMESTAMP}

## 环境信息
- Hostname: $(hostname)
- User: $(whoami)
- OpenClaw Workspace: ${WORKSPACE_DIR}
- 当前 Agent: ${CURRENT_AGENT}

## 安装概览

| 项目 | 数值 |
|------|------|
| 主 workspace 记忆目录 | ✅ 已创建 |
| 动态 Agent 记忆空间 | ${AGENT_COUNT} 个 |
| index.json | ✅ 已创建 |
| MEMORY.md 索引 | ✅ 已创建 |

## 目录结构

```
workspace/
├── MEMORY.md                    ← 主索引
└── memory/
    ├── index.json              ← 结构化索引
    ├── user/                  ← 用户偏好
    ├── feedback/              ← 纠正反馈
    ├── project/              ← 项目上下文
    ├── reference/            ← 外部系统指针
    └── archive/              ← 已归档

workspace-wecom-*/
├── MEMORY.md                  ← 独立索引
└── memory/
    └── {user,feedback,project,reference,archive}/
```

## 下一步

1. **验证安装**: ./verify.sh
2. **开始使用**: 在对话中保存记忆，观察分类
3. **阅读规范**: 查看 memory-types.json 了解四类分类

## 四类记忆分类

| 类型 | 说明 | 示例 |
|------|------|------|
| user | 用户偏好 | Sir 喜欢简洁回答 |
| feedback | 纠正反馈 | 不要用 touser 发图片 |
| project | 项目上下文 | 软著申请已开始 |
| reference | 外部系统指针 | Odoo 系统地址 |

## 技能信息
- Skill: huo15-memory-evolution
- Version: 1.0.0
- 安装时间: ${TIMESTAMP}
EOF

echo "   ✓ 报告: INSTALL-REPORT-${TIMESTAMP}.md"
echo ""

#===========================================
# 完成
#===========================================
echo "================================"
echo "✅ 从零安装完成!"
echo ""
echo "📋 下一步:"
echo "   1. 验证安装: ./verify.sh"
echo "   2. 开始使用新记忆系统"
echo ""
echo "📖 记忆写入规范:"
echo "   1. 将记忆写入 memory/{type}/<name>.md"
echo "   2. 在 MEMORY.md 索引中添加一行指针"
echo ""
