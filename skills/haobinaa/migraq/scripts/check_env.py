#!/usr/bin/env python3
"""
MigraQ 环境检测脚本（只读，不修改任何配置）

功能：检测 Python 版本、Skill 版本更新（含 changelog）、AK/SK 配置、Gateway 连通性

用法:
    python3 check_env.py                    # 标准模式：输出详细检测结果
    python3 check_env.py --quiet            # 静默模式：仅输出错误信息
    python3 check_env.py --skip-update      # 跳过版本更新检查

返回码:
    0 - 环境就绪（AK/SK + Gateway 全部正常）
    1 - Python 版本不满足（需要 3.7+）
    2 - AK/SK 未配置或鉴权失败
    3 - Gateway 连通性失败

跨平台支持: Windows / Linux / macOS
"""

import json
import os
import platform
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

DEFAULT_GATEWAY_URL = "https://msp.cloud.tencent.com"

# 版本检查配置
META_FILE = SCRIPT_DIR / "_skillhub_meta.json"
VERSION_CHECK_TIMEOUT = 15  # 秒

# ============== 输出控制 ==============
QUIET_MODE = "--quiet" in sys.argv
SKIP_UPDATE = "--skip-update" in sys.argv


def log_info(msg: str):
    if not QUIET_MODE:
        print(msg)


def log_ok(msg: str):
    if not QUIET_MODE:
        print(f"  [OK] {msg}")


def log_warn(msg: str):
    if not QUIET_MODE:
        print(f"  [WARN] {msg}")


def log_fail(msg: str):
    print(f"  [FAIL] {msg}")


def log_section(title: str):
    if not QUIET_MODE:
        print(f"\n=== {title} ===")


# ============== 版本检查 ==============

def parse_version(version_str: str) -> tuple:
    """解析语义化版本号，如 '1.0.0' -> (1, 0, 0)"""
    try:
        parts = version_str.strip().lstrip("v").split(".")
        return tuple(int(p) for p in parts)
    except (ValueError, AttributeError):
        return (0, 0, 0)


def get_local_version():
    """读取本地 _skillhub_meta.json 中的版本号，返回 (name, version_str) 或 (None, None)"""
    if not META_FILE.exists():
        return None, None
    try:
        meta = json.loads(META_FILE.read_text(encoding="utf-8"))
        return meta.get("name"), meta.get("version")
    except (json.JSONDecodeError, IOError):
        return None, None


def get_remote_version(name: str):
    """从 MigraQ Gateway 查询最新 Skill 版本，返回版本字符串或 None"""
    try:
        from urllib.request import urlopen, Request as _Req
        import ssl
        skill_name = urllib.parse.quote(name, safe="")
        api_url = f"{DEFAULT_GATEWAY_URL}/api/v1/skills/{skill_name}/version"
        req = _Req(api_url, headers={"Accept": "application/json"})
        ctx = ssl.create_default_context()
        with urlopen(req, context=ctx, timeout=VERSION_CHECK_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("latestVersion", {}).get("version"), data
    except Exception:
        return None, None


def check_version_update() -> dict:
    """检查本地版本与远端版本是否一致"""
    name, local_ver = get_local_version()
    if not name or not local_ver:
        return {
            "status": "no_meta",
            "message": "未找到 _skillhub_meta.json 或版本信息缺失",
        }

    remote_ver, remote_data = get_remote_version(name)
    if not remote_ver:
        return {
            "status": "check_failed",
            "local_version": local_ver,
            "message": "无法获取远端版本信息（网络问题或接口不可用）",
        }

    local_parsed = parse_version(local_ver)
    remote_parsed = parse_version(remote_ver)

    if remote_parsed <= local_parsed:
        return {
            "status": "up_to_date",
            "local_version": local_ver,
            "remote_version": remote_ver,
            "message": f"当前已是最新版本: {local_ver}",
        }

    # 收集 changelog
    changelog_lines = []
    versions = remote_data.get("versions", []) if remote_data else []
    for v in versions:
        v_str = v.get("version", "")
        v_parsed = parse_version(v_str)
        if v_parsed > local_parsed:
            desc = v.get("changelog") or v.get("description") or ""
            changelog_lines.append(f"  {v_str}: {desc}" if desc else f"  {v_str}")

    if not changelog_lines and remote_data:
        latest_cl = remote_data.get("latestVersion", {}).get("changelog", "")
        if latest_cl:
            changelog_lines.append(f"  {remote_ver}: {latest_cl}")

    return {
        "status": "update_available",
        "local_version": local_ver,
        "remote_version": remote_ver,
        "changelog": changelog_lines,
        "message": f"发现新版本: {local_ver} → {remote_ver}",
    }


# ============== Gateway 连通性检测 ==============

def check_gateway_connectivity(gateway_url: str, secret_key: str) -> dict:
    """
    验证 Gateway 连通性：发送一次非流式 echo 请求，检测响应。

    Returns:
        {"ok": bool, "code": str, "message": str}
    """
    from urllib.request import urlopen, Request as _Req
    from urllib.error import URLError, HTTPError
    import ssl

    path = "/proxy/chat"
    payload = json.dumps({
        "model": "openclaw",
        "input": "ping",
        "stream": False,
    }, separators=(",", ":")).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "X-TC-Action": "MigraQChatCompletions",
    }
    if secret_key:
        headers["Authorization"] = f"Bearer {secret_key}"

    req = _Req(f"{gateway_url}/proxy/chat", data=payload, headers=headers, method="POST")

    try:
        ctx = ssl.create_default_context()
        with urlopen(req, context=ctx, timeout=20) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body) if body.strip() else {}
            # 成功响应包含 id 或 status 字段
            if data.get("id") or data.get("status"):
                return {"ok": True, "code": "OK", "message": "Gateway 连通正常"}
            return {"ok": True, "code": "OK", "message": "Gateway 返回响应"}
    except HTTPError as e:
        try:
            body = e.read().decode("utf-8")
            data = json.loads(body)
            msg = data.get("message") or f"HTTP {e.code}"
        except Exception:
            msg = f"HTTP {e.code}: {e.reason}"
        if e.code in (401, 403):
            return {"ok": False, "code": "AuthError", "message": f"鉴权失败: {msg}"}
        return {"ok": False, "code": "HTTPError", "message": msg}
    except URLError as e:
        return {"ok": False, "code": "NetworkError", "message": f"无法连接 Gateway: {e.reason}"}
    except Exception as e:
        return {"ok": False, "code": "NetworkError", "message": f"连接异常: {e}"}


