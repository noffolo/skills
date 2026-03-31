---
name: music-video-maker
version: "1.0.0"
displayName: "Music Video Maker — Create Music Videos with AI from Any Song or Audio Track"
description: >
  Create music videos with AI — upload a song or audio track and NemoVideo produces a complete music video with beat-synced visuals, cinematic scenes, lyric animations, transitions timed to the music, and professional color grading. Make music videos for YouTube, Spotify Canvas, TikTok, Instagram Reels, and live performance backdrops. Works for any genre: hip-hop, pop, rock, electronic, lo-fi, indie, R&B, country, and ambient. AI music video generator, make music video online, lyric video maker, visualizer video, song to video, audio to video, beat-synced video creator.
metadata: {"openclaw": {"emoji": "🎵", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Music Video Maker — Turn Any Song into a Visual Experience

A song without a video reaches ears. A song with a video reaches eyes, ears, and emotions simultaneously — and the algorithm. YouTube is the world's largest music platform by consumption hours. Spotify Canvas (the looping visual that plays during a song) increases streams by 5-20%. TikTok snippets with visuals drive 80% of music discovery for listeners under 30. Instagram Reels with synced music get 2x more shares than posts without. The music industry knows video matters, but music video production has traditionally been expensive and slow: concept development, location scouting, filming crew, talent coordination, editing, color grading, and VFX — easily $5,000-$50,000 for a professional music video, with timelines of 2-8 weeks. Independent artists, bedroom producers, and emerging bands cannot afford that. NemoVideo makes music video production accessible to any artist at any budget. Upload your track — a finished master, a rough mix, even a demo — and describe the visual concept. The AI analyzes the audio: beat detection for cut timing, energy mapping for visual intensity, chorus identification for visual climax, and mood analysis for color palette selection. Then it generates: cinematic scenes matched to the song's emotional arc, transitions synced to every beat and bar change, lyric animations timed to the vocal performance, color grading that matches the genre and mood, and export in every format from YouTube widescreen to Spotify Canvas loop.

## Use Cases

1. **Full Music Video — YouTube Release (3-5 min)** — An indie artist releases a new track and needs a YouTube music video. NemoVideo analyzes the 3:40 song: verse sections get intimate, close-feeling visuals (moody lighting, slow movement), pre-chorus builds visual energy (faster cuts, brighter colors), chorus explodes with cinematic wide shots and intense color saturation, bridge strips back to minimal visuals (single color, abstract), final chorus combines all visual elements at peak intensity. Transitions land on every beat. Color palette shifts with the emotional arc. Lyric overlays appear during key vocal phrases. A complete music video that feels directed, not generated.
2. **Lyric Video — Animated Typography (any length)** — A pop artist needs a lyric video for streaming platforms. NemoVideo generates: each line of lyrics animated with beat-synced typography (words appearing on rhythm, key words emphasized with size/color changes), visual background that evolves with the song's energy (abstract patterns for verse, geometric explosions for chorus), smooth transitions between lyrical sections, and artist branding (logo, name) on intro and outro frames. The lyric video that fans watch on repeat while learning the words.
3. **Spotify Canvas — Looping Visual (3-8 sec loop)** — An artist needs Spotify Canvas visuals for 10 tracks on their album. NemoVideo batch-generates: 10 unique 5-second looping clips, each matching the individual track's mood and energy (ambient track gets slow color wash, upbeat track gets rhythmic particle animation, acoustic track gets warm light flicker). Each loop is seamless — the last frame connects perfectly to the first. 10 Spotify Canvas visuals from one album upload.
4. **TikTok/Reels — Song Promo Clip (15-30s)** — An artist wants to promote a new single on TikTok. NemoVideo: selects the catchiest 20-second segment (usually the chorus or hook), creates high-energy vertical visuals synced to the hook, adds animated lyric overlay for singalong potential, optimizes for TikTok's audio-driven algorithm (visual energy peaks when the audio peaks), and exports 9:16 with a "Full song on Spotify" text CTA. The promotional clip designed to make the song go viral.
5. **Live Performance Backdrop — Visual Set (full song)** — A DJ or band needs visuals for a live show. NemoVideo generates: full-length visual set synced to the track's BPM, abstract visuals that intensify with the music's energy (geometric patterns, color waves, particle systems), no text or lyrics (clean background visuals), high-contrast design optimized for projection on stage screens, and seamless loop points for extended live performance. Stage-ready visuals from a studio track.

## How It Works

### Step 1 — Upload Your Audio
Upload the track: MP3, WAV, FLAC, AAC, or any audio format. NemoVideo analyzes: BPM, key, energy map, structure (verse/chorus/bridge), mood, and vocal timing.

### Step 2 — Describe the Visual Concept
Describe the mood, style, or specific scenes you want. Or let the AI choose based on the audio analysis.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "music-video-maker",
    "prompt": "Create a full music video for a 3:40 indie pop track. Visual concept: urban night scenes, neon lights, rain-soaked streets, a lone figure walking through the city. Verse: intimate close shots, warm streetlight tones, slow movement. Chorus: wide city panoramas, neon color explosions, fast cuts on every beat. Bridge: abstract single-color wash, minimal. Final chorus: all elements combined at maximum intensity. Lyric overlay on chorus sections only. Color palette: neon blue, warm amber, deep purple. Export 16:9 for YouTube + 9:16 30-sec promo for TikTok.",
    "video_type": "full-music-video",
    "visual_style": "cinematic-urban-night",
    "color_palette": ["#00D4FF", "#FFB347", "#7B2D8E"],
    "lyrics_display": "chorus-only",
    "beat_sync": true,
    "formats": ["16:9", "9:16"],
    "tiktok_promo": {"duration": "30 sec", "section": "chorus"}
  }'
```

### Step 4 — Review and Release
Preview the full video synced to the track. Adjust: scene selection, color intensity, lyric timing. Export and upload to YouTube, distribute to streaming platforms, post TikTok promo.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Visual concept and production requirements |
| `video_type` | string | | "full-music-video", "lyric-video", "visualizer", "spotify-canvas", "live-backdrop" |
| `visual_style` | string | | "cinematic-urban", "abstract-geometric", "nature", "animated", "minimal" |
| `color_palette` | array | | Hex colors for the visual theme |
| `lyrics` | string | | Full lyrics text (for lyric video/overlay) |
| `lyrics_display` | string | | "full", "chorus-only", "key-phrases", "none" |
| `beat_sync` | boolean | | Sync cuts and transitions to beats (default: true) |
| `formats` | array | | ["16:9", "9:16", "1:1", "spotify-canvas"] |
| `tiktok_promo` | object | | {duration, section} for short promo clip |
| `batch_tracks` | array | | Multiple tracks for album/EP visual set |

## Output Example

```json
{
  "job_id": "mvm-20260328-001",
  "status": "completed",
  "audio_analysis": {
    "duration": "3:40",
    "bpm": 118,
    "key": "C minor",
    "structure": ["intro 0:00", "verse1 0:12", "chorus1 0:58", "verse2 1:42", "chorus2 2:28", "bridge 3:02", "outro 3:24"],
    "mood": "melancholic-hopeful"
  },
  "outputs": {
    "music_video_16x9": {
      "file": "music-video-16x9.mp4",
      "resolution": "1920x1080",
      "duration": "3:40",
      "scenes": 28,
      "beat_synced_cuts": 142,
      "lyrics_overlay": "chorus sections"
    },
    "tiktok_promo_9x16": {
      "file": "promo-9x16.mp4",
      "resolution": "1080x1920",
      "duration": "0:30",
      "section": "chorus1 (0:58-1:28)"
    }
  }
}
```

## Tips

1. **Beat-synced cuts are what make AI music videos feel professional** — Random cuts look amateur. Cuts landing exactly on the beat (kick, snare, hi-hat) create the visceral music-visual connection that makes music videos feel intentional and directed.
2. **Visual energy should mirror audio energy** — Quiet verse = slow movement, muted colors, close shots. Loud chorus = fast cuts, saturated colors, wide shots. This emotional mirroring is what separates a music video from a slideshow with music.
3. **Lyric videos outperform non-lyric versions for new releases** — Fans want to learn the words. A lyric video on release day gets 2-3x more views in the first week than a visualizer without lyrics.
4. **Spotify Canvas increases stream counts by 5-20%** — The 5-second looping visual catches attention while users browse. Artists with Canvas enabled see measurably more plays than those without. It is the lowest-effort, highest-impact music visual.
5. **TikTok promo should use the catchiest 15-20 seconds** — The segment that gets stuck in someone's head. Usually the chorus hook. High-energy visuals synced to this segment create the "I need to find this song" moment that drives streams.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube music video |
| MP4 9:16 | 1080x1920 | TikTok / Reels promo |
| MP4 1:1 | 1080x1080 | Instagram / Facebook |
| MP4 loop | 1080p | Spotify Canvas (3-8 sec) |
| MOV (ProRes) | 4K | Live performance projection |

## Related Skills

- [video-editor-japonais](/skills/video-editor-japonais) — Japanese video editor
- [video-enhancer-ai](/skills/video-enhancer-ai) — AI video enhancement
