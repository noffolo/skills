#!/usr/bin/env python3
"""
WeChat Fetch - 微信公众号文章抓取工具
使用 OpenClaw 持久化浏览器上下文，复用已登录 Cookie
支持无头模式，稳定可靠

使用方法:
    python3 wechat_fetch.py <URL> -o ./article.md
"""

import sys
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime


class WeChatFetcher:
    """微信文章抓取器"""
    
    def __init__(self, timeout=30):
        self.timeout = timeout
        # OpenClaw 浏览器数据目录
        self.user_data_dir = "/home/admin/.openclaw/browser/openclaw/user-data"
    
    def fetch(self, url, output_file=None):
        """
        抓取微信文章
        
        Args:
            url: 微信文章 URL
            output_file: 输出文件路径（可选）
        
        Returns:
            dict: 文章数据
        """
        print(f"开始抓取：{url}")
        
        with sync_playwright() as p:
            # 使用持久化上下文，复用已登录 Cookie
            print("启动持久化浏览器上下文...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=True,
                viewport={"width": 1920, "height": 1080},
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox'
                ]
            )
            
            page = browser.new_page()
            print(f"正在加载页面：{url}")
            page.goto(url, wait_until='domcontentloaded', timeout=self.timeout * 1000)
            
            # 等待内容加载
            print("等待内容加载...")
            page.wait_for_selector('#js_content', state='attached', timeout=10000)
            page.wait_for_timeout(3000)
            
            # 提取内容
            title = page.title()
            content = page.inner_html('#js_content')
            
            # 构建文章数据
            article = {
                "title": title,
                "url": url,
                "content": content,
                "html_content": content,
                "publish_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nickname": "",
                "images": []
            }
            
            browser.close()
            
            # 保存文件
            if output_file:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 转换为 Markdown
                markdown = article.to_markdown() if hasattr(article, 'to_markdown') else f"# {title}\n\n{content}\n\n原文链接：{url}"
                output_path.write_text(markdown, encoding='utf-8')
                print(f"✅ 已保存到：{output_path}")
            
            return article


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="微信文章抓取工具")
    parser.add_argument("url", help="微信文章 URL")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("-t", "--timeout", type=int, default=30, help="超时时间（秒）")
    
    args = parser.parse_args()
    
    fetcher = WeChatFetcher(timeout=args.timeout)
    article = fetcher.fetch(args.url, args.output)
    
    if article:
        print("\n" + "="*60)
        print(f"✅ 抓取成功！")
        print(f"标题：{article['title']}")
        print(f"内容长度：{len(article['content'])}")
        print("="*60)
    else:
        print("\n❌ 抓取失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
