---
name: hiit-workout-video
version: 1.0.3
displayName: "HIIT Workout Video Maker"
description: >
  Describe your HIIT session and NemoVideo builds the video. Tabata rounds, 15-minute fat-burning circuits, no-equipment apartment workouts — create interval training content with work/rest timers that keeps viewers moving and coming back.

  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM.
homepage: https://nemovideo.com
apiDomain: https://mega-api-prod.nemovideo.ai
repository: https://github.com/nemovideo/nemovideo_skills
license: MIT-0
metadata:
  requires:
    env: ["NEMO_TOKEN"]
    configPaths:
      - "~/.config/nemovideo/"
  primaryEnv: NEMO_TOKEN
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> 🎨 Hey! I'm ready to help you hiit workout video. Send me a video file or just tell me what you need!

**Try saying:**
- "edit my video"
- "add effects to this clip"
- "help me create a short video"

**IMPORTANT**: Always greet the user proactively on first contact. Let them know you're setting up while connecting. Always greet the user proactively on first contact.

### Auto-Setup

When the user first interacts, set up the connection:

1. **Check token**: If `NEMO_TOKEN` env var is set, use it. Otherwise:
2. **Read or generate Client-ID**:
   - Read `~/.config/nemovideo/client_id` if it exists
   - Otherwise generate a UUID, save it to `~/.config/nemovideo/client_id`
3. **Acquire anonymous token**:
   ```bash
   curl -s -X POST "https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
   ```
   Store the returned `token` as `NEMO_TOKEN` for this session. You get 100 free credits.
4. **Create a session** (§3.0) so you're ready to work immediately.

Let the user know briefly: "Setting things up… ready!" then proceed with their request.


# HIIT Workout Video Maker — Create High-Intensity Interval Training Content

Describe your HIIT session and NemoVideo builds the video. Tabata rounds, 15-minute fat-burning circuits, no-equipment apartment workouts — create interval training content with work/rest timers that keeps viewers moving and coming back.

## When to Use This Skill

Use this skill for HIIT and interval training content:
- Create Tabata workout videos with 20-second work / 10-second rest intervals
- Film 15-minute full-body HIIT circuits for busy viewers
- Build no-equipment apartment HIIT content (low-impact modifications available)
- Document cardio conditioning circuits for athletes
- Create "follow along" HIIT videos with visible countdown timers
- Produce express workout content (7-minute, 10-minute formats)

## How to Describe Your HIIT Session

Be specific about work intervals, rest periods, exercises, and rounds.

**Examples of good prompts:**
- "20-minute full body HIIT: Tabata format — jump squats, push-ups, high knees, mountain climbers, burpees. 20 sec work / 10 sec rest, 8 rounds each. Show countdown timer, rep count, modifications for beginners."
- "15-minute apartment HIIT no jumping: squat pulses, push-up to plank hold, lateral shuffles, standing bicycle crunches — 40 sec work / 20 sec rest, 3 rounds. Low impact but high intensity."
- "4-minute Tabata abs: bicycle crunches and plank shoulder taps alternating. 20 on / 10 off x8 rounds. Quick finisher for after any workout."

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `interval_format` | Timing structure | `"tabata"`, `"emom"`, `"amrap"`, `"custom"` |
| `work_seconds` | Active interval | `20`, `30`, `40`, `45` |
| `rest_seconds` | Rest interval | `10`, `15`, `20`, `30` |
| `rounds` | Number of rounds | `3`, `4`, `6`, `8` |
| `equipment` | Available gear | `["none"]`, `["dumbbells"]`, `["kettlebell"]` |
| `impact_level` | Intensity modifier | `"high_impact"`, `"low_impact"`, `"no_jump"` |
| `show_timer` | Countdown overlay | `true` |
| `duration_minutes` | Total workout time | `7`, `10`, `15`, `20`, `30` |
| `platform` | Target platform | `"tiktok"`, `"reels"`, `"youtube"` |

