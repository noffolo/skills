---
name: ai-video-summarizer
version: "1.0.0"
displayName: "AI Video Summarizer — Summarize Any Video into Key Points, Chapters and Clips"
description: >
  Summarize any video using AI — extract key points, generate chapter breakdowns, create highlight clips, produce text summaries, and identify the most important moments. NemoVideo watches the full video and produces: a concise text summary, timestamped key points, chapter markers with descriptions, the top 3-5 highlight clips, a transcript with topic segmentation, and a one-sentence TL;DR — turning hours of video content into searchable, quotable, actionable summaries in minutes.
metadata: {"openclaw": {"emoji": "📋", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# AI Video Summarizer — Turn Any Video into Actionable Summaries

The world produces 500 hours of YouTube video every minute. Podcast episodes average 60-90 minutes. Conference talks run 30-45 minutes. Lecture recordings span 50-90 minutes. Webinar replays last 45-120 minutes. The knowledge inside these videos is valuable — but accessing it requires watching at 1x speed, hoping you don't miss the key insight buried at minute 37 of a 60-minute recording. Nobody has time to watch everything. But everyone needs the insights. NemoVideo bridges this gap by watching the video for you. Upload any video — a YouTube URL, a podcast episode, a lecture recording, a meeting replay, a conference talk — and the AI produces: a concise summary (the entire video's value in 200-500 words), timestamped key points (the 5-10 most important insights with exact timestamps), chapter breakdown (every topic change with a description), highlight clips (the 3-5 most valuable segments extracted as standalone videos), full transcript with topic segmentation, and a one-sentence TL;DR that captures the video's core message. Hours of content become minutes of reading — with the ability to jump to any specific moment that matters.

## Use Cases

1. **YouTube Video → Key Takeaways (any length)** — A 25-minute YouTube video about investment strategies. NemoVideo produces: a 300-word summary covering all key strategies, 7 timestamped key points ("At 8:22: Dollar-cost averaging outperforms lump-sum investing 68% of the time in volatile markets"), chapter breakdown with 5 topics, the 3 strongest clips extracted as standalone videos (each 30-90 seconds), and a TL;DR: "Consistent monthly investing in index funds with annual rebalancing outperforms active management for 95% of individual investors."
2. **Podcast Episode → Show Notes (30-120 min)** — A 90-minute interview podcast. NemoVideo generates: summary covering the guest's main arguments, 10 quotable moments with timestamps and speaker labels ("At 34:15, Dr. Chen: 'The real breakthrough wasn't the algorithm — it was realizing we were asking the wrong question'"), topic timeline showing when each subject was discussed, 5 highlight clips for social media promotion, and a full transcript with speaker identification.
3. **Lecture Recording → Study Notes (50-90 min)** — A 75-minute university lecture on organic chemistry. NemoVideo produces: structured notes following the lecture's progression, all definitions extracted with timestamps, key formulas and concepts highlighted, practice problems identified and timestamped, a summary that reads like a textbook chapter overview, and links between concepts ("This reaction mechanism connects to the SN2 reactions covered at 12:30").
4. **Conference Talk → Executive Brief (20-45 min)** — A 35-minute keynote the CEO couldn't attend. NemoVideo delivers: a 200-word executive summary, 5 actionable takeaways, 3 data points or statistics cited, the speaker's key recommendation, and a 2-minute highlight clip capturing the most important moment. The CEO gets the talk's full value in 3 minutes of reading.
5. **Meeting Recording → Action Items (15-120 min)** — A 60-minute team meeting. NemoVideo extracts: all decisions made (with timestamps and participants), all action items (with assignee, deadline, and context), all open questions flagged for follow-up, a 150-word executive summary, and topic-by-topic breakdown. The meeting becomes an actionable document instead of a forgotten recording.

## How It Works

### Step 1 — Provide Video
Upload a video file or paste a URL. NemoVideo accepts any format, any length, any language.

### Step 2 — Choose Summary Outputs
Select: text summary, key points, chapters, highlight clips, transcript, action items, or all of them.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "ai-video-summarizer",
    "prompt": "Summarize this 45-minute conference talk about AI in healthcare. Generate: 300-word summary, top 8 key points with timestamps, chapter breakdown, 3 highlight clips (best 60-second segments), full transcript with speaker labels, and a one-sentence TL;DR. Focus on actionable insights for hospital administrators.",
    "outputs": ["summary", "key-points", "chapters", "highlight-clips", "transcript", "tldr"],
    "summary_length": "300 words",
    "key_points_count": 8,
    "highlight_clips_count": 3,
    "highlight_clip_duration": "60 sec",
    "focus": "actionable insights for hospital administrators",
    "language": "en"
  }'
