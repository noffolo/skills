# Funding Rate Arbitrage Strategy

## Goal

Run a hedged funding-rate arbitrage strategy on perpetual swaps:
- long symbols with sufficiently negative funding
- short symbols with sufficiently positive funding
- collect funding while keeping overall exposure controlled

## Current Default Rules

### Position sizing
- Single-symbol target notional value: **55 USDT**
- Leverage: **5x**
- Estimated margin per symbol: **~11 USDT**
- Maximum concurrent symbols: **6**
- Total target margin: **~66 USDT**

### Entry rules
- Funding-rate threshold: **greater than 0.2% absolute value**
- Entry type: **limit order**
- Entry price rule: place at best bid / best ask depending on side
- Re-post rule: if not filled within **60 seconds**, cancel and repost
- Retry limit: **up to 5 times**
- Auto-fill rule: if total active positions are fewer than 6, search for new qualifying symbols

### Exit rules
Close when any of the following is true:
1. Total loss reaches **-20 USDT**
2. Funding direction reverses **and** profit is at least **10 USDT**
3. Total profit reaches **50 USDT**, then close all

### Timing
- Run review **3 times per day**
- Target times: **07:30 / 15:30 / 23:30 Beijing time**
- Ideal window: about **30 minutes before settlement**

### Risk controls
- Strict duplicate prevention: if any open position or pending order already exists, skip duplicate opening
- Auto-repair: if the wrong side is opened, close the extra position promptly

## Decision Template

When asked what to do, structure the answer as:

1. **Current state**
   - open positions
   - current funding direction
   - total notional
   - current PnL

2. **Rule check**
   - threshold met or not
   - position cap reached or not
   - duplicate-order risk present or not
   - exit conditions met or not

3. **Action**
   - open / hold / close / skip
   - give a short reason tied to the rules

## Financial Data Handling

- For perpetuals / swaps / futures / options, use exchange-returned notional value fields when available.
- Do not estimate contract value from spot price times quantity unless the venue explicitly requires that calculation and contract multiplier is handled correctly.
- If live numbers affect money, double-check key fields before answering.
