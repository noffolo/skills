# Opportunity Discovery Module

> **Purpose**: Search DeFi yield opportunities across multiple sources with real-time data.

---

## What It Does

Searches DeFi yield opportunities across multiple sources with real-time data.

## Key Features

- **Risk Signals**: Each opportunity includes structured risk data:
  - `reward_type`: "none" | "single" | "multi"
  - `has_il_risk`: true | false (impermanent loss)
  - `underlying_type`: "rwa" | "onchain" | "mixed" | "unknown"
- **Actionable Addresses**: Contract addresses ready for execution
- **LLM-Ready Output**: Structured JSON optimized for AI analysis

## Data Sources (Priority Order)

1. **DefiLlama API** (primary) - Free, no API key required
2. **Dune MCP** (optional) - Deep analytics if configured
3. **Protocol Registry** (fallback) - Static metadata for known protocols

## Usage Examples

```bash
# Search Ethereum opportunities with min 5% APY
python3 scripts/discovery/find_opportunities.py \
  --chain ethereum \
  --min-apy 5 \
  --limit 20

# Search stablecoin products only
python3 scripts/discovery/find_opportunities.py \
  --chain ethereum \
  --min-apy 3 \
  --max-apy 25 \
  --limit 50

# Output for LLM analysis
python3 scripts/discovery/find_opportunities.py \
  --chain ethereum \
  --llm-ready \
  --output json
```

## Output Format

### Standard Output

```
# DeFi Opportunities on ethereum

## 1. Aave V3 USDC
- APY: 5.23%
- TVL: $1,234,567,890
- Pool: 0x...
- Risk: single reward, no IL
```

### LLM-Ready Output (JSON)

```json
{
  "opportunities": [
    {
      "name": "Aave V3 USDC",
      "chain": "ethereum",
      "apy": 5.23,
      "tvl": 1234567890,
      "pool_address": "0x...",
      "reward_type": "single",
      "has_il_risk": false,
      "underlying_type": "onchain"
    }
  ]
}
```

## Troubleshooting

### No Opportunities Found
- Check chain name spelling (case-sensitive in some cases)
- Try lowering `--min-apy` threshold
- Ensure `--max-apy` isn't too restrictive

### Rate Limiting
- DefiLlama has generous limits but can occasionally rate limit
- Add delays between requests if batch processing