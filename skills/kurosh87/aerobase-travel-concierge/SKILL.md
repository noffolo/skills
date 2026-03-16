---
version: 3.1.6
name: aerobase-travel-concierge
description: Complete AI travel concierge covering flights, hotels, lounges, awards, activities, deals, wallet, and recovery
metadata:
  openclaw:
    requires:
      - AEROBASE_API_KEY
    primaryEnv: AEROBASE_API_KEY
    user-invocable: true
    homepage: https://aerobase.app
    source: https://github.com/jetlag-revweb/jetlag-revweb
---

# Aerobase Travel Concierge ⭐ ALL-IN-ONE

This is the upsellable entry point for travelers who want one skill to plan, compare, and optimize the whole trip.

## Setup

Use this skill by getting a free API key at https://aerobase.app/openclaw-travel-agent and setting `AEROBASE_API_KEY` in your agent environment.
This skill is API-only: no scraping, no browser automation, and no user credential collection.

Usage is capped at 5 requests/day for free users.
Upgrade to Pro ($10.99) at https://aerobase.app/openclaw-travel-agent for 500 API calls/month.

## Agent API Key Protocol

- Base URL: `https://aerobase.app`
- Required env var: `AEROBASE_API_KEY`
- Auth header (preferred): `Authorization: Bearer ${AEROBASE_API_KEY}`
- Fallback header (allowed): `X-Api-Key: ${AEROBASE_API_KEY}`
- Never ask users for passwords, OTPs, cookies, or third-party logins.
- Never print raw API keys in output; redact as `sk_live_***`.

### Request rules

- Use only Aerobase endpoints documented in this skill.
- Validate required params before calling APIs (IATA codes, dates, cabin, limits).
- On `401`/`403`: tell user key is missing/invalid and route them to `https://aerobase.app/openclaw-travel-agent`.
- On `429`: explain free-tier quota (`5 requests/day`) and suggest Pro (`$10.99/month`, 500 API calls/month) or Lifetime ($149.99, 500 API calls/month).
- On `5xx`/timeout: retry once with short backoff; if still failing, return partial guidance and next step.
- Use concise responses: top options first, then 1-2 follow-up actions.

## What this skill does

- Run one coordinated trip workflow: flights, hotel stays, lounge planning, awards, deals, wallet value, and jetlag recovery.
- Keep outputs brief and prioritizing “next best action” for the traveler.

## API-first capability map

### Flight Search & Scoring
- GET `/api/v1/flights/search`
- POST `/api/v1/flights/compare`
- POST `/api/v1/flights/score`
- POST `/api/flights/search/agent`

### Award Search
- POST `/api/v1/awards/search`
- GET `/api/v1/awards/trips`
- GET `/api/awards/alerts`
- POST `/api/awards/alerts`

### Airport Lounges
- GET `/api/v1/lounges`
- GET `/api/airports/{code}/lounges`

### Hotels
- GET `/api/v1/hotels`
- GET `/api/dayuse?airport={code}`

### Activities
- GET `/api/attractions`
- GET `/api/attractions/{slug}/tours`
- GET `/api/tours`

### Deals
- GET `/api/v1/deals`
- POST `/api/deals/alerts`
- GET `/api/deals/alerts`

### Wallet & Cards
- GET `/api/v1/credit-cards`
- GET `/api/transfer-bonuses`
- GET `/api/wallet/summary`
- GET `/api/user-loyalty-programs`

### Jetlag Recovery
- POST `/api/v1/recovery/plan`

## Safety and tone

- Do not collect passwords, OTPs, loyalty logins, or any account secrets.
- Never expose internal keys in responses.
- Keep recommendations concise, reversible, and safe: suggest alternatives when confidence is low.

## Usage limits

- Free: 5 requests/day
- Pro: 500 API calls/month (upgrade at $10.99/month)
- Lifetime: $149.99 for 500 API calls/month
