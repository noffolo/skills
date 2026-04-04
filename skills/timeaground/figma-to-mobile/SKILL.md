---
name: figma-to-mobile
description: >
  Convert Figma designs to mobile UI code.
  Supports Android (Jetpack Compose, XML) and iOS (SwiftUI, UIKit).
  Use when a user provides a Figma link and wants mobile layout code.
  Extracts design tokens via Figma REST API, asks clarifying questions,
  then generates production-ready code files.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"], "env": ["FIGMA_TOKEN"] },
        "primaryEnv": "FIGMA_TOKEN",
        "install":
          [
            {
              "id": "python-requests",
              "kind": "shell",
              "command": "pip3 install requests",
              "label": "Install Python requests package",
            },
          ],
      },
  }
---

# Figma to Mobile

Convert Figma designs to mobile UI code with interactive clarification.

Supported: Android Compose, Android XML, iOS SwiftUI, iOS UIKit.

## Prerequisites

- `FIGMA_TOKEN` environment variable set (Figma > Settings > Personal Access Tokens)
- Python 3.8+ with `requests` package

## Trigger & Input

This skill activates when a user provides a Figma link.

The user may also include **inline hints** alongside the link, such as:
- Target platform: "Android XML", "Compose", "SwiftUI", "UIKit"
- Layout preferences: "use ConstraintLayout", "prefer StackView"
- Component notes: "the switch is our custom CompactSwitch", "this is a dynamic list"
- Any other context about the design

**If the user provides hints, respect them and skip the corresponding questions.**
For example, if the user says "Android XML, the 3 cards are a RecyclerView list", do NOT ask about output format or whether the cards are dynamic/static.

## Workflow

### Step 1: Fetch & Analyze

When user provides a Figma link:

1. Run `scripts/figma_fetch.py "<url>"` to get design data
   If the user provides multiple Figma links (different states of the same page), use `--compare` mode to fetch all and get a diff summary. This helps generate multi-state code (selector drawables, conditional styling, etc.)
2. Analyze the structure: identify sections, repeated patterns, component types
3. Note INSTANCE nodes — they indicate reusable components. Check `variantProperties` for component state (e.g. State=Default, Size=Large) — these map to multi-state code
4. Note gradient/shadow data — flag for the user if complex
5. Apply Figma node interpretation rules before generating code

**Detailed interpretation rules**: Read `references/figma-interpretation.md`

### Step 1.5: Structure Summary

Before asking any questions, present a brief **structure summary** to the user so they can confirm your understanding:

> I see: [navigation bar with back button + title] → [2 content sections: user profile card, settings list (8 items)] → [bottom action button]. Total ~25 nodes.

Keep it to 2-3 lines. Mention:
- Major sections identified (nav bar, content areas, footer)
- Repeated patterns ("8 similar list items", "3 tab labels")
- Notable elements (gradients, complex illustrations, stacked cards)

If the user says "that's wrong" or corrects the structure, adjust understanding before proceeding to Step 2.

If the structure is simple and obvious (e.g., a single card with a few text fields), skip this step.

### Step 2: Confirm & Clarify

**Question priority (strict order — ask earlier questions first):**

1. **Output format** (MUST ask first unless user already specified)
   → Android XML / Compose / SwiftUI / UIKit
   This determines all subsequent analysis phrasing and code output.

