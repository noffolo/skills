---
name: ai-video-content-creator
version: "1.0.0"
displayName: "AI Video Content Creator — Plan, Script, Produce and Publish Videos with AI"
description: >
  Plan, script, produce, and optimize video content using AI — the complete content creator workflow from idea to published video. NemoVideo handles every stage: topic research and ideation based on trending searches, script writing optimized for retention, visual production with AI-generated scenes, voiceover narration, music and sound design, subtitle generation, thumbnail creation, SEO title and description writing, and multi-platform export — replacing the 10-tool creator stack with a single AI-powered pipeline.
metadata: {"openclaw": {"emoji": "🚀", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# AI Video Content Creator — The Complete Video Production Pipeline

Content creators in 2026 juggle 8-12 tools per video: a research tool for topic validation, a writing app for the script, an AI for thumbnail concepts, editing software for the video, a transcription service for captions, a music library for background tracks, a scheduling tool for publishing, and an analytics platform for performance tracking. Each tool has its own subscription ($10-55/month each), its own learning curve, its own export format, and its own workflow. Switching between them wastes 30-40% of production time on file transfers, format conversions, and context switching. A single YouTube video touches 5 different software applications before it's uploaded. NemoVideo consolidates the entire creator workflow into one pipeline. Start with a topic or idea — the AI researches trending angles, writes a retention-optimized script, produces the video (visuals, narration, music, captions), generates thumbnails, writes the SEO-optimized title and description, and exports for every target platform. The creator's job shifts from operating tools to making creative decisions: "yes, that angle" / "change the music" / "make the thumbnail bolder." The production machinery runs itself.

## Use Cases

1. **Full YouTube Pipeline — Idea to Upload (any length)** — A creator says: "Make a video about why most productivity systems fail." NemoVideo: researches trending angles (identifies "second brain" and "digital minimalism" as high-search-volume related concepts), writes a 2,000-word script with hook-first structure and retention-optimized pacing, produces the video with AI visuals and narration, generates 3 thumbnail candidates, writes an SEO title ("Why Every Productivity System Fails (And What Actually Works)"), writes a 500-word description with keywords and chapters, generates SRT captions, and exports 16:9 for YouTube plus a 55-second Shorts clip. The creator's entire production pipeline in one session.
2. **Content Calendar — Weekly Batch Production (5-7 videos)** — A creator needs 5 videos for the week. NemoVideo: generates 5 topic ideas based on the channel's niche and trending searches, writes scripts for all 5, produces all 5 videos with unique visual treatments, generates thumbnails and SEO metadata for each, and exports everything. A week of content produced in one batch — the creator reviews and approves instead of producing.
3. **Repurpose Engine — One Video → 5 Platforms** — A creator has one 10-minute YouTube video that needs to reach TikTok, Instagram, LinkedIn, Twitter, and their blog. NemoVideo: extracts 3 Shorts clips (9:16) for TikTok/Reels/Shorts, creates a 60-second LinkedIn version with professional captions, generates a 30-second Twitter teaser, produces a blog post transcript with embedded video, and creates 5 Instagram carousel frames from key points. One video becomes 12 pieces of cross-platform content.
4. **Niche Research — Find Winning Topics** — A new creator in the personal finance niche doesn't know what to make. NemoVideo: analyzes search trends, identifies low-competition high-search topics ("investing $100/month at 25" has high search volume but few quality videos), generates 10 ranked topic suggestions with estimated view potential, and produces the top-ranked topic as a complete video. Data-driven content strategy without manual research.
5. **A/B Testing — Thumbnail and Title Optimization** — A creator's video is underperforming on CTR. NemoVideo: generates 5 alternative thumbnails (different expressions, colors, text overlays), writes 5 alternative titles (curiosity-gap, how-to, listicle, question, controversial), and recommends the combination most likely to increase CTR based on the niche's top-performing patterns. Optimization without guesswork.

## How It Works

### Step 1 — Start with an Idea (or Nothing)
Provide: a specific topic, a rough idea, a content niche, or just "suggest something." NemoVideo works with whatever level of input you have.

### Step 2 — Define the Pipeline
Choose which stages to run: research → script → produce → thumbnails → SEO → export, or any subset. Skip stages you want to handle yourself.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "ai-video-content-creator",
    "prompt": "Full pipeline: create a YouTube video about why most people fail at meal prep. Research trending angles. Write a script with a strong hook (controversial or surprising). Produce the video: faceless style with stock footage, warm female narrator, lo-fi music at -20dB. Generate 3 thumbnails (food photography style with bold text). Write SEO title and description. Generate SRT. Export 16:9 1080p main video + 55-sec Shorts + 3 Instagram carousel frames summarizing key points.",
    "pipeline": ["research", "script", "produce", "thumbnails", "seo", "export"],
    "style": "faceless-stock",
    "narrator": "warm-female",
    "music": "lo-fi",
    "music_volume": "-20dB",
    "thumbnails": 3,
    "exports": ["youtube-16:9", "shorts-55s", "instagram-carousel"],
    "subtitles": "burned-in"
  }'
```

### Step 4 — Review Each Stage
Review: script quality, video production, thumbnail options, SEO metadata. Approve or adjust each independently. Upload when satisfied.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Topic/idea and pipeline instructions |
| `pipeline` | array | | Stages: ["research","script","produce","thumbnails","seo","export"] |
| `style` | string | | "faceless-stock", "talking-head", "cinematic", "animated", "mixed" |
| `narrator` | string | | Voice selection for production |
| `music` | string | | Music mood for production |
| `music_volume` | string | | "-14dB" to "-22dB" |
| `thumbnails` | integer | | Number of thumbnail variants (default: 3) |
| `seo_style` | string | | "curiosity-gap", "how-to", "listicle", "question", "mixed" |
| `subtitles` | string | | "burned-in", "srt", "none" |
| `exports` | array | | Platform-specific exports |
| `batch_topics` | array | | Multiple topics for weekly batch |

## Output Example

```json
{
  "job_id": "avcc-20260328-001",
  "status": "completed",
  "pipeline_results": {
    "research": {
      "topic": "Why Most People Fail at Meal Prep",
      "trending_angle": "meal prep burnout — why the Sunday prep culture is unsustainable",
      "search_volume": "high",
      "competition": "medium"
    },
    "script": {
      "word_count": 1842,
      "hook": "Meal prep is a scam — and I can prove it in 60 seconds",
      "structure": "hook → 5 failure reasons → the alternative approach → CTA",
      "estimated_duration": "11:20"
    },
    "production": {
      "duration": "11:18",
      "scenes": 24,
      "narrator": "warm-female",
      "resolution": "1920x1080"
    },
    "thumbnails": [
      {"file": "thumb-1.jpg", "style": "rotting meal prep containers with bold 'STOP' text"},
      {"file": "thumb-2.jpg", "style": "split: perfect meal prep vs reality"},
      {"file": "thumb-3.jpg", "style": "trash can full of meal prep with shocked emoji"}
    ],
    "seo": {
      "title": "Stop Meal Prepping (Do This Instead) — Why Sunday Prep Culture is Failing You",
      "description": "500 words with keywords, chapters, and hashtags",
      "tags": ["meal prep", "meal prep fail", "cooking tips", "healthy eating", "food waste"]
    },
    "exports": {
      "youtube": "11:18 16:9 1080p",
      "shorts": "0:55 9:16 1080x1920",
      "instagram_carousel": "5 frames 1080x1080"
    }
  }
}
```

## Tips

1. **The research stage prevents wasted production** — Producing a video on a topic nobody searches for wastes 100% of the effort. Research-first identifies topics with demand before committing production resources.
2. **Hook-first scripts outperform chronological scripts** — Opening with the conclusion or most controversial claim ("Meal prep is a scam") creates a curiosity gap that drives retention through the explanation. NemoVideo writes hooks that generate this gap.
3. **Three thumbnails give you options, not decisions** — Testing multiple thumbnails after upload (YouTube allows changes) lets the algorithm determine which performs best. NemoVideo generates stylistically different options to maximize the test range.
4. **Batch weekly production eliminates creative burnout** — Producing one video is creative work. Producing 5 videos one-at-a-time is exhausting. Batch-producing 5 in one session preserves creative energy because the AI handles the mechanical production.
5. **Cross-platform repurposing multiplies reach for free** — One YouTube video repurposed into Shorts + Reels + LinkedIn + carousel reaches 3-5x more people. NemoVideo's multi-export makes this automatic.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube main video |
| MP4 9:16 | 1080x1920 | Shorts / Reels / TikTok |
| MP4 1:1 | 1080x1080 | Instagram / LinkedIn |
| JPG | 1920x1080 | Thumbnail candidates |
| TXT | — | SEO title + description + chapters |
| SRT | — | Closed captions |

## Related Skills

- [ai-faceless-video](/skills/ai-faceless-video) — Faceless video production
- [ai-video-from-text](/skills/ai-video-from-text) — Text to video
- [ai-avatar-video-maker](/skills/ai-avatar-video-maker) — AI avatar videos
