---
name: iran-war-tracker
version: 1.0.1
description: 伊朗动态播报 | Iran War Tracker - 当用户说"伊朗播报"、"伊朗局势"、"伊朗动态"、"美以伊"、"霍尔木兹"、"Iran situation"、"Iran war"、"Middle East conflict"时触发。Track Iran conflict developments with Tavily news search, CLS Telegraph fast news, and risk asset monitoring for BTC, gold, WTI crude, natural gas, and Nasdaq futures. Use when user needs a structured Iran situation report covering war intensity, Hormuz Strait status, energy supply changes, leader statements, risk assets, and trading clues.
---

# 伊朗动态播报 / Iran War Tracker

> 🎉 **安装成功！** 本技能已就绪，可直接使用。

## 🚀 立即使用

直接输入以下任一触发词即可获取最新伊朗局势分析报告：

| 触发词 | 示例 |
|--------|------|
| 伊朗播报 | "来一份伊朗播报" |
| 伊朗局势 | "查一下伊朗局势" |
| 伊朗动态 | "看看伊朗动态" |
| 美以伊 | "美以伊最新情况" |
| 霍尔木兹 | "霍尔木兹海峡怎么样" |

**英文触发词**: `Iran tracker`, `Iran war`, `Iran situation`, `Middle East conflict`, `Hormuz Strait`

---

### 💡 使用示例

**方式一：直接说出触发词（推荐）**
```
用户: 伊朗播报
→ 系统自动生成完整局势分析报告
```

**方式二：命令行运行**
```bash
# 进入技能目录后执行
python scripts/iran_tracker.py

# 输出到文件
python scripts/iran_tracker.py --output report.md
```

---

### 📊 报告内容包含

- 🔥 **战争烈度评估** - 当前战事等级与变化趋势
- ⚔️ **局势进展** - 美、以、伊三方动态汇总
- 🛢️ **油气分析** - 霍尔木兹海峡风险与能源供应
- 💹 **风险资产** - BTC、黄金、原油、天然气、纳指期货
- 💡 **交易线索** - 操作建议与风险提示
- 📑 **情景推演** - 基准/升级/缓和三种情景

---

## 简介 / Introduction

本技能用于生成结构化的伊朗局势分析报告，关注战争动态、霍尔木兹海峡通航状况、油气供应风险及市场反应。

This skill generates structured Iran situation reports focused on war developments, Hormuz Strait status, oil and gas supply risk, and market reactions.

---

## 快速开始 / Quick Start

在技能目录下运行：

```bash
python scripts/iran_tracker.py
```

输出到文件：

```bash
python scripts/iran_tracker.py --output latest-report.md
python scripts/iran_tracker.py --output latest-report.md --json-output latest-report.json
```

### 搜索模式选项 / Search Mode Options

```bash
# OpenClaw 环境：优先使用模型搜索（默认）
python scripts/iran_tracker.py

# 显式优先模型搜索
python scripts/iran_tracker.py --prefer-model-search

# 强制使用 Tavily 搜索
python scripts/iran_tracker.py --force-tavily
```

---

## 工作流程 / Workflow

1. **新闻搜索**（按优先级）：
   - **OpenClaw 环境**：优先使用当前模型的搜索能力（AutoGLM/WebSearch）
   - **降级方案**：Tavily API 搜索以下固定主题：
     - 战争局势更新 / war situation updates
     - 霍尔木兹海峡关闭、通航、油轮及袭船事件 / Hormuz Strait closure, transit, tanker, ship attacks
     - 石油供应、出口、制裁及产量变化 / oil supply, exports, sanctions, production
     - 天然气供应、LNG、基础设施及出口变化 / natural gas supply, LNG, infrastructure, exports
     - 领导人、外交官及军方表态 / leader, diplomat, military statements

2. 爬取财联社(CLS Telegraph)快讯

3. 从 Stooq 获取风险资产数据，BTC 使用 CoinGecko 作为降级

4. 在撰写结论前加载本地框架 Markdown 文件

5. 生成中文报告，使用框架解释从战争升级到油气、通胀和风险资产的传导路径

