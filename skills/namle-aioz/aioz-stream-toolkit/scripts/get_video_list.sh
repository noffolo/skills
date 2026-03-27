#!/bin/bash
# Get media list via POST /media with only PUBLIC_KEY and SECRET_KEY
# Usage: ./get_video_list.sh PUBLIC_KEY SECRET_KEY

PUBLIC_KEY="$1"
SECRET_KEY="$2"

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ] ; then
  echo "Usage: $0 PUBLIC_KEY SECRET_KEY"
    exit 1
fi

curl -s -X POST 'https://api.aiozstream.network/api/media' \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "{}"