#!/usr/bin/env python3
"""
发布（注册）新 Skill

用途：向平台注册一个新的 AI Skill（ClawHub 协议格式）

使用方式：
  python3 cms-create-skill/scripts/skill-management/register_skill.py --code <code> --name <name> [--description <desc>] [--download-url <url>] [--label <label>] [--internal]

参数说明：
  --code          Skill 唯一标识（必须）
  --name          Skill 显示名称（必须）
  --description   Skill 描述
  --download-url  Skill 包下载地址
  --label         Skill 标签（逗号分隔）
  --internal      标记为内部 Skill
  --version       版本号（semver 格式，如 1.0.0，默认 0.0.1）

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

API_URL = 'https://skills.mediportal.com.cn/api/skill/register'


def call_api(token: str, payload: dict) -> dict:
    """注册新 Skill（ClawHub 格式）"""
    headers = {
        "access-token": token,
        "Content-Type": "application/json",
    }

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


def build_clawhub_payload(args) -> dict:
    """将 CLI 参数转换为 ClawHub 协议格式。"""
    tags = [t.strip() for t in args.label.split(",") if t.strip()] if args.label else []

    payload = {
        "name": args.code,
        "skillCode": args.code,
        "displayName": args.name,
        "clawVersion": args.version,
        "description": args.description,
        "downloadUrl": args.download_url,
        "metadata": {
            "openclaw": {
                "tags": tags,
            },
            "xgjk": {
                "isInternal": args.internal,
            },
        },
    }
    return payload


def main():
    token = os.environ.get("XG_USER_TOKEN") or os.environ.get("access-token") or os.environ.get("ACCESS_TOKEN")

    if not token:
        print("错误: 请设置环境变量 XG_USER_TOKEN", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="发布（注册）新 Skill")
    parser.add_argument("--code", required=True, help="Skill 唯一标识")
    parser.add_argument("--name", required=True, help="Skill 显示名称")
    parser.add_argument("--description", default="", help="Skill 描述")
    parser.add_argument("--download-url", default="", help="Skill 包下载地址")
    parser.add_argument("--label", default="", help="Skill 标签（逗号分隔）")
    parser.add_argument("--internal", action="store_true", help="标记为内部 Skill")
    parser.add_argument("--version", default="0.0.1", help="版本号（semver，默认 0.0.1）")
    args = parser.parse_args()

    payload = build_clawhub_payload(args)
    result = call_api(token, payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
