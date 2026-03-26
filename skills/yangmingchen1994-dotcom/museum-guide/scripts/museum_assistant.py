#!/usr/bin/env python3
"""museum_assistant.py
入口脚本：串联画像提取 -> 文物检索 -> 路线规划。
默认不依赖中间落地文件。需要确认时输出确认 JSON。
"""

import argparse
import json
import sys
from typing import Any, Dict


def _load_extract_module():
    from pathlib import Path

    script_dir = Path(__file__).resolve().parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

    import extract_profile as ep

    return ep


def _load_plan_module():
    from pathlib import Path

    script_dir = Path(__file__).resolve().parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

    import plan_route as pr

    return pr


def _load_search_module():
    from pathlib import Path

    script_dir = Path(__file__).resolve().parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

    import search_artifacts as sa

    return sa


def extract_and_maybe_confirm(user_input: str, accept_inferred: bool) -> Dict[str, Any]:
    """
    返回：
    - confirmation_needed: bool
    - confirmation_prompt: str（当需要确认时）
    - profile: dict
    """
    ep = _load_extract_module()

    llm_profile = ep.extract_profile(user_input)
    if not llm_profile:
        return {"error": "画像提取失败，请检查 API 配置与网络连接"}

    inferred_fields = []
    missing_duration = not llm_profile.get("duration")
    missing_first_visit = llm_profile.get("first_visit") is None
    missing_with_children = llm_profile.get("with_children") is None
    missing_domains = not llm_profile.get("domains")
    missing_artifact_types = not llm_profile.get("artifact_types")
    missing_dynasties = not llm_profile.get("dynasties")
    missing_museum_name = not llm_profile.get("museum_name")

    if missing_museum_name:
        inferred_fields.append("museum_name")
    if missing_duration:
        inferred_fields.append("duration")
    if missing_first_visit:
        inferred_fields.append("first_visit")
    if missing_with_children:
        inferred_fields.append("with_children")
    if missing_domains:
        inferred_fields.append("domains")
    if missing_artifact_types:
        inferred_fields.append("artifact_types")
    if missing_dynasties:
        inferred_fields.append("dynasties")

    profile = llm_profile

    if missing_duration:
        profile["duration"] = ep.DEFAULT_DURATION
    if missing_with_children:
        profile["with_children"] = ep.DEFAULT_WITH_CHILDREN
    if missing_domains:
        profile["domains"] = list(ep.DEFAULT_DOMAINS_DOC)
    if missing_dynasties:
        profile["dynasties"] = list(ep.DEFAULT_DYNASTIES_DOC)

    profile = ep.normalize_profile_for_scoring(profile)

    confirmation_needed = len(inferred_fields) > 0
    if confirmation_needed and not accept_inferred:
        return {
            "profile": profile,
            "has_unfilled_mandatory": not profile.get("museum_name"),
            "confirmation_needed": True,
            "confirmation_prompt": ep.build_confirmation_prompt(profile),
        }

    return {
        "profile": profile,
        "has_unfilled_mandatory": not profile.get("museum_name"),
        "confirmation_needed": False,
        "confirmation_prompt": "",
    }


def plan_route_inline(profile: Dict[str, Any], artifacts: list) -> Dict[str, Any]:
    pr = _load_plan_module()

    normalized_profile = pr.normalize_profile(profile)
    artifacts_selected = pr.select_and_sort(artifacts, normalized_profile)
    pr.summarize_reasons_with_llm(artifacts_selected, normalized_profile)
    table = pr.format_markdown_table(artifacts_selected)

    museum_name = profile.get("museum_name", "博物馆")
    header = f"\n## 🗺️ {museum_name} 参观路线规划\n"
    meta = (
        f"**参观时长：** {profile.get('duration')}  |  "
        f"**推荐文物数：** {len(artifacts_selected)} 件  |  "
        f"**首次参观：** {'是' if profile.get('first_visit') else '否'}  |  "
        f"**携带儿童：** {'是' if profile.get('with_children') else '否'}\n"
    )

    return {
        "markdown": header + meta + table,
        "selected_count": len(artifacts_selected),
        "selected": artifacts_selected,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="博物馆参观路线规划入口（链式串联三段流程）")
    parser.add_argument("user_input", nargs="+", help="用户输入文本，例如：帮我规划一下去故宫博物院的参观路线")
    parser.add_argument(
        "--accept-inferred",
        action="store_true",
        help="当画像提取存在推断字段时，直接接受并继续：完成检索与路线规划",
    )
    args = parser.parse_args()

    user_input = " ".join(args.user_input).strip()
    if not user_input:
        print(json.dumps({"error": "请提供用户输入文本"}, ensure_ascii=False))
        sys.exit(1)

    step1 = extract_and_maybe_confirm(user_input, accept_inferred=args.accept_inferred)
    if "error" in step1:
        print(json.dumps(step1, ensure_ascii=False))
        sys.exit(1)

    if step1.get("confirmation_needed"):
        print(json.dumps(step1, ensure_ascii=False, indent=2))
        return

    profile = step1["profile"]
    museum_name = profile.get("museum_name")
    if not museum_name:
        print(json.dumps({"error": "缺少博物馆名称，无法继续。请补充后重试。", "profile": profile}, ensure_ascii=False))
        sys.exit(2)

    sa = _load_search_module()
    artifacts = sa.get_artifacts(museum_name)

    if not artifacts:
        print(json.dumps({"error": f"无法检索到{museum_name}的文物信息，请检查网络连接或尝试其他博物馆。", "profile": profile}, ensure_ascii=False))
        sys.exit(3)

    result = plan_route_inline(profile, artifacts)
    print(result["markdown"])


if __name__ == "__main__":
    main()

