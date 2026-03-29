---
name: email-triage-pro
description: "Intelligently categorize, prioritize, and draft replies for emails. Works with Gmail via OAuth2 or any IMAP provider. AI-powered classification into urgent/important/newsletter/spam categories, generates contextual reply drafts, tracks unanswered emails, and supports scheduled monitoring via cron. Use when: (1) user wants email help or inbox management, (2) user asks to check inbox, triage emails, or find unread messages, (3) draft email replies with AI assistance, (4) find unanswered or forgotten emails, (5) set up automated email monitoring on schedule, (6) user says 'check my email', 'any urgent emails', 'draft a reply', 'email summary', 'inbox zero'. Supports multi-account setups and customizable priority rules."
---

# Email Triage Pro

Intelligent email triage, categorization, and reply drafting.

## Prerequisites

Gmail is the primary supported provider. Two methods:

### Method A: Gmail API (recommended)

Requires Google OAuth credentials. Check if user has GOG skill installed - if so, use it for Gmail access.

### Method B: IMAP fallback

If GOG not available, use `exec` with standard IMAP tools or `curl` to Gmail API.

**OAuth setup** (one-time):
1. Go to https://console.cloud.google.com/apis/credentials
2. Create OAuth 2.0 Client ID (desktop app)
3. Download credentials as `~/.openclaw/credentials/gmail.json`
4. Run first-time auth flow to get refresh token

## Workflow

### 1. Fetch Emails

Use `exec` to call Gmail API:

```bash
# List recent unread emails
curl -s -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=20&q=is:unread&labelIds=INBOX"

# Get full message
curl -s -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages/{MESSAGE_ID}?format=metadata&metadataHeaders=From,Subject,Date"
```

If OAuth not set up and GOG skill not available, instruct user to install GOG first:
`npx clawhub@latest install gog`

### 2. Categorize

Read each email's subject, sender, and snippet. Categorize:

| Category | Criteria | Action |
|----------|----------|--------|
| 🔴 Urgent | Time-sensitive, from boss/client, "ASAP" | Flag immediately |
| 🟡 Important | Work-related, requires response | Draft reply |
| 🟢 Newsletter | Mass email, marketing | Archive suggestion |
| ⚪ Spam/Low | Promotions, automated | Archive suggestion |

### 3. Draft Replies

For urgent and important emails, generate a reply draft following these rules:

- Match the sender's tone (formal if they're formal, casual if casual)
- Keep it concise - max 3 paragraphs
- End with a clear next step or question
- Do NOT send automatically - present draft for user review
- If sender's language is detected (e.g., Norwegian), reply in same language

Format the draft clearly:

```markdown
📧 Reply to: {sender} - "{subject}"

---
{draft text}

---
[Reply] [Edit] [Skip] [Send as-is]
```

### 4. Track Unanswered

For emails that need response, track in a simple state:

```json
{
  "pending_replies": [
    { "message_id": "...", "from": "...", "subject": "...", "received_at": "...", "days_waiting": 2 }
  ]
}
```

If an email has been waiting > 2 days, flag it as overdue.

### 5. Daily Digest Mode

If user sets up a cron job or asks for periodic checking, produce a digest:

```markdown
## 📬 Email Digest - {date}

### 🔴 Needs Your Attention (X)
1. **{Subject}** from {sender} - {1-line summary} - {days_waiting}d waiting
2. ...

### 🟡 Important (X)
1. **{Subject}** from {sender} - {1-line summary}

### 🟢 Newsletters (X)
1. {sender}: "{subject}" → [Archive All]

### 📊 Stats
- Unread: X
- Needs reply: X
- Avg response time: X days
```

## Rate Limiting

Gmail API: 250 quota units/sec (each message = 5 units). For 20 messages = 100 units - safe. Add 1s delay between batch fetches for safety.

## Privacy

- Never share email content with third parties
- Process emails locally via API - do not forward to external services
- Auto-delete drafts older than 30 days from tracking state

## More by TommoT2

- **context-brief** — Optimize context window for longer conversations
- **setup-doctor** — Diagnose and fix OpenClaw setup issues
- **tommo-skill-guard** — Security scanner for all installed skills

Install the full starter pack:
```bash
npx clawhub@latest install context-brief setup-doctor tommo-skill-guard
```
