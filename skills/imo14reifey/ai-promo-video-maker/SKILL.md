---
name: ai-promo-video-maker
version: 1.0.1
displayName: "AI Promo Video Maker — Create Promotional Videos for Products Events and Launches"
description: >
  Create promotional videos with AI — produce product launch promos, event teasers, sale announcements, seasonal campaigns, grand opening videos, and special offer content. NemoVideo generates complete promo videos from a brief: attention-grabbing visuals, urgency-driven messaging, countdown timers, offer displays, platform-optimized formatting, and multi-variant output for A/B testing. The promo video that turns announcements into action. Promo video maker, promotional video creator, sale video maker, event promo video, launch video creator, announcement video, marketing promo generator.
metadata: {"openclaw": {"emoji": "🎉", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

# AI Promo Video Maker — Announcements That Drive Immediate Action

A promotional video has one job: make the viewer act now. Not tomorrow, not "I'll think about it," not bookmarked and forgotten. Now. Every element — visual, audio, textual — serves urgency. The opening grabs attention (0.5 seconds to stop the scroll). The body communicates value (what, why, how much). The close creates urgency (limited time, limited quantity, exclusive access). The CTA removes friction (one tap, one click, one step). This formula is simple. Executing it at scale is hard. Every sale needs a promo video. Every product launch needs a teaser. Every event needs an announcement. Every seasonal campaign needs fresh creative. A retail business runs 20-30 promotions per year. A SaaS company launches 4-8 features. An event organizer promotes 12-50 events. Each promotion needs 3-5 video variants for different platforms and audience segments. That is 60-250 promo videos per year. At $200-1,000 per video through traditional production, annual promo video costs reach $12,000-250,000. NemoVideo produces promo videos from a brief: describe the promotion, define the urgency, and receive complete video assets with multiple variants, multiple formats, and multiple platform exports.

## Use Cases

1. **Product Launch — Teaser + Reveal Campaign (multiple videos)** — A tech brand launches a new product in 2 weeks. NemoVideo produces a 3-phase campaign: Phase 1 — Teaser (7 days before): 15-second mysterious visual with "Something is coming" text, countdown timer, brand colors only, no product shown (builds anticipation). Phase 2 — Reveal (launch day): 30-second product reveal with slow-mo unveiling, key features as animated overlays, price announcement with animated counter, and "Available now" CTA. Phase 3 — Social proof (3 days post-launch): 20-second video with early customer reactions, sales counter ("5,000 sold in 24 hours"), and urgency ("selling fast — get yours"). Three phases, multiple variants per phase, complete launch campaign.

2. **Sale Event — Flash Sale / Black Friday (15-30s)** — A retail brand runs a 48-hour flash sale. NemoVideo creates: countdown-driven opening (animated clock, "48 HOURS ONLY"), product showcase carousel (top 5 deals cycling with original price → sale price animations), percentage-off visuals (large bold "50% OFF" with animated strike-through on original prices), urgency elements (diminishing stock animation, countdown timer persistent in corner), and CTA ("Shop now — sale ends midnight"). Plus 5 product-specific variants (one per deal) for targeted ads. The flash sale creative package that drives revenue spikes.

3. **Event Promotion — Conference/Concert/Webinar (30-60s)** — A tech conference needs to drive registrations. NemoVideo produces: event highlight reel from previous year's photos/videos (social proof that it is worth attending), speaker lineup showcase (photo + name + company for each speaker, animated carousel), agenda teaser (3-4 highlighted sessions with topic and time), venue/location preview, early bird pricing with countdown ("Early bird ends in 5 days — save $200"), and registration CTA. Plus a 15-second countdown version for social stories and a 6-second bumper for YouTube pre-roll.

4. **Seasonal Campaign — Holiday/Back-to-School/Summer (multiple)** — A brand needs seasonal promo content for 4 major shopping periods. NemoVideo batch-produces: themed visual templates per season (holiday: red/green/gold with snow particles; summer: bright/warm with sun rays; back-to-school: energetic/colorful with notebook textures; spring: fresh/light with floral accents), product showcases adapted to seasonal context, seasonal discount animations, and themed CTAs. Four campaigns × 5 variants each × 3 formats = 60 promo assets for the entire year.

5. **Local Business — Grand Opening / Special Offer (15-30s)** — A new restaurant opens and needs to drive foot traffic. NemoVideo creates: food showcase montage (sizzling, plating, satisfied customers — the visuals that trigger hunger), grand opening announcement with date/location (map animation showing the location), opening special offer ("Free appetizer with any entree — opening week only"), atmosphere preview (interior design, ambiance, staff welcoming), and Google Maps link CTA. The local promo video that fills tables on opening week.

## How It Works

### Step 1 — Describe the Promotion
What is being promoted (product, event, sale, offer), the value proposition, the urgency mechanism, and the target audience.

### Step 2 — Set Campaign Parameters
Duration, visual style, urgency elements, platform targets, and number of variants.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "ai-promo-video-maker",
    "prompt": "Create promo videos for a 72-hour flash sale on an online course platform. Main offer: all courses 70%% off. Top 3 courses to feature: Python for Beginners ($99 → $29.70), Digital Marketing Masterclass ($149 → $44.70), Data Science Bootcamp ($199 → $59.70). Urgency: 72-hour countdown timer. Social proof: 50,000+ students enrolled. Style: high-energy, bold typography, bright colors. Generate: 1 main 30-second promo + 3 course-specific 15-second variants + 1 compilation 45-second version. All formats: 16:9, 9:16, 1:1.",
    "promo_type": "flash-sale",
    "duration_main": 30,
    "urgency": {"type": "countdown", "hours": 72},
    "products": [
      {"name": "Python for Beginners", "original": "$99", "sale": "$29.70"},
      {"name": "Digital Marketing Masterclass", "original": "$149", "sale": "$44.70"},
      {"name": "Data Science Bootcamp", "original": "$199", "sale": "$59.70"}
    ],
    "social_proof": "50,000+ students",
    "style": "high-energy-bold",
    "variants": ["main-30s", "python-15s", "marketing-15s", "data-15s", "compilation-45s"],
    "formats": ["16:9", "9:16", "1:1"]
  }'
```

### Step 4 — Launch Campaign
Upload variants to ad platforms, schedule social posts, embed on landing page, and send in email campaign. Track performance per variant.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Promotion description and campaign brief |
| `promo_type` | string | | "product-launch", "flash-sale", "event", "seasonal", "grand-opening", "offer" |
| `urgency` | object | | {type: "countdown"/"limited-stock"/"exclusive", hours/units} |
| `products` | array | | [{name, original_price, sale_price, image}] |
| `social_proof` | string | | "50,000+ customers" or similar |
| `style` | string | | "high-energy-bold", "elegant-minimal", "playful", "corporate" |
| `variants` | array | | List of variant specifications |
| `formats` | array | | ["16:9", "9:16", "1:1", "4:5"] |
| `music` | string | | "energetic", "dramatic", "upbeat", "elegant" |
| `brand_colors` | array | | Hex codes |
| `campaign_phases` | array | | [{phase, timing, content}] for multi-phase campaigns |

## Output Example

```json
{
  "job_id": "apvm-20260328-001",
  "status": "completed",
  "promo_type": "flash-sale",
  "variants_produced": 5,
  "formats_per_variant": 3,
  "total_files": 15,
  "outputs": {
    "main_30s": {"files": ["main-16x9.mp4", "main-9x16.mp4", "main-1x1.mp4"], "duration": "0:30"},
    "python_15s": {"files": ["python-16x9.mp4", "python-9x16.mp4", "python-1x1.mp4"], "duration": "0:15"},
    "marketing_15s": {"files": ["marketing-16x9.mp4", "marketing-9x16.mp4", "marketing-1x1.mp4"], "duration": "0:15"},
    "data_15s": {"files": ["data-16x9.mp4", "data-9x16.mp4", "data-1x1.mp4"], "duration": "0:15"},
    "compilation_45s": {"files": ["compilation-16x9.mp4", "compilation-9x16.mp4", "compilation-1x1.mp4"], "duration": "0:45"}
  }
}
```

## Tips

1. **Urgency must be real and visible** — A countdown timer that the viewer can see ticking creates genuine urgency. Vague urgency ("limited time!") is ignored. Specific urgency ("ends in 47 hours") drives action.
2. **Price animations are more persuasive than static prices** — Watching the original price get struck through while the sale price appears with a satisfying animation creates a visceral sense of savings. The motion communicates "deal" faster than text.
3. **Multiple variants test messaging angles, not just visuals** — A flash sale promo led by "70% off" tests the discount angle. The same sale led by "Learn Python for $29" tests the value angle. Different audiences respond to different framings.
4. **Multi-phase campaigns build anticipation** — A single "sale now" video has one chance. A teaser → reveal → last chance sequence has three opportunities to convert, and each phase builds on the previous one's awareness.
5. **Local businesses need location-specific CTAs** — "Visit us at 123 Main St" or a Google Maps pin is more effective than "Shop now" for local promotions. The CTA should match how the viewer will act (visit in person vs. click online).

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p | YouTube / website / email |
| MP4 9:16 | 1080x1920 | TikTok / Reels / Stories |
| MP4 1:1 | 1080x1080 | Instagram / Facebook feed |
| MP4 4:5 | 1080x1350 | Instagram feed (tall) |

## Related Skills

- [ai-testimonial-video](/skills/ai-testimonial-video) — Testimonial videos
- [ai-explainer-video](/skills/ai-explainer-video) — Explainer videos
- [ai-commercial-video](/skills/ai-commercial-video) — Commercial videos
- [video-ad-maker](/skills/video-ad-maker) — Video ads
