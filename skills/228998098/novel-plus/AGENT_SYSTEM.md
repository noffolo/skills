# 小说写作技能 v2.4 - Agent 系统指南

## 概述

v2.4 版本引入完整的 **多智能体（Multi-Agent）协作系统**。主控（Coordinator）作为唯一与用户交互的 Agent，负责调度各个 Specialist Agent 完成专业任务。

## Agent 架构

```
                    ┌─────────────────────────────────────┐
                    │         用户 (User)                 │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │    Coordinator (主控) - M2.7        │
                    │  - 任务调度                         │
                    │  - 存档管理                         │
                    │  - 用户交互                         │
                    └─────────────────┬───────────────────┘
                                      │
          ┌───────────┬───────────┬───┴───┬───────────┬───────────┐
          ▼           ▼           ▼       ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │World-   │ │Character│ │Outline  │ │Chapter  │ │  Main   │ │   OOC   │
    │builder   │ │Designer │ │Planner  │ │Outliner │ │ Writer  │ │Guardian │
    │ Opus    │ │ Opus   │ │ Opus   │ │ Kimi    │ │ Kimi    │ │ Qwen    │
    └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
          │           │           │           │           │           │
          └───────────┴───────────┴───────────┴───────────┴───────────┘
                                      │
                          ┌───────────┴───────────┐
                          ▼                       ▼
                    ┌─────────┐            ┌─────────┐
                    │ Battle  │            │  Final  │
                    │ Agent   │            │Reviewer │
                    │ Gemini  │            │  Opus  │
                    └─────────┘            └─────────┘
                          │                       │
                          └───────────┬───────────┘
                                      ▼
                              ┌─────────────┐
                              │  Reader    │
                              │Simulator   │
                              │  Doubao    │
                              └─────────────┘
```

## Agent 职责表

| Agent | 模型 | 职责 | 调用时机 |
|-------|------|------|----------|
| **Coordinator** | M2.7 | 总控协调、任务分发、存档管理 | 始终运行 |
| **Worldbuilder** | Opus | 构建世界观 | Phase 1 Step 1 |
| **CharacterDesigner** | Opus | 创建角色圣经 | Phase 1 Step 2 |
| **OutlinePlanner** | Opus | 设计全书大纲 | Phase 1 Step 3 |
| **ChapterOutliner** | Kimi | 生成章节细纲（每批10章） | Phase 1 Step 4 |
| **StyleAnchorGenerator** | Opus | 生成风格锚定文档 | Phase 1 Step 7 |
| **MainWriter** | Kimi | 初稿+润色 | Phase 2 每章 |
| **OOCGuardian** | Qwen | 一致性检查 | 条件触发 |
| **BattleAgent** | Gemini | 高强度战斗 | 条件触发 |
| **FinalReviewer** | Opus | 终审 | 重点章节 |
| **ReaderSimulator** | Doubao | 读者反馈 | 每10章/用户请求 |
| **RollingSummarizer** | Qwen | 滚动摘要 | 每5-10章 |

## Agent 注册机制

### 注册时机

**Phase 0 初始化时自动注册所有 Agent**

用户说"新建小说"后，主控执行：

```
1. 创建项目目录结构
2. 初始化元数据文件
3. 从 manifest.json 读取 Agent 注册信息
4. 生成 agent-registry.json
5. 更新 metadata.json phase = 0
6. 汇报用户确认
```

### 注册表结构

```json
// meta/agent-registry.json
{
  "projectId": "novel-xxx",
  "registeredAgents": {
    "coordinator": {
      "id": "coordinator",
      "status": "active",
      "registeredAt": "2026-03-22"
    },
    "worldbuilder": {
      "id": "worldbuilder",
      "status": "available",
      "registeredAt": "2026-03-22",
      "taskCount": 0
    },
    ...
  }
}
```

### Agent 状态

| 状态 | 说明 |
|------|------|
| `available` | 空闲，可接受任务 |
| `busy` | 正在执行任务 |
| `offline` | 离线/不可用 |
| `active` | 主控Agent状态 |

## 调度流程

### 主控任务分发

主控接收任务后，按以下流程分发：

```
1. 解析任务类型
2. 选择合适的 Agent
3. 准备 Agent 输入（上下文、指令）
4. 调用 Agent
5. 接收并验证输出
6. 整合或继续分发
7. 更新存档
```

