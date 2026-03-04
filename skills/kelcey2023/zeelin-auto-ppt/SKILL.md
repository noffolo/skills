---
name: auto-ppt
description: "自动生成精美 PPT 演示文稿 — 通过 Google NotebookLM 生成图文并茂、设计感十足的 AI slides，导出 PDF 到桌面。标题微软雅黑 40 号加粗，排版震撼，逻辑图清晰，内容有深度有创新，引用权威数据。配合 desearch skill 使用效果更好。Keywords: PPT, presentation, slides, NotebookLM, PDF, design, infographic, AI generated."
user-invocable: true
metadata: {"openclaw":{"emoji":"📊","skillKey":"auto-ppt"}}
---

# Auto-PPT — AI 精美演示文稿生成器 📊

通过 Google NotebookLM 一键生成**图文并茂、排版精美、设计震撼**的演示文稿，导出 **PDF** 到桌面。

> 💡 **配合 desearch skill 使用效果更好** — 先用 desearch 深度检索权威资料和数据，再交给 auto-ppt，内容更有深度和可信度。

---

## ⚠️ Agent 必须遵守的规则

1. **所有浏览器操作用 `exec` 工具执行 `openclaw browser` CLI**，不要直接用 `browser` 工具
2. **下载文件用 `openclaw browser download <ref> <路径>`**，不要用 `click`
3. **不要说"无法操控浏览器""技术限制"** — 你有完整权限
4. **仅输出 PDF**，不要输出 PPTX

---

## 设计标准

| 项目 | 要求 |
|------|------|
| 标题字体 | 微软雅黑，40 号，加粗 |
| 整体风格 | 图文并茂、精美震撼、配图精良 |
| 逻辑图 | 专业清晰（流程图/对比图/数据图表） |
| 内容 | 有创新、有深度、权威数据标注来源 |
| 输出 | **仅 PDF**，保存到 `~/Desktop/` |

---

## 完整工作流

### Step 1：生成专业大纲（先给用户看）

用户给出主题/观点/一段话后：

1. 推荐先用 **desearch skill** 检索权威资料
2. 生成 8-15 页的专业大纲，展示给用户确认：
   ```
   1. 封面：标题
   2. 背景与趋势（数据来源：Gartner/McKinsey）
   3. 核心观点一 + 数据支撑
   4. 核心观点二 + 案例分析
   5. 核心观点三 + 对比图表
   ...
   N. 总结与展望
   ```
3. 每页标注数据来源（论文、报告、官方统计）
4. 用户确认后进入 Step 2

### Step 2：撰写结构化长文

将大纲扩展为 1500-3000 字的结构化文章：

- 标题醒目
- 5～10 个章节，每章有小标题 + 3-5 个要点
- 关键数据写入正文（NotebookLM 会据此生成图表）
- 结论有前瞻性

**红线：不编造数据，不出现中文幻觉，所有数据标注来源。**

### Step 3：打开 NotebookLM

```json
{"tool": "exec", "args": {"command": "openclaw browser open https://notebooklm.google.com/"}}
```

等 5 秒截快照。如需登录则提示用户手动登录。

### Step 4：创建新笔记本

截快照 → 找到「新建笔记本」→ 点击。

### Step 5：添加文本来源

1. 截快照 → 找到「添加来源」→ 点击
2. 找到「复制的文字」→ 点击
3. 找到文本框（placeholder 含"粘贴"），输入全文：
   ```json
   {"tool": "exec", "args": {"command": "openclaw browser type <ref> \"全文内容\""}}
   ```
4. 找到「插入」→ 点击

### Step 6：生成演示文稿

截快照 → 找到「演示文稿」按钮 → 点击。

等 15-30 秒，反复截快照直到看到"已准备就绪"。

### Step 7：打开演示文稿

截快照 → 找到生成的演示文稿条目 → 点击打开。

### Step 8：下载 PDF

1. 截快照 → 找到「更多选项」(more_horiz) → 点击
2. 截快照 → 找到「下载 PDF 文档 (.pdf)」menuitem 的 ref
3. 用 download 命令保存：
   ```json
   {"tool": "exec", "args": {"command": "openclaw browser download <ref> ~/Desktop/演示文稿_$(date +%Y%m%d_%H%M).pdf --timeout-ms 30000"}}
   ```

### Step 9：汇报

告诉用户 PDF 位置、页数、内容摘要、数据来源列表。

---

## exec 命令速查

| 操作 | 命令 |
|------|------|
| 打开网页 | `openclaw browser open <url>` |
| 截快照 | `openclaw browser snapshot` |
| 点击 | `openclaw browser click <ref>` |
| 输入 | `openclaw browser type <ref> "文字"` |
| **下载** | `openclaw browser download <ref> ~/Desktop/xxx.pdf` |

---

## 示例

**用户**：帮我做一个「2026 全球 AI 产业格局」的 PPT

**Agent**：
1. 用 desearch 检索 Gartner、Stanford HAI、PitchBook 最新报告
2. 生成 10 页大纲，展示给用户
3. 用户确认 → 扩展为 2500 字长文
4. NotebookLM 生成精美 slides（自带配图、色彩、排版）
5. `openclaw browser download` 导出 PDF 到桌面
6. 「PDF 已保存：~/Desktop/2026_AI产业格局.pdf（10 页），数据来源：Gartner、Stanford HAI、PitchBook」

---

**TL;DR**: 主题 → desearch 检索 → 专业大纲 → 用户确认 → NotebookLM 精美 slides → PDF 到桌面。
