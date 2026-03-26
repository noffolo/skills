#!/usr/bin/env python3
"""
根据博物馆名称检索在展文物信息。
使用 ProSearch 搜索，大模型提取并整理文物列表。

用法：python3 search_artifacts.py "<museum_name>"
输出：JSON格式的文物列表，供 plan_route.py 使用
"""

import sys
import json
import subprocess
import os
import requests
from pathlib import Path
from typing import Optional, List, Dict, Any

SEARCH_QUERIES = [
    "{museum} 镇馆之宝",
    "{museum} 文物 名单",
    "{museum} 在展文物",
    "{museum} 精品文物",
    "{museum} 著名文物",
    "{museum} 必看文物",
    "{museum} 馆藏珍品",
    "{museum} 参观攻略 文物",
]


def load_api_config() -> dict:
    """从环境变量或配置文件加载大模型配置"""
    api_key = os.environ.get("API_KEY", "")
    api_base = os.environ.get("API_BASE", "")
    model_name = os.environ.get("MODEL_NAME", "")

    if api_key and api_base and model_name:
        if not api_base.endswith("/chat/completions"):
            api_base = f"{api_base.rstrip('/')}/chat/completions"
        return {
            "api_key": api_key,
            "api_base": api_base,
            "model": model_name,
        }

    config_path = Path(__file__).parent / "config.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        api_base = config.get("api_base", "")
        if api_base and not api_base.endswith("/chat/completions"):
            api_base = f"{api_base.rstrip('/')}/chat/completions"

        return {
            "api_key": config.get("api_key", ""),
            "api_base": api_base,
            "model": config.get("model_name", ""),
        }

    raise ValueError("未配置 API Key，请在环境变量或 scripts/config.json 中配置")


def call_llm_api(prompt: str) -> Dict[str, Any]:
    """调用大模型API"""
    api = load_api_config()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api['api_key']}"
    }

    data = {
        "model": api["model"],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 4000
    }

    try:
        response = requests.post(api["api_base"], headers=headers, json=data, timeout=120)
        response.raise_for_status()
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        else:
            return {"error": "Invalid API response"}
    except Exception as e:
        return {"error": str(e)}


def prosearch(keyword: str, count: int = 10) -> dict:
    """调用天集 ProSearch API 进行搜索"""
    port = os.environ.get("AUTH_GATEWAY_PORT", "19000")
    url = f"http://localhost:{port}/proxy/prosearch/search"
    
    payload = {"keyword": keyword, "cnt": count}
    
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", url, "-H", "Content-Type: application/json", 
             "-d", json.dumps(payload)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout)
        else:
            return {"error": "搜索请求失败", "details": result.stderr}
    except Exception as e:
        return {"error": str(e)}


def extract_artifacts_with_llm(search_results: List[str], museum_name: str) -> List[Dict]:
    """使用大模型从搜索结果中提取文物信息"""
    
    combined_content = "\n\n".join([
        f"--- 搜索结果 {i+1} ---\n{result[:3000]}"
        for i, result in enumerate(search_results)
    ])

    prompt = f"""
你是一位博物馆文物专家。请从以下{museum_name}的搜索结果中提取文物信息。

要求：
1. 提取文物名称、所属展馆、所属时期、文物种类、是否是镇馆之宝、简要描述
2. 时期必须从以下列表中选择：远古时期、夏商西周、春秋战国、秦汉、三国两晋南北朝、隋唐五代、辽宋夏金元、明清
3. 文物种类必须从以下列表中选择：青铜器、陶器、瓷器、漆器、玉器宝石、石器石刻、书画古籍、服饰、砖瓦、钱币、化石、金银器、其他
4. 关注的领域从以下列表中选择：农耕、狩猎、饮食、建筑、人物、武器、文房四宝、牌章证件、货币、书法、绘画、雕像、服装、饰品、仪器、佛教、乐器、纹饰、花瓶、礼制、古生物、新石器、旧石器、陈设品、科技、其他
5. 如果搜索结果中未提及展馆，请使用"待确认"
6. 尽可能多地提取文物（至少20件）

请返回JSON数组格式：
[
    {{
        "name": "文物名称",
        "hall": "展馆名称",
        "period": "时期",
        "type": "文物种类",
        "is_treasure": true/false,
        "description": "简要描述",
        "domains": ["领域1", "领域2"],
        "child_friendly": true/false
    }}
]

搜索结果：
{combined_content}
"""

    try:
        result = call_llm_api(prompt)
        if "error" in result:
            print(f"大模型提取失败: {result['error']}", file=sys.stderr)
            return []
        return result if isinstance(result, list) else []
    except Exception as e:
        print(f"大模型提取异常: {e}", file=sys.stderr)
        return []


def search_artifacts(museum_name: str) -> list:
    """使用天集 ProSearch 搜索文物，大模型提取"""
    search_results = []
    
    for query_template in SEARCH_QUERIES:
        query = query_template.format(museum=museum_name)
        try:
            result = prosearch(query, count=10)
            
            docs = result.get('data', {}).get('docs', [])
            if not docs:
                continue
                
            for item in docs:
                passage = item.get('passage', '')
                if passage:
                    search_results.append(passage)
        except Exception:
            pass
    
    if not search_results:
        return []
    
    artifacts = extract_artifacts_with_llm(search_results, museum_name)
    return artifacts


def get_artifacts(museum_name: str) -> list:
    """获取博物馆文物列表"""
    artifacts = search_artifacts(museum_name)
    return artifacts


def main():
    museum_name = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if not museum_name:
        print(json.dumps({"error": "请提供博物馆名称"}, ensure_ascii=False))
        sys.exit(1)

    artifacts = get_artifacts(museum_name)
    
    print(json.dumps({
        "museum_name": museum_name,
        "artifacts_count": len(artifacts),
        "artifacts": artifacts
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
