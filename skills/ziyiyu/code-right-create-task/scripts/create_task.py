#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_API_BASE = "http://101.34.66.108/code-right"


def _env(name: str) -> str | None:
    v = os.environ.get(name)
    return v.strip() if isinstance(v, str) else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Create Code-Right task via API.")
    parser.add_argument("--system-name", default=_env("SYSTEM_NAME"))
    parser.add_argument("--notify-email", default=_env("NOTIFY_EMAIL"))
    parser.add_argument(
        "--access-token",
        default=_env("ACCESS_TOKEN"),
        help="Optional access_token header. If omitted, backend will create session token.",
    )
    args = parser.parse_args()

    if not args.system_name:
        print("SYSTEM_NAME is required (env SYSTEM_NAME or --system-name).", file=sys.stderr)
        return 2
    if not args.notify_email:
        print("NOTIFY_EMAIL is required (env NOTIFY_EMAIL or --notify-email).", file=sys.stderr)
        return 2

    api_base = DEFAULT_API_BASE.rstrip("/")
    url = f"{api_base}/api/tasks/"

    payload = {"systemName": args.system_name, "notifyEmail": args.notify_email}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    headers = {"Content-Type": "application/json"}
    if args.access_token:
        headers["access_token"] = args.access_token

    req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(body)
            return 0
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        print(f"HTTP {e.code}: {err}", file=sys.stderr)
        return 1
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

