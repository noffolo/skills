#!/usr/bin/env python3
"""
Email Verify Script - 验证删除结果
固化版 - 改动需 Wood 哥书面同意
"""

from email_analyzer import connect
import json
import argparse
from pathlib import Path


def verify_deletion():
    """验证删除后的邮箱状态"""
    
    print("📊 验证删除结果...")
    print("📧 连接邮箱...")
    
    server = connect()
    
    try:
        server.select_folder('INBOX')
        
        # 获取邮箱状态
        stats = server.folder_status('INBOX', ['MESSAGES', 'UIDNEXT', 'UNSEEN', 'RECENT'])
        
        print(f"\n✅ 邮箱验证完成！")
        print(f"\n📊 当前邮箱状态：")
        print(f"  总邮件数：{stats.get(b'MESSAGES', 'N/A'):,}")
        print(f"  未读邮件：{stats.get(b'UNSEEN', 'N/A'):,}")
        print(f"  新邮件：{stats.get(b'RECENT', 'N/A'):,}")
        print(f"  UID 下一个：{stats.get(b'UIDNEXT', 'N/A')}")
        
        # 检查是否有标记删除但未 expunge 的邮件
        server.search(b'DELETED')
        deleted_count = len(server.search(b'DELETED'))
        
        if deleted_count > 0:
            print(f"\n⚠️  警告：有 {deleted_count:,} 封邮件已标记删除但未物理删除")
            print("建议运行 expunge 清理")
        else:
            print(f"\n✅ 没有残留的已删除标记邮件")
        
        return stats
    
    except Exception as e:
        print(f"❌ 验证失败：{e}")
        return None
    
    finally:
        server.logout()
        print("\n✅ 断开连接")


def main():
    verify_deletion()


if __name__ == '__main__':
    main()
