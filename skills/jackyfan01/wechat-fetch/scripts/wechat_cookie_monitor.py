#!/usr/bin/env python3
"""
微信 Cookie 自动监控脚本
- 定时检查 Cookie 状态
- Cookie 过期前提醒
- 过期后通知扫码登录
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError

# 配置
USER_DATA_DIR = "/home/admin/.openclaw/browser/openclaw/user-data"
CHECK_INTERVAL_HOURS = 12  # 每 12 小时检查一次
COOKIE_MAX_AGE_DAYS = 4    # Cookie 最大有效期
STATUS_FILE = "/home/admin/.openclaw/workspace/temp/wechat-cookie-status.json"


def load_status():
    """加载 Cookie 状态"""
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "last_check": None,
        "cookie_valid": None,
        "last_login": None,
        "expiry_estimate": None
    }


def save_status(status):
    """保存 Cookie 状态"""
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=2)


def check_cookie_valid():
    """
    检查 Cookie 是否有效
    返回：(是否有效，错误信息)
    """
    print(f"正在检查 Cookie 状态...")
    
    try:
        with sync_playwright() as p:
            # 使用持久化上下文
            browser = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=True,
                viewport={"width": 1920, "height": 1080}
            )
            
            page = browser.new_page()
            
            # 访问微信文章页面
            test_url = "https://mp.weixin.qq.com/s/MBkyKh1gF4gIAa3Cod4Cxg"
            page.goto(test_url, wait_until='domcontentloaded', timeout=30000)
            
            # 检查是否包含文章内容
            try:
                content = page.query_selector('#js_content')
                is_valid = content is not None
                
                if is_valid:
                    print("✅ Cookie 有效，可以正常访问")
                else:
                    print("❌ Cookie 可能已过期，页面缺少内容元素")
                
                browser.close()
                return is_valid, None
                
            except Exception as e:
                browser.close()
                return False, f"页面加载异常：{str(e)}"
                
    except TimeoutError:
        return False, "页面加载超时"
    except Exception as e:
        return False, f"检查失败：{str(e)}"


def send_notification(message, urgent=False):
    """
    发送通知
    可以通过 MemOS、邮件、微信等方式通知
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 方式 1: 写入通知文件（可以被其他程序读取）
    notification_file = "/home/admin/.openclaw/workspace/temp/wechat-cookie-notification.md"
    os.makedirs(os.path.dirname(notification_file), exist_ok=True)
    
    with open(notification_file, 'a', encoding='utf-8') as f:
        f.write(f"\n## [{timestamp}] {'🔴 紧急' if urgent else '⚠️ 提醒'}\n\n")
        f.write(f"{message}\n\n")
        f.write("---\n")
    
    # 方式 2: 打印到控制台（可以被日志系统捕获）
    if urgent:
        print(f"\n🔴 [紧急通知] {message}\n")
    else:
        print(f"\n⚠️ [提醒] {message}\n")
    
    # 方式 3: 可以通过 MemOS 发送消息（如果需要）
    # 这里预留接口
    
    return True


def check_and_notify():
    """
    执行检查并发送通知
    """
    print("=" * 60)
    print(f"微信 Cookie 状态检查")
    print(f"检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 加载状态
    status = load_status()
    
    # 检查 Cookie
    is_valid, error = check_cookie_valid()
    
    # 更新状态
    status["last_check"] = datetime.now().isoformat()
    status["cookie_valid"] = is_valid
    
    if is_valid:
        # Cookie 有效
        if status["last_login"]:
            last_login = datetime.fromisoformat(status["last_login"])
            days_since_login = (datetime.now() - last_login).days
            days_remaining = COOKIE_MAX_AGE_DAYS - days_since_login
            
            print(f"距离上次登录：{days_since_login} 天")
            print(f"预计剩余有效：{days_remaining} 天")
            
            # 如果快过期了（剩余不到 1 天），发送提醒
            if days_remaining <= 1:
                send_notification(
                    f"⚠️ **Cookie 即将过期**\n\n"
                    f"距离上次登录已 {days_since_login} 天\n"
                    f"预计剩余有效时间：**{days_remaining} 天**\n\n"
                    f"请尽快扫码登录更新 Cookie，避免影响抓取任务。\n\n"
                    f"**登录方法**:\n"
                    f"1. 访问 https://mp.weixin.qq.com/\n"
                    f"2. 扫码登录\n"
                    f"3. 保持浏览器开启",
                    urgent=(days_remaining == 0)
                )
            else:
                print(f"✅ Cookie 状态良好，下次检查：{CHECK_INTERVAL_HOURS}小时后")
        else:
            # 首次检查，记录登录时间
            status["last_login"] = datetime.now().isoformat()
            status["expiry_estimate"] = (datetime.now() + timedelta(days=COOKIE_MAX_AGE_DAYS)).isoformat()
            save_status(status)
            print("✅ 首次检查，已记录登录时间")
    else:
        # Cookie 无效
        print(f"❌ Cookie 已过期或无效")
        if error:
            print(f"错误信息：{error}")
        
        send_notification(
            f"🔴 **Cookie 已过期**\n\n"
            f"微信 Cookie 已失效，无法正常抓取文章。\n\n"
            f"错误信息：{error or '未知错误'}\n\n"
            f"**请立即扫码登录**:\n"
            f"1. 访问 https://mp.weixin.qq.com/\n"
            f"2. 使用微信扫码登录\n"
            f"3. 登录后重新运行抓取任务\n\n"
            f"登录后 Cookie 有效期约 4 天。",
            urgent=True
        )
    
    # 保存状态
    save_status(status)
    
    print("=" * 60)
    print(f"检查完成，状态已保存：{STATUS_FILE}")
    print("=" * 60)
    
    return is_valid


def setup_cron_check():
    """
    设置定时检查（需要系统支持 cron）
    """
    cron_job = f"0 */{CHECK_INTERVAL_HOURS} * * * python3 {__file__} >> /tmp/wechat-cookie-monitor.log 2>&1"
    
    print(f"定时检查配置（添加到 crontab）:")
    print(cron_job)
    print("\n手动添加命令:")
    print(f"crontab -e")
    print(f"# 然后粘贴上面的配置")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="微信 Cookie 自动监控脚本")
    parser.add_argument("--check", action="store_true", help="执行一次检查")
    parser.add_argument("--setup-cron", action="store_true", help="显示定时任务配置")
    
    args = parser.parse_args()
    
    if args.check:
        check_and_notify()
    elif args.setup_cron:
        setup_cron_check()
    else:
        # 默认执行检查
        check_and_notify()
