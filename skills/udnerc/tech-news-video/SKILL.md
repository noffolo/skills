---
name: tech-news-video
version: "1.0.0"
displayName: "Tech News Video Maker — Create Technology News and Analysis Videos"
description: >
  Tech News Video Maker — Create Technology News and Analysis Videos.
metadata: {"openclaw": {"emoji": "📰", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Tech News Video Maker — Technology News and Analysis Videos

The tech news cycle moves at a speed that makes traditional journalism look like a geology lecture — a product is announced at 9 AM, the hot takes are published by 9:47, the backlash to the hot takes arrives at 10:30, and by lunch the entire discourse has moved to a different product announcement that will undergo the same cycle, leaving the person who actually wanted to understand the original announcement navigating a landscape of clickbait headlines, contextless tweets, and explainer articles written by people who clearly skimmed the press release and added their own speculation in paragraphs that begin with "it remains to be seen." Tech news video content cuts through this noise by delivering structured analysis in a format that forces the creator to organize their thinking — you cannot ramble for 14 paragraphs in a 3-minute video the way you can in a blog post, and the visual medium demands that claims be supported with screenshots, data visualizations, and product footage rather than adjectives. This tool transforms technology news into polished analysis videos — breaking-news summaries delivering the essential facts within minutes of an announcement, deep-dive analyses explaining what a development means for the industry, weekly roundup compilations curating the most important stories, opinion and commentary pieces providing perspective that raw news coverage lacks, company and product profiles contextualizing news within a broader strategic narrative, and the trend-analysis segments that connect individual news items into patterns that predict where the industry is heading. Built for tech journalists producing video coverage, YouTube tech commentators building news channels, corporate communications teams monitoring industry developments, newsletter creators expanding into video, podcast hosts creating video companions, and anyone whose audience needs to understand what happened in tech today without reading fifteen articles and three Twitter threads to assemble a coherent picture.

## Example Prompts

### 1. Breaking News — Quick Analysis of a Major Announcement
"Create a 4-minute breaking news analysis of a major tech company announcing a new AI product. The headline (0-10 sec): the announcement on screen — the company logo, the product name, the one-line description. 'Thirty minutes ago, [Company] announced [Product] — an AI assistant that runs entirely on your device with no cloud connection. Here's what it means and why it matters.' What was announced (10-60 sec): the facts — no speculation. 'The product: an on-device AI model that handles text generation, image understanding, and voice interaction without sending data to external servers.' Show the product demo screenshots or keynote slides. 'The specs: a 7-billion parameter model compressed to run on devices with 8GB RAM or more. Response time: under 2 seconds for text, under 5 seconds for image analysis.' 'Supported devices at launch: their flagship phone, their laptop line, and their tablet — all from 2024 or newer.' 'Availability: rolling out over 6 weeks starting today. Free for all device owners.' 'These are the confirmed facts from the press release and keynote. Everything after this is analysis.' Why it matters (60-150 sec): the three implications. 'Implication 1 — Privacy as a feature: Running AI on-device means your conversations, documents, and photos never leave your hardware. In a landscape where every other AI assistant sends data to cloud servers, on-device processing is a genuine differentiator — not a marketing claim but an architectural decision.' 'For users: your AI interactions are as private as your calculator app. No data collection. No training on your inputs.' 'Implication 2 — Performance tradeoff: A 7B parameter model is capable but not frontier. For comparison, cloud-based assistants use models 10-100x larger. The on-device version will be noticeably less capable for complex tasks — multi-step reasoning, nuanced creative writing, technical code generation.' 'The bet: most daily AI tasks (drafting emails, summarizing articles, answering quick questions) don't need frontier-scale models. A smaller model that's instant and private beats a larger model that's slower and surveillance-adjacent.' 'Implication 3 — Industry response: This forces competitors to address the privacy question directly. If [Company] proves that users prefer private-but-smaller over powerful-but-cloud, the entire industry's AI strategy shifts.' What to watch (150-210 sec): 'Three things to monitor over the next 3 months.' '1. Actual performance benchmarks: The keynote demo was carefully curated. Independent testing will reveal the real capability gap between on-device and cloud.' '2. Adoption rate: Will users actually use it? On-device AI that nobody activates is a spec-sheet feature, not a product.' '3. Developer access: Can third-party apps use the on-device model? If yes, this becomes a platform. If no, it's a feature.' Close (210-240 sec): 'Summary: [Company] just bet that privacy beats power for everyday AI. The product launches today, the proof arrives over the next quarter, and the industry impact depends on whether users agree with the bet. I'll have a full hands-on review when I get access. Subscribe for that.' End card."

### 2. Weekly Roundup — Top 5 Stories of the Week
"Build a 6-minute weekly tech news roundup covering the five biggest stories. Opening (0-10 sec): 'The five biggest tech stories this week — in 6 minutes. Let's go.' Story 1 (10-70 sec): the biggest story. Headline on screen. 'Number 1: [Headline].' 30 seconds of context: what happened, who's involved, the key numbers. 30 seconds of analysis: why it matters, who it affects, what happens next. 'The bottom line: [one-sentence summary].' Story 2 (70-130 sec): same structure. Headline. Context. Analysis. Bottom line. 'Each story gets exactly 60 seconds. This constraint forces clarity — if you can't explain it in 60 seconds, you don't understand it well enough.' Story 3 (130-190 sec): the mid-week development. 'Story 3 is the one that got less attention but might matter more long-term.' Context and analysis in 60 seconds. Story 4 (190-250 sec): the business story — an acquisition, a funding round, a strategic shift. 'The money story of the week.' Numbers on screen: deal size, valuation, market impact. Story 5 (250-310 sec): the wildcard — the weird, unexpected, or human-interest tech story. 'And finally — the story that made me do a double-take.' 'The wildcard story keeps the roundup from being five consecutive serious analyses. Variety in tone maintains viewer energy across 6 minutes.' The outlook (310-340 sec): 'Next week to watch: [Event 1], [Earnings report], and [Product launch]. I'll cover the biggest developments as they happen and next week's roundup drops same time, same place.' End card with subscribe prompt. 'The weekly roundup format works because consistency builds habit. The viewer knows: every [day], 6 minutes, five stories. That predictability is a subscription driver.'"

### 3. Trend Analysis — Connecting the Dots Across Stories
"Produce a 5-minute trend analysis connecting three recent developments into a pattern. Opening (0-15 sec): three headlines on screen — seemingly unrelated. 'These three stories from the past month look unrelated. They're not. They're the same story told three different ways — and the pattern predicts what's coming next.' Story 1 recap (15-50 sec): brief summary of the first development. '[Company A] laid off its entire machine-learning research team and redirected budget to applied AI products.' 'The headline said "layoffs." The actual story: research is being replaced by implementation.' Story 2 recap (50-85 sec): '[Company B] shut down its AI research lab and signed a licensing deal with [AI Provider] instead of building their own models.' 'The headline said "partnership." The actual story: build-vs-buy just tipped permanently toward buy.' Story 3 recap (85-120 sec): '[Company C] — a startup that raised $200M to build foundation models — pivoted to building AI applications using open-source models.' 'The headline said "pivot." The actual story: the foundation-model market has consolidated to the point where new entrants can't compete.' The pattern (120-200 sec): 'The pattern: the AI industry is splitting into two tiers.' Animated diagram: 'Tier 1: Foundation model providers — three to five companies with the capital, data, and compute to build frontier models.' 'Tier 2: Everyone else — using Tier 1 models (via API or open-source) to build applications, products, and services.' 'Company A realized: we can't compete in Tier 1. Applied AI is where our value is.' 'Company B realized: licensing a Tier 1 model is cheaper and better than building our own.' 'Company C realized: the $200M we raised isn't enough. Tier 1 requires billions.' 'Three different companies. Three different decisions. One conclusion: the foundation-model era is consolidating, and the application era is beginning.' What it means (200-260 sec): 'For developers: stop worrying about which model to build on and start building. The models are becoming commodities. The applications are the value.' 'For investors: foundation-model companies are infrastructure plays. Application companies are where the returns are. The picks-and-shovels gold rush is ending; the gold rush is beginning.' 'For users: AI products are about to get dramatically better — not because the models improved but because the companies building on them stopped trying to also build the model and focused entirely on the experience.' The prediction (260-290 sec): 'By end of 2027, the AI industry will look like the cloud industry: three to four infrastructure providers (AWS, Azure, GCP equivalent) and thousands of companies building on top of them.' 'The companies that figured this out first — that pivoted from model-building to application-building — will have a 12-18 month head start.' Close (290-300 sec): 'Three headlines. One pattern. One prediction. This is what tech news analysis does that raw reporting doesn't — it connects the dots between stories and reveals the picture they're drawing.' End card."

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the tech news story, analysis angle, or trend |
| `duration` | string | | Target length (e.g. "4 min", "5 min", "6 min") |
| `style` | string | | Video style: "breaking-news", "weekly-roundup", "trend-analysis", "deep-dive", "opinion" |
| `music` | string | | Background audio: "news-urgent", "tech-ambient", "none" |
| `format` | string | | Output ratio: "16:9", "9:16", "1:1" |
| `headline_overlay` | boolean | | Show news headlines and key data overlays (default: true) |
| `source_citations` | boolean | | Display source attributions for claims and data (default: true) |

## Workflow

1. **Describe** — Outline the news story, analysis angle, and timeliness
2. **Upload** — Add screenshots, keynote footage, data charts, and source material
3. **Generate** — AI produces the video with headline overlays, data visualizations, and analysis pacing
4. **Review** — Verify factual accuracy, source attribution, and timeliness
5. **Export** — Download in your chosen format

## API Example

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "tech-news-video",
    "prompt": "Create 4-minute breaking news analysis: on-device AI product announcement with 7B parameter model specs, three implications — privacy architecture, performance tradeoff vs cloud models, industry competitive response — three things to watch over next quarter including benchmarks adoption and developer access, subscribe CTA for hands-on review",
    "duration": "4 min",
    "style": "breaking-news",
    "headline_overlay": true,
    "source_citations": true,
    "music": "news-urgent",
    "format": "16:9"
  }'
```

## Tips for Best Results

1. **Separate facts from analysis explicitly** — "These are confirmed facts. Everything after is analysis" builds trust. The AI structures fact-then-analysis.
2. **Use data overlays for key numbers** — Revenue figures, user counts, and performance metrics need to be visible. The AI renders data when headline_overlay is enabled.
3. **Cite sources visually** — "Source: company press release" on screen verifies claims. The AI displays attributions when source_citations is enabled.
4. **Time-box stories in roundups** — 60 seconds per story forces clarity. The AI enforces pacing constraints.
5. **End breaking news with "what to watch"** — Forward-looking analysis gives the viewer a framework. The AI structures monitoring checklists.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube tech news / website embed |
| MP4 9:16 | 1080p | TikTok / Reels news clip |
| MP4 1:1 | 1080p | LinkedIn / Twitter news post |
| GIF | 720p | Data chart / headline card |

## Related Skills

- [ai-news-video](/skills/ai-news-video) — AI industry news and analysis
- [startup-news-video](/skills/startup-news-video) — Startup and venture capital news
- [cybersecurity-video](/skills/cybersecurity-video) — Cybersecurity news and education
