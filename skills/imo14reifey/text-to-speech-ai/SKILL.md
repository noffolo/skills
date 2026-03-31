---
name: text-to-speech-ai
version: "1.0.0"
displayName: "Text to Speech AI — Generate Natural Voiceover and Narration for Videos"
description: >
  Generate natural-sounding voiceover and narration for any video using AI text-to-speech. NemoVideo converts scripts into realistic speech with human-like intonation, emotion, and pacing — choose from 100+ voices across 30+ languages, control speed and emphasis, add pauses for dramatic effect, match the voice to the video's mood, and render the voiceover directly into the video with proper volume mixing against background music and sound effects.
metadata: {"openclaw": {"emoji": "🗣️", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

# Text to Speech AI — Natural Voiceover and Narration for Videos

Voiceover is the invisible backbone of most video content. YouTube explainers, product demos, training modules, social media narration, podcast intros, documentary narration, e-learning courses, corporate communications — all of them depend on a clear, engaging voice delivering the script. Hiring a voiceover artist costs $100-$500 per finished minute for professional quality. Recording yourself requires a quiet room, a decent microphone, and enough takes to get the delivery right (most people need 5-10 takes per paragraph to sound natural on camera). Re-recording when the script changes means scheduling another session. Translation into other languages means hiring additional artists for each language. NemoVideo's AI text-to-speech produces voiceover that is indistinguishable from human narration in casual listening: natural intonation that rises on questions and drops on conclusions, appropriate emphasis on key words, breathing pauses between sentences, emotional modulation that matches the content (excited for announcements, empathetic for support content, authoritative for training), and consistent quality regardless of script length. One script produces voiceover in 30+ languages with native pronunciation and culturally appropriate delivery style — no studio, no scheduling, no re-recording when the script changes.

## Use Cases

1. **YouTube Explainer — Conversational Narration (3-10 min)** — A creator writes a 1,500-word script about "How Solar Panels Actually Work." NemoVideo generates: a warm, conversational male voice that sounds like a knowledgeable friend explaining the topic, natural emphasis on technical terms the first time they appear, brief pauses before each new section for cognitive breathing room, and a slight energy increase during the "surprising fact" sections. The voiceover is mixed into the video at -6dB against -20dB background music with automatic ducking.
2. **Product Video — Confident and Energetic (30-90s)** — A 60-second product launch video needs a voice that communicates excitement and confidence. NemoVideo: generates an energetic female voice with upbeat pacing (170 words/minute vs. standard 150), slight uptick on benefit statements ("and it's completely waterproof"), and a commanding tone on the CTA. The voice matches the product video's energy — not a monotone reading of features.
3. **E-Learning Course — Clear and Patient (5-30 min per module)** — A 12-module online course needs consistent narration across 6 hours of content. NemoVideo: uses the same voice throughout all modules for student familiarity, adjusts pacing to match content complexity (slower for technical explanations, normal for introductions), adds emphasis on vocabulary terms, and includes natural pauses after questions ("Think about this for a moment...") to let learners process. Consistent voice across 6 hours — impossible to schedule with a human artist at this cost.
4. **Multilingual Ad — Same Script, 5 Languages (15-30s)** — A global brand needs the same 20-second ad voiceover in English, Spanish, German, Japanese, and Arabic. NemoVideo: translates the script with marketing-aware localization (not literal translation), selects culturally appropriate voice profiles for each language (formal for Japanese, warm for Brazilian Portuguese), adjusts pacing to fit the same video duration in each language, and delivers 5 voiceover tracks synced to the same visual timeline.
5. **Podcast Intro/Outro — Branded Audio Identity (10-30s)** — A podcast needs a consistent intro voiceover: "Welcome to The Daily Build, where we explore the craft of software engineering. I'm your host, and today we're talking about..." NemoVideo generates a voice that becomes the show's audio identity — same tone, same pacing, same personality every episode. When the intro script changes ("Season 3 of The Daily Build..."), regeneration is instant without rebooking a voice artist.

## How It Works

### Step 1 — Write the Script
Provide the text to be spoken. Mark emphasis with *asterisks*, pauses with [pause], and emotional shifts with [tone: excited] or [tone: serious].

### Step 2 — Choose Voice and Style
Select: gender, age range, accent, emotional tone, and speaking speed. Preview multiple voices before committing.

### Step 3 — Generate
```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "text-to-speech-ai",
    "prompt": "Generate voiceover for a 3-minute YouTube explainer about how neural networks learn. Voice: warm male, mid-30s, American English, conversational and knowledgeable (like a smart friend explaining something). Speed: 150 wpm. Emphasis on technical terms when first introduced. Natural pauses between paragraphs (0.8 sec). Slight energy increase during the surprising-fact section. Mix into existing video at -6dB voice, -20dB background music with ducking.",
    "script": "Have you ever wondered how a computer learns to recognize a cat in a photo? [pause] It turns out the answer is surprisingly similar to how *your* brain does it...",
    "voice": "warm-male-american-30s",
    "speed_wpm": 150,
    "tone": "conversational-knowledgeable",
    "pause_between_paragraphs": 0.8,
    "mix_into_video": true,
    "voice_volume": "-6dB",
    "music_volume": "-20dB",
    "ducking": true,
    "format": "16:9"
  }'
```

### Step 4 — Preview Voice and Mix
Preview the voiceover alone and mixed into the video. Adjust: speed, emphasis, tone, or volume balance. Re-generate specific sections without redoing the entire script.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Script and voice requirements |
| `script` | string | | Full script text with markup ([pause], *emphasis*, [tone: x]) |
| `voice` | string | | Voice profile: gender, age, accent, personality |
| `speed_wpm` | integer | | Words per minute (default: 150) |
| `tone` | string | | "conversational", "authoritative", "energetic", "calm", "empathetic" |
| `language` | string | | "en", "es", "de", "fr", "ja", "zh", "ko", "ar", "pt" |
| `pause_between_paragraphs` | float | | Seconds of pause (default: 0.5) |
| `mix_into_video` | boolean | | Render voiceover into existing video (default: false) |
| `voice_volume` | string | | "-3dB" to "-12dB" (default: "-6dB") |
| `music_volume` | string | | "-16dB" to "-24dB" (default: "-20dB") |
| `ducking` | boolean | | Duck music under speech (default: true) |
| `output_format` | string | | "mp4" (mixed), "wav", "mp3" (audio only) |

## Output Example

```json
{
  "job_id": "tts-20260328-001",
  "status": "completed",
  "script_words": 438,
  "duration_seconds": 175,
  "voice": "warm-male-american-30s",
  "speed_wpm": 150,
  "language": "en",
  "outputs": {
    "voiceover_audio": {
      "file": "voiceover.wav",
      "duration": "2:55",
      "format": "WAV 48kHz 24bit"
    },
    "mixed_video": {
      "file": "explainer-with-voiceover.mp4",
      "duration": "2:55",
      "resolution": "1920x1080",
      "voice_volume": "-6dB",
      "music_volume": "-20dB",
      "ducking_events": 22
    }
  }
}
```

## Tips

1. **150 words per minute is the natural conversational pace** — 130 wpm feels slow and condescending. 170 wpm feels rushed and hard to follow. 150 is the sweet spot for most content. Increase to 160-170 for energetic ads, decrease to 130-140 for technical training.
2. **Mark emphasis sparingly** — Emphasizing every other word sounds robotic. Mark only the words that change the sentence's meaning when stressed: "It's *completely* waterproof" not "*It's* *completely* *waterproof*."
3. **Pauses are more important than speed** — A 0.5-1.0 second pause before a key point creates anticipation. A pause after a question gives the viewer time to think. Pauses make voiceover feel human; constant speech feels mechanical.
4. **Same voice across a series builds familiarity** — Viewers develop a relationship with consistent narration. Changing voices between episodes feels disorienting. Lock in a voice profile for the entire series.
5. **Ducking makes voiceover audible without muting music** — Music dropping 6-8dB during speech means the viewer hears the voice clearly without the music disappearing entirely. The music fills pauses and maintains energy; the voice dominates during speech.

## Output Formats

| Format | Quality | Use Case |
|--------|---------|----------|
| WAV 48kHz | Lossless | Professional editing pipeline |
| MP3 320kbps | High | Web / podcast / lightweight |
| MP4 (mixed) | Source video | Ready-to-publish with voiceover |
| SRT | — | Matching caption file |

## Related Skills

- [instagram-video-caption](/skills/instagram-video-caption) — Instagram captions
- [subtitle-video-generator](/skills/subtitle-video-generator) — Auto subtitles
- [ai-video-generator-free](/skills/ai-video-generator-free) — Text to video
