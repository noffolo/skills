#!/usr/bin/env python3
# Copyright (c) 2026 思捷娅科技 (SJYKJ)
# License: MIT
"""SQLite 数据库初始化"""

import sqlite3
import os
import json
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "email-index.db")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "email-config.json")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS email_index (
            message_id TEXT PRIMARY KEY,
            gmail_uid TEXT NOT NULL,
            subject TEXT DEFAULT '',
            from_addr TEXT DEFAULT '',
            category TEXT DEFAULT 'other',
            priority INTEGER DEFAULT 4,
            confidence REAL DEFAULT 0.0,
            classified_method TEXT DEFAULT '',
            classified_at TEXT,
            replied_at TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_category ON email_index(category);
        CREATE INDEX IF NOT EXISTS idx_priority ON email_index(priority);
        CREATE INDEX IF NOT EXISTS idx_created ON email_index(created_at);

        CREATE TABLE IF NOT EXISTS sent_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            to_addr TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            in_reply_to TEXT DEFAULT '',
            sent_at TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()
    print(f"DB initialized: {DB_PATH}")

if __name__ == "__main__":
    init_db()
