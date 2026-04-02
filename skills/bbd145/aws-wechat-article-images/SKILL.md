---
name: aws-wechat-article-images
description: 为公众号文章生成封面图和正文配图，根据文章内容自动匹配风格。当用户提到「封面」「配图」「插图」「生成图片」「给文章加图」「做个封面」「文章插图」「配个图」时使用。
---

# 配图

## 路由

完整长文从选题到发布 → [aws-wechat-article-main](../aws-wechat-article-main/SKILL.md)；图片消息/九宫格等多图推送 → [aws-wechat-sticker](../aws-wechat-sticker/SKILL.md)。

读取文章中的配图标记，按 Type × Style 体系生成图片。专注于**长文配图**，贴图请用 sticker。

## 脚本目录

**Agent 执行**：确定本 SKILL.md 所在目录为 `{baseDir}`（仓库内即 `skills/aws-wechat-article-images/`）。

| 脚本 | 用途 |
|------|------|
| `scripts/image_create.py` | 专用生图 API：读 **`.aws-article/config.yaml`** 的 **`image_model`** + 仓库根 **`aws.env`** 的 **`IMAGE_MODEL_API_KEY`**|

## 配置检查 ⛔

任何操作执行前，**必须**按 **[首次引导](../aws-wechat-article-main/references/first-time-setup.md)** 执行其中的 **「检测顺序」**。检测通过后才能进行以下操作（或用户明确书面确认「本次不检查」）：

从选题到发布的**前置规则**见 [aws-wechat-article-main/SKILL.md](../aws-wechat-article-main/SKILL.md)；本 skill 只描述配图步骤。

**图片模型**：**`image_model`**（`provider`、`base_url`、`model`、`default_size`、`default_quality` 等）在 **`config.yaml`**；**`IMAGE_MODEL_API_KEY`** 在 **`aws.env`**。键名对照 **`.aws-article/env.example.yaml`**。

**交互约定**：可提示用户上述项是否已填；**一条龙**下通常已通过 **`validate_env.py`**。须遵守 main 的**智能体行为约束**——未通过环境校验且未获用户明确「本次例外」时，不得假装已走专用生图 API。

## Type × Style 体系

Type（画面构成）× Style（视觉风格）自由组合。

完整风格库、兼容矩阵、预设组合、prompt 模板：见 [shared/image-styles/](../shared/image-styles/) 目录。

## 工作流

```
配图进度：
- [ ] 第1步：环境检查 + 本篇约束与文章
- [ ] 第2步：解析配图标记
- [ ] 第3步：确定风格
- [ ] 第4步：生成配图方案
- [ ] 第5步：展示方案并等待确认 ⛔
- [ ] 第6步：生成图片（**脚本失败时**见同节「调用失败」分支，勿静默吞掉报错）
- [ ] 第7步：插入文章
```

### 第1步：环境检查 + 本篇约束与文章

- **全局**：读 **`.aws-article/config.yaml`** — `cover_aspect`、`cover_style`、`image_density`、`caption_style`、`default_image_style`、`multi_image_count`、`tone` 等以之为准（完整字段见 [articlescreening-schema.md](../aws-wechat-article-main/references/articlescreening-schema.md) 与 **`config.example.yaml`**）。
- **本篇**：若同目录有 **`article.yaml`**，可读取 **`cover_image`** 等本篇字段；与 **`config.yaml`** 同名字段时**本篇优先**（与写稿侧合并规则一致）。
- 读取 **`article.md`**（或当前流程规定的正文来源）。

### 第2步：解析配图标记

提取所有 `![类型：描述](placeholder)`。`实证` 类型提示用户提供素材或从 `.aws-article/assets/` 搜索。

**可用素材库**：

- `.aws-article/assets/screenshots/` — 可直接复用的产品/系统截图。优先用于「实证」「界面」类图片；如含敏感信息请打码后使用。

### 第3步：确定风格

**风格加载优先级**：
1. 用户指定（「用水彩风」）
2. **`config.yaml`** 的 **`default_image_style`**（若有）
3. `.aws-article/presets/image-styles/` 下的自定义风格
4. **fallback**：根据正文与 **`config.yaml`** 的 **`tone`** 自动推荐（规则见 [auto-selection.md](../shared/image-styles/auto-selection.md)），默认「扁平矢量」

全文统一风格。完整风格库：[shared/image-styles/styles.md](../shared/image-styles/styles.md)

### 第4步：生成配图方案

为每张图生成方案（类型、风格、prompt 要点）。

