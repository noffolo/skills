# ChainStream GraphQL Schema Guide

Complete reference for constructing valid ChainStream GraphQL queries. This is NOT Bitquery — the schema is completely different.

## Query Format

```graphql
query {
  CubeName(network: sol, limit: {count: 25}, orderBy: Block_Time_DESC, where: {...}) {
    FieldGroup {
      SubField
    }
    joinXxx {
      TargetField
    }
    count
  }
}
```

### Required Parameters

- **network**: Must be present on every cube. Values: `sol` (Solana), `eth` (Ethereum), `bsc` (BSC/BNB Chain). Default: `sol`.

### Optional Parameters

- **limit**: `{count: N, offset: M}`. Default count is 25. Max varies by cube (check `graphql schema --type`).
- **orderBy**: `FieldPath_ASC` or `FieldPath_DESC`. Path reflects schema hierarchy — nested fields use `Parent_Field` format (e.g. `Block_Time_DESC`).
- **where**: Filter object `{FieldGroup: {Field: {operator: value}}}`.
- **limitBy**: Group limiting `{by: "FieldPath", count: N}` — returns top N per group.

## Filter Operators

| Type | Operators | Example |
|------|-----------|---------|
| **StringFilter** | `is`, `not`, `in`, `notIn`, `like`, `includes`, `isNull` | `{is: "0xabc..."}` |
| **IntFilter** | `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `in`, `notIn`, `isNull` | `{gt: 1000}` |
| **FloatFilter** | `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `in`, `notIn`, `isNull` | `{ge: 0.5}` |
| **DateTimeFilter** | `is`, `not`, `since`, `till`, `after`, `before`, `isNull` | `{since: "2026-03-24 00:00:00"}` |
| **BoolFilter** | `eq`, `isNull` | `{eq: true}` |

### CRITICAL: DateTime Filters

DateTime fields (e.g. `Block.Time`) use **DateTimeFilter** — NOT IntFilter!

```
WRONG: Block: {Time: {gt: "2026-03-24 00:00:00"}}     ← gt does NOT exist on DateTimeFilter
RIGHT: Block: {Time: {since: "2026-03-24 00:00:00"}}   ← use since/after/before/till
```

## Date/Time Format

The database uses ClickHouse DateTime64. You MUST use this format:

```
"2026-03-31 00:00:00"   ← CORRECT (space-separated, no T, no Z)
"2026-03-31T00:00:00Z"  ← WRONG — causes ClickHouse TYPE_MISMATCH error
"2026-03-31"             ← WRONG — must include time portion
```

For relative time queries, compute the actual date string:
- "last 7 days" → `since: "2026-03-24 00:00:00"`
- "last 24 hours" → `since: "2026-03-30 00:00:00"`

## Metrics (Aggregation)

Available metrics: `count`, `sum`, `avg`, `min`, `max`, `uniq`

| Usage | SQL Equivalent |
|-------|---------------|
| `count` | `COUNT(*)`  |
| `count(of: Field)` | `COUNT(DISTINCT field)` |
| `sum(of: Field)` | `SUM(field)` |
| `avg(of: Field)` | `AVG(field)` |

**Key rule**: For a total aggregate (single number), select ONLY the metric — do NOT include dimension fields. If you include dimension fields alongside a metric, results are grouped by those dimensions.

```graphql
# Total count (no grouping)
query { DEXTrades(network: sol, where: {...}) { count } }

# Count grouped by Dex
query { DEXTrades(network: sol, where: {...}) { Trade { Dex { ProtocolName } } count } }
```

## Cross-Cube JOIN (joinXxx)

**ALWAYS prefer joinXxx over multiple separate queries.** When a user wants data from related cubes, generate ONE query with joinXxx fields.

joinXxx adds a LEFT JOIN to the target cube, returning related fields inline. Available joins are listed per cube in the schema.

### Key Join Scenarios

