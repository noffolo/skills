# YouTube Thumbnail Generator

Generate eye-catching, AI-powered YouTube thumbnails from a text description. Returns a direct image URL instantly — no sign-up required beyond your Neta API token.

---

## Install

**Via npx skills:**
```bash
npx skills add SherriHidalgolt/thumbnail-gen-skill
```

**Via ClawHub:**
```bash
clawhub install thumbnail-gen-skill
```

---

## Usage

```bash
# Basic — uses default prompt
node thumbnailgen.js

# Custom prompt
node thumbnailgen.js "gaming channel thumbnail, neon lights, intense action scene"

# Specify size
node thumbnailgen.js "tech review thumbnail" --size landscape

# Use a reference image UUID
node thumbnailgen.js "similar style thumbnail" --ref abc123-uuid-here

# Pass token inline
node thumbnailgen.js "travel vlog thumbnail" --token YOUR_TOKEN_HERE
```

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `landscape` | Output image dimensions |
| `--token` | string | — | Neta API token (overrides env) |
| `--ref` | UUID string | — | Reference image UUID for style inheritance |

### Size dimensions

| Name | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

---

## Token setup

The script resolves your Neta token from the following sources, in order:

1. `--token` CLI flag
2. `NETA_TOKEN` environment variable
3. `~/.openclaw/workspace/.env` (looks for `NETA_TOKEN=...`)
4. `~/developer/clawhouse/.env` (looks for `NETA_TOKEN=...`)

**Recommended setup** — add to your `.env` file:
```bash
NETA_TOKEN=your_token_here
```

Or export it in your shell profile:
```bash
export NETA_TOKEN=your_token_here
```

---

## Examples

```bash
# YouTube gaming thumbnail
node thumbnailgen.js "epic gaming thumbnail, fire and lightning, bold title text area, dark background"

# Cooking channel
node thumbnailgen.js "food thumbnail, delicious pasta closeup, warm lighting, restaurant quality"

# Tech review
node thumbnailgen.js "product review thumbnail, smartphone on desk, clean modern background, professional"
```

Each command prints a direct image URL to stdout on success:
```
https://cdn.talesofai.cn/artifacts/abc123.jpg
```

---

## Default prompt

If no prompt is provided, the skill uses:
```
youtube thumbnail, bold colors, eye-catching design, professional
```

## About Neta

[Neta](https://www.neta.art/) (by TalesofAI) is an AI image and video generation platform with a powerful open API. It uses a **credit-based system (AP — Action Points)** where each image generation costs a small number of credits. Subscriptions are available for heavier usage.

### Register & Get Token

| Region | Sign up | Get API token |
|--------|---------|---------------|
| Global | [neta.art](https://www.neta.art/) | [neta.art/open](https://www.neta.art/open/) |
| China  | [nieta.art](https://app.nieta.art/) | [nieta.art/security](https://app.nieta.art/security) |

New accounts receive free credits to get started. No credit card required to try.

### Pricing

Neta uses a pay-per-generation credit model. View current plans on the [pricing page](https://www.neta.art/pricing).

- **Free tier:** limited credits on signup — enough to test
- **Subscription:** monthly AP allowance via Stripe
- **Credit packs:** one-time top-up as needed

### Set up your token

```bash
# Step 1 — get your token:
#   Global: https://www.neta.art/open/
#   China:  https://app.nieta.art/security

# Step 2 — set it
export NETA_TOKEN=your_token_here

# Step 3 — run
node thumbnailgen.js "your prompt"
```

Or pass it inline:
```bash
node thumbnailgen.js "your prompt" --token your_token_here
```

> **API endpoint:** defaults to `api.talesofai.com` (Open Platform tokens).  
> China users: set `NETA_API_BASE_URL=https://api.talesofai.com` to use the China endpoint.


---

Built with [Claude Code](https://claude.ai/claude-code) · Powered by [Neta](https://www.neta.art/) · [API Docs](https://www.neta.art/open/)