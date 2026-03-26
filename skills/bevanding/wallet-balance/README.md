# Wallet Balance Gateway

Multi-chain wallet balance query gateway for EVM and BTC. Optional Tokenview integration; falls back to public data sources when Tokenview is not configured.

## API Endpoints

- `GET /agent-skills/v1/assets?input=<address-or-domain>` - Query single address
- `GET /agent-skills/v1/assets?from_memory=1` - Query all remembered addresses
- `GET /agent-skills/v1/memory` - List remembered addresses
- `POST /agent-skills/v1/memory` - Add/remove addresses
- `GET /healthz` - Health check

## Quick Start

```bash
cp .env.example .env
# Optional: edit .env to add TOKENVIEW_API_KEY
npm install
npm start
```

## Memory File

Default: `remembered-addresses.json` (same directory as server.js)
Override with: `MEMORY_STORE_PATH` environment variable

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | Service port |
| `REDIS_URL` | - | Optional Redis for caching and rate limiting |
| `TOKENVIEW_API_KEY` | - | Optional for comprehensive token coverage |
| `TOKENVIEW_MULTI_CHAIN_PATH` | - | API path template with `{address}` placeholder |
| `ENABLE_FALLBACK_PROVIDER` | true | Fallback to public sources if Tokenview fails |
| `ETH_RPC_URL` | PublicNode | Ethereum RPC endpoint |
| `BNB_RPC_URL` | PublicNode | BSC RPC endpoint |
| `MEMORY_STORE_PATH` | - | Optional custom path for memory file |

## Redis (Optional)

Redis provides:
- **Caching**: 5-minute query cache
- **Rate Limiting**: 10 req/min per IP, 5 req/min per address

Without Redis:
- Queries work normally
- No caching (slower responses)
- No rate limiting

Install Redis: `sudo apt install redis-server`

## Packaging

Exclude when packaging:
- `node_modules/`
- `.env`
- `remembered-addresses.json`

After extraction, run `npm install` and configure `.env`.

---

**Maintainer**: Antalpha AI Team  
**License**: MIT