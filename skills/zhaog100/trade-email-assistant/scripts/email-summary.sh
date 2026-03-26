#!/bin/bash
# Copyright (c) 2026 思捷娅科技 (SJYKJ)
# License: MIT
# 邮件摘要 + 30天清理

set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DB_PATH="$BASE_DIR/data/email-index.db"
LOG_DIR="$BASE_DIR/logs"
LOG_FILE="$LOG_DIR/email-summary.log"

mkdir -p "$LOG_DIR"

if [ ! -f "$DB_PATH" ]; then
    echo "DB not found. Run init-db.py first."
    exit 1
fi

TIMESTAMP=$(date +"%Y-%m-%d")
HOUR=$(date +"%H")

echo "📧 邮件摘要 ($TIMESTAMP)" | tee "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Count by category
echo "📊 按分类统计:" | tee -a "$LOG_FILE"
sqlite3 "$DB_PATH" "SELECT category, COUNT(*) FROM email_index WHERE created_at >= datetime('now', 'start of day') GROUP BY category ORDER BY MIN(priority)" 2>/dev/null | while IFS='|' read -r cat count; do
    case "$cat" in
        inquiry) emoji="🔴 询盘";;
        order)   emoji="🟠 订单";;
        logistics) emoji="🟡 物流";;
        platform)  emoji="🔵 平台";;
        *)        emoji="⚪ 其他";;
    esac
    echo "  $emoji (${count}封)" | tee -a "$LOG_FILE"
done

echo "" | tee -a "$LOG_FILE"

# List today's emails with category
echo "📋 今日邮件:" | tee -a "$LOG_FILE"
sqlite3 -separator " | " "$DB_PATH" "SELECT gmail_uid, from_addr, subject, category FROM email_index WHERE created_at >= datetime('now', 'start of day') ORDER BY priority, created_at DESC" 2>/dev/null | while IFS='|' read -r uid from subject cat; do
    echo "  #$uid | $from | $subject [$cat]" | tee -a "$LOG_FILE"
done

echo "" | tee -a "$LOG_FILE"

# 48h unreplied inquiry warning
echo "⏳ 待回复提醒:" | tee -a "$LOG_FILE"
unreplied=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM email_index WHERE category='inquiry' AND replied_at IS NULL AND created_at < datetime('now', '-48 hours')" 2>/dev/null || echo "0")
echo "  $unreplied 封询盘超过 48h 未回复" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"

# Sent emails today
sent_today=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM sent_emails WHERE sent_at >= datetime('now', 'start of day')" 2>/dev/null || echo "0")
echo "📤 今日已发送: ${sent_today}封" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"

# 30-day cleanup
cleanup_days=$(python3 -c "import json; c=json.load(open('$BASE_DIR/config/email-config.json')); print(c.get('maintenance',{}).get('cleanup_days',30))" 2>/dev/null || echo "30")
deleted=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM email_index WHERE created_at < datetime('now', '-$cleanup_days days')" 2>/dev/null || echo "0")
sqlite3 "$DB_PATH" "DELETE FROM email_index WHERE created_at < datetime('now', '-$cleanup_days days')" 2>/dev/null || true
echo "🧹 清理 ${cleanup_days}天前数据: 删除 ${deleted} 条记录" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "✅ 摘要完成" | tee -a "$LOG_FILE"
