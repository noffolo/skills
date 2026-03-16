---
name: notex-skills
description: NoteX 技能路由网关索引（CWork Key 鉴权），覆盖内容生产（PPT/视频/音频/报告/脑图/测验/闪卡/信息图）、运营数据问答与洞察、笔记本管理（列表/统计/创建/追加来源）、来源索引与详情定位、首页登录链接生成。
---

# NoteX Skills — 索引

本文件提供**能力宪章 + 能力树 + 按需加载规则**。详细参数与流程见各模块 `openapi/` 与 `examples/`。

**当前版本**: v1.2

**接口版本**: 所有业务接口统一使用 `/openapi/*` 前缀，自带 `access-token` 鉴权，不依赖网关。

**能力概览（5 块能力）**：
- `open-link`：生成带 token 的 NoteX 首页访问链接
- `creator`：内容生产（八个工作室模块：PPT/视频/音频/报告/脑图/测验/闪卡/信息图）
- `ops`：运营数据问答与洞察
- `notebooks`：笔记本列表/统计/创建/追加来源
- `sources`：来源索引树与最小详情定位

统一规范：
- 认证与鉴权：`./common/auth.md`
- 通用约束：`./common/conventions.md`

输入完整性规则（强制）：
1. **内容生产必须完整**：调用 `creator` 的八个工作室模块时，必须提供完整上下文文本（`context_text`），不接受摘要、截断或缺失段落的内容。
2. **追加来源必须完整**：`notebooks/add-source` 的来源内容必须是完整原文，避免只传摘要或片段。

素材解析与技能建议（场景补充）：
- 若用户丢链接/文件并要求生成 PPT/音频概览/报告等，建议先使用对应的**解析类技能**提取完整正文，再将完整内容传入 `creator` 的任务请求。

建议工作流（简版）：
1. 读取 `SKILL.md` 与 `common/*`，明确能力范围、鉴权与安全约束。
2. 识别用户意图并路由模块，先打开 `openapi/<module>/api-index.md`。
3. 确认具体接口后，加载 `openapi/<module>/<endpoint>.md` 获取入参/出参/Schema。
4. 补齐用户必需输入，必要时先读取用户文件/URL 并确认摘要。
5. 参考 `examples/<module>/README.md` 组织话术与流程。
6. 若需要联调、批量或复杂编排，再加载对应 `scripts/`。

脚本使用规则（强制）：
1. **脚本可独立执行**：所有 `scripts/` 下的脚本均可脱离 AI Agent 直接在命令行运行。
2. **先读文档再执行**：执行脚本前，**必须先阅读对应模块的 `openapi/<module>/api-index.md`**，获取完整入参说明与约束条件。
3. **入参来源**：脚本的所有入参定义与字段说明以 `openapi/` 文档为准，脚本仅负责编排调用流程。
4. **鉴权一致**：脚本内部同样遵循 `common/auth.md` 的鉴权规则（环境变量 → CWork Key 换取）。

意图路由与加载规则（强制）：
1. **先路由再加载**：必须先判定模块，再打开该模块的 `api-index.md`。
2. **先读文档再调用**：在描述调用或执行前，必须加载对应接口文档（`openapi/<module>/<endpoint>.md`）。
3. **脚本按需**：涉及联调、批量或复杂编排时，必须加载对应 `scripts/`。
4. **不猜测**：若意图不明确，必须追问澄清，不允许跨模块或"默认模块"猜测。

宪章（必须遵守）：
1. **只读索引**：`SKILL.md` 只描述"能做什么"和"去哪里读"，不写具体接口参数。
2. **按需加载**：默认只读 `SKILL.md` + `common`，只有触发某模块时才加载该模块的 `openapi` 与 `examples`，必要时再加载 `scripts`。
3. **对外克制**：对用户只输出"可用能力、必要输入、结果链接或摘要"，不暴露鉴权细节与内部字段。
4. **素材优先级**：用户给了文件或 URL，必须先提取内容再确认，确认后才触发生成或写入。
5. **生产约束**：仅允许生产域名与生产协议，不引入任何测试地址。
6. **接口拆分**：每个 API 独立成文档，路径为 `openapi/<module>/<endpoint>.md`；模块内 `api-index.md` 仅做索引。
7. **危险操作**：对可能导致数据泄露、破坏、越权或高风险副作用的请求，应礼貌拒绝并给出安全替代方案。

