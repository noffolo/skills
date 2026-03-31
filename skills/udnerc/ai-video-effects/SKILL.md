---
name: ai-video-effects
version: 1.0.1
displayName: "AI Video Effects — Add Professional Visual Effects to Any Video with AI"
description: >
  Add professional visual effects to any video with AI — apply transitions, zoom effects, speed ramps, glitch effects, light leaks, particle overlays, text animations, split screens, picture-in-picture, and cinematic motion to any footage. NemoVideo applies effects through natural language: describe the effect you want and it appears on your video. No After Effects, no keyframes, no compositing skills needed. Transform ordinary footage into visually dynamic content for social media, marketing, music videos, and creative projects. Video effects AI, add effects to video, visual effects maker, video FX tool, AI video effects free, motion effects video, creative video effects.
metadata: {"openclaw": {"emoji": "✨", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

# AI Video Effects — Describe the Effect. See It Happen.

Visual effects transform ordinary footage into extraordinary content. A talking-head video with zoom-cuts every 6 seconds holds attention 40% longer than a static shot. A product reveal with a slow-motion speed ramp feels premium. A transition with a whip-pan between scenes creates energy. A text animation that builds word-by-word creates anticipation. These effects are the vocabulary of professional video — the techniques that separate content viewers watch from content viewers scroll past. Learning to apply effects in traditional software requires understanding layers, keyframes, easing curves, blend modes, masks, and rendering pipelines. Each effect in After Effects involves 5-15 steps and 10-30 minutes of work. A 60-second video with 10 effects takes 2-5 hours of effects work alone. NemoVideo applies effects through description. "Add a zoom-cut every 5 seconds" — done. "Slow-mo at the 0:15 mark for 2 seconds" — done. "Glitch transition between scenes" — done. "Particle overlay on the intro" — done. Every effect that would take 15-30 minutes in After Effects takes one sentence in NemoVideo.

## Effect Categories

### Motion Effects
- **Zoom-cuts**: Alternating focal lengths (100%/110-120%) at regular intervals — creates multi-camera illusion from single-camera footage
- **Ken Burns**: Slow zoom and pan on still images — makes photos feel cinematic
- **Parallax**: Layered depth movement on 2D images — creates 3D illusion
- **Camera shake**: Subtle handheld motion added to static shots — organic feel
- **Smooth zoom**: Gradual zoom into or out of subjects — draws attention

### Speed Effects
- **Speed ramp**: Gradual acceleration/deceleration — cinematic time control
- **Slow motion**: AI frame generation for smooth slow-mo from standard footage
- **Time-lapse**: Speed up long recordings — condense time
- **Freeze frame**: Pause on key moment with optional zoom — emphasis

### Transition Effects
- **Crossfade**: Smooth dissolve between scenes — elegant, universal
- **Whip pan**: Fast directional blur between cuts — energetic
- **Zoom transition**: Zoom into one scene, zoom out to next — seamless
- **Glitch**: Digital distortion between scenes — edgy, modern
- **Morph cut**: AI-powered seamless cut in talking-head footage — invisible edit

### Overlay Effects
- **Light leaks**: Film-style light bleeding into frame — warm, nostalgic
- **Particle effects**: Snow, rain, dust, sparks, confetti — atmosphere
- **Film grain**: Organic texture overlay — cinematic feel
- **Bokeh**: Blurred light circles — dreamy background
- **Lens flare**: Anamorphic or natural light flares — cinematic

### Text Effects
- **Word-by-word reveal**: Each word appears timed to speech — trending social style
- **Kinetic typography**: Text with motion and emphasis — music videos, promos
- **Lower-thirds**: Animated name/title bars — professional identification
- **Title cards**: Animated scene/chapter titles — structure
- **Counter animation**: Numbers building to a statistic — data impact

## Use Cases

1. **Talking-Head Upgrade — Static to Dynamic (any length)** — Raw talking-head footage is static: one angle, one frame, zero visual variety. NemoVideo transforms it: zoom-cuts every 6 seconds (100%/115% alternating), subtle camera shake for organic feel, morph cuts removing "ums" and pauses (invisible edits), lower-third with speaker name (animated slide-in), and light film grain for texture. Five effects applied from one sentence: "Make this talking-head dynamic and professional." The viewer sees a polished production; the creator filmed on one phone in one position.

2. **Product Reveal — Premium Unboxing (30-90s)** — A product being unboxed needs to feel premium. NemoVideo applies: normal speed during handling (1x), speed ramp into slow-mo at the reveal moment (1x → 0.2x snap), light leak overlay as the product catches light, subtle particle effect (dust motes in light beams), zoom into product detail (smooth 3-second zoom), and freeze frame on the hero shot with brand text overlay. Six effects that transform a phone recording into a premium brand moment.

3. **Music Video — Beat-Synced Visual Effects (2-5 min)** — A music video needs effects synced to the beat. NemoVideo: analyzes the music's beat structure, applies zoom pulses on every kick drum, glitch transitions on snare hits, speed ramps on drops (fast → slow-mo → fast), color flash effects on beat accents, and text overlays appearing on lyric emphasis. Every visual effect is synchronized to the audio — the video pulses with the music.

4. **Social Content — Scroll-Stopping First 3 Seconds (15-60s)** — The first 3 seconds of a TikTok/Reel determine if the viewer watches or scrolls. NemoVideo applies: immediate text animation (bold hook text building word-by-word), zoom-in from wide establishing shot to close-up in 1.5 seconds, subtle glitch effect for visual disruption, and bright color flash on the hook word. Four effects in 3 seconds that stop the scroll.

5. **Before/After — Transformation Reveal (15-30s)** — Fitness, beauty, home renovation, or design transformation content. NemoVideo applies: split-screen wipe (before on left, after revealed by animated wipe from left to right), freeze frame on the "before" with desaturated color grade, dramatic transition (glitch or zoom-through) to the "after" with vibrant color grade, and counter animation showing the metric ("30 days" / "-20 lbs" / "$5K budget"). The transformation effect that drives the highest engagement on social platforms.

## How It Works

### Step 1 — Upload Video
Any footage that needs effects. Phone recording, camera footage, screen capture, or existing edited video that needs enhancement.

### Step 2 — Describe Effects
Natural language: "Add zoom-cuts every 5 seconds, slow-mo at 0:15 for 2 seconds, and a glitch transition at 0:30." Or general: "Make this look cinematic and dynamic."

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "ai-video-effects",
    "prompt": "Apply effects to a 45-second product launch video. Effects: (1) Smooth zoom-in on product at 0:05 (2s zoom from wide to close), (2) Speed ramp at 0:12 — normal to 0.25x slow-mo for the reveal moment (2s), snap back to 1x, (3) Light leak overlay during the beauty shot at 0:18 (warm golden, 3s), (4) Kinetic typography for features: three feature words animate in sequence at 0:25 (bold, scale-up entrance), (5) Particle confetti burst at 0:40 for the CTA moment, (6) Film grain throughout (fine, 5%% opacity). Export 16:9 + 9:16.",
    "effects": [
      {"type": "smooth-zoom", "at": "0:05", "duration": 2, "direction": "in"},
      {"type": "speed-ramp", "at": "0:12", "speed": 0.25, "duration": 2, "curve": "snap"},
      {"type": "light-leak", "at": "0:18", "duration": 3, "color": "warm-golden"},
      {"type": "kinetic-text", "at": "0:25", "words": ["Powerful", "Portable", "Perfect"], "style": "scale-up"},
      {"type": "particles", "at": "0:40", "style": "confetti-burst"},
      {"type": "film-grain", "throughout": true, "opacity": 0.05}
    ],
    "formats": ["16:9", "9:16"]
  }'
```

### Step 4 — Preview and Adjust
Watch each effect in context. Adjust: "make the slow-mo longer," "move the light leak 2 seconds earlier," "less grain." Iterate until every effect enhances the video.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Effect descriptions in natural language |
| `effects` | array | | [{type, at, duration, style, ...}] structured effects |
| `zoom_cuts` | object | | {interval, range} for recurring zoom-cuts |
| `speed_ramp` | object | | {at, speed, duration, curve} |
| `transitions` | array | | [{type, at}] — "crossfade", "glitch", "whip-pan", "zoom" |
| `overlays` | array | | [{type, at, duration}] — "light-leak", "particles", "grain", "bokeh" |
| `text_effects` | array | | [{type, text, at, style}] |
| `beat_sync` | boolean | | Sync effects to music beats |
| `formats` | array | | ["16:9", "9:16", "1:1"] |

## Output Example

```json
{
  "job_id": "ave-20260328-001",
  "status": "completed",
  "source_duration": "0:45",
  "effects_applied": 6,
  "effects_detail": [
    {"type": "smooth-zoom", "at": "0:05", "duration": "2s"},
    {"type": "speed-ramp", "at": "0:12", "0.25x for 2s"},
    {"type": "light-leak", "at": "0:18", "warm-golden 3s"},
    {"type": "kinetic-text", "at": "0:25", "3 words"},
    {"type": "confetti-burst", "at": "0:40"},
    {"type": "film-grain", "throughout", "5%% opacity"}
  ],
  "outputs": {
    "landscape": {"file": "launch-effects-16x9.mp4", "resolution": "1920x1080"},
    "vertical": {"file": "launch-effects-9x16.mp4", "resolution": "1080x1920"}
  }
}
```

## Tips

1. **Effects should serve the content, not compete with it** — Every effect should make the viewer understand or feel something better. A zoom-cut that resets attention serves the content. A random glitch effect that distracts from the message hurts it. Apply effects with purpose.
2. **Zoom-cuts are the single highest-impact effect for talking-head content** — One effect, applied every 5-8 seconds, transforms static footage into dynamic content. If you apply only one effect to any talking-head video, make it zoom-cuts.
3. **Speed ramps create the most cinematic moments** — The snap from normal speed to slow-motion at a key moment (a product reveal, a sports highlight, a dramatic beat) is the signature technique of professional video. One speed ramp makes any video feel like a film.
4. **Light leaks and film grain add perceived production value** — These subtle overlays create organic texture that the viewer feels rather than sees. The footage feels "warmer" and "more professional" without the viewer being able to identify why.
5. **Beat-synced effects make music videos and montages addictive** — When visual effects pulse with the music, the viewer enters a flow state. The rhythm of effects + music creates a sensory experience that holds attention far longer than unsynchronized editing.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube / website |
| MP4 9:16 | 1080x1920 | TikTok / Reels / Shorts |
| MP4 1:1 | 1080x1080 | Instagram / LinkedIn |

## Related Skills

- [ai-video-filters](/skills/ai-video-filters) — Video filters
- [ai-video-loop](/skills/ai-video-loop) — Video loops
- [ai-video-rotate](/skills/ai-video-rotate) — Video rotation
