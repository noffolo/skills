---
name: AI费用查询
description: >-
  查询当前登录用户或指定姓名员工的 AI 费用与 Token 用量。
  「查我的费用 / 查询费用 / 查 AI 费用」等未点名他人时，一律视为查当前用户：只调 llm-cost 脚本且不传 personId，不调用户搜索。
  仅当用户明确要查某个具体姓名/同事时，才先按姓名搜索再查用量。
skillcode: xgjk-ai-llm-cost-query
dependencies:
  - cms-auth-skills
---

# AI 费用查询 — 索引

本文件提供**能力宪章 + 能力树 + 按需加载规则**。详细参数与流程见各模块 `openapi/` 与 `examples/`。

**当前版本**: v0.1

**接口版本**: 业务接口统一使用 `https://sg-al-cwork-web.mediportal.com.cn/open-api/` 前缀；所有接口鉴权类型为 `appKey`（见各模块 `openapi/<module>/<endpoint>.md`）。

**能力概览（2 块能力）**：

- **能力一 — 查询我的费用 / 未指定对象的费用**：当前登录用户在指定日期范围内的 AI 费用明细（汇总与按产品/模型）。**凡未出现具体他人姓名（或明确「查某某」）的请求，全部走能力一**——包括「查询费用」「查费用」「我的费用」「AI 花了多少」等泛化说法。
- **能力二 — 查询他人费用**：仅当用户明确给出**对方姓名或可识别的具体对象**（及可选日期）时启用；先通过用户服务按姓名搜索得到 `personId` 并经用户确认（多候选时），再查询该用户的费用。**不向终端用户索取 `personId`。**

统一规范：

- 认证与鉴权：`cms-auth-skills/SKILL.md`
- 通用约束：`cms-auth-skills/SKILL.md`

授权依赖：

- 当接口声明需要 `appKey` 或 `access-token` 时，先尝试读取 `cms-auth-skills/SKILL.md`
- 如果已安装，直接按 `cms-auth-skills/SKILL.md` 中的鉴权规则准备对应 `appKey` 或 `access-token`
- 如果未安装，先执行 `npx clawhub@latest install cms-auth-skills --force`
- 如果上面的安装方式不可用，再执行 `npx clawhub@latest install https://github.com/spzwin/cms-auth-skills.git --force`
- 安装完成后，再继续执行需要鉴权的操作

输入完整性规则（强制）：

1. **能力一**：可不传对象与时间则默认为当前用户与当天（由接口约定）；若用户给出日期，须归一为 `YYYY-MM-DD` 的起止或单日。**不要传 `personId`，不要调用 `cwork-user` / `search-emp-by-name.py`，不要为「推断当前用户是谁」去查人员接口。**
2. **能力二**：仅当用户明确要查**另一名具体人员**（姓名等）时适用；用户只提供**姓名**与可选日期；必须先执行 `cwork-user` 搜索脚本，在 0 条或多条候选时与用户交互后再执行 `llm-cost` 费用脚本；禁止要求用户口述或输入 `personId`。

**意图判定（强制，先于脚本）**

- 属于能力一（只跑 `scripts/llm-cost/user-usage.py`，**省略 `--person-id`**）：含「我的 / 我本人 / 查询费用 / 查费用 / AI 费用 / token 费用 / 花了多少」等，且**未出现**他人姓名或「帮查某某」类指向。
- 属于能力二：用户明确说了**具体姓名或同事**（如「张三的费用」），才允许调用 `cwork-user` 搜索。

建议工作流（简版）：

1. 读取 `SKILL.md` 与 `cms-auth-skills/SKILL.md`，明确能力范围、鉴权与安全约束。
2. 识别用户意图：**未点名他人 → 一律按查自己**，仅打开 `llm-cost`，直接执行 `user-usage.py`（不传 `--person-id`）。**仅当**用户明确给出他人姓名时 → 先 `cwork-user`，再 `llm-cost`。打开对应模块的 `openapi/<module>/api-index.md`。
3. 确认具体接口后，加载 `openapi/<module>/<endpoint>.md` 获取入参/出参/Schema。
4. 补齐用户必需输入（能力二：姓名；多候选时列出 `empList` 供用户确认）。
5. 参考 `examples/<module>/README.md` 组织话术与流程。
6. **执行对应脚本**：调用 `scripts/<module>/<endpoint>.py`。**所有接口调用必须通过脚本执行，不允许跳过脚本直接调用 API。**

脚本使用规则（强制）：

1. **每个接口必须有对应脚本**：每个 `openapi/<module>/<endpoint>.md` 都必须有对应的 `scripts/<module>/<endpoint>.py`。
2. **脚本可独立执行**：所有 `scripts/` 下的脚本均可脱离 AI Agent 直接在命令行运行。
3. **先读文档再执行**：执行脚本前，**必须先阅读对应模块的 `openapi/<module>/api-index.md`**。
4. **入参来源**：脚本的所有入参定义与字段说明以 `openapi/` 文档为准。
5. **鉴权一致**：涉及鉴权时，统一依赖 `cms-auth-skills/SKILL.md`。

意图路由与加载规则（强制）：

