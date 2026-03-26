#!/usr/bin/env python3
# Copyright (c) 2026 思捷娅科技 (SJYKJ)
# License: MIT
"""IMAP 邮件拉取 + MIME 解码 + JSON 输出"""

import imaplib
import email
import email.header
import email.utils
import json
import sys
import os
import re
import base64
import quopri
import sqlite3
import time
import logging
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "email-index.db")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "email-check.log"),
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("check-emails")

CONFIG = json.load(open(os.path.join(BASE_DIR, "config", "email-config.json")))

def load_credentials():
    env_file = os.path.expanduser(CONFIG["credentials"]["env_file"])
    creds = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#") and not line.startswith("export"):
                k, v = line.split("=", 1)
                creds[k.strip()] = v.strip().strip('"').strip("'")
    return creds.get("GMAIL_USER"), creds.get("GMAIL_PASS")

def decode_header_value(value):
    if value is None:
        return ""
    parts = email.header.decode_header(value)
    result = []
    for data, charset in parts:
        if isinstance(data, bytes):
            result.append(data.decode(charset or "utf-8", errors="replace"))
        else:
            result.append(data)
    return "".join(result)

def decode_part(part):
    charset = part.get_content_charset() or "utf-8"
    transfer_encoding = (part.get("Content-Transfer-Encoding") or "").lower().strip()
    raw = part.get_payload(decode=True)
    if raw is None:
        return ""
    try:
        if transfer_encoding == "quoted-printable":
            raw = quopri.decodestring(raw)
        elif transfer_encoding == "base64":
            raw = base64.b64decode(raw)
        return raw.decode(charset, errors="replace")
    except Exception:
        return raw.decode("utf-8", errors="replace")

def strip_html(html):
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<p[^>]*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"</p>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"<[^>]+>", "", html)
    html = html.replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">")
    html = html.replace("&amp;", "&").replace("&quot;", '"')
    return re.sub(r"\n{3,}", "\n\n", html).strip()

def extract_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and not part.get_filename():
                return decode_part(part)
        for part in msg.walk():
            if part.get_content_type() == "text/html" and not part.get_filename():
                return strip_html(decode_part(part))
    else:
        if msg.get_content_type() == "text/html":
            return strip_html(decode_part(msg))
        return decode_part(msg)
    return ""

def extract_attachments(msg):
    names = []
    if msg.is_multipart():
        for part in msg.walk():
            fn = part.get_filename()
            if fn:
                names.append(decode_header_value(fn))
    return names

def get_existing_ids():
    if not os.path.exists(DB_PATH):
        return set()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA busy_timeout=5000")
    rows = conn.execute("SELECT message_id FROM email_index").fetchall()
    conn.close()
    return {r[0] for r in rows}

def save_to_db(emails_data):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA busy_timeout=5000")
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    for e in emails_data:
        try:
            conn.execute(
                "INSERT OR IGNORE INTO email_index (message_id, gmail_uid, subject, from_addr, created_at) VALUES (?,?,?,?,?)",
                (e["message_id"], e["uid"], e["subject"], e["from"], now)
            )
        except Exception as ex:
            log.warning("DB write error: %s", ex)
    conn.commit()
    conn.close()

def parse_date(msg):
    date_str = msg.get("Date", "")
    try:
        parsed = email.utils.parsedate_to_datetime(date_str)
        return parsed.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return date_str

def fetch_emails(max_count=20, since=None):
    user, password = load_credentials()
    existing_ids = get_existing_ids()
    preview_len = CONFIG["check"].get("body_preview_length", 200)

    for attempt in range(3):
        try:
            conn = imaplib.IMAP4_SSL(CONFIG["imap"]["host"], CONFIG["imap"]["port"])
            conn.login(user, password)
            conn.select("INBOX", readonly=True)
            break
        except Exception as ex:
            log.error("IMAP connect attempt %d failed: %s", attempt + 1, ex)
            if attempt < 2:
                time.sleep(5)
            else:
                print(json.dumps({"error": f"IMAP connection failed after 3 attempts: {ex}"}))
                sys.exit(1)

    try:
        since_date = None
        if since:
            try:
                since_date = datetime.strptime(since, "%Y-%m-%d").strftime("%d-%b-%Y")
            except ValueError:
                pass
        
        search_criteria = '(UNSEEN)'
        if since_date:
            search_criteria = f'(SINCE {since_date})'
        
        status, messages = conn.search(None, search_criteria)
        if status != "OK" or not messages[0]:
            return {"total": 0, "emails": []}

        uid_list = messages[0].split()[::-1]  # newest first
        uid_list = uid_list[:max_count]
        
        results = []
        for uid_bytes in uid_list:
            uid = uid_bytes.decode()
            try:
                status, data = conn.fetch(uid_bytes, "(BODY.PEEK[] UID)")
                if status != "OK" or not data or not data[0]:
                    continue
                
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # Extract UID from response
                uid_match = re.search(r'UID (\d+)', data[0][0].decode(errors="replace") if data[0][0] else "")
                gmail_uid = uid_match.group(1) if uid_match else uid
                
                message_id = msg.get("Message-ID", "")
                if message_id in existing_ids:
                    continue
                
                from_header = msg.get("From", "")
                from_name, from_addr = email.utils.parseaddr(from_header)
                from_name = decode_header_value(from_name)
                
                body = extract_body(msg)
                attachments = extract_attachments(msg)
                
                results.append({
                    "message_id": message_id,
                    "uid": gmail_uid,
                    "from": from_addr or from_header,
                    "from_name": from_name,
                    "subject": decode_header_value(msg.get("Subject", "")),
                    "date": parse_date(msg),
                    "body_text": body,
                    "body_preview": body[:preview_len] + ("..." if len(body) > preview_len else ""),
                    "has_attachments": len(attachments) > 0,
                    "attachment_names": attachments
                })
            except Exception as ex:
                log.warning("Failed to process email UID %s: %s", uid, ex)
                continue
        
        save_to_db(results)
        return {"total": len(results), "emails": results}
    finally:
        try:
            conn.logout()
        except Exception:
            pass

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Check emails via IMAP")
    parser.add_argument("--max", type=int, default=CONFIG["check"].get("max_emails", 20))
    parser.add_argument("--since", type=str, default=None, help="Date filter YYYY-MM-DD")
    args = parser.parse_args()
    
    result = fetch_emails(args.max, args.since)
    print(json.dumps(result, ensure_ascii=False, indent=2))
