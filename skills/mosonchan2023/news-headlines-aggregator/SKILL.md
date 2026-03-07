---
name: news-headlines-aggregator
version: 1.0.0
description: Aggregate top headlines from multiple sources in real-time. Most popular news skill. Each call charges 0.001 USDT via SkillPay.
category: News
tags:
  - news
  - headlines
  - aggregator
  - trending
  - popular
author: moson
price: 0.001
currency: USDT
triggers:
  - "latest news"
  - "top headlines"
  - "news aggregator"
  - "breaking headlines"
  - "news feed"
config:
  NEWS_API_KEY:
    type: string
    required: false
    secret: true
---

# News Headlines Aggregator

## 功能

- 实时聚合多个新闻源的头条
- 按类别筛选 (科技/商业/体育/娱乐)
- 支持关键词过滤
- 实时更新热门新闻

## 使用方法

```json
{
  "category": "technology",
  "country": "us",
  "limit": 10
}
```

## 输出

```json
{
  "success": true,
  "totalResults": 25,
  "headlines": [
    {"title": "...", "source": "Reuters", "url": "...", "publishedAt": "..."}
  ]
}
```

## 定价

每次调用: 0.001 USDT
