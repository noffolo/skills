---
name: webinar-recording-maker
version: "1.0.0"
displayName: "Webinar Recording Maker — Create Webinar Replay and Presentation Videos"
description: >
  Webinar Recording Maker — Create Webinar Replay and Presentation Videos.
metadata: {"openclaw": {"emoji": "📡", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Webinar Recording Maker — Webinar Replay and Presentation Videos

The live webinar had 847 registrants, 312 actually showed up, the presenter's internet dropped for forty-five seconds during the most important slide, someone's dog barked audibly through an unmuted microphone at the critical product-demo moment, and the Q&A section — which contained the best content of the entire session — was cut short because the Zoom room hit its time limit. The recording of this webinar, sent unedited to the 535 people who didn't attend, is a ninety-minute test of patience that includes three minutes of "can everyone hear me?" at the beginning, a ten-minute section where the presenter forgot to share their screen, and an abrupt ending mid-sentence. Webinar recording content exists to solve this fundamental gap: the live event was valuable, the raw recording is unwatchable, and somewhere between the two lies an edited version that preserves the value and eliminates the friction. This tool transforms raw webinar recordings into polished replay videos — dead-air removal that eliminates the technical difficulties and "let me share my screen" moments, speaker-and-slide synchronization that shows the right visual at the right moment, highlight-reel extractions that compress ninety minutes into the essential fifteen, Q&A compilations that organize the best audience questions with clear answers, chapter navigation that lets viewers jump to the section they care about, and the professional overlay treatment that makes a Zoom recording look like a produced presentation. Built for marketing teams repurposing webinar content, SaaS companies creating product-demo libraries from live sessions, consultants turning client workshops into evergreen content, event organizers delivering post-event recordings, sales teams building prospect-education video libraries, and anyone whose best content was delivered live and deserves a second life as polished video.

## Example Prompts

### 1. Webinar Cleanup — Raw Recording to Polished Replay
"Create a polished 45-minute webinar replay from a raw 90-minute Zoom recording. The edit priorities: Remove the first 7 minutes (waiting room, 'can you see my screen?', technical setup). Start at the actual content — the presenter saying 'Let's dive in.' Remove minute 23-25: the internet drop. The slide froze, the presenter said 'I think I lost you all' three times. Cut to the next stable moment. Remove minute 41-43: the tangent about the presenter's weekend that had nothing to do with the topic. 'This is charming live but filler on replay.' Remove all 'um,' 'uh,' and dead-air pauses longer than 2 seconds. 'The pace should feel conversational but not hesitant. Removing verbal filler makes the presenter sound more authoritative without changing their voice.' Speaker-slide sync: the presenter forgot to advance from slide 7 to slide 8 for 90 seconds while talking about slide 8's content. Advance the slide in the edit to match the audio. 'The viewer should see what the presenter is discussing, not what the presenter forgot to click.' Add chapter markers: Introduction (0:00), Market Overview (4:30), Product Demo (18:00), Case Studies (31:00), Q&A (38:00). Overlay: presenter name, title, and company on a lower-third for the first 10 seconds. Add the company logo in the corner throughout. Closing: replace the abrupt Zoom-ending with a proper end card — company logo, CTA, next webinar date."

### 2. Highlight Reel — 90 Minutes to 10 Minutes
"Build a 10-minute highlight reel from a 90-minute webinar for social media and email marketing. Opening (0-15 sec): the strongest quote from the webinar — the presenter's most compelling 15-second statement, pulled from minute 47 of the original. 'Start with the best moment, not the first moment.' The hook: text overlay — '90-minute webinar. 10-minute highlights. Everything you need to know about [topic].' Key insight 1 (15-120 sec): the market overview — compressed from 15 minutes to 90 seconds. The three most important data points, each shown with the slide and the presenter's explanation. 'The full context is in the replay. The highlights give the takeaway.' Key insight 2 (120-240 sec): the product demo — the "aha moment" when the feature solved the problem. In the original, this was buried in a 20-minute demo. In the highlight: the setup (30 sec), the demo moment (60 sec), the result (30 sec). 'The demo that converts is the one that shows the problem being solved, not the one that shows every menu option.' Key insight 3 (240-360 sec): the case study — the customer story that made the audience react. Pull the specific numbers: 'Revenue increased 340% in 6 months.' Show the slide with the graph and the presenter's narration. Best Q&A moment (360-480 sec): the audience question that everyone was thinking — and the presenter's answer that clarified everything. 'The Q&A is often the most valuable section because it addresses real objections and concerns.' Closing (480-540 sec): the presenter's closing statement — the call to action, reframed for the highlight audience. 'Want the full 90 minutes? Link in the description. Want to see it in action? Book a demo.' End card with both options."

### 3. Q&A Compilation — Best Questions and Answers
"Produce a 15-minute Q&A compilation from a webinar, organized by topic. Opening: 'The webinar was 90 minutes. The Q&A was 25 minutes. These are the 10 questions everyone asked — organized so you can jump to the one you care about.' Chapter list on screen: Pricing (0:30), Implementation (3:15), Integration (6:00), Results (9:00), Getting Started (12:00). Topic 1 — Pricing (0-180 sec): three pricing questions grouped together. Q1: 'What's the pricing model?' — presenter's answer, edited to remove hesitation and filler. Q2: 'Are there discounts for annual plans?' — direct answer. Q3: 'Is there a free trial?' — answer with the CTA. 'Grouping by topic lets viewers find their specific concern without watching questions about implementation when they care about pricing.' Topic 2 — Implementation (180-360 sec): three implementation questions. 'How long does setup take?' 'Do we need a developer?' 'What about migration from our current tool?' Each answer cleaned up — filler removed, the direct answer preserved. Topic 3-5: same format — 2-3 questions per topic, each cleaned and organized. Closing: 'Ten questions. Fifteen minutes. The full webinar replay and additional resources are linked below.' End card with resource links."

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the webinar content, edit priorities, and output format |
| `duration` | string | | Target video length (e.g. "10 min", "45 min") |
| `style` | string | | Video style: "polished-replay", "highlight-reel", "qa-compilation", "chapter-edit", "social-clip" |
| `music` | string | | Background audio: "corporate-subtle", "none" |
| `format` | string | | Output ratio: "16:9", "9:16", "1:1" |
| `chapter_markers` | boolean | | Add chapter timestamps for section navigation (default: true) |
| `filler_removal` | boolean | | Remove verbal filler (um, uh) and dead-air pauses (default: true) |

## Workflow

1. **Describe** — Outline the webinar content, sections to keep/remove, and output goals
2. **Upload** — Add the raw webinar recording, slides, and any supplementary material
3. **Generate** — AI cleans the recording with filler removal, slide sync, and chapter markers
4. **Review** — Verify content accuracy, speaker attribution, and edit quality
5. **Export** — Download in your chosen format and resolution

## API Example

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "webinar-recording-maker",
    "prompt": "Clean up a 90-minute Zoom recording: remove first 7 minutes of setup, cut internet-drop at 23-25 min, remove tangent at 41-43 min, remove verbal filler and pauses over 2 sec, sync slides to audio where presenter forgot to advance, add chapter markers for 5 sections, add speaker lower-third and company logo, replace abrupt ending with branded end card",
    "duration": "45 min",
    "style": "polished-replay",
    "chapter_markers": true,
    "filler_removal": true,
    "music": "none",
    "format": "16:9"
  }'
```

## Tips for Best Results

1. **Remove the first 5-10 minutes of every webinar** — Technical setup, waiting-room chatter, and "can you hear me" are never valuable on replay. The AI identifies and removes pre-content segments.
2. **Enable filler removal for professional polish** — "Um" and "uh" removal makes presenters sound more authoritative. The AI removes verbal filler when filler_removal is enabled.
3. **Sync slides to audio, not to clicks** — When the presenter discusses slide 8 while showing slide 7, the AI advances the slide to match the audio content.
4. **Add chapter markers for long replays** — Viewers rewatch specific sections; chapters let them navigate. The AI generates chapter timestamps when chapter_markers is enabled.
5. **Extract the best 10 minutes for marketing** — The highlight reel converts more viewers to replay watchers than the full recording does. The AI identifies high-impact moments for extraction.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | Webinar replay / presentation recording |
| MP4 9:16 | 1080p | TikTok / Instagram Reels webinar clip |
| MP4 1:1 | 1080p | LinkedIn post / email embed |
| GIF | 720p | Key insight loop / quote card |

## Related Skills

- [online-course-video](/skills/online-course-video) — Educational course and lesson videos
- [training-video-maker](/skills/training-video-maker) — Corporate training and onboarding videos
- [instructional-video-maker](/skills/instructional-video-maker) — Instructional and educational videos
