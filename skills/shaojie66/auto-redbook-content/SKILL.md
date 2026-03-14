---
name: auto-redbook-content
description: "小红书内容抓取与改写工具，支持图片识别和 OCR，输出本地 JSON 文件。触发关键词：抓取小红书笔记、自动生成小红书内容、运行 auto-redbook-content、执行小红书内容流程。"
metadata: { "openclaw": { "emoji": "📕", "requires": { "bins": ["node", "tesseract"] } } }
---

# auto-redbook-content Skill

小红书内容抓取与改写工具，支持图片识别和 OCR，输出本地 JSON 文件。

## 触发关键词
- 抓取小红书笔记
- 自动生成小红书内容
- 运行 auto-redbook-content
- 执行小红书内容流程

## 功能说明
1. 自动抓取小红书热门笔记（支持真实MCP或模拟数据）
2. 智能图片识别（Vision + OCR）
3. AI 改写内容（支持直接模式或Agent模式）
4. 结果输出到本地 JSON 文件
5. 完整错误处理和重试机制

## 环境变量
| 变量名 | 说明 | 必填 | 默认值 |
|--------|------|------|--------|
| REWRITE_MODE | 改写模式：direct（直接由当前Agent处理）或 agent（调用指定Agent处理） | 否 | direct |
| AGENT_ID | 改写使用的Agent ID，agent模式时必填 | 否 | 无 |

## 依赖工具
### 必需
- Node.js >= 14.0.0
- tesseract-ocr：图片文字提取

### 可选
- xiaohongshu MCP：抓取真实笔记（未配置时自动使用模拟数据）
- moltshell-vision：图片内容分析
- image-ocr：OCR封装工具

## 使用示例
对OpenClaw Agent说：
```
请执行 auto-redbook-content 流程，抓取 3 条小红书笔记
```
