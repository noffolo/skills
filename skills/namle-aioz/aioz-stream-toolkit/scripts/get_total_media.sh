#!/bin/bash
# Get total media count via POST /media with optional search and page filters
# Usage: ./get_total_media.sh PUBLIC_KEY SECRET_KEY [SEARCH] [PAGE]

PUBLIC_KEY="$1"
SECRET_KEY="$2"
SEARCH="$3"
PAGE="$4"

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ]; then
  echo "Usage: $0 PUBLIC_KEY SECRET_KEY [SEARCH] [PAGE]"
    exit 1
fi

if [ -n "$PAGE" ] && ! [[ "$PAGE" =~ ^[0-9]+$ ]]; then
  echo "Error: PAGE must be a non-negative integer"
  exit 1
fi

if [ -n "$SEARCH" ] && [ -n "$PAGE" ]; then
  REQUEST_BODY="{\"search\": \"$SEARCH\", \"page\": $PAGE}"
elif [ -n "$SEARCH" ]; then
  REQUEST_BODY="{\"search\": \"$SEARCH\"}"
elif [ -n "$PAGE" ]; then
  REQUEST_BODY="{\"page\": $PAGE}"
else
  REQUEST_BODY='{}'
fi

curl -s -X POST 'https://api.aiozstream.network/api/media' \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "$REQUEST_BODY"