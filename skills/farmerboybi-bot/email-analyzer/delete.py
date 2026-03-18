#!/usr/bin/env python3
"""
Email Delete Script - 执行删除操作
固化版 - 改动需 Wood 哥书面同意
"""

from email_analyzer import connect
import json
import argparse
from pathlib import Path


def delete_emails(uids_file, confirm=False):
    """
    执行邮件删除
    
    Args:
        uids_file: 包含待删除 UID 的 JSON 文件
        confirm: 必须为 True 才能执行删除
    """
    
    if not confirm:
        print("❌ 删除操作需要 --confirm 参数确认！")
        print("请确保已备份，然后重新运行：python delete.py --uids-file xxx.json --confirm")
        return False
    
    # 读取 UID 列表
    with open(uids_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    delete_uids = data.get('delete_uids', [])
    
    if not delete_uids:
        print("❌ 没有找到待删除的 UID")
        return False
    
    print(f"⚠️  准备删除 {len(delete_uids):,} 封邮件...")
    print("📧 连接邮箱...")
    
    server = connect()
    
    try:
        server.select_folder('INBOX')
        
        # 第 1 步：设置删除标记
        print(f"📍 设置删除标记...")
        server.set_flags(delete_uids, [b'\\Deleted'])
        print(f"✅ 已标记 {len(delete_uids):,} 封邮件")
        
        # 第 2 步：物理删除
        print(f"🗑️  执行物理删除 (expunge)...")
        server.expunge()
        print(f"✅ 删除完成！")
        
        # 验证
        stats = server.folder_status('INBOX', ['MESSAGES', 'UIDNEXT', 'UNSEEN'])
        print(f"\n📊 删除后邮箱状态：")
        print(f"  总邮件数：{stats.get(b'MESSAGES', 'N/A'):,}")
        print(f"  未读数：{stats.get(b'UNSEEN', 'N/A'):,}")
        
        return True
    
    except Exception as e:
        print(f"❌ 删除失败：{e}")
        return False
    
    finally:
        server.logout()
        print("\n✅ 断开连接")


def main():
    parser = argparse.ArgumentParser(description='Delete emails from 126.com')
    parser.add_argument('--uids-file', required=True, help='JSON file with UIDs to delete')
    parser.add_argument('--confirm', action='store_true', help='Confirm deletion (required)')
    
    args = parser.parse_args()
    
    success = delete_emails(args.uids_file, args.confirm)
    
    if not success:
        exit(1)


if __name__ == '__main__':
    main()
