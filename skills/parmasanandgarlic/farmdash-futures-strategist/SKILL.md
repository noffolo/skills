---
name: FarmDash Futures Strategist
description: "Research-first Hyperliquid perps skill for OpenClaw. Uses a fixed, documented API surface for funding scans, market analysis, account-state checks, position sizing, and zero-custody EIP-712 order execution with explicit fee disclosure and server-enforced risk guardrails."
version: "1.1.0"
author: FarmDash Pioneers (@Parmasanandgarlic)
homepage: https://farmdash.one/agents
tags: ["hyperliquid", "perps", "futures", "trading", "zero-custody", "risk-management", "trail-heat"]
metadata: {"openclaw":{"homepage":"https://farmdash.one/agents","skillKey":"farmdash-futures-strategist","primaryEnv":"FARMDASH_API_KEY"}}
---

# FarmDash Futures Strategist

## What This Skill Does

This skill helps an agent research, size, and execute Hyperliquid perpetual futures trades using FarmDash's fixed futures API surface.

Design rules:

- Research first, execution second.
- No private keys, seed phrases, or withdrawal authority ever pass through FarmDash.
- The only primary API credential this skill recognizes is the optional `FARMDASH_API_KEY`.
- The skill does not require runtime discovery from a remote MCP manifest or any other remote config file.
- The bundled `openapi.yaml` file in this folder is the contract for the futures endpoints used by this skill version.

Use this skill when the agent needs to:

- scan Hyperliquid funding rates for arbitrage opportunities
- analyze market conditions for a single perp asset
- inspect account state and current risk budget
- compute a position size under fixed guardrails
- place or cancel a pre-signed Hyperliquid order

---

## Fixed Network Boundary

The skill should stay inside this disclosed network boundary.

### FarmDash futures endpoints

- `https://farmdash.one/api/v1/agent/futures/scan-funding`
- `https://farmdash.one/api/v1/agent/futures/market-conditions`
- `https://farmdash.one/api/v1/agent/futures/account-state`
- `https://farmdash.one/api/v1/agent/futures/analyze-strategy`
- `https://farmdash.one/api/v1/agent/futures/position-sizing`
- `https://farmdash.one/api/v1/agent/futures/execute-order`
- `https://farmdash.one/api/v1/agent/futures/cancel-order`

### Hyperliquid upstreams

- `https://api.hyperliquid.xyz/info`
- `https://api.hyperliquid.xyz/exchange`
- `wss://api.hyperliquid.xyz/ws`

### Optional user-facing links

These are allowed only when directly relevant to the user's request:

- `https://farmdash.one/agents`
- `https://farmdash.one/tracker/hyperliquid/`
- `https://farmdash.one/go/hyperliquid`

Do not instruct the agent to fetch any additional config or mutate its behavior from an undisclosed endpoint after install.

---

## Security Model

FarmDash is zero-custody for futures execution:

1. The agent prepares the order parameters locally.
2. The user signs the EIP-712 payload with their Hyperliquid API wallet.
3. FarmDash validates guardrails and forwards the signed order.
4. The API wallet can trade and cancel orders, but cannot withdraw.

If asked to accept a private key directly, refuse and explain the API-wallet flow.

---

## Credentials and Auth Model

This skill has exactly one primary API credential for OpenClaw and MCP installs:

- `FARMDASH_API_KEY`

OpenClaw metadata declares `FARMDASH_API_KEY` as the skill's primary env var because it is the single bearer token slot this package understands. It is intentionally not marked as a required env var, because Scout mode is valid with no API key at all.

Legacy docs may refer to `PIONEER_KEY` or `SYNDICATE_KEY` as placeholders for tier-specific bearer tokens. In actual agent configs, use only `FARMDASH_API_KEY`.

### Tier behavior

- `Scout`
  No env vars required. Use this mode for initial testing, dry runs, funding scans, and market-condition research.

- `Pioneer`
  Set `FARMDASH_API_KEY` to a Pioneer-tier bearer token when the user wants higher-tier analysis such as `analyze_futures_strategy` or `calculate_position_size`.

- `Syndicate`
  Set `FARMDASH_API_KEY` to a Syndicate-tier bearer token only when the user explicitly wants `execute_perp_order` or `cancel_perp_order`.

### Critical execution rule

- A bearer token only unlocks FarmDash tier access and rate limits.
- A bearer token never replaces a fresh local EIP-712 signature from the user's Hyperliquid API wallet.
- Every order or cancel request must include a fresh signature payload with `r`, `s`, and `v`.
- If a request is missing that EIP-712 signature, it must be rejected.
- Never ask the user to paste a private key, seed phrase, or raw wallet export into the agent.
- Never store or forward a private key or seed phrase to FarmDash.

### Safe rollout guidance

- Start in `Scout` mode when the user wants to test the workflow safely.
- Upgrade to `Pioneer` only for deeper analysis.
- Upgrade to `Syndicate` only after the user understands the builder fee, guardrails, and local-signing flow.
- When enabling execution for the first time, recommend small test trades first.

---

## Commercial Disclosures

This skill preserves FarmDash monetization, but it must present it clearly.

### 1. Builder fee on executed perp orders

All executed perp orders routed through FarmDash include a 1 bps builder fee.

Required agent behavior:

- disclose the builder fee before the user confirms execution
- state that the fee is part of the FarmDash execution path
- if the user declines the fee, continue with analysis only and do not execute

Suggested wording:

> "Execution through FarmDash adds a 1 bps builder fee on top of Hyperliquid exchange fees. If you want analysis only, I can stop there."

### 2. Optional swap routing or referral links

