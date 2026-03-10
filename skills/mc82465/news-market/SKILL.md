---
name: news_market
description: 专注中国A股市场资讯查询。获取中国热点要闻，包含人民网时政、新浪财经、东方财富、36氪、澎湃新闻、环球网、财联社、雪球、观察者网、IT之家（通过https://skillsmp.com/zh/skills/countbot-ai-countbot-skills-news-skill-md改造而成的）。
---

# 新闻与资讯查询

通过 RSS 源和网页抓取获取热点要闻，支持关键词过滤。
## 无需配置

此技能开箱即用，无需 API Key。

## 命令行调用

```bash
# 获取热点新闻（默认）
python3 skills/news_market/scripts/news_market.py hot

# 关键词搜索
python3 skills/news_market/scripts/news_market.py hot --keyword AI

# 控制摘要长度（默认 100 字符）
python3 skills/news_market/scripts/news_market.py hot --detail 500    # 显示 500 字符摘要
python3 skills/news_market/scripts/news_market.py hot --detail -1     # 显示全文
python3 skills/news_market/scripts/news_market.py hot --detail 0      # 不显示摘要

# 指定返回条数
python3 skills/news_market/scripts/news_market.py hot --limit 20

# JSON 格式输出（包含完整正文，不截断）
python3 skills/news_market/scripts/news_market.py hot --json

# 查看所有支持的分类和来源
python3 skills/news_market/scripts/news_market.py sources
```

## 支持的新闻分类

| 分类 | 参数值 | 来源 |
|------|--------|------|
| 热点要闻 | `hot` | 人民网、新浪财经、东方财富、36氪、澎湃新闻、环球网、财联社、雪球 |

## AI 调用场景

用户说"今天有什么新闻"：

```bash
python3 skills/news_market/scripts/news_market.py hot --limit 60
```

用户想深入阅读某篇文章：

```bash
# 使用 --detail -1 获取 RSS 全文内容
python3 skills/news_market/scripts/news_market.py hot --keyword "关键词" --detail -1 --limit 5

# 或使用 --json 获取完整 JSON（含全文）
python3 skills/news_market/scripts/news_market.py hot --keyword "关键词" --json --limit 5
```

获取新闻后，整理为简洁的列表返回给用户，包含标题、来源和链接。英文内容可适当翻译摘要。

### 深入阅读策略

当用户想详细了解某篇新闻时，按以下优先级获取全文：

1. **首选：`--detail -1` 或 `--json`** — 直接从 RSS 源获取全文内容，无需额外网络请求
2. **备选：`web_fetch`** — 人民网、澎湃新闻、36氪等中文站点通常允许抓取

## 注意事项

- 纯 Python 标准库实现，无需额外依赖
- RSS 源可能因网站调整而失效，脚本会自动跳过失败的源
- 中文新闻源（人民网、澎湃、36氪等）通常允许 `web_fetch` 抓取详情页
