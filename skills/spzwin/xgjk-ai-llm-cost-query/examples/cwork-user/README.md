# cwork-user — 使用说明

## 什么时候使用

- 用户要**查询某位同事的 AI 费用**，且只提供了**对方姓名**（可选自然语言日期）。
- 需要先解析 **`personId`**，再与 `llm-cost` 模块配合。

## 标准流程

1. **鉴权预检**：按 `cms-auth-skills/SKILL.md` 准备 `appKey`（`XG_BIZ_API_KEY` 或 `XG_APP_KEY`）。
2. **阅读文档**：`openapi/cwork-user/api-index.md` → `openapi/cwork-user/search-emp-by-name.md`。
3. **执行脚本**：`scripts/cwork-user/search-emp-by-name.py --search-key "<姓名>"`。
4. **解析结果**：从 `data.inside.empList[]` 读取 `personId` 与 `name`。
5. **歧义处理**：
   - **0 条**：提示用户核对姓名或更换关键词；**不要**要求用户输入 `personId`。
   - **多条**：列出候选（姓名、部门等），请用户确认一条后再继续。
6. **下一步**：用确认的 `personId` 调用 `scripts/llm-cost/user-usage.py`（见 `examples/llm-cost/README.md`）。

## 说明

默认以 `inside.empList` 为主进行候选展示；是否与 `outside` 联系人联动由业务决定，本 Skill 未强制。
