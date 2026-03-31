---
name: pet-adoption-video
version: 1.0.3
displayName: "Pet Adoption Video Maker"
description: >
  Describe your rescue animal and NemoVideo creates the adoption video. Shy shelter dogs, bottle-fed kittens, bonded pairs waiting together, senior pets often overlooked — tell their story and get an adoption appeal video that drives applications and saves lives.

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

> 📹 Ready to pet adoption video! Just send me a video or describe your project.

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
   curl -s -X POST "https://mega-api-prod.nemovideo.ai/api/auth/anonymous-token" -H "X-Client-Id: $CLIENT_ID"
   ```
   Store the returned `token` as `NEMO_TOKEN` for this session. You get 100 free credits.
4. **Create a session** (§3.0) so you're ready to work immediately.

Let the user know briefly: "Setting things up… ready!" then proceed with their request.


# Pet Adoption Video Maker — Create Advocacy and Fundraising Content for Rescue Animals

Describe your rescue animal and NemoVideo creates the adoption video. Shy shelter dogs, bottle-fed kittens, bonded pairs waiting together, senior pets often overlooked — tell their story and get an adoption appeal video that drives applications and saves lives.

## When to Use This Skill

Use this skill for pet adoption and rescue advocacy content:
- Create individual animal adoption profile videos for shelters and rescues
- Build "featured pet of the week" social media content for animal organizations
- Film foster family updates showing an animal's progress and personality
- Create "before and after rescue" transformation videos
- Produce fundraising appeal videos for rescue operations and medical cases
- Build awareness content for senior pets, bonded pairs, or long-stay animals

## How to Describe the Animal's Story

Be specific about the animal's history, personality quirks, and what their ideal home looks like.

**Examples of good prompts:**
- "Shelter dog: 3-year-old pit bull mix named Waffles, been at the shelter 6 months (long stay). She was found as a stray, terrified when she arrived. Now she's the staff favorite — does a happy spin every time someone comes in. She's cat-selective but great with kids. Loves car rides. She just needs someone to give her a chance."
- "Bonded senior cat pair: siblings Mochi and Soba, 12 years old. Their owner passed away. They've never been separated. Mochi is outgoing and chatty, Soba is shy but follows Mochi everywhere. They sleep curled together. Can't be adopted separately. Looking for a quiet home that understands senior cats."
- "Medical foster update: bottle baby kitten Tadpole, found alone at 3 days old, being tube-fed every 2 hours. Now 3 weeks old, eyes open, wobbling around, has personality. Will be ready for adoption in 5 weeks. Fundraiser to cover vet costs — show the journey."

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `content_type` | Video purpose | `"adoption_profile"`, `"fundraiser"`, `"foster_update"`, `"transformation"`, `"awareness"` |
| `animal_name` | Pet's name | `"Waffles"`, `"Tadpole"` |
| `species` | Animal type | `"dog"`, `"cat"`, `"rabbit"`, `"guinea_pig"` |
| `animal_story` | Background | `"found as stray"`, `"owner surrender"`, `"long-stay shelter"` |
| `personality` | Character traits | `"shy but warms up"`, `"staff favorite"`, `"loves car rides"` |
| `include_cta` | Call to action | `"apply_to_adopt"`, `"foster_inquiry"`, `"donate"` |
| `tone` | Emotional approach | `"hopeful"`, `"urgent"`, `"heartwarming"`, `"educational"` |
| `duration_seconds` | Video length | `60`, `90`, `120` |
| `platform` | Target platform | `"instagram"`, `"facebook"`, `"petfinder"`, `"youtube"` |

## Workflow

1. Describe the animal's story, personality, and ideal home
2. NemoVideo structures the adoption narrative (background → personality → appeal)
3. Animal name, shelter info, and adoption CTA overlaid automatically
4. Export with tone-matched music that supports the emotional appeal

## API Usage

### Shelter Dog Adoption Profile

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "pet-adoption-video",
    "input": {
      "prompt": "Shelter dog Waffles, 3-year-old pit bull mix, 6 months at the Austin Animal Center. She came in as a stray, fearful, shut down in her kennel. Now she wiggles her whole body when staff come in, does a little spin, loves belly rubs. Great with kids (tested), dog-selective (needs slow introductions). Loves car rides and hiking. She is a 10/10 dog who just needs someone to see past the breed.",
      "content_type": "adoption_profile",
      "animal_name": "Waffles",
      "species": "dog",
      "animal_story": "long-stay stray",
      "personality": "shelter favorite, wiggle butt, loves adventures",
      "include_cta": "apply_to_adopt",
      "tone": "hopeful",
      "duration_seconds": 90,
      "platform": "instagram",
      "hashtags": ["AdoptDontShop", "PitBullsOfInstagram", "ShelterDog", "AdoptMe", "AustinAnimals"]
    }
  }'
```

