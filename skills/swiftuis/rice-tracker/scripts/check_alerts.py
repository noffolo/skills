#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日大米库存检查脚本（供 cron 调用）"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

DATA_FILE = Path.home() / ".openclaw" / "workspace" / "rice-shop-records.json"

def days_left(record):
    today = date.today()
    purchased = date.fromisoformat(record["purchase_date"])
    consumed_per_day = record["daily_rate"]
    freq = record.get("frequency", "daily")
    people = record["people"]
    if freq == "workdays":
        days = (today - purchased).days + 1
        workdays = sum(1 for i in range(days)
                       if (purchased + timedelta(i)).weekday() < 5)
        total_consumed = workdays * people * consumed_per_day
    elif freq == "weekends":
        days = (today - purchased).days + 1
        weekends = sum(1 for i in range(days)
                       if (purchased + timedelta(i)).weekday() >= 5)
        total_consumed = weekends * people * consumed_per_day
    else:
        total_consumed = (today - purchased).days * people * consumed_per_day
    remaining = record["quantity"] - total_consumed
    if remaining <= 0:
        return -1
    if freq == "workdays":
        return round(remaining / (people * consumed_per_day))
    elif freq == "weekends":
        return round(remaining * 7 / (2 * people * consumed_per_day))
    else:
        return round(remaining / (people * consumed_per_day))

def expected_date(record):
    d = days_left(record)
    if d < 0:
        return "已吃完"
    return (date.today() + timedelta(days=d)).strftime("%m-%d")

def check():
    if not DATA_FILE.exists():
        return None, None
    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    alerts = []
    for r in records:
        dl = days_left(r)
        r["days_left"] = dl
        r["exp_date"] = expected_date(r)
        if dl < 0:
            alerts.append(f"🚨 【{r['owner']}】的大米已耗尽，请立即采购！")
        elif dl <= 3:
            alerts.append(f"⚠️ 【{r['owner']}】的大米预计 {dl} 天后（{expected_date(r)}）吃完，建议提醒采购。")
    return alerts, records

if __name__ == "__main__":
    alerts, records = check()
    msg_lines = []
    if alerts:
        msg_lines.append("🍚 **大米采购提醒**")
        for a in alerts:
            msg_lines.append(a)
        msg_lines.append("")
        msg_lines.append("请登录系统处理：python3 ~/.openclaw/workspace/skills/rice-tracker/scripts/app.py")
    else:
        if records:
            msg_lines.append(f"🍚 大米检查完毕，今日（{date.today().strftime('%m-%d')}）共 {len(records)} 位客户，库存均充足，无需提醒。")
        else:
            msg_lines.append("🍚 大米检查完毕，暂无客户记录。")
    print("\n".join(msg_lines))
