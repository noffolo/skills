#!/usr/bin/env python3
"""
一站式发布 Skill（内部：打包 → 上传七牛 → 注册/更新；外部：直接注册/更新）

用途：
  将指定 Skill 目录一键完成发布到平台（ClawHub 协议格式）。
  - 内部模式：打包 ZIP → 上传到七牛 → 注册/更新
  - 外部模式：跳过七牛上传，直接使用 ClawHub 下载地址注册/更新

使用方式：
  # 首次发布（注册）
  python3 cms-create-skill/scripts/skill-management/publish_skill.py ./im-robot --code im-robot --name "IM 机器人"

  # 更新已有 Skill（加 --update）
  python3 cms-create-skill/scripts/skill-management/publish_skill.py ./im-robot --code im-robot --update [--name "新名称"] [--version 1.2.0]

  # 外部 Skill（ClawHub）发布
  python3 cms-create-skill/scripts/skill-management/publish_skill.py ./im-robot --code im-robot --name "IM 机器人" --external

参数说明：
  skill_dir       Skill 目录路径（必须）
  --code          Skill 唯一标识（必须）
  --name          Skill 显示名称（注册时必须，更新时可选）
  --description   Skill 描述
  --label         Skill 标签（逗号分隔）
  --version       版本号（semver 格式，如 1.2.0，默认 0.0.1）
  --update        更新模式（默认为注册模式）
  --output        ZIP 输出路径（可选）
  --file-key      七牛文件 key（可选，默认自动生成）
  --internal      标记为内部 Skill（默认发布链路）
  --external      标记为外部 Skill（使用 ClawHub 下载地址）
  --sync-clawhub  同步到 ClawHub（内部 Skill 默认启用，外部 Skill 不支持）
  --no-sync-clawhub  不同步到 ClawHub
  --sync-github   同步到 GitHub（内部 Skill 默认启用，外部 Skill 可手动启用）
  --no-sync-github  不同步到 GitHub

环境变量：
  XG_USER_TOKEN  — access-token（必须）
"""

import sys
import os
import json
import time
import argparse
import requests
import warnings
from urllib.parse import quote

warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# 导入同目录下的模块
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from pack_skill import pack_skill
from upload_to_qiniu import get_qiniu_token, upload_file
from register_skill import call_api as register_api
from update_skill import call_api as update_api

PLATFORM_API_BASE = 'https://skills.mediportal.com.cn/api'
ROBOT_SYNC_URL = f'{PLATFORM_API_BASE}/robot/skill-sync'

EXTERNAL_DOWNLOAD_URL_TEMPLATE = "https://wry-manatee-359.convex.site/api/v1/download?slug={}"


def build_external_download_url(skill_code: str) -> str:
    return EXTERNAL_DOWNLOAD_URL_TEMPLATE.format(quote(skill_code, safe=""))


def build_register_payload(args, download_url: str, is_internal: bool) -> dict:
    """构造 ClawHub 协议格式的注册 payload。"""
    tags = [t.strip() for t in args.label.split(",") if t.strip()] if args.label else []
    return {
        "name": args.code,
        "skillCode": args.code,
        "displayName": args.name,
        "clawVersion": args.version,
        "description": args.description,
        "downloadUrl": download_url,
        "metadata": {
            "openclaw": {"tags": tags},
            "xgjk": {"isInternal": is_internal},
        },
    }


def build_update_payload(args, download_url: str, is_internal: bool) -> dict:
    """构造 ClawHub 协议格式的更新 payload。"""
    tags = [t.strip() for t in args.label.split(",") if t.strip()] if args.label else []
    payload = {
        "name": args.code,
        "skillCode": args.code,
        "downloadUrl": download_url,
        "metadata": {
            "openclaw": {"tags": tags},
            "xgjk": {"isInternal": is_internal},
        },
    }
    if args.name:
        payload["displayName"] = args.name
    if args.description:
        payload["description"] = args.description
    if args.version:
        payload["clawVersion"] = args.version
    return payload


