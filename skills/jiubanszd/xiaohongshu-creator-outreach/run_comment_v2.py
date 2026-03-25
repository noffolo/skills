#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书创作者评论引流脚本 - 简化版
"""

import pandas as pd
import json
import time
import random
import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright, expect

# 配置
COOKIE_FILE = ".xiaohongshu_cookies.json"
INPUT_EXCEL = "xiaohongshu_ai_creators.xlsx"
OUTPUT_DIR = "output"
COMMENT_TEMPLATE = "内容很棒！对你的AI作品很感兴趣，已发私信～"
MIN_DELAY = 3
MAX_DELAY = 8
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"


def load_cookies():
    """加载Cookie"""
    try:
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] 加载Cookie失败: {e}")
        return None


def load_creators():
    """读取创作者列表"""
    try:
        df = pd.read_excel(INPUT_EXCEL)
        print(f"[INFO] 成功读取 {len(df)} 位创作者信息")
        return df
    except Exception as e:
        print(f"[ERROR] 读取Excel失败: {e}")
        return None


def post_comment_simple(page, note_url, comment_text):
    """简化的评论函数"""
    try:
        print(f"[INFO] 访问作品页...")
        page.goto(note_url, wait_until="domcontentloaded", timeout=30000)
        
        # 等待页面加载
        print("[INFO] 等待页面加载...")
        time.sleep(5)
        
        # 尝试找到并点击评论输入区域
        # 通常评论框初始状态是一个占位符或按钮
        print("[INFO] 查找评论输入区域...")
        
        # 首先尝试找到包含placeholder的输入框
        try:
            # 查找评论相关的文本
            comment_placeholders = ['说点什么', '评论', '写评论', '发表你的评论']
            found = False
            
            for placeholder in comment_placeholders:
                try:
                    # 尝试通过placeholder查找
                    textarea = page.locator(f'textarea[placeholder*="{placeholder}"]').first
                    if textarea.is_visible(timeout=3000):
                        print(f"[INFO] 找到评论框 (placeholder: {placeholder})")
                        textarea.click()
                        textarea.fill(comment_text)
                        time.sleep(1)
                        textarea.press("Enter")
                        time.sleep(2)
                        return True, "评论成功"
                except:
                    pass
            
            # 如果没找到，尝试点击"说点什么"等文字按钮
            for text in comment_placeholders:
                try:
                    btn = page.get_by_text(text, exact=False).first
                    if btn.is_visible(timeout=2000):
                        print(f"[INFO] 点击 '{text}' 按钮")
                        btn.click()
                        time.sleep(2)
                        
                        # 点击后查找输入框
                        textarea = page.locator('textarea, div[contenteditable="true"]').first
                        if textarea.is_visible(timeout=3000):
                            print("[INFO] 找到评论输入框")
                            textarea.fill(comment_text)
                            time.sleep(1)
                            
                            # 查找发送按钮
                            send_btn = page.get_by_text("发送", exact=False).first
                            if send_btn.is_visible(timeout=2000):
                                send_btn.click()
                            else:
                                textarea.press("Enter")
                            
                            time.sleep(2)
                            return True, "评论成功"
                except:
                    pass
            
            # 如果还是没找到，尝试通用的方法
            print("[INFO] 尝试通用方法查找...")
            
            # 滚动到页面底部找评论区
            for i in range(3):
                page.evaluate("window.scrollBy(0, 500)")
                time.sleep(1)
            
            # 查找所有可能的输入框
            inputs = page.locator('textarea, div[contenteditable]').all()
            print(f"[INFO] 找到 {len(inputs)} 个可能的输入框")
            
            for inp in inputs:
                try:
                    if inp.is_visible():
                        inp.click()
                        time.sleep(1)
                        inp.fill(comment_text)
                        time.sleep(1)
                        inp.press("Enter")
                        time.sleep(2)
                        return True, "评论成功(通用方法)"
                except:
                    continue
            
            return False, "未找到可交互的评论框"
            
        except Exception as e:
            return False, f"评论过程出错: {e}"
        
    except Exception as e:
        print(f"[ERROR] 发表评论失败: {e}")
        return False, str(e)


def save_progress(results, progress_file):
    """保存进度"""
    try:
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"[INFO] 进度已保存")
    except Exception as e:
        print(f"[ERROR] 保存进度失败: {e}")


def save_results_to_excel(results, output_file):
    """保存结果到Excel"""
    try:
        df = pd.DataFrame(results)
        df.to_excel(output_file, index=False)
        print(f"[INFO] Excel已保存: {output_file}")
    except Exception as e:
        print(f"[ERROR] 保存Excel失败: {e}")


def main():
    """主函数"""
    print("=" * 50)
    print("小红书创作者评论引流")
    print("=" * 50)
    
    # 加载Cookie
    cookies = load_cookies()
    if not cookies:
        print("[ERROR] Cookie加载失败")
        return
    
    # 读取创作者列表
    creators_df = load_creators()
    if creators_df is None or len(creators_df) == 0:
        print("[ERROR] 没有创作者数据")
        return
    
    print(f"[INFO] 共 {len(creators_df)} 位创作者\n")
    
    # 准备结果列表
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    progress_file = os.path.join(OUTPUT_DIR, "comment_progress.json")
    output_file = os.path.join(OUTPUT_DIR, f"comment_{timestamp}.xlsx")
    
    # 启动Playwright
    with sync_playwright() as p:
        try:
            # 启动浏览器
            browser = p.chromium.launch(
                headless=False,
                executable_path=CHROME_PATH,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = browser.new_context(viewport={'width': 1280, 'height': 900})
            context.add_cookies(cookies)
            print("[INFO] Cookie已加载")
            
            page = context.new_page()
            
            # 验证登录状态
            print("[INFO] 检查登录状态...")
            page.goto("https://www.xiaohongshu.com", wait_until="domcontentloaded", timeout=30000)
            time.sleep(5)
            
            # 遍历创作者
            for idx, row in creators_df.iterrows():
                user_id = str(row.get('创作者ID', ''))
                username = str(row.get('创作者名称', ''))
                user_link = str(row.get('主页链接', ''))
                note_link = str(row.get('视频链接', ''))
                
                print(f"\n[{idx+1}/{len(creators_df)}] 处理: {username}")
                
                result = {
                    '创作者ID': user_id,
                    '创作者名称': username,
                    '主页链接': user_link,
                    '作品链接': note_link if note_link != 'nan' else '',
                    '评论内容': COMMENT_TEMPLATE,
                    '评论状态': '待评论',
                    '评论时间': '',
                    '备注': ''
                }
                
                # 检查视频链接
                if not note_link or note_link == 'nan' or pd.isna(note_link):
                    result['评论状态'] = '评论失败'
                    result['备注'] = '无作品链接'
                    results.append(result)
                    save_progress(results, progress_file)
                    continue
                
                # 发表评论
                try:
                    success, msg = post_comment_simple(page, note_link, COMMENT_TEMPLATE)
                    if success:
                        result['评论状态'] = '已评论'
                        result['评论时间'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        result['评论状态'] = '评论失败'
                    result['备注'] = msg
                except Exception as e:
                    result['评论状态'] = '评论失败'
                    result['备注'] = f"异常: {e}"
                
                results.append(result)
                save_progress(results, progress_file)
                
                # 随机延迟
                delay = random.randint(MIN_DELAY, MAX_DELAY)
                print(f"[INFO] 等待 {delay} 秒...")
                time.sleep(delay)
            
            browser.close()
            
        except Exception as e:
            print(f"[ERROR] 浏览器操作失败: {e}")
    
    # 保存最终结果
    save_results_to_excel(results, output_file)
    save_progress(results, progress_file)
    
    # 统计
    success_count = sum(1 for r in results if r['评论状态'] == '已评论')
    fail_count = sum(1 for r in results if r['评论状态'] == '评论失败')
    
    print("\n" + "=" * 50)
    print("任务完成!")
    print(f"总计: {len(results)} 位创作者")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"结果文件: {output_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()