**图片内文字**：画面中出现的文字必须为中文。在 prompt 里**直接写出要显示的中文文案**（如「传统对话AI」「OpenClaw」），禁止只写 “labels in Chinese” 或 “Chinese or English OK”，否则模型会生成英文。

Prompt 构建：[shared/image-styles/prompt-construction.md](../shared/image-styles/prompt-construction.md)

### 第5步：展示方案并等待确认 ⛔

### 第6步：生成图片

**生成方式（优先级）**：

1. **优先：调用专用生图 API**（`scripts/image_create.py`）— 依赖 **`config.yaml` 的 `image_model` + `aws.env` 的 `IMAGE_MODEL_API_KEY`**
2. **降级：当前 Agent 多模态 / 仅出 prompts** — 仅当环境未就绪、用户接受 main「本次例外」、或**已按本节下方「调用失败」表格处理**（网络重试后仍失败等）时

**必须告知用户当前使用的方式**：

- 已配置且调用脚本 → `ℹ️ 使用 image_create.py 调用专用生图模型（{model}）`
- Agent 生图 / 仅 prompts → `ℹ️ 本次未走 image_create.py（原因：…）`

**⛔ 未调用专用 API 时的终点**：只做到第 4 步（或第 5 步）。产出 `imgs/prompts/*.md` 与方案；**不执行**「替换 article 中的 placeholder」或「修复 HTML」。若 `imgs/README.md` 尚不存在或需补充当前方案的说明，可创建/更新（如何配置 **`aws.env` / `config.yaml`**、如何跑 `image_create.py batch`、如何在 `article.html` 中替换）；若已存在且已涵盖当前方案，**不必重写**。

**调用专用 API 时**（在**仓库根**执行，`{baseDir}` 按上表解析；路径按本篇 `imgs/` 调整）：

```bash
python {baseDir}/scripts/image_create.py batch drafts/YYYYMMDD-slug/imgs/prompts/ -o drafts/YYYYMMDD-slug/imgs/
```

单张：`python {baseDir}/scripts/image_create.py generate imgs/prompts/01-cover.md -o imgs/01-cover.png`

连通性自检：`python {baseDir}/scripts/image_create.py test`

图片规格：[references/specs.md](references/specs.md)

#### `image_create.py` 调用失败时（智能体必选分支）

只要执行了 `image_create.py` 且**非零退出或 stderr 有 API/网络错误**，就必须走本节，**不得**只说「生图失败」而不分类、不摘要报错。

运行脚本后**须把终端 stderr 中的具体报错摘要给用户**（含 `❌`、HTTP 状态码、`【配置/认证】`、`网络错误（可重试）` 等关键行），勿只说「失败」。

| 类型 | 判断线索 | 智能体动作 |
|------|----------|------------|
| **网络类** | `URLError`、`网络错误（可重试）`、超时、临时 502/503 | **必须自动再试 1 次**（可短暂等待后重跑同一命令）。**第二次仍为网络类** → 可降级为 **Agent 多模态生图** 或仅保留 prompts；**须明确告知**用户本次未走专用 API。 |
| **配置/凭证类** | 401/403、图片模型配置不完整、`【配置/认证】` | **不要**静默降级。**列出须检查项**（**`config.yaml` 的 `image_model`**、**`aws.env` 的 `IMAGE_MODEL_API_KEY`**、端点、权限），请用户改正后重跑。用户**明确打字**接受本次仅用 Agent/仅 prompts 时，再按 main「本次例外」处理。 |
| **业务/参数类** | `【请求参数】`、400、返回体提示 model/size 不支持 | 将响应摘要给用户；可改 **`config.yaml` 或 env** 中的 model/尺寸后再试；仍失败则与用户商定是否 Agent 生图。 |

**禁止**：配置明显错误时静默改用 Agent 却不说明；网络降级后不告知「本次未走专用生图」。

### 第7步：插入文章

仅当**已生成图片**时执行：替换 placeholder 为实际图片路径，输出到 `imgs/`。

**修复 HTML 的触发条件**：仅当在 `article.html` 中**确实存在** `href="placeholder"` 或 placeholder 被渲染成可点击链接时，才将误转的 `<a>` 改为 `<img>` 或占位说明；**不要**默认每次都执行「修复流程图占位」或「修复 HTML」。

## 过程文件

| 读取 | 产出 |
|------|------|
| **`article.md`**、**`.aws-article/config.yaml`**、本篇可选 **`article.yaml`** 中的标记与配图约束 | `imgs/`（outline + prompts + 图片；未走 API 时为 prompts + 可选 imgs/README.md） |
