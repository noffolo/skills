# Auto-Apply Configuration

This file defines which categories Lucid is allowed to auto-apply without human review.

Only changes with **HIGH confidence** are ever auto-applied — regardless of category.
Medium and low confidence always require human approval.

> **All categories are disabled by default. Enable only after reviewing several nights of output.**

## ❌ Disabled Categories (opt-in — enable by moving to Enabled section below)

Edit this list to enable categories you trust after reviewing Lucid's output.

### Safe (factual, no opinions)
- **Version numbers** — skill/plugin tables clearly outdated
- **Stale Cron IDs** — cron was explicitly removed/replaced in notes
- **Service/port deletions** — clearly documented as removed
- **New project entries** — complete details (URL, repo, path, service) mentioned on 2+ days
- **Infrastructure facts** — new cron IDs, script paths, service names, port assignments
- **Lessons Learned** — purely factual technical lessons (not preferences or opinions)
- **Model Strategy** — agent counts, new agent entries when clearly documented with model + alias
- **Closed Open Loops** — remove resolved items when explicit closure signal exists on 2+ days
- **Stale project status** — update "planning"/"in progress" to "live" when URL + service confirmed on 2+ days

## ✅ Enabled Categories

*(Empty by default — move items here from the Disabled section above to enable them.)*

## ❌ Never Auto-Apply (hardcoded)

These are always manual regardless of confidence:

- Belief Updates (opinions, model preferences, strategy changes)
- Key Decisions
- Family/personal facts
- User preferences or communication style
- Anything you are uncertain about
- Anything with medium or low confidence

## Customization Examples

**Minimal setup** (only version numbers + new projects):
Move only "Version numbers" and "New project entries" to the Enabled section.

**Aggressive setup** (trust the AI more):
Move all safe categories to Enabled — but watch for false positives.

**Conservative setup** (human reviews everything):
Leave Enabled section empty. Lucid will still generate suggestions but never apply them.
