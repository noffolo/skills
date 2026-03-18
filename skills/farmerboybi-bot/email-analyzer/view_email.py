#!/usr/bin/env python3
"""
View Specific Email Content - 查看指定邮件完整内容
"""

from email_analyzer import connect
import argparse
from email.parser import BytesParser
from email.policy import default


def fetch_full_email(server, uid):
    """
    获取邮件完整内容（包括正文）
    """
    # 获取完整 RFC822 邮件
    messages = server.fetch([uid], ['RFC822'])
    
    if uid not in messages:
        return None
    
    raw_email = messages[uid][b'RFC822']
    
    # 解析邮件
    parser = BytesParser(policy=default)
    email_obj = parser.parsebytes(raw_email)
    
    return {
        'subject': email_obj.get('Subject', '无主题'),
        'from': email_obj.get('From', '未知'),
        'to': email_obj.get('To', '未知'),
        'date': email_obj.get('Date', '未知'),
        'body': extract_body(email_obj)
    }


def extract_body(email_obj):
    """
    提取邮件正文内容
    """
    body = ""
    
    if email_obj.is_multipart():
        # 多部分邮件，优先获取 text/html 或 text/plain
        for part in email_obj.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get_content_disposition())
            
            # 跳过附件
            if 'attachment' in content_disposition:
                continue
            
            if content_type == 'text/plain':
                try:
                    body = part.get_content()
                    break
                except:
                    pass
            elif content_type == 'text/html' and not body:
                try:
                    body = part.get_content()
                except:
                    pass
    else:
        # 单部分邮件
        try:
            body = email_obj.get_content()
        except:
            body = "无法提取正文"
    
    return body


def main():
    parser = argparse.ArgumentParser(description='查看指定邮件内容')
    parser.add_argument('--uid', type=int, required=True, help='邮件 UID')
    
    args = parser.parse_args()
    
    print(f"📧 获取邮件 UID: {args.uid}")
    print()
    
    server = connect()
    
    try:
        server.select_folder('INBOX')
        
        email_data = fetch_full_email(server, args.uid)
        
        if not email_data:
            print("❌ 无法获取邮件内容")
            return
        
        print("=" * 80)
        print(f"主题：{email_data['subject']}")
        print(f"发件人：{email_data['from']}")
        print(f"收件人：{email_data['to']}")
        print(f"日期：{email_data['date']}")
        print("=" * 80)
        print()
        print("📄 正文内容：")
        print("-" * 80)
        print(email_data['body'][:3000])  # 限制长度
        print()
    
    finally:
        server.logout()


if __name__ == '__main__':
    main()
