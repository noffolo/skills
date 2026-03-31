---
name: demo-video-maker
version: "1.0.0"
displayName: "Demo Video Maker — Create Product Demo Videos with AI for SaaS Apps and Products"
description: >
  Create product demo videos with AI — generate professional product walkthroughs, feature showcases, onboarding tutorials, and sales demo recordings with animated UI mockups, zoom-and-click highlights, voiceover narration, captions, and music. NemoVideo produces the demo videos that SaaS companies embed on landing pages, product teams share with prospects, customer success teams use for onboarding, and sales teams send after calls — all from a product description or screen recording without a video production team.
metadata: {"openclaw": {"emoji": "🖥️", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Demo Video Maker — Product Demos That Sell Without a Sales Call

A product demo video is the most efficient sales tool in SaaS: it works 24/7, never has an off day, delivers the same perfect pitch every time, and scales to every prospect simultaneously. Landing pages with demo videos convert 72% better than those without. Sales emails with embedded demo videos get 3x more replies. Onboarding flows with demo videos reduce time-to-value by 40% and support tickets by 35%. Every SaaS company knows they need demo videos. Few make enough of them. The bottleneck: recording a quality demo requires a clean environment, a rehearsed script, a screen recording tool, a good microphone, multiple takes (most people need 5-10 takes per section), editing to remove mistakes, adding callouts and highlights, voiceover recording, and final polish. A 3-minute product demo takes a full production day. When the product updates (every sprint), the demo is outdated. NemoVideo produces demo videos from product descriptions, screen recordings, or UI screenshots — and regenerates them when the product changes. Describe what the product does, provide screen recordings or mockups, and the AI creates: a narrative product walkthrough with animated cursor movements, zoom-and-highlight on key features, clean voiceover explaining each step, text callouts for feature names and benefits, background music that maintains professional energy, and multi-format export for landing pages, sales outreach, onboarding, and social media.

## Use Cases

1. **Landing Page — Hero Demo (60-120s)** — A SaaS startup needs the landing page demo that converts visitors into signups. NemoVideo produces: hook that names the pain point ("Tired of managing projects across 5 different tools?"), product reveal (dashboard animation with clean UI mockup), 3 key feature demos (each 15-20 seconds with zoom-to-feature, animated cursor click, and result animation), social proof overlay ("Trusted by 3,000+ teams"), and CTA end frame ("Start free — no credit card required"). Voiceover: confident, friendly, 160 wpm. Music: upbeat-corporate at -18dB. A demo that tells the product story in 90 seconds.
2. **Sales Follow-Up — Personalized Demo (2-5 min)** — After a discovery call, a sales rep needs to send a personalized product walkthrough addressing the prospect's specific use case. NemoVideo generates: personalized opening ("Hi [Company], here's how [Product] solves the workflow challenge you described"), feature walkthrough focused on the relevant capabilities (not the whole product — just what this prospect needs), specific workflow animation showing their use case, comparison moment ("Currently you're doing X manually — here's what it looks like automated"), and a next-step CTA ("Let's schedule a deep dive — calendar link below"). The personalized demo that closes deals.
3. **Onboarding — First 5 Minutes (3-5 min)** — A new user just signed up and needs to reach their first success moment. NemoVideo creates: welcome screen ("Welcome to [Product] — let's get you set up in 5 minutes"), step-by-step walkthrough with animated cursor (Step 1: Create your workspace, Step 2: Invite your team, Step 3: Import your first project), each step shown as screen recording with zoom highlights on clickable elements, progress indicator ("Step 2 of 5"), and completion celebration ("You're all set! Here's what to explore next"). The onboarding video that reduces churn by getting users to value faster.
4. **Feature Launch — What's New (60-90s)** — A product team ships a new feature and needs an announcement video. NemoVideo produces: hook ("The feature you've been asking for is here"), before/after comparison (old workflow vs. new feature), animated walkthrough of the new capability with zoom-and-click, 2-3 benefit callouts as text overlays, and CTA ("Try it now in your dashboard"). Published on the changelog, emailed to users, and posted on social media. Feature adoption driven by clear visual communication.
5. **Investor Pitch — Product in Action (90s-3 min)** — A startup's pitch deck needs a product demo section that shows the product actually working. NemoVideo generates: market context animation (the problem being solved, animated data), product reveal (full UI shown in context), key workflow demonstration (the 2-3 actions that demonstrate core value), outcome visualization (metrics improvement, time saved, error reduction), and scale indication ("This is one user — now imagine 10,000"). The demo that makes investors say "I get it" in under 3 minutes.

## How It Works

### Step 1 — Provide Product Information
Upload: screen recordings, UI screenshots, product descriptions, or feature documentation. NemoVideo works with any combination of these inputs.

### Step 2 — Define Demo Structure
Choose: hook style, features to highlight, narration tone, target audience, and demo length.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "demo-video-maker",
    "prompt": "Create a 90-second landing page demo video for a SaaS project management tool. Structure: Hook (managing projects across scattered tools is chaos) → Product Reveal (clean dashboard overview) → Feature 1: Drag-and-drop task boards (15 sec, zoom to board, animated cursor drag) → Feature 2: Real-time team collaboration (15 sec, animated cursors from multiple users) → Feature 3: Automated weekly reports (15 sec, report generating animation) → Social proof (3000 teams trust us) → CTA (Start free, no credit card). Voice: confident friendly female, 160 wpm. Music: upbeat-corporate at -18dB. Brand colors: blue #2563EB, white.",
    "demo_type": "landing-page",
    "voice": "confident-friendly-female",
    "voice_speed": "160 wpm",
    "music": "upbeat-corporate",
    "music_volume": "-18dB",
    "brand": {"primary": "#2563EB", "secondary": "#FFFFFF"},
    "cursor_animation": true,
    "zoom_highlights": true,
    "captions": {"style": "sentence", "text": "#FFFFFF", "bg": "brand-semitransparent"},
    "duration": "90 sec",
    "format": "16:9"
  }'
```

### Step 4 — Review and Deploy
Preview the demo. Verify: feature accuracy, cursor timing, voiceover clarity. Deploy to landing page, embed in sales emails, or add to onboarding flow.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Product info and demo requirements |
| `demo_type` | string | | "landing-page", "sales-followup", "onboarding", "feature-launch", "pitch" |
| `voice` | string | | "confident-female", "friendly-male", "authoritative", "energetic" |
| `voice_speed` | string | | "140 wpm" (thorough), "160 wpm" (efficient), "170 wpm" (snappy) |
| `music` | string | | "upbeat-corporate", "minimal-tech", "cinematic", "none" |
| `music_volume` | string | | "-14dB" to "-22dB" |
| `brand` | object | | {primary, secondary, logo} |
| `cursor_animation` | boolean | | Animated cursor clicks and movements (default: true) |
| `zoom_highlights` | boolean | | Zoom to features during demo (default: true) |
| `captions` | object | | {style, text, bg} |
| `duration` | string | | "60 sec", "90 sec", "3 min", "5 min" |
| `format` | string | | "16:9", "9:16", "1:1" |
| `personalization` | object | | {company_name, use_case} for sales demos |

## Output Example

```json
{
  "job_id": "dvm-20260328-001",
  "status": "completed",
  "duration_seconds": 92,
  "format": "mp4",
  "resolution": "1920x1080",
  "output_url": "https://mega-api-prod.nemovideo.ai/output/dvm-20260328-001.mp4",
  "demo_structure": {
    "hook": "0:00-0:08 (pain point + curiosity)",
    "product_reveal": "0:08-0:18 (dashboard overview)",
    "feature_1": "0:18-0:35 (task boards with cursor animation)",
    "feature_2": "0:35-0:52 (real-time collaboration)",
    "feature_3": "0:52-1:08 (automated reports)",
    "social_proof": "1:08-1:18 (3000 teams)",
    "cta": "1:18-1:32 (start free)"
  },
  "production": {
    "voice": "confident-friendly-female at 160 wpm",
    "music": "upbeat-corporate at -18dB",
    "cursor_animations": 12,
    "zoom_highlights": 8
  }
}
```

## Tips

1. **90 seconds is the landing page demo sweet spot** — Under 60 seconds cannot demonstrate enough value. Over 2 minutes loses website visitors who are still evaluating. 75-90 seconds delivers: pain → product → proof → action.
2. **Zoom-to-feature is the most important visual technique** — When explaining a feature, zoom the screen to show only that feature at 200% size. The viewer sees exactly what you're describing without scanning a full UI for the relevant element.
3. **Animated cursor creates the "someone is showing me" feeling** — A static screen recording feels like documentation. An animated cursor clicking, dragging, and typing feels like a personal demo from a real person. The cursor transforms a screenshot into a guided experience.
4. **Feature launch videos should show before/after** — "We added X" is informative. "Before, you had to do Y manually. Now, one click does it" is persuasive. The contrast between old workflow and new capability is what drives feature adoption.
5. **Personalized sales demos close 2x more deals** — A generic product demo says "our product does X." A personalized demo says "for [Company], this means Y." The same product, but the prospect sees themselves using it. Personalization is the highest-leverage demo investment.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | Landing page / sales email |
| MP4 9:16 | 1080x1920 | Social media / product hunt |
| MP4 1:1 | 1080x1080 | LinkedIn / tweet embed |
| GIF | 720p | Feature highlight loop |
| WebM | 1080p | Web embed (smaller) |

## Related Skills

- [podcast-video-maker](/skills/podcast-video-maker) — Podcast video creation
- [make-video-ai](/skills/make-video-ai) — AI video creation
