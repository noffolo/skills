---
name: ai-video-trimmer
version: "1.0.0"
displayName: "AI Video Trimmer — Trim Cut and Shorten Videos Intelligently with AI"
description: >
  Trim, cut, and shorten videos intelligently with AI — remove unwanted sections, cut dead air, trim beginnings and endings, extract the best segments, and tighten pacing automatically. NemoVideo goes beyond simple timestamp cutting: AI analyzes content to find natural cut points, removes silences and filler words, detects the strongest segments worth keeping, and produces cleanly trimmed video with smooth transitions at every edit point. Trim video online, cut video AI, shorten video, video cutter, remove silence from video, trim video automatically, AI video cutter free, smart video trimmer.
metadata: {"openclaw": {"emoji": "✂️", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# AI Video Trimmer — Cut the Fat. Keep the Gold.

Every raw video is longer than it should be. A talking-head recording has 20-35% dead air (pauses, silences between thoughts). A meeting recording has 10-15 minutes of "can everyone hear me" at the start. A phone recording has shaky seconds at the beginning and end. A tutorial has repeated takes and false starts. A lecture has off-topic tangents. A stream has low-energy periods between highlights. The valuable content is buried inside unnecessary length. Traditional trimming requires scrubbing through the entire video, identifying every cut point manually, setting in-and-out markers, and ensuring cuts do not land mid-word or mid-action. For a 30-minute video, manual trimming takes 30-60 minutes. NemoVideo trims intelligently. The AI understands content — not just waveforms. It removes silences based on configurable thresholds. It detects filler words ("um," "uh," "you know," "like") and removes them without disrupting speech flow. It identifies the strongest segments by energy, information density, and engagement potential. It finds natural cut points where transitions feel invisible. Every trim is executed with optional crossfade to smooth the edit.

## Use Cases

1. **Talking-Head Tightening — Remove Dead Air (any length)** — A creator records 25 minutes of raw content. NemoVideo: removes all silences over 0.7 seconds (saves 6 minutes), removes filler words — "um" "uh" "like" "you know" (saves 2 minutes), trims the 45-second intro where the creator adjusts the camera, trims the 30-second ending where they reach for the stop button, and produces a tight 16-minute video. Natural speech rhythm is preserved (short pauses under 0.7s remain for breathing room), but every moment of dead air is gone. The video feels energetic and intentional without sounding unnaturally fast.

2. **Meeting Cleanup — Extract the Useful Parts (30-90 min)** — A 60-minute Zoom recording needs to become a 15-minute highlights version for stakeholders who did not attend. NemoVideo: trims the 4-minute "waiting for people to join" start, removes the 8-minute tangent about someone's weekend, cuts the 5-minute technical difficulties in the middle, extracts the 3 key discussion segments (budget review, timeline update, decision items), and produces a 15-minute cleaned version with chapter markers. Stakeholders get the substance without the filler.

3. **Smart Duration Targeting — Hit a Specific Length (any source)** — A creator has 8 minutes of content that needs to be 60 seconds for TikTok. NemoVideo: analyzes all 8 minutes for the single strongest 60-second segment (highest energy, most complete thought, best hook potential), extracts it with clean entry and exit points, trims any internal silences to maximize content density within the 60 seconds, reframes to vertical, adds captions, and exports. Eight minutes intelligently compressed to the best possible 60 seconds — not the first 60 seconds, not random 60 seconds, the best 60 seconds.

4. **Batch Trim — Multiple Videos at Once (multiple files)** — A course creator has 20 lecture recordings, each 45-60 minutes, each with 5-10 minutes of unnecessary content (setup, tangents, repeated explanations). NemoVideo batch-processes all 20: applies consistent trimming rules (remove silences > 1s, trim first/last 30s of each, remove detected tangents), produces cleaned versions, and reports what was removed from each. Twenty hours of raw lectures become 16 hours of tight content in one operation.

5. **Precision Trim — Remove Specific Sections (any length)** — A corporate video has a 15-second section where a presenter accidentally reveals confidential information. NemoVideo: cuts exactly that section (by timestamp or by content description — "remove the part where she mentions the acquisition"), applies a smooth crossfade at the edit point so the cut is invisible, verifies the audio transition sounds natural, and exports. Surgical content removal without re-recording.

## How It Works

### Step 1 — Upload Video
Any video with content that needs trimming. Any length, any format.

### Step 2 — Define Trim Rules
Automatic (AI decides what to cut based on silence/filler/energy analysis), manual (specify timestamps), target-based (reach a specific duration), or combined.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "ai-video-trimmer",
    "prompt": "Trim a 22-minute talking-head video. Remove: all silences over 0.7 seconds, all filler words (um, uh, like, you know), the first 40 seconds (camera setup), the last 25 seconds (reaching to stop recording). Add 0.3s crossfade at each cut point for smooth transitions. Add fade-in at new start and fade-out at new end. Also identify the single best 45-second segment for a TikTok clip. Export main at 16:9, clip at 9:16 with word-by-word captions (white, #FFD700 gold highlight, pill-dark bg).",
    "trim_rules": {
      "silence_threshold": 0.7,
      "filler_removal": true,
      "trim_start": "0:40",
      "trim_end": "last 25s",
      "crossfade": 0.3,
      "fade_in": true,
      "fade_out": true
    },
    "best_clip": {"duration": "45s", "format": "9:16", "captions": {"style": "word-highlight", "text": "#FFFFFF", "highlight": "#FFD700", "bg": "pill-dark"}},
    "format": "16:9"
  }'
```

### Step 4 — Review Trims
Preview: verify no content was incorrectly cut, transitions sound natural, pacing feels right. Download trimmed video and clip.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Trimming instructions |
| `trim_rules` | object | | {silence_threshold, filler_removal, trim_start, trim_end, crossfade} |
| `target_duration` | string | | "60 sec", "5 min", "15 min" — AI trims to target |
| `remove_sections` | array | | [{start, end}] or [{description}] — specific cuts |
| `keep_sections` | array | | [{start, end}] — only keep these segments |
| `best_clip` | object | | {duration, format, captions} — extract best segment |
| `fade_in` | boolean | | Fade in at video start |
| `fade_out` | boolean | | Fade out at video end |
| `batch` | array | | Multiple videos with same rules |

## Output Example

```json
{
  "job_id": "avt-20260328-001",
  "status": "completed",
  "source_duration": "22:15",
  "trimmed_duration": "15:42",
  "time_saved": "6:33 (29%%)",
  "trims_applied": {
    "silences_removed": "4:12 (98 cuts)",
    "fillers_removed": "1:16 (47 instances)",
    "start_trimmed": "0:40",
    "end_trimmed": "0:25",
    "crossfades": 145
  },
  "outputs": {
    "main_video": {"file": "trimmed-16x9.mp4", "duration": "15:42", "resolution": "1920x1080"},
    "best_clip": {"file": "best-moment-9x16.mp4", "duration": "0:44", "timestamp": "8:22-9:06", "captions": "word-highlight"}
  }
}
```

## Tips

1. **0.7-second silence threshold preserves natural rhythm** — Shorter thresholds (0.3-0.5s) make speech feel rushed and robotic. Longer thresholds (1.0s+) leave noticeable pauses. 0.7 seconds removes dead air while keeping the natural breathing rhythm that makes speech sound human.
2. **Filler removal is the edit viewers notice most** — A speaker who says "um" 40 times in 20 minutes sounds uncertain. The same content with fillers removed sounds confident and polished. Filler removal changes the perceived quality of the speaker, not just the video.
3. **Crossfade at every cut point prevents audio pops** — A hard cut in the middle of ambient room tone creates an audible pop or gap. A 0.2-0.3 second crossfade smooths every transition so cuts are imperceptible to the viewer.
4. **Target-duration trimming finds the best content, not just shorter content** — When you need 60 seconds from 8 minutes, the AI evaluates all possible 60-second windows and selects the one with highest engagement potential. This is fundamentally different from cutting the first 7 minutes.
5. **Batch trimming with consistent rules ensures uniform quality** — When processing a content series (course modules, podcast episodes, meeting recordings), applying the same trim rules to all videos produces consistent pacing and quality across the entire series.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube / website |
| MP4 9:16 | 1080x1920 | TikTok / Reels / Shorts |
| MP4 1:1 | 1080x1080 | Instagram / LinkedIn |

## Related Skills

- [ai-video-merger](/skills/ai-video-merger) — Merge videos
- [video-maker-ai](/skills/video-maker-ai) — AI video maker
- [ai-clip-maker](/skills/ai-clip-maker) — Clip extraction
