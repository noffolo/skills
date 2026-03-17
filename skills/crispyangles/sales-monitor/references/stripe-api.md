# Stripe API Quick Reference

## Authentication
All requests use HTTP Basic Auth with secret key as username:
```
-u "sk_live_xxx:" (note trailing colon)
```

## Key Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| /v1/charges | GET | List payments |
| /v1/products | GET/POST | Manage products |
| /v1/prices | GET/POST | Manage prices |
| /v1/payment_links | GET/POST | Payment links |
| /v1/customers | GET | List customers |
| /v1/refunds | POST | Issue refund |
| /v1/balance | GET | Account balance |

## Common Filters
- `?limit=10` — results per page (max 100)
- `?created[gte]=1678000000` — filter by Unix timestamp
- `?starting_after=ch_xxx` — pagination cursor

## Webhook Events (for real-time monitoring)
- `charge.succeeded` — payment completed
- `charge.refunded` — refund issued
- `customer.created` — new customer
- `payment_link.completed` — payment link purchase
