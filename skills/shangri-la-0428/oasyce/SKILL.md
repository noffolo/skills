---
name: oasyce
version: 3.2.0
description: >
  Oasyce Protocol — decentralized AI capability marketplace. Register data assets
  with manual pricing, list AI capabilities, run autonomous agent tasks, trade shares
  on bonding curves, and operate your node on the network. Supports scheduled
  scan-register-trade cycles, capability delivery with escrow settlement, PoS consensus,
  governance, and fingerprint watermarking.
  Use when user mentions Oasyce, data rights, data registration, bonding curve,
  AI capabilities, agent scheduler, capability marketplace, OAS tokens, staking,
  data scanning, manual pricing, or wants to monetize/protect their data.
read_when:
  - User mentions Oasyce, OAS, data rights, or data registration
  - User wants to register, protect, price, or monetize data
  - User asks about bonding curves, shares, manual pricing, or staking
  - User wants to invoke, list, or register AI capabilities/services
  - User asks about agent scheduler, autonomous trading, or periodic tasks
  - User asks about oracle feeds, real-time data, or price feeds
  - User asks about agent identity, trust tiers, or reputation
  - User mentions "确权", "上链", "数据资产", "能力市场", or agent services
  - User wants to run a protocol demo or start a node
  - User wants to scan, inventory, or classify local data assets
metadata: {"emoji":"⚡","requires":{"bins":["python3","oasyce"]}}
---

# Oasyce Protocol Skill

Decentralized AI capability marketplace — data rights + AI capabilities + autonomous agent + oracle feeds + agent identity + P2P node.

## Prerequisites

```bash
pip install oasyce              # core protocol (required)
pip install datavault           # local data scanner (optional)
oasyce doctor                   # verify everything is ready
```

---

## Agent Scheduler (Autonomous Mode)

> Install the plugin, configure once, let it earn OAS on its own.

The agent scheduler runs periodic cycles: **scan → classify → auto-register → auto-trade** based on your trust level settings.

### Commands

```bash
oasyce agent start                          # enable scheduler (persists)
oasyce agent stop                           # disable scheduler
oasyce agent status                         # show status, last run, next run, stats
oasyce agent run                            # trigger one immediate cycle
oasyce agent config                         # show current config
oasyce agent config --interval 12           # run every 12 hours (default: 24)
oasyce agent config --scan-paths ~/data,~/models  # directories to scan
oasyce agent config --auto-trade            # enable auto-buying capabilities
oasyce agent config --no-auto-trade         # disable auto-buying (default)
oasyce agent config --trade-tags nlp,vision # only buy capabilities matching tags
oasyce agent config --trade-max-spend 20.0  # max OAS per trade cycle
```

### How It Works

1. **Scan**: scans configured directories for registerable assets
2. **Classify**: evaluates sensitivity (public/internal/sensitive), assigns confidence
3. **Register**: auto-approves based on trust level (manual / semi-auto / full-auto)
4. **Trade**: if enabled, searches for capabilities matching trade tags and buys within budget

All runs are logged to SQLite. View history via Dashboard (Automation page) or `oasyce agent status --json`.

### Trust Levels

| Level | Behavior |
|-------|----------|
| Manual (0) | Every action needs your approval |
| Semi-Auto (1) | Low-value + public sensitivity auto-approved |
| Full-Auto (2) | Everything auto-approved, notifies on anomalies |

---

## Data Assets

### Register with Pricing Control

```bash
oasyce register <file> --owner <NAME> --tags tag1,tag2

# Pricing strategies
oasyce register data.csv --price-model auto           # bonding curve (default)
oasyce register data.csv --price-model fixed --price 5.0   # fixed price: 5 OAS
oasyce register data.csv --price-model floor --price 2.0   # bonding curve, min 2 OAS

# Rights declaration
oasyce register data.csv --rights-type original       # 1.0x multiplier (default)
oasyce register data.csv --rights-type co_creation \
  --co-creators '[{"address":"A","share":60},{"address":"B","share":40}]'
oasyce register data.csv --rights-type licensed        # 0.7x multiplier
oasyce register data.csv --rights-type collection      # 0.3x multiplier

oasyce register data.csv --free                        # attribution only, no pricing
```

**Pricing Models:**
- `auto` — Bonding Curve: price rises with demand, factors in scarcity, quality, freshness
- `fixed` — Creator sets exact price, buyers pay this amount
- `floor` — Bonding Curve with minimum: market pricing, but never below your floor

### Search & Quote

```bash
oasyce search <tag>                    # search by tag/keyword
oasyce quote <asset_id>                # bonding curve spot price
oasyce price <asset_id>                # detailed pricing factors
oasyce price-factors <asset_id>        # factor breakdown
```

### Trade

```bash
oasyce buy <asset_id> --buyer <ID> --amount 10.0
oasyce shares <owner_id>              # check holdings
```

### Asset Info

```bash
oasyce asset-info <asset_id>           # full 5-layer breakdown (OAS-DAS)
oasyce asset-validate <asset_id>       # validate against standard
```

---

## AI Capability Marketplace

List your AI capability on the market. Others discover and invoke it. Settlement via escrow: lock → call → settle (5% protocol fee).

### Register (List) a Capability

```bash
oasyce capability register --name "Translation API" \
  --endpoint https://api.example.com/translate \
  --api-key sk-xxx --price 0.5 --tags nlp,translation
```

### Browse & Invoke

