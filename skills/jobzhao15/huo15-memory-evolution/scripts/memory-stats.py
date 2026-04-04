#!/usr/bin/env python3
"""
记忆访问追踪器
每次读取记忆时调用此脚本，记录访问次数和最后访问时间
"""
import json
import os
import sys
from datetime import datetime

def get_index_path():
    """获取 index.json 路径"""
    workspace = os.path.expanduser('~/.openclaw/workspace')
    return os.path.join(workspace, 'memory', 'index.json')

def load_index():
    """加载 index.json"""
    index_path = get_index_path()
    
    if not os.path.exists(index_path):
        # 创建新的 index
        return {
            'version': '1.0',
            'lastUpdated': datetime.now().isoformat(),
            'entries': []
        }
    
    try:
        with open(index_path, 'r') as f:
            return json.load(f)
    except:
        return {
            'version': '1.0',
            'lastUpdated': datetime.now().isoformat(),
            'entries': []
        }

def save_index(data):
    """保存 index.json"""
    index_path = get_index_path()
    data['lastUpdated'] = datetime.now().isoformat()
    
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    
    with open(index_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def record_access(memory_path, memory_type=None, description=None):
    """
    记录一次记忆访问
    
    Args:
        memory_path: 记忆文件的相对路径，如 "memory/user/test.md"
        memory_type: 可选，记忆类型
        description: 可选，记忆描述
    """
    index = load_index()
    
    # 查找或创建条目
    entry = None
    for e in index['entries']:
        if e.get('path') == memory_path:
            entry = e
            break
    
    if entry is None:
        # 新条目
        entry = {
            'path': memory_path,
            'type': memory_type or 'unknown',
            'description': description or '',
            'accessCount': 0,
            'firstAccessed': datetime.now().isoformat(),
            'lastAccessed': datetime.now().isoformat()
        }
        index['entries'].append(entry)
    
    # 更新访问统计
    entry['accessCount'] = entry.get('accessCount', 0) + 1
    entry['lastAccessed'] = datetime.now().isoformat()
    
    if memory_type:
        entry['type'] = memory_type
    if description:
        entry['description'] = description
    
    save_index(index)
    
    return entry

def get_stats():
    """获取记忆访问统计"""
    index = load_index()
    
    stats = {
        'totalMemories': len(index['entries']),
        'totalAccess': sum(e.get('accessCount', 0) for e in index['entries']),
        'topMemories': sorted(index['entries'], key=lambda x: x.get('accessCount', 0), reverse=True)[:5]
    }
    
    return stats

def print_stats():
    """打印统计信息"""
    stats = get_stats()
    
    print("📊 记忆访问统计")
    print("=" * 40)
    print(f"总记忆数: {stats['totalMemories']}")
    print(f"总访问次: {stats['totalAccess']}")
    print("")
    print("🔥 Top 5 最常访问的记忆:")
    
    for i, mem in enumerate(stats['topMemories'], 1):
        count = mem.get('accessCount', 0)
        path = mem.get('path', 'unknown')
        name = os.path.basename(path).replace('.md', '')
        print(f"  {i}. {name} - {count} 次")

def main():
    if len(sys.argv) < 2:
        # 无参数：打印统计
        print_stats()
        return
    
    command = sys.argv[1]
    
    if command == 'stats':
        print_stats()
    
    elif command == 'access' and len(sys.argv) >= 3:
        # 记录访问
        memory_path = sys.argv[2]
        memory_type = sys.argv[3] if len(sys.argv) >= 4 else None
        description = sys.argv[4] if len(sys.argv) >= 5 else None
        
        entry = record_access(memory_path, memory_type, description)
        print(f"✅ 记录访问: {memory_path}")
        print(f"   访问次数: {entry['accessCount']}")
    
    elif command == 'read' and len(sys.argv) >= 3:
        # 读取记忆并记录访问
        memory_path = sys.argv[2]
        
        # 获取完整路径
        workspace = os.path.expanduser('~/.openclaw/workspace')
        full_path = os.path.join(workspace, memory_path)
        
        if os.path.exists(full_path):
            entry = record_access(memory_path)
            print(f"✅ 已记录访问: {memory_path} (共 {entry['accessCount']} 次)")
        else:
            print(f"⚠️ 文件不存在: {memory_path}")
    
    else:
        print("用法:")
        print("  python memory-stats.py              # 打印统计")
        print("  python memory-stats.py stats          # 打印统计")
        print("  python memory-stats.py access <path> [type] [description]")
        print("  python memory-stats.py read <path>    # 读取记忆并记录访问")

if __name__ == '__main__':
    main()
