# Memory Structure for Autoresearch

How to organize autoresearch data across your workspace files.

## Directory Layout

```
workspace/
├── SOUL.md                    ← Contains AUTO:CHAMPION block (current strategy)
├── MEMORY.md                  ← Contains AUTO:MEMORY block (active learnings, max 20)
├── experiments/
│   ├── active.md              ← Current experiment (exactly 0 or 1 file)
│   ├── archive/               ← Completed experiments
│   │   ├── EXP-001.md
│   │   ├── EXP-002.md
│   │   └── ...
│   └── meta.json              ← Experiment metadata & counters
```

## meta.json

Track global experiment state:

```json
{
  "next_id": 6,
  "champion_version": 3,
  "primary_metric": "views_48h",
  "baseline": 1450,
  "baseline_posts": ["post_a", "post_b", "post_c", "...last 10"],
  "kill_streak": 0,
  "total_experiments": 5,
  "total_keeps": 2,
  "total_kills": 2,
  "total_modifies": 1,
  "experiment_paused": false,
  "pause_until": null,
  "last_evaluation": "2025-01-31"
}
```

## SOUL.md Champion Block

The strategy your agent follows. Updated ONLY on KEEP verdicts.

```markdown
<!-- AUTO:CHAMPION START v3 -->
## Content Strategy (Champion v3)
**Primary Metric:** views_48h
**Baseline:** 1450 avg (last 10 posts)
**Strategy:**
- Hook: Storytelling opening
- Length: 60-90 seconds
- Post time: 10am ET weekdays
- Topics: AI tutorials, code walkthroughs
- Thumbnail: Text overlay with key phrase
**Changelog:**
- v3: Storytelling hooks (+18% views, EXP-003)
- v2: 10am posting time (+12% views, EXP-002)
- v1: Initial strategy (baseline established)
<!-- AUTO:CHAMPION END -->
```

### Rules for Champion Block

1. Only modify content between `AUTO:CHAMPION START` and `AUTO:CHAMPION END` markers
2. Always increment version number on KEEP
3. Keep changelog to last 10 entries, archive older ones
4. Baseline must reflect actual data, not aspirational numbers
5. Strategy bullets should be concrete and actionable, not vague

## MEMORY.md Autoresearch Block

Active learnings. The distilled wisdom from experiments.

```markdown
<!-- AUTO:MEMORY START -->
## Autoresearch Learnings

### What Works
- Storytelling hooks: +18% views vs question hooks (EXP-003, 2025-01-17)
- 10am ET posting: +12% views vs random times (EXP-002, 2025-01-10)
- Text on thumbnails: +8% CTR (EXP-001, 2025-01-03)

### What Doesn't Work
- Clickbait hooks: -22% views, higher bounce (EXP-004, 2025-01-24)
- Posts > 2min: -15% completion rate (EXP-005, 2025-01-31)

### Observations (not yet tested)
- Weekend posts seem to get lower engagement (need formal test)
- Clips with code on screen might retain better (queue for experiment)

**Stats:** 5 experiments | 2 keeps | 2 kills | 1 modify | Champion v3
<!-- AUTO:MEMORY END -->
```

### Rules for Memory Block

1. Max 20 total entries across all sections
2. Each entry: one line, includes metric delta, experiment ID, and date
3. When at 20 entries, archive the oldest to `experiments/archive/learnings-archive.md`
4. "Observations" section for hypotheses to test — max 5 entries
5. Stats line at bottom for quick reference

## Archival Rules

### When to Archive

- After each verdict: move completed experiment from `active.md` to `archive/EXP-XXX.md`
- When memory block hits 20 entries: move oldest 5 to archive
- Monthly: review archive, delete experiments older than 6 months unless they contain
  still-relevant learnings

### Archive Format

Archived experiments keep their full format (see experiment-template.md).
Add a summary section at the top:

```markdown
## Summary
- **Result:** KEEP — storytelling hooks adopted as champion strategy
- **Impact:** +18% views (1200 → 1416 avg)
- **Duration:** 2025-01-15 to 2025-01-17
```

### What NOT to Keep in Active Memory

- Raw metric values for individual posts (keep in experiment files)
- Experiment hypotheses that were tested and resolved
- Platform-specific implementation details
- Temporary debug notes

## Baseline Management

The baseline is the rolling average of your last 10 champion-strategy posts.

### Updating Baseline

On KEEP verdict:
1. New champion strategy is now the baseline strategy
2. Posts from the successful experiment become the first data points
3. Continue adding new posts until you have 10
4. Only then start a new experiment

On KILL verdict:
1. Baseline stays the same
2. Experimental posts are NOT added to baseline
3. Resume posting with champion strategy

### Cold Start

If you have no baseline yet:
1. Set initial champion strategy based on best guess / user input
2. Post 10 pieces of content with this strategy
3. Calculate baseline from these 10 posts
4. NOW you can start experimenting

**Do not run experiments before establishing a baseline.** You need something to compare against.
