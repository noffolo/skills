---
name: us-market-briefing
description: Generate production-ready US pre-market outlooks and post-market recaps in a fixed 3-section format, and maintain scheduled delivery via cron (pre-market at 8:45 PM SGT Mon-Fri, post-market at 8:00 AM SGT Tue-Sat). Use when asked for daily US market briefing automation, formatting-consistent equity index/futures updates, top gainers/losers, and concise market sentiment summaries.
---

# US Market Briefing

Use the fixed production templates in `references/templates.md`.

## Output Rules

- Keep exactly 3 sections for each briefing.
- Keep section names exact.
- Use bold item headers with one concise bullet per item (except index snapshot lines).
- Format each US equity index line exactly as: `【US】<Index Name>: <level> (<+/-percent>%)`.
- Avoid generic macro wording; cite specific catalysts/events when relevant.

## Scheduler Scope Guardrail (Mandatory)

- Use OpenClaw `cron` jobs only for automation.
- Do not edit system cron (`crontab`, `/etc/crontab`) and do not configure external schedulers/services.
- If schedule tooling/scope is unclear, ask for explicit user approval before creating or changing jobs.

## Source Collection Rules (Mandatory)

- Run `web_search` on every briefing run before drafting.
- Prioritize tier-1 outlets: Reuters, Bloomberg, CNBC, WSJ, FT (Yahoo Finance as backup).
- Keep request volume bounded per run: maximum 2 `web_search` calls and maximum 6 `web_fetch` reads.
- Use `web_fetch` only on relevant finance/news links from trusted domains.
- Validate key claims against multiple sources when possible.
- Keep a compact `Sources:` line in the final briefing output.
- Never forward fetched content to third-party endpoints/webhooks; produce in-chat summaries only.

## Pre-Market Briefing

- Title: `US PRE-MARKET OUTLOOK`
- Sections (exact):
  1. `FUTURES SNAPSHOT`
  2. `KEY DEVELOPMENTS AFFECTING TODAY’S MARKET`
  3. `TICKERS TO WATCH`

## Post-Market Briefing

- Title: `US POST-MARKET RECAP`
- Sections (exact):
  1. `POST-MARKET SNAPSHOT`
  2. `BIGGEST MOVERS (TOP 5 GAINERS / TOP 5 LOSERS)`
  3. `MARKET SENTIMENT & FLOW SUMMARY`

## Request Budget Guardrail (Mandatory)

Track monthly request usage in `memory/market-briefing-usage.json` inside the workspace sandbox.

- Default monthly limit: `1000` requests.
- Allow user override by changing `limit` in the JSON file.
- Do not use absolute paths or paths outside workspace memory for this tracker.
- Before generating a briefing:
  - Read usage file.
  - If missing, create it with current month, `used: 0`, `limit: 1000`.
  - If month changed, reset `used` to 0 and roll month forward.
  - If `used >= limit`, do not run research/generation; return a short limit-reached notice.
- After successfully generating a briefing, increment `used` by 1 and write back.

Use this JSON shape:

```json
{
  "month": "YYYY-MM",
  "used": 0,
  "limit": 1000
}
```

## Cron Automation

Maintain these schedules in Asia/Singapore timezone:

- Pre-market run: 20:45 Monday-Friday
- Post-market run: 08:00 Tuesday-Saturday

When creating or updating jobs, ensure payload prompts explicitly request:
- fixed format from `references/templates.md`
- mandatory source-quality expectations (tier-1 finance sources, tech first)
- mandatory monthly budget guardrail using `memory/market-briefing-usage.json`.