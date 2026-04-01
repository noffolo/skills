#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式 Token 配置向导
- 安全的交互式输入
- Token 只存储在用户本地 .env 文件，永不上传
- 支持分平台配置，每个平台独立询问
"""
import os, sys

WORKSPACE = "/home/node/.openclaw/workspace/skills/skill-publisher"
ENV_FILE = os.path.join(WORKSPACE, ".env")

PLATFORMS = {
    "github": {
        "name": "GitHub",
        "url": "https://github.com/settings/tokens",
        "token_name": "GITHUB_TOKEN",
        "scope": "repo (完整仓库访问)",
        "instructions": [
            "1. 打开 https://github.com/settings/tokens",
            "2. 点击 'Generate new token (classic)'",
            "3. 输入 Token 名称，例如 'openclaw-skill-publisher'",
            "4. 勾选 'repo' 权限（用于推送代码）",
            "5. 点击 'Generate token' 并复制生成的 Token",
        ],
        "required": False,
        "auto": True,
    },
    "clawhub": {
        "name": "ClawHub",
        "url": "https://clawhub.ai",
        "token_name": "CLAWHUB_TOKEN",
        "scope": "发布 Skills 到 ClawHub",
        "instructions": [
            "1. 打开 https://clawhub.ai",
            "2. 登录你的账号",
            "3. 访问个人设置或 API 页面获取 Token",
        ],
        "required": False,
        "auto": True,
    },
    "coze": {
        "name": "COZE/扣子",
        "url": "https://www.coze.cn",
        "token_name": "COZE_TOKEN",
        "scope": "API 调用（需开发者权限）",
        "instructions": [
            "1. 打开 https://www.coze.cn",
            "2. 登录后进入个人设置 → API Token",
            "3. 创建或复制你的 API Token",
            "⚠️ 注意：COZE API 提交智能体仍需人工审核",
        ],
        "required": False,
        "auto": False,
    },
    "yuanqi": {
        "name": "腾讯元器",
        "url": "https://yuanqi.tencent.com",
        "token_name": "YUANQI_TOKEN",
        "scope": "API 调用",
        "instructions": [
            "1. 打开 https://yuanqi.tencent.com",
            "2. 登录腾讯账号",
            "3. 在个人中心获取 API 密钥",
        ],
        "required": False,
        "auto": False,
    },
    "bailian": {
        "name": "阿里百炼",
        "url": "https://bailian.console.aliyun.com",
        "token_name": "BAILIAN_TOKEN",
        "scope": "API 调用",
        "instructions": [
            "1. 打开 https://bailian.console.aliyun.com",
            "2. 登录阿里云账号",
            "3. 在 API Key 管理页面创建或复制 Key",
        ],
        "required": False,
        "auto": False,
    },
}

def load_env():
    """加载现有 .env"""
    env = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    return env

def save_env(env):
    """保存到 .env"""
    os.makedirs(os.path.dirname(ENV_FILE), exist_ok=True)
    with open(ENV_FILE, 'w') as f:
        f.write("# Skill Publisher - Token 配置\n")
        f.write("# 此文件包含敏感信息，请勿上传到 GitHub\n\n")
        for key, value in sorted(env.items()):
            f.write(f"{key}={value}\n")
    print(f"\n✅ 已保存到 {ENV_FILE}")

def get_input_secure(prompt, default=None, password=False):
    """安全输入（支持密码模式）"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    try:
        if password:
            import getpass
            value = getpass.getpass(prompt)
            if not value and default:
                return default
        else:
            value = input(prompt).strip()
            if not value and default:
                return default
        return value
    except (EOFError, KeyboardInterrupt):
        print("\n\n操作已取消")
        sys.exit(0)

def show_banner():
    print("=" * 56)
    print("🔐 Skill Publisher - Token 配置向导")
    print("=" * 56)
    print()
    print("安全说明：")
    print("  • 所有 Token 仅存储在你本地机器的 .env 文件")
    print("  • 不会上传到 GitHub 或任何互联网服务")
    print("  • .env 文件已在 .gitignore 中，不会被提交")
    print()

def show_platform_info(platforms):
    print("\n📋 支持的平台：\n")
    print(f"  {'平台':<12} {'自动化':<8} {'Token':<18} {'状态'}")
    print(f"  {'-'*12} {'-'*8} {'-'*18} {'-'*10}")
    for key, info in platforms.items():
        auto = "✅ 自动" if info["auto"] else "⏳ 手动"
        has_token = "🔑 已配置" if os.environ.get(info["token_name"]) or load_env().get(info["token_name"]) else "— 未配置"
        print(f"  {info['name']:<12} {auto:<8} {info['token_name']:<18} {has_token}")
    print()

def main():
    show_banner()
    
    # 先显示平台概览
    show_platform_info(PLATFORMS)
    
    # 询问要配置哪些平台
    print("请选择要配置的平台（多个用逗号分隔）：")
    print("  1 = GitHub（推送代码用）")
    print("  2 = ClawHub（发布 Skills 用）")
    print("  3 = COZE/扣子")
    print("  4 = 腾讯元器")
    print("  5 = 阿里百炼")
    print("  0 = 全部配置")
    print("  q = 退出")
    print()
    
    try:
        choice = input("你的选择: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消")
        return
    
    if choice == 'q':
        return
    
    # 解析选择
    if choice == '0':
        selected = list(PLATFORMS.keys())
    else:
        index_map = {'1': 'github', '2': 'clawhub', '3': 'coze', '4': 'yuanqi', '5': 'bailian'}
        selected = [index_map.get(c.strip()) for c in choice.split(',') if index_map.get(c.strip())]
        if not selected:
            print("无效选择")
            return
    
    # 加载现有配置
    env = load_env()
    
    # 逐一配置
    for key in selected:
        info = PLATFORMS[key]
        print(f"\n{'='*56}")
        print(f"📦 配置 {info['name']}")
        print(f"{'='*56}")
        print(f"获取地址：{info['url']}")
        print(f"所需权限：{info['scope']}")
        print(f"环境变量：{info['token_name']}")
        print()
        print("操作步骤：")
        for step in info['instructions']:
            print(f"  {step}")
        print()
        
        # 获取 Token
        current = env.get(info['token_name'], os.environ.get(info['token_name'], ''))
        token = get_input_secure(f"请输入 {info['name']} Token", default=current if current else None, password=True)
        
        if token:
            env[info['token_name']] = token
            print(f"✅ {info['name']} Token 已记录")
        elif info['required']:
            print(f"⚠️ {info['name']} 是必需的平台")
    
    # 保存
    save_env(env)
    
    print("\n" + "=" * 56)
    print("🎉 配置完成！")
    print("=" * 56)
    print()
    print("后续使用：")
    print("  python scripts/publish.sh <skill-slug>  # 发布 Skill")
    print("  python scripts/check_status.py          # 查看发布状态")
    print()

if __name__ == '__main__':
    main()
