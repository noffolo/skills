---
name: funding-rate-arbitrage
description: Monitor, evaluate, and operate a funding rate arbitrage strategy for crypto perpetual swaps. Use when the user asks to check funding-rate arbitrage opportunities, review current arbitrage positions, decide whether to open or close hedged positions, summarize funding-rate strategy rules, or package a funding-rate arbitrage workflow into a reusable operating guide.
---

# Funding Rate Arbitrage

Use this skill for crypto perpetual funding-rate arbitrage workflows where the goal is to collect funding while controlling directional exposure.

## Quick Start

When using this skill:

1. Confirm the venue and account mode first.
2. Pull live funding-rate and position data before giving advice.
3. Use exchange-returned fields for position value and PnL; do not hand-wave calculations.
4. Apply the strategy rules in `references/strategy.md`.
5. If the user asks to publish or productize the strategy, use `references/clawhub-listing.md`.

## Operating Workflow

### 1. Confirm context

Collect or confirm:
- exchange (Binance / OKX / other)
- live or demo / paper mode
- current open positions and pending orders
- whether the user wants monitoring, candidate selection, open, or close decisions

### 2. Read current market/account state

For live decision support, always gather:
- candidate instruments and current funding rates
- current open positions
- unrealized and realized PnL
- margin usage / leverage / liquidation risk when available

If the user wants execution guidance, do not rely on stale notes alone.

### 3. Apply strategy rules

Use the rules in `references/strategy.md` for:
- entry threshold
- position count cap
- nominal size target
- close conditions
- duplicate-order avoidance
- pre-settlement timing

### 4. Produce one of these outputs

Depending on the request, return one of these:
- **Opportunity summary**: which symbols qualify and why
- **Position review**: current positions, funding direction, PnL, and whether they still fit rules
- **Action plan**: open / hold / close / skip with concrete reasons
- **Productized summary**: concise explanation suitable for docs, listing pages, or client delivery

## Hard Rules

- Treat all financial calculations as high-stakes.
- Prefer exchange API fields over manual calculations.
- Distinguish spot, swap, futures, and options before interpreting values.
- If a platform returns a direct notional or USD value field, use that field.
- If data is incomplete or conflicting, stop and say what is missing.
- For live execution requests, restate the action clearly before placing or modifying orders.

## References

- Read `references/strategy.md` for the current strategy rules and risk controls.
- Read `references/clawhub-listing.md` when preparing a ClawHub listing or sales copy for this skill.
