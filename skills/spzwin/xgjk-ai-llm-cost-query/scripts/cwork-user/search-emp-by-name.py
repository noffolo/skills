#!/usr/bin/env python3
"""
cwork-user / 按姓名搜索员工

用途：调用 GET /open-api/cwork-user/searchEmpByName，为查询他人 AI 费用解析 personId。

使用方式：
  python3 scripts/cwork-user/search-emp-by-name.py --search-key "张三"

环境变量：
  XG_BIZ_API_KEY 或 XG_APP_KEY — appKey（鉴权类型 appKey）
  以上建议按 cms-auth-skills/SKILL.md 预先准备
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = (
    "https://sg-al-cwork-web.mediportal.com.cn/open-api/cwork-user/searchEmpByName"
)
AUTH_MODE = "appKey"
MAX_RETRIES = 3
RETRY_DELAY_SEC = 1.0


def build_headers() -> dict:
    headers = {"Accept": "application/json"}
    if AUTH_MODE == "appKey":
        app_key = os.environ.get("XG_BIZ_API_KEY") or os.environ.get("XG_APP_KEY")
        if not app_key:
            print("错误: 请设置环境变量 XG_BIZ_API_KEY 或 XG_APP_KEY", file=sys.stderr)
            sys.exit(1)
        headers["appKey"] = app_key
    return headers


def _should_retry(exc: BaseException) -> bool:
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code >= 500
    if isinstance(exc, urllib.error.URLError):
        return True
    return False


def call_api(search_key: str, timeout: int = 60) -> dict:
    params = urllib.parse.urlencode({"searchKey": search_key})
    url = f"{API_BASE}?{params}"
    headers = build_headers()
    last_error: BaseException | None = None
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError) as e:
            last_error = e
            if attempt < MAX_RETRIES - 1 and _should_retry(e):
                time.sleep(RETRY_DELAY_SEC)
                continue
            raise
    assert last_error is not None
    raise last_error


def main() -> None:
    parser = argparse.ArgumentParser(description="按姓名搜索员工（searchEmpByName）")
    parser.add_argument(
        "--search-key",
        required=True,
        help="姓名模糊搜索关键词",
    )
    args = parser.parse_args()
    result = call_api(args.search_key.strip())
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
