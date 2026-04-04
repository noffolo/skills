---
name: huo15-memory-evolution
description: 火一五记忆进化技能 - 基于 Claude Code 源码分析，为 OpenClaw 提供完整的记忆管理系统。支持四类记忆分类、企微动态 Agent 隔离、Dream Agent 日志提炼、Team Memory 共享。触发词：记忆系统、记忆进化、记忆重构。
---

# 🧠 火一五记忆进化技能

> **作者**: 火一五信息科技有限公司  
> **版本**: v2.7.0  
> **参考**: Claude Code 源码 (memdir.ts, memoryTypes.ts, teamMemPaths.ts)  
> **触发词**: 记忆系统、记忆进化、记忆重构、改造记忆系统

---

## 一、简介

火一五记忆进化技能是一套完整的记忆管理系统，基于 Claude Code 源码分析开发，为 OpenClaw 提供媲美甚至部分超越 Claude Code 的记忆能力。

### 核心特性

| 特性 | 说明 |
|------|------|
| 🗂️ **四类记忆分类** | user / feedback / project / reference |
| 🔒 **Agent 记忆隔离** | 每个企微用户/群聊独立记忆空间 |
| 🌙 **Dream Agent** | 每日自动日志提炼，LLM 驱动，自动创建独立记忆文件 |
| 👥 **Team Memory** | 群聊 agent 之间共享部分记忆 |
| ✅ **Drift 校验** | 自动检测过时记忆 |
| 🔄 **批量安装** | 一键为所有动态 agent 安装 |

---

## 二、快速开始

### 2.1 安装技能

```bash
clawhub install huo15-memory-evolution
```

### 2.2 初始化记忆系统

```bash
cd ~/.openclaw/workspace/skills/huo15-memory-evolution
./scripts/install.sh
```

### 2.3 验证安装

```bash
./scripts/verify.sh
```

---

## 三、记忆分类体系

### 3.1 四类记忆

| 类型 | 说明 | 示例 |
|------|------|------|
| **user** | 用户画像、偏好、习惯 | Sir 喜欢简洁回答 |
| **feedback** | 纠正反馈、确认偏好 | 不要用 touser 发图片 |
| **project** | 项目上下文、决策、进展 | 软著申请已开始 |
| **reference** | 外部系统指针 | Odoo 系统地址 |

### 3.2 记忆文件格式

每个记忆文件使用 frontmatter：

```yaml
---
name: wecom-media-send-rule
type: feedback
description: 企微群聊发图片必须用 chatid，不是 touser
created: 2026-03-31
updated: 2026-03-31
---

## 规则
企微群聊发图片必须用 chatid，不是 touser

## 为什么值得记忆
之前用 touser 发送图片失败，报错 86008

## 如何应用
在企微群聊场景下，媒体发送一律使用 chatid 参数
```

### 3.3 禁止写入的内容

- ❌ 代码模式、约定、架构 — 可从代码推导
- ❌ Git 历史 — git log 权威
- ❌ 调试方案 — 修复在代码中
- ❌ 实际凭证值 — 只记录位置
- ❌ 临时任务详情 — 写在 HEARTBEAT.md

---

## 四、核心功能详解

### 4.1 Dream Agent（每日日志提炼）

**原理**：每天自动读取日志，使用 LLM 分析提取值得记忆的内容。

**4 阶段工作流**：

```
Stage 1: Orient    → 读取昨日日志
Stage 2: Gather    → LLM 分析提取记忆
Stage 3: Consolidate → 写入记忆文件 + 更新索引
Stage 4: Prune     → 标记过时记忆
```

**使用方式**：

```bash
# 手动运行
cd ~/.openclaw/workspace/skills/huo15-memory-evolution
./scripts/dream.sh

# 查看日志
cat ~/.openclaw/workspace/memory/YYYY-MM-DD.md

# 查看生成的记忆
ls ~/.openclaw/workspace/memory/project/
```

**定时任务**：每天 09:00 自动运行（已配置 cron）

---

### 4.2 主动记忆写入（save-memory）

**使用方式**：

```bash
# 命令行模式
cd ~/.openclaw/workspace/skills/huo15-memory-evolution
./scripts/save-memory.sh <type> <name> <description> << 'EOF'
记忆内容
EOF

# 示例：写入 feedback
./scripts/save-memory.sh feedback wecom-rules "企微发图片用chatid" << 'EOF'
## 规则
企微群聊发图片必须用 chatid，不是 touser

## 为什么值得记忆
之前用 touser 发送图片失败，报错 86008

## 如何应用
在企微群聊场景下，媒体发送一律使用 chatid 参数
EOF

# 交互模式
./scripts/save-memory.sh --interactive
```

