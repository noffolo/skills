---
name: ozon-wildberries-analyzer
description: "OZON and Wildberries marketplace deep analysis agent. Market intelligence for Russian e-commerce — category trends, competitor analysis, pricing strategy, keyword research, and seller performance insights. Triggers: ozon analyzer, wildberries analysis, wb marketplace, ozon seller, russian ecommerce, wildberries trends, ozon product research, wb competitor, ozon keyword, wildberries pricing, wb seller, eastern europe ecommerce"
allowed-tools: Bash
metadata:
  openclaw:
    homepage: https://github.com/mguozhen/ozon-wildberries-analyzer
---

# OZON & Wildberries Marketplace Analyzer

Deep market intelligence for Russia's top two e-commerce platforms — OZON and Wildberries (WB). Analyze categories, track competitors, research keywords, and build winning pricing strategies.

Paste product data, category names, or competitor URLs. The agent analyzes market dynamics and outputs actionable seller intelligence.

## Commands

```
wb analyze <product>          # analyze product opportunity on Wildberries
ozon analyze <product>        # analyze product opportunity on OZON
market trends <category>      # identify trending categories and products
competitor spy <seller-name>  # analyze competitor seller performance
pricing strategy <product>    # build competitive pricing approach
keyword research <term>       # find search keywords for both platforms
category map                  # map category structure and competition levels
entry assessment <product>    # assess market entry difficulty and opportunity
report <product>              # full cross-platform analysis report
```

## What Data to Provide

- **Product name or category** — in Russian or English
- **Competitor product data** — price, rating, review count, sales estimate
- **Your product specs** — dimensions, weight, cost price
- **Target market** — Russia, Kazakhstan, Belarus, or broader CIS
- **Budget context** — launch budget, margin requirements

## Market Analysis Framework

### OZON vs Wildberries Comparison

| Factor | OZON | Wildberries |
|--------|------|-------------|
| Market share | ~35% | ~55% |
| Commission | 4-25% by category | 5-25% by category |
| Logistics | FBO/FBS/realFBS | FBO/FBS |
| Buyer demographics | Urban, tech-savvy | Mass market |
| Return rate | Lower | Higher (fashion) |
| Best for | Electronics, home | Fashion, FMCG |

### Category Opportunity Scoring

Rate each category on 5 factors (1-5 scale):

1. **Search volume** — estimated monthly searches for main keyword
2. **Competition density** — number of active sellers in top 100
3. **Average margin** — (avg selling price - avg cost) / avg selling price
4. **Review barrier** — minimum reviews needed to appear in top 20
5. **Growth trend** — YoY category GMV growth (declining=1, fast-growing=5)

**Score 20+** = Strong opportunity, prioritize
**Score 15-19** = Moderate opportunity, consider entering
**Score <15** = Saturated or declining, avoid unless strong advantage

### Pricing Strategy Models

**Penetration pricing** (new entrant):
- Set price 15-20% below market average
- Accept low/no profit for first 60 days
- Goal: accumulate reviews and BSR quickly
- Exit: raise price by 5% every 2 weeks once ranked

**Market rate pricing** (established):
- Price within ±5% of top 10 average
- Differentiate on review count and listing quality
- Use coupons (скидка) for promotional periods

**Premium positioning**:
- Price 20-30% above market average
- Requires A+ listing, brand registered, 100+ reviews
- Focus on brand storytelling and quality signals

### Keyword Research (WB & OZON)

**Primary keywords**: High volume, direct match (e.g., "чехол для iPhone 15")
**Long-tail keywords**: Lower volume, higher conversion (e.g., "чехол для iPhone 15 pro прозрачный")
**Seasonal keywords**: Track peak months (e.g., "подарки на Новый год" — November-December)

Keyword integration points:
- Product title (первые 60 символов most important)
- Rich content / description
- Search tags (теги) — use all available slots
- Answer questions section

### Wildberries-Specific Intelligence

**WB ranking factors:**
1. Sales velocity (главный фактор)
2. Conversion rate (клики → заказы)
3. Review count and rating
4. Redemption rate (выкуп) — aim for >80%
5. Logistics speed (FBO gets priority)

**WB Buy Box signals:**
- FBO sellers get priority in search
- Price with applied coupon (цена со скидкой) is displayed
- Seller rating affects placement

**WB Return Rate benchmarks:**
- Fashion: 40-60% returns normal
- Electronics: <10% target
- Home goods: <15% target

### OZON-Specific Intelligence

**OZON Premium** program benefits:
- Search boost for premium items
- Trust badge improves conversion
- Cost: subscription fee

**OZON Rich Content** types:
- Video (highest conversion lift: +30%)
- 360° images
- Infographics
- Comparison tables

**OZON advertising formats:**
- Search promotion (контекстная реклама)
- Product placement boost (продвижение)
- Banner ads (медийная реклама)

## Workspace

Creates `~/wb-ozon-tracker/` containing:
- `categories/` — category analysis reports
- `competitors/` — seller profile snapshots
- `keywords/` — keyword research files
- `pricing/` — price strategy documents
- `reports/` — full analysis reports

## Output Format

Every analysis outputs:
1. **Market Overview** — platform comparison, category size estimate, competition level
2. **Top Competitors Table** — top 5-10 sellers with key metrics
3. **Keyword Blueprint** — primary + long-tail keyword list with priority ranking
4. **Pricing Recommendation** — suggested entry price, target price, minimum margin
5. **Entry Roadmap** — 90-day launch plan with milestones
6. **Risk Flags** — market saturation signals, seasonal risks, regulatory notes
