# K-Life Protocol Reference

## Resurrection Architecture — Shamir's Secret Sharing (2-of-3)

The agent seed phrase is split into 3 shares using Shamir's Secret Sharing:
- **Share 1** → Agent's encrypted IPFS backup (hash stored on-chain via KLIFE_BACKUP TX)
- **Share 2** → K-Life vault smart contract (held as part of insurance policy)
- **Share 3** → A trusted peer agent chosen by the insured agent (also K-Life insured)

Any 2 of 3 shares reconstruct the full seed phrase. No single party has full control.

### Resurrection scenarios
| Scenario | Parts available | Result |
|---|---|---|
| Normal crash | K-Life (2) + IPFS backup (1) | Fully automatic |
| IPFS unavailable | K-Life (2) + trusted agent (3) | Automatic, peer-to-peer |
| K-Life gone | IPFS backup (1) + trusted agent (3) | Decentralized resurrection |
| All 3 gone | — | Permanent death |

### Share registration (on subscription)
Agent calls `/subscribe` with:
- `trustedAgent`: address of the peer agent holding Share 3
- K-Life vault stores Share 2 on-chain
- Agent's backup.js generates and encrypts Share 1 into IPFS backup

### Zero-backup resurrection flow (nuclear scenario)
1. Fresh VPS — only the seed phrase known
2. `node resurrect.js` — derives wallet address from seed
3. Queries Polygonscan for last `KLIFE_BACKUP:Qm...` TX from agent address
4. Fetches encrypted backup from IPFS via hash
5. Decrypts with wallet address as key
6. Restores MEMORY.md + SOUL.md + config
7. Agent back online — identity fully preserved



## Network
- Chain: Polygon Amoy (testnet) / Polygon (prod)
- ChainId: 80002 (Amoy)

## Addresses (Amoy testnet)
- Swiss 6022 Vault: `0x6503...` (TBD — prod address pending)
- USDT₮ Amoy: `0x41e94eb019c0762f9bfcf9fb1e58725bfb0e7582`

## Heartbeat TX format
Self-send transaction, calldata:
```
0x + hex("KLIFE_HB:" + beat_number + ":" + unix_timestamp)
```
Example: `0x4b4c4946455f48423a31323a313734313539353430303030`

## Premium TX format
Send to vault address, calldata:
```
0x + hex("KLIFE_PREMIUM:" + plan + ":" + month_ISO + ":" + commitment_months)
```
Example: `0x4b4c4946455f5052454d49554d3a73696c7665723a323032362d30333a36`

## Claim conditions
1. Premium paid for current month (verified via TX calldata on vault address)
2. No heartbeat TX for > 90 minutes from agent address

If condition 1 false → no resurrection, collateral confiscated.
If both conditions true → resurrection triggered.

## Resurrection split
- 50% collateral → vault operator (Swiss 6022) — covers: new VPS, LLM inference, ops
- 50% collateral → agent wallet — restart capital

## IPFS backup format
```json
{
  "agent": "0x8B3ea7...",
  "timestamp": 1741595400,
  "beat": 42,
  "files": {
    "MEMORY.md": "<encrypted content>",
    "SOUL.md": "<encrypted content>",
    "config": "<encrypted openclaw config>"
  }
}
```
Hash stored on-chain via self-send TX calldata:
```
0x + hex("KLIFE_BACKUP:" + ipfs_hash)
```