模块路由与能力索引（合并版）：

| 用户意图（示例） | 模块 | 能力摘要 | 接口文档 | 示例模板 | 脚本（可独立执行） |
|---|---|---|---|---|---|
| 打开首页、生成登录/访问链接 | `open-link` | 生成带 token 的 NoteX 首页链接 | `./openapi/open-link/api-index.md`（`home-link.md`） | `./examples/open-link/README.md` | `./scripts/open-link/notex-open-link.js` |
| 内容生产（PPT/视频/音频/报告/脑图/测验/闪卡/信息图） | `creator` | 内容创作产物：PPT/视频/音频/报告/脑图/测验/闪卡/信息图 | `./openapi/creator/api-index.md`（`autoTask.md`、`taskStatus.md`） | `./examples/creator/README.md` | `./scripts/creator/skills-run.js` |
| 运营数据问答/洞察 | `ops` | 运营数据问答与洞察（ops-chat） | `./openapi/ops/api-index.md`（`ai-chat.md`） | `./examples/ops/README.md` | `./scripts/creator/skills-run.js`（复用） |
| 笔记本列表/统计/创建/追加来源/来源读取 | `notebooks` | 笔记本统计、列表、创建、追加来源与来源读取 | `./openapi/notebooks/api-index.md`（`list.md`、`category-counts.md`、`create.md`、`add-source.md`、`sources-list.md`、`source-content.md`） | `./examples/notebooks/README.md` | `./scripts/notebooks/notebooks-write.js`、`./scripts/notebooks/notebooks-read.js` |
| 来源索引树/详情 | `sources` | 来源索引树与最小详情定位 | `./openapi/sources/api-index.md`（`index-tree.md`、`details.md`） | `./examples/sources/README.md` | `./scripts/sources/source-index-sync.js` |

能力树（实际目录结构）：
```text
docs/skills
├── SKILL.md
├── common
│   ├── auth.md
│   └── conventions.md
├── openapi
│   ├── common
│   │   └── appkey.md
│   ├── creator
│   │   ├── api-index.md
│   │   ├── autoTask.md
│   │   └── taskStatus.md
│   ├── ops
│   │   ├── api-index.md
│   │   └── ai-chat.md
│   ├── notebooks
│   │   ├── api-index.md
│   │   ├── category-counts.md
│   │   ├── list.md
│   │   ├── create.md
│   │   ├── add-source.md
│   │   ├── sources-list.md
│   │   └── source-content.md
│   ├── sources
│   │   ├── api-index.md
│   │   ├── index-tree.md
│   │   └── details.md
│   └── open-link
│       ├── api-index.md
│       └── home-link.md
├── examples
│   ├── creator/README.md
│   ├── ops/README.md
│   ├── notebooks/README.md
│   ├── sources/README.md
│   └── open-link/README.md
└── scripts                          ← 所有脚本可独立执行
    ├── creator/skills-run.js        ← 执行前先读 openapi/creator/api-index.md
    ├── notebooks/notebooks-write.js ← 执行前先读 openapi/notebooks/api-index.md
    ├── notebooks/notebooks-read.js  ← 执行前先读 openapi/notebooks/api-index.md
    ├── sources/source-index-sync.js ← 执行前先读 openapi/sources/api-index.md
    ├── open-link/notex-open-link.js ← 执行前先读 openapi/open-link/api-index.md
    └── ops/                         ← 目录保留；ops-chat 复用 creator/skills-run.js
├── skill-template
│   └── SKILL.md
```