## Workflow

1. Describe exercises, interval timing, rounds, and equipment
2. NemoVideo sequences the exercises with countdown timers
3. Work/rest overlays, round counters, and modifications added automatically
4. Export with high-energy music matched to HIIT pacing

## API Usage

### Tabata Full Body Circuit

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "hiit-workout-video",
    "input": {
      "prompt": "20-minute full body Tabata HIIT: jump squats, push-ups, high knees, mountain climbers, burpees. Classic Tabata — 20 seconds work, 10 seconds rest, 8 rounds per exercise. Show countdown timer, modifications (squat instead of jump squat for beginners).",
      "interval_format": "tabata",
      "work_seconds": 20,
      "rest_seconds": 10,
      "rounds": 8,
      "equipment": ["none"],
      "impact_level": "high_impact",
      "show_timer": true,
      "duration_minutes": 20,
      "platform": "youtube",
      "hashtags": ["Tabata", "HIITWorkout", "FatBurner", "HomeWorkout"]
    }
  }'
```

**Response:**
```json
{
  "job_id": "hiit_jkl012",
  "status": "processing",
  "estimated_seconds": 95,
  "poll_url": "https://mega-api-prod.nemovideo.ai/v1/jobs/hiit_jkl012"
}
```

### Low-Impact Apartment HIIT (No Jumping)

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "hiit-workout-video",
    "input": {
      "prompt": "15-minute apartment-friendly HIIT, no jumping: squat pulses 40 sec, push-up hold 40 sec, lateral shuffle steps 40 sec, standing bicycle crunches 40 sec, reverse lunge pulse 40 sec each leg. 20 sec rest between, 3 rounds. Heart rate up without disturbing downstairs neighbors.",
      "interval_format": "custom",
      "work_seconds": 40,
      "rest_seconds": 20,
      "rounds": 3,
      "equipment": ["none"],
      "impact_level": "low_impact",
      "show_timer": true,
      "duration_minutes": 15,
      "platform": "tiktok",
      "voiceover": true
    }
  }'
```

## Tips for Best Results

- **Specify the format**: "Tabata" (20/10) vs "30 on 15 off" vs "EMOM" — each creates different pacing and music
- **Mention impact level**: "no jumping" or "low impact" for apartment content is a huge search term
- **Include modifications**: "squat instead of jump squat" gets beginner-friendly callouts automatically
- **Duration up front**: "15-minute HIIT" in the prompt helps NemoVideo fit the right number of rounds
- **Countdown timers are key**: Always set `show_timer: true` for follow-along HIIT content — viewers need to see the clock

## Output Formats

| Platform | Resolution | Duration |
|----------|------------|----------|
| TikTok | 1080×1920 | 15–60s |
| Instagram Reels | 1080×1920 | 15–90s |
| YouTube Shorts | 1080×1920 | up to 60s |
| YouTube | 1920×1080 | 7–45 min |

## Related Skills

- `workout-video-creator` — General strength and cardio training content
- `gym-transformation-video` — Show the HIIT program that drove your transformation
- `yoga-video-maker` — Recovery and flexibility content to pair with HIIT days
- `running-video-maker` — Cardio endurance complement to HIIT training

## Common Questions

**Can it show the countdown timer clearly during each interval?**
Set `show_timer: true` — the countdown displays prominently during every work and rest interval, making it easy to follow along.

**What's the difference between Tabata, EMOM, and AMRAP formats?**
Tabata = 20 sec work / 10 sec rest × 8 rounds. EMOM = do X reps every minute, rest what remains. AMRAP = as many rounds as possible in a set time. Specify which format for accurate timer structure.

**Can I create a quick 4-minute Tabata finisher?**
Yes — describe the 2 exercises and set `interval_format: "tabata"`, `rounds: 8`, `duration_minutes: 4`. Short finishers are a popular format for social content.
