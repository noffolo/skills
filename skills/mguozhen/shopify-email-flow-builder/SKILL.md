---
name: shopify-email-flow-builder
description: "Klaviyo and Shopify Email automation flow designer. Builds complete email flow blueprints for abandoned cart, post-purchase, win-back, welcome series, and browse abandonment — with timing, subject lines, copy angles, segmentation logic, and A/B test ideas. Triggers: email flow, klaviyo flow, email automation, abandoned cart email, post purchase email, winback email, welcome series, email sequence, shopify email, email marketing automation, drip campaign, email funnel"
allowed-tools: Bash
metadata:
  openclaw:
    homepage: https://github.com/mguozhen/shopify-email-flow-builder
---

# Shopify Email Flow Builder

AI-powered email automation design agent — creates complete Klaviyo or Shopify Email flow blueprints with every email mapped out: timing, subject lines, copy angles, segmentation, and A/B test suggestions.

Describe your store, your product, or the flow you need. The agent builds the full sequence from trigger to exit, ready to hand to a copywriter or implement directly.

## Commands

```
build flow <type>                  # build a complete flow blueprint (e.g. build flow abandoned cart)
abandoned cart flow                # abandoned cart recovery sequence (3-email default)
post purchase flow                 # post-purchase onboarding and upsell sequence
winback flow                       # win-back lapsed customers sequence
welcome flow                       # welcome series for new subscribers
browse abandonment flow            # browse abandonment trigger sequence
flow audit                         # audit an existing flow for gaps and optimizations
email copy angle                   # generate subject line + copy angle options for a specific email
flow save <flow-name>              # save flow blueprint to workspace
```

## What Data to Provide

The agent works with:
- **Flow type** — "build abandoned cart flow for a skincare brand"
- **Store context** — product type, price point, brand voice, target customer
- **Existing setup** — "I have a 2-email abandoned cart but it's underperforming"
- **Performance data** — open rates, click rates, revenue per recipient if available
- **Platform** — Klaviyo, Shopify Email, Mailchimp, or other ESP

No API keys needed. No platform integration required.

## Workspace

Creates `~/email-flows/` containing:
- `memory.md` — saved store profiles, brand voice notes, past flows
- `flows/` — saved flow blueprints (markdown)
- `copy-angles.md` — library of subject lines and copy angles by flow type

## The 6 Core Flows

### Flow 1: Welcome Series
**Trigger**: New subscriber (email capture, not yet a customer)
**Goal**: Build relationship, establish brand, drive first purchase

| Email | Timing | Purpose |
|-------|--------|---------|
| Email 1 | Immediately | Welcome + deliver lead magnet (if any), brand story |
| Email 2 | Day 2 | Social proof — bestsellers, reviews, UGC |
| Email 3 | Day 4 | Education — how to use / why you'll love the product |
| Email 4 | Day 7 | Urgency offer — first-purchase discount or free shipping |
| Email 5 | Day 10 | Last chance — expiring offer or simple "did we lose you?" |

### Flow 2: Abandoned Cart
**Trigger**: Cart created, checkout not completed (1 hour minimum delay)
**Goal**: Recover the sale without over-discounting

| Email | Timing | Purpose |
|-------|--------|---------|
| Email 1 | 1 hour after abandonment | Reminder — "You left something behind", no discount |
| Email 2 | 24 hours after Email 1 | Objection handling — reviews, guarantee, FAQ |
| Email 3 | 48 hours after Email 2 | Incentive — offer discount only if previous emails failed |

**Segmentation split**: suppress Email 3 discount for VIP customers (they convert without it).

### Flow 3: Post-Purchase
**Trigger**: Order placed (first purchase)
**Goal**: Confirm, delight, cross-sell, generate reviews

| Email | Timing | Purpose |
|-------|--------|---------|
| Email 1 | Immediately | Order confirmation + what to expect (shipping timeline) |
| Email 2 | Day 3 | Product education — how to get the most from purchase |
| Email 3 | Day 7 (or at delivery) | Check-in — "Did it arrive? How are you liking it?" |
| Email 4 | Day 14 | Review request (post-usage, not at delivery) |
| Email 5 | Day 21 | Cross-sell / complementary product recommendation |
| Email 6 | Day 45 | Replenishment prompt (for consumable products only) |

### Flow 4: Win-Back (Lapsed Customer)
**Trigger**: X days since last purchase (typically 90–180 days, adjust by product purchase cycle)
**Goal**: Re-engage before customer churns permanently

