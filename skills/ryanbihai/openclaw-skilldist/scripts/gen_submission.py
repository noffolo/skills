#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为各平台生成提交文本
支持: COZE, 腾讯元器, 阿里百炼, SkillzWave
"""
import json, os, sys

WORKSPACE = "/home/node/.openclaw/workspace/skills"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

PLATFORMS = {
    "coze": {
        "name": "COZE/扣子",
        "url": "https://www.coze.cn/store/market/bot",
        "color": "\033[0;36m",
        "fields": ["bot_name", "description", "icon", "category", "tags"]
    },
    "skillzwave": {
        "name": "SkillzWave",
        "url": "https://skillzwave.ai/submit/",
        "color": "\033[0;35m",
        "fields": ["repo_url", "title", "description", "category", "tags", "preview"]
    },
    "yuanqi": {
        "name": "腾讯元器",
        "url": "https://yuanqi.tencent.com/market",
        "color": "\033[0;33m",
        "fields": ["name", "description", "icon", "category", "tags"]
    },
    "bailian": {
        "name": "阿里百炼",
        "url": "https://bailian.console.aliyun.com",
        "color": "\033[0;34m",
        "fields": ["name", "description", "category", "tags"]
    }
}

def load_skill(slug):
    """加载 Skill 元数据"""
    paths = [
        f"{WORKSPACE}/{slug}/_meta.json",
        f"{WORKSPACE}/{slug}/SKILL.md"
    ]
    data = {}
    for p in paths:
        if os.path.exists(p):
            if p.endswith('.json'):
                with open(p) as f:
                    data = json.load(f)
                    break
            else:
                data['description'] = open(p).read()[:500]
    return data

def gen_coze(data, slug):
    """生成 COZE 提交文本"""
    name = data.get('name', slug)
    desc = data.get('description', '')[:200]
    version = data.get('version', '1.0.0')
    tags = data.get('tags', [])
    
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 COZE/扣子 提交信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bot 名称: {name}
版本: {version}
描述: {desc}

【配置 JSON】
{{
  "bot_name": "{name}",
  "description": "{desc}",
  "icon": "图标URL（可选）",
  "category": "效率工具",
  "tags": {json.dumps(tags) if tags else '["openclaw", "skill"]'},
  "github_repo": "https://github.com/ryanbihai/{slug}"
}}

【提交步骤】
1. 打开 https://www.coze.cn/store/market/bot
2. 点击「创建 Bot」
3. 填写上述配置信息
4. 提交审核

【注意事项】
- Bot 需要人工审核
- 审核时间：1-3 个工作日
- 确保描述清晰、功能完整
"""

def gen_skillzwave(data, slug):
    """生成 SkillzWave 提交文本"""
    name = data.get('name', slug)
    desc = data.get('description', '')[:300]
    version = data.get('version', '1.0.0')
    tags = data.get('tags', [])
    repo_url = f"https://github.com/ryanbihai/{slug}"
    
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌊 SkillzWave 提交信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

仓库地址: {repo_url}
标题: {name}
版本: {version}
描述: {desc}

【表单字段】
- GitHub URL: {repo_url}
- Title: {name}
- Description: {desc}
- Category: Tools / Productivity
- Tags: {', '.join(tags) if tags else 'openclaw, skill, agent'}

【提交步骤】
1. 访问 https://skillzwave.ai/submit/
2. 登录 GitHub 账号（OAuth）
3. 填写上述表单字段
4. 提交审核

【CLI 安装（可选）】
npm install -g skilz
skilz install {slug}
"""

def gen_yuanqi(data, slug):
    """生成腾讯元器提交文本"""
    name = data.get('name', slug)
    desc = data.get('description', '')[:200]
    
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟡 腾讯元器 提交信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

技能名称: {name}
描述: {desc}

【提交步骤】
1. 打开 https://yuanqi.tencent.com/market
2. 登录腾讯账号
3. 点击「创建技能」
4. 填写名称和描述
5. 配置技能参数
6. 提交审核
"""

def gen_bailian(data, slug):
    """生成阿里百炼提交文本"""
    name = data.get('name', slug)
    desc = data.get('description', '')[:200]
    
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔵 阿里百炼 提交信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

智能体名称: {name}
描述: {desc}

【提交步骤】
1. 打开 https://bailian.console.aliyun.com
2. 登录阿里云账号
3. 进入「智能体市场」
4. 点击「创建智能体」
5. 填写名称和描述
6. 配置参数并发布
"""

def main():
    if len(sys.argv) < 2:
        slug = input("请输入 Skill slug: ").strip()
    else:
        slug = sys.argv[1]
    
    SKILL_DIR = f"{WORKSPACE}/{slug}"
    if not os.path.exists(SKILL_DIR):
        print(f"❌ Skill 目录不存在: {SKILL_DIR}")
        sys.exit(1)
    
    data = load_skill(slug)
    
    print()
    print("━" * 50)
    print("📋 手动平台提交文本生成器")
    print("━" * 50)
    print(f"\n📦 Skill: {data.get('name', slug)}")
    print()
    
    # COZE
    print(gen_coze(data, slug))
    
    # SkillzWave
    print(gen_skillzwave(data, slug))
    
    # 元器
    print(gen_yuanqi(data, slug))
    
    # 百炼
    print(gen_bailian(data, slug))
    
    # 复制提示
    print("━" * 50)
    print("💡 使用提示:")
    print("  • 上述文本可直接复制到各平台表单")
    print("  • 建议先在各平台创建 Bot/技能，获取实际 URL")
    print("  • 各平台都需要人工审核，请耐心等待")
    print()

if __name__ == '__main__':
    main()
