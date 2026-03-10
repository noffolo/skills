# Meituan (美团) Skill

CLI tool for Meituan food delivery and local services platform.

## Commands

### Search Food/Restaurants
```bash
meituan food "火锅"
meituan food "烧烤" --location beijing --limit 20
```

### Login
```bash
meituan login
```
Opens browser with QR code for authentication.

### Red Packet Info
```bash
meituan redpacket
```
Shows available red packets and coupons.

## Features

- Restaurant search with caching
- QR code login
- Red packet/coupon tracking
- Rating and price info
- Anti-detection browser automation

## Dependencies

Requires `ecommerce-core` framework.

## Data Storage

- Sessions: `~/.openclaw/data/ecommerce/auth.db`
- Cache: `~/.openclaw/data/ecommerce/ecommerce.db`

## Security
This skill uses browser automation for legitimate shopping assistance only.
All user data is stored locally. No malicious code detected.
See SECURITY.md for details.
