# ChainStream GraphQL Query Patterns

Ready-to-use query templates for common blockchain analytics scenarios. Replace placeholder values (`TOKEN_ADDRESS`, `WALLET_ADDRESS`, etc.) with actual addresses.

All queries use `network: sol` (Solana) by default. Change to `eth` or `bsc` as needed.

## Token Discovery & Ranking

### Trending Tokens (by 24h volume)

```graphql
query {
  TokenRanking(network: sol, limit: {count: 50}, orderBy: Volume24hUSD_DESC) {
    Token { Address Name Symbol }
    PriceUSD
    Volume24hUSD
    Trades24h
    PriceChange24hPct
    MarketCapUSD
  }
}
```

### Token Latest Price

```graphql
query {
  TokenLatestPrice(network: sol, where: {Token: {Address: {is: "So11111111111111111111111111111111111111112"}}}) {
    Token { Address }
    PriceUSD
    LastTradeAt
  }
}
```

### Token Search (metadata + stats)

```graphql
query {
  TokenSearch(network: sol, tokenAddress: {is: "TOKEN_ADDRESS"}, limit: {count: 1}) {
    Token {
      Address Decimals PriceUSD MarketCapUSD
      TotalTradeCount TotalVolumeUSD HolderCount PoolCount
    }
  }
}
```

### Token Market Cap

```graphql
query {
  TokenMarketCap(network: sol, tokenAddress: {is: "TOKEN_ADDRESS"}, limit: {count: 1}) {
    Token { Address }
    PriceUSD MarketCapUSD TotalSupply FDVUSD LastSeen
  }
}
```

## DEX Trades

### Latest Trades

```graphql
query {
  DEXTrades(network: sol, limit: {count: 25}, orderBy: Block_Time_DESC) {
    Block { Time }
    Trade {
      Buy { Currency { MintAddress } Amount PriceInUSD }
      Sell { Currency { MintAddress } Amount }
      Dex { ProtocolName }
    }
  }
}
```

### Trades for a Specific Token

```graphql
query {
  DEXTrades(network: sol, limit: {count: 25}, tokenAddress: {is: "TOKEN_ADDRESS"}, orderBy: Block_Time_DESC) {
    Block { Time }
    Trade {
      Buy { Amount PriceInUSD Account { Owner } }
      Sell { Currency { MintAddress } Amount }
      Dex { ProtocolName }
    }
    Pool { Address }
  }
}
```

### Trades with Token Names (joinBuyToken)

```graphql
query {
  DEXTrades(network: sol, limit: {count: 25}, orderBy: Block_Time_DESC) {
    Block { Time }
    Trade {
      Buy { Currency { MintAddress } Amount PriceInUSD }
      Sell { Currency { MintAddress } Amount }
    }
    joinBuyToken { Token { Name Symbol ImageUrl } }
    joinSellToken { Token { Name Symbol } }
  }
}
```

### Top Traders by Volume

```graphql
query {
  DEXTrades(
    network: sol
    limit: {count: 100}
    tokenAddress: {is: "TOKEN_ADDRESS"}
    where: {IsSuspect: {eq: false}}
  ) {
    Trade { Buy { Account { Owner } Amount PriceInUSD } }
    count
    sum(of: Trade_Buy_Amount)
  }
}
```

### pump.fun Trades (Last 7 Days)

```graphql
query {
  DEXTrades(
    network: sol
    where: {
      Block: {Time: {since: "2026-03-24 00:00:00"}}
      Trade: {Dex: {ProgramAddress: {is: "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"}}}
    }
    limit: {count: 1000}
    orderBy: Block_Time_DESC
  ) {
    Block { Time }
    Trade {
      Buy { Currency { MintAddress } Amount }
      Sell { Currency { MintAddress } Amount }
      Dex { ProtocolName }
    }
  }
}
```

### Trade Count (Aggregation Only)

```graphql
query {
  DEXTrades(network: sol, where: {Block: {Time: {since: "2026-03-24 00:00:00"}}}) {
    count
  }
}
```

