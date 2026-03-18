# ai-vlog-editor

[![ClawHub Skill](https://img.shields.io/badge/ClawHub-Skill-blueviolet)](https://clawhub.io)
[![Version](https://img.shields.io/badge/version-1.0.6-blue)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **AI Vlog Editor.**
> 把原始生活素材快速做成有节奏、有氛围的 vlog。
>
> Powered by [Sparki](https://sparki.io).

## What It Does

This skill is a scenario-focused wrapper around Sparki's AI video editing workflow.

- Uploads a video file
- Creates an AI processing job with scene-specific defaults
- Polls until processing completes
- Returns a result download URL

## Quick Start

```bash
export SPARKI_API_KEY="sk_live_your_key_here"
RESULT_URL=$(bash scripts/edit_video.sh my_video.mp4 "21" "chill daily life vibes" "9:16")
echo "$RESULT_URL"
```

## Best For
- “帮我把这些素材剪成 vlog”
- “做一个日常/旅行 vlog”
- “把生活素材剪得更有氛围”
- “做成像 YouTube creator 那样的 vlog”

## Notes
- Requires `SPARKI_API_KEY`
- Uses the same reliable scripts as the cleaned `ai-video-editor` fork
- Supports `9:16`, `1:1`, `16:9`
