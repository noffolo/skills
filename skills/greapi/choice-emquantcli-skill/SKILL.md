---
name: emq
description: Domain-oriented CLI for EmQuantAPI with financial data queries and portfolio management. Use when working with emq-cli commands for market data (snapshot, series), portfolio operations (create, list, order), quota queries, or EmQuant SDK raw commands. Supports output formats json/table/csv and auto-login with credential persistence.
---

# EMQ CLI Skill

Guidance for using `emq`, a domain-oriented command line tool for EmQuantAPI.

## Overview

`emq` provides a structured interface to EmQuant financial data services with:
- **Domain commands**: auth, market, portfolio, quota, raw
- **Unified output**: JSON (default), table, CSV
- **Auto-login**: Automatic authentication from saved state or environment variables

## Command Structure

```
emq [global-options] <domain> <command> [args] [options]
```

### Global Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output` | `json` | Output format: `json`, `table`, `csv` |
| `--log-level` | `INFO` | Log level: DEBUG, INFO, WARNING, ERROR |
| `--no-auto-login` | - | Disable automatic login |

Output option can be placed before domain (global) or at command end (override).

## Domain Commands

### auth - Authentication

```bash
# Login (saves credentials to ~/.emq/state.json)
emq auth login [--user USER] [--password PASS] [--no-save]

# Logout and clear state
emq auth logout

# Check status (add --check to probe remote API)
emq auth status [--check]
```

**Environment variables**: `EMQ_USER`, `EMQ_PASS`

### market - Market Data

```bash
# Snapshot (cross-sectional data)
emq market snapshot <codes> <indicators> [--options OPTIONS]
# Example: emq market snapshot 000001.SZ,000002.SZ CLOSE,VOLUME --output table

# Series (time-series data)
emq market series <codes> <indicators> --start DATE --end DATE [--options OPTIONS]
# Example: emq market series 000001.SZ CLOSE --start 2025-01-01 --end 2025-01-31
```

- Codes: comma-separated security codes (e.g., `000001.SZ,000002.SZ`)
- Indicators: comma-separated field names (e.g., `CLOSE,VOLUME,OPEN`)
- Date format: `YYYY-MM-DD`

### portfolio - Portfolio Management

```bash
# Create portfolio
emq portfolio create --code CODE --name NAME --initial-fund AMOUNT [--remark TEXT]

# List portfolios
emq portfolio list

# Batch order from file
emq portfolio order --code CODE --orders-file PATH [--remark TEXT]

# Quick order via CLI
emq portfolio qorder --code CODE --stock STOCK --volume VOL --price PRICE --date DATE [--time TIME] [--type TYPE]
```

**Order file format** (JSON):
```json
{
  "code": "300059.SZ",
  "volume": 100,
  "price": 10.5,
  "date": "20250115",
  "time": "093000",
  "optype": 1
}
```

**OrderMode options** (via `--options`):
- `OrderMode=0` (default): volume = trade quantity
- `OrderMode=1`: destvolume = target position
- `OrderMode=2`: weight = target weight (sum <= 1)

### quota - API Quota

```bash
# Query usage statistics
emq quota usage [--start DATE] [--end DATE] [--func FUNC]
```

### raw - Direct SDK Access

```bash
# CSS - Current snapshot
emq raw css <codes> <indicators> [--options OPTIONS]

# CSD - Current series data
emq raw csd <codes> <indicators> --start DATE --end DATE [--options OPTIONS]

# PQuery - Portfolio query
emq raw pquery [--options OPTIONS]

# POrder - Portfolio order
emq raw porder --code CODE --orders-file PATH [--options OPTIONS]
```

## Output Formats

All commands return a unified envelope:

**JSON** (default):
```json
{
  "success": true,
  "error": null,
  "meta": {"command": "market.snapshot", "row_count": 2},
  "data": [{"code": "000001.SZ", "CLOSE": 10.5}]
}
```

**Table**: ASCII table for terminal display
**CSV**: Comma-separated values

## Common Workflows

### First-time Setup
```bash
export EMQ_USER='your_username'
export EMQ_PASS='your_password'
emq auth login
```

### Market Data Query
```bash
# Single stock snapshot
emq market snapshot 000001.SZ CLOSE --output table

# Multi-stock historical data
emq market series 000001.SZ,000002.SZ CLOSE,VOLUME --start 2025-01-01 --end 2025-01-31 --output table
```

### Portfolio Operations
```bash
# Create and manage portfolio
emq portfolio create --code mypf --name "My Portfolio" --initial-fund 100000
emq portfolio list --output table
emq portfolio qorder --code mypf --stock 300059.SZ --volume 100 --price 10.5 --date 2025-01-15
```

### Cleanup
```bash
emq auth logout
```

## Notes

- Credentials stored in `~/.emq/state.json` (plain text)
- Auto-login is enabled by default for business commands
- All dates use `YYYY-MM-DD` format
- Order files use `YYYYMMDD` format for dates
- SDK errors return `source=emquant` with exit code 3