| Email | Timing | Purpose |
|-------|--------|---------|
| Email 1 | Day 0 (trigger) | "We miss you" — no offer, just re-engagement |
| Email 2 | Day 7 | What's new — new products, improvements, social proof |
| Email 3 | Day 14 | Win-back offer — discount or bonus |
| Email 4 | Day 21 | Final attempt — "Is this goodbye?" (sunset path begins) |

**Sunset**: if no engagement after Email 4, move to suppression list or low-frequency list.

### Flow 5: Browse Abandonment
**Trigger**: Viewed product page, did NOT add to cart (session ended)
**Goal**: Return visitor to the product while interest is warm

| Email | Timing | Purpose |
|-------|--------|---------|
| Email 1 | 4–6 hours after browse | Product spotlight — features, benefits, reviews |
| Email 2 | 48 hours after Email 1 | Social proof focus — reviews, UGC, bestseller badge |

**Note**: only trigger if subscriber, not an existing customer in an active abandoned cart flow.

### Flow 6: VIP / High-Value Customer
**Trigger**: Customer reaches spend threshold (e.g., 3+ orders or $500+ LTV)
**Goal**: Reward loyalty, prevent churn, increase AOV

| Email | Timing | Purpose |
|-------|--------|---------|
| Email 1 | At threshold | VIP welcome — exclusive status, thank you |
| Email 2 | Monthly | Early access to new products / sales |
| Email 3 | Birthday or anniversary | Personal recognition + exclusive offer |

## Subject Line Formulas

| Formula | Example |
|---------|---------|
| Curiosity gap | "This is why your [product] isn't working" |
| Direct benefit | "Get [outcome] in [timeframe]" |
| Social proof | "[X] customers swear by this" |
| Urgency | "Last chance — [offer] ends tonight" |
| Personalization | "[First name], you left something behind" |
| Question | "Did something go wrong?" |
| Number list | "3 things you didn't know about [product]" |

## Segmentation Logic

Key segments to build in Klaviyo:
- **Engaged subscribers**: opened email in last 90 days
- **Unengaged subscribers**: no opens in 90–180 days (reduce send frequency, sunset after 180)
- **First-time buyers**: 1 order placed
- **Repeat buyers**: 2+ orders (exclude heavy discounters)
- **VIP**: top 10% by LTV or order count threshold
- **Discount buyers**: purchased only during sales (suppress from non-sale flows, protect margin)

## A/B Test Suggestions by Flow

| Flow | Test Idea |
|------|-----------|
| Abandoned cart Email 1 | Timing: 30 min vs. 1 hour delay |
| Abandoned cart Email 3 | Discount type: % off vs. $ off vs. free shipping |
| Welcome Email 1 | With vs. without founder video/story |
| Post-purchase Email 4 | Review request timing: Day 7 vs. Day 14 |
| Win-back Email 1 | Emotional tone vs. product-led subject line |

## Output Format

Every flow blueprint outputs:
1. **Flow Overview** — trigger, goal, total emails, estimated duration
2. **Email-by-Email Blueprint** — for each email: timing, subject line (3 options), preview text, copy angle, CTA, segmentation notes
3. **Flow Logic Map** — trigger conditions, exit conditions, branch logic (e.g., "if purchased, exit flow")
4. **Segmentation Rules** — who enters, who is excluded, branch splits
5. **A/B Test Recommendations** — 2–3 specific tests to run first
6. **Performance Benchmarks** — expected open rate, click rate, revenue per recipient by flow type

## Benchmarks

| Flow | Avg Open Rate | Avg Revenue/Recipient |
|------|--------------|----------------------|
| Welcome | 40–60% | $3–8 |
| Abandoned Cart | 35–50% | $5–15 |
| Post-Purchase | 50–70% | $2–6 |
| Win-Back | 10–20% | $1–4 |
| Browse Abandon | 25–40% | $2–8 |

## Rules

1. Always ask for product type and price point before designing flows — a $15 impulse product needs different timing than a $300 considered purchase
2. Never add a discount to abandoned cart Email 1 — train customers to wait for the offer; use reminder tone first
3. Suppress existing customers from welcome flows and new subscribers from win-back flows — overlap causes brand confusion
4. Flag when a store is on Shopify Email vs. Klaviyo — Klaviyo supports conditional splits and predictive analytics; Shopify Email does not
5. Recommend sunset logic for every win-back flow — unengaged subscribers hurt deliverability
6. Keep subject lines under 50 characters for mobile optimization (label when testing longer variants)
7. Save flow blueprints to `~/email-flows/flows/` when flow save command is used
