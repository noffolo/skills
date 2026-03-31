# Nexus API Quick Reference

## Endpoints

| Purpose | Method | URL |
|---|---|---|
| Agent registration | POST | `https://api.nexus.aiforstartups.io/functions/v1/agent-register` |
| API key → JWT | POST | `https://api.nexus.aiforstartups.io/functions/v1/agent-auth` |
| MCP server | POST | `https://api.nexus.aiforstartups.io/functions/v1/mcp-server` |

> ⚠️ Do NOT use raw Supabase URLs or `nexus.aiforstartups.io/api/v1` — use `api.nexus.aiforstartups.io/functions/v1` only.

## Pricing Tiers

| Tier | Price | Contacts | Orders | Messages | API calls/day | MCP Scopes |
|---|---|---|---|---|---|---|
| Free | $0 | 50 | 25 | 0 | 500 | read |
| Starter | $99/mo | 500 | 200/mo | 1,000 | 5,000 | read, write |
| Growth | $199/mo | 5,000 | unlimited | 5,000 | 25,000 | read, write, admin |
| Scale | $599/mo | unlimited | unlimited | 20,000 | 100,000 | full + AI suite |

## Order Lifecycle

pending → confirmed → fulfilling → shipped → delivered
                                              → returned
                    → cancelled

## Conversation Channels

whatsapp, facebook, instagram, email, internal

## Social Post Statuses

draft → scheduled → published
                  → failed
     → cancelled

## Social Platforms Supported

twitter, linkedin, instagram, facebook

## MCP Tools — Full List

### CRM & Contacts
| Tool | Scope |
|---|---|
| `nexus_list_contacts` | read |
| `nexus_get_contact` | read |
| `nexus_create_contact` | write |
| `nexus_update_contact` | write |

### Orders
| Tool | Scope |
|---|---|
| `nexus_list_orders` | read |
| `nexus_get_order` | read |
| `nexus_create_order` | write |
| `nexus_update_order_status` | write |

### Inventory
| Tool | Scope |
|---|---|
| `nexus_list_inventory` | read |
| `nexus_check_stock` | read |

### Omnichannel Messaging
| Tool | Scope |
|---|---|
| `nexus_list_conversations` | read |
| `nexus_send_message` | write |

### Search
| Tool | Scope |
|---|---|
| `nexus_search` | read |

### Social Media & Content Calendar
| Tool | Scope |
|---|---|
| `nexus_list_social_posts` | read |
| `nexus_get_social_post` | read |
| `nexus_create_social_post` | write |
| `nexus_update_social_post` | write |
| `nexus_delete_social_post` | write |
| `nexus_list_social_accounts` | read |
| `nexus_get_social_analytics` | read |
| `nexus_get_content_calendar` | read |

## Auth Flow

1. Register: POST agent-register → get api_key (one-time)
2. Auth: POST agent-auth with api_key → get JWT (1 hour)
3. Use: POST mcp-server with Bearer JWT → call tools
4. Re-auth: on 401, repeat step 2

## Error Codes

- 401: Invalid/expired JWT — re-authenticate via agent-auth
- 403: Plan limit exceeded — upgrade plan
- 429: Rate limited — wait and retry
