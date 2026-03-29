---
name: readgzh
displayName: "ReadGZH — 微信公众号文章 AI 阅读器"
type: skill
version: 1.3.4
author: sweeyeah
description: "让 AI 读懂微信公众号。自研 7 阶段提取管线，99.89% 穿透反爬，Token 消耗降低 50–87%。支持 ChatGPT、Claude、Perplexity、Gemini 等平台无缝引用。| Let AI read and understand WeChat Official Accounts. Self-developed 7-stage extraction pipeline, 99.89% anti-crawl penetration, Token consumption reduced by 50–87%. Supports ChatGPT, Claude, Perplexity, Gemini and more."
tags: wechat, scraper, ai-reading, markdown, china
category: utility
---

# ReadGZH — 微信公众号文章 AI 阅读器

ReadGZH 是一款专为 AI 智能体设计的微信公众号内容解析工具。它通过服务端代理绕过微信的反爬虫机制，将复杂的公众号 HTML 转换为纯净、结构化的 Markdown 内容，大幅节省 Token 消耗。

## 🚀 核心特性 (Key Features)

- **99.89% 穿透率**：自研 7 阶段提取管线，完美绕过客户端指纹检测与反爬拦截。
- **50-87% Token 节省**：自动剥离内联样式、冗余标签及广告干扰，输出极简 Markdown。
- **CDN 永久代理**：将图片路由至持久化 CDN，解决微信图片 2 小时过期的硬伤。
- **全球共享缓存**：转换过的文章永久入库，后续任何用户或 Agent 读取均**完全免费**。
- **零安装依赖**：纯云端 API 模式，无需本地微信客户端或浏览器环境。
- **原生支持 MCP**：内置 Model Context Protocol，支持 AI Agent 协议化直接调用。

## 🛠️ 如何使用 (Usage)

直接对你的 AI 助手下令：
> **“帮我读一下这篇文章：[微信公众号链接]”**

## 📡 API 与集成 (API & Integration)

由 **[readgzh.site](https://readgzh.site)** 提供技术支持。

### 开发者入口
- **API 基础地址**: `https://api.readgzh.site`
- **MCP 服务端**: `POST https://api.readgzh.site/mcp-server`
- **文档中心**: [readgzh.site/docs](https://readgzh.site/docs)
- **免费 Key 领取**: [readgzh.site/dashboard](https://readgzh.site/dashboard) (每日 50 次免费额度)

## 🛡️ 开发者 (Identity)
由 **[Sweesama](https://github.com/sweesama)** 开发并维护。
