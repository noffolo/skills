#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 全局记忆集成模块
让 OpenClaw 在所有对话中自动使用知识库
"""

import sys
import json
from pathlib import Path

from .config import load_config, resolve_index_path
from .knowledge_core import KnowledgeSearcher


class GlobalMemory:
    """全局记忆管理器"""

    def __init__(self):
        self.config = load_config()
        self.searcher = KnowledgeSearcher(self.config)
        self.context_prefix = """【知识库上下文】
以下是与你当前问题相关的知识库内容，请优先参考这些信息回答：

"""
        self.context_suffix = """
---
请基于以上知识库内容回答用户问题。如果知识库中没有相关信息，请基于你的通用知识回答，但要在开头说明"知识库中没有找到相关内容"。
"""

    def get_context(self, query: str) -> str:
        """获取知识库上下文"""
        results = self.searcher.search(query)

        if not results:
            return ""

        context_parts = [self.context_prefix]

        for i, result in enumerate(results, 1):
            doc = result['document']
            matched_blocks = result['matched_blocks']

            context_parts.append(f"## {i}. {doc.get('title', '无标题')}")
            context_parts.append(f"来源：{doc.get('relative_path', doc.get('path', ''))}")
            context_parts.append("")

            if matched_blocks:
                context_parts.append("相关内容：")
                for block in matched_blocks[:2]:
                    context_parts.append(f"- *{block['title']}*：{block['preview']}...")
                context_parts.append("")

        context_parts.append(self.context_suffix)

        return "\n".join(context_parts)

    def should_inject(self, query: str) -> bool:
        """判断是否应该注入知识库上下文"""
        results = self.searcher.search(query)
        return len(results) > 0 and results[0]['score'] > 5

    def get_stats(self) -> dict:
        """获取统计信息"""
        return self.searcher.get_stats()


def main():
    """CLI 入口"""
    if len(sys.argv) < 2:
        print("用法：")
        print("  global_memory.py context <查询>  # 获取上下文")
        print("  global_memory.py should <查询>   # 判断是否注入")
        print("  global_memory.py stats          # 查看统计")
        sys.exit(1)

    memory = GlobalMemory()
    command = sys.argv[1]

    if command == 'context':
        if len(sys.argv) < 3:
            print("错误：需要提供查询词")
            sys.exit(1)
        query = sys.argv[2]
        context = memory.get_context(query)
        print(context if context else "# 无相关知识库内容")

    elif command == 'should':
        if len(sys.argv) < 3:
            print("错误：需要提供查询词")
            sys.exit(1)
        query = sys.argv[2]
        should = memory.should_inject(query)
        print(f"应该注入：{should}")

    elif command == 'stats':
        stats = memory.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    else:
        print(f"未知命令：{command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
