#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI entrypoint for the WeChat Article Assistant skill."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from typing import Any

from account_service import (
    add_account,
    add_account_by_keyword,
    add_account_by_url,
    delete_account,
    list_account_articles,
    list_accounts,
    list_sync_targets,
    resolve_account_by_url,
    search_account,
    set_sync_target,
)
from article_service import article_detail, recent_articles
from env_check import env_check
from database import Database
from login_service import login_clear, login_import, login_info, login_poll, login_start, login_wait
from log_utils import configure_logging, get_logger
from mp_client import WechatLoginExpiredError, WechatMPClient, WechatRequestError
from openclaw_messaging import OpenClawMessenger, resolve_message_target
from session_store import get_login_session
from sync_service import sync_account, sync_all, sync_due, sync_logs
from utils import json_dumps, parse_bool


LOGGER = get_logger(__name__)


def _parse_proxy_urls(values: Any) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        values = [values]
    urls: list[str] = []
    for value in values:
        text = str(value or "").replace("\r", "\n").replace(",", "\n").replace(";", "\n")
        for item in text.split("\n"):
            item = item.strip()
            if item:
                urls.append(item)
    seen: set[str] = set()
    result: list[str] = []
    for item in urls:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _serialize_proxy_urls(values: Any) -> str:
    return "\n".join(_parse_proxy_urls(values))


def _proxy_row_with_list(row: dict[str, Any]) -> dict[str, Any]:
    data = dict(row or {})
    data["proxy_urls"] = _parse_proxy_urls(data.get("proxy_url"))
    data["proxy_count"] = len(data["proxy_urls"])
    return data


def _add_json_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="输出 JSON 结果")


def _add_message_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--channel", type=str, default="", help="消息渠道")
    parser.add_argument("--target", type=str, default="", help="消息目标")
    parser.add_argument("--account", type=str, default="", help="消息账号，可选")
    parser.add_argument("--inbound-meta-json", type=str, default="", help="Inbound Context JSON")
    parser.add_argument("--inbound-meta-file", type=str, default="", help="Inbound Context 文件路径")


def _resolve_message_target(args: argparse.Namespace):
    return resolve_message_target(
        channel=args.channel or None,
        target=args.target or None,
        account=args.account or None,
        inbound_meta_json=args.inbound_meta_json or None,
        inbound_meta_file=args.inbound_meta_file or None,
    )


def _resolve_messenger(args: argparse.Namespace) -> OpenClawMessenger | None:
    target = _resolve_message_target(args)
    if not target:
        return None
    return OpenClawMessenger(target)


def _validate_login_message_args(args: argparse.Namespace) -> dict[str, Any] | None:
    message_target = _resolve_message_target(args)
    if message_target:
        return None
    return {
        "success": False,
        "error": "login-start 缺少 channel/target，无法发送二维码。请检查 Inbound Context 提取或显式传入 --channel 与 --target；若 Inbound Context 中有 account_id，也应一并传入 --account。",
        "formatted_text": "login-start 缺少 channel/target，无法发送二维码。请检查 Inbound Context 提取或显式传入 --channel 与 --target；若 Inbound Context 中有 account_id，也应一并传入 --account。",
        "data": {
            "provided": {
                "channel": getattr(args, "channel", "") or "",
                "target": getattr(args, "target", "") or "",
                "account": getattr(args, "account", "") or "",
                "inbound_meta_json": bool(getattr(args, "inbound_meta_json", "")),
                "inbound_meta_file": getattr(args, "inbound_meta_file", "") or "",
            }
        },
    }


def _attach_message_target(result: dict[str, Any], message_target) -> dict[str, Any]:
    if not message_target:
        return result
    data = result.setdefault("data", {})
    if isinstance(data, dict):
        data.setdefault("message_target", asdict(message_target))
    return result


