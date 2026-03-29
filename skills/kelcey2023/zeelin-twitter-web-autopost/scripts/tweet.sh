#!/bin/bash
# tweet.sh - open X compose page, type tweet, then post with preflight checks/retries.
# Usage: bash tweet.sh "tweet content" "base_url"

set -euo pipefail

TWEET_TEXT="${1:-}"
BASE_URL="${2:-https://x.com}"
CLI="${OPENCLAW_CLI:-openclaw browser}"

if [ -z "$TWEET_TEXT" ]; then
  echo "Error: Tweet content is required"
  exit 1
fi

get_snapshot() {
  local snap
  snap="$($CLI snapshot 2>/dev/null || true)"
  if [ -z "$snap" ]; then
    snap="$($CLI snapshot --interactive 2>/dev/null || true)"
  fi
  printf "%s" "$snap"
}

extract_first_ref() {
  grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//' || true
}

find_textbox_ref() {
  local snap="$1"
  local ref
  ref="$(
    echo "$snap" \
      | grep -Ei 'textbox' \
      | grep -Ei '帖子文本|post text|tweet text|what is happening|有什么新鲜事|发生了什么|compose post' \
      | extract_first_ref
  )"
  if [ -z "$ref" ]; then
    ref="$(
      echo "$snap" \
        | grep -Ei 'textbox' \
        | extract_first_ref
    )"
  fi
  printf "%s" "$ref"
}

list_textbox_refs() {
  local snap="$1"
  echo "$snap" \
    | grep -Ei 'textbox' \
    | grep -oE 'ref=e[0-9]+' \
    | sed 's/ref=//' \
    | awk '!seen[$0]++' || true
}

find_enabled_post_button() {
  local snap="$1"
  echo "$snap" \
    | grep -E 'button.*(发帖|发布|Post|Tweet)' \
    | grep -v '\[disabled\]' \
    | extract_first_ref
}

is_login_required() {
  local snap="$1"
  echo "$snap" | grep -qE 'Sign in|登录|登录 X|Create account|创建账号|电话、邮件地址或用户名'
}

find_success_signal() {
  local snap="$1"
  echo "$snap" | grep -qE 'Your post was sent|已发送|帖子已发送|Post sent|已发布'
}

echo "Starting browser..."
$CLI start >/dev/null 2>&1 || true

if ! $CLI status >/dev/null 2>&1; then
  echo "Error: OpenClaw browser relay unavailable. Please ensure gateway is online."
  exit 1
fi

echo "Opening compose page..."
$CLI open "${BASE_URL}/compose/post" >/dev/null 2>&1 || true
$CLI wait --time 2600 >/dev/null 2>&1 || sleep 3

SNAPSHOT="$(get_snapshot)"
if [ -z "$SNAPSHOT" ]; then
  echo "Error: No browser snapshot available."
  exit 1
fi

if is_login_required "$SNAPSHOT"; then
  echo "Error: X login required. Please login first."
  exit 1
fi

TEXTBOX_REF="$(find_textbox_ref "$SNAPSHOT")"
if [ -z "$TEXTBOX_REF" ]; then
  echo "Compose textbox not found, fallback to /home ..."
  $CLI open "${BASE_URL}/home" >/dev/null 2>&1 || true
  $CLI wait --time 2600 >/dev/null 2>&1 || sleep 3
  SNAPSHOT="$(get_snapshot)"
  TEXTBOX_REF="$(find_textbox_ref "$SNAPSHOT")"
fi

if [ -z "$TEXTBOX_REF" ]; then
  echo "Error: Could not find tweet input box"
  echo "$SNAPSHOT" | grep -iE 'textbox|input|post|tweet|compose|输入|发帖|发布|新鲜事|发生了什么' | head -60 || true
  exit 1
fi

echo "Typing into $TEXTBOX_REF ..."
$CLI click "$TEXTBOX_REF" >/dev/null 2>&1 || true
$CLI type "$TEXTBOX_REF" "$TWEET_TEXT" >/dev/null 2>&1 || true
$CLI wait --time 1200 >/dev/null 2>&1 || sleep 1

SNAPSHOT2="$(get_snapshot)"
POST_BUTTON_REF="$(find_enabled_post_button "$SNAPSHOT2")"

if [ -z "$POST_BUTTON_REF" ]; then
  echo "Post button disabled, retrying alternate textboxes..."
  while IFS= read -r ALT_REF; do
    [ -z "$ALT_REF" ] && continue
    $CLI click "$ALT_REF" >/dev/null 2>&1 || true
    $CLI type "$ALT_REF" "$TWEET_TEXT" >/dev/null 2>&1 || true
    $CLI wait --time 800 >/dev/null 2>&1 || sleep 1
    SNAPSHOT2="$(get_snapshot)"
    POST_BUTTON_REF="$(find_enabled_post_button "$SNAPSHOT2")"
    if [ -n "$POST_BUTTON_REF" ]; then
      TEXTBOX_REF="$ALT_REF"
      break
    fi
  done < <(list_textbox_refs "$SNAPSHOT2")
fi

echo "Trying publish hotkey first..."
$CLI click "$TEXTBOX_REF" >/dev/null 2>&1 || true
$CLI press "Meta+Enter" >/dev/null 2>&1 || true
$CLI press "Control+Enter" >/dev/null 2>&1 || true
$CLI wait --time 1800 >/dev/null 2>&1 || sleep 2

POSTED=0
for _ in 1 2 3 4 5 6 7 8; do
  SNAPSHOT3="$(get_snapshot)"
  if find_success_signal "$SNAPSHOT3"; then
    POSTED=1
    break
  fi

  POST_BUTTON_REF="$(find_enabled_post_button "$SNAPSHOT3")"
  if [ -n "$POST_BUTTON_REF" ]; then
    echo "Clicking post button: $POST_BUTTON_REF"
    $CLI click "$POST_BUTTON_REF" >/dev/null 2>&1 || true
  fi

  $CLI wait --time 900 >/dev/null 2>&1 || sleep 1
done

if [ "$POSTED" -eq 1 ]; then
  echo "Tweet published successfully."
else
  echo "Post action executed, but no explicit success signal detected yet. Please verify in timeline."
fi
