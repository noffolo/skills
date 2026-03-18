---
name: aippt
version: 2.1.0
description: "通过 AiPPT.cn 开放平台 API 智能生成专业 PPT 演示文稿，支持标题生成、文件导入、URL导入、模板选择、自动导出下载"
author: "小龙 🐉"
triggers:
  - PPT
  - ppt
  - 演示文稿
  - aippt
  # ... 其他触发词
env:
  AIPPT_APP_KEY:
    required: true
    description: "AiPPT 开放平台 API Key"
  AIPPT_SECRET_KEY:
    required: true
    description: "AiPPT 开放平台 Secret Key"
  AIPPT_UID:
    required: false
    default: "openclaw_default"
    description: "用户标识 (多用户隔离)"
dependencies:
  bins: ["curl", "python3", "openssl"]
metadata:
  openclaw:
    entrypoint: "scripts/aippt.sh"
---
# AiPPT Skill

> 通过 [AiPPT.cn](https://aippt.cn) 开放平台 API，用自然语言对话生成专业 PPT 演示文稿。


## 概述

本 Skill 集成了 AiPPT.cn 的智能 PPT 生成服务，支持：
- 🎯 **智能生成** — 输入标题，AI 自动生成大纲、内容、排版
- 📄 **文件导入** — 从 Word、PDF、Markdown、TXT 等文件生成 PPT
- 🌐 **网页导入** — 从 URL 抓取内容生成 PPT
- 🎨 **模板选择** — 15000+ 专业模板可选
- 📥 **自动下载** — 生成完成后自动下载 PPTX/PDF/Word 文件到本地

## 前置条件

### 环境依赖
- `curl` — HTTP 请求
- `python3` — JSON 解析
- `openssl` — HMAC-SHA1 签名

### API 密钥
在 `.env` 文件中配置（或设置环境变量）：

```bash
AIPPT_APP_KEY=你的AppKey
AIPPT_SECRET_KEY=你的SecretKey
# 可选: 用户标识 (默认: openclaw_default)
# AIPPT_UID=my_user_id
```

获取密钥: 前往 [AiPPT 开放平台](https://open.aippt.cn) 注册开发者账号。

## 使用方式

### 对话触发

用户在对话中提到以下关键词时自动触发：
- "做PPT"、"生成PPT"、"创建PPT"
- "演示文稿"、"幻灯片"
- "aippt"、"AiPPT"

### 基本对话示例

```
用户: 帮我做一个关于"人工智能发展趋势"的PPT
助手: 好的，正在为您生成PPT...
      → 创建任务 ✓
      → 生成大纲 ✓
      → 生成内容 ✓
      → 选择模板 ✓
      → 生成PPT作品 ✓
      → 导出下载 ✓
      PPT已下载到桌面: 人工智能发展趋势.pptx (25MB)
```

## 命令参考

### 一键生成（推荐）

```bash
bash scripts/aippt.sh generate <标题> [template_id] [output_path] [format]
```

**参数:**
| 参数 | 必需 | 说明 |
|------|------|------|
| 标题 | ✅ | PPT 主题 |
| template_id | ❌ | 模板 ID (不指定则随机选择) |
| output_path | ❌ | 输出文件路径 (默认: skill目录下) |
| format | ❌ | ppt(默认) / pdf / word |

### 分步操作

| 命令 | 说明 |
|------|------|
| `auth` | 获取/刷新 Token |
| `create <标题> [type]` | 创建任务 |
| `create_with_file <文件> [type]` | 从文件创建 |
| `create_from_url <URL>` | 从网页创建 |
| `outline <task_id>` | 获取大纲 (SSE 流式) |
| `content <task_id> [template_id]` | 触发内容生成 → 返回 ticket |
| `check <ticket>` | 检查生成状态 |
| `wait <ticket> [timeout]` | 等待内容生成完成 |
| `templates [page] [size]` | 搜索模板 |
| `options` | 获取模板筛选选项 |
| `save <task_id> <template_id>` | 生成 PPT 作品 |
| `export <design_id> [format]` | 触发导出 |
| `export_result <task_key>` | 查询导出结果 |
| `wait_export <task_key>` | 等待导出完成 |
| `download <task_id> <tpl_id> <path>` | 生成+导出+下载三合一 |

## API 流程详解

### 完整生成流程 (8 步)

```
┌─────────┐   ┌─────────┐   ┌──────────┐   ┌───────────────┐
│ 1.创建  │──▶│ 2.大纲  │──▶│ 3.触发   │──▶│ 4.轮询等待    │
│ 任务    │   │ (SSE)   │   │ 内容生成 │   │ (ticket)      │
│ ~0.3s   │   │ ~6s     │   │ ~1.5s    │   │ ~25s          │
└─────────┘   └─────────┘   └──────────┘   └───────┬───────┘
                                                     │
┌─────────┐   ┌─────────┐   ┌──────────┐   ┌───────▼───────┐
│ 8.下载  │◀──│ 7.轮询  │◀──│ 6.触发   │◀──│ 5.生成作品    │
│ 文件    │   │ 导出结果│   │ 导出     │   │ (save)        │
│ ~6s     │   │ ~18s    │   │ ~0.3s    │   │ ~10s          │
└─────────┘   └─────────┘   └──────────┘   └───────────────┘

总耗时: 约 60-90 秒
```

### 关键接口说明

#### 1. 鉴权 — `GET /api/grant/token/`
- HMAC-SHA1 签名: `"GET@/api/grant/token/@{timestamp}"`
- Token 有效期: 3 天 (259200秒)
- 自动缓存到 `.token_cache.json`

#### 2. 创建任务 — `POST /api/ai/chat/v2/task`
- `type=1`: 智能生成 (输入标题)
- `type=3/4/5/7/8/9/10`: 文件导入
- `type=16`: URL 导入
- 返回 `task_id`

#### 3. 获取大纲 — `GET /api/ai/chat/outline?task_id={id}`
- **SSE (Server-Sent Events) 流式返回**
- `event:message` + `data:{"content":"..."}` 片段
- `event:close` + `data:api-close` 结束
- 大纲为 Markdown 格式 (H1-H4 层级)

#### 4. 触发内容生成 — `GET /api/ai/chat/v2/content?task_id={id}`
- 可选传 `template_id`
- ⚠️ **返回 `ticket`（不是 task_id!）** 后续轮询必须用 ticket

#### 5. 轮询生成状态 — `GET /api/ai/chat/v2/content/check?ticket={ticket}`
- ⚠️ **参数是 `ticket`，不是 `task_id`!** 这是最常见的错误
- `status: 1` = 生成中
- `status: 2` = 完成

#### 6. 生成作品 — `POST /api/design/v2/save`
- 参数: `task_id` + `template_id` (都必需)
- 返回 `design_id` (PPT 作品 ID)
- 耗时约 10 秒

#### 7. 触发导出 — `POST /api/download/export/file`
- 参数: `id`(design_id), `format`(ppt/pdf/png/word), `edit`(true/false)
- 返回 `task_key`

#### 8. 查询导出结果 — `POST /api/download/export/file/result`
- 参数: `task_key`
- 完成时返回下载 URL 数组
- 建议 3 秒间隔轮询

### 创建类型一览

| type | 说明 | 输入 |
|------|------|------|
| 1 | 智能生成 | 标题文本 |
| 3 | Word 导入 | .doc/.docx 文件 |
| 4 | XMind 导入 | .xmind 文件 |
| 5 | FreeMind 导入 | .mm 文件 |
| 7 | Markdown 导入 | .md 文件 |
| 8 | PDF 导入 | .pdf 文件 |
| 9 | TXT 导入 | .txt 文件 |
| 10 | PPTX 导入 | .ppt/.pptx 文件 |
| 16 | URL 导入 | 网页链接 |

### 导出格式

| format | 说明 |
|--------|------|
| ppt | PPTX 文件 (默认) |
| pdf | PDF 文件 |
| png | PNG 图片 |
| word | Word 文档 |

### 错误码

| code | 说明 | 处理方式 |
|------|------|----------|
| 40007 | 余额不足 | 充值或联系管理员 |
| 40008 | 功能未开通 | 开通相应服务 |
| 43101 | Token 过期 | 删除缓存重新认证 |
| 43102 | 签名错误 | 检查 Secret Key |
| 12100 | AI 生成失败 | 重试或换标题 |
| 12101 | 内容审核失败 | 修改内容 |

## 文件结构

```
aippt-skill/
├── SKILL.md           ← 本文件 (Skill 文档)
├── skill.json         ← Skill 元数据 & 触发器
├── scripts/
│   └── aippt.sh       ← API 集成脚本 (v2.0)
├── .env               ← API 密钥 (不要提交到版本库!)
└── .token_cache.json  ← Token 缓存 (自动生成)
```

## 对接 OpenClaw 的使用指南

当用户要求生成 PPT 时，助手应:

1. **确认主题**: 明确 PPT 标题/内容
2. **执行生成**: 调用 `bash scripts/aippt.sh generate "标题"`
3. **实时反馈**: 将 stderr 上的进度信息告知用户
4. **交付文件**: 报告文件路径和大小

如果用户有特殊需求:
- 指定模板: 先用 `templates` 搜索，再传 `template_id`
- 从文件生成: 用 `create_with_file` 代替 `create`
- 从网页生成: 用 `create_from_url` 代替 `create`
- 导出 PDF: 在 `generate` 命令中指定 `format=pdf`

## 已知限制 & 改进建议

### 当前限制
1. **SSE 大纲不可编辑**: 大纲生成后无法修改再生成，需要新建任务
2. **模板只有封面图**: 搜索结果只有 `id` 和 `cover_img`，无法预览排版效果
3. **无进度百分比**: 内容生成只有"进行中/完成"两个状态
4. **导出耗时较长**: PPT 渲染+导出约需 30 秒

### 建议 AiPPT 改进
1. ⭐ 支持大纲编辑后重新生成内容
2. ⭐ 模板搜索返回更多元数据 (名称、风格标签、页数)
3. 内容生成增加进度百分比
4. 提供 Webhook 回调替代轮询
5. 支持批量生成

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 2.2.0 | 2026-03-10 | 修复: 文件hidden flag问题, 去掉xattr hack, 多格式导出顺序执行, 文件格式验证 |
| 2.1.0 | 2026-03-10 | 修复: 多格式导出改为顺序执行(避免队列满20003), 增加文件验证, generate支持多格式 |
| 2.0.0 | 2026-03-10 | 重写: 修复 ticket/task_id 混淆, 补全 save+export 流程, 支持一键 generate |
| 1.0.0 | 2026-03-04 | 初版: 基础 API 调用 |
