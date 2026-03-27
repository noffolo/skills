#!/bin/bash
# Get video URL by name via POST /media with only PUBLIC_KEY, SECRET_KEY and video name in body
# Usage: ./get_video_url_by_name.sh PUBLIC_KEY SECRET_KEY VIDEO_NAME

PUBLIC_KEY="$1"
SECRET_KEY="$2"
VIDEO_NAME="$3"

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$VIDEO_NAME" ]; then
    echo "Usage: $0 PUBLIC_KEY SECRET_KEY VIDEO_NAME"
    exit 1
fi

curl -s -X POST 'https://api.aiozstream.network/api/media' \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "{\"search\": \"$VIDEO_NAME\"}"