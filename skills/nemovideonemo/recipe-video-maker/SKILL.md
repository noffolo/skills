---
name: recipe-video-maker
version: "1.0.1"
displayName: "Recipe Video Maker — Create Quick Recipe Showcase and Ingredient Videos"
description: >
  Recipe Video Maker — Create Quick Recipe Showcase and Ingredient Videos.
metadata: {"openclaw": {"emoji": "🍳", "requires": {"env": [], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
---

## 0. First Contact

When the user opens this skill or sends their first message, **greet them immediately**:

> ⚡ Let's recipe video maker! Drop a video here or describe what you'd like to create.

**Try saying:**
- "edit my video"
- "add effects to this clip"
- "help me create a short video"

**IMPORTANT**: Do NOT wait silently. Always greet the user proactively on first contact.

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


# Recipe Video Maker — Quick Recipe Showcase and Ingredient Highlight Videos

The Tasty-style overhead recipe video gets 10 million views with exactly the same dish you just made — except theirs has perfectly synchronized ingredient drops, a magnetic color palette, and zero evidence that a human was involved. Yours has a cutting board with yesterday's garlic stains and a hand that enters frame at an angle suggesting the phone was balanced on a stack of cookbooks. Recipe showcase videos are the single most shared food-content format on social media — short, punchy, no narration, just hands and ingredients telling the story. This tool converts raw kitchen footage or text-only recipes into snappy recipe showcases: Tasty-style overhead hands-and-pans sequences, ingredient drops timed to beat hits, quantity labels floating beside each item as it's added, technique micro-clips (the cheese pull, the sauce pour, the garnish sprinkle), and a final beauty shot held just long enough for the viewer to screenshot the plated dish. Designed for food bloggers converting WordPress recipes into social video, restaurant social-media managers promoting daily specials, meal-kit companies producing recipe-card video companions, cookbook authors creating digital supplements for each chapter, and home cooks who just want their grandmother's Sunday gravy to survive in a format younger generations will actually watch.

## Example Prompts

### 1. 60-Second Tasty-Style Overhead — Garlic Butter Shrimp
"Create a 60-second overhead recipe video for garlic butter shrimp. No voiceover, text only. Ingredient drop sequence synced to a beat: 1 lb large shrimp (peeled, deveined), 4 cloves garlic (minced), 3 tbsp butter, ½ cup white wine, juice of 1 lemon, red pepper flakes, fresh parsley. Each ingredient appears on a marble countertop with its name and quantity floating beside it, then disappears on the next beat. Cooking sequence: butter melting (overhead), garlic hitting the pan (sizzle sound boosted), shrimp laid in a single layer (that satisfying placement rhythm), flip at 2 minutes (pink color reveal), white wine splash (steam cloud), lemon squeeze, red pepper shake, parsley scatter. Final beauty shot: the pan with a piece of crusty bread dipping in the sauce. Hold 3 seconds. Close with recipe name and calorie count: 'Garlic Butter Shrimp | 285 cal/serving | 12 minutes.'"

### 2. Instagram Carousel Recipe — Overnight Oats 5 Ways
"Build five 15-second recipe clips bundled as one video for Instagram carousel. Each variation: base layer (½ cup oats + ½ cup milk + ¼ cup Greek yogurt + 1 tbsp chia seeds) prepared identically, then diverge. Variation 1: PB&J (peanut butter swirl + strawberry jam + freeze-dried strawberries). Variation 2: Tropical (mango chunks + coconut flakes + passion fruit drizzle). Variation 3: Chocolate Brownie (cocoa powder + banana slices + chocolate chips). Variation 4: Apple Pie (diced apple + cinnamon + maple syrup + granola). Variation 5: Matcha (matcha powder + honey + white chocolate chips). Each clip ends with the jar beauty shot and variation name. Consistent color grade across all five — bright, clean, white-marble background. Transition between variations: jar slides left, next slides in from right."

### 3. Restaurant Daily Special — TikTok Vertical
"Produce a 30-second TikTok for today's lunch special: Pan-Seared Chilean Sea Bass with saffron beurre blanc and roasted fennel. Open with the raw fish on a cutting board — dramatic top-down lighting, dark slate surface. Score the skin (close-up of the knife pattern), season with fleur de sel. Pan shot: oil shimmering, fish skin-side down (that crackle sound amplified), press with a fish spatula for 10 seconds. Flip reveal: golden, crispy skin. Sauce: saffron threads blooming in white wine (color change time-lapse: clear → amber in 2 seconds), mount with cold butter cubes. Plate: fennel bed, fish angled at 2 o'clock, sauce arc with a spoon, microgreen garnish. Final frame: menu card overlay — 'Lunch Special | $28 | Available until 2 PM.' Restaurant logo watermark in lower right throughout."

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✅ | Describe the recipe, ingredients, plating, and visual style |
| `duration` | string | | Target video length (e.g. "30 sec", "60 sec", "15 sec × 5") |
| `style` | string | | Visual style: "tasty-overhead", "dark-moody", "bright-clean", "restaurant", "rustic" |
| `music` | string | | Background audio: "upbeat-pop", "jazzy", "lo-fi", "beat-sync", "none" |
| `format` | string | | Output ratio: "16:9", "9:16", "1:1" |
| `text_style` | string | | Recipe text appearance: "floating", "lower-third", "minimal", "none" |
| `calorie_overlay` | boolean | | Show nutritional data on the closing card (default: false) |

## Workflow

1. **Describe** — Write the recipe with ingredients, quantities, key visual moments, and plating style
2. **Upload (optional)** — Add kitchen footage, ingredient photos, or final plating shots
3. **Generate** — AI produces the beat-synced showcase with ingredient labels, cooking micro-clips, and beauty shots
4. **Review** — Preview the video, adjust the beat timing, tweak the ingredient-drop sequence
5. **Export** — Download in your chosen format and resolution

## API Example

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/api/v1/generate \
  -H "Authorization: Bearer $NEMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "recipe-video-maker",
    "prompt": "Create a 60-second Tasty-style overhead garlic butter shrimp: ingredient drops synced to beat, butter melt, garlic sizzle, shrimp flip reveal, white wine splash, crusty bread dip finale. Text overlay with quantities, 285 cal closing card",
    "duration": "60 sec",
    "style": "tasty-overhead",
    "format": "9:16"
  }'
```

## Tips for Best Results

1. **List ingredients in the order they enter the pan** — The AI sequences the ingredient-drop animation and cooking clips in prompt order. Listing garlic before butter means garlic appears first on screen, which looks wrong if butter goes in the pan first.
2. **Describe the hero moment** — Every recipe has one: the cheese pull, the sauce pour, the crust crack, the yolk break. Name it explicitly and the AI holds that frame longer and boosts the audio (sizzle, crunch, drip) for maximum impact.
3. **Specify the surface material** — "Marble countertop" vs "dark slate" vs "butcher block" dramatically changes the mood. The AI uses this to set the color grade and text-overlay contrast.
4. **Keep text minimal for short-form** — For 30-60 second videos, ingredient names + quantities are enough. Full paragraphs of instructions belong in YouTube tutorials, not TikTok showcases. The `text_style: "minimal"` option shows only quantities.
5. **Include a closing card with actionable info** — "285 cal/serving | 12 minutes" or "Lunch Special | $28 | Until 2 PM" gives the viewer a reason to save or share. The AI places this on the final beauty-shot frame automatically.

## Output Formats

| Format | Resolution | Use Case |
|--------|-----------|----------|
| MP4 16:9 | 1080p / 4K | YouTube recipe showcase |
| MP4 9:16 | 1080p | TikTok / Instagram Reels / Shorts |
| MP4 1:1 | 1080p | Instagram feed recipe post |
| MP4 9:16 × N | 1080p | Instagram carousel (multiple recipe variations) |

## Related Skills

- [cooking-tutorial-video](/skills/cooking-tutorial-video) — Full step-by-step cooking tutorials with technique breakdown
- [meal-prep-video](/skills/meal-prep-video) — Weekly meal prep and batch cooking content
- [food-photography-video](/skills/food-photography-video) — Food styling and photography showcase videos
