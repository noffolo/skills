#!/usr/bin/env python3
"""
Email Analyzer Core Module - 126.com IMAP Client
固化版 - 改动需 Wood 哥书面同意

✅ 2026-03-15 修复：日期范围逻辑错误
- 原错误：SINCE 15-Mar-2026 BEFORE 15-Mar-2026（矛盾，返回 0）
- 修复后：SINCE 15-Mar-2026 BEFORE 16-Mar-2026（包含当天）
"""

from imapclient import IMAPClient
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import sys

# 🔒 固化配置（禁止修改）
CONFIG = {
    "server": "imap.126.com",
    "port": 993,
    "ssl": True,
    "email": "biqiang@126.com",
    "password": "WUEw8qhBwjzpUAZW",
    "timeout": 60,
}

# 📋 固化关键词列表
DELETE_KW = [
    'sale', 'discount', 'promo', 'deal', 'offer', 'clearance',
    'newsletter', 'subscription', 'weekly', 'monthly', 'unsubscribe',
    'notification', 'alert', 'update', 'reminder', 'verification',
    'ecobee', 'rachio', 'nest', 'ring', 'smart home',
    'hoa', 'community', 'meeting', 'election', 'board',
    'temu', 'shein', 'wish', 'aliexpress', 'sponsor', 'ad'
]

KEEP_KW = [
    'forsyth', 'school', 'lhs', 'teacher', 'student',
    'chase', 'visa', 'statement', 'bank', 'credit card',
    'amazon', 'order', 'shipping', 'tracking', 'delivery',
    'uber', 'lyft', 'flight', 'hotel', 'airline', 'delta',
    'google', 'icloud', 'dropbox', 'onedrive', 'apple',
    'insurance', 'medical', 'health', 'doctor', 'hospital',
    'tax', 'irs', 'government', 'utility', 'power', 'water',
    'receipt', 'invoice', 'warranty', 'contract', 'lease'
]


def connect():
    """连接到 126 邮箱 IMAP"""
    print(f"📧 连接到 {CONFIG['server']}...")
    
    server = IMAPClient(
        CONFIG['server'],
        ssl=CONFIG['ssl'],
        port=CONFIG['port'],
        timeout=CONFIG['timeout']
    )
    
    # ⚠️ ID 命令必须用 ASCII！
    server.id_({
        "name": "Email-Analyzer",
        "version": "1.0",
        "contact": CONFIG['email']
    })
    
    server.login(CONFIG['email'], CONFIG['password'])
    print("✅ 登录成功")
    
    return server


def format_imap_date(date_str):
    """
    将 YYYY-MM-DD 格式转换为 IMAP 日期格式 (DD-MMM-YYYY)
    例如：2021-02-26 → 26-Feb-2021
    """
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return dt.strftime('%d-%b-%Y')


def get_next_day(date_str):
    """
    获取给定日期的下一天
    例如：2026-03-15 → 2026-03-16
    
    ✅ 新增函数：修复日期范围逻辑
    """
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    next_dt = dt + timedelta(days=1)
    return next_dt.strftime('%Y-%m-%d')


