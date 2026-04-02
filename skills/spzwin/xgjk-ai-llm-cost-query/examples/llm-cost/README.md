# llm-cost — 使用说明

## 什么时候使用

- **能力一**：用户查**自己的** AI 费用，或**只说「查询费用 / 查费用 / AI 费用 / token」而未点名他人**——一律视为当前登录用户（可带日期，默认当天）。**不要**为解析「当前用户」去调用户搜索接口，**不要**传 `personId`。
- **能力二**：仅当用户**明确要查另一名具体人员**（姓名等），在已通过 `cwork-user` 搜索并确认 **`personId`** 后，查询**他人**的费用（可带日期）。

## 标准流程

1. **鉴权预检**：按 `cms-auth-skills/SKILL.md` 准备 `appKey`。
2. **阅读文档**：`openapi/llm-cost/api-index.md` → `openapi/llm-cost/user-usage.md`。
3. **执行脚本**：
   - **能力一**：不传 `--person-id`；可按需传 `--start-time` / `--end-time`。
   - **能力二**：传入 `--person-id`（来自搜索脚本，**非用户口述**）；可按需传日期参数。
   - **向用户展示时**优先：`python3 scripts/llm-cost/user-usage.py ... --format markdown`，输出已为 Markdown 表格，可直接交付或稍作导语。
4. **输出结果**（成功且 `resultCode` 表示成功时）：
   - **版式**：以 **Markdown 表格** 为主（总览表 → 各产品小计表 → 各产品下模型明细表）；见 `SKILL.md`「呈现形式」。
   - **Token 数字**：优先使用 JSON 中的 `*Display` 字段（K / M）；见 `SKILL.md`「数字展示」。
   - **第一段 — 总览**：该用户在查询条件下的**输入 Token 合计**、**输出 Token 合计**（及总费用等若 `data` 有）。
   - **第二段起 — 按产品**：对每个产品先写**产品名**与**该产品小计**（输入/输出 Token 等），再在该产品下列出**各模型**及每模型的输入/输出 Token。
   - 产品之间依次排列；见 `SKILL.md`「查询结果呈现给用户」与 `openapi/llm-cost/user-usage.md` 的 `data` 层级说明。
   - 失败时向用户展示 `resultMsg`，不套用上述结构。

## 话术提示

- 「查我的费用」「查询费用」「查费用」「AI 花了多少」（未说查谁）→ **不调** `cwork-user`，直接 `user-usage.py`，**不传** `--person-id`。
- 「查张三的费用」→ 先 `cwork-user` 再 `user-usage.py`，全程不要求用户提供数字 ID。
