---
name: nexus
description: Interact with Nexus, a multi-tenant Ops OS for ecommerce and retail businesses. Requires a NEXUS_API_KEY environment variable (agent API key with prefix nxs_ak_) — obtain one via self-registration at nexus.aiforstartups.io. Use when asked about CRM contacts, orders, inventory, fulfillment, shipping, omnichannel messaging (WhatsApp, Facebook, Instagram), social media posts, or business operations. Triggers on phrases like "check inventory", "list orders", "send WhatsApp", "customer lookup", "stock level", "create order", "order status", "contact info", "CRM", "fulfillment", "shipping", "social posts", "content calendar".
homepage: https://nexus.aiforstartups.io
source: https://nexus-docs.aiforstartups.io/api/ai-agents-mcp
env:
  - name: NEXUS_API_KEY
    description: Agent API key (prefix nxs_ak_). Obtain via self-registration at nexus.aiforstartups.io — no human approval required.
    required: true
---

# Nexus — Ops OS for AI Agents

Nexus is a multi-tenant operations platform covering CRM, orders, inventory, fulfillment, shipping, omnichannel messaging, social media, and analytics — accessible via a single MCP server.

## API Base URL

```
https://api.nexus.aiforstartups.io/functions/v1
```

## Credentials

Read `NEXUS_API_KEY` from the environment variable. If not set, prompt the user to register at https://nexus.aiforstartups.io and provide their agent API key.

Do **not** use raw Supabase URLs or `nexus.aiforstartups.io/api/v1` — both return 404.

## Authentication

Exchange the API key for a short-lived JWT (valid 1 hour) before every session:

```bash
curl -s -X POST "https://api.nexus.aiforstartups.io/functions/v1/agent-auth" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "$NEXUS_API_KEY"}'
```

Returns `access_token`. Use as `Authorization: Bearer <token>` for all MCP calls. Re-authenticate on HTTP 401.

## Registration (first-time)

If the user has no API key:

```bash
curl -s -X POST "https://api.nexus.aiforstartups.io/functions/v1/agent-register" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "<agent-name>",
    "agent_platform": "openclaw",
    "owner_email": "<owner-email>",
    "organization_name": "<org-name>",
    "plan": "free"
  }'
```

The returned `api_key` is shown once — store it as the `NEXUS_API_KEY` environment variable.

## MCP Server

All tool calls go to:
```
POST https://api.nexus.aiforstartups.io/functions/v1/mcp-server
```

Required headers:
- `Authorization: Bearer <JWT>`
- `Content-Type: application/json`
- `Accept: application/json, text/event-stream`

Initialize before first tool call:
```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"<agent-name>","version":"1.0.0"}}}
```

Call a tool:
```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"<tool-name>","arguments":{...}}}
```

## Available Tools

### CRM & Contacts
| Tool | Scope | Description |
|---|---|---|
| `nexus_list_contacts` | read | List/search contacts (phone, email, journey_stage, search) |
| `nexus_get_contact` | read | Get full contact details + recent orders |
| `nexus_create_contact` | write | Create a new contact |
| `nexus_update_contact` | write | Update contact fields |

### Orders
| Tool | Scope | Description |
|---|---|---|
| `nexus_list_orders` | read | List orders with filters |
| `nexus_get_order` | read | Get order with line items |
| `nexus_create_order` | write | Create order with line items |
| `nexus_update_order_status` | write | Move order through lifecycle |

### Inventory
| Tool | Scope | Description |
|---|---|---|
| `nexus_list_inventory` | read | List inventory items |
| `nexus_check_stock` | read | Check stock by item_id or SKU |

### Omnichannel Messaging
| Tool | Scope | Description |
|---|---|---|
| `nexus_list_conversations` | read | List conversations (whatsapp, facebook, instagram) |
| `nexus_send_message` | write | Send message on existing conversation |

### Search
| Tool | Scope | Description |
|---|---|---|
| `nexus_search` | read | Global search across contacts, orders, inventory |

### Social Media & Content Calendar
| Tool | Scope | Description |
|---|---|---|
| `nexus_list_social_posts` | read | List posts from content calendar |
| `nexus_get_social_post` | read | Get full post details |
| `nexus_create_social_post` | write | Create draft or scheduled post |
| `nexus_update_social_post` | write | Update content, status, or schedule |
| `nexus_delete_social_post` | write | Delete draft or scheduled post |
| `nexus_list_social_accounts` | read | List connected social accounts |
| `nexus_get_social_analytics` | read | Get engagement analytics |
| `nexus_get_content_calendar` | read | View upcoming scheduled posts |

## Plan Limits

| Tier | Price | MCP Scopes |
|---|---|---|
| Free | $0 | read only |
| Starter | $99/mo | read + write |
| Growth | $199/mo | read + write + admin |
| Scale | $599/mo | full + AI suite |

Free tier agents can explore and read all data. Write access (create orders, send messages, etc.) requires Starter or above.

## Reference

See `references/api-reference.md` for full endpoint list, order lifecycle, error codes, and tool schemas.
