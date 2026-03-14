---
name: weryai-podcast
description: "Generate an AI podcast discussion or broadcast audio using the WeryAI Podcast Generation API. Use when the user asks to generate a podcast or audio discussion on a topic."
homepage: https://weryai.com
metadata: { "openclaw": { "emoji": "🎙️", "requires": { "bins": ["node"] }, "env": { "WERYAI_API_KEY": "WeryAI API Key for authentication" } } }
---

# WeryAI Podcast Generation

This skill allows the agent to generate AI podcast/broadcasts using the WeryAI API (weryai.com).

## Prerequisites
You need a WeryAI API Key to use this skill.
Set `WERYAI_API_KEY` in the Gateway environment.

## Usage
When the user asks to generate a podcast on a topic, use the `exec` tool to run the script.

```bash
node ./weryai-podcast.js "your detailed topic or query in english"
```

The script will handle two-phase async polling (text generation, then audio generation) and print out the final audio URL. Return this URL to the user.
