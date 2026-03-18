#!/usr/bin/env python3
"""
Selective Email Delete - 选择性删除邮件
"""

from email_analyzer import connect, DELETE_KW, KEEP_KW
import json
import argparse


def select_emails_for_deletion(analysis_file, categories_to_delete):
    """
    从分析报告中选择指定类别的邮件 UID 进行删除
    
    Args:
        analysis_file: 分析报告 JSON 文件
        categories_to_delete: 要删除的类别列表，如 ['temu_promo', 'linkedin']
    
    Returns:
        list: 待删除的 UID 列表
    """
    with open(analysis_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    delete_uids = data.get('delete_uids', [])
    
    # 注意：这里需要重新获取邮件详情来判断类别
    # 简化处理：直接返回所有 delete_uids，让用户确认
    
    print(f"📊 分析报告：{data.get('date_range', '未知')}")
    print(f"总建议删除：{len(delete_uids)} 封")
    print(f"本次选择删除类别：{categories_to_delete}")
    print()
    
    # ⚠️ 注意：需要重新连接 IMAP 获取每封邮件的类别
    # 这里简化处理，返回全部 delete_uids
    # 实际应该根据主题/发件人筛选
    
    return delete_uids


def main():
    parser = argparse.ArgumentParser(description='选择性删除邮件')
    parser.add_argument('--analysis-file', required=True, help='分析报告 JSON 文件')
    parser.add_argument('--categories', nargs='+', required=True, help='要删除的类别，如 temu_promo linkedin')
    parser.add_argument('--confirm', action='store_true', help='确认删除')
    
    args = parser.parse_args()
    
    print(f"🗑️  选择性删除邮件")
    print(f"目标类别：{', '.join(args.categories)}")
    print()
    
    # 连接邮箱
    server = connect()
    
    try:
        server.select_folder('INBOX')
        
        # 读取分析报告
        with open(args.analysis_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        delete_uids = data.get('delete_uids', [])
        
        if not delete_uids:
            print("❌ 没有找到待删除的邮件")
            return
        
        # 获取邮件详情并筛选
        messages = server.fetch(delete_uids, [
            'BODY.PEEK[HEADER.FIELDS (SUBJECT FROM)]'
        ])
        
        target_uids = []
        
        for uid in delete_uids:
            if uid not in messages:
                continue
            
            header = messages[uid].get(
                b'BODY[HEADER.FIELDS (SUBJECT FROM)]', 
                b''
            ).decode('utf-8', errors='ignore').lower()
            
            should_delete = False
            category = 'unknown'
            
            # 根据类别判断
            if 'temu' in header:
                if 'temu_promo' in args.categories:
                    should_delete = True
                    category = 'temu_promo'
            elif 'linkedin' in header:
                if 'linkedin' in args.categories:
                    should_delete = True
                    category = 'linkedin'
            
            if should_delete:
                target_uids.append(uid)
                print(f"✅ 选中：UID {uid} - {category}")
        
        print()
        print(f"📊 选中 {len(target_uids)} 封邮件待删除")
        
        if not target_uids:
            print("❌ 没有选中任何邮件")
            return
        
        if not args.confirm:
            print()
            print("⚠️  请输入 'yes' 确认删除：")
            confirm = input("> ")
            if confirm != 'yes':
                print("❌ 删除已取消")
                return
        
        # 执行删除
        print()
        print("🗑️  执行删除...")
        server.set_flags(target_uids, [b'\\Deleted'])
        server.expunge()
        
        print(f"✅ 成功删除 {len(target_uids)} 封邮件！")
        
        # 验证
        stats = server.folder_status('INBOX', ['MESSAGES', 'UNSEEN'])
        print(f"\n📊 删除后邮箱状态：")
        print(f"  总邮件数：{stats.get(b'MESSAGES', 'N/A'):,}")
        print(f"  未读数：{stats.get(b'UNSEEN', 'N/A'):,}")
    
    finally:
        server.logout()
        print("\n✅ 断开连接")


if __name__ == '__main__':
    main()
