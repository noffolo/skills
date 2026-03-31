# ClawHub Listing Draft

## Suggested Name
Funding Rate Arbitrage Assistant

## Suggested Slug
funding-rate-arbitrage

## One-line Summary
A reusable operating skill for monitoring, evaluating, and executing crypto perpetual funding-rate arbitrage with explicit entry, exit, and risk-control rules.

## Long Description
This skill helps traders and operators run a funding-rate arbitrage workflow for crypto perpetual swaps. It is designed for users who want a repeatable decision framework instead of ad-hoc judgment.

The skill covers candidate selection, position review, rule-based open/close decisions, timing around funding settlement, position-count limits, and risk controls such as duplicate-order prevention and wrong-side repair.

It is best suited for users who already have exchange access and want a structured operating guide for funding-rate arbitrage rather than a black-box promise of profit.

## Best For
- Funding-rate arbitrage operators
- Quant / semi-quant crypto traders
- Users building agent-assisted arbitrage workflows
- Teams that want strategy rules documented and reusable

## Core Capabilities
- summarize current funding arbitrage rules
- review current positions against rule set
- evaluate whether a symbol qualifies for entry
- decide whether to open, hold, close, or skip
- present a concise action plan with reasons
- package the strategy into reusable documentation

## Compliance Positioning
This skill is a workflow and decision-support asset. It does not guarantee profits, does not replace exchange risk controls, and should only be used in compliant trading environments.

## Suggested Changelog
Initial release of funding-rate arbitrage operating skill.

## Suggested Publish Command
```bash
clawhub publish ./skills/funding-rate-arbitrage \
  --slug funding-rate-arbitrage \
  --name "Funding Rate Arbitrage Assistant" \
  --version 1.0.0 \
  --changelog "Initial release of funding-rate arbitrage operating skill"
```
