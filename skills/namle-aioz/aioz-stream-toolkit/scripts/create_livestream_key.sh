#!/bin/bash
# Create livestream key with default configuration
# Usage: ./create_livestream_key.sh PUBLIC_KEY SECRET_KEY KEY_NAME

PUBLIC_KEY="$1"
SECRET_KEY="$2"
KEY_NAME="$3"

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$KEY_NAME" ]; then
    echo "Usage: $0 PUBLIC_KEY SECRET_KEY KEY_NAME"
    exit 1
fi

curl -s -X POST 'https://api.aiozstream.network/api/live_streams' \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "save": true,
    "type": "video",
    "name": "'"$KEY_NAME"'"
  }'