#!/usr/bin/env python3
"""
llm-cost / 用户使用明细

用途：调用 GET /open-api/llm-cost/user-usage，查询当前用户或指定 personId 的 AI 费用明细。

使用方式：
  python3 scripts/llm-cost/user-usage.py
  python3 scripts/llm-cost/user-usage.py --format markdown
  python3 scripts/llm-cost/user-usage.py --start-time 2026-04-01 --end-time 2026-04-02
  python3 scripts/llm-cost/user-usage.py --person-id 20001

环境变量：
  XG_BIZ_API_KEY 或 XG_APP_KEY — appKey（鉴权类型 appKey）
  以上建议按 cms-auth-skills/SKILL.md 预先准备
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://sg-al-cwork-web.mediportal.com.cn/open-api/llm-cost/user-usage"
AUTH_MODE = "appKey"
MAX_RETRIES = 3
RETRY_DELAY_SEC = 1.0


def format_token_display(value: int | float) -> str:
    """Token 等大额计数：≥1M 用 M，≥1K 用 K；否则千分位。"""
    if isinstance(value, bool):
        return str(value)
    try:
        n = float(value)
    except (TypeError, ValueError):
        return str(value)
    if n != n:  # NaN
        return ""
    sign = "-" if n < 0 else ""
    n = abs(n)
    if n >= 1_000_000:
        v = n / 1_000_000
        s = f"{v:.2f}".rstrip("0").rstrip(".")
        return f"{sign}{s}M"
    if n >= 1_000:
        v = n / 1_000
        s = f"{v:.2f}".rstrip("0").rstrip(".")
        return f"{sign}{s}K"
    iv = int(n)
    if iv == n:
        return f"{sign}{iv:,}"
    s = f"{n:.2f}".rstrip("0").rstrip(".")
    return f"{sign}{s}"


def _is_token_count_key(key: str) -> bool:
    return "token" in key.lower()


def _md_cell(value: object) -> str:
    if value is None:
        return ""
    text = str(value).replace("|", "\\|").replace("\n", " ")
    return text


def _token_in_display(d: dict) -> str:
    v = d.get("inputTokensDisplay")
    if v is not None and str(v).strip() != "":
        return str(v)
    raw = d.get("inputTokens")
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        return format_token_display(raw)
    return _md_cell(raw)


def _token_out_display(d: dict) -> str:
    v = d.get("outputTokensDisplay")
    if v is not None and str(v).strip() != "":
        return str(v)
    raw = d.get("outputTokens")
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        return format_token_display(raw)
    return _md_cell(raw)


def build_markdown_tables(data: dict) -> str:
    """将 user-usage 的 data 转为 Markdown 表格（总览 → 各产品小计 → 各模型明细）。"""
    lines: list[str] = []
    q = data.get("query")
    if isinstance(q, dict) and q:
        lines.append("## 查询条件\n")
        lines.append("| 字段 | 值 |")
        lines.append("| --- | --- |")
        for key, val in q.items():
            if str(key).endswith("Display"):
                continue
            lines.append(f"| {_md_cell(key)} | {_md_cell(val)} |")
        lines.append("")

    s = data.get("summary")
    if isinstance(s, dict) and s:
        lines.append("## 用户总览\n")
        lines.append("| 指标 | 数值 |")
        lines.append("| --- | --- |")
        if s.get("personName") is not None:
            lines.append(f"| 用户 | {_md_cell(s.get('personName'))} |")
        lines.append(f"| 输入 Token | {_md_cell(_token_in_display(s))} |")
        lines.append(f"| 输出 Token | {_md_cell(_token_out_display(s))} |")
        if "callCount" in s:
            lines.append(f"| 调用次数 | {_md_cell(s.get('callCount'))} |")
        if "cost" in s:
            cur = s.get("currency") or ""
            label = f"费用 ({cur})" if cur else "费用"
            lines.append(f"| {label} | {_md_cell(s.get('cost'))} |")
        lines.append("")

    products = data.get("products")
    if not isinstance(products, list) or not products:
        return "\n".join(lines).rstrip() + "\n"

    for idx, p in enumerate(products, start=1):
        if not isinstance(p, dict):
            continue
        pname = p.get("productName") or p.get("productId") or f"产品{idx}"
        pid = p.get("productId")
        title = f"## 产品 {idx}：{_md_cell(pname)}"
        if pid is not None:
            title += f"（`{_md_cell(pid)}`）"
        lines.append(title + "\n")
        lines.append("### 产品小计\n")
        lines.append("| 指标 | 数值 |")
        lines.append("| --- | --- |")
        lines.append(f"| 输入 Token | {_md_cell(_token_in_display(p))} |")
        lines.append(f"| 输出 Token | {_md_cell(_token_out_display(p))} |")
        if "callCount" in p:
            lines.append(f"| 调用次数 | {_md_cell(p.get('callCount'))} |")
        if "cost" in p:
            cur = p.get("currency") or ""
            label = f"费用 ({cur})" if cur else "费用"
            lines.append(f"| {label} | {_md_cell(p.get('cost'))} |")
        lines.append("")

        models = p.get("models")
        if not isinstance(models, list) or not models:
            lines.append("")
            continue
        lines.append("### 模型明细\n")
        lines.append(
            "| 模型 | 输入 Token | 输出 Token | 调用 | 费用 |"
        )
        lines.append("| --- | --- | --- | --- | --- |")
        for m in models:
            if not isinstance(m, dict):
                continue
            mname = (
                m.get("modelName")
                or m.get("name")
                or m.get("modelCode")
                or m.get("modelId")
                or "—"
            )
            row_cost = ""
            if "cost" in m:
                row_cost = str(m.get("cost"))
            elif "totalCost" in m:
                row_cost = str(m.get("totalCost"))
            cc = m.get("callCount", "")
            lines.append(
                "| "
                + _md_cell(mname)
                + " | "
                + _md_cell(_token_in_display(m))
                + " | "
                + _md_cell(_token_out_display(m))
                + " | "
                + _md_cell(cc)
                + " | "
                + _md_cell(row_cost)
                + " |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def enrich_token_display_fields(obj: object) -> object:
    """为含 token 的数值字段追加同名 `*Display` 字符串（K/M），便于 Agent 直接展示。"""
    if isinstance(obj, dict):
        out: dict[str, object] = {}
        for k, v in obj.items():
            out[k] = enrich_token_display_fields(v)
            if (
                _is_token_count_key(k)
                and isinstance(v, (int, float))
                and not isinstance(v, bool)
                and v == v
            ):
                out[f"{k}Display"] = format_token_display(v)
        return out
    if isinstance(obj, list):
        return [enrich_token_display_fields(x) for x in obj]
    return obj


def build_headers() -> dict:
    headers = {"Accept": "application/json"}
    if AUTH_MODE == "appKey":
        app_key = os.environ.get("XG_BIZ_API_KEY") or os.environ.get("XG_APP_KEY")
        if not app_key:
            print("错误: 请设置环境变量 XG_BIZ_API_KEY 或 XG_APP_KEY", file=sys.stderr)
            sys.exit(1)
        headers["appKey"] = app_key
    return headers


def _should_retry(exc: BaseException) -> bool:
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code >= 500
    if isinstance(exc, urllib.error.URLError):
        return True
    return False


def call_api(
    person_id: int | None,
    start_time: str | None,
    end_time: str | None,
    timeout: int = 60,
) -> dict:
    params: dict[str, str] = {}
    if person_id is not None:
        params["personId"] = str(person_id)
    if start_time:
        params["startTime"] = start_time
    if end_time:
        params["endTime"] = end_time
    query = urllib.parse.urlencode(params) if params else ""
    url = API_BASE + ("?" + query if query else "")
    headers = build_headers()
    last_error: BaseException | None = None
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError) as e:
            last_error = e
            if attempt < MAX_RETRIES - 1 and _should_retry(e):
                time.sleep(RETRY_DELAY_SEC)
                continue
            raise
    assert last_error is not None
    raise last_error


def main() -> None:
    parser = argparse.ArgumentParser(description="用户使用明细（user-usage）")
    parser.add_argument(
        "--person-id",
        type=int,
        default=None,
        help="用户 personId；不传表示当前登录用户",
    )
    parser.add_argument("--start-time", default=None, help="开始日期 YYYY-MM-DD")
    parser.add_argument("--end-time", default=None, help="结束日期 YYYY-MM-DD")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="json=仅输出 Result JSON；markdown=仅输出 Markdown 表格（便于直接贴给用户）",
    )
    args = parser.parse_args()
    result = call_api(args.person_id, args.start_time, args.end_time)
    if isinstance(result, dict) and result.get("data") is not None:
        result = {
            **result,
            "data": enrich_token_display_fields(result["data"]),
        }
    if args.format == "markdown":
        if not isinstance(result, dict):
            print(json.dumps(result, ensure_ascii=False))
            return
        rc = result.get("resultCode")
        if rc is not None and rc != 1:
            print(json.dumps(result, ensure_ascii=False))
            return
        data = result.get("data")
        if not isinstance(data, dict):
            print(json.dumps(result, ensure_ascii=False))
            return
        print(build_markdown_tables(data), end="")
        return
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
