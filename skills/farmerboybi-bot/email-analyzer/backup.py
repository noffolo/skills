#!/usr/bin/env python3
"""
Email Backup Script - 删除前备份
固化版 - 改动需 Wood 哥书面同意
"""

import json
from datetime import datetime
from pathlib import Path
import argparse


def backup_uids(uids_file, output_file, batch_id=None):
    """备份待删除的 UID 列表"""
    
    # 读取 UID 列表
    with open(uids_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    delete_uids = data.get('delete_uids', [])
    
    if not delete_uids:
        print("❌ 没有找到待删除的 UID")
        return False
    
    # 生成备份文件
    backup = {
        'backup_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'batch_id': batch_id or data.get('batch_id', 'unknown'),
        'date_range': data.get('date_range', 'unknown'),
        'delete_count': len(delete_uids),
        'uids': delete_uids
    }
    
    output_path = Path(output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(backup, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 备份完成！")
    print(f"📊 备份内容：{len(delete_uids):,} 封邮件 UID")
    print(f"💾 备份文件：{output_path}")
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Backup UIDs before deletion')
    parser.add_argument('--uids-file', required=True, help='Input JSON file with UIDs')
    parser.add_argument('--output', required=True, help='Output backup file')
    parser.add_argument('--batch', help='Batch ID (optional)')
    
    args = parser.parse_args()
    
    success = backup_uids(args.uids_file, args.output, args.batch)
    
    if not success:
        exit(1)


if __name__ == '__main__':
    main()
