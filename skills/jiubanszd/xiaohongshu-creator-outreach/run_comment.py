#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书创作者评论引流脚本
"""

import pandas as pd
import json
import time
import random
import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright

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
        print(f"加载Cookie失败: {e}")
        return None


def load_creators():
    """读取创作者列表"""
    try:
        df = pd.read_excel(INPUT_EXCEL)
        print(f"成功读取 {len(df)} 位创作者信息")
        return df
    except Exception as e:
        print(f"读取Excel失败: {e}")
        return None


def get_latest_note_link(page, user_link):
    """获取用户最新作品链接"""
    try:
        print(f"访问用户主页: {user_link}")
        page.goto(user_link, wait_until="networkidle", timeout=30000)
        time.sleep(3)
        
        # 查找第一个笔记链接
        # 小红书笔记链接格式: /explore/xxxx 或 /discovery/item/xxxx
        note_links = page.locator('a[href*="/explore/"], a[href*="/discovery/item/"]').all()
        
        for link in note_links:
            href = link.get_attribute('href')
            if href and ('/explore/' in href or '/discovery/item/' in href):
                full_url = f"https://www.xiaohongshu.com{href}" if href.startswith('/') else href
                print(f"找到最新作品: {full_url}")
                return full_url
        
        print("未找到作品链接")
        return None
    except Exception as e:
        print(f"获取作品链接失败: {e}")
        return None


def post_comment(page, note_url, comment_text):
    """在作品下发表评论"""
    try:
        print(f"访问作品页: {note_url}")
        page.goto(note_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)  # 等待页面完全加载
        
        # 等待评论区加载 - 滚动到页面底部
        print("滚动到评论区...")
        for i in range(5):
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(1)
        
        # 尝试查找评论输入框 - 更多选择器
        selectors = [
            'textarea[placeholder*="评论"]',
            'textarea[placeholder*="说点什么"]',
            'textarea[placeholder*="写评论"]',
            'div[contenteditable="true"]',
            'input[placeholder*="评论"]',
            'input[placeholder*="说点什么"]',
            '.comment-input',
            '.input-area textarea',
            '[class*="comment"] textarea',
            '[class*="input"] textarea',
            '[class*="editor"]',
            'textarea',
            'div[contenteditable]',
        ]
        
        comment_box = None
        used_selector = None
        
        for selector in selectors:
            try:
                elements = page.locator(selector).all()
                for elem in elements:
                    if elem.is_visible(timeout=2000):
                        # 检查是否在评论区附近
                        comment_box = elem
                        used_selector = selector
                        print(f"找到评论框: {selector}")
                        break
                if comment_box:
                    break
            except Exception as e:
                continue
        
        # 如果没找到，尝试通过文字定位
        if not comment_box:
            print("尝试通过文字定位评论框...")
            try:
                # 查找包含"评论"或"说点什么"的元素
                comment_trigger = page.locator('text=说点什么, text=评论, text=写评论').first
                if comment_trigger.is_visible(timeout=3000):
                    comment_trigger.click()
                    time.sleep(2)
                    # 再次查找输入框
                    for selector in selectors:
                        try:
                            box = page.locator(selector).first
                            if box.is_visible(timeout=2000):
                                comment_box = box
                                used_selector = selector
                                print(f"点击后找到评论框: {selector}")
                                break
                        except:
                            continue
            except Exception as e:
                print(f"通过文字定位失败: {e}")
        
        if not comment_box:
            # 截图保存用于调试
            try:
                page.screenshot(path=f"output/debug_screenshot_{int(time.time())}.png")
                print("已保存调试截图到 output/ 目录")
            except:
                pass
            print("未找到评论框")
            return False, "未找到评论框"
        
        # 点击评论框确保聚焦
        try:
            comment_box.click()
            time.sleep(1)
        except:
            pass
        
        # 输入评论内容
        print(f"输入评论: {comment_text}")
        comment_box.fill(comment_text)
        time.sleep(2)
        
        # 查找发送按钮
        send_selectors = [
            'button:has-text("发送")',
            'button:has-text("评论")',
            'button[type="submit"]',
            '.send-btn',
            '[class*="send"]',
            'button:has-text("Post")',
            'button:has-text("Send")',
            'button:has-text("发布")',
        ]
        
        send_btn = None
        for selector in send_selectors:
            try:
                btn = page.locator(selector).first
                if btn.is_visible(timeout=2000):
                    send_btn = btn
                    print(f"找到发送按钮: {selector}")
                    break
            except:
                continue
        
        if send_btn:
            send_btn.click()
            print("评论发送成功")
            time.sleep(3)
            return True, "评论成功"
        else:
            # 尝试按回车键发送
            comment_box.press("Enter")
            print("按回车发送评论")
            time.sleep(3)
            return True, "评论成功(回车)"
        
    except Exception as e:
        print(f"发表评论失败: {e}")
        return False, str(e)


def check_verification(page):
    """检查是否遇到验证码"""
    try:
        # 检查常见的验证码提示
        verification_keywords = ['验证码', '验证', '滑块', 'captcha', 'verify']
        page_content = page.content()
        for keyword in verification_keywords:
            if keyword in page_content:
                return True
        return False
    except:
        return False


def save_progress(results, progress_file):
    """保存进度"""
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"进度已保存到: {progress_file}")


def save_results_to_excel(results, output_file):
    """保存结果到Excel"""
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)
    print(f"结果已保存到: {output_file}")


def main():
    """主函数"""
    print("=" * 50)
    print("小红书创作者评论引流")
    print("=" * 50)
    
    # 加载Cookie
    cookies = load_cookies()
    if not cookies:
        print("Cookie加载失败，请检查登录状态")
        return
    
    # 读取创作者列表
    creators_df = load_creators()
    if creators_df is None or len(creators_df) == 0:
        print("没有创作者数据")
        return
    
    print(f"\n共 {len(creators_df)} 位创作者需要评论")
    
    # 准备结果列表
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    progress_file = os.path.join(OUTPUT_DIR, "comment_progress.json")
    output_file = os.path.join(OUTPUT_DIR, f"comment_{timestamp}.xlsx")
    
    # 启动Playwright
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(
            headless=False,  # 非 headless 模式便于调试
            executable_path=CHROME_PATH,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800}
        )
        
        # 添加Cookie
        context.add_cookies(cookies)
        print("Cookie已加载")
        
        page = context.new_page()
        
        # 先访问小红书首页确认登录状态
        print("检查登录状态...")
        page.goto("https://www.xiaohongshu.com", wait_until="networkidle", timeout=30000)
        time.sleep(3)
        
        # 检查是否遇到验证码
        if check_verification(page):
            print("[!] 检测到验证码，等待30秒...")
            time.sleep(30)
        
        # 再次检查是否还有验证码
        if check_verification(page):
            print("[!] 验证码可能仍未完成，继续尝试执行...")
        
        # 遍历创作者
        for idx, row in creators_df.iterrows():
            user_id = row.get('创作者ID', '')
            username = row.get('创作者名称', '')
            user_link = row.get('主页链接', '')
            note_link = row.get('视频链接', '')
            
            print(f"\n[{idx+1}/{len(creators_df)}] 处理创作者: {username} ({user_id})")
            
            result = {
                '创作者ID': user_id,
                '创作者名称': username,
                '主页链接': user_link,
                '作品链接': note_link,
                '评论内容': COMMENT_TEMPLATE,
                '评论状态': '待评论',
                '评论时间': '',
                '备注': ''
            }
            
            try:
                # 直接使用视频链接
                if not note_link or pd.isna(note_link):
                    print("视频链接为空，尝试从主页获取...")
                    note_url = get_latest_note_link(page, user_link)
                    if note_url:
                        note_link = note_url
                        result['作品链接'] = note_link
                
                if not note_link or pd.isna(note_link):
                    result['评论状态'] = '评论失败'
                    result['备注'] = '无作品链接'
                    results.append(result)
                    continue
                
                # 直接发表评论
                success, msg = post_comment(page, note_link, COMMENT_TEMPLATE)
                if success:
                    result['评论状态'] = '已评论'
                    result['评论时间'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    result['备注'] = msg
                else:
                    result['评论状态'] = '评论失败'
                    result['备注'] = msg
                    
                    # 检查是否是验证码
                    if check_verification(page):
                        print("[!] 检测到验证码，请手动完成验证...")
                        # 保存进度
                        save_progress(results, progress_file)
                        time.sleep(30)  # 等待30秒
                
                results.append(result)
                
                # 随机延迟
                delay = random.randint(MIN_DELAY, MAX_DELAY)
                print(f"等待 {delay} 秒...")
                time.sleep(delay)
                
            except Exception as e:
                print(f"处理创作者时出错: {e}")
                result['评论状态'] = '评论失败'
                result['备注'] = str(e)
                results.append(result)
                
                # 保存进度
                save_progress(results, progress_file)
        
        browser.close()
    
    # 保存最终结果
    save_results_to_excel(results, output_file)
    save_progress(results, progress_file)
    
    # 统计
    success_count = sum(1 for r in results if r['评论状态'] == '已评论')
    fail_count = sum(1 for r in results if r['评论状态'] == '评论失败')
    skip_count = sum(1 for r in results if r['评论状态'] == '已跳过')
    
    print("\n" + "=" * 50)
    print("评论引流任务完成!")
    print(f"总计: {len(results)} 位创作者")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"跳过: {skip_count}")
    print(f"结果文件: {output_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()
