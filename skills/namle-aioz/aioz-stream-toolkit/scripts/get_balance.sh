#!/bin/bash
# Get user balance/info from AIOZ API
# Usage: ./get_balance.sh PUBLIC_KEY SECRET_KEY

PUBLIC_KEY="$1"
SECRET_KEY="$2"

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ]; then
    echo "Usage: $0 PUBLIC_KEY SECRET_KEY"
    exit 1
fi

# Send request to get user info / balance
RESPONSE=$(curl -s -X GET "https://api.aiozstream.network/api/user/me" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY")

echo "$RESPONSE" | jq . || echo "$RESPONSE"
