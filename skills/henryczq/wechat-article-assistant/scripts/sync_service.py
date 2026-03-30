#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manual sync and external scheduled sync entrypoints."""

from __future__ import annotations

import time

from article_service import upsert_articles
from database import Database
from log_utils import get_logger
from mp_client import WechatLoginExpiredError, WechatRequestError
from session_store import update_login_validation
from utils import failure, now_ts, success


LOGGER = get_logger(__name__)


def _format_sync_error(message: str) -> tuple[str, str | None]:
    normalized = str(message or "").strip()
    if normalized.lower() == "invalid session":
        return "微信网络限制，请使用代理", normalized
    return normalized, None


def _account_name(db: Database, fakeid: str) -> str:
    row = db.row("SELECT nickname FROM account WHERE fakeid = ?", (fakeid,))
    return str((row or {}).get("nickname") or fakeid)


def _log_sync(db: Database, fakeid: str, status: str, message: str, articles_synced: int, started_at: int, finished_at: int) -> None:
    db.execute(
        """
        INSERT INTO sync_log (fakeid, nickname, status, message, articles_synced, started_at, finished_at, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            fakeid,
            _account_name(db, fakeid),
            status,
            message,
            articles_synced,
            started_at,
            finished_at,
            finished_at,
        ),
    )


def _update_sync_status(db: Database, fakeid: str, status: str, message: str) -> None:
    db.execute(
        """
        UPDATE sync_config
        SET last_sync_at = ?, last_sync_status = ?, last_sync_message = ?, updated_at = ?
        WHERE fakeid = ?
        """,
        (now_ts(), status, message, now_ts(), fakeid),
    )


def sync_account(db: Database, fakeid: str, max_pages: int | None = None, page_size: int = 5, extra_pages_after_existing: int = 1) -> dict:
    started_at = now_ts()
    from mp_client import WechatMPClient

    LOGGER.info(
        "sync_account start fakeid=%s max_pages=%s page_size=%s extra_pages_after_existing=%s",
        fakeid,
        max_pages,
        page_size,
        extra_pages_after_existing,
    )
    client = WechatMPClient(db)
    known_ids = {row["id"] for row in db.rows("SELECT id FROM article WHERE fakeid = ?", (fakeid,))}
    queued_ids: set[str] = set()

    all_new = []
    total_count = 0
    pages_fetched = 0
    existing_hit_page: int | None = None
    try:
        validated = client.validate_login()
        update_login_validation(
            db,
            True,
            nickname=str(validated.get("nickname") or ""),
            head_img=str(validated.get("head_img") or ""),
        )
        page_index = 0
        while True:
            if max_pages and page_index >= max_pages:
                break
            begin = page_index * page_size
            payload = client.fetch_article_page(fakeid=fakeid, begin=begin, count=page_size)
            total_count = int(payload.get("total_count") or total_count)
            remote_articles = payload.get("articles") or []
            LOGGER.debug(
                "sync_account page fakeid=%s page_index=%s begin=%s remote_articles=%s total_count=%s",
                fakeid,
                page_index,
                begin,
                len(remote_articles),
                total_count,
            )
            if not remote_articles:
                break

            found_existing = False
            for article in remote_articles:
                aid = str(article.get("aid") or f"{article.get('appmsgid', 0)}_{article.get('itemidx', 1)}")
                article_id = f"{fakeid}:{aid}"
                if article_id in known_ids:
                    found_existing = True
                    continue
                if article_id in queued_ids:
                    continue
                queued_ids.add(article_id)
                all_new.append(article)
            pages_fetched += 1
            if found_existing and existing_hit_page is None:
                existing_hit_page = page_index
            if existing_hit_page is not None and page_index - existing_hit_page >= max(0, extra_pages_after_existing):
                break
            if total_count and begin + page_size >= total_count:
                break
            page_index += 1

        saved = upsert_articles(db, fakeid, all_new)
        synced_count = len(saved)
        db.execute(
            """
            UPDATE account
            SET total_count = ?, articles_synced = articles_synced + ?, last_sync_at = ?, updated_at = ?
            WHERE fakeid = ?
            """,
            (total_count, synced_count, now_ts(), now_ts(), fakeid),
        )
        message = f"同步完成，新增 {synced_count} 篇文章"
        LOGGER.info(
            "sync_account success fakeid=%s synced_count=%s total_count=%s pages_fetched=%s",
            fakeid,
            synced_count,
            total_count,
            pages_fetched,
        )
        _update_sync_status(db, fakeid, "success", message)
        _log_sync(db, fakeid, "success", message, synced_count, started_at, now_ts())
        return success(
            {
                "fakeid": fakeid,
                "articles_synced": synced_count,
                "total_count": total_count,
                "pages_fetched": pages_fetched,
                "existing_hit_page": existing_hit_page,
                "extra_pages_after_existing": max(0, extra_pages_after_existing),
                "message": message,
            },
            message,
        )
    except WechatLoginExpiredError as exc:
        message = "微信登录已过期，请重新扫码登录"
        request_debug = client.get_last_request_debug()
        LOGGER.warning("sync_account login expired fakeid=%s error=%s raw_error=%s", fakeid, message, str(exc))
        update_login_validation(db, False)
        _update_sync_status(db, fakeid, "failed", message)
        _log_sync(db, fakeid, "failed", message, 0, started_at, now_ts())
        data = {
            "fakeid": fakeid,
            "original_error": str(exc),
            "login_expired": True,
        }
        if request_debug:
            data["request_debug"] = request_debug
        return failure(message, data)
    except WechatRequestError as exc:
        raw_message = str(exc)
        message, original_error = _format_sync_error(raw_message)
        request_debug = client.get_last_request_debug()
        LOGGER.warning("sync_account failed fakeid=%s error=%s raw_error=%s", fakeid, message, raw_message)
        _update_sync_status(db, fakeid, "failed", message)
        _log_sync(db, fakeid, "failed", message, 0, started_at, now_ts())
        data = {"fakeid": fakeid}
        if original_error:
            data["original_error"] = original_error
        if request_debug:
            data["request_debug"] = request_debug
        return failure(message, data)


def sync_all(db: Database, interval_seconds: int = 0) -> dict:
    targets = db.rows("SELECT fakeid FROM sync_config WHERE enabled = 1 ORDER BY fakeid")
    interval_seconds = max(0, int(interval_seconds or 0))
    LOGGER.info("sync_all targets=%s interval_seconds=%s", len(targets), interval_seconds)
    results = []
    success_count = 0
    for index, item in enumerate(targets):
        result = sync_account(db, item["fakeid"])
        results.append(result)
        if result.get("success"):
            success_count += 1
        if interval_seconds > 0 and index < len(targets) - 1:
            LOGGER.info("sync_all sleep interval_seconds=%s before_next=%s", interval_seconds, targets[index + 1]["fakeid"])
            time.sleep(interval_seconds)
    return success(
        {
            "total": len(targets),
            "success": success_count,
            "failed": len(targets) - success_count,
            "interval_seconds": interval_seconds,
            "results": results,
        },
        f"已执行 {len(targets)} 个同步任务，成功 {success_count} 个",
    )


def sync_due(db: Database, grace_minutes: int = 3) -> dict:
    now = now_ts()
    now_struct = time.localtime(now)
    now_minute_of_day = int(now_struct.tm_hour) * 60 + int(now_struct.tm_min)
    grace_minutes = max(0, int(grace_minutes or 0))
    targets = db.rows("SELECT * FROM sync_config WHERE enabled = 1 ORDER BY fakeid")
    due_targets = []
    results = []
    LOGGER.debug("sync_due checking enabled_targets=%s grace_minutes=%s", len(targets), grace_minutes)

    for item in targets:
        scheduled_minute_of_day = int(item.get("sync_hour") or 0) * 60 + int(item.get("sync_minute") or 0)
        delta = now_minute_of_day - scheduled_minute_of_day
        if delta < 0 or delta > grace_minutes:
            continue

        last_sync_at = item.get("last_sync_at")
        if last_sync_at:
            struct = time.localtime(int(last_sync_at))
            if struct.tm_year == now_struct.tm_year and struct.tm_yday == now_struct.tm_yday:
                last_sync_minute_of_day = int(struct.tm_hour) * 60 + int(struct.tm_min)
                if last_sync_minute_of_day >= scheduled_minute_of_day:
                    continue
        due_targets.append(item)

    for target in due_targets:
        results.append(sync_account(db, target["fakeid"]))

    return success(
        {
            "checked": len(targets),
            "due": len(due_targets),
            "grace_minutes": grace_minutes,
            "results": results,
        },
        f"本次到点同步目标数: {len(due_targets)}",
    )


def sync_logs(db: Database, fakeid: str = "", limit: int = 50) -> dict:
    LOGGER.debug("sync_logs fakeid=%s limit=%s", fakeid, limit)
    if fakeid:
        rows = db.rows(
            """
            SELECT * FROM sync_log
            WHERE fakeid = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (fakeid, limit),
        )
    else:
        rows = db.rows(
            """
            SELECT * FROM sync_log
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )
    return success(
        {
            "total": len(rows),
            "logs": rows,
        },
        f"同步日志条数: {len(rows)}",
    )
