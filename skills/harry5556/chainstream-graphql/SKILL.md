---
name: chainstream-graphql
description: >-
  Execute flexible GraphQL queries against ChainStream's on-chain data warehouse (22 cubes across Solana, Ethereum, BSC).
  Use when user needs custom analytics beyond standard REST/MCP — cross-cube JOINs, custom aggregations, complex WHERE filters,
  time-series analysis, or SQL-level flexibility on blockchain data. Supports x402/MPP auto-payment.
  Keywords: GraphQL, query, cube, DEXTrades, TokenRanking, OHLC, aggregation, join, on-chain analytics, custom query.
---

# ChainStream GraphQL

Flexible GraphQL interface to ChainStream's on-chain data warehouse. 22 cubes covering DEX trades, token analytics, wallet PnL, transfers, blocks, transactions, and more — across Solana, Ethereum, and BSC.

- **Endpoint**: `https://graphql.chainstream.io/graphql` (routed through APISIX gateway)
- **CLI**: `npx @chainstream-io/cli graphql`
- **Auth**: API Key via `X-API-KEY` header
- **Payment**: x402 (USDC on Base/Solana) or MPP (USDC.e on Tempo) — auto-handled by CLI

## When to Use GraphQL vs chainstream-data

| Scenario | Use | Why |
|----------|-----|-----|
| Standard token search, market trending, wallet profile | `chainstream-data` (REST/MCP) | Pre-built endpoints, simpler |
| Cross-cube JOIN (trades + instructions, trades + token names) | **GraphQL** | joinXxx support |
| Custom aggregation (count, sum, avg with groupBy) | **GraphQL** | Metrics + dimension grouping |
| Complex filters (multi-condition WHERE, nested) | **GraphQL** | Full filter operator support |
| Time-series data with custom resolution | **GraphQL** | OHLC cube + time filters |
| Data not exposed by REST API | **GraphQL** | Direct access to all 22 cubes |

## Integration Path

1. **Has API Key?**
   → YES → Use CLI directly: `npx @chainstream-io/cli graphql query --query '...'`
   → NO → CLI auto-handles on first 402 (see Payment section below)

2. **First time / unsure about schema?**
   → Run `npx @chainstream-io/cli graphql schema --summary` to discover available cubes
   → Run `npx @chainstream-io/cli graphql schema --type DEXTrades` to drill into a specific cube

3. **Need full schema reference for complex query construction?**
   → Run `npx @chainstream-io/cli graphql schema --full` for complete field list + rules

## Getting an API Key

GraphQL goes through ChainStream's unified APISIX gateway — **same API Key and subscription quota as the REST API**.