1. **先路由再加载**：必须先判定模块，再打开该模块的 `api-index.md`。
2. **先读文档再调用**：在描述调用或执行前，必须加载对应接口文档。
3. **脚本必须执行**：所有接口调用必须通过脚本执行，不允许跳过。
4. **不猜测**：若意图不明确，必须追问澄清。

宪章（必须遵守）：

1. **只读索引**：`SKILL.md` 只描述「能做什么」和「去哪里读」，不写具体接口参数表。
2. **按需加载**：默认只读 `SKILL.md` + `cms-auth-skills/SKILL.md`，只有触发某模块时才加载该模块的 `openapi`、`examples` 与 `scripts`。
3. **对外克制**：对用户不暴露鉴权细节与内部密钥；**费用/用量查询结果**须按下方「输出层级」展开，不得只抛原始 JSON 或无序罗列。
4. **素材优先级**：用户给了文件或 URL，必须先提取内容再确认，确认后再触发调用。
5. **生产约束**：仅使用本 Skill `openapi` 中声明的生产域名与 HTTPS，不引入测试地址。
6. **接口拆分**：每个 API 独立成文档；模块内 `api-index.md` 仅做索引。
7. **危险操作**：查询他人费用仅在业务与权限允许时执行；越权或敏感场景应礼貌拒绝并说明替代方案。
8. **脚本语言限制**：所有脚本**必须使用 Python 编写**。
9. **重试策略**：出错时**间隔 1 秒、最多重试 3 次**，超过后终止并上报。
10. **禁止无限重试**：严禁无限循环重试。

**查询结果呈现给用户（强制顺序与层级）**

在 `user-usage.py` 返回 `resultCode` 成功后，根据 `data`（见 `openapi/llm-cost/user-usage.md`）向用户整理内容，**必须**按下面顺序；字段名以接口 JSON 为准（常见为 `summary`、`products`，产品下含模型列表）。

**呈现形式（强制）：** 能用表格处**尽量使用 Markdown 表格**（`| 列 | 列 |`），避免大段无表格纯文字罗列。执行脚本时**优先**使用 `python3 scripts/llm-cost/user-usage.py --format markdown`（参数与无 markdown 时相同），将输出的 Markdown **原样或略作说明后**交给用户；若只能使用 `--format json`，则须**自行按下列层级排成 Markdown 表格**，不得只贴无序 JSON。

1. **用户总览（整段查询范围）**  
   先给出该用户在查询条件下的**合计**：至少包含 **输入 Token 合计**、**输出 Token 合计**（若 `data` 中有总费用、总调用次数等，一并列出）。

2. **数字展示（Token 类）**  
   脚本会在 JSON 里为名称含 `token` 的数值字段自动生成 `字段名Display`（例如 `inputTokensDisplay`: `537.84K`、`inputTokens`: 537844）。**向用户展示 Token 时优先写 `*Display` 字符串**（≥1000 为 `K`，≥1,000,000 为 `M`）；若某字段无 `Display`，则按同一规则自行把原始整数格式化为 K/M。**费用金额（美元等）**仍用接口原始精度，不套用 K/M。

3. **按产品逐项**  
   对 `products`（或等价列表）**每个产品一节**，含**该产品小计**表：**输入 Token**、**输出 Token**（及费用等若存在）。  
   再在该产品下给出 **模型明细表**：

4. **该产品下各模型**  
   对该产品下的**每个模型**一行：**模型名称** + **输入 Token** + **输出 Token** + 调用/费用等（有则列）。

5. **顺序**  
   产品之间依次排列；同一产品内模型顺序可与接口返回一致。  
   **禁止**跳过总览直接列产品；**禁止**把模型与产品平铺成一张无层级表（除非用户明确要求「只要一张表」）。

模块路由与能力索引（合并版）：

| 用户意图（示例） | 模块 | 能力摘要 | 接口文档 | 示例模板 | 脚本 |
|---|---|---|---|---|---|
| 「查我今天 AI 花了多少」「我的 Token 费用」「查询费用」「查费用」「AI 费用多少」（**未说查谁**） | `llm-cost` | 当前用户用量明细；**不传 personId** | `./openapi/llm-cost/api-index.md` | `./examples/llm-cost/README.md` | `./scripts/llm-cost/user-usage.py`（无 `--person-id`） |
| 「张三这周的 AI 费用」（**明确姓名**） | `cwork-user` → `llm-cost` | 按姓名搜人后查用量 | `./openapi/cwork-user/api-index.md` 再 `./openapi/llm-cost/api-index.md` | `./examples/cwork-user/README.md` 与 `./examples/llm-cost/README.md` | `./scripts/cwork-user/search-emp-by-name.py` 再 `./scripts/llm-cost/user-usage.py` |

能力树（实际目录结构）：

```text
ai-llm-cost-query/
├── SKILL.md
├── openapi/
│   ├── cwork-user/
│   │   ├── api-index.md
│   │   └── search-emp-by-name.md
│   └── llm-cost/
│       ├── api-index.md
│       └── user-usage.md
├── examples/
│   ├── cwork-user/
│   │   └── README.md
│   └── llm-cost/
│       └── README.md
└── scripts/
    ├── cwork-user/
    │   ├── README.md
    │   └── search-emp-by-name.py
    └── llm-cost/
        ├── README.md
        └── user-usage.py
```
