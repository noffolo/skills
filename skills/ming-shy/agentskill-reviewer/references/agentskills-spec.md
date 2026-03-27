# AgentSkills 规范参考

本文档总结 AgentSkills 的核心规范要求，供评审时参考。

## 核心原则

### 1. 简洁至上 (Concise is Key)
- **默认假设 Codex 很聪明**：只添加 Codex 不知道的信息
- **挑战每段内容**："Codex 真的需要这个解释吗？"
- **token 是公共资源**：skill 要与其他内容共享上下文窗口
- **优先示例而非冗长解释**

### 2. 渐进式披露 (Progressive Disclosure)
三级加载系统：
1. **Metadata (name + description)** - 始终在上下文（~100 词）
2. **SKILL.md body** - 触发后加载（<5k 词，建议 <500 行）
3. **Bundled resources** - 按需加载（无限制）

### 3. 设置适当的自由度 (Degrees of Freedom)
- **高自由度**：文本指令，多种方法都有效时
- **中等自由度**：伪代码/参数化脚本，存在首选模式时
- **低自由度**：具体脚本/少参数，操作脆弱或必须一致时

## 必需结构

### SKILL.md 结构
```markdown
---
name: skill-name (必需)
description: 功能说明 + 触发条件 (必需)
---

# Skill Name

[指令和指导内容]
```

### 目录结构
```
skill-name/
├── SKILL.md (必需)
├── scripts/ (可选) - 可执行代码
├── references/ (可选) - 按需加载的文档
└── assets/ (可选) - 输出中使用的文件
```

## YAML Frontmatter 要求

### name（必需）
- 小写字母、数字、连字符
- 短小精悍，动词引导
- 工具命名空间化（如 `gh-address-comments`）

### description（必需）
**这是主要触发机制，必须包含：**
1. **功能说明**：skill 做什么
2. **触发条件**：何时使用（具体场景、关键词）

**示例：**
- ❌ 差："处理 PDF"（太模糊）
- ✅ 好："读取、编辑、合并、分割 PDF 文件。支持文本提取、页面旋转、水印添加。当用户要求操作 .pdf 文件、提取 PDF 内容、PDF 格式转换时使用。"

**注意：**
- 所有"何时使用"信息必须在 description，不能在 body
- Body 只在触发后才加载，所以 body 中的"When to Use"无效

## Body 内容要求

### 长度控制
- **建议 <500 行**
- 接近此限制时拆分到 references/

### 内容质量
- ✅ 提供 Codex 不知道的程序性知识
- ✅ 特定领域的细节
- ✅ 工作流程、工具集成指导
- ❌ 重复 Codex 已知的常识
- ❌ 过度解释显而易见的步骤
- ❌ 在 SKILL.md 和 references/ 重复内容

### 写作风格
- **祈使句/不定式形式**（如 "Read the file" 而非 "You should read"）
- **简洁示例优于冗长解释**
- **清晰的结构**：标题、列表、代码块

## Bundled Resources 指南

### scripts/ - 可执行代码
**何时使用：**
- 重复编写相同代码
- 需要确定性可靠性

**要求：**
- 可执行权限
- Shebang（如 `#!/usr/bin/env python3`）
- 基本错误处理
- 注释说明用途

### references/ - 按需文档
**何时使用：**
- 详细参考资料（API 文档、schema、策略）
- 多框架/多变体支持
- 长内容（>10k 词）

**组织模式：**
- 按领域组织（如 finance.md、sales.md）
- 按框架组织（如 aws.md、gcp.md）
- 在 SKILL.md 中明确引用并说明何时加载

**最佳实践：**
- 避免深度嵌套（所有 references 从 SKILL.md 直接引用）
- 长文件（>100 行）应有目录
- 内容只存在一处（SKILL.md 或 references/，不重复）

### assets/ - 输出资源
**何时使用：**
- 模板、图片、图标
- 样板代码、字体
- 输出中使用但不需要加载到上下文的文件

**示例：**
- logo.png、slides.pptx
- frontend-template/
- font.ttf

## 禁止的内容

### 不应存在的文件
- ❌ README.md
- ❌ INSTALLATION_GUIDE.md
- ❌ QUICK_REFERENCE.md
- ❌ CHANGELOG.md
- ❌ 其他辅助文档

**原因：** Skill 只应包含 AI 执行任务所需的信息，不应包含人类阅读的辅助文档。

## 命名规范

### Skill 名称
- 小写字母、数字、连字符
- 动词引导的短语
- 工具命名空间（必要时）
- <64 字符
- 目录名与 skill 名称完全一致

**示例：**
- ✅ `pdf-editor`
- ✅ `gh-address-comments`
- ❌ `PDF_Editor`
- ❌ `pdfEditor`

## 渐进式披露模式

### 模式 1：高层指南 + 引用
```markdown
# PDF Processing

## Quick start
[核心示例]

## Advanced features
- **Form filling**: See [FORMS.md](references/FORMS.md)
- **API reference**: See [REFERENCE.md](references/REFERENCE.md)
```

### 模式 2：按领域组织
```
bigquery-skill/
├── SKILL.md (概览和导航)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

### 模式 3：条件细节
```markdown
## Editing documents
基本编辑直接修改 XML。

**For tracked changes**: See [REDLINING.md](references/REDLINING.md)
**For OOXML details**: See [OOXML.md](references/OOXML.md)
```

## 安全原则

- 谨慎处理外部操作（邮件、推文、公开发帖）
- 脚本不应允许任意命令注入
- 优先使用 `trash` 而非 `rm`
- 不确定时应询问用户

---

本文档基于 OpenClaw 官方 skill-creator 规范整理，供 skill-reviewer 评审时参考。
