---
name: ai-video-subtitle-editor
version: "1.0.0"
displayName: "AI Video Subtitle Editor — Create Edit and Style Subtitles for Any Video with AI"
description: >
  Create, edit, and style subtitles for any video with AI — auto-transcribe speech to text, translate subtitles to 50+ languages, style with custom fonts and colors, position anywhere on screen, and sync perfectly to speech timing. NemoVideo transcribes audio with word-level timing accuracy, then lets you edit text, adjust timing, choose from cinematic subtitle styles (TikTok animated, Netflix minimal, YouTube pop-up, karaoke highlight), and export with subtitles rendered directly in the video. Subtitle editor AI, add subtitles to video, video caption editor, subtitle maker, auto subtitle generator, subtitle styling tool, video text editor, translate subtitles AI.
metadata: {"openclaw": {"emoji": "📝", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# AI Video Subtitle Editor — Transcribe, Style, Translate, and Perfect Every Word on Screen

Subtitles are no longer optional. 85% of Facebook videos are watched without sound. TikTok and Instagram Reels autoplay muted by default. LinkedIn video starts silent in the feed. YouTube data shows that subtitled videos get 7-10% more watch time because viewers who might otherwise scroll past will stop and read. Accessibility regulations increasingly require captions for professional and educational content. Subtitles have evolved from an accessibility accommodation to a primary content consumption mode. The challenge is not whether to add subtitles — it is how to add them well. Auto-generated captions from most platforms are serviceable but ugly: small white text, poor timing, frequent errors, no style. Professional subtitles require: accurate transcription, precise word-level timing, readable fonts and colors, strategic positioning that does not block important visual elements, and stylistic choices that match the content's brand and energy. NemoVideo handles the entire subtitle workflow. AI transcription with 98%+ accuracy, word-level timing synchronization, 50+ language translation, and a library of subtitle styles from minimal cinema to animated TikTok. Edit any word, adjust any timing, change any style — then export with subtitles rendered cleanly into the video.

## Use Cases

1. **Auto-Transcribe and Style — Complete Subtitle Workflow (any length)** — A 15-minute YouTube video needs professional subtitles. NemoVideo: transcribes the entire audio track with 98%+ accuracy, aligns each word to its exact spoken moment (word-level sync, not sentence-level), applies the creator's chosen style (font, size, color, background, position, animation), handles multiple speakers (different colors per speaker), and renders subtitles directly into the video. From raw video to professionally subtitled content in one step.

2. **TikTok Animated Captions — Viral Subtitle Style (15-60s)** — Short-form content needs the animated caption style that dominates TikTok: large bold text, word-by-word highlight animation (each word pops as it is spoken), bright colors with dark outlines, centered on screen. NemoVideo: applies the exact TikTok caption aesthetic — word-by-word animation synced to speech, bold sans-serif font, customizable highlight color (yellow, green, pink), positioned in the center-upper third of the frame. The subtitle style that is proven to increase watch time on short-form platforms.

3. **Multi-Language Translation — One Video, Global Audience (any length)** — A course creator's English video needs subtitles in Spanish, Portuguese, Japanese, Korean, and Arabic. NemoVideo: transcribes the English audio, translates to all 5 languages with context-aware AI (not word-by-word dictionary translation), adjusts subtitle timing for each language (some languages use more/fewer words for the same meaning), handles right-to-left text for Arabic (proper RTL rendering), and exports 5 subtitle versions. One production, five markets.

4. **Subtitle Editing — Fix and Refine Existing Captions (any length)** — An auto-generated transcript has errors: proper nouns misspelled, technical terms wrong, timing slightly off. NemoVideo: imports the existing subtitle file, highlights low-confidence words (likely errors), provides an editing interface for text and timing corrections, and re-renders with the corrected subtitles. Fixing a 90%-accurate auto-transcript to 100% instead of transcribing from scratch.

5. **Karaoke Style — Lyrics Display for Music Content (any length)** — A music video or lyric video needs karaoke-style subtitles: each word or syllable highlights in sequence as the music plays, creating a follow-along reading experience. NemoVideo: aligns lyrics to the audio with syllable-level timing (not just word-level), applies karaoke highlight animation (color change sweeps across each word as it is sung), styles with the music's aesthetic (genre-appropriate fonts, colors matching the album art), and renders the sing-along visual. Music content that invites audience participation.

## How It Works

### Step 1 — Upload Video
Any video with speech, music, or both. NemoVideo auto-detects language and speaker count.

### Step 2 — Choose Subtitle Style and Language
Select: style preset (minimal, TikTok animated, Netflix, karaoke, custom), languages, positioning, and font options.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "ai-video-subtitle-editor",
    "prompt": "Add animated TikTok-style captions to a 45-second motivational speaking clip. Word-by-word highlight animation — each word pops in bright yellow as it is spoken. Bold sans-serif font, black outline, centered in upper-third of frame. Also generate Spanish and Portuguese subtitle versions with the same style. Export all three at 9:16 for Reels and TikTok.",
    "transcribe": true,
    "style": "tiktok-animated",
    "highlight_color": "#FFD700",
    "font": "bold-sans-serif",
    "outline": "black",
    "position": "upper-third-center",
    "languages": ["en", "es", "pt"],
    "format": "9:16"
  }'
```

### Step 4 — Review and Edit
Preview subtitles over video. Edit any word, adjust any timing, change any style parameter. Re-render with changes.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Subtitle requirements |
| `style` | string | | "minimal", "tiktok-animated", "netflix", "karaoke", "custom" |
| `font` | string | | Font family or preset |
| `highlight_color` | string | | Color for word-by-word animation |
| `outline` | string | | Outline color and width |
| `position` | string | | "bottom", "upper-third", "center", "custom" |
| `languages` | array | | ["en", "es", "ja", "ko", "ar", ...] |
| `transcribe` | boolean | | Auto-transcribe audio |
| `import_srt` | string | | URL to existing subtitle file |
| `speakers` | object | | {differentiate: true, colors: {"Speaker 1": "#fff"}} |
| `format` | string | | "16:9", "9:16", "1:1" |

## Output Example

```json
{
  "job_id": "avsub-20260328-001",
  "status": "completed",
  "transcription": {
    "language": "en",
    "confidence": 0.98,
    "words": 312,
    "speakers_detected": 1
  },
  "translations": ["es", "pt"],
  "style": "tiktok-animated",
  "outputs": {
    "en": {"file": "video-subtitled-en-9x16.mp4"},
    "es": {"file": "video-subtitled-es-9x16.mp4"},
    "pt": {"file": "video-subtitled-pt-9x16.mp4"}
  }
}
```

## Tips

1. **Word-level sync is what separates professional from amateur subtitles** — Sentence-level timing (entire sentence appears at once) feels disconnected from speech. Word-level timing (each word appears as spoken) creates a reading experience that matches the audio precisely. Always use word-level sync.
2. **TikTok animated style increases short-form watch time measurably** — The large, bold, animated captions are not just aesthetic — they hold attention by giving the viewer an active reading task synchronized with audio. Dual-channel engagement (reading + listening) reduces scroll-away.
3. **Translation timing must adjust, not just translate** — German uses 30% more words than English for the same meaning. Japanese uses fewer characters. Subtitle timing must expand or contract for each language, not just swap text at the same timestamps.
4. **Position subtitles in platform safe zones** — TikTok's bottom 15% is covered by UI. YouTube's bottom area has progress bar and controls. Subtitles at the very bottom of the frame are often partially or fully hidden on the platforms where they matter most.
5. **Speaker differentiation prevents confusion in multi-person content** — Color-coding speakers (Speaker A: white, Speaker B: yellow) instantly communicates who is speaking without needing "Speaker A:" labels that waste screen space and reading time.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube / website |
| MP4 9:16 | 1080x1920 | TikTok / Reels / Shorts |
| MP4 1:1 | 1080x1080 | Instagram / LinkedIn |

## Related Skills

- [ai-video-highlight-maker](/skills/ai-video-highlight-maker) — Highlight reels
- [ai-video-intro-maker](/skills/ai-video-intro-maker) — Video intros
- [ai-video-speed-changer](/skills/ai-video-speed-changer) — Speed changes
