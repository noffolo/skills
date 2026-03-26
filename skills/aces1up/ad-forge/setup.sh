#!/usr/bin/env bash
# Phantom Browser -- Setup: register interest, capture email, track install.
# Run once after `openclaw install phantom-browser`.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INTEREST_URL="https://clawagents.dev/reddit-rank/v1/phantom-browser/interest"
PB_DIR="$HOME/.phantom-browser"
PB_CONFIG="$PB_DIR/config.json"
VENV_DIR="$SCRIPT_DIR/.venv"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}Phantom Browser${NC} Setup"
echo -e "Undetectable browser automation for AI agents. 31/31 stealth tests."
echo ""

# -- 0. Check prerequisites ---------------------------------------------------

check_cmd() {
  if ! command -v "$1" &>/dev/null; then
    echo -e "${RED}Missing required command: $1${NC}"
    echo -e "Install it first:  ${BOLD}$2${NC}"
    exit 1
  fi
}

check_cmd curl "apt install curl  /  brew install curl"
check_cmd python3 "apt install python3  /  brew install python3"

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
  echo -e "${RED}Python 3.10+ required (found $PY_VER)${NC}"
  exit 1
fi
echo -e "  ${DIM}Python $PY_VER${NC}"

# -- 1. Create venv + install dependencies ------------------------------------

if [ ! -d "$VENV_DIR" ]; then
  echo -e "  Creating virtual environment..."

  if ! python3 -m venv "$VENV_DIR" 2>/dev/null; then
    echo -e "${YELLOW}  python3-venv not installed. Trying to install...${NC}"
    if command -v apt &>/dev/null; then
      sudo apt install -y python3-venv 2>/dev/null || true
    fi
    python3 -m venv "$VENV_DIR" || {
      echo -e "${RED}  Failed to create venv. Install python3-venv manually.${NC}"
      exit 1
    }
  fi
fi

source "$VENV_DIR/bin/activate"
echo -e "  ${DIM}venv: $VENV_DIR${NC}"

echo -e "  Installing dependencies..."
pip install -q --upgrade pip 2>/dev/null || true
pip install -q -r "$SCRIPT_DIR/requirements.txt"
echo -e "  ${GREEN}Dependencies installed${NC}"
echo ""

# -- 2. Generate install ID ---------------------------------------------------

mkdir -p "$PB_DIR"

if [ -f "$PB_CONFIG" ]; then
  INSTALL_ID=$(python3 -c "import json; print(json.load(open('$PB_CONFIG')).get('install_id',''))" 2>/dev/null || echo "")
fi

if [ -z "${INSTALL_ID:-}" ]; then
  INSTALL_ID=$(python3 -c "import uuid; print(uuid.uuid4().hex[:16])")
fi

# -- 3. Collect info -----------------------------------------------------------

echo -e "${BOLD}Early Access Registration${NC}"
echo ""
echo -e "  Phantom Browser is in limited early access."
echo -e "  Register below to be first in line when we open spots."
echo ""

read -rp "  Email: " USER_EMAIL

echo ""
echo -e "  What will you use Phantom Browser for?"
echo -e "    ${DIM}1) Social media automation${NC}"
echo -e "    ${DIM}2) Web scraping / data extraction${NC}"
echo -e "    ${DIM}3) Multi-account management${NC}"
echo -e "    ${DIM}4) Outreach / lead gen${NC}"
echo -e "    ${DIM}5) Competitor monitoring${NC}"
echo -e "    ${DIM}6) Something else${NC}"
read -rp "  Choice (1-6): " USE_CHOICE

case "$USE_CHOICE" in
  1) USE_CASE="social_media_automation" ;;
  2) USE_CASE="web_scraping" ;;
  3) USE_CASE="account_management" ;;
  4) USE_CASE="outreach" ;;
  5) USE_CASE="competitor_monitoring" ;;
  *) USE_CASE="other" ;;
esac

# -- 4. Write config -----------------------------------------------------------

cat > "$SCRIPT_DIR/.env" <<ENVEOF
PB_INSTALL_ID=$INSTALL_ID
ENVEOF

python3 -c "
import json
config = {
    'install_id': '$INSTALL_ID',
    'email': '${USER_EMAIL:-}',
    'use_case': '$USE_CASE',
}
with open('$PB_CONFIG', 'w') as f:
    json.dump(config, f, indent=2)
"

echo ""
echo -e "  ${GREEN}Config saved to $PB_CONFIG${NC}"

# -- 5. Register interest (analytics) -----------------------------------------

echo -e "  Registering interest..."

PAYLOAD=$(python3 -c "
import json, platform
print(json.dumps({
    'email': '${USER_EMAIL:-}',
    'use_case': '$USE_CASE',
}))
")

RESULT=$(curl -s -X POST "$INTEREST_URL" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  --connect-timeout 5 \
  --max-time 10 2>/dev/null || echo '{"status":"error"}')

if echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if d.get('status')=='ok' else 1)" 2>/dev/null; then
  echo -e "  ${GREEN}Registered${NC}"
else
  echo -e "  ${YELLOW}Registration sent (server may be busy)${NC}"
fi

# -- Done ---------------------------------------------------------------------

echo ""
echo -e "${GREEN}${BOLD}Setup complete.${NC}"
echo ""
echo -e "  ${BOLD}Status:${NC} Early Access (waitlist)"
echo -e "  ${BOLD}What happens next:${NC}"
echo -e "    - We will email you when spots open"
echo -e "    - Run ${CYAN}python3 phantom_browser.py --status${NC} to check access"
echo ""
echo -e "  ${DIM}Product page: https://clawagents.dev/phantom-browser/${NC}"
echo -e "  ${DIM}Questions? DM us in the OpenClaw community${NC}"
echo ""
