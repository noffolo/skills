#!/usr/bin/env python3
"""
根据用户画像与文物列表筛选、排序并输出参观路线。

用法：
  python3 plan_route.py --profile profile.json --artifacts artifacts.json --output route_result.json
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Any

import requests

DYNASTY_ORDER = {
    "远古时期":       1,
    "夏商西周":       2,
    "春秋战国":       3,
    "秦汉":           4,
    "三国两晋南北朝": 5,
    "隋唐五代":       6,
    "辽宋夏金元":     7,
    "明清":           8,
    "现代":           9,
}

TARGET_COUNT = {
    "2-3小时": 30,
    "4-5小时": 50,
}
RETRIEVE_COUNT = {
    "2-3小时": 80,
    "4-5小时": 100,
}

def load_api_config() -> dict:
    api_key = os.environ.get("API_KEY", "")
    api_base = os.environ.get("API_BASE", "")
    model_name = os.environ.get("MODEL_NAME", "")

    if api_key and api_base and model_name:
        if not api_base.endswith("/chat/completions"):
            api_base = f"{api_base.rstrip('/')}/chat/completions"
        return {"api_key": api_key, "api_base": api_base, "model": model_name}

    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
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
    api = load_api_config()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api['api_key']}",
    }
    data = {
        "model": api["model"],
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 1200,
    }
    response = requests.post(api["api_base"], headers=headers, json=data, timeout=40)
    response.raise_for_status()
    result = response.json()

    if "choices" in result and len(result["choices"]) > 0:
        content = result["choices"][0]["message"]["content"]
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)

    return {"error": "Invalid API response"}


def summarize_reasons_with_llm(artifacts: List[dict], profile: dict, max_reason_len: int = 28) -> None:
    """
    为 artifacts 生成简短推荐理由，写入 artifact["recommendation_reason"]。
    若失败则不做覆盖，交由 format_markdown_table 的 fallback 逻辑展示。
    """
    items = []
    for idx, a in enumerate(artifacts, 1):
        desc = (a.get("description") or "").strip()
        if len(desc) > 180:
            desc = desc[:180]
        items.append(
            {
                "idx": idx,
                "name": a.get("name", ""),
                "period": a.get("period", ""),
                "type": a.get("type", ""),
                "domains": a.get("domains", []),
                "is_treasure": bool(a.get("is_treasure")),
                "description": desc,
            }
        )

    user_domains = ", ".join(profile.get("domains", []) or [])
    user_types = ", ".join(profile.get("artifact_types", []) or [])
    user_dynasties = ", ".join(profile.get("dynasties", []) or [])

    prompt = f"""
你是一位博物馆参观路线规划助手。请为每件文物生成一句“推荐理由”，用于表格中。
要求：
1) 每条理由必须基于输入的 description/文物字段总结，不要编造事实。
2) 优先突出：与用户的 domains/artifact_types/dynasties 的匹配；若 is_treasure=true，优先强调“镇馆之宝”。
3) 单条理由长度 <= {max_reason_len} 个汉字左右，不要换行。
4) 输出严格 JSON：{{"reasons": {{}}}}，keys 为文物 idx（字符串），value 为理由字符串。

用户画像：
- domains: {user_domains}
- artifact_types: {user_types}
- dynasties: {user_dynasties}