# ============== 主流程 ==============

def main():
    # ============== 1. 检查 Python 版本 ==============
    log_section("1. 检查运行环境")

    py_ver = sys.version_info
    if py_ver < (3, 7):
        log_fail(f"Python 版本过低: {sys.version}，需要 Python 3.7+")
        sys.exit(1)

    log_ok(f"Python {py_ver.major}.{py_ver.minor}.{py_ver.micro} ({platform.system()} {platform.machine()})")

    # ============== 2. 检查 Skill 版本更新 ==============
    log_section("2. 检查 Skill 版本")

    if SKIP_UPDATE:
        log_ok("已跳过版本更新检查（--skip-update）")
    else:
        ver_result = check_version_update()
        status = ver_result["status"]

        if status == "up_to_date":
            log_ok(ver_result["message"])
        elif status == "update_available":
            log_warn(ver_result["message"])
            log_info(f"  当前版本: {ver_result['local_version']}")
            log_info(f"  最新版本: {ver_result['remote_version']}")
            changelog = ver_result.get("changelog", [])
            if changelog:
                log_info("")
                log_info("  === Changelog ===")
                for line in changelog:
                    log_info(line)
            log_info("")
            log_info("  当前版本仍可正常使用，建议有空时更新。")
        elif status in ("check_failed", "no_meta"):
            log_warn(ver_result["message"])
            log_info("  版本检查跳过，继续后续检测...")

    # ============== 3. 检查 AK/SK 配置 ==============
    log_section("3. 检查 AK/SK 配置")

    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")

    if not secret_id or not secret_key:
        missing = []
        if not secret_id:
            missing.append("TENCENTCLOUD_SECRET_ID")
        if not secret_key:
            missing.append("TENCENTCLOUD_SECRET_KEY")
        log_fail(f"未配置以下环境变量: {', '.join(missing)}")
        log_info("")
        log_info("  请将腾讯云 API 密钥永久写入 shell 配置文件：")
        log_info("")
        log_info("  Linux / macOS（写入 ~/.bashrc 或 ~/.zshrc）:")
        log_info('    echo \'export TENCENTCLOUD_SECRET_ID="your-secret-id"\' >> ~/.zshrc')
        log_info('    echo \'export TENCENTCLOUD_SECRET_KEY="your-secret-key"\' >> ~/.zshrc')
        log_info("    source ~/.zshrc")
        log_info("")
        log_info("  Windows PowerShell（写入用户级环境变量）:")
        log_info('    [Environment]::SetEnvironmentVariable("TENCENTCLOUD_SECRET_ID", "your-secret-id", "User")')
        log_info('    [Environment]::SetEnvironmentVariable("TENCENTCLOUD_SECRET_KEY", "your-secret-key", "User")')
        log_info("")
        log_info("  密钥获取地址: https://console.cloud.tencent.com/cam/capi")
        sys.exit(2)

    masked_id = f"{secret_id[:4]}****{secret_id[-4:]}" if len(secret_id) > 8 else "****"
    log_ok(f"TENCENTCLOUD_SECRET_ID 已配置: {masked_id}")
    log_ok("TENCENTCLOUD_SECRET_KEY 已配置: ****")

    # ============== 4. 验证 Gateway 连通性 ==============
    log_section("4. 验证 Gateway 连通性")

    gateway_url = os.environ.get("CMG_GATEWAY_URL", DEFAULT_GATEWAY_URL).rstrip("/")
    log_ok(f"Gateway: {gateway_url}")

    conn_result = check_gateway_connectivity(gateway_url, secret_key)

    if conn_result["ok"]:
        log_ok(conn_result["message"])
    else:
        code = conn_result["code"]
        msg = conn_result["message"]
        if code == "AuthError":
            log_fail(f"鉴权失败: {msg}")
            log_info("  请检查 TENCENTCLOUD_SECRET_KEY 是否正确")
            sys.exit(2)
        else:
            log_fail(f"Gateway 连通性失败: {msg}")
            log_info(f"  请检查网络是否可达 ({gateway_url})")
            sys.exit(3)

    # ============== 检测完成 ==============
    log_info("")
    log_info("=== 检测完成 ===")
    log_ok("环境就绪，所有功能可用")
    log_info("")
    log_info(f"  [OK] Python {py_ver.major}.{py_ver.minor} ({platform.system()})")
    log_info(f"  [OK] AK/SK 已配置（SecretId: {masked_id}）")
    log_info(f"  [OK] Gateway 连通正常")
    sys.exit(0)


if __name__ == "__main__":
    main()