2. **Structural ambiguities** (only ask what you're genuinely unsure about)
   → "These N items look similar — dynamic list or fixed layout?"
   → "This area: single image asset or icon-on-background combo?"

3. **Component choices** (only if platform-relevant)
   → "Any custom components to use? (otherwise I'll use platform defaults)"

**Rules for questions:**
- Skip any question the user already answered via inline hints
- Max 3-5 questions total, fewer is better
- Each question gives concrete options with one-line pros/cons
- Every question includes an open option: "or tell me more about this"
- Use natural language, no JSON or technical dumps
- If everything is clear (user gave full context + simple structure), skip Step 2 entirely

**Confidence guide — when to ask vs. when to just generate:**
- ≥3 sibling nodes with similar structure → likely a list → ASK (dynamic vs static)
- INSTANCE nodes sharing same componentId → reusable component → MENTION but can default
- Single clear hierarchy, no ambiguity → high confidence → SKIP questions, go to Step 3
- Gradient/complex shadow in design → MENTION in summary ("I see a gradient here, I'll approximate it as X")

### Step 2.5: Project Scan (optional but recommended)

If the target project is available locally, run a project scan:

```bash
python scripts/project_scan.py /path/to/project --json --output scan-report.json
```

**How to use scan results in code generation**: Read `references/scan-usage.md`

### Step 3: Generate Code

After user confirms (or if no questions needed), generate code files.

**Detailed generation rules**: Read `references/generation-rules.md`

If multiple files are needed, output each with a clear filename header:
```
📄 activity_notification_settings.xml
[code]

📄 item_expert_notification.xml
[code]
```

### Step 4: Iterate & Capture Feedback

After showing code, ask briefly:
> Matches the design? Any adjustments?

**The user can then give feedback to refine the output.** Common iterations:
- "间距大了" → adjust specific spacing
- "Switch 换成我们的 CustomSwitch" → swap component
- "把标题栏去掉" → remove section
- "换成 Compose 版本" → regenerate in different format
- "颜色不对，这里应该是 #333333" → fix specific values

Continue iterating until the user is satisfied. Each round only regenerates the changed parts, not the entire file (unless the user asks for full regeneration).

**Feedback capture (automatic):**
Whenever the user corrects your generated output, log the correction to `feedback-log.md` in the project root (create if it doesn't exist). Each entry follows this format:

```
## YYYY-MM-DD HH:MM
- **Platform**: Android XML / Compose / SwiftUI / UIKit
- **Figma node type**: (e.g., FRAME with icon, Tab bar, Button group)
- **Issue**: Brief description of what was wrong
- **Before**: What the agent generated (snippet or description)
- **After**: What the user wanted (snippet or description)
- **Rule candidate**: (optional) If this correction suggests a general pattern rule, note it here
```

Log entries should be:
- **Concise** — only the relevant diff, not entire files
- **Categorized** — always include platform and Figma node type for later analysis
- **Actionable** — focus on the mapping error, not cosmetic preferences (e.g., "user prefers 16dp" is not a rule; "VECTOR compositions should be single ImageView" is)

Do NOT log:
- One-off personal preferences (specific color choices, naming conventions)
- Corrections to non-mapping issues (typos, import statements)
- Feedback the user explicitly says is project-specific, not general

Periodically (or when asked), run `scripts/feedback_analyze.py` to identify patterns and generate rule candidates.

## Error Handling

- **FIGMA_TOKEN not set** (script outputs `FIGMA_TOKEN_NOT_SET`) → do NOT ask user to run commands. Instead:
  1. Tell the user you need a Figma Personal Access Token
  2. Tell them where to get it: Figma → avatar (top-left) → Settings → Security → Personal Access Tokens
  3. Ask them to paste the token in chat
  4. Once they provide it (starts with `figd_`), write it to the project root `.env` file: `echo 'FIGMA_TOKEN=figd_xxx' >> .env`
  5. Retry the figma_fetch command — it will read from `.env` automatically
- **FIGMA_TOKEN invalid** (API returns 403/401) → token may have expired or been revoked. Ask user to regenerate and paste new token. Update `.env` file.
- **Invalid URL** → show valid URL example: `https://www.figma.com/design/<fileKey>/<name>?node-id=<id>`
- **API error** → show error message, suggest checking network/proxy
- **Node too large (>200 children)** → suggest selecting a smaller frame
- **Depth auto-increased** → the script auto-retries with deeper depth if it detects truncated children. Inform user if this happens ("I needed to fetch deeper to get all details").
