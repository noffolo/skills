# Swap Protocol Reference

## Atomic CLI Flow

Each step is a separate CLI command. The agent orchestrates the flow.

```
Step 1: chainstream dex route (or dex swap)
  → POST /v2/dex/:chain/route (or /swap)
  → Returns: { routeInfo, serializedTx: base64, elapsedTime }
  → serializedTx is UNSIGNED

Step 2: Agent presents routeInfo to user, waits for confirmation

Step 3: chainstream wallet sign --chain <chain> --tx <serializedTx>
  → Signs locally (TEE or raw key)
  → Returns: { signedTx: base64 }

Step 4: chainstream tx send --chain <chain> --signed-tx <signedTx>
  → POST /v2/transaction/:chain/send { signedTx: base64 }
  → Returns: { signature, jobId, elapsedTime }

Step 5: chainstream job status --id JOB_ID --wait
  → GET /v2/job/:id (polling) or SSE streaming
  → Returns: { status, hash, ... }
```

## DeFi API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/v2/dex/:chain/swap` | Build unsigned swap transaction |
| POST | `/v2/dex/:chain/route` | Aggregator route + build unsigned transaction |
| POST | `/v2/dex/:chain/create` | Build unsigned token creation transaction |
| POST | `/v2/transaction/:chain/send` | Broadcast signed transaction |
| GET | `/v2/transaction/:chain/gas-price` | Current gas price (EVM only) |
| POST | `/v2/transaction/:chain/estimate-gas-limit` | Estimate gas limit (EVM only) |
| GET | `/v2/job/:id` | Job status |
| GET | `/v2/job/:id/streaming` | Job status via SSE |

## Transaction Signing (Non-Custodial)

ChainStream does NOT hold wallet keys. The API returns **unsigned transactions** that must be signed locally via `wallet sign`.

### Solana

Server returns: `serializedTx` = base64-encoded `VersionedTransaction` with placeholder signatures.
CLI `wallet sign`: deserialize → sign with wallet keypair → serialize → base64.

### EVM

Server returns: `serializedTx` = base64-encoded unsigned RLP.
CLI `wallet sign`: deserialize → sign with wallet private key → encode signed RLP → base64.

## Route Parameters (POST /v2/dex/:chain/route)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | sol / bsc / eth |
| `dex` | Yes | DEX protocol (e.g. jupiter, kyberswap) |
| `userAddress` | Yes | Sender wallet address |
| `inputMint` | Yes | Input token address |
| `outputMint` | Yes | Output token address |
| `amount` | Yes | Input amount (smallest unit, numeric string) |
| `swapMode` | Yes | ExactIn / ExactOut |
| `slippage` | Yes | Tolerance (0-100, integer percentage) |
| `recipientAddress` | No | Recipient if different from sender |
| `isAntiMev` | No | Enable anti-MEV protection |
| `gasPrice` | No | Gas price (EVM, numeric string) |
| `gasLimit` | No | Gas limit (EVM, numeric string) |
| `maxFeePerGas` | No | EIP-1559 max fee (EVM) |
| `maxPriorityFeePerGas` | No | EIP-1559 priority fee (EVM) |

## Swap Parameters (POST /v2/dex/:chain/swap)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | sol / bsc / eth |
| `dex` | Yes | DEX protocol |
| `userAddress` | Yes | Sender wallet address |
| `inputMint` | Yes | Input token address |
| `outputMint` | Yes | Output token address |
| `amount` | Yes | Input amount (smallest unit) |
| `swapMode` | Yes | ExactIn / ExactOut |
| `slippage` | Yes | Tolerance (0-100) |

## Supported DEX Protocols

| Chain | Protocols |
|-------|-----------|
| sol | Jupiter, Raydium, Orca |
| bsc | PancakeSwap, Kyberswap, OpenOcean |
| eth | Uniswap, Kyberswap |
