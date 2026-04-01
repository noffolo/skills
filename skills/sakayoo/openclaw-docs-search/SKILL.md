---
name: "openclaw-docs-search"
description: "Search OpenClaw official docs and return concise Markdown. Invoke when users ask about OpenClaw docs, config, CLI, channels, or skills."
homepage: "https://docs.openclaw.ai/"
user-invocable: true
---

# openclaw-docs-search

用于检索 OpenClaw 官方文档，并将结果整理为适合 LLM 阅读的 Markdown。

## ⚡ 快速使用（必读）

### 前置条件：安装依赖

首次使用前需要安装依赖：
```bash
cd ~/.openclaw/workspace/skills/openclaw-docs-search
npm install
```

### 命令一：搜索文档

```bash
node ~/.openclaw/workspace/skills/openclaw-docs-search/dist/search.js search "<英文关键字>" en
```

- **英文搜索**（推荐）: `... search "multi agent" en`
- **中文搜索**: `... search "多代理" zh-Hans`

示例：
```bash
node ~/.openclaw/workspace/skills/openclaw-docs-search/dist/search.js search "create multiple agents" en
```

返回格式化的 Markdown 搜索结果，包含页面路径（`page` 字段），后续可用于获取详情。

### 命令二：获取文档详情

从搜索结果中获取 `page` 路径后，使用此命令获取完整内容：

```bash
node ~/.openclaw/workspace/skills/openclaw-docs-search/dist/search.js doc "<page路径>"
```

示例：
```bash
node ~/.openclaw/workspace/skills/openclaw-docs-search/dist/search.js doc "concepts/multi-agent"
```

返回干净的 Markdown 正文（自动提取 `#content-area` 并转换为 Markdown）。

---

## 适用场景

- 用户询问 OpenClaw 的安装、配置、CLI、渠道接入、Skills、Gateway、诊断或运维问题
- 需要快速定位某个官方文档页面并返回简洁摘要
- 需要进一步读取单篇文档正文，并尽量减少噪音与 Token 消耗

> **⚠️ 重要提示：**
> 由于官方英文文档的搜索命中率远高于中文文档，**请在发起搜索前，务必将用户的中文查询意图翻译为英文关键字进行搜索**。接口默认语言已设置为 `en`。如果确实需要查阅中文结果，再显式将 `language` 指定为 `zh-Hans`。

---

## 工作原理

### 搜索流程

1. 向 OpenClaw 官方搜索 API 发送请求
2. 获取 JSON 结果，提取 `page`、`breadcrumbs`、`content` 等字段
3. 清理 HTML 标签（如 `<mark>` 高亮），格式化为 Markdown

返回示例：
```markdown
### 1. Agents > Multi-agent > Multi-Agent Routing
- **路径**: `concepts/multi-agent`
- **内容**: Multi-Agent Routing Goal: multiple isolated agents...
```

### 获取详情流程

1. 拼接 URL：`https://docs.openclaw.ai/<page路径>`
2. 获取 HTML 页面
3. 提取 `id="content-area"` 元素
4. 使用 `turndown` 转换为 Markdown
5. 添加来源标识：`> 来源: https://docs.openclaw.ai/...`

## 输出要求

- 搜索结果优先返回精简 Markdown，而不是原始 JSON
- 删除搜索高亮标签、冗余元数据、重复标题和无关噪音
- 详情页只保留 `#content-area` 主内容，不返回整页导航、页脚或脚本内容
- 在结果中尽量保留来源路径，便于后续继续深挖

## 约束

- 不批量镜像整个站点
- 不请求与文档正文无关的敏感页面
- 不返回真实密钥、令牌或用户私密信息
- 优先以"按需查阅"的方式工作，减少不必要请求

## 常见问题

### 搜索无结果？

1. 尝试用更通用的英文关键词
2. 使用官方文档目录探索：`https://docs.openclaw.ai/llms.txt`

### 依赖安装失败？

确保 Node.js 版本 >= 18，然后重试：
```bash
cd ~/.openclaw/workspace/skills/openclaw-docs-search
rm -rf node_modules package-lock.json
npm install
```