**支持的类型**：user / feedback / project / reference

---

### 4.3 Drift 校验（记忆有效性检查）

**原理**：检查记忆文件是否存在、更新日期是否过期。

```bash
cd ~/.openclaw/workspace/skills/huo15-memory-evolution
./scripts/check-drift.sh
```

**输出示例**：

```
🔍 记忆 Drift 检查
================================
检查日期: 2026-04-05
过期阈值: 2026-01-05 (90天前)

🔹 user/
   ✅ OK: user-preferences.md

🔹 feedback/
   ✅ OK: wecom-rules.md
   ⏰ OLD: old-rule.md (updated: 2025-01-01)

📊 检查结果汇总
   ✅ 正常: 5
   ⏰ 过期: 1
```

**定时任务**：每 6 小时自动检查（已配置 cron）

---

### 4.4 Team Memory 共享

**功能**：将某个记忆标记为团队共享，同步到所有群聊 agent。

```bash
cd ~/.openclaw/workspace/skills/huo15-memory-evolution

# 查看共享列表
./scripts/team-memory.sh list

# 共享一个记忆
./scripts/team-memory.sh share wecom-rules

# 取消共享
./scripts/team-memory.sh unshare wecom-rules

# 同步到所有群聊 agent
./scripts/team-memory.sh sync

# 交互模式
./scripts/team-memory.sh interactive
```

---

### 4.5 记忆隔离

**架构**：每个企微用户/群聊有独立的 workspace。

```
~/.openclaw/
├── workspace/                          # 主 Agent (ZhaoBo)
│   ├── MEMORY.md                      # 主索引
│   └── memory/                        # 主记忆
│       ├── user/
│       ├── feedback/
│       ├── project/
│       └── reference/
├── workspace-wecom-default-dm-xun/   # Xun 的独立空间
│   ├── MEMORY.md                      # 独立索引
│   └── memory/                        # 独立记忆（与主 Agent 完全隔离）
└── workspace-wecom-default-group-xxx/ # 群聊 Agent
    ├── MEMORY.md
    └── memory/
```

**敏感信息保护**：银行账号、公司凭证等绝不可出现在非主 Agent 的记忆中。

---

## 五、脚本清单

| 脚本 | 功能 | 频率 |
|------|------|------|
| `dream.sh` | 每日日志提炼（4阶段） | 每天 09:00 |
| `dream-api.py` | LLM API 调用 | 被 dream.sh 调用 |
| `dream-consolidate.py` | 记忆文件生成器 | 被 dream.sh 调用 |
| `save-memory.sh` | 主动记忆写入 | 按需 |
| `check-drift.sh` | Drift 校验 | 每 6 小时 |
| `memory-stats.py` | 记忆访问统计 | 每次读取时 |
| `team-memory.sh` | Team Memory 共享 | 按需 |
| `install.sh` | 从零安装 | 首次安装 |
| `batch-install.sh` | 批量为所有 Agent 安装 | 首次安装 |
| `verify.sh` | 验证安装 | 按需 |
| `snapshot.sh` | 快照备份 | 升级前 |
| `rollback.sh` | 回滚 | 按需 |

---

## 六、配置说明

### 6.1 路径路由

技能根据 `OC_AGENT_ID` 自动选择正确的 workspace：

```javascript
// config/agent-routing.js
if (agentId === 'main') {
    base = '~/.openclaw/workspace'
} else if (agentId.startsWith('wecom-dm-')) {
    base = `~/.openclaw/workspace-${agentId}`  // 私聊 agent
} else if (agentId.startsWith('wecom-group-')) {
    base = `~/.openclaw/workspace-${agentId}`  // 群聊 agent
}
```

### 6.2 记忆类型定义

详细定义见 `config/memory-types.json`。

---

## 七、完整示例

### 7.1 首次安装完整流程

```bash
# 1. 安装技能
clawhub install huo15-memory-evolution

# 2. 初始化（为所有动态 agent 创建记忆空间）
cd ~/.openclaw/workspace/skills/huo15-memory-evolution
./scripts/install.sh

# 3. 验证
./scripts/verify.sh

# 4. 查看结果
cat ~/.openclaw/workspace/MEMORY.md
```

### 7.2 每日使用流程

```bash
# 1. 在对话中保存记忆
./scripts/save-memory.sh feedback my-rule "我的规则" << 'EOF'
记忆内容...
EOF

# 2. 查看当前记忆
cat ~/.openclaw/workspace/MEMORY.md

# 3. 运行 drift 检查
./scripts/check-drift.sh
```

### 7.3 升级前备份

