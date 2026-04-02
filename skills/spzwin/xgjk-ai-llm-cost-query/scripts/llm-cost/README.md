# 脚本清单 — llm-cost

## 共享依赖

无（标准库 + 环境变量 `appKey`）。

## 脚本列表

| 脚本 | 对应接口 | 用途 |
|---|---|---|
| `user-usage.py` | `GET /open-api/llm-cost/user-usage` | 查询当前用户或指定 `personId` 的 AI 使用明细 |

## 使用方式

```bash
export XG_BIZ_API_KEY="your-app-key"
# 或 export XG_APP_KEY="your-app-key"

# 能力一：当前用户、默认当天（不传 personId 与日期）
python3 scripts/llm-cost/user-usage.py

# 指定日期范围
python3 scripts/llm-cost/user-usage.py --start-time 2026-04-01 --end-time 2026-04-07

# 仅输出 Markdown 表格（便于直接贴给用户；推荐）
python3 scripts/llm-cost/user-usage.py --format markdown
python3 scripts/llm-cost/user-usage.py --format markdown --start-time 2026-04-01 --end-time 2026-04-07

# 能力二：指定 personId（由 Agent 从搜索接口得到，非用户口述）
python3 scripts/llm-cost/user-usage.py --person-id 20001 --start-time 2026-04-01 --end-time 2026-04-07
```

## 输出说明

默认 `--format json`：输出 **JSON**（`Result<T>`）。`user-usage.py` 会在 `data` 内为名称含 `token` 的数值字段附加 `字段名Display`（K/M）。**向用户展示时推荐** `--format markdown`：仅输出 **Markdown 表格**（查询条件、用户总览、各产品小计、各模型明细），无须再手工排版。若仍用 JSON，Agent 须按 `SKILL.md` 自行排成 Markdown 表格。

## 规范

1. **必须使用 Python** 编写
2. **鉴权遵循** `cms-auth-skills/SKILL.md` 规范
3. **入参定义以** `openapi/llm-cost/` 文档为准
4. 出错时**间隔 1 秒、最多重试 3 次**（可重试错误）
