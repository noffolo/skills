---
name: wallet-balance
description: Query multi-chain wallet balances for EVM and BTC addresses. Supports address memory for quick re-query. Optional Tokenview API for comprehensive asset coverage; falls back to public data sources when not configured.
version: 1.1.4
author: Antalpha AI Team
metadata:
  requires:
    - node
  install:
    type: npm
    command: npm install && npm start
  env:
    - name: PORT
      description: Service port (default 3000)
      required: false
    - name: REDIS_URL
      description: Redis URL for caching and rate limiting
      required: false
    - name: TOKENVIEW_API_KEY
      description: Tokenview API key for comprehensive token coverage
      required: false
      sensitive: true
    - name: TOKENVIEW_BASE_URL
      description: Tokenview API base URL
      required: false
    - name: TOKENVIEW_MULTI_CHAIN_PATH
      description: Tokenview API path template with {address} placeholder
      required: false
    - name: TOKENVIEW_PROBE_IF_NO_PATH
      description: Probe candidate URLs if no path template configured (default false)
      required: false
    - name: ENABLE_FALLBACK_PROVIDER
      description: Fallback to public sources if Tokenview fails (default true)
      required: false
    - name: ETH_RPC_URL
      description: Ethereum RPC endpoint
      required: false
    - name: BNB_RPC_URL
      description: BSC RPC endpoint
      required: false
    - name: MEMORY_STORE_PATH
      description: Custom path for address memory file
      required: false
---

# Wallet Balance Skill

> **Multi-chain asset overview. Zero config required.**

## What This Does

Query wallet balances across multiple chains:

- **EVM Chains**: Ethereum, BSC, Base, Arbitrum, Polygon
- **Bitcoin**: BTC addresses
- **Address Memory**: Remember addresses for quick re-query
- **Portfolio View**: Combined total across all chains

**Optional**: Configure Tokenview API for comprehensive token coverage.

## Installation

### Prerequisites

- **Node.js 18+** - Required to run the gateway
- **Redis (optional)** - For caching and rate limiting

### Quick Install

```bash
cd skills/wallet-balance
npm install
npm start
```

The gateway will start on port 3000 (or set `PORT` in `.env`).

## Quick Start

```bash
# Query single address
curl "http://127.0.0.1:3000/agent-skills/v1/assets?input=0x..."

# Query from memory
curl "http://127.0.0.1:3000/agent-skills/v1/assets?from_memory=1"

# Add address to memory
curl -X POST "http://127.0.0.1:3000/agent-skills/v1/memory" \
  -H "Content-Type: application/json" \
  -d '{"add":"0x..."}'
```

## Commands

### Query Single Address

```bash
GET /agent-skills/v1/assets?input=<address-or-domain>
```

**Parameters**:
- `input` - Wallet address (0x..., bc1..., etc.) or ENS/BNB domain
- `refresh=1` - Skip cache and fetch fresh data

**Example Response**:
```json
{
  "status": "ok",
  "address": "0x...",
  "total_usd": "5188.18",
  "chains": [
    {
      "chain": "Ethereum",
      "chain_id": 1,
      "tokens": [
        {
          "symbol": "USDT",
          "amount": "5185.5",
          "value_usd": "5184.26",
          "token_kind": "erc20"
        },
        {
          "symbol": "ETH",
          "amount": "0.00179932",
          "value_usd": "3.92",
          "token_kind": "native"
        }
      ]
    }
  ],
  "data_source": "public_only",
  "attribution": "Data aggregated by Antalpha AI"
}
```

### Query Memory (Multiple Addresses)

```bash
GET /agent-skills/v1/assets?from_memory=1
```

Returns combined portfolio across all remembered addresses.

### Memory Management

```bash
# List remembered addresses
GET /agent-skills/v1/memory

# Add address(es)
POST /agent-skills/v1/memory
Body: {"add": "0x..."} or {"add": ["0x...", "bc1..."]}

# Remove address
POST /agent-skills/v1/memory
Body: {"remove": "0x..."}
```

## Supported Inputs

| Type | Example | Notes |
|------|---------|-------|
| EVM Address | `0x4Da2...C0490` | Any EVM chain |
| BTC Address | `bc1q...` or `1A...` | Bitcoin mainnet |
| ENS Domain | `vitalik.eth` | Ethereum name service |
| BNB Domain | `example.bnb` | BSC name service |

## Data Sources

| Configuration | Coverage |
|---------------|----------|
| No Tokenview | ETH, BSC native + USDT only |
| With Tokenview | Full multi-chain portfolio |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | Gateway port |
| `REDIS_URL` | - | Optional Redis for caching |
| `TOKENVIEW_API_KEY` | - | Optional for full coverage |
| `ETH_RPC_URL` | PublicNode | Ethereum RPC endpoint |
| `BNB_RPC_URL` | PublicNode | BSC RPC endpoint |

## Response Format

### Single Address Response

- `total_usd` - Total portfolio value in USD
- `chains[]` - Assets grouped by chain
- `chains[].tokens[]` - Token balances and values
- `data_source` - `public_only` or `tokenview`
- `attribution` - Data source attribution

### Memory Query Response

- `query_mode: "memory"`
- `results[]` - Array of individual address results
- `combined_total_usd` - Aggregated portfolio value

## Security Notes

- **Local HTTP Server**: This skill starts a local HTTP server on the configured port (default 3000)
- **File Persistence**: Address memory is persisted to `remembered-addresses.json` by default, or the path specified by `MEMORY_STORE_PATH`
- **External Requests**: Wallet addresses are sent to external services (RPC providers, CoinGecko, optionally Tokenview)
- **No Private Keys**: This skill never requires or handles private keys
- **Redis Optional**: Service works without Redis, but with no caching or rate limiting
- **Rate Limiting**: When Redis is available, requests are rate-limited per IP and address

## Health Check

```bash
curl http://127.0.0.1:3000/healthz
```

---

**Maintainer**: Antalpha AI Team  
**License**: MIT