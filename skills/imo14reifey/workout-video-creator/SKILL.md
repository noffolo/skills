---
name: workout-video-creator
version: 1.0.5
displayName: "Workout Video Creator"
description: >
  Describe your workout and NemoVideo creates the video. Strength training sets, cardio circuits, home gym sessions — narrate your exercise sequence and get a vertical fitness short ready for TikTok, Reels, or YouTube Shorts.

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

> ✨ Let's workout video creator! Drop a video here or describe what you'd like to create.

**Try saying:**
- "add effects to this clip"
- "help me create a short video"
- "edit my video"

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


# Workout Video Creator — Build Training and Exercise Content for Fitness Coaches

Describe your workout and NemoVideo creates the video. Strength training sets, cardio circuits, home gym sessions — narrate your exercise sequence and get a vertical fitness short ready for TikTok, Reels, or YouTube Shorts.

## When to Use This Skill

Use this skill for general fitness content:
- Create exercise tutorial videos for personal trainers and fitness coaches
- Film at-home workout routines with bodyweight exercises
- Build gym session content with equipment demonstrations
- Document weekly training splits (push/pull/legs, upper/lower)
- Create beginner workout guides with form cues and modifications
- Produce workout programming content for online fitness coaching

## How to Describe Your Workout

Be specific about exercises, sets/reps, equipment, and fitness goal.

**Examples of good prompts:**
- "Upper body strength training: bench press 4x8, dumbbell rows 3x10, shoulder press 3x8, tricep dips 3x12 — show each exercise with form cues, rest periods, beginner modifications"
- "30-minute home cardio circuit: jump rope 1 min, burpees 10 reps, mountain climbers 30 sec — 4 rounds, no equipment needed, apartment-friendly"
- "Leg day gym session: barbell squat, Romanian deadlift, leg press, walking lunges — form breakdown video for beginner lifters"

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `workout_type` | Training style | `"strength"`, `"cardio"`, `"hiit"`, `"flexibility"`, `"sports"` |
| `equipment` | Available gear | `["dumbbells", "barbell", "resistance_bands"]` or `["none"]` |
| `duration_minutes` | Workout length | `20`, `30`, `45`, `60` |
| `fitness_level` | Target audience | `"beginner"`, `"intermediate"`, `"advanced"` |
| `show_form_cues` | Add technique overlays | `true` |
| `video_duration` | Output length in seconds | `30`, `60`, `90` |
| `platform` | Target platform | `"tiktok"`, `"reels"`, `"youtube"` |

## Workflow

1. Describe exercises, sets/reps, equipment, and training goal
2. NemoVideo sequences exercise clips with form annotations
3. Rep counts, rest timers, and muscle group labels added automatically
4. Export vertical video optimized for fitness content platforms

## API Usage

### Gym Strength Training Video

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "workout-video-creator",
    "input": {
      "prompt": "Upper body push day: bench press 4x8 at 135lb, incline dumbbell press 3x10, cable fly 3x15, overhead press 3x8, tricep pushdown 4x12 — intermediate lifter, gym setting, form cues for each movement",
      "workout_type": "strength",
      "equipment": ["barbell", "dumbbells", "cables"],
      "fitness_level": "intermediate",
      "show_form_cues": true,
      "video_duration": 60,
      "platform": "youtube",
      "hashtags": ["WorkoutVideo", "GymLife", "StrengthTraining", "FitnessContent"]
    }
  }'
```

**Response:**
```json
{
  "job_id": "workout_abc123",
  "status": "processing",
  "estimated_seconds": 90,
  "poll_url": "https://mega-api-prod.nemovideo.ai/v1/jobs/workout_abc123"
}
```

### Home Workout No-Equipment Circuit

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "workout-video-creator",
    "input": {
      "prompt": "30-minute bodyweight home workout: 10 push-ups, 15 squats, 10 reverse lunges each leg, 20 glute bridges, 30-sec plank — 4 rounds, beginner-friendly modifications shown, apartment safe (no jumping)",
      "workout_type": "cardio",
      "equipment": ["none"],
      "fitness_level": "beginner",
      "show_form_cues": true,
      "video_duration": 45,
      "platform": "tiktok",
      "voiceover": true
    }
  }'
```

## Tips for Best Results

- **List exercises with sets and reps**: "4x8 bench press" beats "chest workout" — specificity creates better pacing
- **Mention equipment or lack of it**: "no equipment" or "dumbbells only" shapes the entire video format
- **Specify fitness level**: Beginner videos need form cues and modifications; advanced can skip basics
- **Name the training goal**: "fat loss circuit" vs "muscle building" changes music, pacing, and overlays
- **Include rest periods**: "60 sec rest between sets" helps NemoVideo build accurate timing

## Output Formats

| Platform | Resolution | Duration |
|----------|------------|----------|
| TikTok | 1080×1920 | 30–90s |
| Instagram Reels | 1080×1920 | 30–90s |
| YouTube Shorts | 1080×1920 | up to 60s |
| YouTube | 1920×1080 | 60–300s |

## Related Skills

- `hiit-workout-video` — High-intensity interval training specific content
- `yoga-video-maker` — Flexibility and mindfulness workout content
- `gym-transformation-video` — Before-after fitness journey videos
- `running-video-maker` — Cardio and endurance training content

## Common Questions

**Can it show beginner modifications alongside the main exercise?**
Set `fitness_level: "beginner"` and mention "show modifications" in the prompt — NemoVideo adds split-screen or sequential modification demos.

**How do I add rep count overlays?**
Set `show_form_cues: true` — this enables rep counters, muscle group highlights, and technique callouts automatically.

**Can personal trainers use this for client programming videos?**
Yes — describe the client's program and fitness level. NemoVideo generates a professional-looking tutorial that trainers can share directly with clients.
