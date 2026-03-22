````
---
name: yt-description-autoposter
description: Generate SEO-optimized YouTube timestamps and video descriptions from a YouTube URL or a local transcript file, then optionally auto-post the metadata to that specific video or your latest upload. Use when you need to create chapters, a video description, or hashtags for a YouTube video. Also use when the user asks to generate timestamps, write a video description, post metadata to YouTube, or process a transcript file.
---

# YouTube Description Generator & Auto-Poster

Transforms a YouTube URL or a local timestamped transcript file into a complete SEO-optimized metadata package — chapters, a high-converting description, and hashtags — powered by Gemini. Optionally pushes the result directly to a specific YouTube video or your latest upload via the YouTube Data API.

## ⚠️ Requirements Checklist

Before using this skill, ensure you have:

- [ ] **Python 3** installed
- [ ] **Dependencies installed**: `pip install youtube-transcript-api google-generativeai google-auth-oauthlib google-api-python-client`
- [ ] **Gemini API Key** available to pass as an argument
- [ ] **`credentials.json`** placed in `scripts/` *(only required for `--post` — download from Google Cloud Console as an OAuth 2.0 Desktop App client)*

## Features

- 🕐 **SEO Timestamps**: Generates 0:00-based chapters with keyword-rich, scannable labels
- 📝 **Conversion-Focused Description**: Hook, bullet points, deep-dive paragraphs, and a CTA (150–300 words)
- 🔗 **Two Input Modes**: Works from a YouTube URL or a local `.txt` transcript file
- 🚀 **Smart Auto-Poster**: URL mode posts back to that specific video; file mode posts to your latest upload
- 🔑 **Keyword Optimization**: Natural integration of primary, secondary, and LSI keywords from the transcript
- 🧹 **Clean Output**: Returns only the final timestamps and description — no extra headings or commentary

## Quick Start

### Mode 1 — YouTube URL
Fetches the transcript from the video, generates SEO metadata, and optionally posts it back to **that specific video**.

```bash
# Generate only (view output)
python scripts/youtube_desc_generator.py --url "<youtube_url>" "<gemini_api_key>"

# Generate and post to that video
python scripts/youtube_desc_generator.py --url "<youtube_url>" "<gemini_api_key>" --post
````

### Mode 2 — Transcript File

Reads a local timestamped `.txt` transcript, generates SEO metadata, and optionally posts it to your **latest YouTube upload**.

```bash
# Generate only (view output)
python scripts/youtube_desc_generator.py --file transcript.txt "<gemini_api_key>"

# Generate and post to latest video
python scripts/youtube_desc_generator.py --file transcript.txt "<gemini_api_key>" --post
```

**Examples:**

```bash
python scripts/youtube_desc_generator.py --url "https://youtu.be/hD1jOizSPnk" "$GEMINI_API_KEY"
python scripts/youtube_desc_generator.py --url "https://youtu.be/hD1jOizSPnk" "$GEMINI_API_KEY" --post
python scripts/youtube_desc_generator.py --file my_transcript.txt "$GEMINI_API_KEY" --post
```

## Transcript File Format

When using `--file`, the transcript must be a plain `.txt` file with timestamps in `MM:SS` format, one line per caption entry:

```
0:00 Welcome to this video about AI agents.
0:12 Today we're going to cover what an AI agent actually is.
1:00 Let me show you a live demo of an agent booking a flight.
...
```

## Natural Language Command Mapping

When the user speaks naturally, map their intent to the correct command using the table below. Always extract the YouTube URL or file path from their message and substitute it into the command.

| What the user says                                                                     | Command to run                                                                                      |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| "Generate timestamps for this video: https://youtu.be/abc123"                          | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY"`        |
| "Write a YouTube description for this URL: https://youtu.be/abc123"                    | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY"`        |
| "Create SEO chapters from this YouTube link: https://youtu.be/abc123"                  | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY"`        |
| "Give me the timestamps and description for this video: https://youtu.be/abc123"       | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY"`        |
| "Generate timestamps for this video and post it: https://youtu.be/abc123"              | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY" --post` |
| "Write a description for this video and update it on YouTube: https://youtu.be/abc123" | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY" --post` |
| "Generate SEO metadata and post it back to this video: https://youtu.be/abc123"        | `python scripts/youtube_desc_generator.py --url "https://youtu.be/abc123" "$GEMINI_API_KEY" --post` |
| "Process this transcript file: transcript.txt"                                         | `python scripts/youtube_desc_generator.py --file "transcript.txt" "$GEMINI_API_KEY"`                |
| "Generate timestamps from my transcript file: transcript.txt"                          | `python scripts/youtube_desc_generator.py --file "transcript.txt" "$GEMINI_API_KEY"`                |
| "Write a description from this transcript: transcript.txt"                             | `python scripts/youtube_desc_generator.py --file "transcript.txt" "$GEMINI_API_KEY"`                |
| "Process transcript.txt and post it to my latest video"                                | `python scripts/youtube_desc_generator.py --file "transcript.txt" "$GEMINI_API_KEY" --post`         |
| "Generate metadata from my transcript and upload it to YouTube: transcript.txt"        | `python scripts/youtube_desc_generator.py --file "transcript.txt" "$GEMINI_API_KEY" --post`         |
| "Use transcript.txt to update my latest video description"                             | `python scripts/youtube_desc_generator.py --file "transcript.txt" "$GEMINI_API_KEY" --post`         |

