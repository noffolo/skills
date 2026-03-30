# Experiment Template

Copy this file to `experiments/active.md` when starting a new experiment.
Only ONE active experiment at a time.

---

```markdown
# EXP-XXX: [One-line description of what you're testing]

**Status:** ACTIVE
**Variable:** [The ONE thing being changed, e.g., hook_style, post_time, content_length]
**Mutation:** [New value] (was: [old value from champion])
**Champion Version:** v[N]
**Created:** YYYY-MM-DD
**Evaluation Date:** YYYY-MM-DD  (created + evaluation_window)
**Evaluation Window:** 48h | 24h | 7d (depends on content type)

## Hypothesis
[Why you think this mutation might improve the primary metric. One sentence.]

## Posts
| Post ID | Posted At | Platform | Variant Used |
|---------|-----------|----------|-------------|
| | | | |

## Metrics (filled during evaluation)
| Post ID | Primary Metric Value | Collected At |
|---------|---------------------|-------------|
| | | |

**Experiment Average:** [calculated]
**Champion Baseline:** [from SOUL.md]
**Delta:** [experiment_avg - baseline]
**Improvement:** [delta / baseline as %]

## Verdict
**Decision:** KEEP / MODIFY / KILL
**Rationale:** [One sentence explaining the decision based on data]
**Threshold Used:** ±10% (default)

## Actions Taken
- [ ] Updated SOUL.md champion block (KEEP only)
- [ ] Updated MEMORY.md learnings
- [ ] Archived to experiments/archive/EXP-XXX.md
- [ ] Updated baseline (KEEP only)
- [ ] Reset kill_streak (KEEP only) / Incremented kill_streak (KILL only)

## Variant Details (if A/B testing hooks)
**Variants Generated:**
1. [variant 1]
2. [variant 2]
3. [variant 3]
**Selected:** Variant [N]
**Rationale:** [Why this variant was chosen for testing]
```

---

## Naming Convention

- Format: `EXP-XXX` where XXX is zero-padded sequential number
- Example: `EXP-001`, `EXP-012`, `EXP-100`
- Find the next number by checking `experiments/archive/` for the highest existing ID

## Status Transitions

```
PROPOSED  → ACTIVE      (when first post goes out)
ACTIVE    → EVALUATING  (when evaluation_date arrives)
EVALUATING → KEEP       (improvement ≥ threshold)
EVALUATING → MODIFY     (within noise band, can extend ONCE)
EVALUATING → KILL       (regression ≥ threshold)
MODIFY    → KEEP/KILL   (after extension period)
```

## Evaluation Windows by Content Type

| Content Type | Default Window | Min Posts | Notes |
|---|---|---|---|
| Video clips | 48h after last post | 3 | Views stabilize quickly |
| Tweets/posts | 24h after last post | 5 | High volume, fast feedback |
| Blog posts | 7d after last post | 2 | Slow traffic curve |
| Newsletter | Per-send (open rate) | 2 | Metric available immediately |
| Podcasts | 7d after publish | 1 | Download curves are slow |
