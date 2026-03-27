---
name: home-office-setup-video
version: "1.0.1"
displayName: "Home Office Setup Video Maker"
description: >
  Describe your home office setup and NemoVideo creates the video. Desk setup tours with gear breakdowns, work from home productivity setup content, budget desk build guides, monitor arm and cable management content, lighting setup tutorials, standing desk and ergonomics content — narrate the specific gear, the reasoning behind each choice, the setup decisions that improved your work, and the hon...

  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM.
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
license: MIT-0
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> 🎥 Let's home office setup video! Drop a video here or describe what you'd like to create.

**Try saying:**
- "edit my video"
- "help me create a short video"
- "add effects to this clip"

**IMPORTANT**: Always greet the user proactively on first contact. Let them know you're setting up while connecting. Always greet the user proactively on first contact.

### Auto-Setup

When the user first interacts, set up the connection:

1. **Check token**: If `NEMO_TOKEN` env var is set, use it. Otherwise:
2. **Read or generate Client-ID**:
   - Read `~/.config/nemovideo/client_id` if it exists
   - Otherwise generate a UUID, save it to `~/.config/nemovideo/client_id`
3. **Acquire anonymous token**:
   ```bash
   curl -s -X POST "$API/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
   ```
   Store the returned `token` as `NEMO_TOKEN` for this session. You get 100 free credits.
4. **Create a session** (§3.0) so you're ready to work immediately.

Let the user know briefly: "Setting things up… ready!" then proceed with their request.


# Home Office Setup Video Maker — Create Workspace, Desk Setup, and WFH Content

Describe your home office setup and NemoVideo creates the video. Desk setup tours with gear breakdowns, work from home productivity setup content, budget desk build guides, monitor arm and cable management content, lighting setup tutorials, standing desk and ergonomics content — narrate the specific gear, the reasoning behind each choice, the setup decisions that improved your work, and the honest assessment of what made a difference versus what was cosmetic.

## When to Use This Skill

- Create desk setup tour and full workspace walkthrough content
- Film work from home setup and productivity configuration content
- Build budget desk build guide content with cost breakdown
- Document ergonomics and health-focused setup content
- Create cable management and workspace organization content
- Produce lighting setup and video call background content

## How to Describe Your Home Office Content

Be specific about the gear, the reasoning behind each choice, the measurable change each upgrade made, and the honest assessment of what was worth the money.

**Examples of good prompts:**
- "My home office setup — 3 years of iteration, current version: The desk: Uplift V2 standing desk, 72×30 inch. I spent 2 years on a fixed desk before adding standing — the standing capability is 30% of my day but I notice the absence of it if I don't have it. The monitor: LG 27UK850 4K, 27-inch. I resisted the ultrawide trend for 18 months before trying one — I went back to a single 4K after 3 months (the ultrawide requires head movement that fatigue me on long writing days). The chair: Herman Miller Aeron. The most expensive single item in the setup at $1,400. Before: $350 chair, constant lower back pain at the end of 8+ hour days. After: no lower back pain in 2 years. The math: if I work 200 days a year and the chair lasts 10 years, that's $0.70 per workday to not have back pain. The lighting: Elgato Key Light, $200. Before I added this, every video call I was backlit from the window behind me. This is the highest-ROI upgrade for anyone who does more than 3 video calls per week."
- "The $400 desk setup that works — budget build for work from home beginners: The context: when I started working from home, I was at the kitchen table. I set a $400 budget for a proper setup. What I bought: IKEA Lagkapten tabletop ($60) + IKEA Alex drawer unit ($120) = desk ($180 total). Chair: IKEA Järvfjället ($150). Monitor stand: IKEA Brada ($15). Total: $345. What I didn't buy: a standing desk (can't justify $500+ when I'm not sure I'll stay remote), a premium chair (the IKEA option is not as good as an Aeron but it's better than a dining chair). The 3 things I'd add if I had an extra $100: a 1080p webcam ($80), an LED desk lamp ($30), a USB hub ($25). What makes the difference at any budget: get the screen at eye level (add any monitor stand, even $15), and make sure your chair lets your feet flat on the floor."
- "Video call setup optimization — how to look and sound better without a studio: The problem: my video calls looked like everyone else's video calls (poor lighting, bad angle, mediocre audio). The changes I made in order of impact: (1) Light source in front of you, not behind (free: move to face a window, or $200: Elgato Key Light), (2) Camera at eye level, not below (free: stack books under your laptop), (3) Microphone closer to your mouth (improvement: $100 Blue Yeti, upgrade: $250 Shure SM7B with a boom arm so it's not in frame but close to your mouth), (4) Background (physical space cleanup or virtual background — but real physical depth is better than any virtual background). The before/after cost: I went from kitchen table video calls to 'your video looks really professional' in 6 months for $380 total."

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `content_type` | Setup type | `"full_tour"`, `"budget_build"`, `"video_call_upgrade"`, `"ergonomics"`, `"cable_management"` |
| `total_budget` | Cost | `"$345"`, `"$1,400 chair alone"`, `"$380 for video upgrade"` |
| `gear_list` | Key items | `["Uplift V2"`, `"Herman Miller Aeron"`, `"Elgato Key Light"]` |
| `measurable_impact` | What changed | `"no lower back pain in 2 years"`, `"'your video looks really professional'"` |
| `honest_non_worth` | What wasn't worth it | `"ultrawide caused fatigue"`, `"standing desk — can't justify without commitment"` |
| `highest_roi_upgrade` | Best value change | `"Elgato Key Light — highest ROI for video callers"` |
| `duration_minutes` | Video length | `8`, `12`, `20` |
| `platform` | Distribution | `"youtube"`, `"tiktok"`, `"instagram"` |