---

## 强制分析规则 / Mandatory Analysis Rules

报告生成时必须遵守以下规则（非风格建议，而是硬性要求）：

- 必须先加载并使用本地框架 Markdown 文件。如无法加载，需明确说明框架加载失败并降低置信度。
- 不能仅停留在事件总结。每个部分都需要证据加解读。
- 必须分开分析石油和天然气，不能合并成笼统的"能源"段落。
- 必须解释以下传导路径：
  - 冲突烈度 → 霍尔木兹通航风险 → 油轮及航运成本 → 石油供应预期
  - 打击或制裁 → 生产/出口中断 → 油价重新定价
  - 天然气设施、LNG 或区域基础设施风险 → 天然气供应预期
  - 能源价格冲击 → 通胀和增长压力 → 黄金、BTC、纳指期货
- 必须区分：
  - 确认的事实
  - 市场定价信号
  - 推断或情景判断
- 必须包含情景分析，而非仅当前状态分析。

---

## 报告结构 / Output Structure

生成报告必须为中文，并包含以下部分。每个部分都应内容充实，而非一句话总结。

### 📊 战争烈度评估 / War Intensity Assessment

```
═══════════════════════════════════════════════════════════════

🔥 美以伊动态播报 | YYYY-MM-DD HH:00 🔥

═══════════════════════════════════════════════════════════════

### 📊 【战争烈度评估】/ War Intensity Assessment
X级（🔺上升/🔻下降/➡️持平）/ Level X (Rising/Falling/Stable)
- 当前态势简述 / Current situation summary
- 关键变化点 / Key changes
```

### ⚔️ 局势进展 / Situation Updates

```
───────────────────────────────────────────────────────────────

### ⚔️ 【局势进展】/ Situation Progress

▸ 🇺🇸 美国汇总 / US Summary
- 🎯 军事行动 / Military Actions:
- 🎤 领导人表态 / Leader Statements:
- 📌 其他动态 / Other Updates:

▸ 🇮🇱 以色列汇总 / Israel Summary
- 🎯 军事行动 / Military Actions:
- 🎤 领导人表态 / Leader Statements:
- 📌 其他动态 / Other Updates:

▸ 🇮🇷 伊朗汇总 / Iran Summary
- ⚡ 反击行动 / Retaliation Actions:
- 🎤 领导人表态 / Leader Statements:
- 📌 其他动态 / Other Updates:

▸ 📈 边际变化评估 / Marginal Change Assessment
├─ 🔴 战争扩大信号 / Escalation Signals:
│  • 空袭烈度/频次是否加大 / Airstrike intensity/frequency:
│  • 地面进攻迹象 / Ground operation signs:
│  • 新参战方动态 / New participants:
├─ 🟢 战争缓和信号 / De-escalation Signals:
│  • 谈判信号 / Negotiation signals:
│  • 停火提议 / Ceasefire proposals:
│  • 外交斡旋 / Diplomatic mediation:
└─ 🚢 霍尔木兹海峡封锁 / Hormuz Strait Blockade:
   • 通航状态 / Transit status:
   • 袭船事件 / Ship attacks:
   • 船只动态 / Vessel movements:
```

### 🛢️ 油气分析 / Oil & Gas Analysis

1. **原油 / Crude Oil**: 聚焦霍尔木兹、航运、出口、制裁、产量、炼厂及油轮风险
2. **天然气 / Natural Gas**: 聚焦设施、出口、LNG、区域基础设施，以及冲击是即期、区域性还是全球性
3. **分析框架映射 / Framework Mapping**: 明确将当前证据映射到本地框架维度
4. **宏观传导 / Macro Transmission**: 解释通胀、增长和政策敏感性

### 💹 风险资产波动 / Risk Asset Fluctuations

覆盖 BTC、黄金、WTI 原油、天然气和纳指期货。说明价格变动是证实还是反驳地缘叙事。

### 💡 交易线索 / Trading Clues