def _print_result(result: dict[str, Any], as_json: bool) -> int:
    if as_json:
        print(json_dumps(result))
    else:
        if result.get("formatted_text"):
            print(result["formatted_text"])
        else:
            print(json_dumps(result))
    return 0 if result.get("success") else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WeChat Article Assistant CLI")
    parser.add_argument("--debug", action="store_true", help="开启调试日志，并同时输出到控制台与日志文件")
    parser.add_argument("--log-level", default="", help="日志级别，例如 DEBUG/INFO/WARNING")
    parser.add_argument("--log-console", type=parse_bool, default=None, help="是否输出控制台日志")
    parser.add_argument("--log-file", type=parse_bool, default=None, help="是否写入日志文件")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_login_start = subparsers.add_parser("login-start", help="生成微信公众号登录二维码")
    _add_message_args(parser_login_start)
    parser_login_start.add_argument("--sid", type=str, default="", help="自定义 sid")
    parser_login_start.add_argument("--wait", type=parse_bool, default=False, help="生成二维码后是否直接等待登录完成")
    parser_login_start.add_argument("--timeout", type=int, default=300, help="配合 --wait 使用的最长等待秒数")
    parser_login_start.add_argument("--interval", type=int, default=3, help="配合 --wait 使用的轮询间隔秒数")
    parser_login_start.add_argument("--notify", type=parse_bool, default=True, help="是否发送二维码和登录结果通知")
    _add_json_flag(parser_login_start)

    parser_login_poll = subparsers.add_parser("login-poll", help="轮询扫码登录状态")
    _add_message_args(parser_login_poll)
    parser_login_poll.add_argument("--sid", required=True, help="二维码会话 sid")
    parser_login_poll.add_argument("--notify", type=parse_bool, default=False, help="状态变化时发送通知")
    _add_json_flag(parser_login_poll)

    parser_login_wait = subparsers.add_parser("login-wait", help="等待扫码登录完成")
    _add_message_args(parser_login_wait)
    parser_login_wait.add_argument("--sid", required=True, help="二维码会话 sid")
    parser_login_wait.add_argument("--timeout", type=int, default=300, help="最长等待秒数")
    parser_login_wait.add_argument("--interval", type=int, default=3, help="轮询间隔秒数")
    parser_login_wait.add_argument("--notify", type=parse_bool, default=True, help="是否发送登录结果通知")
    _add_json_flag(parser_login_wait)

    parser_login_import = subparsers.add_parser("login-import", help="导入已有登录 token/cookie 文件")
    parser_login_import.add_argument("--file", required=True, help="旧系统导出的 cookie JSON 文件")
    parser_login_import.add_argument("--validate", type=parse_bool, default=True, help="导入后立即校验")
    _add_json_flag(parser_login_import)

    parser_login_info = subparsers.add_parser("login-info", help="查看当前登录状态")
    parser_login_info.add_argument("--validate", type=parse_bool, default=False, help="是否调用微信接口校验")
    _add_json_flag(parser_login_info)

    parser_login_clear = subparsers.add_parser("login-clear", help="清除当前登录状态")
    _add_json_flag(parser_login_clear)

    parser_proxy_set = subparsers.add_parser("proxy-set", help="设置文章/同步代理")
    parser_proxy_set.add_argument("--url", type=str, default="", help="代理地址，例如 http://127.0.0.1:7890")
    parser_proxy_set.add_argument("--enabled", type=parse_bool, default=True, help="是否启用代理")
    parser_proxy_set.add_argument("--apply-article-fetch", type=parse_bool, default=True, help="文章详情抓取是否走代理")
    parser_proxy_set.add_argument("--apply-sync", type=parse_bool, default=True, help="同步和远端文章清单是否走代理")
    parser_proxy_set.add_argument("--urls", action="append", default=[], help="澶氫釜浠ｇ悊鍦板潃锛屽彲澶氭浼犲叆鎴栫敤鎹㈣/閫楀彿鍒嗛殧")
    _add_json_flag(parser_proxy_set)

    parser_proxy_show = subparsers.add_parser("proxy-show", help="查看代理配置")
    _add_json_flag(parser_proxy_show)

    parser_search_account = subparsers.add_parser("search-account", help="搜索公众号")
    parser_search_account.add_argument("keyword", help="关键字")
    parser_search_account.add_argument("--limit", type=int, default=10, help="候选数量")
    _add_json_flag(parser_search_account)

    parser_resolve_account_url = subparsers.add_parser("resolve-account-url", help="根据文章链接反查公众号")
    parser_resolve_account_url.add_argument("--url", required=True, help="公众号文章链接")
    parser_resolve_account_url.add_argument("--limit", type=int, default=20, help="候选数量")
    _add_json_flag(parser_resolve_account_url)

    parser_add_account = subparsers.add_parser("add-account", help="添加公众号")
    parser_add_account.add_argument("--fakeid", required=True, help="公众号 fakeid")
    parser_add_account.add_argument("--nickname", required=True, help="公众号昵称")
    parser_add_account.add_argument("--alias", default="", help="公众号别名")
    parser_add_account.add_argument("--avatar", default="", help="头像 URL")
    parser_add_account.add_argument("--service-type", type=int, default=0, help="服务类型")
    parser_add_account.add_argument("--signature", default="", help="公众号简介")
    parser_add_account.add_argument("--enable-sync", type=parse_bool, default=True, help="是否启用同步")
    parser_add_account.add_argument("--sync-hour", type=int, default=8, help="同步小时")
    parser_add_account.add_argument("--sync-minute", type=int, default=0, help="同步分钟")
    parser_add_account.add_argument("--initial-sync", type=parse_bool, default=False, help="添加后是否立即同步")
    _add_json_flag(parser_add_account)

    parser_add_by_keyword = subparsers.add_parser("add-account-by-keyword", help="按关键字自动添加公众号")
    parser_add_by_keyword.add_argument("keyword", help="关键字或公众号名")
    parser_add_by_keyword.add_argument("--limit", type=int, default=10, help="候选数量")
    parser_add_by_keyword.add_argument("--initial-sync", type=parse_bool, default=False, help="添加后是否立即同步")
    _add_json_flag(parser_add_by_keyword)

    parser_add_by_url = subparsers.add_parser("add-account-by-url", help="根据文章链接自动添加公众号")
    parser_add_by_url.add_argument("--url", required=True, help="公众号文章链接")
    parser_add_by_url.add_argument("--limit", type=int, default=20, help="候选数量")
    parser_add_by_url.add_argument("--initial-sync", type=parse_bool, default=False, help="添加后是否立即同步")
    _add_json_flag(parser_add_by_url)

    parser_list_accounts = subparsers.add_parser("list-accounts", help="列出本地公众号")
    _add_json_flag(parser_list_accounts)

    parser_delete_account = subparsers.add_parser("delete-account", help="删除公众号及其本地文章")
    parser_delete_account.add_argument("--fakeid", default="", help="公众号 fakeid")
    parser_delete_account.add_argument("--nickname", default="", help="公众号昵称")
    _add_json_flag(parser_delete_account)

    parser_list_sync_targets = subparsers.add_parser("list-sync-targets", help="列出同步目标")
    _add_json_flag(parser_list_sync_targets)

    parser_set_sync_target = subparsers.add_parser("set-sync-target", help="设置同步目标配置")
    parser_set_sync_target.add_argument("--fakeid", default="", help="公众号 fakeid")
    parser_set_sync_target.add_argument("--nickname", default="", help="公众号昵称")
    parser_set_sync_target.add_argument("--enabled", type=parse_bool, default=True, help="是否启用")
    parser_set_sync_target.add_argument("--sync-hour", type=int, default=None, help="同步小时")
    parser_set_sync_target.add_argument("--sync-minute", type=int, default=None, help="同步分钟")
    _add_json_flag(parser_set_sync_target)

    parser_list_account_articles = subparsers.add_parser("list-account-articles", help="查询公众号文章清单")
    parser_list_account_articles.add_argument("--fakeid", default="", help="公众号 fakeid")
    parser_list_account_articles.add_argument("--nickname", default="", help="公众号昵称")
    parser_list_account_articles.add_argument("--begin", type=int, default=0, help="起始偏移")
    parser_list_account_articles.add_argument("--count", type=int, default=10, help="条数")
    parser_list_account_articles.add_argument("--keyword", default="", help="搜索关键字")
    parser_list_account_articles.add_argument("--remote", type=parse_bool, default=True, help="是否查询远端")
    parser_list_account_articles.add_argument("--save", type=parse_bool, default=True, help="远端结果是否写入本地数据库")
    _add_json_flag(parser_list_account_articles)

    parser_sync = subparsers.add_parser("sync", help="同步单个公众号")
    parser_sync.add_argument("--fakeid", required=True, help="公众号 fakeid")
    _add_json_flag(parser_sync)

    parser_sync_all = subparsers.add_parser("sync-all", help="同步全部启用的公众号")
    parser_sync_all.add_argument("--interval-seconds", type=int, default=0, help="不同公众号之间的同步间隔秒数")
    _add_json_flag(parser_sync_all)

    parser_sync_due = subparsers.add_parser("sync-due", help="供外部定时任务调用的到点同步入口")
    parser_sync_due.add_argument("--grace-minutes", type=int, default=3, help="允许补跑的分钟窗口，默认 3 分钟")
    _add_json_flag(parser_sync_due)

    parser_sync_logs = subparsers.add_parser("sync-logs", help="查看同步日志")
    parser_sync_logs.add_argument("--fakeid", default="", help="按 fakeid 过滤")
    parser_sync_logs.add_argument("--limit", type=int, default=50, help="最多返回条数")
    _add_json_flag(parser_sync_logs)

    parser_recent = subparsers.add_parser("recent-articles", help="查看最近文章")
    parser_recent.add_argument("--hours", type=int, default=24, help="最近多少小时")
    parser_recent.add_argument("--limit", type=int, default=50, help="最多返回条数")
    _add_json_flag(parser_recent)

    parser_article_detail = subparsers.add_parser("article-detail", help="抓取单篇文章详情")
    parser_article_detail.add_argument("--aid", default="", help="文章 aid")
    parser_article_detail.add_argument("--link", default="", help="公众号文章链接")
    parser_article_detail.add_argument("--download-images", type=parse_bool, default=True, help="是否下载图片")
    parser_article_detail.add_argument("--include-html", type=parse_bool, default=False, help="是否返回并保存 HTML")
    parser_article_detail.add_argument("--force-refresh", type=parse_bool, default=False, help="是否跳过缓存重新抓取")
    parser_article_detail.add_argument("--save", type=parse_bool, default=True, help="是否落地保存 article.json 和 article.md")
    _add_json_flag(parser_article_detail)

    parser_doctor = subparsers.add_parser("doctor", help="检查登录、代理与基础环境状态")
    _add_json_flag(parser_doctor)

    parser_env_check = subparsers.add_parser("env-check", help="检查 Skill 运行环境与依赖")
    _add_json_flag(parser_env_check)

    return parser