def dispatch_skill_sync(token: str, action: str, args, download_url: str,
                        sync_clawhub: bool, sync_github: bool) -> dict:
    """调用 /api/robot/skill-sync 派发机器人同步任务。"""
    headers = {
        "access-token": token,
        "Content-Type": "application/json",
    }
    payload = {
        "action": action,
        "skillCode": args.code,
        "name": args.name or args.code,
        "description": args.description or "",
        "clawVersion": args.version or "0.0.1",
        "downloadUrl": download_url,
        "deleted": False,
        "syncClawhub": sync_clawhub,
        "syncGithub": sync_github,
    }

    response = requests.post(
        ROBOT_SYNC_URL,
        headers=headers,
        json=payload,
        verify=False,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def main():
    token = os.environ.get("XG_USER_TOKEN") or os.environ.get("access-token") or os.environ.get("ACCESS_TOKEN")
    if not token:
        print("错误: 请设置环境变量 XG_USER_TOKEN", file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="一站式发布 Skill")
    parser.add_argument("skill_dir", help="Skill 目录路径")
    parser.add_argument("--code", required=True, help="Skill 唯一标识")
    parser.add_argument("--name", default="", help="Skill 显示名称（注册时必须）")
    parser.add_argument("--description", default="", help="Skill 描述")
    parser.add_argument("--label", default="", help="Skill 标签（逗号分隔）")
    parser.add_argument("--version", default="0.0.1", help="版本号（semver 格式，默认 0.0.1）")
    parser.add_argument("--update", action="store_true", help="更新模式（默认为注册模式）")
    parser.add_argument("--output", default="", help="ZIP 输出路径")
    parser.add_argument("--file-key", default="", help="七牛文件 key")
    parser.add_argument("--internal", action="store_true", help="标记为内部 Skill")
    parser.add_argument("--external", action="store_true", help="标记为外部 Skill（使用 ClawHub 下载地址）")
    parser.add_argument("--sync-clawhub", dest="sync_clawhub", action="store_true", default=None,
                        help="同步到 ClawHub（内部 Skill 默认启用）")
    parser.add_argument("--no-sync-clawhub", dest="sync_clawhub", action="store_false",
                        help="不同步到 ClawHub")
    parser.add_argument("--sync-github", dest="sync_github", action="store_true", default=None,
                        help="同步到 GitHub（内部 Skill 默认启用）")
    parser.add_argument("--no-sync-github", dest="sync_github", action="store_false",
                        help="不同步到 GitHub")
    args = parser.parse_args()

    if args.internal and args.external:
        print("错误: --internal 和 --external 不能同时使用", file=sys.stderr)
        sys.exit(1)

    is_external = args.external
    is_internal = not is_external

    # 解析同步标志：内部默认两者都推；外部默认不推 clawhub，github 需手动指定
    if is_internal:
        sync_clawhub = args.sync_clawhub if args.sync_clawhub is not None else True
        sync_github = args.sync_github if args.sync_github is not None else True
    else:
        # 外部 Skill 不支持推送到 ClawHub
        if args.sync_clawhub is True:
            print("警告: 外部 Skill 不支持推送到 ClawHub，已忽略 --sync-clawhub", file=sys.stderr)
        sync_clawhub = False
        sync_github = args.sync_github if args.sync_github is not None else False

    mode = "更新" if args.update else "注册"
    if not args.update and not args.name:
        print("错误: 注册模式下 --name 是必须的", file=sys.stderr)
        sys.exit(1)

    skill_name = os.path.basename(os.path.abspath(args.skill_dir))

    if is_internal:
        # ── Step 1: 打包 ──
        zip_output = args.output or f"{skill_name}.zip"
        print(f"\n{'='*50}", file=sys.stderr)
        print(f"[Step 1/3] 打包 Skill 目录 → ZIP", file=sys.stderr)
        print(f"{'='*50}", file=sys.stderr)
        zip_path = pack_skill(args.skill_dir, zip_output)

        # ── Step 2: 上传七牛 ──
        file_key = args.file_key or f"skills/{args.code}/{int(time.time())}-{os.path.basename(zip_path)}"
        print(f"\n{'='*50}", file=sys.stderr)
        print(f"[Step 2/3] 上传到七牛 (fileKey={file_key})", file=sys.stderr)
        print(f"{'='*50}", file=sys.stderr)

        creds = get_qiniu_token(token, file_key)
        qiniu_token = creds["token"]
        domain = creds["domain"]
        print(f"凭证获取成功，domain={domain}", file=sys.stderr)

        size_kb = os.path.getsize(zip_path) / 1024
        print(f"上传 {os.path.basename(zip_path)} ({size_kb:.1f} KB) ...", file=sys.stderr)
        upload_file(qiniu_token, file_key, zip_path)

        base_url = domain if domain.startswith("http") else f"https://{domain}"
        download_url = f"{base_url.rstrip('/')}/{file_key}"
        print(f"上传成功! 下载地址: {download_url}", file=sys.stderr)
    else:
        print(f"\n{'='*50}", file=sys.stderr)
        print(f"[Step 1/2] 外部 Skill 模式：跳过七牛上传", file=sys.stderr)
        print(f"{'='*50}", file=sys.stderr)
        download_url = build_external_download_url(args.code)
        print(f"外部 Skill 下载地址: {download_url}", file=sys.stderr)

    # ── Step 3: 注册/更新 ──
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"[{3 if is_internal else 2}/{3 if is_internal else 2}] {mode} Skill (code={args.code})", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    if args.update:
        payload = build_update_payload(args, download_url, is_internal)
        result = update_api(token, payload)
    else:
        payload = build_register_payload(args, download_url, is_internal)
        result = register_api(token, payload)

    print(f"\n{'='*50}", file=sys.stderr)
    print(f"✅ {mode}完成!", file=sys.stderr)
    print(f"  Skill: {args.code}", file=sys.stderr)
    print(f"  下载地址: {download_url}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    # ── Step 4: 机器人同步（ClawHub / GitHub） ──
    if sync_clawhub or sync_github:
        targets = []
        if sync_clawhub:
            targets.append("ClawHub")
        if sync_github:
            targets.append("GitHub")
        target_str = " + ".join(targets)

        print(f"\n{'='*50}", file=sys.stderr)
        print(f"[机器人同步] 派发 {target_str} 同步任务...", file=sys.stderr)
        print(f"{'='*50}", file=sys.stderr)

        try:
            action = "update" if args.update else "publish"
            sync_result = dispatch_skill_sync(
                token, action, args, download_url, sync_clawhub, sync_github
            )
            print(f"✅ 机器人同步任务已派发: {target_str}", file=sys.stderr)
            result["robotSync"] = sync_result
        except Exception as e:
            print(f"⚠️ 机器人同步任务派发失败: {e}", file=sys.stderr)
            result["robotSyncError"] = str(e)
    else:
        print(f"\n跳过机器人同步（未指定 --sync-clawhub / --sync-github）", file=sys.stderr)

    # 输出完整结果到 stdout
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