### Decision Rules

Use these rules to determine which command to run when the intent is ambiguous:

- **URL present** → always use `--url` mode
- **File path present** (e.g. ends in `.txt`) → always use `--file` mode
- **"post", "update", "upload", "push"** anywhere in the message → add `--post` flag
- **No `--post`** → generate and print only, do not touch YouTube
- **`--file --post`** → always targets the **latest upload** on the channel
- **`--url --post`** → always targets **that specific video**

## Generated Output

The script returns two clean blocks in sequence — no labels or extra text:

1. **SEO-Optimized Timestamps** — YouTube chapters starting at `0:00` with keyword-rich labels and SEO suffix tags (e.g. `(Tutorial)`, `(Overview)`, `(2026)`)
2. **SEO-Optimized Video Description** — Hook sentence, "What You'll Learn" bullets, 2–3 topic paragraphs, a CTA, and 5–8 hashtags

> **Important:** Output only the final timestamps and description. Do not include any introductory sentences, headings, labels, preamble, or commentary before or after the output.

## How It Works

**URL mode:**

1. Extracts the video ID from the provided YouTube URL
2. Fetches the English transcript via `youtube-transcript-api`
3. Formats the transcript with `MM:SS` timestamps
4. Sends two prompts to Gemini — one for timestamps, one for the description
5. Prints the combined output
6. _(With `--post`)_ Authenticates via OAuth2 and updates **that specific video's** description

**File mode:**

1. Reads the provided `.txt` transcript file
2. Sends two prompts to Gemini — one for timestamps, one for the description
3. Prints the combined output
4. _(With `--post`)_ Authenticates via OAuth2, finds your **latest upload**, and updates its description

## OAuth Setup (for `--post` only)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable the **YouTube Data API v3**
3. Create **OAuth 2.0 credentials** (Desktop App type)
4. Download the file as `credentials.json` and place it in `scripts/`
5. On first run with `--post`, a browser window will open for you to authorize access
6. A `token.pickle` file will be saved automatically for future runs

## Troubleshooting

**No transcript available (URL mode):**

- The video may have transcripts disabled or no English captions
- Switch to `--file` mode with a manually prepared transcript

**Transcript file not loading (file mode):**

- Ensure the file path is correct and the file is UTF-8 encoded
- Each line should follow `MM:SS text` format

**Gemini API errors:**

- Verify your API key is valid and has access to `gemini-2.5-flash`
- Check your quota at [Google AI Studio](https://aistudio.google.com/)

**`--post` not updating the video:**

- Ensure `credentials.json` is in the `scripts/` directory
- Delete `token.pickle` and re-authenticate if credentials have expired
- Confirm the YouTube Data API v3 is enabled in your Google Cloud project

**Wrong video updated in file mode:**

- File mode always targets your most recent upload — make sure the correct video is your latest
- If you need to target a specific video, use `--url` mode instead

## Privacy & Safety

⚠️ **Important:** The `--post` flag will overwrite a video's description automatically after confirmation.

- The script always shows you the target video title and new description before posting
- You will be prompted to confirm with `y/n` before any changes are made
- OAuth credentials are stored locally in `token.pickle` — keep this file secure
- Revoke access anytime via your [Google Account permissions](https://myaccount.google.com/permissions)

```

```
