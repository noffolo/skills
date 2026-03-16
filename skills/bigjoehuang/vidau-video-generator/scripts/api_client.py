#!/usr/bin/env python3
"""
Vidau API 请求封装：发起 HTTP 请求并将 URL、方法、参数、响应写入日志文件。
日志路径由环境变量 VIDAU_API_LOG 指定，默认当前目录下的 vidau_api.log。
"""
import os
from datetime import datetime
from typing import Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

LOG_PATH = os.environ.get("VIDAU_API_LOG", "vidau_api.log")


class APIError(Exception):
    """HTTP 错误，携带状态码与响应 body，便于调用方打印。"""
    def __init__(self, message: str, status_code: int, body: str = ""):
        super().__init__(message)
        self.code = status_code
        self.body = body


def _write_log(
    method: str,
    url: str,
    params_or_body: Optional[str],
    response_status: Optional[int],
    response_body: str,
    error: Optional[str] = None,
) -> None:
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write("\n" + "=" * 60 + "\n")
            f.write(f"[{datetime.now().isoformat()}] API 请求\n")
            f.write("-" * 40 + "\n")
            f.write(f"URL:    {url}\n")
            f.write(f"方法:   {method}\n")
            f.write(f"参数:   {params_or_body or '(无)'}\n")
            f.write("-" * 40 + "\n")
            f.write(f"响应状态: {response_status}\n")
            if error:
                f.write(f"错误:   {error}\n")
            f.write(f"响应体: {response_body[:2000]}\n")
            if len(response_body) > 2000:
                f.write("...(截断)\n")
            f.write("=" * 60 + "\n")
    except OSError:
        pass


def api_request(
    method: str,
    url: str,
    headers: Optional[dict] = None,
    data: Optional[bytes] = None,
    timeout: float = 30,
) -> Tuple[bytes, int]:
    """
    发起 HTTP 请求，并将请求 URL、方法、参数与响应结果写入日志文件。
    返回 (响应 body 字节, HTTP 状态码)。
    若发生 HTTPError，会先记录日志再抛出；URLError 同理。
    """
    params_str: Optional[str] = None
    if data:
        try:
            params_str = data.decode("utf-8")
        except Exception:
            params_str = "<binary>"

    try:
        req = Request(url, data=data, headers=headers or {}, method=method)
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            status = getattr(resp, "status", 200)
            body_str = raw.decode("utf-8", errors="replace")
            _write_log(method, url, params_str, status, body_str)
            return raw, status
    except HTTPError as e:
        err_body = b""
        try:
            err_body = e.read()
        except Exception:
            pass
        body_str = err_body.decode("utf-8", errors="replace")
        _write_log(method, url, params_str, e.code, body_str, error=str(e.reason))
        raise APIError(str(e.reason), e.code, body_str) from e
    except URLError as e:
        _write_log(method, url, params_str, None, "", error=str(e.reason))
        raise
