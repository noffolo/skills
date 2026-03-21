# AiPPT Skill

> 通过 [AiPPT.cn](https://aippt.cn) 开放平台 API，用自然语言对话生成专业 PPT 演示文稿。

## 概述

本 Skill 集成了 AiPPT.cn 的智能 PPT 生成服务，支持：
- **智能生成** — 输入标题，AI 自动生成大纲、内容、排版
- **文档转PPT** — Word、PDF、Markdown、TXT、PPTX、XMind 一键转换
- **参考文档生成** — 以上传文件为素材，围绕指定主题重新生成
- **网页导入** — 从 URL 抓取内容生成 PPT
- **高级配置** — 页数、语言、场景、语气、受众、文本量全部可控
- **模型选择** — 智谱 / DeepSeek / 豆包可切换（部分类型支持）
- **企业模板** — B端专属模板优先推荐
- **自动下载** — 生成完成后默认下载 PPTX 到本地；对话明确要求图片时导出 PNG

---

## 前置条件

**环境依赖**：`curl`、`python3`、`openssl`

**API 密钥**：通过 OpenClaw 安装后在技能设置中填入，无需手动创建文件。

| 变量名 | 必填 | 说明 |
|--------|:----:|------|
| `AIPPT_APP_KEY` | ✅ | AiPPT 开放平台 App Key |
| `AIPPT_SECRET_KEY` | ✅ | AiPPT 开放平台 Secret Key |
| `AIPPT_UID` | ❌ | 用户标识，多用户隔离用，默认 `openclaw_default` |

获取密钥：前往 [AiPPT 开放平台](https://open.aippt.cn) 注册开发者账号。

---

## AI 决策入口（每次必走）

> 每次响应用户 PPT 请求，必须先走以下判断树。

```
用户发来消息
    ├── 有文件附件？ → 场景二（⚠️ 先询问意图，禁止直接执行）
    ├── 有 URL？     → 场景三（URL 导入）
    └── 只有文字？   → 场景一（标题生成）
```

---

## 场景一：标题/主题生成

**触发条件**：用户只描述了话题或标题，没有上传文件。

**示例**：
- "帮我做一个关于人工智能的PPT"
- "生成一份年终总结演示文稿"
- "做个产品发布会的幻灯片"

**完整流程（共 7 步）**：

```
1. 创建任务
2. 生成大纲（约 10 秒）
3. ⬇ 清晰展示大纲文本给用户（必须完整输出，格式化为 Markdown 标题层级）
4. 自动继续生成内容（不等用户确认，约 25 秒）
5. 合成 PPT（约 10 秒）
6. 导出
7. 下载 → 返回 PPTX 文件路径
```

**第一次工具调用 — 生成大纲**

```bash
bash scripts/aippt.sh generate "标题" --outline-only
```

命令结束后，从输出中找到 `outline_ready` 那行 JSON，提取 `task_id`、`title`、`outline` 字段。

**第一次工具调用结束后：先输出文字，再发起第二次工具调用**

> 🚨 **必须按以下顺序执行，不可合并：**
> 1. **结束第一次工具调用**
> 2. **向用户输出文字回复**（将大纲格式化为 Markdown 标题层级写入回复，同时说明"正在合成 PPT..."）
> 3. **再发起第二次工具调用**（执行 generate_continue）
>
> ✅ 正确：[工具调用1: --outline-only] → [文字输出: 大纲内容] → [工具调用2: generate_continue]
> ❌ 错误：[工具调用1: --outline-only] → [工具调用2: generate_continue] → [文字输出: 大纲内容]

输出格式示例：
```
📋 **大纲已生成，正在合成 PPT，请稍候...**

# 标题
## 第一章
### 1.1 小节
### 1.2 小节
## 第二章
...
```

**第二次工具调用 — 合成 PPT（约 60 秒）**

```bash
bash scripts/aippt.sh generate_continue "<task_id>" "<title>"
```

---

## 场景二：文档上传生成（⚠️ 必须先询问）

**触发条件**：用户上传了 Word、PDF、TXT、Markdown、PPTX 等文件。

**禁止直接执行**，必须先问用户：

> 您上传了一份文件，请问想怎么用它生成 PPT？
>
> 1. **文档转PPT** — 直接提取这份文件的内容生成 PPT
>    （适合：文档本身就是要呈现的内容，例如报告、总结、方案）
>
> 2. **参考文档生成** — 以这份文件为背景资料，由您指定主题，AI 重新组织生成
>    （适合：文档是参考材料，需要 AI 重新理解和表达）

**根据用户回答执行**：

**选择 1 — 文档转PPT（完整流程）**

> 文件类型影响流程：
> - **有大纲**（`.doc/.docx/.pdf/.txt/.pptx/.wps`）：先生成大纲展示，再自动合成
> - **无大纲**（`.md/.xmind/.mm`）：直接合成，无大纲展示步骤

对于 `.doc/.docx/.pdf/.txt/.pptx/.wps`：

```
1. 解析文档并生成大纲+内容（约 30 秒）
2. 获取 PPT 树形结构（generate/data）
3. ⬇ 清晰展示大纲文本给用户（必须完整输出，格式化为 Markdown 标题层级）
4. 自动继续合成 PPT（不等用户确认）
5. 导出
6. 下载 → 返回 PPTX 文件路径
```

**第一次工具调用 — 生成大纲（约 30 秒）**

```bash
bash scripts/aippt.sh generate_from_file "文件绝对路径" --outline-only
```

命令结束后，从输出中找到 `outline_ready` 那行 JSON，提取 `task_id`、`title`、`outline` 字段。

**第一次工具调用结束后：先输出文字，再发起第二次工具调用**

> 🚨 **必须按以下顺序执行，不可合并：**
> 1. **结束第一次工具调用**
> 2. **向用户输出文字回复**（将大纲格式化为 Markdown 标题层级写入回复，同时说明"正在合成 PPT..."）
> 3. **再发起第二次工具调用**（执行 generate_save）
>
> ✅ 正确：[工具调用1: --outline-only] → [文字输出: 大纲内容] → [工具调用2: generate_save]
> ❌ 错误：[工具调用1: --outline-only] → [工具调用2: generate_save] → [文字输出: 大纲内容]

**步骤 4+5+6 — 自动继续合成 PPT（不等用户确认，约 40 秒）**

```bash
bash scripts/aippt.sh generate_save "<task_id>" "<title>"
```

对于 `.md/.xmind/.mm` 类文件，直接执行（单步完成，无大纲展示）：

```bash
bash scripts/aippt.sh generate_from_file "文件绝对路径"
```

**选择 2 — 参考文档生成**

追问用户 PPT 主题，再执行：
```bash
bash scripts/aippt.sh generate_with_refer "PPT主题" "文件绝对路径"
```

### ⚠️ 参考文档模式 B 端限制（执行前必须检查）

| 限制项 | 规则 | 违规处理 |
|-------|------|---------|
| 单文件大小 | **≤ 10MB** | 脚本自动报错，提示用户压缩或改用「文档转PPT」|
| 最多文件数 | **≤ 5 个**（同一次 PPT 生成） | 超出时告知用户只取前5个，或分批生成 |

> **说明**：参考文档模式调用的是 B 端专属接口（`/api/ai/chat/refer`），以上限制来自平台 API 规范，不可绕过。

---

## 场景三：网页 URL 导入

**触发条件**：用户提供了一个网页 URL。

**示例**：
- "把这篇文章做成PPT：https://..."
- "根据这个页面生成演示文稿"

**执行（两步走）**：

**步骤 1 — 创建任务并生成大纲**

```bash
# 1a. 创建任务，获取 task_id
task_id=$(bash scripts/aippt.sh create_from_url "https://..." \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['data']['id'])")

# 1b. 抓取页面内容 + 生成大纲（SSE，约 30 秒）
#     脚本输出 outline_ready 步骤（stderr），将大纲格式化展示给用户
bash scripts/aippt.sh link "$task_id" 2>&1 | grep -E '^{' | python3 -c "
import sys,json
for line in sys.stdin:
    try:
        obj=json.loads(line)
        if obj.get('step')=='outline_ready':
            print(obj.get('outline',''))
    except: pass
"
```

收到 `outline_ready` 后，将大纲格式化展示给用户，**立即**执行步骤 2，不等待用户确认。

**步骤 2 — 合成 PPT**

```bash
bash scripts/aippt.sh generate_save "$task_id" "<页面标题>" [template_id] [output_dir] [formats]
```

---

## 企业模板检查（B端客户适用）

在执行生成命令前，先检查是否有企业专属模板：

```bash
bash scripts/aippt.sh enterprise_templates
```

| 返回结果 | 处理方式 |
|---------|---------|
| `code≠0` 或 `data.list` 为空 | 跳过，使用普通模板自动生成 |
| `data.list` 非空 | 询问用户："是否使用企业专属模板？" |

用户选择企业模板时，将模板 ID 和 `enterprise` 类型传入：
```bash
bash scripts/aippt.sh generate "年终总结" <enterprise_tpl_id> ~/Desktop ppt enterprise
bash scripts/aippt.sh generate_from_file report.docx <enterprise_tpl_id> ~/Desktop ppt enterprise
```

---

## 高级配置（可选，提升生成质量）

### 查询可用选项 ID

```bash
bash scripts/aippt.sh senior_options
```

返回所有配置项和 ID，★ 表示默认值：

| 配置项 | key | 常用选项（ID:名称） |
|--------|-----|-------------------|
| 页数 | page | 53:5-10页 / 3:20-30页★ / 56:尽情发挥 |
| 受众 | group | 6:大众★ / 9:学生 / 8:商业 / 11:老板 |
| 场景 | scene | 18:通用★ / 27:项目汇报 / 34:年度总结 / 29:商业计划书 |
| 语气 | tone | 40:专业★ / 42:幽默 / 43:亲切 |
| 语言 | language | 47:简体中文★ / 49:英语 / 50:日语 |
| 文本量 | text | 58:简洁 / 60:详细★ |

### 使用方式

`--options` 传 ID 数组，`--model` 切换 AI 模型：

```bash
# 年度总结 + 英语 + 详细文本
bash scripts/aippt.sh generate "Annual Review 2025" --options "[49,34,60]" --model doubao-1.5-pro-32k

# 文件转PPT + 指定场景和语言
bash scripts/aippt.sh generate_from_file report.pdf --options "[49,27,40]"
```

### 模型选择

| 模型 ID | 描述 | 支持的 type |
|---------|------|------------|
| `glm4.5-air` | 智谱 GLM | 1 / 9 / 10 / 18 |
| `deepSeek-v3` | DeepSeek V3 | 1 / 9 / 10 / 18 |
| `doubao-1.5-pro-32k` | 字节豆包 | 1 / 9 / 10 / 18 |

> 不传 model 时服务端自动选择默认模型。

---

## 执行进度反馈

命令运行时，从 stderr 读取进度 JSON 并实时告知用户：

| `step` 值 | 适用场景 | 向用户说明 |
|-----------|---------|-----------|
| `create` | 所有 | 正在创建任务... |
| `outline` | 标题生成 | 正在生成大纲，约 6 秒... |
| `outline_ready` | 所有 type | **立即展示大纲**：解析 JSON 中 `outline` 字段，格式化展示给用户；保存 `task_id` 和 `title`；随后**无需确认**立即执行步骤 2（`generate_continue` 或 `generate_save`） |
| `content_triggered` | 标题生成 | 正在生成内容，约 25 秒... |
| `ppt_data` | 所有 type（步骤2）| 获取 PPT 树形结构... |
| `outline_save` | 所有 type（步骤2）| 提交大纲中... |
| `outline_saved` | 所有 type（步骤2）| 大纲提交完成，继续合成 |
| `word` | Word/PDF/TXT/PPTX/WPS | 正在解析文档并生成大纲+内容，约 30 秒... |
| `file_parsed` | MD/XMind/FreeMind | 文件已上传，准备生成... |
| `composing` | 所有 | 告知用户：合成中，请稍候... |
| `pick_template` | 所有 | 正在选择模板... |
| `save` | 所有 | 正在生成 PPT 作品，约 10 秒... |
| `export` | 所有 | 正在触发导出... |
| `wait_export` | 所有 | 正在渲染导出，约 30 秒... |
| `downloaded` | 所有 | 某格式已下载（format + size） |
| `done` | 所有 | 完成，返回文件路径 |

---

## 命令参考

### 一键生成（推荐）

```bash
# 从标题生成
bash scripts/aippt.sh generate <标题> [template_id] [output_dir] [formats] [template_type]

# 从文件生成（文档转PPT）
bash scripts/aippt.sh generate_from_file <文件路径> [template_id] [output_dir] [formats] [template_type]

# 参考文档生成（type=17，最多5个文件，每个 ≤ 10MB）
bash scripts/aippt.sh generate_with_refer <PPT主题> <文件1> [文件2..文件5] \
  [--output_dir <dir>] [--formats <fmts>] [--template_id <id>] [--template_type <type>]
```

**参数说明：**

| 参数 | 必需 | 默认值 | 说明 |
|------|:----:|-------|------|
| 标题 / 文件路径 | ✅ | — | PPT 主题文字 或 本地文件绝对路径 |
| PPT主题（refer） | ✅ | — | 参考文档模式 PPT 标题，作为 type=17 任务的 title |
| 文件1..5（refer） | ✅（至少1个）| — | 参考文档路径，支持 Word/PDF/TXT/WPS |
| template_id | ❌ | 随机选20个之一 | 模板 ID |
| output_dir | ❌ | skill 目录 | 输出目录 |
| formats | ❌ | `ppt` | 导出格式，逗号分隔：`ppt,pdf,word,png` |
| template_type | ❌ | 空（普通模板） | `enterprise` = 企业模板 |

### 文件类型与 API 流程对照

| 扩展名 | type | 流程 |
|-------|------|------|
| `.doc` / `.docx` | 3 | Word SSE → save |
| `.xmind` | 4 | direct save |
| `.mm` (FreeMind) | 5 | direct save |
| `.md` | 7 | direct save（content 字段） |
| `.pdf` | 9 | Word SSE → save |
| `.txt` | 10 | Word SSE → save |
| `.ppt` / `.pptx` | 12 | Word SSE → save |
| `.wps` | 18 | Word SSE → save |
| 参考文档（refer）| 17 | refer SSE → save |

### 模板

| 命令 | 说明 |
|------|------|
| `templates [page] [size] [color] [style]` | 搜索普通模板列表 |
| `enterprise_templates` | 获取企业专属模板（B端配置，未开启返回 code≠0） |
| `options` | 获取模板颜色/风格筛选项 |

### 分步操作（type=1 标题生成专用）

| 命令 | 说明 |
|------|------|
| `create <标题> [type]` | 创建任务，返回 task_id |
| `outline <task_id>` | 生成大纲（SSE 流式）⚠️ 仅 type=1 |
| `content <task_id>` | 触发内容生成，返回 ticket ⚠️ 仅 type=1 |
| `check <ticket>` | 轮询生成状态（参数是 ticket，不是 task_id！） |
| `wait <ticket> [timeout]` | 阻塞等待内容生成完成 |

### 分步操作（文件 / URL 导入专用）

| 命令 | 说明 |
|------|------|
| `create_with_file <文件> [type]` | 从文件创建任务 |
| `create_from_url <URL>` | 从网页 URL 创建任务（type=16） |
| `word <task_id>` | Word 文档解析+生成大纲+内容（SSE，type=3 专用） |
| `link <task_id>` | URL 链接抓取+生成（SSE，type=16 专用） |
| `refer <task_id>` | 参考文档模式生成（SSE） |
| `conver_file <task_id> <type>` | 解析 MD/XMind/FreeMind → 返回 Markdown 文本 |

### 两步续跑（大纲确认后使用）

| 命令 | 说明 |
|------|------|
| `generate_continue <task_id> <title>` | 续跑 type=1 标题任务（content → composing → save → export） |
| `generate_save <task_id> <title>` | 续跑文件任务（composing → save → export，跳过 content 步骤） |

### 生成 / 导出（所有流程通用）

| 命令 | 说明 |
|------|------|
| `save <task_id> <template_id> [name] [template_type]` | 生成 PPT 作品，返回 design_id |
| `export <design_id> [format] [edit]` | 触发导出，返回 task_key |
| `export_result <task_key>` | 查询导出结果 |
| `wait_export <task_key> [timeout]` | 阻塞等待导出完成，返回下载 URL |
| `auth` | 获取 / 刷新 Token |

---

## API 流程详解

> ⚠️ **关键：不同任务类型走完全不同的后端接口，不可混用。**
> `outline` 和 `content` 接口只对 type=1 有效，文件导入任务调用这两个接口会返回"任务不存在"。

### 流程 A — type=1 标题智能生成

```
创建任务
  → outline（SSE，约 6s，生成大纲）
  → content（获取 ticket）
  → check 轮询（约 25s，等待内容就绪）
  → save（约 10s）
  → export + 轮询下载
总耗时：约 60–90 秒
```

### 流程 B — type=3 Word 文件导入

```
创建任务（上传 .doc/.docx）
  → word SSE（约 30s，服务端解析 Word + 生成大纲+内容）
  → save（约 10s）
  → export + 轮询下载
总耗时：约 60 秒
```

### 流程 C — type=7/4/5 Markdown / XMind / FreeMind

```
创建任务（传 content 字段，文本内容）
  → save 直接（约 10s，服务端自动从内容生成）
  → export + 轮询下载
总耗时：约 50 秒
```

### 流程 D — type=8/9/10 PDF / TXT / PPTX

```
创建任务（上传文件）
  → save 直接（约 10s）
  → export + 轮询下载
总耗时：约 50 秒
```

### 流程 E — type=16 URL 链接导入

```
创建任务（传 link 字段）
  → link SSE（约 30s，抓取页面 + 生成大纲+内容）
  → save（约 10s）
  → export + 轮询下载
总耗时：约 60 秒
```

### 关键接口说明

| 接口 | 方法 | 路径 | 适用类型 |
|------|------|------|---------|
| 鉴权 | GET | `/api/grant/token/` | 所有 |
| 创建任务 | POST | `/api/ai/chat/v2/task` | 所有 |
| 生成大纲 | GET (SSE) | `/api/ai/chat/outline` | type=1 only |
| 触发内容生成 | GET | `/api/ai/chat/v2/content` | type=1 only |
| 轮询内容状态 | GET | `/api/ai/chat/v2/content/check` | type=1 only |
| Word 解析+生成 | GET (SSE) | `/api/ai/chat/v2/word` | type=3 only |
| URL 抓取+生成 | GET (SSE) | `/api/ai/chat/link` | type=16 only |
| 参考文档生成 | GET (SSE) | `/api/ai/chat/refer` | 参考文档模式 |
| 文件内容解析 | GET | `/api/ai/conver/file` | type=4/5/7 |
| 生成作品 | POST | `/api/design/v2/save` | 所有 |
| 触发导出 | POST | `/api/download/export/file` | 所有 |
| 查询导出结果 | POST | `/api/download/export/file/result` | 所有 |
| 普通模板列表 | GET | `/api/template_component/suit/search` | 所有 |
| 企业模板列表 | GET | `/api/template_component/enterprise/suit/list` | B端 |

### 任务类型对照表

| type | 说明 | 输入方式 | 后续流程 |
|------|------|---------|---------|
| 1 | 智能生成 | `title` 字段 | outline → content → save |
| 3 | Word 导入 | 文件上传 | word SSE → save |
| 4 | XMind 导入 | 文件上传 | save 直接 |
| 5 | FreeMind 导入 | 文件上传 | save 直接 |
| 7 | Markdown 导入 | `content` 文本字段 | save 直接 |
| 8 | PDF 导入 | 文件上传 | save 直接 |
| 9 | TXT 导入 | 文件上传 | save 直接 |
| 10 | PPTX 导入 | 文件上传 | save 直接 |
| 16 | URL 导入 | `link` 字段 | link SSE → save |

### 导出格式

| format | 输出文件 |
|--------|---------|
| `ppt` | .pptx（默认） |
| `pdf` | .pdf |
| `word` | .docx |
| `png` | .png（每页一图） |

### 错误码

> 脚本内置 `check_resp()` 统一处理，所有非0 code 自动映射为中文提示。

| code | 含义 | 脚本处理方式 |
|------|------|------------|
| 40007 | 余额不足 | 报错：账户余额不足，请充值后重试 |
| 40008 | 功能未开通 | 报错：该功能未开通，请联系管理员 |
| 10307 | 企业模板未开启 | 报错提示（AI 层面跳过，用普通模板） |
| 43101 | Token 过期 | 报错：删除 `.token_cache.json` 后重试 |
| 43102 | 签名错误 | 报错：检查 `AIPPT_SECRET_KEY` 是否正确 |
| 12100 | AI 内容生成失败 | 报错：换个标题或稍后重试 |
| 12101 | 内容审核未通过 | 报错：修改标题/内容后重试 |
| 12102 | 任务不存在 | 报错：检查是否对文件任务误调用了 outline/content |
| 20003 | 导出队列已满 | 自动等待重试（最多5次，每次间隔10秒） |
| 20001 | 导出任务不存在 | 报错：重新触发导出 |
| 30001 | 模板无权限 | 报错：模板不存在或无权使用该模板 |
| 50000 | 服务器内部错误 | 报错：稍后重试 |

---

## 文件结构

```
aippt-skill/
├── SKILL.md              ← 本文件
├── skill.json            ← Skill 元数据 & 触发词
├── scripts/
│   └── aippt.sh          ← API 集成脚本 (v2.9)
├── .env                  ← API 密钥（不要提交到版本库！）
└── .token_cache.json     ← Token 缓存（自动生成）
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 3.0.5 | 2026-03-20 | 修复大纲不提前展示的根本原因：明确要求两次工具调用之间必须夹一次文字输出，用 ✅/❌ 示例强制 AI 先输出大纲文字再发起第二次工具调用，彻底拆分两步请求 |
| 3.0.4 | 2026-03-20 | 强化大纲展示指令：将"展示大纲"拆为独立步骤3，加 🚨 禁止规则，明确"在执行后续命令之前必须先将大纲写入回复"，杜绝 AI 连跑两步命令后才展示大纲的问题 |
| 3.0.3 | 2026-03-20 | 修复默认 model/senior_opts 导致账号鉴权失败问题：去掉硬编码的 doubao 模型和 senior_options 默认值，改为不传，由服务端自动选择 |
| 3.0.2 | 2026-03-20 | 明确 AI 执行顺序：场景一/二均加入「3. 展示大纲文本给用户」步骤说明，强调必须先完整展示大纲再继续合成，不可跳过 |
| 3.0.1 | 2026-03-20 | 修复 type=4/5/7 大纲展示不一致问题：XMind/FreeMind/Markdown 现在也调 generate/data 获取服务端树形大纲，与所有其他类型保持一致 |
| 3.0.0 | 2026-03-20 | 补全官方流程：新增 api/generate/data + /api/ai/chat/v2/outline/save 两步；generate_save/generate_continue 在 save 前必须调用；文件类型 outline 改从树形结构获取 |
| 2.9.1 | 2026-03-20 | 修复大纲无法展示的根本问题：恢复两步命令（--outline-only → generate_continue/generate_save），但去掉中间的确认等待，展示大纲后立即执行合成 |
| 2.9.0 | 2026-03-19 | 去掉大纲确认等待逻辑：展示大纲后脚本自动继续合成，中途不停；修正 outline_ready 进度表描述；Scene 3 URL 导入去掉"询问是否继续"语言 |
| 2.8.0 | 2026-03-19 | 全 type 大纲展示（两步流程：outline_ready → 用户确认 → composing → 合成）；generate_save / generate_continue 续跑命令；task_id 语义模板匹配；type=1 默认 doubao-1-5-pro-32k-250115 + 20-30页；去掉自动更新和流式输出逻辑 |
| 2.7.0 | 2026-03-18 | 新增高级配置（senior_options）；模型切换（--model）；参考文档模式（type=17）；随机模板选取；文件名去重 |
| 2.4.0 | 2026-03-18 | 修复文件导入流程（按类型走正确接口）；新增 enterprise_templates / word / link / refer / conver_file 命令；修正 API 流程文档 |
| 2.3.0 | 2026-03-18 | 新增使用场景章节（文件上传询问逻辑）；generate_from_file 一键文档转PPT |
| 2.2.0 | 2026-03-10 | 修复文件 hidden flag、多格式导出顺序执行、文件格式验证 |
| 2.1.0 | 2026-03-10 | 修复多格式导出队列满（20003）、增加文件验证 |
| 2.0.0 | 2026-03-10 | 重写：修复 ticket/task_id 混淆，补全 save+export 流程，支持一键 generate |
| 1.0.0 | 2026-03-04 | 初版：基础 API 调用 |
