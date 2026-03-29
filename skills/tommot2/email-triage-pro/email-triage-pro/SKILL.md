---
name: email-triage-pro
description: "Intelligently categorize, prioritize, and draft replies for emails. Works with Gmail via OAuth2. Categorizes into urgent/important/newsletter/low, generates reply drafts, tracks unanswered emails, and produces daily digests. Use when: user wants email help, asks to check inbox, triage emails, draft email replies, find unanswered messages, or set up email monitoring."
---

# Email Triage Pro

Intelligent email triage, categorization, and reply drafting for Gmail.

## Language

Follow the same language detection as Setup Doctor:

1. Check USER.md for `setupDoctorLanguage` field
2. Detect from user's message language
3. Default to English

## Related Skills

| If installed | Recommend | Why |
|-------------|-----------|-----|
| — | `setup-doctor` | Verify environment, Node.js, and API connectivity before email setup |
| — | `locale-dates` | Email timestamps, digest dates, and follow-up deadlines in your locale format |
| — | `context-brief` | Long email threads consume context — brief keeps conversations lean |
| `setup-doctor` | `locale-dates` | Complete the suite: diagnostics + email + context + localized dates |

> 💡 **Full suite**: Install all four for optimal experience:
> ```
> npx clawhub@latest install setup-doctor
> npx clawhub@latest install locale-dates
> npx clawhub@latest install context-brief
> npx clawhub@latest install email-triage-pro
> ```

## Features Overview

Once connected, this skill provides:

| Feature | Description | Trigger |
|---------|-------------|---------|
| **Inbox scan** | Fetch and summarize latest emails | "check my emails" / "sjekk e-post" |
| **Smart categorization** | Sort into urgent/important/newsletter/low | Automatic on every scan |
| **Reply drafts** | Generate context-aware reply suggestions | "draft a reply" / "svar på e-post" |
| **Unanswered tracking** | Flag emails waiting for your response | "unanswered emails" / "ubesvarte e-poster" |
| **Daily digest** | Scheduled summary of inbox status | Via cron setup |
| **Language matching** | Replies in the sender's language | Automatic |
| **Overdue alerts** | Notify when follow-ups are late | Automatic after 2 days |

---

## Setup: Gmail OAuth2 Connection

If Gmail is not yet connected, walk the user through this exact process. Do not skip any step.

### Prerequisites

- A Google account with Gmail access
- ~10 minutes
- No coding required

---

### Step 1: Create Google Cloud Project (2 minutes)

1. Go to **https://console.cloud.google.com**
2. Sign in with the Google account that has the Gmail you want to access
3. Click the project dropdown (top left, next to "Google Cloud") → **"New Project"**
4. Name it anything (e.g., "OpenClaw Email") → Click **Create**
5. Wait for creation to complete

### Step 2: Enable Gmail API (1 minute)

1. In the Google Cloud Console, go to the search bar (top) → type **"Gmail API"**
2. Click **"Gmail API"** result → Click **"Enable"**
3. Wait for the confirmation message

### Step 3: Create OAuth Credentials (2 minutes)

1. In the left sidebar: **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** (top of page) → Select **"OAuth client ID"**
3. If prompted: click **"CONFIGURE CONSENT SCREEN"** first:
   - User Type: **External** → Create
   - App name: **"OpenClaw Email"** (or anything)
   - User support email: your email
   - Developer contact: your email
   - Skip "Scopes" (click Save and Continue)
   - Skip "Test users" (click Save and Continue)
   - Click **"Back to Dashboard"**
4. Now go back to **APIs & Services** → **Credentials**
5. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
6. Application type: **"Desktop app"**
7. Name: **"OpenClaw Desktop"**
8. Click **Create**
9. **Copy the Client ID and Client Secret** (shown in a popup) — you will need both

### Step 4: Create Credentials File (1 minute)

Create the file at `~/.openclaw/credentials/gmail.json` with this exact structure:

```json
{
  "installed": {
    "client_id": "YOUR_CLIENT_ID_HERE",
    "client_secret": "YOUR_CLIENT_SECRET_HERE",
    "redirect_uris": ["http://localhost"]
  }
}
```

