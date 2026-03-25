#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书创作者评论引流 - 主入口
策略：在创作者最新作品下评论，引导对方关注或查看私信
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from comment_bot import CommentBot, asyncio

def main():
    bot = CommentBot()
    asyncio.run(bot.run())

if __name__ == "__main__":
    main()
