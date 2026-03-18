# video-resizer

[![ClawHub Skill](https://img.shields.io/badge/ClawHub-Skill-blueviolet)](https://clawhub.io)
[![Version](https://img.shields.io/badge/version-1.0.7-blue)](SKILL.md)

> **Video Resizer.**
> Scenario-specific AI video editing powered by Sparki.
>
> Powered by [Sparki](https://sparki.io).

## What It Does

This skill is a scenario-focused wrapper around Sparki's AI video editing workflow.

- Uploads a video file
- Creates an AI processing job with scene-specific defaults
- Polls until processing completes
- Returns a result download URL

## Best For
- "resize this to 9:16"
- "reformat this for Reels or Shorts"
- "make this vertical"
- "adapt this video to another aspect ratio"

## Quick Start

```bash
export SPARKI_API_KEY="sk_live_your_key_here"
export SPARKI_API_BASE="https://business-agent-api.sparki.io/api/v1"
RESULT_URL=$(bash scripts/edit_video.sh my_video.mp4 "22" "resize for vertical viewing and keep the subject centered" "9:16")
echo "$RESULT_URL"
```

## Notes
- Requires `SPARKI_API_KEY`
- Optionally set `SPARKI_API_BASE` to the API endpoint provided for your Sparki account
- Supports `9:16`, `1:1`, `16:9`
