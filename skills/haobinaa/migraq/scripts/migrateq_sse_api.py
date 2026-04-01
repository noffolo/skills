#!/usr/bin/env python3
"""
MigraQ Gateway MigraQChatCompletions SSE 流式调用脚本

通过腾讯云 AK/SK 鉴权调用 MigraQ Gateway 的 MigraQChatCompletions 接口。
鉴权方式：SecretId 通过 X-TC-SecretId header 传递，SecretKey 通过 Authorization: Bearer header 传递。
如果未配置 AK/SK，则走 Mock 模式（无鉴权头，仅用于测试）。

接口固定参数：
    host:    https://msp.cloud.tencent.com（内置默认，可通过 CMG_GATEWAY_URL 环境变量覆盖）
    path:    /proxy/chat
    action:  MigraQChatCompletions

    请求格式：
    {"model": "openclaw", "input": "...", "stream": true, "SessionID": "<uuid>"}

响应格式（SSE，标准 OpenAI Responses API 格式）：
    event: response.output_text.delta
    data: {"type":"response.output_text.delta","delta":"...", ...}

    event: response.completed
    data: {"type":"response.completed","response":{"id":"resp_...","output":[...],"usage":{...}}}

    data: [DONE]

Session 管理：
    Gateway 按 API Key 服务端自动维护会话上下文，支持多轮对话。
    session_id 由调用方生成（UUID v4），用于调用方追踪同一对话。
    用户要开启新对话时调用 clear_session() 清除服务端上下文。

纯 Python 标准库实现，无外部依赖，支持 Windows / Linux / macOS。

用法 (命令行):
    python3 migrateq_sse_api.py <question> [session_id]
    python3 migrateq_sse_api.py --clear-session

示例:
    python3 migrateq_sse_api.py '阿里云50台ECS如何迁移到腾讯云？'
    python3 migrateq_sse_api.py '详细说说 go2tencentcloud 步骤' '550e8400-e29b-41d4-a716-446655440000'

作为模块导入:
    from migrateq_sse_api import call_sse_api, generate_session_id
    session_id = generate_session_id()
    result = call_sse_api(question="如何评估迁移成本？", session_id=session_id)

环境变量（可选）:
    CMG_GATEWAY_URL            - 覆盖内置 Gateway 地址（可选，默认 https://msp.cloud.tencent.com）
    TENCENTCLOUD_SECRET_ID     - 腾讯云 SecretId（可选，不填则走 Mock 模式）
    TENCENTCLOUD_SECRET_KEY    - 腾讯云 SecretKey，通过 Authorization: Bearer header 鉴权（可选，不填则走 Mock 模式）

输出格式（统一 JSON）:
    成功: {"success": true, "action": "MigraQChatCompletions", "data": {"content": "...", "is_final": true, "session_id": "..."}, "requestId": "..."}
    失败: {"success": false, "action": "MigraQChatCompletions", "error": {"code": "...", "message": "..."}, "requestId": ""}
"""

import hashlib
import json
import os
import ssl
import sys
import time
import uuid
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ---------------------------------------------------------------------------
# 固定参数
# ---------------------------------------------------------------------------
ACTION = "MigraQChatCompletions"
_PATH = "/proxy/chat"


# ---------------------------------------------------------------------------
# 会话管理
# ---------------------------------------------------------------------------

def generate_session_id() -> str:
    """
    生成新的 SessionID（UUID v4）。

    SessionID 用于控制多轮对话上下文：
    - 同一对话的所有轮次必须使用同一个 SessionID
    - 用户开启新对话时调用本函数生成新的 SessionID

    Returns:
        str: UUID v4 格式的 SessionID
    """
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# 内部工具函数
# ---------------------------------------------------------------------------

def _get_ssl_context():
    """获取 SSL 上下文，始终启用证书验证"""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def _make_error(code: str, message: str, request_id: str = "") -> dict:
    """构造统一错误结果"""
    return {
        "success": False,
        "action": ACTION,
        "error": {"code": code, "message": message},
        "requestId": request_id,
    }


