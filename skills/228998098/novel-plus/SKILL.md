# 小说写作技能包 (novel-plus)

## 版本

**v2.4** - 多智能体协作版

## 描述

这是一个完整的小说写作技能包，采用 **多智能体（Multi-Agent）协作架构**。主控（Coordinator）统一调度各专业 Agent，覆盖项目初始化、世界观构建、角色圣经、大纲细纲、章节协作写作、审核迭代全生命周期。

## 核心特性

- **多 Agent 协作**：12 个专业 Agent，各司其职
- **自动注册**：Phase 0 初始化时自动注册所有 Agent
- **智能调度**：主控根据任务类型自动分发
- **自动推进**：支持连续写作 n 章，减少人工干预
- **完整存档**：版本化管理，可追溯

## 激活关键词

| 关键词 | 激活阶段 |
|--------|----------|
| "新建小说" / "新项目" | Phase 0 |
| "开始写小说" / "创建小说" | Phase 0（引导） |
| "世界观" / "设定" | Phase 1 Step 1 |
| "角色" / "人物" | Phase 1 Step 2 |
| "大纲" / "章节规划" | Phase 1 Step 3-4 |
| "审核大纲" / "检查架构" | Phase 1 Step 5 |
| "写第X章" / "写第X到Y章" | Phase 2 |
| "写第X章，自动推进N章" | Phase 2（自动推进） |
| "读者反馈" | Phase 2（立即触发读者模拟） |
| "继续写作" / "停止写作" | Phase 2（恢复/停止自动推进） |
| "重写第X章" / "重写第X章第Y段" | Phase 3 |
| "修改" / "补设定" | Phase 3 |

## 目录结构

```
novel-plus/
├── manifest.json              # 技能包元数据配置（含Agent注册信息）
├── instructions.md            # 完整技能指令（v2.4）
├── AGENT_SYSTEM.md           # Agent系统指南
├── README.md                 # 本说明文件
├── agents/                   # Agent定义目录
│   ├── coordinator.md        # 主控协调
│   ├── worldbuilder.md       # 世界观构建
│   ├── character-designer.md # 角色设计
│   ├── outline-planner.md    # 大纲规划
│   ├── chapter-outliner.md   # 章节细纲
│   ├── main-writer.md        # 主笔
│   ├── ooc-guardian.md       # OOC守护
│   ├── battle-agent.md       # 战斗写作
│   ├── final-reviewer.md     # 终稿审核
│   ├── reader-simulator.md   # 读者模拟
│   ├── style-anchor-generator.md  # 风格锚定生成
│   └── rolling-summarizer.md # 滚动摘要
├── references/               # 参考模板目录
│   └── ...
└── templates/                # 项目模板目录
    └── project-template/      # 完整项目模板
```

## Agent 架构

```
                        ┌─────────────────┐
                        │      用户       │
                        └────────┬────────┘
                                 │
                                 ▼
                   ┌─────────────────────────┐
                   │   Coordinator (主控)    │
                   │      MiniMax M2.7       │
                   │  - 任务调度              │
                   │  - 存档管理              │
                   │  - 用户交互              │
                   └───────────┬─────────────┘
                               │
        ┌──────────┬──────────┼──────────┬──────────┐
        ▼          ▼          ▼          ▼          ▼
   ┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐
   │World-   ││Character││Outline  ││Chapter  ││  Main   │
   │builder  ││Designer ││Planner  ││Outliner ││ Writer  │
   │(Opus)   ││(Opus)   ││(Opus)   ││(Kimi)   ││(Kimi)   │
   └─────────┘└─────────┘└─────────┘└─────────┘└─────────┘
        │          │          │          │          │
        └──────────┴──────────┴──────────┴──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
              ┌─────────┐          ┌─────────┐
              │ Battle  │          │  Final  │
              │ Agent   │          │Reviewer │
              │(Gemini) │          │ (Opus)  │
              └─────────┘          └─────────┘
```

## 使用方法

### 作为 OpenClaw Skill 使用

1. 将此目录复制到 OpenClaw 的 skills 目录
2. 在 OpenClaw 配置中注册此 skill
3. 使用激活关键词（如"新建小说"）开始对话

## 项目目录结构

