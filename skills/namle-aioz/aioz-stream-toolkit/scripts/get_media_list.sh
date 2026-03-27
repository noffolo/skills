#!/bin/bash
# Get media list via GET /media with optional search and page filters
# Usage: ./get_media_list.sh PUBLIC_KEY SECRET_KEY [SEARCH] [PAGE]

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

QUERY=""

if [ -n "$SEARCH" ]; then
  ENCODED_SEARCH="${SEARCH// /%20}"
  QUERY="?search=$ENCODED_SEARCH"
fi

if [ -n "$PAGE" ]; then
  if [ -n "$QUERY" ]; then
    QUERY="$QUERY&page=$PAGE"
  else
    QUERY="?page=$PAGE"
  fi
fi

curl -s -X GET "https://api.aiozstream.network/api/media$QUERY" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY"