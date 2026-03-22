#!/usr/bin/env python3
"""
YouTube Description Generator + Auto-Poster

Two modes:
  1. YouTube URL  — fetches transcript from the video, generates SEO metadata,
                    and optionally posts it back to THAT specific video.
  2. Transcript file — reads a pre-made timestamped transcript (.txt),
                       generates SEO metadata, and optionally posts it to your
                       LATEST YouTube upload.
"""

import re
import os
import sys
import pickle
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# ---------- YouTube Data API setup ----------
# Path configuration to look in the same directory as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, 'credentials.json')
TOKEN_PICKLE = os.path.join(SCRIPT_DIR, 'token.pickle')


def get_authenticated_service():
    """Authenticate and return the YouTube API service."""
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Credentials file '{CREDENTIALS_FILE}' not found. "
                    "Download it from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(TOKEN_PICKLE, 'wb') as token:
                pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)


def get_latest_video(youtube):
    """Return (video_id, title, current_description) of the most recent upload."""
    request = youtube.search().list(
        part='snippet',
        forMine=True,
        maxResults=1,
        order='date',
        type='video'
    )
    response = request.execute()
    if not response['items']:
        raise Exception("No videos found on your channel.")
    video = response['items'][0]
    return (
        video['id']['videoId'],
        video['snippet']['title'],
        video['snippet']['description']
    )


def get_video_title(youtube, video_id):
    """Return the title of a specific video by ID."""
    response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
    if not response['items']:
        raise Exception(f"Video {video_id} not found.")
    return response['items'][0]['snippet']['title']


def update_video_description(youtube, video_id, new_description):
    """Replace the description of a specific video."""
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
    if not video_response['items']:
        raise Exception(f"Video {video_id} not found.")
    snippet = video_response['items'][0]['snippet']
    snippet['description'] = new_description

    youtube.videos().update(
        part='snippet',
        body={
            'id': video_id,
            'snippet': snippet
        }
    ).execute()
    print(f"✅ Description updated for video {video_id}.")


# ---------- Transcript helpers ----------
def extract_video_id(url):
    """Extract YouTube video ID from various URL formats, including Shorts."""
    patterns = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/live/|youtube\.com/shorts/)([^&?/]+)",
        r"^([a-zA-Z0-9_-]{11})$"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL or video ID")


def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def fetch_transcript_from_url(video_id):
    """Fetch and format a transcript from a YouTube video ID."""
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)
    transcript = transcript_list.find_transcript(['en'])
    snippets = transcript.fetch()

    formatted = ""
    for snippet in snippets:
        formatted += f"{format_time(snippet.start)} {snippet.text}\n"
    return formatted


def load_transcript_from_file(filepath):
    """Read a pre-made timestamped transcript from a .txt file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Transcript file not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


# ---------- SEO generation ----------
def generate_timestamps_and_description(formatted_transcript, api_key):
    """
    Generate SEO-optimized timestamps and video description from a formatted transcript.
    Returns (timestamps_text, description_text).
    """
    timestamp_prompt = f"""
Output ONLY the timestamps. Do not include any introductory sentence, heading, label, or extra text before or after the timestamps. Start your response directly with 0:00.

Create SEO-optimized YouTube timestamps from this transcript following these best practices:

Format Requirements:
- First timestamp MUST be 0:00 (YouTube's requirement for chapters)
- Use MM:SS format (or HH:MM:SS for videos over 1 hour)
- Each timestamp on a new line
- Minimum 3 timestamps (YouTube's chapter requirement)
- Each segment at least 10 seconds long
- 3 - 5 Timestamps max for a video thats 10 minutes or under
- You can go over 5 timestamps if that video is longer than 10 minutes

SEO Best Practices:
- Include primary keywords naturally in each timestamp description
- Use action-oriented, descriptive language
- Think like a viewer searching for specific information
- Make each timestamp scannable and valuable

Add SEO Suffix Keywords at the end of each timestamp line such as:
(Overview) | (Tutorial) | (Full Guide) | (BEST) | (FREE) | (2026) | (How To) | (Review) | (Tips) | (Step by Step) | (Explained) | (Comparison) | (For Beginners) | (Pro Tips) | (vs. Other Tools) | (Setup) | (Walkthrough) | (Features) | (Demo) | (Hands On)

Transcript:
{formatted_transcript}

Important Formatting Notes:
- Put the PRIMARY KEYWORD or a variation of it in the FIRST timestamp (0:00)
- Include MAJOR PRODUCT NAMES as keywords naturally (e.g., Google Flow, Veo 3.1, Nano Banana 2)
- End with a CONCLUSION or FINAL THOUGHTS timestamp
- Keep each description under 8 words for scannability
"""

    description_prompt = f"""
Output ONLY the video description. Do not include any introductory sentence, heading, label, or extra text before or after the description. Start your response directly with the first sentence of the hook.

Create an SEO-optimized YouTube video description from this transcript following these best practices:

Structure Requirements:
- Start with a 2-3 sentence hook that includes the PRIMARY KEYWORD naturally in the first sentence
- Follow with a "What You'll Learn" or "In This Video" section using bullet points
- Include a mid-section that expands on the key topics covered (2-3 short paragraphs)
- End with a Call To Action (CTA) section encouraging likes, comments, and subscriptions
- Total length: 150-300 words (optimal for YouTube SEO)

SEO Best Practices:
- Place the most important keyword in the FIRST 100 characters (YouTube prioritizes this)
- Include 3-5 secondary keywords naturally throughout the description
- Use action-oriented language and power words
- Write for humans first, search engines second — no keyword stuffing
- Include relevant long-tail keyword phrases as natural sentences
- Think like a viewer searching for this topic — what would they type?

Keyword Placement Strategy:
- PRIMARY KEYWORD: appears in first sentence and at least once more naturally
- SECONDARY KEYWORDS: sprinkled throughout bullet points and paragraphs
- LSI KEYWORDS (related terms): woven into the mid-section paragraphs
- Include year (2026) where relevant for freshness signals

Formatting Rules:
- Use line breaks between sections for readability
- Bullet points for the "What You'll Learn" section
- Keep sentences short and punchy (under 20 words each)
- No clickbait — the description must accurately reflect the video content
- Avoid ALL CAPS except for section headers if used

Call To Action Section must include:
- Subscribe prompt with channel benefit statement
- Like and comment encouragement with a specific question to spark engagement
- One relevant hashtag group at the very end (5-8 hashtags)

Transcript:
{formatted_transcript}

Important Notes:
- Extract the real topic and main value proposition from the transcript
- Do NOT fabricate information not present in the transcript
- The description should make someone who hasn't watched the video want to watch it
- End hashtags should include the primary keyword, niche keywords, and broad reach keywords
"""

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    timestamps = model.generate_content(timestamp_prompt).text
    description = model.generate_content(description_prompt).text

    return timestamps, description


# ---------- Main ----------
def main():
    parser = argparse.ArgumentParser(
        description="Generate SEO timestamps + description from a YouTube URL or transcript file."
    )

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--url',  metavar='YOUTUBE_URL',      help='YouTube video URL — fetches transcript and posts back to THAT video')
    source.add_argument('--file', metavar='TRANSCRIPT_FILE',  help='Path to a timestamped .txt transcript — posts to your LATEST video')

    parser.add_argument('gemini_api_key', help='Gemini API key')
    parser.add_argument('--post', action='store_true', help='Automatically post the generated metadata to YouTube')
    args = parser.parse_args()

    try:
        # --- Mode 1: YouTube URL ---
        if args.url:
            video_id = extract_video_id(args.url)
            print(f"Fetching transcript for video {video_id}...")
            formatted_transcript = fetch_transcript_from_url(video_id)
            target_video_id = video_id  # post back to THIS video

        # --- Mode 2: Transcript file ---
        else:
            print(f"Loading transcript from {args.file}...")
            formatted_transcript = load_transcript_from_file(args.file)
            target_video_id = None  # will resolve to latest video at post time

        # --- Generate SEO content ---
        print("Generating timestamps and description...")
        timestamps, description = generate_timestamps_and_description(
            formatted_transcript, args.gemini_api_key
        )

        full_description = timestamps + "\n\n" + description

        print(full_description)

        # --- Optionally post to YouTube ---
        if args.post:
            youtube = get_authenticated_service()

            if target_video_id:
                # URL mode — post to the specified video
                title = get_video_title(youtube, target_video_id)
                print(f"\nTarget video: {title} ({target_video_id})")
            else:
                # File mode — post to latest upload
                target_video_id, title, _ = get_latest_video(youtube)
                print(f"\nLatest video: {title} ({target_video_id})")

            # Proceed directly without manual confirmation
            update_video_description(youtube, target_video_id, full_description)
            print("Done.")
        else:
            print("\n(Use --post to automatically update the YouTube video description)")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