def handle_command(args: argparse.Namespace) -> dict[str, Any]:
    db = Database()
    try:
        LOGGER.debug("handle_command command=%s", args.command)
        if args.command == "login-start":
            validation_error = _validate_login_message_args(args)
            if validation_error:
                return validation_error
            message_target = _resolve_message_target(args)
            messenger = OpenClawMessenger(message_target) if message_target else None
            result = login_start(
                db,
                messenger=messenger,
                sid=args.sid,
                wait=args.wait,
                timeout=args.timeout,
                interval=args.interval,
                notify=args.notify,
            )
            return _attach_message_target(result, message_target)
        if args.command == "login-poll":
            message_target = _resolve_message_target(args)
            result = login_poll(
                db,
                sid=args.sid,
                messenger=OpenClawMessenger(message_target) if message_target else None,
                notify=args.notify,
            )
            return _attach_message_target(result, message_target)
        if args.command == "login-wait":
            message_target = _resolve_message_target(args)
            result = login_wait(
                db,
                sid=args.sid,
                timeout=args.timeout,
                interval=args.interval,
                messenger=OpenClawMessenger(message_target) if message_target else None,
                notify=args.notify,
            )
            return _attach_message_target(result, message_target)
        if args.command == "login-import":
            return login_import(db, file_path=args.file, validate=args.validate)
        if args.command == "login-info":
            return login_info(db, validate=args.validate)
        if args.command == "login-clear":
            return login_clear(db)
        if args.command == "proxy-set":
            now = int(__import__("time").time())
            proxy_urls = _parse_proxy_urls(getattr(args, "urls", []) or [])
            proxy_urls.extend(_parse_proxy_urls(getattr(args, "url", "")))
            serialized_proxy_urls = _serialize_proxy_urls(proxy_urls)
            db.execute(
                """
                INSERT INTO proxy_config (name, enabled, proxy_url, apply_article_fetch, apply_sync, created_at, updated_at)
                VALUES ('default', ?, ?, ?, ?, COALESCE((SELECT created_at FROM proxy_config WHERE name = 'default'), ?), ?)
                ON CONFLICT(name) DO UPDATE SET
                  enabled = excluded.enabled,
                  proxy_url = excluded.proxy_url,
                  apply_article_fetch = excluded.apply_article_fetch,
                  apply_sync = excluded.apply_sync,
                  updated_at = excluded.updated_at
                """,
                (
                    1 if args.enabled else 0,
                    serialized_proxy_urls,
                    1 if args.apply_article_fetch else 0,
                    1 if args.apply_sync else 0,
                    now,
                    now,
                ),
            )
            row = _proxy_row_with_list(db.row("SELECT * FROM proxy_config WHERE name = 'default'") or {})
            return {"success": True, "data": row, "formatted_text": "代理配置已更新"}
        if args.command == "proxy-show":
            row = _proxy_row_with_list(db.row("SELECT * FROM proxy_config WHERE name = 'default'") or {})
            return {"success": True, "data": row, "formatted_text": "当前代理配置"}
        if args.command == "search-account":
            return search_account(db, keyword=args.keyword, limit=args.limit)
        if args.command == "resolve-account-url":
            return resolve_account_by_url(db, url=args.url, limit=args.limit)
        if args.command == "add-account":
            return add_account(
                db,
                fakeid=args.fakeid,
                nickname=args.nickname,
                alias=args.alias,
                avatar=args.avatar,
                service_type=args.service_type,
                signature=args.signature,
                enable_sync=args.enable_sync,
                sync_hour=args.sync_hour,
                sync_minute=args.sync_minute,
                initial_sync=args.initial_sync,
            )
        if args.command == "add-account-by-keyword":
            return add_account_by_keyword(db, keyword=args.keyword, limit=args.limit, initial_sync=args.initial_sync)
        if args.command == "add-account-by-url":
            return add_account_by_url(db, url=args.url, limit=args.limit, initial_sync=args.initial_sync)
        if args.command == "list-accounts":
            return list_accounts(db)
        if args.command == "delete-account":
            return delete_account(db, fakeid=args.fakeid, nickname=args.nickname)
        if args.command == "list-sync-targets":
            return list_sync_targets(db)
        if args.command == "set-sync-target":
            return set_sync_target(
                db,
                fakeid=args.fakeid,
                nickname=args.nickname,
                enabled=args.enabled,
                sync_hour=args.sync_hour,
                sync_minute=args.sync_minute,
            )
        if args.command == "list-account-articles":
            return list_account_articles(
                db,
                fakeid=args.fakeid,
                nickname=args.nickname,
                begin=args.begin,
                count=args.count,
                keyword=args.keyword,
                remote=args.remote,
                save_remote=args.save,
            )
        if args.command == "sync":
            return sync_account(db, fakeid=args.fakeid)
        if args.command == "sync-all":
            return sync_all(db, interval_seconds=args.interval_seconds)
        if args.command == "sync-due":
            return sync_due(db, grace_minutes=args.grace_minutes)
        if args.command == "sync-logs":
            return sync_logs(db, fakeid=args.fakeid, limit=args.limit)
        if args.command == "recent-articles":
            return recent_articles(db, hours=args.hours, limit=args.limit)
        if args.command == "article-detail":
            return article_detail(
                db,
                aid=args.aid,
                link=args.link,
                download_images=args.download_images,
                include_html=args.include_html,
                force_refresh=args.force_refresh,
                save_files=args.save,
            )
        if args.command == "doctor":
            session = get_login_session(db)
            proxy = _proxy_row_with_list(db.row("SELECT * FROM proxy_config WHERE name = 'default'") or {})
            client = WechatMPClient(db)
            env_result = env_check()
            session_summary: dict[str, Any] = {}
            if session:
                cookies = session.get("cookies") or []
                session_summary = {
                    "id": session.get("id"),
                    "token": session.get("token", ""),
                    "nickname": session.get("nickname", ""),
                    "head_img": session.get("head_img", ""),
                    "source": session.get("source", ""),
                    "valid": bool(session.get("valid")),
                    "last_validated_at": session.get("last_validated_at"),
                    "expires_at": session.get("expires_at"),
                    "created_at": session.get("created_at"),
                    "updated_at": session.get("updated_at"),
                    "cookie_count": len(cookies),
                    "has_cookie_header": bool(session.get("cookie_header")),
                }
            login_health: dict[str, Any] = {
                "present": bool(session and session.get("token")),
                "validated": False,
                "message": "未找到登录会话",
                "reason": "未找到登录会话",
                "reason_type": "missing_session",
            }
            if session and session.get("token"):
                try:
                    validated = client.validate_login()
                    login_health = {
                        "present": True,
                        "validated": True,
                        "message": "登录态校验通过",
                        "reason": "登录态校验通过",
                        "reason_type": "ok",
                        "nickname": validated.get("nickname", ""),
                        "head_img": validated.get("head_img", ""),
                        "token": validated.get("token", ""),
                    }
                except WechatLoginExpiredError as exc:
                    login_health = {
                        "present": True,
                        "validated": False,
                        "message": str(exc),
                        "reason": str(exc),
                        "reason_type": "login_expired",
                    }
                except WechatRequestError as exc:
                    login_health = {
                        "present": True,
                        "validated": False,
                        "message": str(exc),
                        "reason": str(exc),
                        "reason_type": "request_error",
                    }
            return {
                "success": True,
                "data": {
                    "logged_in": bool(login_health.get("validated")),
                    "login_session": session_summary,
                    "login_health": login_health,
                    "proxy_config": proxy or {},
                    "proxy_health": {
                        "sync": client.check_proxy_health("sync"),
                        "article": client.check_proxy_health("article"),
                    },
                    "env_check": env_result.get("data", {}),
                },
                "formatted_text": "系统状态检查完成",
            }
        if args.command == "env-check":
            return env_check()
        return {"success": False, "error": f"未知命令: {args.command}", "formatted_text": f"未知命令: {args.command}"}
    finally:
        db.close()


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(
        level="DEBUG" if args.debug else (args.log_level or None),
        console=True if args.debug else args.log_console,
        file_logging=True if args.debug else args.log_file,
        force=True,
    )
    try:
        LOGGER.debug("main argv=%s", argv or [])
        result = handle_command(args)
    except Exception as exc:
        LOGGER.exception("command failed")
        result = {
            "success": False,
            "error": str(exc),
            "formatted_text": str(exc),
        }
    return _print_result(result, as_json=bool(getattr(args, "json", False)))
