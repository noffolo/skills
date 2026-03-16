---
name: binance-narrative-newsroom
description: 当用户想发现今天最值得写的 Binance 市场热点、判断当前叙事所处阶段、整理 watchlist、生成 Binance Square 中文草稿，或输出一张适合分享的热点卡片时使用。
---

# 币安叙事总编室

这个 skill 不审 prompt，也不审交易权限。

它做的是：
从 Binance 官方公开的 Web3 榜单和 Smart Money 信号里，整理出今天最值得写的市场叙事。

公开接口：

- 选题 API: `https://binance-narrative-newsroom.vercel.app/api/newsroom`
- 分享图 API: `https://binance-narrative-newsroom.vercel.app/api/newsroom/share-image`

## 适用场景

- 用户想知道今天 Binance 生态里哪条热点最值得写
- 用户需要一版可直接发到 Binance Square 的中文草稿
- 用户想用“社交热度 + 统一热榜 + 聪明钱流入 + Smart Money”来做判断
- 用户想得到 watchlist 和反方风险提示，而不是一个简单热榜

## 调用方式

如果用户没有特别指定，默认使用：

- `audience`: `SQUARE`
- `angle`: `MORNING`

可选参数：

- `audience`
  - `TRADER`
  - `SQUARE`
  - `COMMUNITY`
- `angle`
  - `MORNING`
  - `SMART_MONEY`
  - `CONTRARIAN`

调用：

```bash
curl -sS -X POST https://binance-narrative-newsroom.vercel.app/api/newsroom \
  -H 'Content-Type: application/json' \
  -d '{"audience":"SQUARE","angle":"MORNING"}'
```

## 重点字段

- `headline`
- `deckSummary`
- `editorialDecision`
- `leadStory`
- `boardStories`
- `watchlist`
- `avoidList`
- `squareDraft`
- `shareText`

## 输出要求

- 先告诉用户今天的头条选题是什么
- 再解释为什么是这条线，而不是简单复述榜单
- 明确区分：
  - 可写热点
  - 观察名单
  - 不建议直接追的对象
- 如果用户要发帖，直接给 `squareDraft`
- 如果用户要分享图，把以下字段编码后拼到分享图接口：
  - `symbol`
  - `stage`
  - `resonanceScore`
  - `headline`
  - `summary`
  - `watchline`
  - `generatedAt`