```
projects/<项目名>/
├── meta/
│   ├── project.md          # 项目元数据
│   ├── metadata.json       # 统一元数据
│   ├── config.md          # 模型分工配置
│   ├── style-anchor.md    # 风格锚定文档
│   └── agent-registry.json # Agent注册表（v2.4新增）
├── worldbuilding/
│   └── world.md           # 世界观文档
├── characters/
│   ├── protagonist.md     # 主角档案
│   └── characters.md      # 其他角色
├── outline/
│   ├── outline.md         # 全书大纲
│   └── chapter-outline.md # 章节细纲
├── chapters/
│   ├── ch01.md           # 当前最新版
│   └── history/          # 历史版本
├── archive/
│   ├── archive.md        # 项目日志
│   └── reader-feedback/  # 读者反馈
└── references/
    └── ...
```

## 生命周期阶段

```
Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 3
  │           │           │           │
初始化     前期架构     章节写作    维护迭代
```

### Phase 0：新建项目初始化

- 收集核心设定
- 创建项目目录树
- **自动注册所有 Agent 到 agent-registry.json**
- 初始化元数据文件

### Phase 1：前期架构阶段

- **Worldbuilder** 构建世界观
- **CharacterDesigner** 创建角色圣经
- **OutlinePlanner** 设计全书大纲
- **ChapterOutliner** 生成章节细纲
- **StyleAnchorGenerator** 生成风格锚定文档

### Phase 2：章节写作阶段

- **MainWriter** 主笔写作
- **OOCGuardian** 条件触发一致性检查
- **BattleAgent** 高强度战斗场面
- **FinalReviewer** 重点章节终审
- **RollingSummarizer** 每5-10章更新摘要
- **ReaderSimulator** 每10章读者反馈

### Phase 3：维护与迭代

- 章节/段落重写
- 补设定/世界观扩展
- 修改大纲
- 风格调整

## Agent 职责表

| Agent | 模型 | 职责 | 调用时机 |
|-------|------|------|----------|
| Coordinator | M2.7 | 总控协调 | 始终运行 |
| Worldbuilder | Opus | 世界观构建 | Phase 1 |
| CharacterDesigner | Opus | 角色设计 | Phase 1 |
| OutlinePlanner | Opus | 大纲规划 | Phase 1 |
| ChapterOutliner | Kimi | 章节细纲 | Phase 1 |
| MainWriter | Kimi | 初稿+润色 | Phase 2 |
| OOCGuardian | Qwen | 一致性检查 | 条件触发 |
| BattleAgent | Gemini | 高强度战斗 | 条件触发 |
| FinalReviewer | Opus | 终审 | 重点章节 |
| ReaderSimulator | Doubao | 读者反馈 | 每10章 |
| StyleAnchorGenerator | Opus | 风格文档 | Phase 1 |
| RollingSummarizer | Qwen | 滚动摘要 | 每5-10章 |

## 核心铁律（优先级降序）

1. **P0 用户边界违规**（绝对禁止）
2. **P1 人设崩坏/OOC**（严格禁止）
3. **P2 设定逻辑冲突**（必须修复）
4. **P3 风格偏离**（应当修复）
5. **P4 节奏字数偏差**（优化项）

## 自动推进参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| auto_advance_chapters | 4 | 一次自动写4章 |
| write_interval_seconds | 6 | 每章完成后等待秒数 |
| auto_confirm | false | 是否自动确认继续 |

## 文档说明

| 文档 | 说明 |
|------|------|
| `manifest.json` | 技能包配置，包含 Agent 注册信息 |
| `instructions.md` | 完整技能指令（详细流程） |
| `AGENT_SYSTEM.md` | Agent 系统指南（调度机制、回退策略） |
| `agents/*.md` | 各 Agent 的定义和 Prompt |
| `references/*.md` | 模板文件 |
| `templates/` | 项目模板 |

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0 | 2026-03-21 | 初始Phase架构版 |
| v2.1 | 2026-03-21 | 优化读者模拟、滚动摘要等 |
| v2.2 | 2026-03-21 | 新增自动推进机制 |
| v2.3 | 2026-03-21 | 优化常规章节调用次数 |
| **v2.4** | 2026-03-22 | **新增多Agent协作系统，自动注册机制** |
