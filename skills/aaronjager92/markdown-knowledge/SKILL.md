---
AIGC:
    ContentProducer: aaronjager92
    ContentPropagator: aaronjager92
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3044022034e6daf3f0786d21ef2568623a1e6e0a36e3cd41ea3e0baa508e44e5ace196e502200fb1cf2cb5a2c9f27df76bc0586fe9afae2999b1240778c4e4c3e9f965ba2dbe
    ReservedCode2: 304602210087b45b240f07e5b9bd5299bcccc081cb20a5d346accf5e315a2a557e8b79d3dd022100ffd28c9922852e0eed62b2c3af92f4aa8d78f60222521061213a0d0d4518cf54
author: aaronjager92
defaults:
    auto_refresh: true
    knowledge_path: ~/Knowledge
    index_path: ~/.openclaw/skills/markdown-knowledge/index.json
    search_top_k: 3
description: 将本地 Markdown 知识库与 OpenClaw 集成，支持语义检索和上下文注入
homepage: https://github.com/your-repo/markdown-knowledge
license: MIT
name: markdown-knowledge
tags:
    - markdown-knowledge
    - markdown
    - retrieval
    - productivity
triggers:
    - action: search
      description: 检索知识库相关内容
      patterns:
        - "搜索知识库"
        - "查一下知识库"
        - "知识库里"
        - "查知识库"
        - "知识库搜索"
        - "知识库查询"
    - action: rebuild
      description: 重建知识库索引
      patterns:
        - "刷新知识库"
        - "更新知识库"
        - "重建知识库"
        - "刷新知识库索引"
        - "更新知识库索引"
        - "重建知识库索引"
    - action: stats
      description: 查看知识库统计
      patterns:
        - "知识库统计"
        - "查看知识库"
        - "知识库状态"
version: 1.1.0
---

# Markdown Knowledge Base

将您的本地 Markdown 知识库与 OpenClaw 无缝集成，让 AI 助手能够基于您的专业知识回答问题。

> 📖 **完整文档：** 请参阅 [PROJECT.md](./PROJECT.md) 获取详细的中英文双语说明。
> **Full Documentation:** See [PROJECT.md](./PROJECT.md) for complete bilingual documentation.

---

## 💡 AI 使用指南（重要）

当用户提问时，AI 应遵循以下流程：

### 1. 收到问题 → 立即搜索知识库

当用户的问题**匹配触发词**（如"搜索知识库"、"查一下知识库"等）时，**调用 search 动作**检索本地知识库：
```
search 动作，输入：用户问题的关键词
```

### 2. 搜到结果 → 注入上下文并回答

如果知识库有相关内容：
- 将相关文档片段作为上下文
- 告诉用户"根据知识库《文档标题》..."
- 引用关键内容回答

### 3. 搜不到结果 → 明确告知

如果知识库没有相关内容：
- 告诉用户"知识库中没有找到相关信息"
- 然后基于通用知识回答
- 可以建议用户补充相关文档

### 4. 知识库文档格式

Markdown 文档建议包含以下头部信息（提高检索精度）：

```markdown
---
title: 文档标题
keywords: 关键词1, 关键词2
tags: [标签1, 标签2]
created: 2024-01-15
---

# 文档标题

正文内容...
```

---

## 🔧 手动触发命令

用户可以直接说以下命令触发知识库操作：

| 用户说法 | 触发动作 | 说明 |
|----------|----------|------|
| "刷新知识库索引" | rebuild | 立即重建索引 |
| "更新知识库" | rebuild | 立即重建索引 |
| "重建知识库索引" | rebuild | 立即重建索引 |
| "知识库统计" | stats | 查看索引统计 |
| "查看知识库" | stats | 查看索引统计 |

---

## 快速开始

### 安装

```bash
clawhub install markdown-knowledge
```

### 首次使用

安装后先构建索引：

```bash
python3 knowledge_base.py init
python3 knowledge_base.py build
```

### 配置知识库路径

编辑 `~/.openclaw/skills/markdown-knowledge/config.json`：

```json
{
    "knowledge_path": "~/Knowledge",
    "index_path": "~/.openclaw/skills/markdown-knowledge/index.json",
    "search_top_k": 3,
    "auto_refresh": true
}
```

将你的 Markdown 文件放入 `~/Knowledge` 目录即可。

---

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `knowledge_path` | string | `~/Knowledge` | Markdown 文档目录 |
| `index_path` | string | `~/.openclaw/skills/markdown-knowledge/index.json` | 索引文件路径 |
| `search_top_k` | number | `3` | 返回结果数量 |
| `auto_refresh` | boolean | `true` | 自动刷新索引 |

---

## 工作原理

```
用户提问
    ↓
AI 调用 search 动作
    ↓
检索本地 Markdown 知识库
    ↓
匹配最相关的文档片段
    ↓
注入上下文 → AI 回答
```

---

## 系统要求

- Python 3.8+
- OpenClaw 1.0+
- 本地 Markdown 文档目录

---

## 支持平台

- ✅ 树莓派
- ✅ Linux
- ✅ macOS
- ✅ Windows

---

## ⚠️ GlobalMemory 全局注入模块（可选功能，默认禁用）

`lib/global_memory.py` 是独立的全局注入模块，**默认不启用**。

**用途**：如果被挂载到 OpenClaw 全局，它会在**每次对话**中自动检索知识库并注入上下文，可能影响所有对话。

**当前状态**：已禁用，不影响常规使用。

**如需启用**（仅推荐高级用户）：
1. 确认了解 GlobalMemory 的行为影响
2. 手动将其挂载到 OpenClaw 的全局 hooks
3. 注意：这会对所有对话注入知识库上下文
