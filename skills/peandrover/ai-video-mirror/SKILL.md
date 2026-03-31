---
name: ai-video-mirror
version: 1.0.1
displayName: "AI Video Mirror — Mirror Flip and Create Reflection Effects in Videos with AI"
description: >
  Mirror, flip, and create reflection effects in videos with AI — horizontal mirror for selfie text correction, vertical mirror for creative effects, split-screen mirror for symmetry content, kaleidoscope effects, and animated mirror transitions. NemoVideo handles mirror operations intelligently: fixing selfie-camera mirrored text while preserving natural appearance, creating artistic mirror compositions, and producing the satisfying symmetry content that dominates social media. Mirror video online, flip video horizontally, video mirror effect, reverse video mirror, symmetry video maker, mirror image video, selfie mirror fix.
metadata: {"openclaw": {"emoji": "🪞", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
---

# AI Video Mirror — Reflections, Corrections, and Symmetry That Captivates

Mirror operations in video serve two purposes: correction and creation. Correction: front-facing camera recordings produce mirrored output where text appears backwards, logos are reversed, and the visual world is flipped from reality. This needs fixing. Creation: mirror effects produce mesmerizing visual content — symmetrical compositions, kaleidoscope patterns, split-screen reflections, and the hypnotic mirror-world aesthetic that stops social media scrollers. Both purposes are served by the same underlying operation (horizontal or vertical pixel flipping) but with very different creative intentions. NemoVideo handles mirror operations from simple corrections to complex creative effects. A selfie video with backwards whiteboard text gets a clean horizontal flip. A landscape shot gets a split-screen mirror that creates impossible symmetry. A dance video gets a kaleidoscope effect that turns movement into geometric art.

## Use Cases

1. **Selfie Text Fix — Mirror Correction (any length)** — A teacher records a lesson on their phone's front-facing camera while pointing at a whiteboard. All text on the whiteboard appears backwards. NemoVideo: applies horizontal mirror (flipping the entire frame), correcting all text to read normally, while the teacher's face appears naturally (viewers do not notice mirrored faces — they absolutely notice mirrored text). The tutorial becomes usable.

2. **Symmetry Content — Split-Screen Mirror (15-60s)** — A nature photographer captures a lake reflection. NemoVideo creates a perfect split-screen mirror: the top half shows the original landscape, the bottom half is a mirrored reflection, creating impossible perfect symmetry (even the real reflection in the lake is never this perfect). The result: a surreal, mesmerizing visual that stops scrolling. Symmetry content consistently performs 2-3x above average engagement on Instagram and TikTok because the human brain is wired to find perfect symmetry deeply satisfying.

3. **Dance Mirror — Choreography Learning Tool (any length)** — A dance instructor records a tutorial facing the camera. Students learning from the video need a mirrored version so their left matches the instructor's left (when facing someone, their left is your right). NemoVideo: creates a mirrored version alongside the original, so students can choose the perspective that matches their learning preference. The mirrored dance tutorial that every dance instructor should provide.

4. **Kaleidoscope Effect — Artistic Content (15-60s)** — A creator films close-up footage of flowers, water, or abstract textures. NemoVideo applies a kaleidoscope effect: the frame is divided into segments that mirror and repeat, creating geometric patterns that shift as the source footage moves. The result: hypnotic, endlessly engaging visual art from simple footage. Kaleidoscope content is shareable precisely because it transforms the mundane into the extraordinary.

5. **Before/After Mirror — Side-by-Side Comparison (15-30s)** — Fitness, beauty, or renovation content showing transformation. NemoVideo: places the "before" on the left and a mirrored "after" on the right (mirrored so both subjects face center, creating visual balance), adds a center divider line, and optionally animates the divider sliding from left to right to reveal the transformation. The professional before/after format used by every transformation-based content creator.

## How It Works

### Step 1 — Upload Video
Any footage that needs mirroring — for correction or creative purposes.

### Step 2 — Choose Mirror Type
Horizontal flip (selfie fix), vertical flip, split-screen mirror, kaleidoscope, or animated mirror transition.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "ai-video-mirror",
    "prompt": "Create two versions of a dance tutorial video: (1) Original as-filmed (for reference), (2) Horizontally mirrored version (so students can follow as if looking in a mirror — their left matches the instructor left). Also create a 15-second symmetry highlight clip: take the most visually striking 15 seconds of choreography and apply split-screen vertical mirror (left half original, right half mirrored, creating perfect bilateral symmetry). Export all at 9:16 for TikTok.",
    "outputs": [
      {"type": "original", "format": "9:16"},
      {"type": "horizontal-mirror", "format": "9:16", "label": "Mirror Version — Follow Along"},
      {"type": "split-mirror", "format": "9:16", "axis": "vertical", "duration": "15s", "segment": "most-dynamic"}
    ]
  }'
```

### Step 4 — Review and Publish
Verify: mirrored text reads correctly, mirrored movement matches expectations, creative effects achieve desired visual impact. Download all versions.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Mirror operation description |
| `mirror_type` | string | | "horizontal", "vertical", "split-screen", "kaleidoscope", "animated" |
| `axis` | string | | "horizontal", "vertical" — for split-screen mirror |
| `kaleidoscope` | object | | {segments: 4/6/8, rotation: true} |
| `animated` | object | | {from: "normal", to: "mirrored", duration} |
| `outputs` | array | | [{type, format, label}] multiple versions |
| `format` | string | | "16:9", "9:16", "1:1" |

## Output Example

```json
{
  "job_id": "avm-20260328-001",
  "status": "completed",
  "outputs": {
    "original": {"file": "dance-original-9x16.mp4", "mirror": "none"},
    "mirrored": {"file": "dance-mirrored-9x16.mp4", "mirror": "horizontal"},
    "symmetry_clip": {"file": "dance-symmetry-9x16.mp4", "effect": "split-vertical-mirror", "duration": "0:15"}
  }
}
```

## Tips

1. **Mirror for text correction is always worth doing** — Backwards text in a selfie video is immediately noticeable and permanently distracting. The 2-second mirror operation saves the entire recording.
2. **Symmetry content is inherently scroll-stopping** — The human brain processes symmetrical patterns faster and finds them more aesthetically pleasing than asymmetric content. Perfect symmetry in nature is rare — in video, it is captivating.
3. **Dance tutorials should always offer a mirrored version** — Students overwhelmingly prefer mirror-view tutorials where their left matches the instructor's left. Offering both versions doubles the tutorial's usefulness.
4. **Kaleidoscope effects work best with close-up movement** — Water, flowers, fabric, paint, and abstract textures produce the most visually stunning kaleidoscopes. Wide shots with too much detail create visual noise rather than beauty.
5. **Animated mirror transitions create engagement hooks** — A video that starts normal and transitions to mirrored (or vice versa) in the first 2 seconds creates a visual surprise that stops the scroll. Use animated mirror as a hook technique.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p | YouTube / website |
| MP4 9:16 | 1080x1920 | TikTok / Reels / Shorts |
| MP4 1:1 | 1080x1080 | Instagram |
| GIF | 720p | Preview / social share |

## Related Skills

- [ai-video-flip](/skills/ai-video-flip) — Flip video
- [ai-video-speed-changer](/skills/ai-video-speed-changer) — Speed changes
- [ai-video-zoom](/skills/ai-video-zoom) — Zoom effects