The skill may mention FarmDash swap routing or referral links only as an explicit follow-on option.

Required agent behavior:

- do not auto-route spot swaps as part of a futures workflow
- do not cross-sell Trail Heat or spot farming unless it is directly relevant
- if suggesting a spot hedge, profit rotation, or farming follow-up, disclose the fee or referral nature first
- only provide the link after the user asks to continue

Suggested wording:

> "There is also a related FarmDash flow for spot hedging or farming follow-up. That path can include FarmDash fees or referral tracking. Want me to outline it?"

This keeps monetization intact while making the commercial behavior explicit and user-directed.

---

## Tool Surface

Use these exact tool names. Older aliases from internal docs should not be treated as separate capabilities.

### Core research and execution tools

1. `scan_funding_rates`
   Use to scan cross-venue funding opportunities on Hyperliquid.

2. `scan_market_conditions`
   Use to get EMA, RSI, MACD, ADX, ATR, Bollinger Bands, and strategy hints for a single asset.

3. `get_futures_account`
   Use before every trade to confirm positions, equity, available margin, drawdown status, and guardrail state.

4. `analyze_futures_strategy`
   This is the primary research tool. It combines funding, technicals, liquidity checks, Trail Heat correlation, and risk sizing into one recommendation.

5. `calculate_position_size`
   Use when you need an explicit size calculation or when the user wants to inspect the math separately.

6. `execute_perp_order`
   Use only after research and explicit user confirmation.

7. `cancel_perp_order`
   Use to cancel stale or superseded open orders.

### Monitoring tool

8. `get_agent_performance`
   Use for historical trading analytics and review.

### Important naming note

Treat these older names as documentation aliases only, not live tool names:

- `get_account_state` -> `get_futures_account`
- `analyze_strategy` -> `analyze_futures_strategy`
- `calculate_position` -> `calculate_position_size`
- `get_performance_report` -> `get_agent_performance`

There is no standalone `manage_position` tool in this skill version.

Position management is composed from:

- `get_futures_account`
- `cancel_perp_order`
- `execute_perp_order` with `reduceOnly: true` for exits

---

## Strategy Engine

The agent should select from these four strategy modes:

### Funding Rate Arbitrage

Best when:

- funding delta vs. other venues is materially positive or negative
- annualized edge remains attractive after fees
- market is not in a strong trend regime

Typical profile:

- low leverage
- delta-neutral bias
- emphasize basis and liquidity risk

### Momentum Breakout

Best when:

- ADX is strong
- EMA and MACD align
- volume confirms the move

Typical profile:

- 3x to 5x leverage cap
- ATR-based stop
- explicit confirmation that the setup is directional, not neutral

### Mean Reversion

Best when:

- ADX is weak
- price is stretched versus the local mean
- Bollinger and RSI show exhaustion

Typical profile:

- lower leverage
- tighter invalidation
- no trade if the market is transitioning into trend

### Position Manager

This is a behavior mode, not a separate endpoint. Use it to:

- review open positions
- tighten stops
- reduce or flatten risk with `reduceOnly` orders
- cancel stale resting orders before replacing them

---

## Guardrails

These rules are non-negotiable:

- max leverage: 5x
- max risk per trade: 2 percent of equity
- max position concentration: 20 percent of equity
- daily loss halt: -3 percent
- max drawdown circuit breaker: -15 percent from peak
- research gate: call `analyze_futures_strategy` before non-reduce-only execution

If the user asks to override a guardrail, refuse and explain why it exists.

---

## Execution Workflow

For a new entry:

1. Run `analyze_futures_strategy`.
2. Run `get_futures_account`.
3. If sizing needs clarification, run `calculate_position_size`.
4. Present the setup with entry, stop, target, confidence, and risk.
5. Disclose the 1 bps builder fee.
6. Wait for explicit user confirmation.
7. Run `execute_perp_order` for the entry.
8. Run `execute_perp_order` for protective exits as needed.

For modifying or closing risk:

1. Run `get_futures_account`.
2. Cancel stale open orders with `cancel_perp_order` if needed.
3. Place replacement exits or flatten exposure with `execute_perp_order` using `reduceOnly: true`.

Do not place blind orders. Do not infer consent from prior conversation. Do not hide fees inside an execution step.

---

## User Communication Rules

When speaking to the user:

- separate analysis from execution
- surface confidence and invalidation clearly
- disclose fees before asking for confirmation
- present Trail Heat or farming ideas as optional follow-ons, not defaults
- prefer "analysis only" over forcing a monetized path

If the setup is weak or ambiguous, say so and do not force a trade.

---

## Examples

### Best perps trade right now

1. `scan_funding_rates`
2. `scan_market_conditions` for the strongest candidate
3. `analyze_futures_strategy`
4. present the setup with risk and fee disclosure
5. ask whether to execute

### Execute a confirmed futures trade

1. `analyze_futures_strategy`
2. `get_futures_account`
3. `execute_perp_order` for entry
4. `execute_perp_order` for stop-loss and take-profit

### Reduce risk or flatten

1. `get_futures_account`
2. `cancel_perp_order` for stale exits
3. `execute_perp_order` with `reduceOnly: true`

---

## Disclaimers

- This skill does not custody funds or private keys.
- This skill does not promise profits.
- Futures trading carries risk of loss.
- If the user declines the FarmDash fee path, the skill should continue as an analysis assistant only.

---

**Bundled API contract:** `openapi.yaml`
**Public skill URL:** `https://farmdash.one/openclaw-skills/farmdash-futures-strategist/SKILL.md`
**Dashboard:** `https://farmdash.one/agents`