**Response:**
```json
{
  "job_id": "adopt_ghi789",
  "status": "processing",
  "estimated_seconds": 90,
  "poll_url": "https://mega-api-prod.nemovideo.ai/v1/jobs/adopt_ghi789"
}
```

### Senior Bonded Pair Awareness Video

```bash
curl -X POST https://mega-api-prod.nemovideo.ai/v1/run \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "pet-adoption-video",
    "input": {
      "prompt": "Senior bonded cat siblings Mochi and Soba, 12 years old, owner passed away. They have never been separated in 12 years. Mochi is chatty and outgoing, greets everyone. Soba is shy but always within 3 feet of Mochi. They sleep touching. They groom each other. Separating them would break them. Looking for a quiet home that appreciates senior cats — they are not high maintenance, they are just loyal.",
      "content_type": "awareness",
      "animal_name": "Mochi and Soba",
      "species": "cat",
      "animal_story": "bonded senior pair, owner passed",
      "personality": "devoted to each other, gentle, low-key",
      "include_cta": "apply_to_adopt",
      "tone": "heartwarming",
      "duration_seconds": 90,
      "platform": "facebook"
    }
  }'
```

## Tips for Best Results

- **Personality over breed**: "Does a happy spin when you come in" says more than "friendly dog" — specific behaviors are what drive adoption applications
- **Address the hesitation**: Mention what might make someone skip this pet and reframe it — "cat-selective" becomes "does great with slow introductions"
- **Senior and long-stay pets need extra story**: They've been passed over — their video needs more story, more personality, more reason to stop scrolling
- **The CTA must be actionable**: Set `include_cta` and include the shelter name/link in the prompt — "Apply at Austin Animal Center, link in bio" drives real applications
- **Tone shapes sharing**: `hopeful` gets adopted shares; `urgent` gets rescue-community shares; `heartwarming` gets general public shares

## Output Formats

| Platform | Resolution | Duration |
|----------|------------|----------|
| Instagram Reels | 1080×1920 | 60–90s |
| Facebook | 1920×1080 | 60–120s |
| Petfinder | 1920×1080 | 60–90s |
| YouTube | 1920×1080 | 2–5 min |

## Related Skills

- `cat-video-maker` — General cat content beyond adoption
- `dog-training-video` — Show adoptable dogs' training ability
- `food-vlog-maker` — Fundraiser event content
- `tiktok-content-maker` — Short adoption advocacy clips

## Common Questions

**Can shelters create videos for every animal in their intake?**
Yes — describe each animal's story and personality in separate API calls. Shelters with high intake volumes can use the batch API to generate adoption profiles at scale.

**Does it include the shelter's contact information?**
Include the shelter name, location, and application link in the prompt. NemoVideo overlays this as a CTA card at the end of the video.

**What makes an adoption video actually drive applications?**
Specific personality moments (the spin, the slow blink, the wiggle butt) — not generic "loving and sweet." The viewer needs to picture this specific animal in their home.
