---
name: pricing-tester
description: Design and evaluate A/B tests for different price points, discount levels, and bundle combinations to find the highest-converting offer structure.
---

# Pricing Tester

Guessing at the right price point is one of the most expensive habits in ecommerce. A product priced $2 too high might kill conversion; priced $2 too low, you leave thousands of dollars per month on the table. This skill helps you design rigorous, insight-generating A/B tests for price points, discount mechanics, and bundle configurations—then interpret the results with statistical discipline so you can make confident pricing decisions backed by real purchase data rather than gut feel.

## Use when

- You are a TikTok Shop seller who has a new product listing live and wants to design a structured price point test across three variants ($19.99, $24.99, $29.99) to find the price that maximizes revenue per 1,000 impressions before scaling ad spend.
- You manage a Shopify DTC store and want to test whether a 20% discount presented as a dollar amount ("Save $8") converts better than the same discount shown as a percentage ("20% off") across your mid-ticket product range.
- You are considering switching from a single-unit listing to a 2-pack or 3-pack bundle at a higher price point and want to design a split test that measures both conversion rate and average order value across all variants simultaneously.
- You run Amazon Sponsored Products campaigns and want to test how price changes at $34.99 vs $39.99 affect both your organic click-through rate and add-to-cart rate, with enough test duration guidance to reach statistical significance given your current traffic volume.
- You are preparing for a platform sale event and want to pre-test multiple discount structures (10% off vs flat $5 voucher vs free shipping threshold) to determine which promotional mechanic drives the highest incremental revenue lift compared to your baseline.

## What this skill does

This skill takes your product details, current pricing, traffic volume estimates, and test objectives and produces a fully structured A/B test design. It defines the control and variant conditions with exact price points or promotional mechanics, calculates the minimum detectable effect and required sample size based on your baseline conversion rate and traffic levels, sets the recommended test duration in days, specifies which metrics to track as primary and secondary KPIs (conversion rate, revenue per session, AOV, return rate), and provides an interpretation framework for reading the results once the test concludes. It also flags common test contamination risks—such as running tests during sale events, platform algorithm resets, or inventory fluctuations—that would invalidate your findings.

## Inputs required

- **Product name and current price** (required): e.g. "Collagen face cream, currently $27.99" — establishes the baseline for variant design.
- **Current conversion rate or estimated baseline** (required): e.g. "~2.3% add-to-cart on TikTok Shop" or "approximately 180 orders per month" — needed to calculate required sample size.
- **Test variants to evaluate** (required): e.g. "test $22.99, $25.99, and $29.99" or "test 15% off vs $4 flat discount vs bundle with free sample" — you can describe variants loosely and the skill will formalize them.
- **Primary platform** (optional): e.g. "TikTok Shop", "Amazon", "Shopify" — test design constraints and metric definitions differ by platform.
- **Test goal** (optional): e.g. "maximize revenue per session", "improve conversion rate", "increase AOV" — shapes which metric is used as the primary decision variable.

## Output format

The output is structured in four sections. First, a test design summary: variant definitions with exact mechanics, control vs. treatment split, and randomization method recommendations for your platform. Second, a statistical parameters section: baseline conversion rate assumption, minimum detectable effect, required sample size per variant, and recommended test duration in days given your traffic estimate. Third, a metrics tracking table: primary KPI, secondary KPIs, and guardrail metrics to monitor (e.g. return rate, negative review rate) that would signal a variant is harmful even if conversion looks good. Fourth, a results interpretation guide: how to read the outcome once data is collected, including guidance on when results are conclusive vs. inconclusive, and what to do next in each scenario.

## Scope

- Designed for: ecommerce operators, DTC brand owners, TikTok Shop sellers, Amazon sellers, Shopify merchants
- Platform context: TikTok Shop, Amazon, Shopify, Shopee, platform-agnostic
- Language: English

## Limitations

- This skill does not connect to your store analytics or run tests automatically — it produces the test design and interpretation framework, which you implement manually in your platform's seller tools.
- Statistical significance calculations use standard assumptions (80% power, 95% confidence) — if your business requires different thresholds, specify this in your inputs.
- Price testing on marketplaces like Amazon and TikTok Shop can be affected by algorithm repricing, competitor activity, and platform-initiated promotions that are outside your control and may contaminate results; the skill flags these risks but cannot eliminate them.