def analyze_date_range(server, start_date, end_date):
    """
    分析指定日期范围的邮件
    
    Args:
        server: IMAPClient 实例
        start_date: 开始日期 (YYYY-MM-DD)
        end_date: 结束日期 (YYYY-MM-DD)
    
    Returns:
        dict: 分析报告
    
    ✅ 2026-03-15 修复：日期范围逻辑错误
    - 原错误：SINCE 15-Mar-2026 BEFORE 15-Mar-2026（矛盾）
    - 修复后：SINCE 15-Mar-2026 BEFORE 16-Mar-2026（包含当天）
    """
    # 转换日期格式
    start_imap = format_imap_date(start_date)
    # ✅ 修复：end_date 需要 +1 天，才能包含 end_date 当天
    end_date_next = get_next_day(end_date)
    end_imap = format_imap_date(end_date_next)
    
    print(f"📊 分析日期范围：{start_date} ~ {end_date}")
    print(f"IMAP 格式：{start_imap} ~ {end_imap} (BEFORE {end_imap} 包含 {end_date})")
    
    # 选择收件箱
    server.select_folder('INBOX')
    
    # ✅ 修复后的搜索条件
    search_criteria = f'(SINCE {start_imap} BEFORE {end_imap})'
    print(f"搜索条件：{search_criteria}")
    
    uids = server.search(search_criteria)
    
    print(f"找到 {len(uids)} 封邮件")
    
    # 分类统计
    delete_uids = []
    keep_uids = []
    other_uids = []
    
    categories = {
        'temu_promo': 0,
        'smart_home': 0,
        'hoa_community': 0,
        'newsletter': 0,
        'school': 0,
        'finance': 0,
        'shopping': 0,
        'other': 0
    }
    
    # 批量获取邮件头（每次 100 封）
    batch_size = 100
    for i in range(0, len(uids), batch_size):
        batch = uids[i:i+batch_size]
        
        # 获取邮件头信息
        messages = server.fetch(batch, ['BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)]'])
        
        for uid in batch:
            if uid not in messages:
                continue
            
            header_data = messages[uid]
            header = header_data.get(b'BODY[HEADER.FIELDS (SUBJECT FROM DATE)]', b'').decode('utf-8', errors='ignore')
            
            # 提取主题和发件人
            subject = ''
            from_line = ''
            for line in header.split('\r\n'):
                if line.lower().startswith('subject:'):
                    subject = line[8:].strip()
                elif line.lower().startswith('from:'):
                    from_line = line[5:].strip()
            
            # 转小写匹配
            subject_lower = subject.lower()
            from_lower = from_line.lower()
            combined = subject_lower + ' ' + from_lower
            
            # 分类判断
            is_delete = False
            category = 'other'
            
            # 删除关键词匹配
            for kw in DELETE_KW:
                if kw in combined:
                    is_delete = True
                    
                    # 确定分类
                    if 'temu' in combined or 'shein' in combined or 'wish' in combined or 'aliexpress' in combined:
                        category = 'temu_promo'
                    elif 'ecobee' in combined or 'rachio' in combined or 'nest' in combined or 'ring' in combined or 'smart home' in combined:
                        category = 'smart_home'
                    elif 'hoa' in combined or 'community' in combined or 'meeting' in combined or 'election' in combined or 'board' in combined:
                        category = 'hoa_community'
                    elif 'newsletter' in combined or 'subscription' in combined or 'weekly' in combined or 'monthly' in combined:
                        category = 'newsletter'
                    elif 'sale' in combined or 'discount' in combined or 'promo' in combined or 'deal' in combined or 'offer' in combined:
                        category = 'shopping'
                    else:
                        category = 'other'
                    
                    break
            
            # 保留关键词匹配
            if not is_delete:
                for kw in KEEP_KW:
                    if kw in combined:
                        is_delete = False
                        category = 'other'
                        break
            
            # 归类
            if is_delete:
                delete_uids.append(uid)
                categories[category] = categories.get(category, 0) + 1
            else:
                keep_uids.append(uid)
                categories['other'] = categories.get('other', 0) + 1
    
    # 生成报告
    total = len(uids)
    delete_count = len(delete_uids)
    keep_count = len(keep_uids)
    
    report = {
        'batch_id': datetime.now().strftime('%Y%m%d_%H%M%S'),
        'date_range': f'{start_date} ~ {end_date}',
        'total': total,
        'delete_count': delete_count,
        'keep_count': keep_count,
        'other_count': 0,
        'delete_uids': delete_uids,
        'keep_uids': keep_uids,
        'other_uids': [],
        'categories': categories,
        'delete_percentage': round(delete_count / total * 100, 2) if total > 0 else 0
    }
    
    return report


def print_report(report):
    """打印分析报告"""
    print("\n📊 邮件分析报告\n")
    print(f"批次：{report['batch_id']}")
    print(f"日期范围：{report['date_range']}")
    print(f"总邮件数：{report['total']} 封\n")
    
    print(f"建议删除：{report['delete_count']} 封 ({report['delete_percentage']}%)")
    for cat, count in report['categories'].items():
        if count > 0:
            print(f"  - {cat}: {count} 封")
    
    print(f"\n建议保留：{report['keep_count']} 封")
    print(f"其他/不确定：{report['other_count']} 封")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='126 邮箱邮件分析工具')
    parser.add_argument('--mode', choices=['analyze', 'backup', 'delete', 'verify'], default='analyze',
                        help='操作模式')
    parser.add_argument('--start-date', help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--uids-file', help='UID 文件路径')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--confirm', action='store_true', help='确认删除操作')
    
    args = parser.parse_args()
    
    if args.mode == 'analyze':
        if not args.start_date or not args.end_date:
            print("❌ 分析模式需要 --start-date 和 --end-date 参数")
            sys.exit(1)
        
        # 连接
        server = connect()
        
        try:
            # 分析
            report = analyze_date_range(server, args.start_date, args.end_date)
            
            # 打印报告
            print_report(report)
            
            # 保存 JSON
            output_path = Path(args.output) if args.output else Path(f"/Users/lobster/.openclaw/workspace/analysis_{report['batch_id']}.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 报告已保存到：{output_path}")
            print("\n⚠️ 请 Wood 哥确认后回复'删除'执行删除操作！")
            
        finally:
            print("\n✅ 断开连接")
            server.logout()
    
    else:
        print(f"❌ 未知或未实现模式：{args.mode}")
        sys.exit(1)


if __name__ == '__main__':
    main()
