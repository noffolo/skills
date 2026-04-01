#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查所有 Skill 的发布状态
用法:
  python scripts/check_status.py [slug]     # 查看指定 Skill
  python scripts/check_status.py all         # 查看所有 Skills
  python scripts/check_status.py --watch     # 持续监控（每 30 秒）
"""
import json, os, subprocess, sys, time
from pathlib import Path

WORKSPACE = "/home/node/.openclaw/workspace/skills"
SKILL_PKG = Path(__file__).resolve().parent.parent
ENV_FILE   = SKILL_PKG / ".env"

# 平台定义
PLATFORMS = {
    "clawhub": {
        "name": "ClawHub",
        "color": "\033[0;32m",  # 绿色
        "check": "clawhub",
        "auto": True
    },
    "github": {
        "name": "GitHub",
        "color": "\033[0;34m",  # 蓝色
        "check": "github",
        "auto": True
    },
    "skillzwave": {
        "name": "SkillzWave",
        "color": "\033[0;35m",  # 紫色
        "check": "manual",
        "auto": False
    },
    "coze": {
        "name": "COZE",
        "color": "\033[0;36m",  # 青色
        "check": "manual",
        "auto": False
    },
    "yuanqi": {
        "name": "腾讯元器",
        "color": "\033[0;33m",  # 黄色
        "check": "manual",
        "auto": False
    },
    "bailian": {
        "name": "阿里百炼",
        "color": "\033[0;34m",  # 蓝色
        "check": "manual",
        "auto": False
    }
}

def load_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env

def check_clawhub(slug):
    try:
        r = subprocess.run(
            ['npx', '-y', 'clawhub', 'inspect', slug, '--json'],
            capture_output=True, text=True, timeout=15, cwd=str(SKILL_PKG)
        )
        data = json.loads(r.stdout)
        s = data.get('skill', {})
        stats = s.get('stats', {})
        ver = s.get('tags', {}).get('latest', '?')
        return {
            'status': '✅ 已发布',
            'version': ver,
            'downloads': stats.get('downloads', 0),
            'stars': stats.get('stars', 0),
            'url': f'https://clawhub.ai/skills/{slug}'
        }
    except Exception as e:
        return {'status': f'❌ ({str(e)[:40]})', 'version': '?', 'downloads': 0, 'stars': 0, 'url': ''}

def check_github(slug):
    env = load_env()
    token = env.get('GITHUB_TOKEN', '')
    try:
        import urllib.request
        url = f"https://api.github.com/repos/ryanbihai/{slug}"
        headers = {"Authorization": f"token {token}"} if token else {}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return {
                'status': '✅ 已推送',
                'stars': data.get('stargazers_count', 0),
                'forks': data.get('forks_count', 0),
                'updated': data.get('updated_at', '')[:10],
                'url': data.get('html_url', '')
            }
    except:
        return {'status': '❌ 未配置/未推送', 'stars': 0, 'forks': 0, 'url': ''}

def get_local_info(slug):
    p = Path(WORKSPACE) / slug / "_meta.json"
    if p.exists():
        d = json.load(open(p))
        return d.get('version', '?'), d.get('changelog', '')[:50] if d.get('changelog') else '无更新说明'
    return '?', '目录不存在'

def print_skill_status(slug):
    ver, changelog = get_local_info(slug)
    
    print()
    print("━" * 56)
    print(f"📦 {slug}")
    print(f"   本地版本: v{ver}")
    print(f"   更新说明: {changelog}")
    print()
    
    env = load_env()
    
    # ClawHub
    color = PLATFORMS['clawhub']['color']
    if env.get('CLAWHUB_TOKEN'):
        ch = check_clawhub(slug)
        print(f"   🌐 ClawHub:  {ch['status']} | v{ch['version']} | ↓{ch['downloads']} | ⭐{ch['stars']}")
        if ch['url']:
            print(f"      {ch['url']}")
    else:
        print(f"   🌐 ClawHub:  ⏳ 未配置 Token（跳过）")
    
    # GitHub
    gh = check_github(slug)
    print(f"   💻 GitHub:   {gh['status']} | ⭐{gh['stars']} | 更新:{gh.get('updated','?')}")
    if gh['url']:
        print(f"      {gh['url']}")
    
    # 手动平台
    print()
    print("   ⏳ 手动平台（需人工提交）:")
    print("      🌊 SkillzWave: https://skillzwave.ai/submit/")
    print("      🤖 COZE:      https://www.coze.cn/store/market/bot")
    print("      🟡 腾讯元器:   https://yuanqi.tencent.com/market")
    print("      🔵 阿里百炼:   https://bailian.console.aliyun.com")
    
    print()
    print("   💡 生成提交文本:")
    print(f"      python scripts/gen_submission.py {slug}")

def list_skills():
    """列出所有本地 Skills"""
    skills = []
    for d in Path(WORKSPACE).iterdir():
        if d.is_dir() and (d / "_meta.json").exists():
            skills.append(d.name)
    return sorted(skills)

def main():
    args = sys.argv[1:]
    
    # 解析参数
    slug = None
    watch = False
    
    for arg in args:
        if arg == '--watch':
            watch = True
        elif arg == 'all':
            slug = None
        elif not arg.startswith('-'):
            slug = arg
    
    if watch:
        print("🔄 持续监控模式（Ctrl+C 退出）")
        while True:
            if slug:
                print_skill_status(slug)
            else:
                for s in list_skills():
                    print_skill_status(s)
            print("\n⏰ 30 秒后刷新...")
            time.sleep(30)
            print("\033[2J\033[H")  # 清屏
    elif slug:
        print_skill_status(slug)
    else:
        skills = list_skills()
        if not skills:
            print("❌ 未找到任何 Skill")
            print(f"   请确认 Skills 目录: {WORKSPACE}")
            return
        
        print()
        print("━" * 56)
        print(f"📊 所有 Skills（共 {len(skills)} 个）")
        print("━" * 56)
        
        for s in skills:
            print_skill_status(s)
    
    print()
    print("━" * 56)
    print("💡 提示：")
    print("   • 查看指定 Skill: python scripts/check_status.py <slug>")
    print("   • 持续监控: python scripts/check_status.py <slug> --watch")
    print("   • 发布 Skill: python scripts/publish.sh <slug>")
    print("━" * 56)

if __name__ == '__main__':
    main()