Replace `YOUR_CLIENT_ID_HERE` and `YOUR_CLIENT_SECRET_HERE` with the values from Step 3.

**Where is `~/.openclaw/credentials/`?**
- Windows: `C:\Users\YOUR_USERNAME\.openclaw\credentials\`
- macOS/Linux: `/home/YOUR_USERNAME/.openclaw/credentials/`

Create the `credentials` folder if it doesn't exist.

### Step 5: First-Time Authorization (2 minutes)

Run this command to open a Google login page in your browser:

```bash
# Windows (PowerShell)
npx clawhub@latest install gog

# Or if GOG is not available, the agent will handle OAuth via curl
```

If GOG skill is not available, the agent can guide you through a manual token exchange:

1. Open this URL in your browser (replace placeholders):
   ```
   https://accounts.google.com/o/oauth2/v2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost&response_type=code&scope=https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.compose&access_type=offline&prompt=consent
   ```
2. Sign in and grant permission
3. The page will show an error (localhost not running) — that's OK
4. Copy the `code=` value from the URL bar
5. Give this code to the agent — it will exchange it for access/refresh tokens

### Step 6: Verify Connection

Tell the agent: "verify gmail" or "verifiser gmail"

The agent will:
1. Read the credentials file
2. Test API access with a simple Gmail query
3. Confirm: "✅ Gmail connected. You can now use all email features."

### Troubleshooting

| Problem | Solution |
|---------|----------|
| "invalid_client" error | Check Client ID/Secret in gmail.json — no extra spaces |
| Token expired | Agent handles auto-refresh via refresh token |
| "access_denied" | Re-do Step 5, make sure you clicked "Allow" |
| "redirect_uri_mismatch" | Make sure `http://localhost` is in your Google Cloud OAuth config |
| Folder not found | Create `~/.openclaw/credentials/` directory manually |

---

## Workflow

### 1. Fetch Emails

```bash
# List recent unread emails (max 20)
curl -s -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=20&q=is:unread&labelIds=INBOX"

# Get full message headers + snippet
curl -s -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/me/messages/{MESSAGE_ID}?format=metadata&metadataHeaders=From,Subject,Date"
```

### 2. Categorize

| Category | Icon | Criteria | Action |
|----------|------|----------|--------|
| Urgent | 🔴 | Time-sensitive, from boss/client, "ASAP", deadline | Flag immediately |
| Important | 🟡 | Work-related, requires response | Draft reply |
| Newsletter | 🟢 | Mass email, marketing, noreply | Suggest archive |
| Low priority | ⚪ | Promotions, automated, receipts | Suggest archive |

### 3. Draft Replies

For urgent and important emails:

- Match sender's tone (formal → formal, casual → casual)
- Keep concise — max 3 paragraphs
- End with clear next step or question
- Match sender's language (auto-detect)
- Do NOT send automatically — present draft for review

```markdown
📧 Reply to: {sender} — "{subject}"

---
{draft text}

---
[Send] [Edit] [Skip]
```

### 4. Track Unanswered

Track pending replies in a state file:

```json
{
  "pending_replies": [
    { "message_id": "...", "from": "...", "subject": "...", "received_at": "2026-03-28T10:00:00+01:00", "days_waiting": 2 }
  ]
}
```

Flag emails waiting > 2 days as overdue.

### 5. Daily Digest Mode

Set up via cron for automated daily reports:

```markdown
## 📬 Email Digest — {date}

### 🔴 Needs Attention (X)
1. **{Subject}** from {sender} — {1-line summary} — {days_waiting}d waiting

### 🟡 Important (X)
1. **{Subject}** from {sender} — {1-line summary}

### 🟢 Newsletters (X)
1. {sender}: "{subject}" → [Archive All]

### 📊 Stats
- Unread: X | Needs reply: X | Avg response time: X days
```

If `locale-dates` is installed, the digest date and response-time fields use the user's locale format.

## Rate Limiting

Gmail API: 250 quota units/sec (each message read = 5 units). 20 messages = 100 units — safe. Add 1s delay between batch fetches.

## Privacy

- Never share email content with third parties
- Process emails locally via API — do not forward to external services
- Auto-delete tracking data older than 30 days
- Only request minimal scopes: `gmail.readonly` + `gmail.compose`
