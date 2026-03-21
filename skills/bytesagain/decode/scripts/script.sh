#!/usr/bin/env bash
# decode — Encoder/decoder tool
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
set -euo pipefail
VERSION="3.0.1"

BOLD='\033[1m'; GREEN='\033[0;32m'; RED='\033[0;31m'; RESET='\033[0m'
die() { echo -e "${RED}Error: $1${RESET}" >&2; exit 1; }

# === base64-encode ===
cmd_base64_encode() {
    local input="${1:?Usage: decode base64-encode <text or file>}"
    if [ -f "$input" ]; then
        base64 "$input"
    else
        echo -n "$input" | base64
    fi
}

# === base64-decode ===
cmd_base64_decode() {
    local input="${1:?Usage: decode base64-decode <encoded-text>}"
    if [ -f "$input" ]; then
        base64 -d "$input"
    else
        echo -n "$input" | base64 -d 2>/dev/null || die "Invalid base64 input"
    fi
    echo ""
}

# === url-encode ===
cmd_url_encode() {
    local input="${1:?Usage: decode url-encode <text>}"
    python3 -c "
import sys
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
print(quote(sys.argv[1], safe=''))
" "$input"
}

# === url-decode ===
cmd_url_decode() {
    local input="${1:?Usage: decode url-decode <encoded-text>}"
    python3 -c "
import sys
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote
print(unquote(sys.argv[1]))
" "$input"
}

# === hex-encode ===
cmd_hex_encode() {
    local input="${1:?Usage: decode hex-encode <text>}"
    echo -n "$input" | xxd -p | tr -d '\n'
    echo ""
}

# === hex-decode ===
cmd_hex_decode() {
    local input="${1:?Usage: decode hex-decode <hex-string>}"
    echo -n "$input" | xxd -r -p 2>/dev/null || die "Invalid hex input"
    echo ""
}

# === jwt-decode ===
cmd_jwt_decode() {
    local token="${1:?Usage: decode jwt-decode <jwt-token>}"

    # JWT = header.payload.signature
    local header payload
    header=$(echo -n "$token" | cut -d. -f1)
    payload=$(echo -n "$token" | cut -d. -f2)

    [ -z "$header" ] && die "Invalid JWT: missing header"
    [ -z "$payload" ] && die "Invalid JWT: missing payload"

    # Fix base64url padding
    _b64url_decode() {
        local data="$1"
        # Replace URL-safe chars
        data=$(echo -n "$data" | tr '_-' '/+')
        # Add padding
        local pad=$((4 - ${#data} % 4))
        [ "$pad" -lt 4 ] && data="${data}$(printf '%0.s=' $(seq 1 $pad))"
        echo -n "$data" | base64 -d 2>/dev/null
    }

    echo -e "${BOLD}JWT Token${RESET}"
    echo ""
    echo -e "${BOLD}Header:${RESET}"
    _b64url_decode "$header" | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin),indent=2))" 2>/dev/null || echo "  (decode failed)"
    echo ""
    echo -e "${BOLD}Payload:${RESET}"
    _b64url_decode "$payload" | python3 -c "
import json, sys, time
data = json.load(sys.stdin)
for k,v in data.items():
    if k in ('exp','iat','nbf') and isinstance(v, (int,float)):
        ts = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(v))
        print('  {}: {} ({})'.format(k, v, ts))
    else:
        print('  {}: {}'.format(k, v))
" 2>/dev/null || echo "  (decode failed)"
    echo ""
    echo -e "${BOLD}Signature:${RESET}"
    echo "  $(echo -n "$token" | cut -d. -f3 | head -c 40)..."
}

# === html-encode ===
cmd_html_encode() {
    local input="${1:?Usage: decode html-encode <text>}"
    python3 -c "
import sys
try:
    from html import escape
except ImportError:
    from cgi import escape
print(escape(sys.argv[1]))
" "$input"
}

# === html-decode ===
cmd_html_decode() {
    local input="${1:?Usage: decode html-decode <encoded-text>}"
    python3 -c "
import sys
try:
    from html import unescape
except ImportError:
    from HTMLParser import HTMLParser
    unescape = HTMLParser().unescape
print(unescape(sys.argv[1]))
" "$input"
}

