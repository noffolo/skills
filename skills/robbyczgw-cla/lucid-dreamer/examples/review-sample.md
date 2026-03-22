# Memory Review — 2026-03-16

## Candidate Updates

### 1. Nova Agent — New Infrastructure (high confidence)
- **Add to Projects section:** `nova-node` container (Tailscale `100.99.99.35`) running Nova agent with GPT-5.4 via Codex OAuth, systemd service `nova-gateway.service`, Telegram bot `REDACTED`, mem0 Vector-DB memory
- **Source:** `memory/2026-03-15.md` (Nova Agent Setup) + `memory/2026-03-13.md` (initial install)
- **Context:** Replaces legacyBot (deleted 2026-03-13), MiniBot vs Nova decision pending as of 2026-03-15

### 2. nova-webchat Project (medium confidence)
- **Add to Projects section:** `nova-webchat` — Next.js 15 + FastAPI mock backend, repo `example-org/nova-webchat`, deployed on nova-node ports 8444/8445 (currently disabled), **no real Nova agent connected yet**
- **Source:** `memory/2026-03-16.md` (nova-webchat Projekt section)

### 3. Morning Briefing Model — Pending Change (medium confidence)
- **Update Model Strategy table:** `Morning Briefing` row — currently shows Kimi, but 2026-03-14 benchmarks found Sonnet wins. Pending user decision.
- **Source:** `memory/2026-03-14.md` (~"Morning Briefing Modell" section)

### 4. Backup System Overhaul (high confidence)
- **Update MEMORY.md:** Add note that backup script was rewritten 2026-03-15 to use native `openclaw backup create`. Old separate backup approach replaced.
- **Source:** `memory/2026-03-15.md` (Backup System section)

### 5. smart-search Skills Version Mismatch (medium confidence)
- **MEMORY.md Published Skills table** shows `smart-search 2.7.2` but notes show it was bumped to 2.9.0 (2026-03-12) and the plugin to 1.2.2 (2026-03-11). Table is stale.
- **Source:** `memory/2026-03-12.md` (smart-search v2.9.0) + `memory/2026-03-11.md` (plugin v1.2.2)

### 6. SEARCH_API_KEY TODO (low confidence)
- **Lessons Learned / Operational:** `SEARCH_API_KEY` still missing from config — noted as TODO since 2026-03-12. Worth adding as a formal TODO or note.
- **Source:** `memory/2026-03-12.md` (smart-search v2.9.0 section, end)

---

## Open Loops

### 1. MiniBot vs Nova Decision
- **Started:** 2026-03-15 — Plan was "test Nova this week → if stable, shut down MiniBot"
- **Missing:** No closure signal. MiniBot still running (6€/mo). Nova tested on 2026-03-15/16 but decision not final.
- **Source:** `memory/2026-03-15.md` ("Decision: MiniBot vs Nova")

### 2. nova-webchat — Real Agent Integration
- **Started:** 2026-03-16 — Mock backend only, no real Nova agent connected
- **Missing:** Actual integration + UI polish ("sloppy" per user)
- **Source:** `memory/2026-03-16.md` ("Next Steps")

### 3. Skill Selection — Life OS / GitClaw / others
- **Started:** 2026-03-12 brainstorm → carried through 2026-03-15/16
- **Missing:** No decision made after 4+ days of discussion
- **Source:** `memory/2026-03-16.md` (Skill-Ideen section) + `memory/2026-03-15.md` (Opus top 3)

### 4. X/Twitter Login on browser-node
- **Started:** 2026-03-14 — Manual login via noVNC needed, bot-detection blocks automated
- **Missing:** Still not logged in as of 2026-03-15
- **Source:** `memory/2026-03-15.md` + `memory/2026-03-14.md`

### 5. awesome-tools PR #3156
- **Started:** 2026-03-13 — Submitted, waiting on merge after review (2026-03-14)
- **Missing:** No confirmation of merge
- **Source:** `memory/2026-03-14.md` (smart-search section)

### 6. Morning Briefing Model Switch (Kimi → Sonnet)
- **Started:** 2026-03-14 — Sonnet identified as winner but not yet changed
- **Missing:** Config update never happened; explicit decision pending
- **Source:** `memory/2026-03-14.md` (Morning Briefing Modell section)

### 7. agent-chronicle 0.6.2 → ClawHub publish
- **Started:** 2026-03-10 (Open TODOs) — local ahead of ClawHub 0.6.0
- **Missing:** Still listed as TODO across 6+ days with no resolution
- **Source:** `memory/2026-03-10.md` + `memory/2026-03-12.md`