def _make_success(data: dict, request_id: str = "") -> dict:
    """构造统一成功结果"""
    return {
        "success": True,
        "action": ACTION,
        "data": data,
        "requestId": request_id,
    }


def _resolve_credentials(secret_id: str = None, secret_key: str = None):
    """
    读取 AK/SK 凭证（优先参数，其次环境变量）。

    鉴权设计：
      - TENCENTCLOUD_SECRET_KEY 作为 Bearer Token 传给 Gateway
      - 与 CloudQ 使用同一套 AK/SK 环境变量，用户只需配置一次
      - 未配置时走 Mock 模式（无 Authorization 头）

    Returns:
        (secret_id, secret_key): 均可为空字符串（Mock 模式）
    """
    secret_id = secret_id or os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = secret_key or os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    return secret_id, secret_key


# ---------------------------------------------------------------------------
# SSE 行解析
# ---------------------------------------------------------------------------

def parse_sse_line(line: str):
    """
    解析单行 SSE 数据。

    Returns:
        dict | None:
            - id 行:               {"type": "id", "value": "..."}
            - event 行:            {"event": "<value>"}
            - data 行(JSON 有效):  {"event": "data", "data": {...}}
            - data 行(JSON 无效):  {"event": "data", "raw": "..."}
            - 空行/注释行:          None
    """
    if not line or line.startswith(":"):
        return None

    if line.startswith("id:"):
        return {"type": "id", "value": line[3:].strip()}

    if line.startswith("data:"):
        payload = line[5:].lstrip()
        try:
            return {"event": "data", "data": json.loads(payload)}
        except (json.JSONDecodeError, ValueError):
            return {"event": "data", "raw": payload}

    if line.startswith("event:"):
        return {"event": line[6:].strip()}

    return None


# ---------------------------------------------------------------------------
# SSE 流式 API 调用
# ---------------------------------------------------------------------------

def call_sse_api(question: str, session_id: str,
                 gateway_url: str = None,
                 secret_id: str = None, secret_key: str = None,
                 on_delta=None, timeout: int = 600) -> dict:
    """
    调用 MigraQChatCompletions SSE 流式 API。

    Args:
        question:    用户问题（必填）
        session_id:  会话 ID（同一对话必须保持不变）
        gateway_url: Gateway 地址，不传则使用内置默认地址（可通过 CMG_GATEWAY_URL 环境变量覆盖）
        secret_id:   腾讯云 SecretId，不传则从环境变量读取
        secret_key:  腾讯云 SecretKey（作为 Bearer Token），不传则从环境变量读取
        on_delta:    回调函数，每收到一段流式文本时调用，参数为 str
        timeout:     请求超时秒数，默认 120

    Returns:
        dict: 统一格式的结果字典
    """
    gateway_url = (gateway_url or os.environ.get("CMG_GATEWAY_URL", "https://msp.cloud.tencent.com")).rstrip("/")
    secret_id, secret_key = _resolve_credentials(secret_id, secret_key)

    payload = {
        "model": "openclaw",
        "input": question,
        "stream": True,
        "SessionID": session_id,
    }
    payload_str = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "X-TC-Action": ACTION,
    }
    # 凭证统一通过 Authorization header 传递
    if secret_id:
        headers["X-TC-SecretId"] = secret_id
    if secret_key:
        headers["Authorization"] = f"Bearer {secret_key}"

    req = Request(
        f"{gateway_url}{_PATH}",
        data=payload_str.encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        ctx = _get_ssl_context()
        resp = urlopen(req, context=ctx, timeout=timeout)
    except HTTPError as e:
        try:
            body = e.read().decode("utf-8")
            data = json.loads(body)
            msg = data.get("message") or data.get("error") or f"HTTP {e.code}"
        except Exception:
            msg = f"HTTP {e.code}: {e.reason}"
        return _make_error("HTTPError", f"MigraQ Gateway 返回错误: {msg}")
    except URLError as e:
        return _make_error(
            "NetworkError",
            f"无法连接 MigraQ Gateway ({gateway_url}): {e.reason}"
        )
    except Exception as e:
        return _make_error("NetworkError", f"请求异常: {e}")

    return _parse_sse_stream(resp, session_id, on_delta)


def clear_session(gateway_url: str = None,
                  secret_id: str = None, secret_key: str = None) -> dict:
    """
    清除当前会话上下文（DELETE /proxy/session）。

    Args:
        gateway_url: Gateway 地址，不传则使用内置默认地址（可通过 CMG_GATEWAY_URL 环境变量覆盖）
        secret_id:   腾讯云 SecretId（当前未使用，保留接口一致性）
        secret_key:  腾讯云 SecretKey（作为 Bearer Token）

    Returns:
        dict: 统一格式的结果字典
    """
    gateway_url = (gateway_url or os.environ.get("CMG_GATEWAY_URL", "https://msp.cloud.tencent.com")).rstrip("/")
    secret_id, secret_key = _resolve_credentials(secret_id, secret_key)

    headers = {}
    if secret_key:
        headers["Authorization"] = f"Bearer {secret_key}"

    req = Request(
        f"{gateway_url}/proxy/session",
        headers=headers,
        method="DELETE",
    )

    try:
        ctx = _get_ssl_context()
        with urlopen(req, context=ctx, timeout=600) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body) if body.strip() else {}
            return _make_success(data)
    except HTTPError as e:
        return _make_error("HTTPError", f"清除会话失败: HTTP {e.code} {e.reason}")
    except URLError as e:
        return _make_error("NetworkError", f"无法连接 Gateway: {e.reason}")
    except Exception as e:
        return _make_error("NetworkError", f"请求异常: {e}")


