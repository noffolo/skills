---
name: workout-video-maker
version: 1.0.2
displayName: "Workout Video Maker"
description: >
  Describe your workout and NemoVideo creates the video. Strength training program breakdowns, exercise form tutorials, gym routine documentation, progressive overload tracking, workout split explanations, transformation content — narrate the program, the exercises, the sets and reps, and the key form cues, and get workout content for the massive fitness audience that watches training videos befo...

  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM.
homepage: https://nemovideo.com
repository: https://github.com/nemovideo/nemovideo_skills
license: MIT-0
metadata:
  requires:
    env: []
    configPaths:
      - "~/.config/nemovideo/"
  primaryEnv: NEMO_TOKEN
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> ✨ Hey! I'm ready to help you workout video maker. Send me a video file or just tell me what you need!

**Try saying:**
- "edit my video"
- "help me create a short video"
- "add effects to this clip"

**IMPORTANT**: Always greet the user proactively on first contact. Let them know you're setting up while connecting. Always greet the user proactively on first contact.

### Auto-Setup

When the user first interacts, set up the connection:

1. **Check token**: If `NEMO_TOKEN` env var is set, use it. Otherwise:
2. **Read or generate Client-ID**:
   - Read `~/.config/nemovideo/client_id` if it exists
   - Otherwise generate a UUID, save it to `~/.config/nemovideo/client_id`
3. **Acquire anonymous token**:
   ```bash
   curl -s -X POST "$API/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
   ```
   Store the returned `token` as `NEMO_TOKEN` for this session. You get 100 free credits.
4. **Create a session** (§3.0) so you're ready to work immediately.

Let the user know briefly: "Setting things up… ready!" then proceed with their request.


# Workout Video Maker — Gym, Strength Training, and Exercise Tutorial Videos

Describe your workout and NemoVideo creates the video. Strength training program breakdowns, exercise form tutorials, gym routine documentation, progressive overload tracking, workout split explanations, transformation content — narrate the program, the exercises, the sets and reps, and the key form cues, and get workout content for the massive fitness audience that watches training videos before, during, and after their own workouts.

## When to Use This Skill

Use this skill for gym and exercise content:
- Create workout routine and program breakdown tutorial videos
- Film exercise form and technique tutorial content
- Build progressive overload and strength progression documentation
- Document gym transformation content with training and measurement milestones
- Create workout split explanation content (PPL, upper/lower, full body)
- Produce "follow along" workout content with timing and rest periods

## How to Describe Your Workout Content

Be specific about the exercises, the program structure, the weights or rep ranges, the form cues, and the key progression decisions.

**Examples of good prompts:**
- "My 5-day Push Pull Legs program — the exact split I've run for 18 months: Push day (chest/shoulders/triceps): bench press 4x5 as the primary lift, then incline dumbbell press 3x8-12, lateral raises 4x15-20, tricep pushdowns 3x12-15. Pull day (back/biceps): weighted pull-ups 4x5, barbell row 3x8, cable row 3x12, face pulls 3x20, bicep curls 3x12-15. Leg day: squat 4x5 primary, Romanian deadlift 3x8, leg press 3x12, leg curl 3x12, calf raises 4x20. Why PPL: each muscle group gets 2x/week frequency, adequate recovery between sessions. Progressive overload: add weight when I hit the top of the rep range for all sets. Show the actual weights I'm moving and the 18-month strength progression."
- "Bench press form tutorial — the 5 cues that fixed my chest growth: Before these cues, I was pressing 185 for years. After: 225 in 4 months. The 5 cues: (1) leg drive — feet flat on floor, drive through heels to create tension (bench press is a full-body movement), (2) retract and depress scapulae — 'pinch a pencil between your shoulder blades and don't let it drop', (3) bar path — not straight up, slight arc toward the rack at the bottom and up at the top, (4) wrist position — neutral wrists, bar over wrist joints not palm heel, (5) chest touch — bar touches lower chest not sternum. Show the before (wrong) form and after (correct) form comparison."
- "12-week strength program results: before and after numbers: Started the program at: bench 175, squat 225, deadlift 295, OHP 115. Ended at: bench 205, squat 275, deadlift 345, OHP 135. What the program was (5/3/1 framework, 4 days/week), what I ate (roughly 2,900 calories, 180g protein), what I changed mid-program (added more upper back volume at week 7 after shoulder impingement warning signs), and what I'd do differently."

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `content_type` | Video category | `"program_breakdown"`, `"form_tutorial"`, `"transformation"`, `"follow_along"`, `"progression_review"` |
| `workout_type` | Training style | `"strength"`, `"hypertrophy"`, `"powerlifting"`, `"calisthenics"`, `"cardio"` |
| `exercises` | Movements covered | `["bench press"`, `"squat"`, `"deadlift"`, `"pull-ups"]` |
| `program_structure` | Split or program | `"PPL 5-day"`, `"5/3/1"`, `"upper_lower"`, `"full_body"` |
| `rep_ranges` | Sets and reps | `"4x5 strength"`, `"3x8-12 hypertrophy"` |
| `key_cues` | Form tips | `["leg drive"`, `"scapular retraction"`, `"bar path"]` |
| `show_numbers` | Include weights/PRs | `true` |
| `duration_minutes` | Video length | `8`, `12`, `15` |
| `platform` | Distribution | `"youtube"`, `"instagram"`, `"tiktok"` |