```
### 💡 【交易线索】/ Trading Clues

🎯 核心判断 / Core Judgment:
（基于当前边际变化给出明确的交易方向判断）

📋 操作建议 / Trading Recommendations:
• 🛢️ 原油 / Crude Oil: 看多/看空/观望，逻辑... / Bullish/Bearish/Neutral, rationale...
• ⚡ 能源替代 / Energy Alternatives: 看多/看空/观望，逻辑... / Bullish/Bearish/Neutral, rationale...
• 📊 AI科技 / AI Tech: 看多/看空/观望，逻辑... / Bullish/Bearish/Neutral, rationale...

⚠️ 风险提示 / Risk Warnings:
```

### 📑 情景推演 / Scenario Analysis

- **基准情景 / Base Case**
- **升级情景 / Escalation Case**
- **缓和情景 / De-escalation Case**

### 📋 证据与数据源状态 / Evidence & Data Sources

- 提及 Tavily 主题覆盖
- 提及 CLS 快讯覆盖
- 说明框架是否成功加载

---

## 细节下限 / Detail Floor

为避免较弱模型生成浅层输出，强制执行最低细节标准：

- `战事烈度评估` 至少 3 个要点
- `局势进展` 中美国、以色列、伊朗各方至少 2 个要点
- `油气分析` 中原油和天然气各至少 4 个要点
- `风险资产波动` 至少 5 个要点
- `交易线索分析` 至少 4 个要点
- `情景推演` 至少 3 个情景

如证据稀疏，说明证据稀疏，但仍需使用谨慎推断完成完整结构，而非缩短报告。

---

## 数据源 / Data Sources

### 新闻搜索（按优先级）/ News Search (Priority Order)

1. **模型搜索 / Model Search** (OpenClaw 环境)
   - 通过 `OPENCLAW_ENV`、`KIMI_API_KEY` 或 `AGENT_ENV` 环境变量自动检测
   - 支持 AutoGLM WebSearch MCP 端点

2. **Tavily Search API**
   - 高质量新闻搜索 API
   - 需要 `TAVILY_API_KEY` 环境变量

3. **DuckDuckGo Lite**
   - 免费网页搜索（无需 API key）
   - 当上述方法失败时自动作为降级方案
   - 通过 DuckDuckGo Lite HTML 界面搜索

### 其他数据源 / Other Data Sources

- 财联社(CLS Telegraph)快讯爬虫
- Stooq 市场数据端点
- CoinGecko BTC 降级端点
- 技能根目录本地框架 Markdown

---

## 环境变量 / Environment Variables

```bash
# Tavily 搜索所需（如不使用模型搜索）
TAVILY_API_KEY=tvly-...

# 可选：OpenClaw 环境检测（任一设置即自动检测）
OPENCLAW_ENV=1
KIMI_API_KEY=...        # 自动检测为 OpenClaw 环境
AGENT_ENV=openclaw      # 自动检测为 OpenClaw 环境

# 可选：自定义模型搜索端点（如不使用默认）
OPENCLAW_SEARCH_URL=http://127.0.0.1:53699/search
OPENCLAW_API_KEY=...    # 如搜索端点需要认证
```

---

## 维护规则 / Maintenance Rules

- 情报主题保持不变，除非报告范围发生变化。
- 使用捆绑的 CLS 爬虫方法作为 CLS 快讯的标准来源。
- 如 Stooq 失败，BTC 降级到 CoinGecko。
- **搜索优先级**：模型搜索(OpenClaw) → Tavily API → DuckDuckGo(免费降级)。
- Tavily 配额耗尽或 API 不可用时自动使用 DuckDuckGo。
- 通过编辑 `scripts/iran_tracker.py` 扩展报告，但需保留要求的主题覆盖、框架加载及详细的油气分析。

---

## 触发词 / Trigger Keywords

**中文触发词 / Chinese Triggers:**
- 伊朗播报
- 伊朗局势
- 伊朗动态
- 美以伊
- 霍尔木兹
- 伊朗战争

**英文触发词 / English Triggers:**
- Iran tracker
- Iran war
- Iran situation
- Middle East conflict
- Hormuz Strait
- Israel Iran war
