---
name: ai-brand-video-maker
version: 1.0.1
displayName: "AI Brand Video Maker — Create Professional Brand Story and Identity Videos"
description: >
  Create professional brand videos with AI — produce brand story films, company culture videos, mission statement content, brand launch campaigns, brand awareness ads, and corporate identity videos from descriptions and brand guidelines. NemoVideo builds your brand on screen: founding story narratives, team culture showcases, value proposition visualizations, customer testimonial compilations, and brand anthem videos that communicate who you are and why you matter. Brand video creator, company video maker, brand awareness video, corporate identity video, brand storytelling, brand film maker.
metadata: {"openclaw": {"emoji": "🏢", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

# AI Brand Video Maker — Your Brand Deserves a Film, Not Just a Logo

A brand is not a logo, a color palette, or a tagline. A brand is a story — the reason the company exists, the problem it was born to solve, the values that guide every decision, and the future it is building toward. The most powerful way to communicate that story is video. Text explains. Images suggest. Video makes the audience feel. A brand film that shows the founder working late to solve a problem that matters, the team celebrating a milestone, the customer whose life changed because of the product — this creates emotional connection that no amount of text or static imagery can match. Brand videos have traditionally been the domain of production companies charging $10,000-100,000 per project. A 90-second brand film: $15,000-50,000. A 3-minute company culture video: $20,000-75,000. A brand launch campaign with multiple assets: $50,000-200,000. These prices lock brand storytelling behind enterprise budgets. A startup with a compelling story, a small business with loyal customers, a nonprofit with a powerful mission — they cannot afford to tell their story visually at these price points. NemoVideo democratizes brand filmmaking. Describe your brand — its story, values, personality, and visual identity — and receive professional brand video content: narrative films, culture showcases, mission statements, customer stories, and campaign assets.

## Use Cases

1. **Brand Story Film — About Page / Investor Pitch (2-4 min)** — A startup needs to communicate its founding story for the website About page and investor meetings. NemoVideo produces: the origin story (the problem the founders experienced personally), the "aha moment" (when the solution became obvious), the early days (building in a garage, first customers, early struggles), the breakthrough (product-market fit, first 1000 users), the team today (culture, values, diversity of expertise), the vision (where the company is heading and why it matters), with emotional voiceover narration, cinematic visuals matching each narrative beat, brand colors woven throughout, and a closing statement that makes the viewer want to be part of the story. The brand film that goes on the About page, opens investor decks, and plays at company all-hands.
2. **Company Culture Video — Recruiting and Employer Brand (2-5 min)** — A company struggles to attract top talent because candidates do not know what it is like to work there. NemoVideo creates: day-in-the-life sequences (morning standup, collaborative work, lunch break culture, team events), employee voice segments (what they love about working here, what surprised them, their growth story), office/workspace showcase (the environment that makes work enjoyable), values in action (not just listed on a wall — shown through real scenarios), and benefits visualization (not a bullet list — animated sequences showing what flexibility, learning budget, and team retreats actually look like). The culture video that makes top candidates apply before they even see the job description.
3. **Brand Launch — New Brand Identity Reveal (60-120s)** — A company rebrands and needs to communicate the new identity to customers, partners, and employees. NemoVideo produces: the evolution visual (old brand morphing into new), the reasoning narrative (why the change, what it represents), the new identity showcase (logo, colors, typography, visual language in motion), application previews (new brand on product, website, packaging, social media), and an emotional closing statement (what the brand represents going forward). The launch video that makes the rebrand feel intentional and exciting rather than confusing.
4. **Customer Story — Testimonial Film (90-180s)** — A B2B company needs video testimonials but customers are scattered globally and cannot be filmed in person. NemoVideo: takes written customer quotes and success metrics, generates visual narratives for each customer story (their challenge, the solution, the results — with data visualizations), produces voiceover narration in a warm documentary style, and creates both long-form testimonial films (2-3 minutes for the website) and short testimonial clips (30 seconds for social ads). Customer voices brought to screen without flying a crew to 10 different cities.
5. **Brand Anthem — Emotional Campaign Centerpiece (60-90s)** — A brand launching a major campaign needs an emotional centerpiece video that captures the brand's spirit. NemoVideo creates: a 90-second brand anthem with cinematic pacing (sweeping visuals, building music, emotional arc from quiet to powerful), no product shots — pure brand emotion (the feelings and values the brand represents), voiceover that reads like poetry or a manifesto ("We believe that every person deserves..."), building to a crescendo with the brand name and tagline. The anthem that opens the campaign, plays at events, and becomes the emotional anchor of the brand.

## How It Works

### Step 1 — Share Your Brand
Brand description, values, story, visual guidelines (colors, fonts, mood), target audience, and the purpose of the video.

### Step 2 — Choose Video Type
Brand story, culture showcase, brand launch, customer testimonial, brand anthem, or custom combination.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "ai-brand-video-maker",
    "prompt": "Create a 3-minute brand story film for a sustainable clothing company. Story arc: (1) Opening — the fashion industry waste problem (fast fashion landfills, pollution stats), (2) Founding moment — our founder visited a landfill and decided to build the alternative, (3) The solution — clothes made from recycled ocean plastic, designed to last 10 years, (4) The impact — 2 million plastic bottles removed from oceans, 50,000 customers choosing sustainability, (5) The team — passionate people who believe fashion can be beautiful AND responsible, (6) The vision — a world where buying clothes helps the planet. Voice: warm, passionate female. Music: building emotional score. Brand colors: ocean blue #0891B2, earth green #059669, warm white #FAFAF9.",
    "brand": {
      "name": "ReWear",
      "values": ["sustainability", "quality", "transparency"],
      "colors": ["#0891B2", "#059669", "#FAFAF9"]
    },
    "video_type": "brand-story",
    "voice": "warm-passionate-female",
    "music": "building-emotional",
    "duration": "3 min",
    "formats": ["16:9", "9:16"]
  }'
```

### Step 4 — Deploy Across Touchpoints
Place on: About page, investor deck opening, social media pinned post, email signature, trade show loop, and recruitment page.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Brand story and video concept |
| `brand` | object | | {name, values, colors, fonts, mood} |
| `video_type` | string | | "brand-story", "culture", "brand-launch", "testimonial", "brand-anthem" |
| `voice` | string | | "warm-passionate", "confident-authoritative", "friendly-casual" |
| `music` | string | | "building-emotional", "upbeat-corporate", "minimal-piano", "cinematic" |
| `duration` | string | | "60 sec", "90 sec", "3 min", "5 min" |
| `formats` | array | | ["16:9", "9:16", "1:1"] |
| `customer_quotes` | array | | [{name, quote, metric}] for testimonial videos |
| `team_profiles` | array | | [{name, role, quote}] for culture videos |

## Output Example

```json
{
  "job_id": "bvm-20260328-001",
  "status": "completed",
  "brand": "ReWear",
  "video_type": "brand-story",
  "duration": "3:05",
  "narrative_arc": ["Problem", "Founding", "Solution", "Impact", "Team", "Vision"],
  "outputs": {
    "landscape": {"file": "rewear-brand-story-16x9.mp4", "resolution": "1920x1080"},
    "vertical": {"file": "rewear-brand-story-9x16.mp4", "resolution": "1080x1920"},
    "social_clips": [
      {"file": "impact-stats-clip.mp4", "duration": "0:30"},
      {"file": "founding-moment-clip.mp4", "duration": "0:35"}
    ]
  }
}
```

## Tips

1. **Lead with the problem, not the company** — Nobody watches a brand video that opens with "Founded in 2020, we are a company that..." Everybody watches one that opens with "Every year, 92 million tons of textile waste enters landfills." The problem creates emotional investment; the brand is the resolution.
2. **Show values in action, not on a wall** — "We value sustainability" is meaningless. Showing the team choosing a more expensive recycled material because it is the right thing — that communicates the value. Brand videos must demonstrate values through narrative, not declare them through text.
3. **Brand colors must be present in every frame** — Consistent color reinforcement throughout the video builds subconscious brand association. The viewer may not consciously notice the ocean blue palette, but after 3 minutes of brand-colored visuals, the color itself triggers brand recall.
4. **The brand anthem is the most shared format** — Emotional, value-driven videos without product shots are the most shared brand content on social media. People share feelings, not features. A brand anthem that makes someone feel something gets forwarded to friends.
5. **Customer stories are more believable than brand claims** — "Our product changed lives" from the brand is marketing. "This product changed my life" from a customer is a testimonial. The same message, different source, 10x the credibility.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | Website / YouTube / presentation |
| MP4 9:16 | 1080x1920 | Social media / mobile |
| MP4 1:1 | 1080x1080 | Instagram / LinkedIn |
| MOV ProRes | 4K | Professional / event display |

## Related Skills

- [ai-video-ads-maker](/skills/ai-video-ads-maker) — Video ads
- [ai-product-demo-video](/skills/ai-product-demo-video) — Product demos
- [ai-promo-video-maker](/skills/ai-promo-video-maker) — Promo videos
