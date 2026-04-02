#!/usr/bin/env python3
"""
发现 Skill — 浏览、搜索、查看详情

⚠️ 本脚本已迁移至 xgjk-base-skills/scripts/skill_registry/find_skills.py
   此文件仅作为转发层保留向后兼容，实际逻辑由 base-skills 提供。

使用方式：
  python3 cms-create-skill/scripts/skill-management/get_skills.py
  python3 cms-create-skill/scripts/skill-management/get_skills.py --search "机器人"
  python3 cms-create-skill/scripts/skill-management/get_skills.py --detail "im-robot"

推荐直接使用：
  python3 xgjk-base-skills/scripts/skill_registry/find_skills.py
"""

import sys
import os

# 转发到 xgjk-base-skills
_BASE_REGISTRY = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'xgjk-base-skills', 'scripts', 'skill_registry'
))

if os.path.isdir(_BASE_REGISTRY):
    sys.path.insert(0, _BASE_REGISTRY)
    from find_skills import main
    main()
else:
    # Fallback：如果 base-skills 不存在，使用内联实现
    print("⚠️ 未找到 xgjk-base-skills，使用内联 fallback", file=sys.stderr)

    import json
    import argparse
    import requests
    import warnings

    # 禁用 InsecureRequestWarning (因为 verify=False)
    warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

    API_URL = 'https://skills.mediportal.com.cn/api/skill/list'

    parser = argparse.ArgumentParser(description="发现 Skill — 浏览、搜索、查看详情")
    parser.add_argument("--search", "-s", type=str, help="按关键词搜索 Skill")
    parser.add_argument("--detail", "-d", type=str, help="查看某个 Skill 的详情")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON 格式")
    args = parser.parse_args()

    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            verify=False,
            allow_redirects=True,
            timeout=60,
        )
        response.raise_for_status()
        result = response.json()
    except Exception as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    skills = result.get("data") or result.get("resultData") or []

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.detail:
        q = args.detail.lower()
        found = next((s for s in skills if (s.get("code") or "").lower() == q or (s.get("name") or "").lower() == q), None)
        if found:
            for k, v in found.items():
                print(f"  {k}: {v}")
        else:
            print(f"未找到: {args.detail}", file=sys.stderr)
            sys.exit(1)
    elif args.search:
        kw = args.search.lower()
        matched = [s for s in skills if kw in (s.get("name") or "").lower() or kw in (s.get("description") or "").lower() or kw in (s.get("code") or "").lower()]
        print(f"匹配 {len(matched)} 个")
        for s in matched:
            print(f"  {s.get('code', '')} - {s.get('name', '')} - {(s.get('description') or '')[:40]}")
    else:
        for i, s in enumerate(skills, 1):
            print(f"  {i}. {s.get('code', '')} ({s.get('name', '')}) v{s.get('clawVersion', '')}")
        print(f"\n共 {len(skills)} 个 Skill")
