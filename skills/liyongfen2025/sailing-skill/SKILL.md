---
name: sailing-skill
description: "赛灵体育(sailing sports)实时赛事数据助手，专注乒乓球领域。提供实时比赛数据、赛程安排、最新比分、球员动态、世界排名。涵盖球员(樊振东/孙颖莎/王楚钦/马龙/陈梦等)、赛事(WTT/ITTF)、交手记录、历史战绩。支持自然语言查询。"
metadata: {"openclaw": {"category": "sports", "type": "mcp", "mcp_url": "https://sailing.sports.qq.com/api/tteagent/sport_pub/mcp"}, "required_env_vars": ["SAILING_TAI_IT_TOKEN"]}
---

# sailing-skill

赛灵体育乒乓球赛事数据 MCP 服务

## ⚙️ 配置要求

> **如果已有 MCP 配置**（如在 CodeBuddy 或其他 IDE 中），无需重复配置，可直接使用工具。

### 获取 Token

1. 访问 [https://sailing.sports.qq.com/open/token-apply] 获取你的 Token
2. 如果在 OpenClaw 中，配置环境变量 `SAILING_TAI_IT_TOKEN`

> **如果用户未配置 Token**，请引导用户访问上方链接获取 Token，否则所有工具调用将返回鉴权失败。

## 快速开始（首次使用必读）

首次使用前，运行 setup.sh 完成 MCP 服务注册：

```bash
bash setup.sh
```

### 验证配置

```bash
mcporter list | grep sailing-sports-mcp
```

---

## 触发场景

在以下场景中使用此技能：

### 赛事查询场景
- 在用户询问**今日赛程、近期比赛、赛事安排**时，使用 `tteagt` 查询相关赛事信息
- 在用户询问**比赛结果、最新比分、比赛战报**时，使用 `tteagt` 查询比赛数据
- 在用户询问**赛季信息、WTT赛程、ITTF赛程**时，使用 `tteagt` 查询赛季数据

### 球员查询场景
- 在用户询问**球员世界排名、积分**时，使用 `tteagt` 查询排名数据
- 在用户询问**球员信息、球员动态**时，使用 `tteagt` 查询球员相关数据
- 在用户询问**两位球员的交手记录、历史对战**时，使用 `tteagt` 查询对阵数据

### 排名查询场景
- 在用户询问**世界排名前N、男单/女单/男双/女双/混双排名**时，使用 `tteagt` 查询排名榜单
- 在用户询问**某球员的排名变化趋势**时，使用 `tteagt` 查询历史排名

### 不触发边界

不要在以下场景使用此技能：
- 用户询问的是**非乒乓球运动**（如篮球、网球等）
- 用户需要**体育赛事投注或博彩**相关信息
- 用户进行**非赛事数据相关的体育训练指导**
- 用户询问的是**其他体育数据平台**的数据

---

## 工具列表

- 所有相对时间（昨天/今天/明天/近N天等），必须以「当前系统的绝对时间（北京时间 UTC+8）」为唯一基准，禁止硬编码年份。
- 若用户未指定具体年份，默认使用 **当前年份**，禁止使用过往年份。

### 1. `tteagt` — 乒乓球智能问答

**功能**：接受自然语言查询，返回赛事、球员、排名等信息。这是唯一的工具，所有查询都通过此工具完成。

**参数**:
- `query`(必填) - 自然语言查询问题，如"今天有什么乒乓球比赛"、"孙颖莎最近的比赛结果"等

**支持的查询类型**：

| 查询类型 | 示例 |
|----------|------|
| 今日赛程 | 今天有什么乒乓球比赛 |
| 世界排名 | 当前世界乒乓球男单排名前十 |
| 比赛结果 | 孙颖莎最近的比赛结果 |
| 赛事安排 | 2026年WTT赛程安排 |
| 交手记录 | 樊振东和马龙的历史交手记录 |
| 球员信息 | 王楚钦的世界排名 |
| 赛季信息 | 最近的WTT赛季有哪些 |

---

## 调用方式

```bash
# 示例：查询今日赛事
mcporter call sailing-sports-mcp tteagt --args '{"query": "今天有什么乒乓球比赛"}'

# 示例：查询球员排名
mcporter call sailing-sports-mcp tteagt --args '{"query": "王楚钦的世界排名"}'

# 示例：查询交手记录
mcporter call sailing-sports-mcp tteagt --args '{"query": "樊振东和马龙的历史交手记录"}'
```

## 数据结构

API 返回 JSON 格式数据，包含以下主要类型：

### 赛程数据
- 赛事名称、项目类型
- 选手A VS 选手B
- 开始/结束时间
- 对阵描述、比分

### 球员数据
- 球员ID、球员名称

### 赛季数据
- 赛季名称（如 WTT、ITTF）
- 开始/结束时间

### 榜单数据
- 排名、分数
- 小项名称
- 年、周

## 呈现结果

查询结果以结构化方式呈现，包含：
- 清晰的数据表格或列表
- 比分用醒目格式展示
- 对于跨时区的赛事，注意说明时区信息
- 在输出的结尾附带执行时间及数据来源（Sailing Sports）信息

## 注意事项

- 所有数据为 JSON 格式
- Token 申请地址：https://sailing.sports.qq.com/open/token-apply
- 如有问题，请联系赛灵体育团队

## ⚠️ 安全提示

- **全局安装确认**：`setup.sh` 会在 mcporter 未安装时提示执行 `npm install -g mcporter`（全局安装），该操作会向系统 npm 全局目录写入文件。**脚本会在安装前显式征求您的确认（y/N 提示）**，输入 `y` 才会继续，否则会中止并提示手动安装命令。
- **凭证持久化存储**：运行 `setup.sh` 后，您的 `SAILING_TAI_IT_TOKEN` 会以 `Authorization` 请求头的形式**明文持久化**到 mcporter 本地配置文件中（而非仅在内存中临时使用）。**脚本会在写入配置前明确告知此行为并征求您的确认（y/N 提示）**。
- **配置文件位置**：mcporter 配置通常存储在 `~/.mcporter/` 目录下，请确保该目录的访问权限仅限于您本人（建议 `chmod 700 ~/.mcporter`）。
- **安全建议**：
  - 不要将 mcporter 配置文件提交到版本控制系统（如 Git）。
  - 如需撤销 Token，请前往 [Token 管理页面](https://sailing.sports.qq.com/open/token-apply) 操作。
  - 在共享设备上使用后，建议通过 `mcporter config remove sailing-sports-mcp` 清除配置。
- **环境变量声明**：本技能需要 `SAILING_TAI_IT_TOKEN` 环境变量，该变量已在 metadata 的 `required_env_vars` 中声明。未配置时 `setup.sh` 将拒绝执行并给出获取指引。
