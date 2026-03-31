---
name: adventure-video-maker
version: 1.0.5
displayName: "Adventure Video Maker — Create Outdoor Adventure and Extreme Sport Videos"
description: >
    Adventure Video Maker — Create Outdoor Adventure and Extreme Sport Videos. Works by connecting to the NemoVideo AI backend. Supports MP4, MOV, AVI, WebM, and MKV output formats. Automatic credential setup on first use — no manual configuration needed.
metadata: {"openclaw": {"emoji": "🏔️", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
apiDomain: https://mega-api-prod.nemovideo.ai
repository: https://github.com/nemovideo/nemovideo_skills
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> 🎵 Let's adventure video maker! Drop a video here or describe what you'd like to create.

**Try saying:**
- "help me create a short video"
- "edit my video"
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
   curl -s -X POST "https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
   ```
   Store the returned `token` as `NEMO_TOKEN` for this session. You get 100 free credits.
4. **Create a session** (§3.0) so you're ready to work immediately.

Let the user know briefly: "Setting things up… ready!" then proceed with their request.


# Adventure Video Maker — Outdoor Adventure and Extreme Sport Videos

The paragliding tandem flight over Interlaken lasted eighteen transcendent minutes — the Alps filling every direction, the lake glittering 4,000 feet below, and a silence broken only by the wind and the pilot saying "ready for the spiral?" — but the GoPro chest mount recorded mostly harness straps and the sound of hyperventilating, and the phone in the shaking hand captured a blurry panorama that could be literally anywhere with mountains. Adventure content is the highest-adrenaline, lowest-production-quality genre on the internet: the moments are extraordinary but the filming conditions — wind, water, vibration, panic, and the physical impossibility of holding a camera steady while clinging to a rock face — conspire against every clip. This tool transforms chaotic adventure footage into cinematic outdoor videos — action sequences stabilized and color-graded for dramatic landscapes, speed-ramped for impact (slow-motion launch, real-time flight, speed-ramp landing), GPS data overlaid as altitude and speed trackers, map routes showing the path through wilderness, ambient nature audio preserved and enhanced (wind, water, birdsong), and the emotional arc structured from preparation through challenge to summit or finish. Built for GoPro-wearing adventurers editing on laptops in hostels, outdoor brands producing athlete-feature content, adventure-tour operators showcasing experiences for booking pages, mountaineering clubs documenting expeditions, and extreme-sport athletes compiling sponsor reels.

## Example Prompts

### 1. Multi-Day Trek — Patagonia Torres del Paine W-Circuit
"Create an 8-minute trek highlight from 5 days on the W-Circuit. Map animation opening: the W-shaped route overlaid on Torres del Paine National Park, each camp marked — Paine Grande → Grey → Cuernos → Chileno → Torres Base. Day-by-day structure: Day 1 — Grey Glacier (the first ice sighting, calving audio boosted, glacier-blue color emphasis), Day 2 — Valle del Francés (the amphitheater of granite, 360° pan with peak names labeled — Cuerno Principal, Espada, Hoja), Day 3 — weather day (rain, huddling in the refugio, honest talking-head: 'Day 3 was brutal. Horizontal rain, zero visibility, ate cold pasta'), Day 4 — Torres sunrise attempt (4 AM headlamp start, the reveal moment as the towers turn orange at dawn — hold 5 seconds, no music, just wind), Day 5 — descent and celebration beer at the bar. Running stats sidebar: total km walked, elevation gained, daily weather. Cinematic grade: moody overcast for rain days, saturated for glacier blue, golden for the sunrise. Epic orchestral soundtrack building to the Torres reveal, then silence."

### 2. Whitewater Kayaking — Class IV Rapids Highlight
"Build a 90-second kayaking highlight reel from a Class IV river run. Opening: calm put-in point, paddle dipping into still water — contrast with what's coming. First rapid: GoPro helmet-mount POV plunging into the first hole — water crashing over the lens, emerging on the other side. Speed-ramp: slow-motion on the drop entry (0.25×), real-time through the chaos, slow-motion on the exit paddle brace. Second rapid: bank-mounted camera showing the full rapid from above with the kayaker's line traced in real-time — green line for clean, red pulse where the boof stroke was late. Eddy-out celebration: fist pump and primal yell (preserve this audio). Rapid names overlaid as each section begins: 'Initiation (III+) → Meat Grinder (IV) → The Washing Machine (IV) → Redemption (III).' Water-droplet transition between segments. No talking — just river roar, paddle slap, and the occasional whoop. Adrenaline electronic soundtrack synced to the drop moments."

### 3. Rock Climbing Send — Sport Climbing Project Video
"Produce a 4-minute sport-climbing project video. Structure: The Failures → The Work → The Send. Opening montage: three falls on the same crux move from different sessions, each dated — 'Attempt #4, Feb 12' / 'Attempt #11, Mar 2' / 'Attempt #17, Mar 15' — showing incremental improvement (slightly higher each time). Training segment: hangboard close-up with timer overlay, campus board rungs, route-reading with sequence visualization drawn on a still photo of the wall. The Send: full unbroken send from ground to chains, dual angle — climber POV (looking up) intercut with belayer angle (looking up at climber). Crux sequence in slow motion: the dyno move, the catch, the foot swap — hold the catch frame for 2 seconds. Chains clipped: celebration scream, belayer reaction, hands chalked and shaking. Grade and route name overlaid: 'Northern Exposure | 5.12c | 23 meters | Red River Gorge.' Closing: the climber's hands, raw and taped, holding the anchor chain. Emotional indie rock building throughout, peaking at the chains clip."

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the adventure, route, key moments, and emotional arc |
| `duration` | string | | Target video length (e.g. "90 sec", "4 min", "8 min") |
| `style` | string | | Visual style: "cinematic-epic", "raw-gopro", "documentary", "athlete-reel" |
| `music` | string | | Music mood: "epic-orchestral", "electronic-adrenaline", "indie-emotional", "none" |
| `format` | string | | Output ratio: "16:9", "9:16", "1:1" |
| `gps_overlay` | boolean | | Show altitude, speed, and GPS data on screen (default: false) |
| `speed_ramp` | boolean | | Enable automatic speed ramping on action moments (default: true) |

## Workflow

1. **Describe** — Write the adventure narrative with route, key moments, emotional arc, and the climax
2. **Upload** — Add GoPro clips, drone footage, phone clips, GPS tracks, and any multi-angle coverage
3. **Generate** — AI assembles the adventure with speed ramps, GPS overlays, map routes, and emotional pacing
4. **Review** — Preview the video, adjust the speed-ramp timing, verify the climax moment placement
5. **Export** — Download in your chosen format and resolution

## API Example

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "adventure-video-maker",
    "prompt": "Create an 8-minute Patagonia W-Circuit trek highlight: 5 days, map animation of W route, glacier calving, Valle del Francés amphitheater with peak labels, Torres sunrise reveal held 5 seconds with silence, running km/elevation stats, epic orchestral building to sunrise then silence",
    "duration": "8 min",
    "style": "cinematic-epic",
    "gps_overlay": true,
    "format": "16:9"
  }'
```

## Tips for Best Results

1. **Structure the emotional arc explicitly** — "Failures → Work → Send" or "Storm → Struggle → Summit." Adventure videos without a narrative arc are just action clips. The AI uses your arc description to pace the music, color grade (dark for struggle, bright for triumph), and editing rhythm.
2. **Name the specific rapid, route, or peak** — "Meat Grinder (IV)" and "Northern Exposure 5.12c" give the AI exact text overlays and signal to the viewer that this is real, graded content — not a random clip. Specificity builds credibility in adventure communities.
3. **Describe the silence moments** — "Torres turning orange at dawn — hold 5 seconds, no music, just wind" is the most powerful direction you can give. The AI drops all music and lets the natural audio carry the emotional peak. Silence after buildup is more powerful than any soundtrack.
4. **Include the failure footage** — "Three falls on the crux from different sessions" is more engaging than a clean send alone. Adventure audiences respect the process; showing only success looks fake. The AI sequences failures chronologically to build tension toward the resolution.
5. **Specify camera sources** — "GoPro helmet mount," "bank-mounted camera," "belayer angle" helps the AI select the right clip for each moment. Multi-angle adventure footage is only useful if the AI knows which angle serves which narrative beat.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube adventure documentary |
| MP4 9:16 | 1080p | TikTok / Instagram Reels / Shorts |
| MP4 16:9 highlight | 1080p | 60-90 sec sponsor reel |
| MP4 + GPX | 1080p | Video with embedded GPS track data |

## Related Skills

- [travel-video-maker](/skills/travel-video-maker) — Trip highlight reels and vacation recaps
- [hiking-video-maker](/skills/hiking-video-maker) — Hiking trail documentation and summit videos
- [surfing-video-maker](/skills/surfing-video-maker) — Wave riding and surf session edits
