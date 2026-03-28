---
name: instagram-reels-editor
version: "1.0.0"
displayName: "Instagram Reels Editor — AI Editor for Reels with Transitions Music and Captions"
description: >
  Edit Instagram Reels with AI — create scroll-stopping vertical videos with trending transitions, beat-synced music, animated captions, hook text, engagement stickers, and Reels-optimized formatting. NemoVideo transforms raw footage into polished Reels content: 9:16 vertical crop with face tracking, trending audio sync, word-by-word captions in the style that drives engagement, pattern-interrupt transitions every 3-5 seconds, and hooks that stop the scroll in the first 0.5 seconds. Instagram Reels editor online, Reels maker, edit Reels with music, Reels caption generator, Instagram video editor, Reels transition effects, vertical video editor for Instagram.
metadata: {"openclaw": {"emoji": "📸", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Instagram Reels Editor — Every Edit Optimized for the Reels Algorithm

Instagram Reels rewards specific content patterns. Not opinions — data. Reels that hold attention past the 3-second mark get distributed to the Explore page. Reels with captions get 40% higher reach because 80% of Instagram users scroll with sound off. Reels with pattern-interrupt transitions every 3-5 seconds maintain the average 1.3-second attention span that the platform has trained into its users. Reels that use trending audio get a distribution boost from Instagram's recommendation system. Reels that are exactly 7, 15, 30, or 60 seconds perform better than odd lengths because Instagram's algorithm categorizes them into optimal distribution buckets. None of this is secret. Instagram publishes these signals in their creator documentation. The challenge is not knowing what works — it is executing all of it simultaneously in every Reel. A creator must: shoot vertical (or reframe horizontal footage), edit to exact duration targets, add captions in the trending style, sync cuts to trending audio beats, add a hook in the first 0.5 seconds, include pattern-interrupts every 3-5 seconds, and export at Instagram's preferred specs. NemoVideo handles all of these optimizations from a single description. Upload footage, describe the Reel, and every algorithm-friendly edit is applied automatically.

## Use Cases

1. **Talking-Head Reel — Hook + Content + CTA (15-30s)** — A business coach records 2 minutes of phone video with one key tip. NemoVideo: extracts the best 25-second segment (highest energy, clearest delivery), adds a text hook in the first frame ("The networking mistake costing you clients" — bold white text, dark background, 1 second), cuts to the speaking content with word-by-word animated captions (trending style: white bold, yellow highlight on active word, dark pill background), applies gentle zoom-cuts every 5 seconds (100% → 110% alternating for visual variety), adds trending audio at -22dB under the speech, and ends with a CTA overlay ("Follow for more tips" with animated arrow). A raw 2-minute ramble becomes a polished 25-second Reel optimized for distribution.
2. **Product Showcase Reel — Visual Transitions (15-30s)** — A small business owner has 8 product photos and 3 short video clips. NemoVideo: arranges them in a visual story (problem → solution → product shots → social proof), applies trending transitions between each (smooth zoom, whip pan, morph cut — different transition for each cut), syncs every transition to the beat of a trending audio track, adds text overlays on each segment ("Handmade" / "Sustainable" / "Ships Tomorrow"), includes price and shop link as a persistent bottom overlay, and exports at exactly 15 seconds (optimal for product Reels). Static product content becomes a dynamic shopping Reel.
3. **Before/After Reel — Transformation Content (7-15s)** — A makeup artist has a before and after. NemoVideo: opens with "Before" text over the unedited photo (2 seconds), applies a dramatic transition (the signature swipe, zoom-in, or glitch effect), reveals the "After" with slow pan across the finished look (3 seconds with subtle zoom), then quick-cuts between before and after (1-second alternations for impact), with trending audio that has a beat drop at the transition moment. Before/after is the highest-performing Reel format for beauty, fitness, home renovation, and design creators.
4. **Carousel-Style Reel — Educational Content (30-60s)** — A financial educator wants to explain "5 money habits of millionaires" in Reel format. NemoVideo: creates a title card hook ("5 habits that made me a millionaire" — bold text, engaging visual), then 5 segments (one per habit) each with: numbered text overlay ("Habit #3"), supporting visual or stock clip, 5-second duration per habit, smooth transition between segments, and a recap final card. Word-by-word captions throughout for sound-off viewers. Educational carousel Reels get saved (bookmarked) at 5x the rate of standard content — saves are Instagram's strongest ranking signal.
5. **Trending Audio Sync — Dance/Lifestyle (15-30s)** — A lifestyle creator wants clips from their week synced to a trending audio. NemoVideo: takes 10-15 short clips, selects the best moments from each, arranges by visual flow (matching movement direction, color palette, energy level), syncs every cut to the audio beat (cut on kick, transition on snare), adjusts clip speed where needed to match beat timing (slight speed-up or slow-down to land on beats), adds cohesive color grade, and exports at exactly 15 or 30 seconds. The "weekly montage" format that consistently goes viral on Reels.

## How It Works

### Step 1 — Upload Raw Content
Video clips, photos, or a mix. Phone footage, camera footage, screen recordings — any source. NemoVideo handles vertical reframing from horizontal source.

### Step 2 — Describe the Reel
What is the content about? What feeling should it create? Any specific style or trend to follow? Be specific or general — NemoVideo adapts.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "instagram-reels-editor",
    "prompt": "Create a 30-second talking-head Reel from raw 3-minute footage. Hook: bold text card first frame — Stop doing THIS on Instagram (white text, red underline on THIS, black bg, 1.2 sec). Content: extract the punchiest 25 seconds of speaking. Captions: word-by-word highlight (white bold #FFFFFF, active word #FF6B6B coral, dark pill bg, bottom center, large mobile-readable font). Zoom-cuts: alternate 100%%/112%% every 6 sec. Music: trending lo-fi at -22dB with speech ducking. CTA: last 3 sec overlay — Save this for later 🔖 (animated bookmark icon). Color grade: warm-bright Instagram aesthetic.",
    "hook": {"text": "Stop doing THIS on Instagram", "style": "bold-red-underline", "duration": 1.2},
    "captions": {"style": "word-highlight", "text": "#FFFFFF", "highlight": "#FF6B6B", "bg": "pill-dark", "position": "bottom-center", "size": "large"},
    "zoom_cuts": {"interval": 6, "range": "100-112"},
    "music": {"track": "trending-lofi", "volume": "-22dB", "ducking": true},
    "cta": {"text": "Save this for later 🔖", "duration": 3, "animation": "slide-up"},
    "color_grade": "warm-bright",
    "duration": 30,
    "format": "9:16"
  }'
```

### Step 4 — Preview and Post
Check: hook grabs attention in under 1 second, captions are readable on mobile, transitions land on beats, CTA is clear. Post directly to Instagram.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Reel concept and edit instructions |
| `hook` | object | | {text, style, duration} — first-frame hook |
| `captions` | object | | {style, text, highlight, bg, position, size} |
| `zoom_cuts` | object | | {interval, range} |
| `transitions` | string | | "trending", "smooth-zoom", "whip-pan", "morph", "glitch" |
| `music` | object | | {track, volume, ducking} |
| `beat_sync` | boolean | | Sync cuts to audio beats (default: true) |
| `cta` | object | | {text, duration, animation} — call to action |
| `color_grade` | string | | "warm-bright", "moody", "clean", "vibrant" |
| `duration` | integer | | Target duration: 7, 15, 30, 60 |
| `format` | string | | "9:16" (always vertical for Reels) |
| `text_overlays` | array | | [{text, timestamp, style}] |

## Output Example

```json
{
  "job_id": "ire-20260328-001",
  "status": "completed",
  "source_duration": "3:05",
  "reel_duration": "0:30",
  "format": "9:16 (1080x1920)",
  "edits": {
    "hook": "Stop doing THIS on Instagram (1.2s)",
    "content_extracted": "25s from 3:05 source",
    "captions": "word-highlight (white + #FF6B6B coral)",
    "zoom_cuts": 5,
    "music": "trending lo-fi at -22dB with ducking",
    "cta": "Save this for later 🔖 (3s slide-up)",
    "color_grade": "warm-bright"
  },
  "output": {
    "file": "reel-instagram-ready.mp4",
    "resolution": "1080x1920",
    "duration": "0:30",
    "file_size": "18.2 MB"
  }
}
```

## Tips

1. **The first 0.5 seconds decide everything** — Instagram's algorithm measures "initial retention" — did the viewer stop scrolling? A bold text hook with high contrast and an emotionally triggering statement ("Stop doing this" / "Nobody talks about this" / "This changed everything") is the single most important element of any Reel.
2. **Word-by-word captions are not optional for Reels** — 80% of Instagram users scroll with sound off. Without captions, 80% of your potential audience sees moving lips with no context and scrolls past. Captions are the content for the sound-off majority.
3. **Pattern-interrupts every 3-5 seconds maintain attention** — A zoom-cut, a transition, a text overlay appearing, a scene change — any visual change resets the viewer's attention clock. Without pattern-interrupts, the viewer's brain decides "I've seen enough" at the 3-second mark.
4. **Trending audio gives algorithmic distribution boost** — Instagram's recommendation system actively promotes Reels using audio that is currently trending. Even at -22dB under speech, the audio tag matters for distribution. Always include trending audio.
5. **Save-worthy content gets 5x the distribution** — Instagram weights saves (bookmarks) as the strongest engagement signal. Educational content ("5 tips"), reference content ("save for later"), and actionable content ("try this today") drive saves. End every Reel with a save prompt.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 9:16 | 1080x1920 | Instagram Reels |
| MP4 9:16 | 1080x1920 | Also works for TikTok / Shorts |
| MP4 1:1 | 1080x1080 | Instagram Feed fallback |

## Related Skills

- [reels-creator](/skills/reels-creator) — Create Reels from scratch
- [video-reverser](/skills/video-reverser) — Reverse video effects
- [auto-caption-video](/skills/auto-caption-video) — Auto captioning
