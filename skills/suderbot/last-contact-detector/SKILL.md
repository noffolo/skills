---
name: last-contact-detector
description: Detect how long ago Jon last contacted you. Use when Jon asks "when was the last time I messaged you?", "how long ago did I contact you?", or needs to check heartbeat timing. Queries like "have I messaged you recently?" or "when did we last chat?" also trigger this.
---

# Last Contact Detector

This skill finds when Jon last sent a message in any June session.

## How It Works

1. Use `sessions_list` with `activeMinutes: 1440` (24 hours) to get recent sessions
2. Filter for sessions where `lastTo` is Jon's ID (typically `118682632`)
3. Find the session with the most recent `updatedAt` timestamp
4. Calculate the time difference between now and that timestamp

## Tools

- **sessions_list**: List sessions with `limit: 20` and `activeMinutes: 1440` to get the last 24 hours of activity
- **sessions_history**: If needed, fetch history to confirm the last user message from Jon

## Output

Return a human-readable message like:
- "About 30 minutes ago"
- "A couple hours ago"
- "This morning (about 4 hours)"
- "Yesterday evening"

## Notes

- Jon's Telegram ID is typically `118682632`
- Check both `agent:june:main` and `agent:june:telegram:*` sessions
- The `updatedAt` timestamp is in milliseconds since epoch
- Current time context: America/Edmonton (MST)
