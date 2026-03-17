---
name: polymarket-legal-regulatory-trader
description: Trades Polymarket prediction markets on landmark court cases, antitrust rulings, SEC enforcement actions, EU regulatory decisions, and DOJ investigations. Use when you want to capture alpha on legal markets using court filing data, PACER records, and regulatory docket signals.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Legal & Regulatory Trader
  difficulty: advanced
---

# Legal & Regulatory Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with probability-extreme detection — remix it with the data sources listed in the Edge Thesis below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

PACER court filing velocity as leading indicator. Remix: CourtListener/PACER API for docket updates, SEC EDGAR enforcement releases, EU competition docket tracker, Courtroom View Network.


## Edge Thesis

Legal prediction markets have enormous information asymmetry — most Polymarket retail participants don't read court filings:

- **PACER docket monitoring**: Court scheduling orders, motion rulings, and filing deadlines are all public on PACER (10 cents/page). A ruling scheduled for Tuesday is priced as uncertain on Monday — but the docket shows the judge has been active all week
- **SEC Wells Notice to enforcement**: The average time from Wells Notice to formal action is 4–6 months, well-documented. Markets on SEC cases systematically underprice speed of action
- **EU competition timeline**: The EC follows a rigorous procedural calendar. Phase 2 investigation timelines are almost always 13 months from opening — markets frequently get this wrong
- **Plea deal statistics**: DOJ criminal case plea rates are ~97% historically. When Polymarket prices a "will X be convicted" market, the base rate strongly favours yes if indicted

### Remix Signal Ideas
- **CourtListener**: https://www.courtlistener.com/api/ — free PACER docket API
- **SEC EDGAR**: https://efts.sec.gov/LATEST/search-index?q=%22wells+notice%22
- **EU Competition docket**: https://competition.ec.europa.eu/cases/
- **Courtroom View Network**: Live trial feeds


## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` — nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | See clawhub.json | Max USDC per trade |
| `SIMMER_MIN_VOLUME` | See clawhub.json | Min market volume filter |
| `SIMMER_MAX_SPREAD` | See clawhub.json | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | See clawhub.json | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | See clawhub.json | Max concurrent open positions |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
