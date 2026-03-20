# Veevid — AI Video Generator (OpenClaw Skill)

All-in-one AI video generator: **text to video**, **image to video**, and **reference-to-video** via [Veevid AI](https://veevid.ai). One API, 10+ state-of-the-art video generation models.

## Install

```bash
openclaw skill install veevid
```

Or manually:
```bash
git clone https://github.com/HappyLifeTech/veevid-skill.git ~/.openclaw/skills/veevid
```

## Quick Start

1. Get your API Key at [veevid.ai/settings/api-keys](https://veevid.ai/settings/api-keys)
2. Save it: `echo "vv_sk_xxx" > ~/.config/veevid/api_key`
3. Tell your agent: *"Generate a video of a sunset over the ocean"*

## What Your Agent Can Do

- **Text to Video** — Describe a scene, get a video
- **Image to Video** — Animate a photo or product image
- **Model Selection** — Choose from 9+ AI video models
- **Credit Management** — Check balance, estimate costs

## Supported Models

| Model | Best For | Credits |
|-------|----------|---------|
| Veo 3.1 | Budget-friendly, fixed 8s | 20 / 140 |
| Grok Imagine | Fastest | 10-40 |
| Kling 3.0 | Multi-shot, audio | 48-495 |
| LTX 2.3 | Open-source, 4K | 48-960 |
| Sora 2 Stable | Best realism (4-20s) | 80-2000 |
| Sora 2 | Longer clips, storyboard (10-25s) | 20-315 |

[Full model reference →](references/api-reference.md)

## Links

- [Veevid AI](https://veevid.ai)
- [API Key Management](https://veevid.ai/settings/api-keys)
- [Pricing](https://veevid.ai/pricing)
- [Blog](https://veevid.ai/blog)

## License

MIT
