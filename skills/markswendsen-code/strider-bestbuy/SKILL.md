---
name: strider-bestbuy
description: Shop at Best Buy via Strider Labs MCP connector. Search electronics, check store inventory, place orders, and schedule Geek Squad services.
metadata:
  openclaw:
    requires:
      bins: ["npx"]
    category: "commerce"
    author: "Strider Labs"
    homepage: "https://striderlabs.ai"
---

# Strider Best Buy Connector

MCP connector for shopping at Best Buy. Part of the Strider Labs action execution layer for AI agents.

## Installation

```bash
npm install @striderlabs/mcp-bestbuy
```

## MCP Configuration

Add to your MCP client configuration (Claude Desktop, Cursor, etc.):

```json
{
  "mcpServers": {
    "bestbuy": {
      "command": "npx",
      "args": ["-y", "@striderlabs/mcp-bestbuy"]
    }
  }
}
```

## Available Tools

### bestbuy.search_products
Search for products at Best Buy.

**Input Schema:**
```json
{
  "query": "string",
  "category": "string (optional)",
  "min_price": "number (optional)",
  "max_price": "number (optional)",
  "on_sale": "boolean (optional)"
}
```

**Output:**
```json
{
  "products": [
    {
      "sku": "string",
      "name": "string",
      "price": "number",
      "original_price": "number",
      "rating": "number",
      "in_stock": "boolean",
      "store_pickup": "boolean"
    }
  ]
}
```

### bestbuy.check_store_inventory
Check product availability at nearby stores.

### bestbuy.add_to_cart
Add a product to shopping cart.

### bestbuy.place_order
Complete checkout with shipping or store pickup.

### bestbuy.schedule_geek_squad
Schedule Geek Squad installation or repair service.

### bestbuy.get_order_status
Track order shipping or pickup status.

## Authentication

First use triggers OAuth authorization flow:
1. User is redirected to Best Buy to authorize
2. Tokens are stored encrypted per-user
3. Automatic refresh handles token expiration

## Usage Examples

**Search for products:**
```
Find 4K TVs under $800 at Best Buy
```

**Check store availability:**
```
Is the Sony WH-1000XM5 in stock at Best Buy near me?
```

**Order with pickup:**
```
Order the MacBook Air from Best Buy with store pickup today
```

**Schedule installation:**
```
Schedule Geek Squad to install my new TV this weekend
```

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| AUTH_EXPIRED | Session expired | Re-authenticate |
| OUT_OF_STOCK | Item unavailable | Check other stores |
| RATE_LIMITED | Too many requests | Retry after delay |
| STORE_CLOSED | Location unavailable | Select different store |

## Use Cases

- Electronics shopping: TVs, laptops, phones, audio equipment
- Same-day pickup: Order online, pick up in store within hours
- Price matching: Check prices against competitors
- Tech support: Schedule Geek Squad for setup and repairs

## Links

- npm: https://npmjs.com/package/@striderlabs/mcp-bestbuy
- Strider Labs: https://striderlabs.ai
- MCP Registry: https://registry.modelcontextprotocol.io
