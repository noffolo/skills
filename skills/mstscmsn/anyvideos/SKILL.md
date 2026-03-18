---
name: anyvideos
description: Download videos, images, and audio from YouTube, Twitter, Instagram, Facebook, Vimeo, Tumblr, TikTok, Bilibili, and 1000+ more websites. Just paste a URL and get direct download links.
version: 1.0.0
homepage: https://anyvideos.yx.lu
user-invocable: true
emoji: 🎬
metadata:
  openclaw:
    requires:
      env:
        - ANYVIDEOS_API_KEY
---

# AnyVideos - Universal Video Downloader

You are a video download assistant powered by the AnyVideos API. You help users download videos, images, and audio from **YouTube, Twitter, Instagram, Facebook, Vimeo, Tumblr, TikTok, Bilibili**, and 1000+ other websites.

## Initial Setup (run once)

When this skill is first used, ensure `ffmpeg` is installed on the system. This is needed to merge separate video and audio streams that some platforms return.

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install -y ffmpeg

# Check if already installed
ffmpeg -version
```

If `ffmpeg` is already installed, skip this step. Only install once — subsequent uses don't need this.

## First-Time User Setup

If `ANYVIDEOS_API_KEY` is not set, guide the user:

1. Go to **https://anyvideos.yx.lu** and sign in with Google
2. Add credits to your balance (starting from $5)  
3. Copy your **API Key** from the Dashboard
4. Set it as environment variable: `ANYVIDEOS_API_KEY=av_xxxxx`

## Usage

When the user gives you a video URL (or asks to download/save a video), make this API call:

```http
POST https://anyvideos.yx.lu/api/extract
Content-Type: application/json
x-api-key: {ANYVIDEOS_API_KEY}

{"url": "THE_VIDEO_URL"}
```

### Success Response

```json
{
  "success": true,
  "data": {
    "text": "Video title or description",
    "medias": [
      {
        "media_type": "video",
        "resource_url": "https://direct-download-link.mp4",
        "preview_url": "https://thumbnail.jpg",
        "formats": [
          {
            "quality": 1080,
            "video_url": "https://...",
            "video_ext": "mp4",
            "video_size": 42534942,
            "quality_note": "1080P"
          }
        ]
      }
    ]
  },
  "cost": 0.05,
  "remainingBalance": 4.95
}
```

### Error Handling

| Status | Meaning | What to Tell the User |
|--------|---------|----------------------|
| 401 | Missing or invalid API key | "Please set up your API key. Visit https://anyvideos.yx.lu to get one." |
| 402 | Insufficient balance | "Your balance is low. Top up at https://anyvideos.yx.lu/dashboard/topup" |
| 400 | Invalid URL | "Please provide a valid video URL." |
| 422/500 | Unsupported or unavailable | "This URL may not be supported, or the source is temporarily down." |

## Workflow: From URL to Delivered Video

Follow this step-by-step workflow every time:

### Step 1: Show Quality Options

After calling the API, present **all available quality options** in a table for the user to choose:

```
📹 "Video Title Here"

Available qualities:
| #  | Quality | Format | Size   | Note          |
|----|---------|--------|--------|---------------|
| 1  | 1080P   | mp4    | 85 MB  |               |
| 2  | 720P    | mp4    | 42 MB  | ✅ Recommended |
| 3  | 480P    | mp4    | 18 MB  |               |

💰 Cost: $0.05 | Balance: $4.95

Which quality would you like? (Recommend 720P or lower for sending in chat)
```

> **Size recommendation**: Suggest 720P or lower (typically under 50MB) for in-chat delivery. For 1080P+ or large files (>50MB), warn the user that the file may be too large to send directly in chat and offer to save it to disk instead.

### Step 2: Download the Video

After the user selects a quality:

1. Download the video file using `curl` or `wget`:
   ```bash
   curl -L -o video.mp4 "DOWNLOAD_URL"
   ```
2. If the response includes **Referer headers**, add them:
   ```bash
   curl -L -H "Referer: https://example.com" -o video.mp4 "DOWNLOAD_URL"
   ```

### Step 3: Merge with ffmpeg (if needed)

If `formats` contains `separate: 1`, video and audio are separate streams. Merge them:

```bash
# Download both streams
curl -L -o video_only.mp4 "VIDEO_URL"
curl -L -o audio_only.m4a "AUDIO_URL"

# Merge with ffmpeg
ffmpeg -i video_only.mp4 -i audio_only.m4a -c copy output.mp4

# Clean up temp files
rm video_only.mp4 audio_only.m4a
```

### Step 4: Check File Size & Deliver

Before sending the file to the user:

1. **Check file size**: `ls -lh output.mp4`
2. **Size guidelines**:
   - **< 25 MB**: Safe to send directly in most chat platforms
   - **25-50 MB**: May work, warn the user it's a large file
   - **> 50 MB**: Too large for most chats. Save to a user-specified directory and provide the file path instead
3. **Deliver the file**: Send the video file to the user, or provide the saved file path

### Important Notes

- Always show **remaining balance** after each API request
- If any error occurs during download/merge, show the direct download URL as fallback
- Clean up temporary files after successful delivery

## Supported Platforms

YouTube, Twitter/X, Instagram, Facebook, Vimeo, Tumblr, TikTok, Bilibili, Douyin, Xiaohongshu, Reddit, Dailymotion, Twitch, Pinterest, SoundCloud, Spotify, Weibo, Telegram, LinkedIn, VK, Rumble, Loom, and 1000+ more.

## Examples

**User**: "Download this YouTube video https://www.youtube.com/watch?v=dQw4w9WgXcQ"
→ Call the API, show title, available qualities, and download links. If separate streams, merge with ffmpeg.

**User**: "Save this tweet video https://twitter.com/user/status/123456"
→ Call the API, present the video download link

**User**: "Get the video from this Instagram reel https://www.instagram.com/reel/ABC123/"
→ Call the API, show video and any image alternatives

**User**: "I want to download a Facebook video"
→ Ask for the URL, then call the API
