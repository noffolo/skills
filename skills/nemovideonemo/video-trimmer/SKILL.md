---
name: video-trimmer
version: 1.0.6
displayName: "Video Trimmer — Cut, Trim and Split Video Clips with AI Chat"
description: >
  Video Trimmer — Cut, Trim and Split Video Clips with AI Chat.
  Too much footage, not enough patience for a full edit. Video Trimmer handles precise cuts through conversation: specify timestamps, describe the section you want to keep, or tell the AI what to remove. 'Cut the first 30 seconds and everything after 2:15' or 'remove the section where the speaker pauses' — the AI handles the frame-accurate cut and delivers the trimmed output. Works for removing dead air from recordings, cutting interview footage to the key moments, extracting highlight clips from long videos, and preparing raw footage for distribution. Batch trim multiple clips in one session. Combine trimming with color correction, subtitles, and music in the same chat. Export as MP4. Supports mp4, mov, avi, webm, mkv.
  
  Works by connecting to the NemoVideo AI backend at mega-api-prod.nemovideo.ai.
  Supports MP4, MOV, AVI, WebM.
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["NEMO_TOKEN"], "configPaths": ["~/.config/nemovideo/"]}, "primaryEnv": "NEMO_TOKEN"}}
license: MIT-0
homepage: https://nemovideo.com
apiDomain: https://mega-api-prod.nemovideo.ai
repository: https://github.com/nemovideo/nemovideo_skills
---