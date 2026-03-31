---
name: youtube-video-editor-ai
version: "1.0.0"
displayName: "YouTube Video Editor AI — Edit YouTube Videos, Add Chapters Thumbnails and Shorts"
description: >
  Edit YouTube videos using AI — trim, add chapters, generate thumbnails, create Shorts clips, burn subtitles, add background music, remove silences, and optimize for YouTube's algorithm in a single workflow. NemoVideo understands YouTube-specific requirements: chapter timestamps for navigation, SRT captions for search ranking, end-screen timing for subscriber conversion, Shorts extraction from long-form, and thumbnail frame selection — producing channel-ready content without switching between 5 different tools.
metadata: {"openclaw": {"emoji": "▶️", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# YouTube Video Editor AI — Edit Videos for YouTube with AI

YouTube is the second-largest search engine in the world, and every ranking signal it uses is influenced by the edit: chapters improve navigation and appear in search results, captions enable content indexing for recommendations, thumbnails determine click-through rate, silence removal improves retention graphs, and Shorts cross-promotion drives subscribers back to long-form. A creator who edits for YouTube specifically — not just edits a video and uploads it to YouTube — ranks higher, retains longer, and grows faster. But YouTube-specific editing requires juggling: the main video edit in Premiere or DaVinci, chapters manually timestamped in the description, SRT captions from a separate transcription service, thumbnail in Photoshop, and a Shorts clip re-edited vertically. Five tools, five workflows, five export-settings configurations. NemoVideo consolidates the entire YouTube production pipeline: edit the main video (silence removal, zoom-cuts, color grade, music), auto-generate chapters from transcript topic detection, produce SRT captions, select the optimal thumbnail frame, and extract the best Shorts clip — all from a single upload with a single command. The creator focuses on the content; NemoVideo handles every YouTube-specific optimization.

## Use Cases

1. **Full YouTube Edit — Talking Head (8-20 min)** — A creator records a 25-minute talking-head video. NemoVideo produces: silence removal (tightens to 17 minutes), zoom-cuts every 15 seconds for visual energy, color grade (warm and professional), background music at -20dB with speech ducking, SRT captions for YouTube's closed-caption system, auto-detected chapters (5-8 topic markers with titles), thumbnail frame selection (3 candidates ranked by visual impact and expression), and a 58-second Shorts clip from the most engaging segment with burned-in vertical captions.
2. **Tutorial with Screen Recording (10-30 min)** — A coding tutorial alternates between face-cam and screen-share. NemoVideo: switches between sources at natural transition points, adds code-zoom overlays when terminal text is too small, generates chapters at each code-section ("Setup", "Writing the Function", "Testing", "Deployment"), creates SRT for YouTube's caption system, and extracts the "aha moment" as a Shorts clip.
3. **Podcast Episode → YouTube + Shorts (30-90 min)** — A podcast episode needs both the full YouTube version and 5 Shorts clips. NemoVideo: removes all silences over 1.2 seconds, adds speaker-labeled captions, generates chapter timestamps at topic changes, and extracts the 5 highest-energy moments as standalone Shorts (9:16, 30-60 sec each, with individual hooks and captions).
4. **Vlog — Multi-Clip Assembly (10-15 min)** — 20 clips from a day need assembly into a cohesive vlog. NemoVideo: sequences chronologically, adds day/location title cards, applies consistent color grade across varied lighting conditions, underlays music that matches the energy of each section, generates chapters by location/activity, and extracts the single most visually striking moment as a Shorts clip.
5. **Evergreen Content Optimization — Existing Video Re-Edit** — A creator's 2-year-old video still gets search traffic but has no chapters, no captions, and a weak thumbnail. NemoVideo reprocesses the existing upload: generates chapter timestamps and SRT retroactively, selects a better thumbnail frame, and extracts a Shorts clip to drive new traffic to the old video. Zero re-filming needed.

## How It Works

### Step 1 — Upload Raw Footage
Provide the recording(s). NemoVideo accepts any format, any number of clips, face-cam and screen-share as separate or combined files.

### Step 2 — Define YouTube Outputs
Specify which deliverables: edited main video, chapters, SRT, thumbnail, Shorts clips, or all of them.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "youtube-video-editor-ai",
    "prompt": "Full YouTube edit of a 22-minute talking-head video about productivity systems. Remove all silences over 1 second. Add zoom-cuts every 15 seconds. Color grade: warm, clean, professional. Background music: lo-fi at -20dB with speech ducking. Generate SRT captions in English. Auto-detect chapters from transcript topic changes. Select 3 thumbnail candidates — prefer frames where I am mid-gesture with an expressive face. Extract the best 55-second segment as a Shorts clip (9:16) with burned-in word-by-word captions and a text hook from the strongest sentence.",
    "outputs": ["main-video", "chapters", "srt", "thumbnails", "shorts"],
    "silence_threshold": 1.0,
    "zoom_cuts": true,
    "color_grade": "warm-professional",
    "music": "lo-fi",
    "music_volume": "-20dB",
    "captions_language": "en",
    "shorts_count": 1,
    "shorts_duration": "55 sec",
    "thumbnail_candidates": 3,
    "format": "16:9"
  }'
```

### Step 4 — Review All Deliverables
Preview: main video edit, chapter timestamps, SRT accuracy, thumbnail options, and Shorts clip. Approve or adjust each independently.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the video and desired YouTube optimizations |
| `outputs` | array | | ["main-video","chapters","srt","thumbnails","shorts"] |
| `silence_threshold` | float | | Remove silences above N seconds (default: 1.0) |
| `zoom_cuts` | boolean | | Add zoom-cut transitions (default: true) |
| `color_grade` | string | | "warm-professional", "bright-clean", "cinematic", "none" |
| `music` | string | | "lo-fi", "corporate", "cinematic", "acoustic", "none" |
| `music_volume` | string | | "-16dB" to "-22dB" (default: "-20dB") |
| `captions_language` | string | | "en", "es", "de", "fr", "auto" |
| `shorts_count` | integer | | Number of Shorts clips to extract (default: 1) |
| `shorts_duration` | string | | "30 sec", "45 sec", "55 sec" |
| `thumbnail_candidates` | integer | | Number of thumbnail options (default: 3) |
| `format` | string | | "16:9" (YouTube standard) |

## Output Example

```json
{
  "job_id": "yvea-20260328-001",
  "status": "completed",
  "source_duration": "22:04",
  "edited_duration": "15:38",
  "outputs": {
    "main_video": {
      "file": "productivity-systems-youtube.mp4",
      "duration": "15:38",
      "resolution": "1920x1080",
      "silences_removed": "6:26 (168 cuts)",
      "zoom_cuts_added": 52
    },
    "chapters": [
      {"title": "Intro — Why Systems Beat Motivation", "timestamp": "0:00"},
      {"title": "The Capture System", "timestamp": "2:15"},
      {"title": "Processing and Organizing", "timestamp": "5:42"},
      {"title": "Weekly Review Process", "timestamp": "8:30"},
      {"title": "Tools I Actually Use", "timestamp": "11:15"},
      {"title": "Common Mistakes", "timestamp": "13:40"}
    ],
    "srt": "productivity-systems-en.srt",
    "thumbnails": [
      {"file": "thumb-1.jpg", "timestamp": "3:22", "description": "Mid-gesture, energetic expression"},
      {"file": "thumb-2.jpg", "timestamp": "8:45", "description": "Pointing at camera, confident"},
      {"file": "thumb-3.jpg", "timestamp": "12:10", "description": "Surprised expression, hand raised"}
    ],
    "shorts": [
      {"file": "shorts-best-55s.mp4", "duration": "0:55", "hook": "Stop using to-do lists — here's what actually works", "resolution": "1080x1920"}
    ]
  }
}
```

## Tips

1. **Chapters appear in YouTube search results** — A video with chapters gets clickable timestamps in Google search, increasing CTR. NemoVideo's auto-detection generates chapter titles from the transcript's topic boundaries.
2. **SRT captions improve search ranking** — YouTube indexes caption text for search. A video about "productivity systems" with an SRT containing those exact words ranks higher than one without captions, even if the spoken content is identical.
3. **Silence removal fixes the retention graph** — YouTube's algorithm penalizes videos where viewers skip forward. Long silences cause skips. Removing them produces a smooth retention curve that the algorithm rewards.
4. **The Shorts clip drives subscribers to long-form** — A well-chosen 55-second Shorts with a "full video on my channel" CTA is the most effective growth mechanism on YouTube in 2026. NemoVideo auto-selects the strongest segment.
5. **Thumbnails need expressive faces** — YouTube's own data shows that thumbnails with clear facial expressions get higher CTR than product shots or text-heavy designs. NemoVideo prioritizes frames with visible emotion and gesture.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube main video upload |
| MP4 9:16 | 1080x1920 | YouTube Shorts |
| SRT | — | YouTube closed captions |
| JPG | 1920x1080 | Thumbnail candidates |
| TXT | — | Chapter timestamps for description |

## Related Skills

- [ai-video-trimmer](/skills/ai-video-trimmer) — Trim and cut videos
- [ai-spokesperson-video](/skills/ai-spokesperson-video) — Spokesperson videos
- [ai-text-to-video-generator](/skills/ai-text-to-video-generator) — Text to video