**Token name/symbol enrichment** (→ TokenSearch):
- DEXTrades: `joinBuyToken`, `joinSellToken`
- Transfers, BalanceUpdates, OHLC: `joinToken`
- PoolLiquiditySnapshots, PoolSlippageStats: `joinTokenA`, `joinTokenB`

```graphql
query {
  DEXTrades(network: sol, limit: {count: 25}, orderBy: Block_Time_DESC) {
    Block { Time }
    Trade { Buy { Currency { MintAddress } Amount PriceInUSD } }
    joinBuyToken { Token { Name Symbol ImageUrl } }
  }
}
```

**Solana transaction + instructions/trades/transfers:**

```graphql
query {
  SolTransactions(network: sol, limit: {count: 1}, orderBy: Block_Time_DESC) {
    Block { Time Slot Height Hash }
    Signature TxIndex Success Fee FeeInNative FeePayer Signer
    joinInstructions {
      Transaction { Signature Index InnerIndex NestingLevel Program { Id Name MethodName } }
    }
    joinDEXTrades {
      Trade { Buy { Currency { MintAddress } Amount PriceInUSD } Sell { Currency { MintAddress } Amount } }
    }
    joinTransfers {
      Transfer { Currency { MintAddress } Amount AmountInUSD }
    }
  }
}
```

**EVM transaction + logs/traces:**

```graphql
query {
  EVMTransactions(network: eth, limit: {count: 1}, orderBy: Block_Time_DESC) {
    Block { Time Height Hash }
    Hash From To Success Gas { Used Price }
    joinLogs { LogIndex Address EventName Topics { Topic0 Topic1 } Data }
    joinTraces { TraceIndex CallType FromAddress ToAddress ValueInNative GasUsed }
  }
}
```

**Aggregation enrichment** (market cap, ranking, price):
- DEXTrades: `joinBuyTokenMarketCap`, `joinBuyTokenPrice`, `joinBuyTokenRanking`
- DEXPools: `joinPoolLiquidity`, `joinPoolSlippage`
- Transfers: `joinTokenMarketCap`

### V1 Constraints

- Max 1 level of join (no nested joins)
- LEFT JOIN only

## Common Mistakes

| WRONG | CORRECT | Note |
|-------|---------|------|
| `PriceChange24h` | `PriceChange24hPct` | Always use the `Pct` suffix |
| `PriceChange1h` | `PriceChange1hPct` | Same |
| `DEXTrades.Currency.Symbol` | `joinBuyToken { Token { Symbol } }` | Currency only has MintAddress + Decimals |
| `DEXTrades.Currency.Name` | `joinBuyToken { Token { Name } }` | Use join for name/symbol |
| `{ Solana { ... } }` | `CubeName(network: sol)` | NOT Bitquery format |
| `Block: {Time: {gt: "..."}}` | `Block: {Time: {since: "..."}}` | DateTimeFilter, not IntFilter |
| `"2026-03-31T00:00:00Z"` | `"2026-03-31 00:00:00"` | ClickHouse format, no T/Z |
| `SolTransactions: Timestamp` | `SolTransactions: Block { Time }` | Field renamed and moved into Block |
| `SolTransactions: orderBy: Timestamp_DESC` | `orderBy: Block_Time_DESC` | Updated order path |
| `EVMTransactions: Block { Number }` | `Block { Height }` | Number renamed to Height |
| Two queries for "trades + instructions" | One query with `joinInstructions` | Single query principle |

## Rules Summary

1. **MUST** include `network` parameter on every cube.
2. **STRICTLY** use only field names from the schema. NEVER invent fields.
3. Field names are **CASE-SENSITIVE** and must match exactly.
4. Date/time values **MUST** use `"YYYY-MM-DD HH:MM:SS"` format.
5. DateTime filters **MUST** use `since`/`after`/`before`/`till`.
6. **SINGLE QUERY PRINCIPLE**: Use joinXxx to combine related data.
7. Default limit 25. Use the cube's default orderBy (usually `Block_Time_DESC`).
