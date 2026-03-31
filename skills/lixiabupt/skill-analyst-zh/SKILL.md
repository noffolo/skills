---
name: skill-analyst-zh
description: 在安装或发布 OpenClaw skill 之前进行分析评估。对比已安装或 ClawHub 上的同类 skill，检查功能重叠，进行安全审查，给出明确的安装/发布建议。使用场景：用户想评估某个 skill 是否值得安装、对比 ClawHub 上的同类 skill、检查本地 skill 是否达到发布标准。触发词："分析 skill-name"、"评估安装/发布某某技能"、"这个skill值得装吗"、"能发布吗"、"skill对比"。
---

# 技能分析师

分析员模式：在你安装或发布 skill 之前，帮你分析、对比、把关。

## 前置条件

- `clawhub` CLI 可用（用于搜索和查看详情）
- `skill-vetter` 可选（用于安全审查）

## 工具

两个辅助脚本位于 `scripts/` 目录：

```
node <skill目录>/scripts/analyst-search.mjs <关键词> [--limit N]
node <skill目录>/scripts/analyst-inspect.mjs <skill名称> [--files]
```

两者均输出结构化 JSON。

## 工作流：安装评估

触发："分析安装 <skill名称>" 或 "这个skill值得装吗"

### 第一步：侦察目标

```
node scripts/analyst-search.mjs "<skill名称>"
node scripts/analyst-inspect.mjs "<最佳匹配>"
```

获取：名称、作者、版本、简介、许可证、最近更新时间。

### 第二步：查看已安装 skill

```
clawhub list
```

或扫描 skills 目录下的 SKILL.md 文件。

### 第三步：查找重叠

将目标 skill 的简介和描述与已安装 skill 进行对比：

- 搜索功能关键词或用途重叠的 skill
- 评估重叠程度：高(HIGH) / 中(MEDIUM) / 低(LOW) / 无(NONE)
- 标注关键差异

### 第四步：安全检查（可选）

如果已安装 `skill-vetter`，对目标运行安全审查。

如果未安装，标注"安全审查已跳过"。

### 第五步：生成报告

```
## 🔍 分析报告：安装 <skill名称>

### 概览
| 字段 | 值 |
|------|-----|
| 名称 | ... |
| 作者 | ... |
| 版本 | ... |
| 许可证 | ... |
| 更新时间 | ... |

### 与已安装 Skill 的重叠
- skill-a：中(MEDIUM) — 用途相似但方法不同
- skill-b：无(NONE) — 不相关

### 独特价值
- 功能 X（没有任何已安装 skill 覆盖）
- 相比 skill-z 的改进点 Y

### 风险
- 需要 Z 的 API 密钥
- 3个月未更新

### 结论
✅ 推荐安装 — 独特价值，安全可靠
⚠️ 考虑安装 — 有顾虑，建议先了解 X
❌ 不推荐 — 与 skill-a 重复
```

## 工作流：发布评估

触发："分析发布 <skill名称>" 或 "能发布吗"

### 第一步：读取本地 skill

从工作区或 skills 目录读取 SKILL.md。

提取：名称、描述、功能概要、文件列表。

### 第二步：搜索竞品

```
node scripts/analyst-search.mjs "<skill名称>"
node scripts/analyst-search.mjs "<描述中的关键词>"
```

使用 2-3 个不同关键词搜索，确保不遗漏。

### 第三步：分析竞品

对每个相关结果：

```
node scripts/analyst-inspect.mjs "<竞品>"
```

对比：功能覆盖、版本成熟度、更新频率、独特性。

### 第四步：生成报告

```
## 🔍 分析报告：发布 <skill名称>

### 你的 Skill
| 字段 | 值 |
|------|-----|
| 名称 | ... |
| 文件数 | ... |
| 描述 | ... |

### ClawHub 上的竞品
| Skill | 作者 | 版本 | 重叠度 | 更新时间 |
|-------|------|------|--------|----------|
| ... | ... | ... | 高/中/低 | ... |

### 你的优势
- 与竞品的关键差异
- 你填补的空白

### 改进建议
- 发布前建议增加 X
- 考虑 Y 以提升可用性

### 结论
✅ 可以发布 — 独特贡献，准备就绪
⚠️ 先优化再发布 — 需改进 X
❌ 重新考虑 — 与现有 skill 过于相似，建议为其贡献
```

## 配置

编辑 `config.json` 自定义评估参数：

```json
{
  "searchLimit": 8,           // 每次搜索最大结果数
  "overlapThresholds": {      // 重叠分级阈值
    "high": 0.7,
    "medium": 0.4,
    "low": 0.2
  },
  "securityRequired": false,  // 是否强制安全审查
  "securitySkill": "skill-vetter"
}
```

## 输出规范

- 始终使用表格进行结构化对比
- 分析简洁，以可操作性为导向
- 以明确结论收尾（推荐/观望/跳过/可发布/先优化/重新考虑）
- 使用以上报告模板，不要自由发挥
