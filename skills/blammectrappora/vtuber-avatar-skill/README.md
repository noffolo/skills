# VTuber Avatar Creator

Generate stunning VTuber-style avatar images from a text description using AI. Get back a direct image URL instantly — perfect for virtual YouTubers, streamers, and anime-style character creation.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/vtuber-avatar-skill
```

**Via ClawHub:**
```bash
clawhub install vtuber-avatar-skill
```

---

## Usage

```bash
# Use the default VTuber prompt
node vtuberavatar.js

# Custom description
node vtuberavatar.js "cat girl vtuber, blue twin tails, big expressive eyes, idol outfit"

# Portrait size (default), anime style
node vtuberavatar.js "fox ears vtuber, warm colors, streaming overlay background"

# Landscape layout
node vtuberavatar.js "bunny girl vtuber with microphone" --size landscape

# Tall format, great for phone wallpapers or full-body sheets
node vtuberavatar.js "dragon vtuber, silver hair, fantasy armor" --size tall

# Use a reference image UUID to inherit its style
node vtuberavatar.js "same vtuber, winter outfit" --ref <picture_uuid>
```

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--token` | string | — | Override API token (see Token Setup below) |
| `--ref` | picture_uuid | — | Reference image UUID to inherit style/params |

### Size dimensions

| Size | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

---

## Token Setup

This skill requires a `NETA_TOKEN` from the Neta / talesofai platform. The token is resolved in this order:

1. `--token <your_token>` CLI flag
2. `NETA_TOKEN` environment variable
3. `~/.openclaw/workspace/.env` file containing `NETA_TOKEN=...`
4. `~/developer/clawhouse/.env` file containing `NETA_TOKEN=...`

**Recommended setup** — add to `~/.openclaw/workspace/.env`:
```
NETA_TOKEN=your_token_here
```

---

## Output

The script prints a single image URL to stdout on success:

```
https://cdn.talesofai.cn/.../<image>.webp
```

Pipe it wherever you need:
```bash
node vtuberavatar.js "witch vtuber" | pbcopy       # copy to clipboard (macOS)
node vtuberavatar.js "witch vtuber" | xclip         # copy to clipboard (Linux)
```

---

## Default Prompt

When no description is provided, the skill uses:

> vtuber avatar, anime style, expressive face, colorful hair, streaming overlay ready, clean background, chibi proportions optional, high detail eyes, virtual YouTuber aesthetic

---

Built with Claude Code · Powered by Neta