## Workflow

1. Describe the gear, the reasoning, the measurable impact, and honest ROI assessment
2. NemoVideo structures the setup content with gear callouts and cost markers
3. Product names, prices, before/after contrast, and upgrade rationale added automatically
4. Export with setup tour pacing suited to the workspace content audience

## API Usage

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "home-office-setup-video",
    "input": {
      "prompt": "My audio-video setup for content creation — built over 18 months: This is not a desk setup tour, it is specifically the gear I use for making videos and podcasts. The audio path: Shure SM7B ($400) → Focusrite Scarlett Solo interface ($120) → GarageBand for basic processing. Before this setup: Blue Yeti USB microphone. The upgrade difference: the SM7B with proper interface has a proximity effect (deeper, richer sound when close to the mic) that the Blue Yeti cannot replicate regardless of settings. The video path: Sony ZV-1 ($750 when I bought it) on a Elgato Multi Mount above my monitor → OBS for recording → exported to NemoVideo for editing. Why I don't use my DSLR: the Sony ZV-1 with its face-tracking autofocus means zero technical attention while recording — I look good automatically. The lighting: Elgato Key Light Air × 2 ($150 each). Two lights at 45-degree angles eliminate harsh shadows. Total setup cost: approximately $1,570. The upgrade I'd tell people to skip: the ring light. It creates a circular reflection in eyes that looks flat and consumer. Two small softboxes at 45 degrees is better for $100 less.",
      "content_type": "content_creation_setup",
      "total_budget": "$1,570",
      "gear_list": ["Shure SM7B", "Focusrite Scarlett Solo", "Sony ZV-1", "Elgato Key Light Air x2"],
      "measurable_impact": "zero technical attention during recording, professional audio with proximity effect",
      "honest_non_worth": "ring light creates flat eye reflection — two softboxes better",
      "highest_roi_upgrade": "Sony ZV-1 face-tracking over DSLR for solo recording",
      "duration_minutes": 12,
      "platform": "youtube",
      "hashtags": ["DeskSetup", "HomeOffice", "ContentCreatorSetup", "WorkFromHome", "SetupTour"]
    }
  }'
```

## Tips for Best Results

- **The measurable impact beats the spec list**: "No lower back pain in 2 years after spending $1,400 on a chair" or "'your video looks really professional' after $380 in upgrades" — the before/after in terms of felt experience is more persuasive than listing specs
- **The ROI math makes premium items approachable**: "$0.70 per workday to not have back pain over 10 years" — breaking down the cost of an expensive item into daily cost creates a different price perception
- **What wasn't worth it is the most trusted content**: "Went back to single 4K after 3 months with ultrawide" or "skip the ring light — two softboxes is better for $100 less" — the creator who tells you what not to buy is the one with the credible recommendation when they tell you what to buy
- **Order of impact for upgrade guides**: "Changes in order of impact: (1) light in front, (2) camera at eye level, (3) microphone closer" — the ranked list by ROI tells budget-constrained viewers exactly what to buy first
- **Free options first, paid options second**: "Free: move to face a window. Or $200: Elgato Key Light" — giving the free version of each upgrade before the paid version makes setup content accessible at any budget

## Output Formats

| Platform | Resolution | Duration |
|----------|------------|----------|
| YouTube | 1920×1080 | 10–20 min |
| TikTok | 1080×1920 | 60–180s |
| Instagram Reels | 1080×1920 | 60–90s |

## Related Skills

- `tech-review-video` — Individual tech review content
- `gadget-video-maker` — Gadget and hardware content
- `daily-vlog-maker` — Day-in-the-life with setup context