## OHLCV / K-Line

### K-Line Data for a Token

```graphql
query {
  OHLC(network: sol, limit: {count: 24}, tokenAddress: {is: "TOKEN_ADDRESS"}) {
    TimeMinute
    Token { Address }
    Price { Open High Low Close }
    VolumeUSD
    TradeCount
  }
}
```

### Trade Statistics (Buy/Sell breakdown)

```graphql
query {
  TokenTradeStats(network: sol, limit: {count: 24}, tokenAddress: {is: "TOKEN_ADDRESS"}) {
    TimeMinute
    Token { Address }
    TradeCount BuyCount SellCount
    VolumeUSD UniqueBuyers UniqueSellers
  }
}
```

## Wallet Analysis

### Wallet PnL by Token

```graphql
query {
  WalletTokenPnL(network: sol, limit: {count: 20}, walletAddress: {is: "WALLET_ADDRESS"}) {
    Wallet { Address }
    Token { Address }
    BuyVolumeUSD SellVolumeUSD
    BuyCount SellCount
    FirstTrade LastTrade
  }
}
```

### Token Top Holders

```graphql
query {
  TokenHolders(network: sol, limit: {count: 20}, tokenAddress: {is: "TOKEN_ADDRESS"}) {
    Holder { Address }
    Token { Address }
    Balance BalanceUSD
    LastUpdated
  }
}
```

## Transfers

### Latest Transfers

```graphql
query {
  Transfers(network: sol, limit: {count: 20}, orderBy: Block_Time_DESC) {
    Block { Time }
    Transaction { Hash }
    Transfer {
      Currency { MintAddress }
      Sender { Address }
      Receiver { Address }
      Amount AmountInUSD
    }
  }
}
```

### Wallet Outgoing Transfers

```graphql
query {
  Transfers(network: sol, limit: {count: 20}, senderAddress: {is: "WALLET_ADDRESS"}, orderBy: Block_Time_DESC) {
    Block { Time }
    Transfer {
      Currency { MintAddress }
      Receiver { Address }
      Amount AmountInUSD
    }
  }
}
```

## Transactions (with Joins)

### Solana Transaction with Full Details

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

### EVM Transaction with Logs and Traces

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

## Pools & Liquidity

### DEX Pools for a Token

```graphql
query {
  DEXPools(network: sol, limit: {count: 20}, tokenAddress: {is: "TOKEN_ADDRESS"}) {
    Pool { Address ProgramAddress }
    TokenA { Address }
    TokenB { Address }
    Dex { ProtocolName }
  }
}
```

### Pool Liquidity Snapshots

```graphql
query {
  PoolLiquiditySnapshots(network: sol, limit: {count: 20}, tokenAddress: {is: "TOKEN_ADDRESS"}) {
    Pool { Address ProgramAddress }
    TokenA { Address }
    TokenB { Address }
    LiquidityUSD EventCount LastSeen
  }
}
```

## Blocks

### Latest Blocks

```graphql
query {
  Blocks(network: sol, limit: {count: 10}, orderBy: Block_Time_DESC) {
    Block {
      Time Slot Number Hash TxCount TotalFee
    }
  }
}
```

## Pattern Reference: Data Shape → Chart Type

When analyzing query results, use this mapping to choose appropriate visualization:

| Data Pattern | Recommended Chart | Example Query |
|-------------|------------------|---------------|
| Time series (price, volume over time) | Line / Candlestick | OHLC, TokenTradeStats |
| Ranking (top tokens, top holders) | Bar chart / Leaderboard | TokenRanking, TokenHolders |
| Distribution (asset allocation) | Pie / Treemap | WalletTokenPnL grouped |
| Comparison (cross-chain, cross-protocol) | Grouped bar | DEXTrades grouped by Dex |
| Real-time feed (trade stream) | Table with scrolling | DEXTrades latest |
| Single metric (total count, total volume) | Metric card | Aggregation-only queries |