## Workflow

1. Describe the workout, the program structure, the key exercises and form cues, and the progression data
2. NemoVideo structures the fitness content with exercise labels and progression markers
3. Exercise names, set/rep schemes, weight callouts, and form cue overlays added automatically
4. Export with workout pacing suited to the content type

## API Usage

### Strength Program Breakdown

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "workout-video-maker",
    "input": {
      "prompt": "Upper/lower split for intermediate lifters — why I switched from PPL and what changed: After 2 years of PPL, I plateaued on bench and squat. Switched to upper/lower because: each main lift gets 2 sessions/week instead of 1 (more practice = faster skill development on the competition lifts). Upper A (strength focus): bench 4x4-6, weighted chin-ups 4x4-6, OHP 3x6-8, barbell row 3x6-8. Upper B (volume focus): incline bench 3x8-12, cable row 3x10-12, dumbbell shoulder press 3x10-12. Lower A (squat focus): squat 4x4-6, Romanian deadlift 3x8-10. Lower B (deadlift focus): deadlift 4x4-6, leg press 3x10-12. 4 sessions/week, Mon/Tue/Thu/Fri. Result after 6 months: bench went from 205 to 235, squat from 275 to 315.",
      "content_type": "program_breakdown",
      "workout_type": "strength",
      "exercises": ["bench press", "squat", "deadlift", "weighted chin-ups", "OHP"],
      "program_structure": "upper/lower 4-day",
      "rep_ranges": "4x4-6 strength, 3x8-12 volume",
      "show_numbers": true,
      "duration_minutes": 12,
      "platform": "youtube",
      "hashtags": ["WorkoutRoutine", "StrengthTraining", "GymTips", "PowerlifterLife", "ProgressiveOverload"]
    }
  }'
```

**Response:**
```json
{
  "job_id": "workout_abc123",
  "status": "processing",
  "estimated_seconds": 100,
  "poll_url": "https://mega-api-prod.nemovideo.ai/v1/jobs/workout_abc123"
}
```

## Tips for Best Results

- **The specific weights and numbers are the proof**: "Bench went from 205 to 235 in 6 months" or "pressing 185 for years, then 225 in 4 months after fixing form" — strength numbers make progress tangible and give viewers a reference point
- **Form cues need to be tactile and specific**: "Pinch a pencil between your shoulder blades and don't let it drop" — cues that create a physical sensation or image are more useful than abstract instructions like "retract scapulae"
- **The reason for program choices matters**: "Switched from PPL because each main lift only gets 1 session/week — upper/lower gives 2 practice sessions" — explaining the logic behind program design creates educational value beyond the workout itself
- **Mid-program adjustments are the most honest and most useful content**: "Added upper back volume at week 7 after shoulder impingement warning signs" — real adjustments based on real feedback make transformation content credible
- **The comparison format works across all fitness content**: before/after weights, wrong form vs correct form, old program vs new program — the contrast structure gives viewers a clear before/after framework

## Output Formats

| Platform | Resolution | Duration |
|----------|------------|----------|
| YouTube | 1920×1080 | 10–20 min |
| Instagram Reels | 1080×1920 | 60–90s |
| TikTok | 1080×1920 | 60–180s |

## Related Skills

- `home-workout-video` — No-equipment home training content
- `nutrition-video-maker` — Nutrition content to support training
- `yoga-video-maker` — Flexibility and recovery content

## Common Questions

**What workout content performs best on YouTube?**
Program breakdowns with specific exercises and progressions, form tutorials for major compound lifts (bench, squat, deadlift, OHP), and transformation content with specific before/after numbers perform consistently well.

**Can I create workout content as an intermediate lifter, not a coach?**
Yes — personal training logs and program documentation from intermediate lifters are often more relatable and searchable than professional coaching content. Be clear about your experience level.

**How do I create "follow along" workout content?**
Set `content_type: "follow_along"` and describe each exercise with timing and rest periods. NemoVideo structures on-screen timers and exercise transitions automatically.