# === rot13 ===
cmd_rot13() {
    local input="${1:?Usage: decode rot13 <text>}"
    echo -n "$input" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
    echo ""
}

# === binary ===
cmd_binary_encode() {
    local input="${1:?Usage: decode binary <text>}"
    echo -n "$input" | xxd -b | awk '{for(i=2;i<=7;i++) printf "%s ", $i; print ""}'
}

# === detect: auto-detect encoding ===
cmd_detect() {
    local input="${1:?Usage: decode detect <text>}"

    echo -e "${BOLD}Encoding Detection${RESET}"

    # Check base64
    if echo -n "$input" | base64 -d > /dev/null 2>&1; then
        local decoded
        decoded=$(echo -n "$input" | base64 -d 2>/dev/null)
        if [ -n "$decoded" ] && echo "$input" | grep -qE '^[A-Za-z0-9+/=]+$'; then
            echo "  Base64 → $decoded"
        fi
    fi

    # Check JWT
    local dots
    dots=$(echo -n "$input" | tr -cd '.' | wc -c)
    if [ "$dots" -eq 2 ]; then
        echo "  JWT detected (use: decode jwt-decode)"
    fi

    # Check URL encoding
    if echo "$input" | grep -q '%[0-9A-Fa-f][0-9A-Fa-f]'; then
        echo "  URL-encoded → $(cmd_url_decode "$input")"
    fi

    # Check hex
    if echo "$input" | grep -qE '^[0-9a-fA-F]+$' && [ $((${#input} % 2)) -eq 0 ]; then
        local hex_decoded
        hex_decoded=$(echo -n "$input" | xxd -r -p 2>/dev/null)
        if [ -n "$hex_decoded" ]; then
            echo "  Hex → $hex_decoded"
        fi
    fi

    # Check HTML entities
    if echo "$input" | grep -q '&[a-z]*;'; then
        echo "  HTML-encoded → $(cmd_html_decode "$input")"
    fi
}

show_help() {
    cat << EOF
decode v$VERSION — Encoder/decoder tool

Usage: decode <command> <input>

Base64:
  base64-encode <text|file>     Encode to base64
  base64-decode <encoded>       Decode from base64

URL:
  url-encode <text>             URL-encode text
  url-decode <encoded>          URL-decode text

Hex:
  hex-encode <text>             Convert to hex
  hex-decode <hex>              Convert from hex

Web:
  html-encode <text>            HTML entity encode
  html-decode <encoded>         HTML entity decode
  jwt-decode <token>            Decode JWT token (header + payload + timestamps)

Other:
  rot13 <text>                  ROT13 cipher
  binary <text>                 Show binary representation
  detect <text>                 Auto-detect encoding and decode

  help                          Show this help
  version                       Show version

Requires: base64, xxd, python3
EOF
}

[ $# -eq 0 ] && { show_help; exit 0; }

case "$1" in
    base64-encode|b64e)  shift; cmd_base64_encode "$@" ;;
    base64-decode|b64d)  shift; cmd_base64_decode "$@" ;;
    url-encode|urle)     shift; cmd_url_encode "$@" ;;
    url-decode|urld)     shift; cmd_url_decode "$@" ;;
    hex-encode|hexe)     shift; cmd_hex_encode "$@" ;;
    hex-decode|hexd)     shift; cmd_hex_decode "$@" ;;
    jwt-decode|jwt)      shift; cmd_jwt_decode "$@" ;;
    html-encode)         shift; cmd_html_encode "$@" ;;
    html-decode)         shift; cmd_html_decode "$@" ;;
    rot13)               shift; cmd_rot13 "$@" ;;
    binary|bin)          shift; cmd_binary_encode "$@" ;;
    detect|auto)         shift; cmd_detect "$@" ;;
    help|-h)             show_help ;;
    version|-v)          echo "decode v$VERSION"; echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com" ;;
    *)                   echo "Unknown: $1"; show_help; exit 1 ;;
esac