- **Dashboard users**: [app.chainstream.io](https://app.chainstream.io) → API Keys
- **AI Agents (x402)**: CLI auto-purchases on first 402 — USDC on Base or Solana → API Key auto-saved to `~/.config/chainstream/config.json`
- **AI Agents (MPP)**: `tempo request "https://api.chainstream.io/mpp/purchase?plan=<PLAN>"` → API Key auto-returned
- **CLI auto-payment**: No pre-purchase needed. First `graphql query` that triggers 402 → interactive plan selection → payment → auto-retry

```bash
# Option A: Set existing API Key
npx @chainstream-io/cli config set --key apiKey --value <your-api-key>

# Option B: Create wallet for x402 auto-payment
npx @chainstream-io/cli login

# Option C: Check pricing first
npx @chainstream-io/cli wallet pricing
```

## Endpoint Selector

| Intent | CLI Command |
|--------|-------------|
| List all cubes + descriptions | `npx @chainstream-io/cli graphql schema --summary` |
| Explore one cube's fields | `npx @chainstream-io/cli graphql schema --type <CubeName>` |
| Full schema reference | `npx @chainstream-io/cli graphql schema --full` |
| Force-refresh cached schema | `npx @chainstream-io/cli graphql schema --summary --refresh` |
| Execute inline query | `npx @chainstream-io/cli graphql query --query '<graphql>'` |
| Execute query from file | `npx @chainstream-io/cli graphql query --file ./query.graphql` |
| Execute with variables | `npx @chainstream-io/cli graphql query --query '...' --var '{"network":"eth"}'` |
| Machine-readable output | Append `--json` to any command |

## AI Workflow

### Step 1: Discover Schema (first time or when unsure)

```bash
npx @chainstream-io/cli graphql schema --summary
```

This returns a compact list of all 22 cubes with descriptions and top-level fields. If you need details on a specific cube:

```bash
npx @chainstream-io/cli graphql schema --type DEXTrades
```

### Step 2: Construct and Execute Query

**MANDATORY — READ** [references/schema-guide.md](references/schema-guide.md) before constructing your first query.

Based on schema knowledge + user intent, construct a GraphQL query and execute:

```bash
npx @chainstream-io/cli graphql query --query 'query {
  DEXTrades(network: sol, limit: {count: 25}, orderBy: Block_Time_DESC) {
    Block { Time }
    Trade { Buy { Currency { MintAddress } Amount PriceInUSD } Sell { Currency { MintAddress } Amount } Dex { ProtocolName } }
  }
}' --json
```

If the user has no subscription, CLI auto-handles x402 payment transparently — prompts for plan, pays, retries.

### Step 3: Analyze Results

- Parse JSON output
- Identify data patterns (time series, ranking, distribution, comparison)
- Provide insights in natural language
- If visualization is needed, choose appropriate chart type based on data shape

## Query Construction Quick Reference

```
query {
  CubeName(network: sol|eth|bsc, limit: {count: N}, orderBy: Field_DESC, where: {...}) {
    FieldGroup { SubField }
    joinXxx { ... }
    count
  }
}
```

- **network**: Required on every cube. `sol` = Solana, `eth` = Ethereum, `bsc` = BSC.
- **limit**: `{count: N, offset: M}`. Default 25.
- **orderBy**: `FieldPath_ASC` or `FieldPath_DESC`. Most cubes default to `Block_Time_DESC`.
- **where**: `{Group: {Field: {operator: value}}}`.
- **DateTime format**: `"YYYY-MM-DD HH:MM:SS"` — NO `T`, NO `Z`. Critical for ClickHouse.
- **DateTimeFilter**: `since`, `till`, `after`, `before` — NEVER `gt`/`lt`.
- **joinXxx**: LEFT JOIN to related cubes. Always prefer over multiple queries.

## NEVER Do

- NEVER use Bitquery syntax (`{ Solana { ... } }` or `{ EVM { ... } }`) — this is a completely different schema
- NEVER guess field names without checking schema first — run `graphql schema --summary` or `--type`
- NEVER use ISO 8601 datetime format (`2026-03-31T00:00:00Z`) — ClickHouse requires `"2026-03-31 00:00:00"`
- NEVER use `gt`/`lt` on DateTime fields — use `since`/`after`/`before`/`till`
- NEVER split related data into multiple queries when joinXxx can combine them
- NEVER auto-select a payment plan — always let the user choose

## Error Recovery

| Error | Meaning | Recovery |
|-------|---------|----------|
| 401 / "Not authenticated" | No API Key configured | `npx @chainstream-io/cli config set --key apiKey --value <key>` |
| 402 | No active subscription | CLI auto-handles: plan selection → x402/MPP payment → retry. **MANDATORY — READ** [`shared/x402-payment.md`](../shared/x402-payment.md) for manual purchase flow |
| "GraphQL error: ..." | Invalid query syntax or non-existent field | Check field names against `graphql schema --type <cube>` |
| 429 | Rate limit | Wait 1s, exponential backoff |
| 5xx | Server error | Retry once after 2s |

On 401/402: ask the user "Do you have a ChainStream API Key?" — if yes, set it; if no, load [`shared/x402-payment.md`](../shared/x402-payment.md) for the full purchase flow. GraphQL shares the same API Key / subscription pool as the REST API — no separate purchase needed.

## Skill Map

| Reference | Content | When to Load |
|-----------|---------|--------------|
| [schema-guide.md](references/schema-guide.md) | Query syntax, filter operators, joinXxx rules, common mistakes | Before constructing any query |
| [query-patterns.md](references/query-patterns.md) | 15+ ready-to-use query templates by scenario | When building queries for common use cases |
| [x402-payment.md](../shared/x402-payment.md) | x402 and MPP payment protocols, plan purchase flow | On 402 errors or when user needs subscription |
| [authentication.md](../shared/authentication.md) | API Key setup, wallet auth, MCP config | On auth errors |

## Related Skills

- [chainstream-data](../chainstream-data/) — Standard REST/MCP queries for common analytics (token search, market trending, wallet profile). Use when pre-built endpoints suffice.
- [chainstream-defi](../chainstream-defi/) — DeFi execution: swap, bridge, create token, sign transactions. Use when analysis leads to action.
