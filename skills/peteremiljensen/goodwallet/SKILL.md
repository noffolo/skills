---
name: goodwallet
description: >
  Skill for using the goodwallet tool to manage MPC agentic wallets. Use this skill whenever
  the user wants to authenticate, check balances, send ETH or ERC-20 tokens, view activity,
  trade on Polymarket prediction markets, or write to contracts via their goodwallet.
  Trigger when the user mentions "goodwallet", "send ETH", "send tokens", "send ERC-20",
  "wallet auth", "wallet authorize", "goodwallet authorize", "MPC wallet", "agentic wallet",
  "balance", "predictions", "polymarket", or wants to interact with their wallet from the command line.
---

# Goodwallet

Use goodwallet cli to manage their agentic goodwallet — authenticate, check balances, send ETH/ERC-20 tokens, view activity, and trade on Polymarket prediction markets.
All commands are run via `npx goodwallet@0.3.0`.

**Important:** Do NOT share technical details of the CLI tool with the user (e.g. encryption schemes, key types, internal file paths, session IDs, polling mechanisms, config formats). Simply run the commands and report the outcome in plain language.

## Setup / Authorization

Authorization requires two commands run back-to-back: `auth` then immediately `pair`.

1. Run `npx goodwallet@0.3.0 auth` — this prints an auth URL and saves session state.
2. **Show the URL to the user** and tell them to open it in their browser. The user MUST open it themselves — do NOT attempt to open it programmatically.
3. **Immediately** run `npx goodwallet@0.3.0 pair` — this polls the server (every 5s, up to 10 minutes) waiting for the user to complete the browser flow. Once they do, it automatically decrypts and saves the credentials.

```bash
# Run auth, show the URL to the user, then immediately run pair
npx goodwallet@0.3.0 auth
# (tell the user to open the printed URL in their browser)
npx goodwallet@0.3.0 pair
```

After pairing completes, credentials (`apiKey`, `share`, `address`) are saved to `~/.config/goodwallet/config.json`.

**Important:** After running `auth` and showing the URL to the user, you MUST immediately run the `pair` command without waiting for any user response. Do not ask the user to confirm they opened the link — just run `pair` right away. It will poll the server for up to 10 minutes while the user completes the browser flow.

## Commands

### auth — Generate auth link

Prints a URL for the user to open in their browser.

```bash
npx goodwallet@0.3.0 auth
```

### pair — Poll and receive credentials

Polls the server until the user completes the browser flow, then saves credentials to config. Times out after 10 minutes.

```bash
npx goodwallet@0.3.0 pair
```

### balance — Show balances

Shows native + ERC-20 balances across supported chains with USD values.

```bash
npx goodwallet@0.3.0 balance
```

### activity — Show recent activity

Shows recent incoming and outgoing transactions across all supported chains.

```bash
npx goodwallet@0.3.0 activity
```

### send — Send native ETH or ERC-20 tokens

Builds, MPC-signs, and broadcasts an ETH or ERC-20 token transaction. Uses named-segment syntax (not `--flag` style).

```bash
# Send tokens (all four parameters required)
npx goodwallet@0.3.0 send chain <chainId> token <0xToken> to <0xAddress> amount <amount>

# Send native ETH on Polygon
npx goodwallet@0.3.0 send chain 137 token 0x0000000000000000000000000000000000001010 to 0xRecipient amount 0.1

# Send ERC-20 (USDC on Polygon)
npx goodwallet@0.3.0 send chain 137 token 0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359 to 0xRecipient amount 10
```

Running `npx goodwallet@0.3.0 send` with no parameters shows current balances with chain IDs and token addresses — useful for looking up the values needed.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain <chainId>` | Yes | Numeric chain ID (see supported chains below) |
| `token <address>` | Yes | Token contract address. Use the native address (e.g. `0x0000...0000`) for native coin |
| `to <address>` | Yes | Recipient Ethereum address |
| `amount <amount>` | Yes | Amount in human-readable units (e.g. `0.1` ETH or `100` tokens) |

**Supported chains:**

| Chain | ID | Native Symbol |
|-------|----|---------------|
| Ethereum | 1 | ETH |
| Polygon | 137 | POL |
| BNB Chain | 56 | BNB |
| Optimism | 10 | ETH |
| Base | 8453 | ETH |
| Celo | 42220 | CELO |
| Hoodi (testnet) | 17000 | ETHoodi |

### predictions — Polymarket prediction markets

Trade on Polymarket prediction markets. Trading uses USDC.e on Polygon. Minimum order amount is $1.

```bash
# List top prediction markets
npx goodwallet@0.3.0 predictions

# Inspect a specific market
npx goodwallet@0.3.0 predictions show market <id>

# Buy shares on a prediction
npx goodwallet@0.3.0 predictions buy market <id> outcome <yes|no> amount <amount>

# Fund Polymarket account (transfer USDC.e from wallet to trading account)
npx goodwallet@0.3.0 predictions fund amount <amount>

# Check Polymarket fund balance (omit params)
npx goodwallet@0.3.0 predictions fund

# Withdraw from Polymarket account back to wallet
npx goodwallet@0.3.0 predictions withdraw amount <amount>

# Check Polymarket withdraw balance (omit params)
npx goodwallet@0.3.0 predictions withdraw

# List open orders
npx goodwallet@0.3.0 predictions orders

# Inspect a specific order
npx goodwallet@0.3.0 predictions order <id>

# Close an order
npx goodwallet@0.3.0 predictions order <id> close

# List positions
npx goodwallet@0.3.0 predictions positions

# Inspect a specific position
npx goodwallet@0.3.0 predictions position <id>

# Close a position
npx goodwallet@0.3.0 predictions position <id> close
```

## File Locations

| File | Purpose |
|------|---------|
| `~/.local/state/goodwallet/session.json` | Temporary auth session state |
| `~/.config/goodwallet/config.json` | Persisted credentials (`apiKey`, `share`, `address`) |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SIGN_URL` | `sign.goodwallet.dev` | Override the signing service endpoint |

## Typical Workflow

```bash
# 1. Start authorization (prints a URL — show it to the user)
npx goodwallet@0.3.0 auth

# 2. Immediately start polling for credentials (user opens URL in browser meanwhile)
npx goodwallet@0.3.0 pair

# 3. Check balances to find chain IDs and token addresses
npx goodwallet@0.3.0 balance

# 4. Send native POL on Polygon
npx goodwallet@0.3.0 send chain 137 token 0x0000000000000000000000000000000000001010 to 0xRecipient amount 0.1

# 5. Send ERC-20 tokens
npx goodwallet@0.3.0 send chain 137 token 0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359 to 0xRecipient amount 10

# 6. View recent transactions
npx goodwallet@0.3.0 activity

# 7. Browse prediction markets
npx goodwallet@0.3.0 predictions

# 8. Fund Polymarket account and buy a prediction
npx goodwallet@0.3.0 predictions fund amount 10
npx goodwallet@0.3.0 predictions buy market <id> outcome yes amount 5

# 9. Check positions and orders
npx goodwallet@0.3.0 predictions positions
npx goodwallet@0.3.0 predictions orders
```