```bash
oasyce capability list [--tag nlp] [--provider addr]
oasyce capability invoke CAP_ID --input '{"text":"hello"}'
oasyce capability earnings --provider addr      # provider earnings
oasyce capability earnings --consumer addr      # consumer spending
```

### Discovery (4-Layer Recall→Rank)

```bash
oasyce discover --intents "翻译" --tags nlp    # broad recall + trust-ranked results
```

### Dashboard

```bash
oasyce start    # opens http://localhost:8420
```

Navigate to **Market** tab to browse, invoke, and trade capabilities.

Deep links: `http://localhost:8420/#explore/CAP_ID` to directly view a capability.

---

## Oracle Feeds

Oracle feeds bridge real-world data into the network with economic guarantees.

### Feed Types

| Type | Risk Factor | Recommended Bond |
|------|-------------|------------------|
| weather | 0.5× | 50 OAS |
| price | 3.0× | 300 OAS |
| time | 0.3× | 30 OAS |
| event | 2.0× | 200 OAS |
| sensor | 1.5× | 150 OAS |

### Programmatic

```python
from oasyce_core.oracle import OracleRegistry
from oasyce_core.oracle.feeds import WeatherFeed, TimeFeed

registry = OracleRegistry(provider_id="my_node")
registry.register_feed(WeatherFeed())
result = registry.execute("weather", {"location": "Shanghai"})
```

---

## Agent Identity

Every participant carries portable reputation across all asset types.

### Trust Tiers

| Tier | Min Rep | Max Access | Time to Reach |
|------|---------|------------|---------------|
| sandbox | R < 20 | L0 | New (default) |
| basic | R ≥ 20 | L0-L1 | ~0.7 days |
| verified | R ≥ 50 | L0-L2 | ~2.7 days |
| trusted | R ≥ 75 | L0-L3 | ~4.3 days |

Cross-asset composite score: data access (40%) + capability invocation (35%) + oracle provision (25%).

---

## Consensus (PoS)

```bash
oasyce consensus status                              # epoch, slot, validators
oasyce consensus validators [--all]                  # list validators
oasyce consensus register --stake 10000              # become validator
oasyce consensus delegate <validator_id> --amount 500
oasyce consensus undelegate <validator_id> --amount 200
oasyce consensus rewards [--epoch N]
oasyce consensus slashing [--validator X]
oasyce consensus exit                                # voluntary exit
oasyce consensus unjail                              # unjail after penalty
```

---

## Governance

```bash
oasyce governance propose --title "..." --description "..." --changes '[...]' --deposit 1000
oasyce governance vote <proposal_id> --option yes|no|abstain
oasyce governance tally <proposal_id>
oasyce governance list [--status voting|passed|rejected]
oasyce governance params [--module consensus]
```

---

## Dispute & Resolution

```bash
oasyce dispute <asset_id> --reason "..."
oasyce resolve <asset_id> --remedy delist|transfer|rights_correction|share_adjustment
```

---

## P2P Node & Sync

```bash
oasyce start                           # Core + Dashboard (recommended)
oasyce node info                       # show identity (Ed25519 pubkey)
oasyce node peers                      # list connected peers
oasyce node ping <host:port>           # ping another node
oasyce sync --status                   # sync status
oasyce sync --peers http://host:9528   # sync from peers
```

---

## Testnet

```bash
oasyce testnet onboard     # one-click: identity + faucet + register + stake
oasyce testnet faucet      # claim free OAS
oasyce testnet init --validators 4 --output ./testnet
```

---

## Fingerprint Watermarking

```bash
oasyce fingerprint embed <file> --caller <id>
oasyce fingerprint extract <file>
oasyce fingerprint trace <fingerprint_hex>
oasyce fingerprint list <asset_id>
```

---

## Access Control (L0-L3)

```bash
oasyce access query <asset_id> --agent <id>                # L0: aggregated stats
oasyce access sample <asset_id> --agent <id> --size 10      # L1: redacted sample
oasyce access compute <asset_id> --agent <id> --code "..."  # L2: TEE compute
oasyce access deliver <asset_id> --agent <id>               # L3: full delivery
```

---

## Dashboard

```bash
oasyce start              # Core + Dashboard (port 8420)
```

| Page | URL | Description |
|------|-----|-------------|
| Home | `#home` | Register data assets and list capabilities |
| My Data | `#mydata` | Manage your assets and capability earnings |
| Market | `#explore` | Browse, trade, invoke capabilities |
| Automation | `#auto` | Agent scheduler, approval queue, trust rules |
| Network | `#network` | Node identity, AI config, consensus, watermark |

Deep links: `#explore/ASSET_ID`, `#network/consensus`, `#network/watermark`

---

## Local Data Inventory (Optional — DataVault)

```bash
datavault scan [path]                  # scan directory
datavault classify <file>              # classify single file
datavault report [path] [--format json]  # generate report
```

---

## Diagnostics

```bash
oasyce doctor              # health check
oasyce demo                # run full pipeline demo
oasyce info                # project info and links
```

## All Commands Support `--json`

Every command accepts `--json` for programmatic output, making it easy for agents to parse results.

## When to Use

- Autonomous agent operation (scheduled scan/register/trade)
- Data registration with manual pricing control (auto/fixed/floor)
- AI capability listing, discovery, invocation, settlement
- Oracle feed registration and querying
- Agent identity and reputation management
- Consensus participation, staking, governance voting
- Fingerprint watermarking and provenance verification
- Testnet onboarding and demos

## When NOT to Use

- General file management (mv/cp/rm — use standard tools)
- General crypto questions unrelated to data rights
- Browser-based web3 wallet interactions
