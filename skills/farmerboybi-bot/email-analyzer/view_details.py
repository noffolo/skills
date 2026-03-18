#!/usr/bin/env python3
"""
Email Detail Viewer - 查看邮件详细内容
"""

from email_analyzer import connect
import json
from datetime import datetime
import argparse


def fetch_email_details(server, uids, label="邮件"):
    """
    获取邮件详细信息（主题、发件人、日期）
    """
    print(f"\n📧 {label}详情 ({len(uids)} 封):\n")
    print(f"{'序号':<4} {'主题':<50} {'发件人':<30} {'日期'}")
    print("-" * 120)
    
    # 批量获取邮件头
    messages = server.fetch(uids, [
        'BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)]'
    ])
    
    for i, uid in enumerate(uids, 1):
        if uid not in messages:
            print(f"{i:<4} [无法获取 UID: {uid}]")
            continue
        
        header = messages[uid].get(
            b'BODY[HEADER.FIELDS (SUBJECT FROM DATE)]', 
            b''
        ).decode('utf-8', errors='ignore')
        
        # 解析头部
        subject = "无主题"
        sender = "未知"
        date = "未知"
        
        for line in header.split('\n'):
            line_lower = line.lower()
            if line_lower.startswith('subject:'):
                subject = line[8:].strip()
            elif line_lower.startswith('from:'):
                sender = line[5:].strip()
            elif line_lower.startswith('date:'):
                date = line[5:].strip()
        
        # 截断过长的主题
        if len(subject) > 48:
            subject = subject[:45] + "..."
        if len(sender) > 28:
            sender = sender[:25] + "..."
        
        print(f"{i:<4} {subject:<50} {sender:<30} {date}")
    
    print()


def main():
    parser = argparse.ArgumentParser(description='查看邮件详细内容')
    parser.add_argument('--analysis-file', required=True, help='分析报告 JSON 文件')
    
    args = parser.parse_args()
    
    # 读取分析报告
    with open(args.analysis_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    delete_uids = data.get('delete_uids', [])
    keep_uids = data.get('keep_uids', [])
    
    print(f"📊 邮件详细报告")
    print(f"日期范围：{data.get('date_range', '未知')}")
    print(f"总邮件：{data.get('total', 0)} 封")
    print()
    
    # 连接邮箱
    server = connect()
    
    try:
        # 选择收件箱（必须！）
        server.select_folder('INBOX')
        
        # 获取删除邮件详情
        if delete_uids:
            fetch_email_details(server, delete_uids, "🗑️ 建议删除")
        
        # 获取保留邮件详情
        if keep_uids:
            fetch_email_details(server, keep_uids, "✅ 建议保留")
    
    finally:
        server.logout()
        print("✅ 断开连接")


if __name__ == '__main__':
    main()