def _parse_sse_stream(resp, session_id: str, on_delta) -> dict:
    """
    解析 MigraQChatCompletions SSE 流并构建结果。

    Gateway 使用标准 OpenAI Responses API SSE 格式：
        event: response.output_text.delta
        data: {"type":"response.output_text.delta","delta":"...", ...}

        event: response.completed
        data: {"type":"response.completed","response":{"id":"resp_...","output":[...],"usage":{...}}}

        data: [DONE]

    注：session 由 Gateway 按 API Key 服务端维护，响应中不返回 session_id。
    """
    content_parts = []
    request_id = ""
    usage = {}

    for raw_line in resp:
        line = raw_line.decode("utf-8").rstrip("\r\n")

        # 结束标记
        if line == "data: [DONE]":
            break

        parsed = parse_sse_line(line)
        if parsed is None:
            continue
        if parsed.get("event") != "data":
            continue

        data = parsed.get("data")
        if not isinstance(data, dict):
            continue

        event_type = data.get("type", "")

        # 流式文本增量
        if event_type == "response.output_text.delta":
            delta = data.get("delta", "")
            if delta:
                content_parts.append(delta)
                if on_delta:
                    on_delta(delta)

        # 完成事件：提取 request_id 和 usage
        elif event_type == "response.completed":
            response = data.get("response", {})
            request_id = response.get("id", "")
            usage = response.get("usage", {})
            break

    return _make_success(
        {
            "content": "".join(content_parts),
            "is_final": True,
            "session_id": session_id,  # 透传调用方传入的 session_id
            "usage": usage,
        },
        request_id,
    )


# ---------------------------------------------------------------------------
# 命令行入口
# ---------------------------------------------------------------------------

def _output_json(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False)


def main():
    """命令行入口：python3 migrateq_sse_api.py <question> [session_id]"""
    args = sys.argv[1:]

    # --clear-session 模式
    if args and args[0] == "--clear-session":
        result = clear_session()
        print(_output_json(result))
        sys.exit(0 if result.get("success") else 1)

    if len(args) < 1:
        print(_output_json(_make_error(
            "MissingParameter",
            "用法: python3 migrateq_sse_api.py <question> [session_id]\n"
            "     python3 migrateq_sse_api.py --clear-session"
        )))
        sys.exit(1)

    question = args[0]
    session_id = args[1] if len(args) > 1 else generate_session_id()

    def on_delta(delta: str):
        print(delta, end="", flush=True)

    result = call_sse_api(question=question, session_id=session_id, on_delta=on_delta)

    # 流式输出结束后换行，再打印统一 JSON 结果
    print()
    print(_output_json(result))

    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
