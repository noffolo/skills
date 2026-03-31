---
name: bocha-search-python
description: 博查搜索 (Bocha Search) 的 Python 实现技能，提供增强的网页搜索能力。当用户需要通过博查 AI 搜索 API 进行网页搜索、获取联网信息、查找最新资讯或中文内容时使用此技能。与现有的 JavaScript 版本相比，本技能提供更稳定的连接、更灵活的输出格式（原始 JSON/Brave 兼容格式/Markdown）、更好的错误处理和重试机制。适用于 AI Agent 需要联网搜索、RAG 应用获取网页摘要、中文内容检索等场景。
---

# 博查搜索 Python 版 (Bocha Search Python)

## 概述

博查搜索 Python 版是一个增强的博查 AI 搜索 API 客户端，专为 AI Agent 和自动化工作流设计。相比现有的 JavaScript 版本，本技能提供：

- **更稳定的连接**：内置重试机制和错误处理
- **灵活的输出格式**：支持原始 JSON、Brave/Bing 兼容格式和 Markdown
- **多重配置来源**：.env 文件、环境变量
- **完整的时间范围过滤**：支持精确日期和日期范围
- **详细的错误信息**：帮助快速诊断问题

## 快速开始

### 1. 配置 API 密钥

提供 API 密钥的两种方式（按优先级排序）：

1. **`.env` 文件**：在 `~/.openclaw/.env` 中添加（优先级最高）
   ```
   BOCHA_API_KEY=sk-your-api-key
   ```

2. **环境变量**：设置 `BOCHA_API_KEY`
   ```bash
   export BOCHA_API_KEY="sk-your-api-key"
   ```

> API 密钥获取：访问 https://open.bochaai.com → API KEY 管理

### 2. 基本搜索

```bash
# 使用位置参数
python3 scripts/search.py "沪电股份"

# 使用 --query 选项
python3 scripts/search.py --query "人工智能" --count 5

# 返回详细摘要
python3 scripts/search.py "DeepSeek" --summary

# 限制时间范围
python3 scripts/search.py "AI新闻" --freshness oneWeek --count 10
```

### 3. 输出格式

```bash
# 原始 JSON 格式（API 原始响应）
python3 scripts/search.py "阿里巴巴" --format raw

# Brave/Bing 兼容格式（默认，适合 AI 使用）
python3 scripts/search.py "阿里巴巴" --format brave

# Markdown 格式（人类可读）
python3 scripts/search.py "阿里巴巴" --format md
```

## 高级用法

### 时间范围过滤

支持多种时间范围格式：

| 值 | 说明 | 示例 |
|----|------|------|
| `noLimit` | 不限时间（默认） | `--freshness noLimit` |
| `oneDay` | 一天内 | `--freshness oneDay` |
| `oneWeek` | 一周内 | `--freshness oneWeek` |
| `oneMonth` | 一个月内 | `--freshness oneMonth` |
| `oneYear` | 一年内 | `--freshness oneYear` |
| `YYYY-MM-DD` | 指定日期 | `--freshness 2025-04-06` |
| `YYYY-MM-DD..YYYY-MM-DD` | 日期范围 | `--freshness 2025-01-01..2025-04-06` |

示例：
```bash
# 搜索 2025 年 4 月的内容
python3 scripts/search.py "苹果发布会" --freshness 2025-04

# 搜索 2025 年第一季度内容
python3 scripts/search.py "财报" --freshness 2025-01-01..2025-03-31
```

### 错误处理与重试

脚本内置错误处理和重试机制：

```bash
# 设置重试次数（默认 2 次）
python3 scripts/search.py "查询" --retries 3

# 设置超时时间（默认 30 秒）
python3 scripts/search.py "查询" --timeout 60
```

### 自定义 API 端点

支持备用 API 端点：

```bash
# 使用备用端点
python3 scripts/search.py "查询" --endpoint "https://api.bocha.cn/v1/web-search"
```

## 输出示例

### Brave 兼容格式（默认）

```json
{
  "type": "search",
  "query": "阿里巴巴",
  "totalResults": 12345,
  "resultCount": 10,
  "results": [
    {
      "index": 1,
      "title": "阿里巴巴发布2024年ESG报告",
      "url": "https://www.alibabagroup.com/document...",
      "description": "阿里巴巴集团发布《2024财年环境、社会和治理（ESG）报告》...",
      "summary": "报告显示，阿里巴巴扎实推进减碳举措...",
      "siteName": "阿里巴巴集团",
      "publishedDate": "2024-07-22T00:00:00+08:00"
    }
  ]
}
```

### Markdown 格式

```markdown
## 搜索结果: 阿里巴巴
*找到约 12345 条结果*

1. **阿里巴巴发布2024年ESG报告**
   *阿里巴巴集团*
   [https://www.alibabagroup.com/document...](https://www.alibabagroup.com/document...)
   阿里巴巴集团发布《2024财年环境、社会和治理（ESG）报告》...
   *摘要*: 报告显示，阿里巴巴扎实推进减碳举措...
   *发布时间*: 2024-07-22T00:00:00+08:00
```

## 在 OpenClaw 中使用

### 直接调用脚本

```bash
# 从 OpenClaw workspace 根目录调用
python3 skills/bocha-search-python/scripts/search.py "查询"

# 使用绝对路径
python3 /root/.openclaw/workspace/skills/bocha-search-python/scripts/search.py "查询"
```

### 集成到 Agent 工作流

在 Agent 的响应中调用搜索并处理结果：

```python
# 示例：在 Python 代码中调用
import subprocess
import json

def bocha_search(query, count=5):
    cmd = [
        "python3",
        "/root/.openclaw/workspace/skills/bocha-search-python/scripts/search.py",
        "--query", query,
        "--count", str(count),
        "--format", "brave"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        raise Exception(f"搜索失败: {result.stderr}")
```

## 故障排除

### 常见错误

| 错误代码 | 原因 | 解决方案 |
|----------|------|----------|
| `INVALID_ARGUMENT` | 参数错误 | 检查查询关键词和参数格式 |
| `API_ERROR` | API 请求失败 | 检查 API 密钥和网络连接 |
| `UNKNOWN_ERROR` | 未知错误 | 查看详细错误信息并重试 |

### 调试模式

要查看更多调试信息，可以修改脚本或添加调试输出：

```python
# 在 search.py 中添加调试
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 验证 API 密钥

```bash
# 简单测试 API 密钥是否有效
curl -X POST "https://api.bochaai.com/v1/web-search" \
  -H "Authorization: Bearer YOUR-API-KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "count": 1}'
```

## 性能建议

1. **限制结果数量**：默认返回 10 条，根据需要调整
2. **使用适当的时间范围**：避免不必要的全文搜索
3. **缓存结果**：对重复查询考虑本地缓存
4. **批量处理**：避免频繁的单个请求

## 资源

### scripts/search.py
主搜索脚本，包含所有核心功能。

## 版本历史

- **0.1.0** (2026-03-27): 初始版本，基于博查搜索 API 构建，提供增强的 Python 实现
- **0.1.1** (2026-03-28): 安全改进 - 添加技能元数据声明必需的环境变量 BOCHA_API_KEY，解决安全扫描警告

## 相关技能

- `bocha-search`: 原始的 JavaScript 版本
- `tavily-search`: Tavily 搜索 API 技能
- `web_search`: 内置网页搜索工具

---

**注意**：本技能需要有效的博查 API 密钥。使用前请确保已注册并获取密钥。