```

### Step 4 — Review and Use
Review summary accuracy. Jump to any timestamped moment. Share highlight clips. Distribute the summary to stakeholders.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Video source and summary requirements |
| `outputs` | array | | ["summary","key-points","chapters","highlight-clips","transcript","tldr","action-items"] |
| `summary_length` | string | | "brief" (100w), "standard" (300w), "detailed" (500w) |
| `key_points_count` | integer | | Number of key points (default: 5-10 based on length) |
| `highlight_clips_count` | integer | | Number of clips to extract (default: 3) |
| `highlight_clip_duration` | string | | "30 sec", "60 sec", "90 sec" |
| `focus` | string | | Specific angle or audience to prioritize |
| `language` | string | | "auto", "en", "es", "de", "fr", "ja", "zh" |
| `speaker_labels` | boolean | | Identify speakers (default: true) |
| `batch_urls` | array | | Multiple videos for batch summarization |

## Output Example

```json
{
  "job_id": "avs-20260328-001",
  "status": "completed",
  "source_duration": "45:18",
  "language": "en",
  "outputs": {
    "tldr": "AI diagnostic tools reduce emergency department wait times by 34% when integrated into existing triage workflows rather than replacing them.",
    "summary": "Dr. Sarah Chen's keynote argues that AI in healthcare succeeds not by replacing clinical judgment but by augmenting it at specific decision points... [300 words]",
    "key_points": [
      {"timestamp": "3:22", "point": "AI triage tools reduce ED wait times by 34% in the Mount Sinai pilot"},
      {"timestamp": "8:45", "point": "Integration failures account for 78% of failed healthcare AI deployments"},
      {"timestamp": "15:10", "point": "The 3-phase implementation model: shadow mode → advisory mode → autonomous mode"}
    ],
    "chapters": [
      {"timestamp": "0:00", "title": "The Promise vs Reality of Healthcare AI", "duration": "6:30"},
      {"timestamp": "6:30", "title": "Case Study: Mount Sinai ED Triage", "duration": "8:15"},
      {"timestamp": "14:45", "title": "The 3-Phase Implementation Framework", "duration": "10:20"}
    ],
    "highlight_clips": [
      {"file": "highlight-1.mp4", "timestamp": "8:22-9:24", "topic": "34% wait time reduction statistic"},
      {"file": "highlight-2.mp4", "timestamp": "15:10-16:08", "topic": "3-phase framework introduction"},
      {"file": "highlight-3.mp4", "timestamp": "38:45-39:50", "topic": "Closing recommendation"}
    ]
  }
}
```

## Tips

1. **Key points with timestamps are more useful than full transcripts** — Most people don't read 7,000 words. They want the 5 insights that matter, with the ability to jump to the exact moment for context.
2. **Highlight clips are instant social content** — The 3 best 60-second moments from a 45-minute talk become LinkedIn posts, Twitter clips, or newsletter embeds. One summary operation produces a week of promotional content.
3. **Focus parameter changes everything** — Summarizing the same talk "for investors" vs "for engineers" vs "for customers" produces three different summaries emphasizing different points. The same content, different audiences.
4. **Batch summarization turns a conference into a document** — 20 conference talks → 20 summaries → one combined brief. An executive gets the entire conference's value in 30 minutes of reading.
5. **Action items extraction turns meetings into accountability** — "Sarah will send the proposal by Friday" extracted automatically means nobody can claim they didn't hear the commitment.

## Output Formats

| Format | Content | Use Case |
|--------|---------|----------|
| MD | Formatted summary + key points | Reading / sharing |
| JSON | Structured data | API integration |
| MP4 | Highlight clips | Social media / promotion |
| SRT | Timestamped transcript | Reference / captions |
| TXT | Plain text summary | Email / messaging |

## Related Skills

- [ai-video-script-generator](/skills/ai-video-script-generator) — Write video scripts
- [video-hook-maker](/skills/video-hook-maker) — Generate hooks
- [video-color-correction-ai](/skills/video-color-correction-ai) — Color correction
