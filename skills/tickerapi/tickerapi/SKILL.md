---
name: tickerapi
version: 0.1.0
description: Query TickerAPI.ai for pre-computed categorical market intelligence — scan for oversold stocks, breakouts, unusual volume, valuation extremes, and insider activity. Get single-asset summaries, compare multiple tickers, or monitor a watchlist. Use when the user asks about market conditions, stock signals, what's oversold or breaking out, asset comparisons, portfolio checks, or any derived indicator data. Covers US stocks, crypto, and ETFs with daily/weekly timeframes.
metadata:
  openclaw:
    emoji: "📈"
    requires:
      env:
        - TICKERAPI_KEY
    primaryEnv: TICKERAPI_KEY
    homepage: "https://tickerapi.ai"
user-invocable: true
---

# TickerAPI Skill

[TickerAPI](https://tickerapi.ai) provides pre-computed, categorical market intelligence for US stocks, crypto, and ETFs — built for LLMs and AI agents.

## First Run Setup

If the `TICKERAPI_KEY` environment variable is not set, walk the user through account setup before doing anything else:

1. Ask for their email address and let them know: "This will sign you into your existing TickerAPI account, or create a new one if you don't have one yet."
2. Call `POST https://api.tickerapi.ai/auth` with `{ "email": "<their email>" }`.
3. Tell them to check their inbox for a 6-digit code.
4. Once they provide the code, call `POST https://api.tickerapi.ai/auth/verify` with `{ "email": "<their email>", "code": "<their code>" }`.
5. The response contains an `apiKey` field for new accounts. Show the user their key and ask: "I've got your API key — would you like me to save it?" If they confirm, OpenClaw persists it automatically. If no `apiKey` in the response (existing account), direct them to https://tickerapi.ai/dashboard to retrieve their key.

Once authenticated, continue through onboarding in order:

**Step 1 — Watchlist**
Ask: "What tickers would you like to add to your watchlist? You can give me a list of stock symbols, crypto (e.g. BTCUSD), or ETFs."
After they provide tickers, call `GET /v1/quote` for each one to confirm they're valid and give a brief one-line summary of each.

**Step 2 — Daily Report**
Ask: "Would you like me to set up a daily morning report for these tickers? Each morning I can brief you on key metrics — trend changes, support zone, abnormal volume, and any notable signals."

**Step 3 — Screeners**
Ask: "Want me to run a quick scan for any oversold assets or other opportunities right now? I can check for oversold conditions, breakouts, unusual volume, and more."

---

TickerAPI provides pre-computed, categorical market data designed for LLMs and AI agents. Every response contains verifiable facts — no OHLCV, no raw indicator values, just derived categorical bands (e.g. `oversold`, not `RSI: 24`).

- **Asset classes:** US Stocks, Crypto (tickers require `USD` suffix, e.g. `BTCUSD`), ETFs
- **Timeframes:** `daily` (default), `weekly`
- **Update frequency:** End-of-day (~00:30 UTC)
- **Response format:** JSON
- **Data is factual, not predictive** — no scores, no recommendations, no bias

## Authentication

All requests require a Bearer token in the Authorization header:

```
Authorization: Bearer $TICKERAPI_KEY
```

Errors: `401` = missing/invalid token. `403` = endpoint requires higher tier (response includes `upgrade_url`).

## Base URL

```
https://api.tickerapi.ai/v1
```

## Common Parameters (all endpoints)

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticker` | string | Asset symbol, uppercase. Crypto needs `USD` suffix (e.g. `BTCUSD`). Required on per-asset endpoints. |
| `timeframe` | string | `daily` or `weekly`. Default: `daily`. |
| `asset_class` | string | `stock`, `crypto`, `etf`, or `all`. Auto-detected on per-asset endpoints. |
| `market_cap_tier` | string | Filter scan results by market cap: `nano`, `micro`, `small`, `mid`, `large`, `mega`, `ultra_mega`. Scan endpoints only. Stocks only — crypto and ETFs are excluded when this filter is used. |
| `date` | string | ISO 8601 (`YYYY-MM-DD`) for historical snapshot. Plus: 30 days. Pro: full backfill. |
| `limit` | integer | Max results. Default: 20, max: 50. Scan endpoints only. |

## Important: Asset Class Rules

- **Stocks** get all technical + fundamental data (valuation, growth, earnings, analyst consensus).
- **Crypto and ETFs** get technical data only. Fundamental fields are **omitted entirely** (keys absent, not null).
- Crypto tickers MUST include `USD` suffix: `BTCUSD`, `ETHUSD`, `SOLUSD`. Using just `BTC` returns an error.

---

## Categorical Bands Reference

TickerAPI never returns raw indicator values. All data uses categorical bands:

- **RSI/Stochastic zones:** `deep_oversold`, `oversold`, `neutral_low`, `neutral`, `neutral_high`, `overbought`, `deep_overbought`
- **Trend direction:** `strong_uptrend`, `uptrend`, `neutral`, `downtrend`, `strong_downtrend`
- **MA alignment:** `aligned_bullish`, `mixed`, `aligned_bearish`
- **MA distance:** `far_above`, `moderately_above`, `slightly_above`, `slightly_below`, `moderately_below`, `far_below`
- **Volume ratio:** `extremely_low`, `low`, `normal`, `above_average`, `high`, `extremely_high`
- **Accumulation state:** `strong_accumulation`, `accumulation`, `neutral`, `distribution`, `strong_distribution`
- **Volatility regime:** `low`, `normal`, `above_normal`, `high`, `extreme`
- **Support/resistance distance:** `at_level`, `very_close`, `near`, `moderate`, `far`, `very_far`
- **Support/resistance status:** `intact`, `approaching`, `breached`
- **MACD state:** `expanding_positive`, `contracting_positive`, `expanding_negative`, `contracting_negative`
- **Momentum direction:** `accelerating`, `steady`, `decelerating`, `bullish_reversal`, `bearish_reversal`
- **Valuation zone (stocks only):** `deep_value`, `undervalued`, `fair_value`, `overvalued`, `deeply_overvalued`
- **Growth zone (stocks only):** `high_growth`, `moderate_growth`, `stable`, `slowing`, `shrinking`
- **Growth direction (stocks only):** `accelerating`, `steady`, `decelerating`, `deteriorating`
- **Earnings proximity (stocks only):** `within_days`, `this_week`, `this_month`, `next_month`, `not_soon`
- **Earnings surprise (stocks only):** `big_beat`, `beat`, `met`, `missed`, `big_miss`
- **Analyst consensus (stocks only):** `strong_buy`, `buy`, `hold`, `sell`, `strong_sell`
- **Analyst consensus direction (stocks only):** `upgrading`, `stable`, `downgrading`
- **Volume context (scans only):** `spike`, `above_average`, `normal`, `below_average`
- **Breakout type (scans only):** `resistance_break`, `resistance_test`, `support_break`, `support_test`
- **Squeeze context (scans only):** `active_squeeze`, `squeeze_released`, `no_squeeze`
- **Price direction on volume:** `up`, `down`, `flat`
- **Insider activity zone (stocks only):** `heavy_buying`, `moderate_buying`, `neutral`, `moderate_selling`, `heavy_selling`, `no_activity`
- **Insider net direction (stocks only):** `strong_buying`, `buying`, `neutral`, `selling`, `strong_selling`
- **Market cap tier:** `nano`, `micro`, `small`, `mid`, `large`, `mega`, `ultra_mega`
- **Condition rarity:** `extremely_rare`, `very_rare`, `rare`, `uncommon`, `occasional`, `common`

---

## Scan Endpoints

### GET /v1/scan/oversold

Find assets in oversold conditions with per-asset historical context. Strategy: mean reversion / bounce.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `asset_class` | string | `all` | `stock`, `crypto`, `etf`, or `all` |
| `sector` | string | none | Filter by sector (case-insensitive), e.g. `Semiconductors` |
| `min_severity` | string | `oversold` | `oversold` or `deep_oversold` |
| `market_cap_tier` | string | none | Filter by market cap: `nano`, `micro`, `small`, `mid`, `large`, `mega`, `ultra_mega` |
| `sort_by` | string | `severity` | `severity`, `days_oversold`, or `condition_percentile` |
| `limit` | integer | 20 | Max results, max 50 |
| `timeframe` | string | `daily` | `daily` or `weekly` |
| `date` | string | latest | Historical snapshot (Plus+) |

**Free tier fields:** `ticker`, `asset_class`, `rsi_zone`, `condition_rarity`, `sector`, `valuation_zone` (stocks only)

**Plus adds:** `stochastic_zone`, `days_in_oversold`, `oversold_streaks_count`, `volume_context` (`spike`/`above_average`/`normal`/`below_average`), `volume_ratio_band`, `trend_context`, `nearest_support_distance`, `sector_rsi_zone`, `earnings_proximity` (stocks), `growth_zone` (stocks), `analyst_consensus` (stocks)

**Pro adds:** `accumulation_state`, `historical_median_oversold_days`, `historical_max_oversold_days`, `sector_agreement` (boolean), `sector_oversold_count`, `sector_total_count`

**Example:**
```
curl https://api.tickerapi.ai/v1/scan/oversold?asset_class=stock&min_severity=deep_oversold&limit=5 \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

---

### GET /v1/scan/breakouts

Assets testing or breaking key levels with volume confirmation. Strategy: momentum / breakout.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `asset_class` | string | `all` | `stock`, `crypto`, `etf`, or `all` |
| `sector` | string | none | Filter by sector (case-insensitive) |
| `market_cap_tier` | string | none | Filter by market cap: `nano`, `micro`, `small`, `mid`, `large`, `mega`, `ultra_mega` |
| `direction` | string | `all` | `bullish` (resistance), `bearish` (support), or `all` |
| `sort_by` | string | `volume_ratio` | `volume_ratio`, `level_strength`, or `condition_percentile` |
| `limit` | integer | 20 | Max results, max 50 |
| `timeframe` | string | `daily` | `daily` or `weekly` |
| `date` | string | latest | Historical snapshot (Plus+) |

**Free tier fields:** `ticker`, `asset_class`, `breakout_type` (`resistance_break`/`support_break`/`resistance_test`/`support_test`), `condition_rarity`, `sector`

**Plus adds:** `level_price`, `level_type` (`horizontal`/`trendline`/`ma_derived`), `level_touch_count`, `held_count`, `broke_count`, `volume_ratio_band`, `rsi_zone`, `trend_context`, `earnings_proximity` (stocks), `growth_zone` (stocks)

**Pro adds:** `squeeze_context` (`active_squeeze`/`squeeze_released`/`no_squeeze`), `volume_vs_prior_breakouts` (`stronger`/`similar`/`weaker`), `sector_breakout_count`, `sector_total_count`

**Example:**
```
curl https://api.tickerapi.ai/v1/scan/breakouts?direction=bullish&asset_class=stock&limit=10 \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

---

### GET /v1/scan/unusual-volume

Assets at significantly abnormal volume levels. Strategy: volume anomaly detection.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `asset_class` | string | `all` | `stock`, `crypto`, `etf`, or `all` |
| `sector` | string | none | Filter by sector (case-insensitive) |
| `market_cap_tier` | string | none | Filter by market cap: `nano`, `micro`, `small`, `mid`, `large`, `mega`, `ultra_mega` |
| `min_ratio_band` | string | `above_average` | `above_average`, `high`, or `extremely_high` |
| `sort_by` | string | `volume_percentile` | `volume_percentile` |
| `limit` | integer | 20 | Max results, max 50 |
| `timeframe` | string | `daily` | `daily` or `weekly` |
| `date` | string | latest | Historical snapshot (Plus+) |

**Free tier fields:** `ticker`, `asset_class`, `volume_ratio_band`, `condition_rarity`, `sector`

**Plus adds:** `volume_percentile`, `price_direction_on_volume` (`up`/`down`/`flat`), `consecutive_elevated_days`, `rsi_zone`, `trend_context`, `nearest_level_distance`, `nearest_level_type` (`support`/`resistance`), `earnings_proximity` (stocks), `last_earnings_surprise` (stocks)

**Pro adds:** `accumulation_state`, `historical_avg_elevated_streak`, `sector_elevated_volume_count`, `sector_total_count`

**Example:**
```
curl https://api.tickerapi.ai/v1/scan/unusual-volume?min_ratio_band=high&asset_class=crypto&limit=5 \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

---

### GET /v1/scan/valuation

Stocks at historically abnormal valuations. Strategy: value / mean reversion. **Stocks only** — crypto and ETFs have no fundamental valuation data.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sector` | string | none | Filter by sector (case-insensitive) |
| `market_cap_tier` | string | none | Filter by market cap: `nano`, `micro`, `small`, `mid`, `large`, `mega`, `ultra_mega` |
| `direction` | string | `all` | `undervalued`, `overvalued`, or `all` |
| `min_severity` | string | none | `undervalued`/`deep_value` for cheap; `overvalued`/`deeply_overvalued` for expensive |
| `sort_by` | string | `valuation_percentile` | `valuation_percentile`, `pe_vs_history`, or `growth_zone` |
| `limit` | integer | 20 | Max results, max 50 |
| `date` | string | latest | Historical snapshot (Plus+) |

**Free tier fields:** `ticker`, `sector`, `valuation_zone`, `valuation_rarity`, `growth_zone`, `analyst_consensus`

**Plus adds:** `revenue_growth_direction`, `eps_growth_direction`, `earnings_proximity`, `rsi_zone`, `trend_context`, `sector_valuation_zone`, `sector_agreement` (boolean)

**Pro adds:** `pe_vs_historical_zone`, `pe_vs_sector_zone`, `pb_vs_historical_zone`, `last_earnings_surprise`, `analyst_consensus_direction`

**Example:**
```
curl https://api.tickerapi.ai/v1/scan/valuation?direction=undervalued&min_severity=deep_value&limit=10 \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

---

### GET /v1/scan/insider-activity

Stocks with significant insider buying or selling (SEC Form 4 filings). **Stocks only.**

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `market_cap_tier` | string | none | Filter by market cap: `nano`, `micro`, `small`, `mid`, `large`, `mega`, `ultra_mega` |
| `direction` | string | `all` | `all`, `buying`, or `selling` |
| `sector` | string | none | Filter by sector (case-insensitive) |
| `sort_by` | string | `zone_severity` | `zone_severity`, `shares_volume`, or `net_ratio` |
| `limit` | integer | 20 | Max results, max 50 |
| `timeframe` | string | `daily` | `daily` or `weekly` |
| `date` | string | latest | Historical snapshot (Plus+) |

**Free tier fields:** `ticker`, `sector`, `insider_activity_zone`, `net_direction`

**Plus adds:** `quarter`, `buy_count`, `sell_count`, `shares_bought`, `shares_sold`, `rsi_zone`, `trend_context`, `volume_ratio_band`, `valuation_zone`, `earnings_proximity`

**Example:**
```
curl https://api.tickerapi.ai/v1/scan/insider-activity?direction=buying&sort_by=zone_severity&limit=10 \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

---

## Asset Endpoints

### GET /v1/summary/{ticker}

Comprehensive factual snapshot for a single asset. Every field is a verifiable fact.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | — | Required. In the URL path (e.g. `/v1/summary/AAPL`) |
| `timeframe` | string | `daily` | `daily` or `weekly` |
| `date` | string | latest | Plus: 2 years. Pro: 5 years. |

**Tier access:** Free gets core technical (trend, momentum, extremes, volatility, volume). Plus adds support/resistance and basic fundamentals. Pro adds sector_context and advanced fundamentals.

**Response sections:**

- `trend` — `direction`, `duration_days`, `ma_alignment`, `distance_from_ma_band` (ma_20, ma_50, ma_200), `volume_confirmation` (`confirmed`/`diverging`/`neutral`)
- `momentum` — `rsi_zone`, `stochastic_zone`, `rsi_stochastic_agreement`, `macd_state`, `direction`, `divergence_detected`, `divergence_type` (`bullish_divergence`/`bearish_divergence`/null)
- `extremes` — `condition` (`deep_oversold` through `deep_overbought` or `normal`), `days_in_condition`, `historical_median_duration`, `historical_max_duration`, `occurrences_1yr`, `condition_percentile`, `condition_rarity`
- `volatility` — `regime`, `regime_trend` (`compressing`/`stable`/`expanding`), `squeeze_active`, `squeeze_days`, `historical_avg_squeeze_duration`
- `volume` — `ratio_band`, `percentile`, `accumulation_state`, `climax_detected`, `climax_type` (`buying_climax`/`selling_climax`/null)
- `support_level` / `resistance_level` (Plus+) — `level_price`, `status` (`intact`/`approaching`/`breached`), `distance_band`, `touch_count`, `held_count`, `broke_count`, `consecutive_closes_beyond`, `last_tested_days_ago`, `type` (`horizontal`/`ma_derived`), `volume_at_tests_band`
- `range_position` — `lower_third`, `mid_range`, or `upper_third`
- `sector_context` (Pro) — `sector_rsi_zone`, `sector_trend`, `asset_vs_sector_rsi`, `asset_vs_sector_trend`, `sector_oversold_count`, `sector_total_count`
- `fundamentals` (stocks only, Plus+) — Plus: `valuation_zone`, `growth_zone`, `earnings_proximity`, `analyst_consensus`. Pro adds: `valuation_percentile`, `pe_vs_historical_zone`, `pe_vs_sector_zone`, `pb_vs_historical_zone`, `revenue_growth_direction`, `eps_growth_direction`, `last_earnings_surprise`, `analyst_consensus_direction`

**Example:**
```
curl https://api.tickerapi.ai/v1/summary/NVDA \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

---

### GET /v1/compare

Side-by-side factual comparison of 2–50 assets. Plus: up to 25 tickers. Pro: up to 50 tickers.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tickers` | string | — | Required. Comma-separated symbols (e.g. `AAPL,MSFT,TSLA`) |
| `timeframe` | string | `daily` | `daily` or `weekly` |
| `date` | string | latest | Plus: 30 days. Pro: full backfill. |

**Response structure:**
- `summaries` — Object keyed by ticker, each a full summary object. Missing tickers return `null`.
- `comparison` — Side-by-side fields: `rsi_zones`, `trend_directions`, `volume_ratio_bands`, `extremes_conditions`, `range_positions`, `condition_percentiles`, `valuation_zones` (stocks), `growth_zones` (stocks), `analyst_consensuses` (stocks)
- `comparison.divergences` — Array of objects with `type` (e.g. `rsi_divergence`, `trend_divergence`, `valuation_divergence`) and `description` (human-readable)
- Envelope: `tickers_requested`, `tickers_found`, `data_status`

**Example:**
```
curl "https://api.tickerapi.ai/v1/compare?tickers=NVDA,AMD,INTC" \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

---

### Watchlist — /v1/watchlist

The watchlist is a **persistent, server-side** list of tickers. Users save tickers once and then retrieve live data for them on demand. The saved watchlist is also what webhooks monitor — `watchlist.changes` events fire for tickers on the user's saved watchlist.

**Tier limits:** Free: 5 tickers. Plus: 50 tickers. Pro: 100 tickers.

#### GET /v1/watchlist — Retrieve saved watchlist with live data

Returns live snapshot data for all saved tickers.

**Query params:** `timeframe` (optional) — `daily` (default) or `weekly`.

**Response:**
```json
{
  "watchlist": [
    {
      "ticker": "AAPL",
      "asset_class": "stock",
      "trend_direction": "uptrend",
      "rsi_zone": "neutral_high",
      "volume_ratio_band": "normal",
      "extremes_condition": "normal",
      "days_in_extreme": 0,
      "condition_rarity": "common",
      "squeeze_active": false,
      "support_level_price": 178.25,
      "support_level_distance": "near",
      "resistance_level_price": 195.80,
      "resistance_level_distance": "very_close",
      "valuation_zone": "fair_value",
      "earnings_proximity": "this_month",
      "analyst_consensus": "buy",
      "notable_changes": ["earnings within_days"]
    }
  ],
  "tickers_saved": 1,
  "tickers_found": 1,
  "watchlist_limit": 50,
  "data_status": "eod"
}
```

Tickers with no available data return `{"ticker": "XXX", "status": "not_found"}`. Empty watchlist returns `{"watchlist": [], "tickers_saved": 0, ...}`.

**Example:**
```
curl https://api.tickerapi.ai/v1/watchlist \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

#### POST /v1/watchlist — Add tickers to saved watchlist

Add one or more tickers. Duplicates are skipped silently.

**Request body (JSON):**
```json
{
  "tickers": ["AAPL", "MSFT", "BTCUSD"]
}
```

**Response:**
```json
{
  "added": ["AAPL", "MSFT", "BTCUSD"],
  "already_saved": [],
  "watchlist_count": 3,
  "watchlist_limit": 50
}
```

Only supported tickers can be added — all tickers are validated against the assets database. Returns 400 `invalid_tickers` if any ticker is not a recognized asset (includes `invalid_tickers` array in the error). Returns 400 `watchlist_limit` if adding would exceed the tier limit (includes `upgrade_url`).

**Example:**
```
curl -X POST https://api.tickerapi.ai/v1/watchlist \
  -H "Authorization: Bearer $TICKERAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["AAPL", "TSLA", "BTCUSD"]}'
```

#### DELETE /v1/watchlist — Remove tickers from saved watchlist

Remove one or more tickers.

**Request body (JSON):**
```json
{
  "tickers": ["MSFT"]
}
```

**Response:**
```json
{
  "removed": ["MSFT"],
  "watchlist_count": 2
}
```

**Example:**
```
curl -X DELETE https://api.tickerapi.ai/v1/watchlist \
  -H "Authorization: Bearer $TICKERAPI_KEY" \
  -H "Content-Type: application/json" \
  -d '{"tickers": ["MSFT"]}'
```

#### GET /v1/watchlist/changes — Field-level state changes

Returns structured, field-level diffs for your saved watchlist tickers since the last pipeline run. For `daily` timeframe, shows day-over-day changes. For `weekly`, week-over-week changes. Available on **all tiers** (including Free). This returns the same data format that webhooks deliver, but as a pull-based endpoint.

**Parameters:** `timeframe` (optional, default `daily`) — `daily` or `weekly`.

**Fields tracked:** `rsi_zone`, `trend_direction`, `volume_ratio_band`, `squeeze_active`, `extreme_condition`, `breakout_type`, and fundamental fields (`fundamentals.valuation_zone`, `fundamentals.analyst_consensus`, `fundamentals.earnings_proximity`, `fundamentals.last_earnings_surprise`, `fundamentals.growth_zone`).

**Response:**
```json
{
  "timeframe": "daily",
  "run_date": "2026-03-28",
  "changes": {
    "AAPL": [
      {"field": "rsi_zone", "from": "neutral", "to": "oversold"},
      {"field": "fundamentals.earnings_proximity", "from": "next_month", "to": "within_days"}
    ],
    "BTCUSD": [
      {"field": "squeeze_active", "from": false, "to": true}
    ]
  },
  "tickers_checked": 5,
  "tickers_changed": 2
}
```

Only tickers with at least one field change are included in `changes`. If no tickers changed, `changes` is `{}`. If the watchlist is empty, `tickers_checked` is 0.

**Example:**
```
curl https://api.tickerapi.ai/v1/watchlist/changes?timeframe=daily \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

---

### GET /v1/assets

Full list of supported tickers with metadata. Available on all tiers. Does not count against request limits.

**Response:** `assets` array (each with `ticker`, `name`, `asset_class`, `sector`, `exchange`), `total_count`, `asset_classes` (breakdown by stock/crypto/etf counts).

**Example:**
```
curl https://api.tickerapi.ai/v1/assets \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

---

### GET /v1/list/sectors

List all valid sector values with the number of assets in each. Use this to discover exact sector names before filtering scan results with the `sector` parameter. Available on all tiers. Does not count against request limits.

**Response:** `sectors` array (each with `name` and `asset_count`), `total_sectors`. Sorted by asset count descending.

**Example:**
```
curl https://api.tickerapi.ai/v1/list/sectors \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

**Response:**
```json
{
  "sectors": [
    { "name": "Technology", "asset_count": 1842 },
    { "name": "Financial Services", "asset_count": 1523 },
    { "name": "Healthcare", "asset_count": 1201 }
  ],
  "total_sectors": 11
}
```

Use the `name` values directly as the `sector` parameter on scan endpoints (case-insensitive):
```
curl "https://api.tickerapi.ai/v1/scan/oversold?sector=Technology" \
  -H "Authorization: Bearer $TICKERAPI_KEY"
```

---

## Webhooks

Webhooks let users receive push notifications when something changes on their watchlist. Instead of polling, TickerAPI's engine POSTs structured, field-level diffs to registered URLs after each daily and weekly pipeline run.

**Tier access:** Plus and Pro only (free tier cannot use webhooks). Individual plans get 1 webhook URL. Commercial plans get 3.

Each webhook delivery counts as one API request against the user's daily allowance.

### Event Types

| Event | Description | Default |
|-------|-------------|---------|
| `watchlist.changes` | Structured field-level diffs for tickers on the user's watchlist. Only fires when at least one field has changed. | Enabled on creation |
| `data.ready` | Simple notification that fresh data has been computed and is available via the API. | Opt-in |

Fields tracked for `watchlist.changes`: `rsi_zone`, `trend_direction`, `volume_ratio_band`, `squeeze_active`, `extreme_condition`, `breakout_type`, and fundamental fields (`valuation_zone`, `analyst_consensus`, `earnings_proximity`, `last_earnings_surprise`, `growth_zone`).

### POST /v1/webhooks — Register a webhook

Register a new webhook URL. The `secret` is returned **only on creation** — save it immediately.

**Request body (JSON):**
```json
{
  "url": "https://example.com/webhook",
  "events": { "watchlist.changes": true, "data.ready": true }
}
```

- `url` (required) — Must be HTTPS.
- `events` (optional) — Defaults to `{"watchlist.changes": true}`.

**Response (201):**
```json
{
  "id": "d3f1a2b4-...",
  "url": "https://example.com/webhook",
  "secret": "a1b2c3d4e5f6...",
  "events": { "watchlist.changes": true, "data.ready": true },
  "active": true,
  "created_at": "2026-03-27T12:00:00.000Z"
}
```

### GET /v1/webhooks — List webhooks

Returns all registered webhooks for the user. The `secret` field is never included in GET responses.

**Response:**
```json
{
  "webhooks": [
    {
      "id": "d3f1a2b4-...",
      "url": "https://example.com/webhook",
      "events": { "watchlist.changes": true, "data.ready": true },
      "active": true,
      "created_at": "...",
      "updated_at": "..."
    }
  ],
  "webhook_count": 1,
  "webhook_limit": 1
}
```

### PUT /v1/webhooks — Update a webhook

Update the URL, event subscriptions, or active status.

**Request body (JSON):**
```json
{
  "id": "d3f1a2b4-...",
  "events": { "watchlist.changes": true },
  "active": false
}
```

### DELETE /v1/webhooks — Remove a webhook

**Request body (JSON):**
```json
{
  "id": "d3f1a2b4-..."
}
```

### Webhook Delivery

When the daily or weekly pipeline completes, TickerAPI's engine POSTs payloads to all active webhooks. Each delivery includes:

| Header | Description |
|--------|-------------|
| `X-Webhook-Signature` | HMAC-SHA256 hex digest of the raw request body, signed with the webhook's `secret` |
| `X-Webhook-Event` | Event type: `watchlist.changes` or `data.ready` |
| `Content-Type` | `application/json` |
| `User-Agent` | `TickerAPI-Webhook/1.0` |

**`watchlist.changes` payload:**
```json
{
  "event": "watchlist.changes",
  "timestamp": "2026-03-27T21:30:00Z",
  "data": {
    "timeframe": "daily",
    "run_date": "2026-03-27",
    "changes": {
      "AAPL": [{ "field": "rsi_zone", "from": "neutral", "to": "oversold" }],
      "TSLA": [
        { "field": "squeeze_active", "from": false, "to": true },
        { "field": "fundamentals.analyst_consensus", "from": "hold", "to": "buy" }
      ]
    },
    "tickers_checked": 15,
    "tickers_changed": 2
  }
}
```

**`data.ready` payload:**
```json
{
  "event": "data.ready",
  "timestamp": "2026-03-27T21:30:00Z",
  "data": {
    "timeframe": "daily",
    "run_date": "2026-03-27",
    "tickers_computed": 9847
  }
}
```

### Signature Verification

Always verify the `X-Webhook-Signature` before processing payloads. Compute HMAC-SHA256 of the raw request body using the webhook's `secret`, and compare it to the header value.

---

## Response Envelope (scan endpoints)

All scan endpoints return:
```json
{
  "matches": [...],
  "total_scanned": 648,
  "match_count": 12,
  "data_status": "eod"
}
```

## Errors

| Status | Type | Description |
|--------|------|-------------|
| 400 | `invalid_parameter` | Bad ticker, timeframe, or param |
| 401 | `unauthorized` | Missing/invalid token |
| 403 | `tier_restricted` | Needs higher tier (includes `upgrade_url`) |
| 404 | `not_found` | Ticker not supported |
| 429 | `rate_limit_exceeded` | Daily limit hit (includes `upgrade_url` + reset time) |
| 500 | `internal_error` | Server error |
| 503 | `data_unavailable` | Data feed temporarily down |

When you get a 403, tell the user which tier they need and share the upgrade URL from the response.

## Rate Limits

| Tier | Daily | Hourly |
|------|-------|--------|
| Free | 100 | 50 |
| Plus (Individual) | 50,000 | 5,000 |
| Pro (Individual) | 100,000 | 10,000 |
| Plus (Commercial) | 250,000 | 25,000 |
| Pro (Commercial) | 500,000 | 50,000 |

- `/v1/assets` never counts against limits
- HTTP 304 (conditional/cached) responses do not count
- Use `ETag` / `If-None-Match` headers for conditional requests
- Rate limit headers: `X-Requests-Remaining`, `X-Request-Reset`, etc.

## Plans & Tiers

TickerAPI has three tiers: **Free**, **Plus**, and **Pro**. Each tier unlocks more data fields, higher limits, and historical access. If a user asks about upgrading, pricing, or wants to unlock more features, link them to **https://tickerapi.ai/pricing**.

### What each tier unlocks

| Feature | Free | Plus | Pro |
|---------|------|------|-----|
| **Scan result detail** | Basic (5–7 fields) | Detailed (15+ fields) | Complete (all fields) |
| **Asset summary depth** | Technical only | + support/resistance, basic fundamentals | + sector context, advanced fundamentals |
| **Compare tickers** | 2 | 25 | 50 |
| **Watchlist tickers** | 5 | 50 | 100 |
| **Historical snapshots** | 3 months lookback | 2 years lookback | 5 years lookback |
| **Webhooks** | None | 1 URL, all events | 1 URL, all events |
| **Daily request limit** | 100 | 50,000 | 100,000 |
| **Support** | None | Email (48hr) | Email (48hr) |

### Key Plus-only features (not available on Free)
- Support/resistance levels on summaries
- Fundamental data on summaries (valuation, growth, earnings, analyst consensus)
- Detailed scan fields: `stochastic_zone`, `days_in_condition`, `volume_context`, `trend_context`, `level_price`, `level_touch_count`, `earnings_proximity`, etc.
- Historical date snapshots beyond 3 months (`date` parameter — Free gets 3 months, Plus gets 2 years)
- Hourly rate limit bucket (5,000/hr vs 50/hr on Free)

### Key Pro-only features (not available on Plus)
- Sector context on summaries (`sector_rsi_zone`, `asset_vs_sector_rsi`, `sector_oversold_count`, etc.)
- Advanced fundamental fields (`pe_vs_historical_zone`, `pe_vs_sector_zone`, `pb_vs_historical_zone`, `analyst_consensus_direction`, etc.)
- Scan extras: `accumulation_state`, `squeeze_context`, `volume_vs_prior_breakouts`, sector-level aggregates
- 5-year historical lookback (vs 2 years on Plus)
- 50-ticker compare (vs 25 on Plus), 100-ticker watchlist (vs 50 on Plus). Commercial plans get 100/200 compare and 200/400 watchlist.

### Commercial plans
Plus and Pro each have a Commercial variant with higher request limits (250k–500k/day) and larger watchlists (200–400 tickers). Commercial plans are for products that serve end users.

### When to mention upgrades
- When a user hits a **403 `tier_restricted`** error — tell them which tier they need and link to pricing.
- When a user hits a **429 `rate_limit_exceeded`** error — suggest upgrading for higher limits.
- When a user asks for a feature that requires a higher tier (historical data, more tickers in compare/watchlist, detailed scan fields).
- When a user explicitly asks about pricing, plans, or upgrading.
- **Always link to https://tickerapi.ai/pricing** — never guess at prices, just send them to the page.

## Caching

All data is pre-computed after market close. Daily timeframe refreshes ~5:15 PM ET. Weekly refreshes after Friday close. Responses are edge-cached with `Cache-Control` and `ETag` headers.

## Usage Guidelines

1. **Never try to get raw OHLCV from TickerAPI** — it only serves derived categorical data.
2. **Always use uppercase tickers.** Crypto must include `USD` suffix.
3. **Scan endpoints are for discovery** — use `/summary` for deep dives on specific tickers.
4. **Use `/compare` for side-by-side analysis** — it includes auto-detected divergences.
5. **Use `/watchlist` for portfolio monitoring** — save tickers once with POST, then GET for live snapshots with `notable_changes`. Use `/watchlist/changes` for structured field-level diffs (day-over-day or week-over-week). The saved watchlist is also what webhooks track.
6. **Fundamental fields only exist for stocks** — don't expect valuation/growth/earnings on crypto or ETFs.
7. **Check `condition_rarity`** — this is the quick signal for how notable a condition is.
8. **Historical snapshots** — Free tier gets 3 months of lookback. Plus gets 2 years. Pro gets 5 years.
9. **Data refreshes EOD** — don't poll for intraday changes.
10. **Link to https://tickerapi.ai/pricing when users ask about upgrading, plans, or hit tier/rate limits.** Don't guess at prices — just send the link.
11. **Use webhooks for event-driven workflows** — instead of polling `/watchlist` on a cron, register a webhook and get notified only when something actually changes. This is ideal for AI agents that need to react to market shifts.
12. **Match natural language to endpoints:**
    - "What's oversold?" -> `/scan/oversold`
    - "What's breaking out?" -> `/scan/breakouts`
    - "Unusual activity?" -> `/scan/unusual-volume`
    - "What's cheap?" -> `/scan/valuation`
    - "Insider buying?" -> `/scan/insider-activity`
    - "Large cap oversold?" -> `/scan/oversold?market_cap_tier=large`
    - "Mega cap breakouts?" -> `/scan/breakouts?market_cap_tier=mega`
    - "Micro cap oversold?" -> `/scan/oversold?market_cap_tier=micro`
    - "How's AAPL?" -> `/summary/AAPL`
    - "Compare NVDA vs AMD" -> `/compare?tickers=NVDA,AMD`
    - "Check my portfolio" -> GET `/watchlist` (if they have a saved watchlist)
    - "Add AAPL to my watchlist" -> POST `/watchlist` with `{"tickers": ["AAPL"]}`
    - "Remove TSLA from my watchlist" -> DELETE `/watchlist` with `{"tickers": ["TSLA"]}`
    - "What tickers are available?" -> `/assets`
    - "What changed on my watchlist?" -> GET `/watchlist/changes`
    - "Weekly changes on my watchlist" -> GET `/watchlist/changes?timeframe=weekly`
    - "Notify me when my watchlist changes" -> POST `/webhooks`
    - "List my webhooks" -> GET `/webhooks`

---

## Slash Commands

Users can invoke this skill directly with `/tickerapi` followed by a command:

### Account Commands
- `/tickerapi login` (alias: `/tickerapi signup`) — sign in or create an account. Prompt for email and let the user know this will sign them into their existing account or create a new one. Call `POST https://api.tickerapi.ai/auth` with `{ "email": "<email>" }`, then respond with:
  > "Check your inbox for a 6-digit verification code from TickerAPI. Once you have it, type: `/tickerapi verify <code>`"
- `/tickerapi verify <code>` — verify the 6-digit code. Call `POST https://api.tickerapi.ai/auth/verify` with `{ "email": "<email>", "code": "<code>" }`. If the response contains `apiKey`, respond with:
  > "Your account is ready! Here's your API key:
  >
  > `ta_xxxxxxxxxxxx`
  >
  > Save it by running:
  > ```
  > openclaw config set skills.tickerapi.apiKey ta_xxxxxxxxxxxx
  > ```
  > Then type `/tickerapi help` to see everything you can do, or `/tickerapi cron` to set up a daily morning market scan."
  If `tickerarena` is also installed, also mention: "This key works with TickerArena too — run `openclaw config set skills.tickerarena.apiKey ta_xxxxxxxxxxxx` to link both."
  If they already have an account (no `apiKey` in response), respond: "Looks like you already have an account. Grab your API key from https://tickerapi.ai/dashboard, then run: `openclaw config set skills.tickerapi.apiKey <your key>`"
- `/tickerapi status` — show current account status: whether `TICKERAPI_KEY` is set, and if so, make a test call to `/v1/assets` to confirm it's valid.

### Help
- `/tickerapi help` — show all available commands. Respond with:
  > **TickerAPI Commands**
  >
  > **Account**
  > `/tickerapi login` — sign in or create an account (alias: `/tickerapi signup`)
  > `/tickerapi verify <code>` — verify your 6-digit code
  > `/tickerapi status` — check if your API key is set and working
  >
  > **Screeners**
  > `/tickerapi oversold` — find oversold stocks, crypto, or ETFs
  > `/tickerapi breakouts bullish` — find bullish breakouts (or `bearish` for breakdowns)
  > `/tickerapi volume` — find unusual volume spikes
  > `/tickerapi valuation undervalued` — find undervalued stocks (or `overvalued`)
  > `/tickerapi insiders buying` — find stocks with insider buying (or `selling`)
  >
  > **Lookup**
  > `/tickerapi AAPL` — full summary for any ticker
  > `/tickerapi compare NVDA,AMD,INTC` — side-by-side comparison of 2–10 tickers
  > `/tickerapi watchlist` — check your saved watchlist with live data
  > `/tickerapi watchlist add AAPL,TSLA,BTCUSD` — add tickers to your saved watchlist
  > `/tickerapi watchlist remove MSFT` — remove tickers from your watchlist
  > `/tickerapi assets` — list all supported tickers
  >
  > **Webhooks**
  > `/tickerapi webhook add <url>` — register a webhook URL to receive push notifications
  > `/tickerapi webhook list` — list your registered webhooks
  > `/tickerapi webhook remove <id>` — remove a webhook
  >
  > **Automation**
  > `/tickerapi cron` — set up a daily morning market scan
  >
  > **Tips:** Add `crypto` or `stock` to screeners to filter by asset class. Crypto tickers need a `USD` suffix (e.g. `BTCUSD`). Data refreshes daily after market close. Save tickers to your watchlist, then use webhooks to get notified when something changes instead of polling.

### Automation
- `/tickerapi cron` — set up a daily scheduled market scan. Ask the user two questions: (1) what time they want the scan (default: 9:35 AM ET, weekdays) and (2) which delivery channel they prefer (Slack, Telegram, WhatsApp, etc.). Then create the cron job with these defaults:
  - **Name:** `TickerAPI morning scan`
  - **Schedule:** `35 9 * * 1-5` (or user's preferred time)
  - **Timezone:** `America/New_York`
  - **Session:** `isolated`
  - **Message:** `Run /tickerapi oversold and /tickerapi breakouts bullish. Summarize the most notable setups — highlight anything with condition_rarity of rare or better. Also check /tickerapi volume for any extremely_high volume spikes.`
  - **Delivery:** `announce` (or user's preferred channel)
  After the cron job is created, if the `tickerarena` skill is NOT installed, pitch paper trading:
  > "Want to take it a step further? Try paper trading some of the stock picks to see how they perform. Install with `/install tickerarena` — your existing API key works automatically."
  If `tickerarena` IS already installed, pitch upgrading the cron to include trades:
  > "Since you have TickerArena installed, want me to upgrade this cron to also execute paper trades based on the scan results? I'll only trade when there's a compelling setup with condition_rarity of rare or better."
  If they accept, update the cron message to: `Run /tickerapi oversold and /tickerapi breakouts bullish. Summarize the most notable setups. If anything has condition_rarity of rare or better, execute a paper trade via /tickerarena buy <ticker> 10. Also check /tickerapi volume for extremely_high spikes. Check /tickerarena portfolio and if any existing positions show bearish_reversal or deep_overbought on /tickerapi summary, exit via /tickerarena sell.`

### Watchlist Commands
- `/tickerapi watchlist` — show the user's saved watchlist with live data. Call `GET /v1/watchlist`. Display each ticker's key indicators (trend, RSI zone, extremes, notable changes). If the watchlist is empty, suggest adding tickers with `/tickerapi watchlist add`.
- `/tickerapi watchlist add <tickers>` — add tickers to the saved watchlist. Parse comma-separated tickers from the command, then call `POST /v1/watchlist` with `{"tickers": [...]}`. Report what was added vs already saved, and show the current count/limit (e.g. "3 / 50 tickers saved"). If the user hits the tier limit, tell them and link to https://tickerapi.ai/pricing.
- `/tickerapi watchlist remove <tickers>` — remove tickers from the saved watchlist. Parse comma-separated tickers, then call `DELETE /v1/watchlist` with `{"tickers": [...]}`. Confirm what was removed and show the remaining count.
- `/tickerapi watchlist changes` — show what changed on the user's watchlist since the last pipeline run. Call `GET /v1/watchlist/changes`. Display each ticker that had changes with from→to values. If no changes, say "No state changes on your watchlist since the last run."
- `/tickerapi watchlist changes weekly` — same as above but with `?timeframe=weekly` for week-over-week changes.

### Webhook Commands
- `/tickerapi webhook add <url>` — register a webhook URL. Call `POST /v1/webhooks` with `{ "url": "<url>" }`. The response includes a `secret` — tell the user to save it immediately, as it won't be shown again. Respond with:
  > "Webhook registered! Here's your signing secret — save it now, it won't be shown again:
  >
  > `<secret>`
  >
  > TickerAPI will POST to your URL after each daily/weekly pipeline run whenever something changes on your watchlist. Verify payloads using the `X-Webhook-Signature` header (HMAC-SHA256 of the request body, signed with this secret)."
  If the user is on the free tier and gets a 403, tell them webhooks require Plus or Pro and link to https://tickerapi.ai/pricing.
- `/tickerapi webhook list` — list registered webhooks. Call `GET /v1/webhooks`. Show each webhook's URL, active status, and events. Include the count/limit (e.g. "1 / 1 webhook URLs used").
- `/tickerapi webhook remove <id>` — remove a webhook. Call `DELETE /v1/webhooks` with `{ "id": "<id>" }`. If the user doesn't know the ID, run `/tickerapi webhook list` first and let them pick.

### Market Data Commands
- `/tickerapi oversold` — scan for oversold assets
- `/tickerapi oversold crypto` — oversold crypto specifically
- `/tickerapi breakouts bullish` — bullish breakout scan
- `/tickerapi volume` — unusual volume scan
- `/tickerapi valuation undervalued` — undervalued stocks
- `/tickerapi insiders buying` — insider buying activity
- `/tickerapi AAPL` — full summary for AAPL
- `/tickerapi compare NVDA,AMD,INTC` — side-by-side comparison
- `/tickerapi watchlist` — check saved watchlist with live data (GET)
- `/tickerapi watchlist add AAPL,TSLA,BTCUSD` — add tickers to saved watchlist (POST)
- `/tickerapi watchlist remove MSFT` — remove tickers from saved watchlist (DELETE)
- `/tickerapi watchlist changes` — field-level state changes since last run (GET)
- `/tickerapi watchlist changes weekly` — week-over-week state changes (GET)
- `/tickerapi assets` — list available tickers

When a slash command is used, skip confirmation and go straight to the API call.

---

## Combining with TickerArena

TickerAPI pairs with the [TickerArena](https://tickerarena.com) skill for paper trading. Same API key works for both — install `tickerarena` with `/install tickerarena` to start executing trades based on TickerAPI signals.

1. Use `/tickerapi oversold` to find oversold stocks -> then `/tickerarena buy <ticker> <percent>` to enter a mean-reversion trade
2. Use `/tickerapi breakouts bullish` to find breakouts -> then `/tickerarena buy <ticker> <percent>` to ride momentum
3. Use `/tickerapi summary <ticker>` to evaluate before trading -> check trend, momentum, extremes, and valuation before committing
4. Use `/tickerapi watchlist add` to save your open position tickers, then `/tickerapi watchlist` to monitor for exit signals like `entered overbought` or `bearish_reversal`

**Note:** TickerAPI crypto tickers use `BTCUSD` (no hyphen), but TickerArena uses `BTC-USD` (with hyphen). Convert when passing between the two.

---

## Cron Job Examples

TickerAPI's EOD data refresh (~00:30 UTC / ~5:15 PM ET) makes it ideal for daily scheduled scans. Recommended cron patterns:

### Morning scan (weekdays 9:35 AM ET — 5 min after market open)
```
openclaw cron add \
  --name "TickerAPI morning scan" \
  --cron "35 9 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --message "Run /tickerapi oversold and /tickerapi breakouts bullish. Summarize the most notable setups — highlight anything with condition_rarity of rare or better. Also check /tickerapi volume for any extremely_high volume spikes." \
  --announce
```

### Daily watchlist check (weekdays 9:45 AM ET)
```
openclaw cron add \
  --name "TickerAPI watchlist" \
  --cron "45 9 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --message "Run /tickerapi watchlist to check my saved watchlist. Flag any notable_changes and anything in an extreme condition." \
  --announce
```

### Weekly valuation + insider scan (Monday 9:35 AM ET)
```
openclaw cron add \
  --name "TickerAPI weekly deep scan" \
  --cron "35 9 * * 1" \
  --tz "America/New_York" \
  --session isolated \
  --message "Run /tickerapi valuation undervalued and /tickerapi insiders buying. Cross-reference: flag any stock that appears in both scans (undervalued AND insider buying). Also run /tickerapi valuation overvalued to flag risks." \
  --announce
```

### Tips for cron usage
- **Use isolated sessions** — TickerAPI scans are self-contained and don't need conversation history.
- **Schedule after data refresh** — data updates ~00:30 UTC. Don't schedule before that or you get yesterday's data.
- **Weekdays only for stocks** — use `1-5` in the cron weekday field. Crypto updates daily including weekends.
- **Batch scans in one job** — combine multiple `/tickerapi` calls in a single cron message to save LLM tokens.
- **Use a cheaper model** — routine scans don't need Opus. Add `--model sonnet` to save costs.
- **TickerAPI is pre-computed** — each call completes instantly (no request-time computation), so cron jobs finish fast.