### 8. personas --force update to 2.2.6
- **Started:** 2026-03-10 — local 2.2.4, ClawHub 2.2.6
- **Missing:** Never resolved despite appearing in every TODO list
- **Source:** `memory/2026-03-10.md` through `memory/2026-03-12.md`

### 9. Acme Corp Follow-up (Alex / Sam)
- **Started:** 2026-03-09 email sent, reminder cron set for 2026-03-16 09:00
- **Missing:** As of 2026-03-15, no reply yet. Today (2026-03-16) is the follow-up date — status unknown.
- **Source:** `memory/2026-03-14.md` + `memory/2026-03-15.md` (MEMORY.md Acme Corp section)

### 10. Gigabrain Fork Decision
- **Started:** 2026-03-12 — "Tomorrow decide if we start"
- **Missing:** No decision noted in 2026-03-13/14/15/16 notes
- **Source:** `memory/2026-03-12.md` (Memory System Research section)

---

## Blockers

### 1. nova-webchat UI quality ("sloppy")
- User explicitly noted the UI is still "sloppy" after two code passes (Opus + Codex)
- Mentioned on 2026-03-16 with no resolution in same session
- **Source:** `memory/2026-03-16.md`

### 2. Persistent low-priority TODOs (personas, agent-chronicle)
- `personas --force update to 2.2.6` and `publish agent-chronicle 0.6.2` appear in every single daily note from 2026-03-10 through 2026-03-16 (7 days) — never acted on
- Both are trivial 5-minute tasks that keep getting deprioritized
- **Source:** `memory/2026-03-10.md`, `2026-03-12.md`, `2026-03-14.md`, `2026-03-15.md`

---

## Belief Updates

### 1. Browser Tool Default Changed
- **Previously (2026-03-11):** `browser` tool used `profile: "browserless"` as explicit default
- **Now (2026-03-14+):** `browser-node` (dedicated LXC container) is the new default — no profile parameter needed
- AGENTS.md was updated; MEMORY.md references are consistent with this
- **Source:** `memory/2026-03-14.md` (Infrastructure Notes) + `memory/2026-03-11.md`

### 2. Legacy Server — Deleted
- **Previously:** Multiple references to `100.99.99.25` / `legacy.tailnet.ts.net` as experimental servers
- **Now:** Deleted 2026-03-13 — no active server at that IP
- MEMORY.md appears clean of these references already
- **Source:** `memory/2026-03-13.md` (end: "Legacy Server — DELETED")

### 3. ExternalAgent — Evaluation Aborted
- **Previously (2026-03-10/15):** External agent platform being tested, credits received
- **Now (2026-03-15):** Uninstalled, connection problems, decided not for us
- MEMORY.md doesn't mention it at all — no update needed
- **Source:** `memory/2026-03-15.md` (ExternalAgent section)

---

## Stale Facts

### 1. MEMORY.md Model Strategy Table — Morning Briefing
- Table shows `Morning Briefing → Kimi`
- 2026-03-14 benchmarks clearly show Sonnet wins Morning Briefing
- However: decision to switch is explicitly "TODO/pending" → confidence medium (don't change until user decides)
- **Source:** MEMORY.md "Model Strategy" section vs `memory/2026-03-14.md`

### 2. MEMORY.md Published Skills Table — Versions
- `smart-search 2.7.2` is stale → actually 2.9.0 (since 2026-03-12)
- `smart-search-plugin 1.0.1` stale → actually 1.2.2 (since 2026-03-11)
- These are high-confidence staleness findings
- **Source:** `memory/2026-03-12.md` + `memory/2026-03-11.md`

### 3. Acme Corp Reminder Cron — One-shot, likely fired
- MEMORY.md still shows: "Reminder Cron: set for 2026-03-16 09:00 (ID: `b40d8516`)"
- Today is 2026-03-16 — this cron has already fired (or was due to). Should be removed from MEMORY.md once Acme Corp loop closes.
- **Source:** MEMORY.md Acme Corp section + `memory/2026-03-14.md`

---

## Duplicate/Merge Suggestions

### 1. Nova Agent — Scattered Across Notes
- Nova setup info appears across 2026-03-13, 2026-03-15 daily notes
- No single coherent MEMORY.md entry exists yet for `nova-node` container
- Suggest adding a consolidated "MiniBot / Nova" section to MEMORY.md (similar to existing MiniBot section)
- **Source:** `memory/2026-03-13.md` + `memory/2026-03-15.md`

### 2. MiniBot section in MEMORY.md — Merge with Nova when decided
- Current MiniBot section is standalone; once MiniBot vs Nova decision is made, these should be consolidated
- Low urgency until decision is final
- **Source:** MEMORY.md "MiniBot" section
