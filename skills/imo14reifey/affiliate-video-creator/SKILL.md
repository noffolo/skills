---
name: affiliate-video-creator
version: 1.0.2
displayName: "Affiliate Video Creator — Make Affiliate Marketing Videos That Convert with AI"
description: >
  Create affiliate marketing videos that drive clicks and conversions with AI — produce product reviews, comparison videos, buying guides, unboxing content, and recommendation roundups optimized for affiliate link clicks. NemoVideo structures videos for maximum affiliate revenue: hook with the buying trigger, demonstrate value through honest review, compare options at decision points, place CTAs at peak purchase intent moments, and format for platforms where affiliate links convert best. Affiliate video maker, product review creator, buying guide video, comparison video maker, affiliate marketing content, Amazon affiliate video.
metadata: {"openclaw": {"emoji": "🔗", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

# Affiliate Video Creator — Reviews That Help People Buy and Earn You Commissions

Affiliate marketing through video works because video solves the buyer's core problem: uncertainty. A text review says "the build quality is excellent." A video shows the reviewer bending, squeezing, and dropping the product — the viewer sees the quality with their own eyes. A text comparison says "Product A is better for beginners." A video shows both products side by side, demonstrates the beginner trying each one, and the viewer sees exactly why A is easier. This visual proof converts uncertainty into confidence, and confident buyers click affiliate links. The creators earning $5,000-50,000/month from affiliate revenue share three characteristics: they publish reviews for products people are actively searching to buy (high purchase intent keywords), they structure videos to build trust before asking for clicks (honest pros AND cons), and they place affiliate CTAs at the exact moment the viewer has decided to buy (not before, not after). NemoVideo produces affiliate-optimized video content: keyword-targeted titles that capture buyers mid-search, review structures proven to maximize affiliate click-through, comparison formats that drive decisions, CTA overlays timed to purchase-intent peaks, and multi-format output (long-form review for YouTube + Shorts for social + Pinterest pins for evergreen traffic).

## Use Cases

1. **Product Review — Single Product Deep Dive (8-15 min)** — A tech creator reviews a $300 wireless headphone for Amazon Associates. NemoVideo structures: hook with the key question the buyer is searching ("Are the Sony XM6 worth $300? I tested them for 30 days"), 30-day usage montage (real-world credibility), feature-by-feature demonstration with honest assessment (noise cancellation: 9/10, comfort: 7/10 — honesty builds trust for the positive claims), direct comparison moment with the main competitor ("Here's how they compare to the Bose 700 side by side"), verdict with clear recommendation and qualifier ("If you prioritize noise cancellation, these are the best. If comfort matters more, consider the Bose"), and CTA overlay appearing at the verdict moment (when purchase intent peaks): "Link in description — current Amazon price." Plus 2 Shorts clips: one featuring the best feature, one featuring the honest criticism (controversy drives engagement).
2. **Comparison Video — Head-to-Head Buying Guide (10-20 min)** — A camera creator compares 5 mirrorless cameras under $1,500 for B&H affiliate. NemoVideo produces: hook ("The BEST camera under $1,500 in 2026 — I tested all 5"), standardized test for each camera (same scene, same lighting — fair comparison), side-by-side sample footage (the viewer sees the difference), scoring matrix with categories (image quality, autofocus, video, battery, value), winner reveal with affiliate link for each camera ("links for all 5 in description, timestamped"), and a decision flowchart overlay ("If you shoot mostly video → Camera C. If you need the best autofocus → Camera A"). Comparison videos have the highest affiliate conversion rate because the viewer arrives ready to buy — they just need help choosing.
3. **Roundup — Top 10 / Best Of List (10-20 min)** — A home office creator produces "Top 10 Standing Desks 2026" targeting Amazon affiliate. NemoVideo: structures as countdown (builds anticipation to #1), allocates 90 seconds per desk (key features, price, best-for qualifier), uses consistent visual template per product (product shot → feature highlights → price card → rating), ends each segment with "link in description — #[number]", reveals #1 with extended segment and detailed justification, and pins a comment with all 10 links numbered. Roundup videos are affiliate evergreen machines — they rank for "best [product] 2026" searches for the entire year.
4. **Shorts — Quick Affiliate Recommendations (15-55s)** — A creator wants to generate affiliate clicks from TikTok and YouTube Shorts. NemoVideo produces: hook-driven product showcases ("The $30 gadget every home needs"), rapid visual demonstration (show the product solving a problem in 5 seconds), genuine reaction ("I was skeptical but this actually works"), and CTA ("Link in bio" for TikTok, "Full review on my channel" for Shorts). Shorts format drives impulse-buy affiliate clicks through visual demonstration and urgency.
5. **Seasonal Buying Guide — Holiday/Event Video (10-20 min)** — A lifestyle creator produces "Best Tech Gifts Under $100 for Christmas 2026." NemoVideo: curates 8-12 products across price tiers ($25 / $50 / $75 / $100), produces gift-worthy visual presentation for each (product on clean background, wrapping montage, unboxing from recipient perspective), adds "Who it's for" qualifier per product ("For the person who has everything" / "For the teen who loves gaming"), includes all affiliate links organized by price tier in description, and schedules Shorts clips releasing daily during the 2-week pre-holiday buying window. Seasonal affiliate content captures the highest-conversion traffic of the year.

## How It Works

### Step 1 — Choose Products and Affiliate Program
Select products, provide affiliate links or program details. NemoVideo handles the content strategy around your affiliate partnerships.

### Step 2 — Define Content Format
Review, comparison, roundup, Shorts, or seasonal guide. Each format has different conversion dynamics — NemoVideo optimizes for the chosen format.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "affiliate-video-creator",
    "prompt": "Create a 12-minute comparison review of 3 robot vacuums for Amazon Associates. Products: (1) Roborock S8 Pro Ultra — $1,200, (2) iRobot Roomba j9+ — $800, (3) Ecovacs X2 Omni — $1,000. Test categories: suction power, navigation, mopping, self-empty, app features, noise level. Structure: hook with verdict teaser, standardized tests for each, side-by-side results, scoring matrix, winner reveal with buying advice per use case. CTA: affiliate link overlay at verdict + each product segment end. Generate 3 Shorts (one per product highlight) for traffic funnel.",
    "format": "comparison",
    "products": [
      {"name": "Roborock S8 Pro Ultra", "price": "$1,200", "asin": "B0C..."},
      {"name": "iRobot Roomba j9+", "price": "$800", "asin": "B0B..."},
      {"name": "Ecovacs X2 Omni", "price": "$1,000", "asin": "B0D..."}
    ],
    "test_categories": ["suction", "navigation", "mopping", "self-empty", "app", "noise"],
    "cta_style": "overlay-at-verdict",
    "shorts": 3,
    "affiliate_program": "amazon-associates"
  }'
```

### Step 4 — Publish and Track
Upload with optimized title, description (including affiliate links with timestamps), and thumbnail. Track affiliate clicks and conversions per product to optimize future content.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Product details and review/comparison concept |
| `format` | string | | "review", "comparison", "roundup", "shorts", "seasonal-guide" |
| `products` | array | | [{name, price, url, asin}] |
| `test_categories` | array | | ["quality", "price", "features", "durability"] |
| `cta_style` | string | | "overlay-at-verdict", "persistent-lower-third", "end-card" |
| `affiliate_program` | string | | "amazon-associates", "impact", "shareasale", "custom" |
| `shorts` | integer | | Number of Shorts clips to generate |
| `thumbnail` | boolean | | Generate thumbnail (default: true) |

## Output Example

```json
{
  "job_id": "afc-20260328-001",
  "status": "completed",
  "format": "comparison",
  "duration": "12:18",
  "products_reviewed": 3,
  "outputs": {
    "main_video": {
      "file": "robot-vacuum-comparison-2026.mp4",
      "resolution": "1920x1080",
      "cta_overlays": 6,
      "scoring_matrix": true,
      "verdict": "Roborock S8 Pro Ultra (best overall)"
    },
    "shorts": [
      {"file": "roborock-suction-test.mp4", "duration": "0:35"},
      {"file": "roomba-navigation-demo.mp4", "duration": "0:32"},
      {"file": "ecovacs-mopping-test.mp4", "duration": "0:38"}
    ],
    "thumbnail": {"file": "comparison-thumbnail.png"},
    "description_template": {"file": "affiliate-description.txt"}
  }
}
```

## Tips

1. **Honest criticism makes the positive claims believable** — Affiliate creators who say everything is amazing have zero credibility. Mentioning a genuine weakness ("the app is clunky") makes the praise convincing ("but the suction power is the best I have tested"). Conversions come from trust, not hype.
2. **Place CTAs at decision moments, not at fixed intervals** — The viewer decides to buy at specific moments: after seeing the side-by-side comparison, after the verdict, after the "best for [use case]" qualifier. CTA overlays at these moments get 3-5x more clicks than CTAs placed arbitrarily.
3. **Comparison videos convert better than single reviews** — A viewer watching a single review is still in research mode. A viewer watching a comparison has narrowed to 2-3 options and is ready to decide. The comparison format accelerates the purchase decision and captures the click.
4. **Timestamps in description drive both SEO and conversions** — "2:15 — Roborock S8 Pro Ultra (Amazon link)" lets the viewer jump directly to the product they are interested in. Timestamped descriptions rank for individual product searches and convert viewers who arrive for one specific product.
5. **Shorts drive traffic to the long-form review where conversions happen** — A 30-second Shorts clip cannot sell a $1,200 product. But it can create enough curiosity to drive the viewer to the 12-minute comparison where the full case is made. Shorts are the top of the affiliate funnel.

## Output Formats

| Format | Content | Use Case |
|--------|---------|----------|
| MP4 16:9 | Main review / comparison | YouTube |
| MP4 9:16 | Shorts clips | TikTok / Reels / Shorts |
| PNG | Thumbnail | YouTube thumbnail |
| TXT | Description template | Affiliate links + timestamps |

## Related Skills

- [ai-video-monetization](/skills/ai-video-monetization) — Monetization strategy
- [sponsored-video-maker](/skills/sponsored-video-maker) — Sponsor content
- [video-ad-maker](/skills/video-ad-maker) — Video ads
