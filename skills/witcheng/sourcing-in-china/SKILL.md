---
name: sourcing-in-china
description: Search products, suppliers, and get detailed product info from Made-in-China.com via MCP server. Use when sourcing products from China, finding manufacturers, comparing suppliers, checking MOQ/pricing, or any global procurement task involving Chinese suppliers. Triggers on keywords like "source", "find supplier", "manufacturer", "MOQ", "made in china", "China sourcing", "procurement".
---

# Sourcing in China

Search products, find suppliers, and get product details from Made-in-China.com using the `made-in-china` MCP server via `mcporter`.

## Prerequisites

- `mcporter` CLI installed (`npm i -g mcporter`)
- MCP server `made-in-china` configured in `config/mcporter.json` with SSE endpoint: `https://mcp.chexb.com/sse`
- See [mcporter docs](https://mcporter.dev) for configuration details

## Available Tools

| Tool | Purpose | Key Params |
|------|---------|------------|
| `search_products` | Search products by keyword | `keyword`, `page` (30/page) |
| `search_suppliers` | Search manufacturers/suppliers | `keyword`, `page` (10/page) |
| `get_product_detail` | Full product page details | `url` (product URL) |

## Quick Commands

```bash
# Search products
mcporter call made-in-china.search_products keyword="LED light" page=1

# Search suppliers
mcporter call made-in-china.search_suppliers keyword="LED light"

# Get product detail (use URL from search results)
mcporter call made-in-china.get_product_detail url="https://..."
```

## Sourcing Workflow

### 1. Product Discovery

Start with `search_products` to find products matching requirements. Each result includes:
- Product name, price, MOQ
- Key specifications (properties)
- Supplier name and link
- Product image

Iterate pages for broader results. Refine keywords for precision (e.g., "12V LED strip waterproof" vs "LED").

### 2. Supplier Evaluation

Use `search_suppliers` to find manufacturers. Results include:
- Company name and business type (Manufacturer / Trading Company)
- Main products and location
- Certification badges (ISO, audited, etc.)

**Prefer manufacturers over trading companies** for better pricing. Check badges for quality signals.

### 3. Product Deep Dive

Use `get_product_detail` on promising products. Returns:
- Full specifications and description
- All product images
- Sample pricing (if available)
- Product categories and video URL
- Supplier/brand info

### 4. Comparison & Recommendation

When comparing options, organize by:
- **Price range** (unit price + MOQ)
- **Supplier credibility** (badges, business type)
- **Specifications match** (vs buyer requirements)
- **Sample availability** (sample price if listed)

## Best Practices

- Use English keywords for best results on Made-in-China.com
- Search both products AND suppliers for the same keyword to get different perspectives
- Always check MOQ — it varies dramatically between suppliers
- "Manufacturer" business type typically means better unit pricing
- Cross-reference supplier badges: Audited Supplier > general listings
- For detailed specs, always follow up with `get_product_detail`

## Output Format

Present results in clean, scannable format:
- Use tables for product/supplier comparisons
- Highlight price, MOQ, and key specs prominently
- Include direct links to products and supplier pages
- Flag notable badges or certifications

For more on sourcing strategy, see [references/sourcing-guide.md](references/sourcing-guide.md).
