#!/usr/bin/env python3
# Copyright (c) 2026 思捷娅科技 (SJYKJ)
# License: MIT
"""SMTP 邮件发送（--dry-run 默认，需 --send 确认）"""

import smtplib
import json
import sys
import os
import sqlite3
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "email-index.db")
LOG_DIR = os.path.join(BASE_DIR, "logs")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "email-config.json")

os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "email-send.log"),
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("send-email")

CONFIG = json.load(open(CONFIG_PATH))

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

def send_email(to, subject, body, cc=None, dry_run=True, in_reply_to=None):
    user, password = load_credentials()
    config = CONFIG["smtp"]
    
    msg = MIMEMultipart("alternative")
    msg["From"] = user
    msg["To"] = to
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    if cc:
        msg["Cc"] = cc
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = in_reply_to
    
    msg.attach(MIMEText(body, "plain", "utf-8"))
    
    recipients = [to]
    if cc:
        recipients.extend([c.strip() for c in cc.split(",")])
    
    if dry_run:
        print(json.dumps({
            "mode": "dry-run",
            "to": to,
            "cc": cc or "",
            "subject": subject,
            "body_preview": body[:300] + ("..." if len(body) > 300 else ""),
            "in_reply_to": in_reply_to or "",
            "body_length": len(body)
        }, ensure_ascii=False, indent=2))
        log.info("[DRY-RUN] Email preview: to=%s subject=%s", to, subject)
        return {"status": "dry-run", "message_id": None}
    
    try:
        if config.get("ssl"):
            server = smtplib.SMTP_SSL(config["host"], config["port"])
        else:
            server = smtplib.SMTP(config["host"], config["port"])
            server.starttls()
        
        server.login(user, password)
        send_result = server.sendmail(user, recipients, msg.as_string())
        msg_id = msg["Message-ID"] or f"<sent-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}@gmail.com>"
        server.quit()
        
        # Record to DB
        record_sent(to, subject, body, in_reply_to)
        
        log.info("Email sent: to=%s subject=%s msg_id=%s", to, subject, msg_id)
        print(json.dumps({
            "status": "sent",
            "to": to,
            "subject": subject,
            "message_id": msg_id,
            "accepted": list(send_result.keys()) if send_result else recipients
        }, ensure_ascii=False, indent=2))
        return {"status": "sent", "message_id": msg_id}
        
    except smtplib.SMTPAuthenticationError as e:
        log.error("SMTP auth failed: %s", e)
        print(json.dumps({"error": "SMTP authentication failed. Check GMAIL_USER/GMAIL_PASS in ~/.openclaw/secrets/gmail.env"}))
        sys.exit(2)
    except Exception as e:
        log.error("SMTP send error: %s", e)
        print(json.dumps({"error": f"SMTP send failed: {e}"}))
        sys.exit(2)

def record_sent(to_addr, subject, body, in_reply_to):
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute(
            "INSERT INTO sent_emails (to_addr, subject, body, in_reply_to) VALUES (?,?,?,?)",
            (to_addr, subject, body, in_reply_to or "")
        )
        conn.commit()
        conn.close()
    except Exception as ex:
        log.warning("Failed to record sent email: %s", ex)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Send email via SMTP")
    parser.add_argument("--to", required=True, help="Recipient email")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", help="Email body text")
    parser.add_argument("--body-file", help="Read body from file")
    parser.add_argument("--cc", default="", help="CC recipients (comma-separated)")
    parser.add_argument("--in-reply-to", default="", help="In-Reply-To message ID")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview only (default)")
    parser.add_argument("--send", action="store_true", help="Actually send the email")
    args = parser.parse_args()
    
    body = args.body
    if args.body_file:
        with open(args.body_file) as f:
            body = f.read()
    if not body:
        print(json.dumps({"error": "No body provided. Use --body or --body-file"}))
        sys.exit(1)
    
    send_email(
        to=args.to,
        subject=args.subject,
        body=body,
        cc=args.cc or None,
        dry_run=not args.send,
        in_reply_to=args.in_reply_to or None
    )
