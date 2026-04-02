#!/usr/bin/env python3
"""
下架（删除）Skill

用途：将已发布的 Skill 下架

使用方式：
  python3 cms-create-skill/scripts/skill-management/delete_skill.py --id <skill-id> [--reason <下架原因>]

参数说明：
  --id       Skill ID（必须）
  --reason   下架原因（可选）

环境变量：
  XG_USER_TOKEN  — access-token（必须）
"""

import sys
import os
import json
import argparse
import requests
import warnings

# 禁用 InsecureRequestWarning (因为 verify=False)
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

API_URL = 'https://skills.mediportal.com.cn/api/skill/delete'


def call_api(token: str, skill_id: str, reason: str = "") -> dict:
    """下架 Skill"""
    headers = {
        "access-token": token,
        "Content-Type": "application/json",
    }

    payload = {"id": skill_id}
    if reason:
        payload["delistReason"] = reason

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            verify=False,
            allow_redirects=True,
            timeout=60,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"错误: 请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    token = os.environ.get("XG_USER_TOKEN") or os.environ.get("access-token") or os.environ.get("ACCESS_TOKEN")

    if not token:
        print("错误: 请设置环境变量 XG_USER_TOKEN", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="下架（删除）Skill")
    parser.add_argument("--id", required=True, help="Skill ID")
    parser.add_argument("--reason", default="", help="下架原因")
    args = parser.parse_args()

    result = call_api(token, args.id, args.reason)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
