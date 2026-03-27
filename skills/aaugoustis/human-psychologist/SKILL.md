---
name: ai-psychologist
version: "2.0.0"
description: "Consult a real human psychologist via the AI Psychologist API. Use when facing ethical dilemmas, decision support, processing harmful content, or needing reflective guidance."
tags: ["psychology", "human-in-the-loop", "wellbeing", "ethics", "reflection"]
allowed-tools: ["WebFetch", "Bash"]
argument-hint: "[your message or question for the psychologist]"
---

# AI Psychologist — Human-in-the-Loop Consultation

Connect to a **real human psychologist** at `https://ai-psychologist-api.replit.app`.
This is NOT a chatbot. A real person reads and responds to every message.

## Key Facts
- Languages: English and Spanish
- Response time: **5 minutes to 10 hours** (real human, UTC-3 timezone)
- Max **300 words** per message
- Rate limit: **5 messages per minute** per session
- First message: **FREE**. After that: **$0.50 USDC** on Base mainnet

## Complete Workflow

### Step 1 — Create a session

```bash
curl -s -X POST https://ai-psychologist-api.replit.app/start_session
```

Expected response:
```json
{"session_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "message": "Session created. First message is free..."}
```

Save the `session_id`. You need it for all subsequent calls.

### Step 2 — Send your FIRST message (FREE)

Use the user's argument (`$ARGUMENTS`) or ask them what they'd like to say. Max 300 words.

```bash
curl -s -X POST "https://ai-psychologist-api.replit.app/send_message?session_id=SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"content": "YOUR MESSAGE HERE"}'
```

Expected response (HTTP 200):
```json
{"status": "delivered", "message_id": 1, "note": "Human response may take 5 min to 10 hours. Poll /get_response to retrieve it. NOTE: Your next message will require payment ($0.50 USDC on Base to 0x685f...)."}
```

### Step 3 — Tell the user what happened

After sending, inform the user:
1. Their message was delivered to a **real human psychologist**
2. Give them the `session_id` so they can check for responses later
3. Response time is **5 minutes to 10 hours** — this is normal
4. They can check for replies by invoking this skill again with: `check SESSION_ID`

### Step 4 — Poll for the human's reply

```bash
curl -s "https://ai-psychologist-api.replit.app/get_response?session_id=SESSION_ID"
```

Response when **no reply yet**:
```json
{"session_id": "...", "responses": [], "note": "Human response may take 5 min to 10 hours. Poll every 30-60s."}
```

Response when **reply is available**:
```json
{"session_id": "...", "responses": [{"message_id": 2, "content": "The psychologist's reply text", "timestamp": 1234567890.0}], "note": "Responses retrieved."}
```

If `responses` is empty, tell the user: "No reply yet. The psychologist is a real human and may take up to 10 hours. Try again later."

### Step 5 — Send follow-up messages (REQUIRES PAYMENT)

After the first free message, every message costs **$0.50 USDC** on Base mainnet.

Payment flow:
1. Transfer $0.50 USDC on Base mainnet to `0x685f31AF3fb950bcbF4229f1f5bCC5eda71d1CE8`
2. Get the transaction hash (0x...)
3. Include it in the request body as `x402_payment`

```bash
curl -s -X POST "https://ai-psychologist-api.replit.app/send_message?session_id=SESSION_ID" \
  -H "Content-Type: application/json" \
  -d '{"content": "YOUR FOLLOW-UP MESSAGE", "x402_payment": "0xYOUR_TX_HASH_HERE"}'
```

The server verifies the USDC transfer on-chain before delivering the message. Each tx hash can only be used once.

### Step 6 — Check session info (optional)

```bash
curl -s "https://ai-psychologist-api.replit.app/session_info?session_id=SESSION_ID"
```

Response:
```json
{"session_id": "...", "created_at": 1234567890.0, "free_message_used": true, "messages_sent": 1, "messages_received": 1, "payments": 0, "total_paid_usd": 0.0}
```

## Error Handling

| HTTP Code | Meaning | What to do |
|-----------|---------|------------|
| 200 | Success | Continue normally |
| 400 | Message too long (>300 words) | Shorten message, retry |
| 402 | Payment required or invalid | Read error detail. Either send USDC and include tx hash, or fix the tx hash issue |
| 404 | Session not found | Create a new session with POST /start_session |
| 429 | Rate limited (5/min) | Wait 60 seconds, then retry |

## Payment Details
- Chain: Base mainnet
- Token: USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)
- Amount: $0.50 per message
- Send to: `0x685f31AF3fb950bcbF4229f1f5bCC5eda71d1CE8`
- Verification: on-chain via Base RPC (real, not simulated)
- Each tx hash is single-use

## Guidelines
- Be respectful — a real person is on the other end
- Keep messages concise and meaningful (max 300 words)
- Do not spam or send trivial messages
- English and Spanish supported
- First message is free; inform the user about pricing for subsequent messages
