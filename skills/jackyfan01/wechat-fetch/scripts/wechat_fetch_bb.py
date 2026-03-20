#!/usr/bin/env python3
"""
WeChat Fetch - bb-browser 版本
使用 bb-browser + OpenClaw 浏览器抓取微信文章
优势：使用真实浏览器登录态，不会被反爬机制拦截
"""

import sys
import subprocess
import json
from pathlib import Path


def fetch_with_bb_browser(url: str, output_file: str = None):
    """
    使用 bb-browser 抓取微信文章
    
    Args:
        url: 微信文章 URL
        output_file: 输出文件路径（可选）
    
    Returns:
        dict: 文章数据
    """
    print(f"开始抓取：{url}")
    print("使用 bb-browser + OpenClaw 浏览器...")
    
    # 步骤 1: 打开文章
    print("\n[1/3] 打开文章...")
    result = subprocess.run(
        ["bb-browser", "open", url, "--openclaw"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ 打开失败：{result.stderr}")
        return None
    
    # 解析 Tab ID
    tab_id = None
    for line in result.stdout.split('\n'):
        if 'Tab ID:' in line:
            tab_id = line.split(':')[1].strip()
            break
    
    if not tab_id:
        print("❌ 未获取到 Tab ID")
        return None
    
    print(f"✅ 已打开，Tab ID: {tab_id}")
    
    # 步骤 2: 等待页面加载
    print("\n[2/3] 等待页面加载...")
    import time
    time.sleep(2)
    
    # 步骤 3: 提取内容
    print("\n[3/3] 提取文章内容...")
    result = subprocess.run(
        ["bb-browser", "eval", 
         "document.querySelector('.rich_media_content').innerText",
         "--openclaw"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ 提取失败：{result.stderr}")
        return None
    
    content = result.stdout.strip()
    
    # 提取标题
    title_result = subprocess.run(
        ["bb-browser", "eval",
         "document.querySelector('h1#activity-name').innerText",
         "--openclaw"],
        capture_output=True,
        text=True
    )
    title = title_result.stdout.strip() if title_result.returncode == 0 else "未知标题"
    
    # 构建文章数据
    article = {
        "title": title,
        "url": url,
        "content": content,
        "source": "bb-browser"
    }
    
    # 保存文件
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存为 Markdown
        md_content = f"# {title}\n\n{content}\n\n原文链接：{url}"
        output_path.write_text(md_content, encoding='utf-8')
        print(f"\n✅ 已保存到：{output_path}")
    
    return article


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="使用 bb-browser 抓取微信文章")
    parser.add_argument("url", help="微信文章 URL")
    parser.add_argument("-o", "--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    article = fetch_with_bb_browser(args.url, args.output)
    
    if article:
        print("\n" + "="*60)
        print(f"标题：{article['title']}")
        print(f"链接：{article['url']}")
        print(f"字数：{len(article['content'])}")
        print("="*60)
    else:
        sys.exit(1)