```bash
# 1. 创建快照
./scripts/snapshot.sh

# 2. 执行升级
clawhub install huo15-memory-evolution

# 3. 如有问题，回滚
./scripts/rollback.sh snapshots/memory-snapshot-YYYY-MM-DD-HHMMSS.tar.gz
```

---

## 八、故障排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| Dream Agent LLM API 失败 | 网络问题或 API Key | 检查网络，查看 `/tmp/dream-api.log` |
| 记忆文件创建成功但索引未更新 | 权限问题 | 检查 MEMORY.md 写入权限 |
| Agent 隔离失效 | 旧 workspace 未清理 | 运行 `batch-install.sh` 重新初始化 |
| 敏感信息泄露 | 手动编辑错误 | 运行 `verify.sh` 检查，用 `rollback.sh` 恢复 |

---

## 九、新增功能详解

### 9.1 Dream Agent 自动创建独立记忆文件

Dream Agent 不仅创建日志摘要，还自动根据 LLM 分析结果创建独立的记忆文件：

```bash
# 日志 → LLM 分析 → 独立记忆文件
memory/
├── user/sir_communication_preference.md    ← 自动创建
├── feedback/agent_memory_isolation_verified.md  ← 自动创建
├── project/memory_system_v230_development.md  ← 自动创建
└── reference/claude_code_as_spec_reference.md  ← 自动创建
```

### 9.2 记忆访问统计

追踪每个记忆被访问的次数和最后访问时间：

```bash
# 查看统计
python3 scripts/memory-stats.py stats

# 读取记忆时自动记录访问
python3 scripts/memory-stats.py read memory/user/preference.md
# ✅ 已记录访问: memory/user/preference.md (共 3 次)

# 手动记录访问
python3 scripts/memory-stats.py access memory/user/test.md user "测试记忆"
```

**统计信息**：
- 访问次数（accessCount）
- 首次访问时间（firstAccessed）
- 最后访问时间（lastAccessed）
- 存储在 `memory/index.json` 中

---

## 十、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| **v2.7.0** | 2026-04-05 | 实现日志提炼为独立记忆文件 + 记忆访问统计 |
| v2.6.0 | 2026-04-05 | 新增与其他技能的关系说明 |
| v2.5.0 | 2026-04-05 | 规范化文档，完善使用说明 |
| v2.4.0 | 2026-04-05 | Dream Agent LLM API 修复，新增 save-memory.sh、team-memory.sh |
| v2.3.0 | 2026-04-05 | 对标 Claude 源码，完善记忆规范 |
| v2.0.0 | 2026-04-04 | Dream Agent + Drift 校验 |
| v1.0.0 | 2026-04-03 | 初始版本 |

---

## 十、与其他技能的关系

### 10.1 已替代的技能（不可共存）

以下技能与 huo15-memory-evolution 功能重叠，**不可共存**：

| 技能 | 原功能 | 替代方案 |
|------|--------|---------|
| **memory-tiering** | HOT/WARM/COLD 分层 | ✅ huo15-memory-evolution 四类分类 |
| **fluid-memory** | 遗忘曲线衰减 | ✅ huo15-memory-evolution Drift 校验 |
| **memory-hygiene** | 向量记忆清理 | ✅ huo15-memory-evolution check-drift.sh |
| **self-improving-agent** | 错误/纠正记录 | ✅ huo15-memory-evolution feedback 类型记忆 |

> ⚠️ 如果安装了以上技能，请先卸载再安装 huo15-memory-evolution

### 10.2 可共存的技能

以下技能与 huo15-memory-evolution **互补**，可以共存：

| 技能 | 关系 | 说明 |
|------|------|------|
| **clever-compact** | 互补 | 会话压缩恢复，不处理长期记忆 |
| **context-optimizer** | 互补 | 上下文压缩优化，huo15 处理跨会话持久化 |
| **context-persistence** | 互补 | 跨会话持久化，与 huo15 记忆互补 |
| **proactive-agent** | 互补 | 主动 Agent，不涉及记忆管理 |
| **memory-hygiene** | 已替代 | 向量记忆清理，已被 check-drift.sh 替代 |

### 10.3 完整技能栈建议

```
必装（核心）：
✅ huo15-memory-evolution   - 记忆管理系统

可选（增强）：
✅ clever-compact           - 会话压缩
✅ context-optimizer        - 上下文优化
✅ proactive-agent          - 主动行为
✅ self-improving-agent     - 错误学习（已被 huo15 部分替代）
```

---

## 十一、相关链接

- **ClawHub**: https://clawhub.ai/jobzhao15/huo15-memory-evolution
- **源码仓库**: https://cnb.cool/huo15/openclaw-workspace

---

*火一五信息科技有限公司出品 | 参考 Claude Code 开源实现*