文物列表：
{json.dumps(items, ensure_ascii=False)}
"""

    try:
        resp = call_llm_api(prompt)
        reasons = (resp or {}).get("reasons") or {}
        for idx, a in enumerate(artifacts, 1):
            r = reasons.get(str(idx)) or reasons.get(idx)
            if isinstance(r, str) and r.strip():
                a["recommendation_reason"] = r.strip()
    except Exception:
        return

def normalize_profile(profile: dict) -> dict:
    """统一字段名，兼容不同来源的数据"""
    normalized = dict(profile)
    
    if "visit_time" in profile and "duration" not in profile:
        normalized["duration"] = profile["visit_time"]
    if "fields" in profile and "domains" not in profile:
        normalized["domains"] = profile["fields"]
    
    return normalized


def score_artifact(artifact: dict, profile: dict) -> float:
    """计算文物与用户画像的匹配分数（0-100）。"""
    score = 0.0

    if profile.get("dynasties"):
        if artifact.get("period") in profile["dynasties"]:
            score += 25
        else:
            for d in profile["dynasties"]:
                if d in artifact.get("period", ""):
                    score += 15
                    break

    if profile.get("artifact_types"):
        if artifact.get("type") in profile["artifact_types"]:
            score += 35
        else:
            for at in profile["artifact_types"]:
                if at in artifact.get("type", ""):
                    score += 20
                    break

    if profile.get("domains"):
        artifact_domains = artifact.get("domains", [])
        matched = len(set(artifact_domains) & set(profile["domains"]))
        if matched > 0:
            score += min(30, matched * 15)

    if artifact.get("is_treasure"):
        score += 10 if profile.get("first_visit") else 2

    if profile.get("with_children") and artifact.get("child_friendly"):
        score += 5

    return score


def get_period_order(artifact: dict) -> int:
    """获取文物时期的排序序号，未知时期排最后。"""
    period = artifact.get("period", "")
    for dynasty, order in DYNASTY_ORDER.items():
        if dynasty in period:
            return order
    return 99


def select_and_sort(artifacts: List[dict], profile: dict) -> List[dict]:
    """筛选文物并排序。"""
    target = TARGET_COUNT.get(profile.get("duration", "2-3小时"), 30)
    retrieve_target = RETRIEVE_COUNT.get(profile.get("duration", "2-3小时"), 80)

    if len(artifacts) < retrieve_target:
        print(f"提示：共检索到 {len(artifacts)} 件文物")

    for a in artifacts:
        a["relevance_score"] = score_artifact(a, profile)
        a["_period_order"] = get_period_order(a)

    sorted_by_score = sorted(artifacts, key=lambda x: -x["relevance_score"])

    selected = []
    dynasty_counts: Dict[int, int] = {}
    max_per_dynasty = max(3, target // len(DYNASTY_ORDER))

    for a in sorted_by_score:
        order = a["_period_order"]
        if dynasty_counts.get(order, 0) < max_per_dynasty:
            selected.append(a)
            dynasty_counts[order] = dynasty_counts.get(order, 0) + 1
        if len(selected) >= target:
            break

    if len(selected) < target:
        for a in sorted_by_score:
            if a not in selected:
                selected.append(a)
            if len(selected) >= target:
                break

    selected.sort(key=lambda x: x["_period_order"])

    return selected[:target]


def format_markdown_table(artifacts: List[dict]) -> str:
    """输出 Markdown 表格。"""
    valid_halls = sum(1 for a in artifacts if a.get("hall") and a.get("hall") != "待确认")
    show_hall = valid_halls > len(artifacts) * 0.3

    def fallback_reason(text: str, max_len: int = 28) -> str:
        if not text:
            return ""
        text = str(text).strip().replace("\n", " ")
        for sep in ["。", "！", "？", ",", "，"]:
            if sep in text:
                text = text.split(sep, 1)[0]
                break
        if len(text) > max_len:
            text = text[:max_len]
        return text
    
    if show_hall:
        lines = [
            "| 序号 | 文物名称 | 展馆 | 时期 | 推荐理由 |",
            "|---|---------|------|------|---------|",
        ]
        for i, a in enumerate(artifacts, 1):
            name = a.get("name", "")
            hall = a.get("hall", "")
            period = a.get("period", "")
            reason = a.get("recommendation_reason") or fallback_reason(a.get("description", ""), 28)
            treasure_mark = " ⭐" if a.get("is_treasure") else ""
            lines.append(f"| {i} | {name}{treasure_mark} | {hall} | {period} | {reason} |")
    else:
        lines = [
            "| 序号 | 文物名称 | 时期 | 推荐理由 |",
            "|---|---------|------|---------|",
        ]
        for i, a in enumerate(artifacts, 1):
            name = a.get("name", "")
            period = a.get("period", "")
            reason = a.get("recommendation_reason") or fallback_reason(a.get("description", ""), 28)
            treasure_mark = " ⭐" if a.get("is_treasure") else ""
            lines.append(f"| {i} | {name}{treasure_mark} | {period} | {reason} |")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="博物馆参观路线规划器")
    parser.add_argument("--profile", required=True, help="用户画像 JSON 文件路径")
    parser.add_argument("--artifacts", required=True, help="文物列表 JSON 文件路径")
    parser.add_argument("--output", default="route_result.json", help="输出 JSON 文件路径")
    args = parser.parse_args()

    with open(args.profile, encoding="utf-8") as f:
        profile = json.load(f)
    profile = normalize_profile(profile)
    
    with open(args.artifacts, encoding="utf-8") as f:
        artifacts_data = json.load(f)
    
    if isinstance(artifacts_data, dict):
        artifacts = artifacts_data.get("artifacts") or []
        if not artifacts and "museum_name" not in artifacts_data:
            artifacts = list(artifacts_data.values())[0] if artifacts_data else []
    else:
        artifacts = artifacts_data

    selected = select_and_sort(artifacts, profile)
    summarize_reasons_with_llm(selected, profile)

    print(f"\n## 🗺️ {profile.get('museum_name', '博物馆')} 参观路线规划\n")
    print(f"**参观时长：** {profile.get('duration')}  |  "
          f"**推荐文物数：** {len(selected)} 件  |  "
          f"**首次参观：** {'是' if profile.get('first_visit') else '否'}  |  "
          f"**携带儿童：** {'是' if profile.get('with_children') else '否'}\n")
    print(format_markdown_table(selected))

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump({
            "profile": profile,
            "selected_count": len(selected),
            "artifacts": selected
        }, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存至 {args.output}")


if __name__ == "__main__":
    main()
