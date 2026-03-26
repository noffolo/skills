#!/usr/bin/env python3
"""
phantom_browser.py -- Phantom Browser CLI.

Early access status checker and interest tracker.
Full browser automation skill ships after early access opens.

Usage:
  python3 phantom_browser.py --status
  python3 phantom_browser.py --info
"""

import argparse
import json
import os
import sys

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
                           "requests", "python-dotenv"])
    import requests
    from dotenv import load_dotenv

# Load env
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_env_path = os.path.join(_SCRIPT_DIR, ".env")
if os.path.exists(_env_path):
    load_dotenv(_env_path)

_home_config = os.path.expanduser("~/.phantom-browser/config.json")
_config = {}
if os.path.exists(_home_config):
    try:
        with open(_home_config) as f:
            _config = json.load(f)
    except Exception:
        pass

VERSION = "0.1.0"
INTEREST_URL = "https://clawagents.dev/reddit-rank/v1/phantom-browser/interest"
PRODUCT_URL = "https://clawagents.dev/phantom-browser/"

CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
DIM = "\033[2m"
NC = "\033[0m"


def show_status():
    """Show current registration status."""
    install_id = _config.get("install_id") or os.environ.get("PB_INSTALL_ID", "")
    email = _config.get("email", "")

    print()
    print(f"  {CYAN}{BOLD}Phantom Browser{NC} v{VERSION}")
    print(f"  Undetectable browser automation for AI agents")
    print()

    if install_id:
        print(f"  {GREEN}Registered{NC}")
        print(f"  Install ID: {DIM}{install_id}{NC}")
        if email:
            print(f"  Email: {DIM}{email}{NC}")
        print()
        print(f"  {BOLD}Status:{NC} Early Access (waitlist)")
        print(f"  {BOLD}Access:{NC} {YELLOW}Pending{NC}")
        print()
        print(f"  We will notify you when spots open.")
        print(f"  Product page: {DIM}{PRODUCT_URL}{NC}")
    else:
        print(f"  {YELLOW}Not registered{NC}")
        print(f"  Run {CYAN}bash setup.sh{NC} to register for early access.")
    print()


def show_info():
    """Show product info."""
    print()
    print(f"  {CYAN}{BOLD}Phantom Browser{NC}")
    print(f"  Undetectable browser automation for AI agents")
    print()
    print(f"  {BOLD}What it does:{NC}")
    print(f"  Your AI agents browse the web, log into platforms, and interact")
    print(f"  with sites without getting flagged, throttled, or banned.")
    print()
    print(f"  {BOLD}How:{NC}")
    print(f"  - Tool layer (not CDP remote control)")
    print(f"  - WindMouse cursor physics (real curves, not straight lines)")
    print(f"  - Natural keystroke delays (variable, not uniform)")
    print(f"  - Per-profile fingerprinting (screen, fonts, GPU, timezone)")
    print(f"  - Residential IP routing (real ISPs, not datacenters)")
    print(f"  - Headless on $6/mo VPS (no GUI needed)")
    print(f"  - System-level agent access control")
    print()
    print(f"  {BOLD}Proof:{NC}")
    print(f"  - 31/31 stealth tests passed (bot.sannysoft.com)")
    print(f"  - Real GPU fingerprint (GTX 1650, not SwiftShader)")
    print(f"  - 762 lines custom stealth code")
    print()
    print(f"  {BOLD}Requirements:{NC}")
    print(f"  - VPS (Ubuntu, 2GB+ RAM, $6+/mo)")
    print(f"  - OpenClaw installed")
    print(f"  - Residential proxy (Decodo, Bright Data, IPRoyal)")
    print()
    print(f"  Product page: {DIM}{PRODUCT_URL}{NC}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Phantom Browser - Undetectable browser automation for AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--status", "-s", action="store_true",
                        help="Check registration and access status")
    parser.add_argument("--info", "-i", action="store_true",
                        help="Show product information")
    parser.add_argument("--version", action="version",
                        version=f"phantom-browser {VERSION}")

    args = parser.parse_args()

    if args.info:
        show_info()
    else:
        show_status()


if __name__ == "__main__":
    main()