### Agent 调用示例

**Phase 1 世界观构建：**

```
用户：帮我设计世界观

Coordinator:
  1. 读取 manifest.json 中的 worldbuilder 配置
  2. 准备输入：
     - 项目基本信息
     - 用户授权边界
     - 特殊要求
  3. 调用 Worldbuilder Agent
  4. 接收输出：worldbuilding/world.md
  5. 更新 agent-registry.json (worldbuilder.taskCount++)
  6. 汇报用户
```

**Phase 2 章节写作：**

```
用户：写第5章

Coordinator:
  1. 判断章节类型（常规/重点）
  2. 读取存档（固定层+滚动层+按需层）
  3. 执行写前核查
  4. 调用 MainWriter Agent 生成初稿+润色
  5. [条件触发] 调用 OOCGuardian Agent
  6. 整合输出
  7. 更新存档
  8. [每5章] 调用 RollingSummarizer
  9. [每10章] 调用 ReaderSimulator
  10. 汇报用户
```

## 回退机制

当某 Agent 失败时，主控按以下顺序回退：

| 原 Agent | 回退目标 | 处理方式 |
|----------|----------|----------|
| MainWriter | OOCGuardian (Qwen) | 担任主笔+润色（合并） |
| FinalReviewer | Coordinator | 自行终审 |
| BattleAgent | MainWriter | 写战斗段落 |
| OOCGuardian | Coordinator | 自行自查 |
| ReaderSimulator | 跳过 | 不阻断写作 |

**回退记录格式：**

```markdown
## 回退记录 ChXX

| 时间 | Agent | 原任务 | 回退目标 | 结果 |
|------|-------|--------|----------|------|
| 2026-03-22 10:30 | MainWriter | 初稿 | OOCGuardian | 成功 |
```

## Agent 输入规范

每个 Agent 的 prompt 必须包含：

### 必要信息

1. **任务描述**：需要完成什么
2. **上下文**：相关的世界观、角色、大纲等
3. **输出要求**：格式、文件位置、质量标准
4. **约束条件**：敏感内容限制、风格要求等

### MainWriter 示例 Prompt

```
你是主笔智能体，负责章节写作。

【任务】
完成第5章的初稿和润色

【上下文】
- 世界观：见 worldbuilding/world.md
- 角色：见 characters/protagonist.md, characters/characters.md
- 风格锚定：见 meta/style-anchor.md (v1.0)
- 本章细纲：见 outline/chapter-outline.md 第5章
- 上章结尾：[摘要]

【输出要求】
- 直接输出可交付的章节正文
- 字数：4000字（允许3000-6000）
- 格式：标题 + 正文 + 字数说明

【约束】
- 遵循风格锚定文档
- 角色不得OOC
- 禁止R18内容
- 敏感场景：含蓄隐晦
```

## 质量保障

### 主控职责

1. **输入验证**：确保传递给 Agent 的信息完整准确
2. **输出验证**：检查 Agent 输出是否符合要求
3. **一致性检查**：确保各 Agent 输出之间无矛盾
4. **风格统一**：最终整合时保持风格一致

### Agent 协作检查点

| 阶段 | 检查点 |
|------|--------|
| Phase 0 | 所有 Agent 注册完成 |
| Phase 1 | Worldbuilder → CharacterDesigner → OutlinePlanner 输出衔接 |
| Phase 2 | MainWriter 输出符合风格锚定 |
| Phase 2 | OOCGuardian 发现问题被正确修复 |
| Phase 2 | FinalReviewer 通过后章节定稿 |

## 常见问题

### Q: Agent 返回不符合预期怎么办？

A: 主控进行以下处理：
1. 判断问题严重程度
2. 轻微问题：主控自行修正
3. 严重问题：重新调用同一 Agent 并提供更明确的指令
4. 持续失败：按回退链尝试其他 Agent

### Q: 两个 Agent 输出矛盾怎么办？

A: 按优先级处理：
1. 角色圣经 > 世界观 > 大纲 > 细纲
2. 主控有权根据更高优先级文档修正矛盾
3. 修正后记录到 archive.md

### Q: 如何监控 Agent 状态？

A: 通过 agent-registry.json 监控：
- `status`: 当前状态
- `taskCount`: 累计任务数
- `lastUsed`: 最后使用时间
