#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书创作者建联Bot - 自动化方案（模拟真人操作）
技术策略：
1. 随机延迟模拟真人操作间隔
2. 鼠标移动轨迹模拟
3. 逐字输入模拟真实打字
4. 智能元素定位（多策略备选）
5. 低频率发送（5-10条/天）
6. 异常自动暂停保护账号
"""

import asyncio
import json
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

try:
    from playwright.async_api import async_playwright, Page
except ImportError:
    print("ERROR: pip install playwright")
    exit(1)

try:
    import pandas as pd
except ImportError:
    print("ERROR: pip install pandas openpyxl")
    exit(1)


@dataclass
class OutreachRecord:
    """建联记录"""
    creator_id: str
    creator_name: str
    home_url: str
    matched_keyword: str
    message: str = ""
    status: str = "待发送"
    send_time: str = ""
    reply_time: str = ""
    notes: str = ""
    
    def to_dict(self):
        return {
            "创作者ID": self.creator_id,
            "创作者名称": self.creator_name,
            "主页链接": self.home_url,
            "匹配关键词": self.matched_keyword,
            "发送消息": self.message,
            "建联状态": self.status,
            "发送时间": self.send_time,
            "回复时间": self.reply_time,
            "备注": self.notes,
        }


class OutreachBot:
    def __init__(self):
        self.src_dir = Path(__file__).parent
        self.workspace = self.src_dir.parent
        self.config_dir = self.workspace / "config"
        self.config_dir.mkdir(exist_ok=True)
        self.output_dir = self.workspace / "output"
        self.output_dir.mkdir(exist_ok=True)
        
        # 找输入文件
        finder_output = Path.home() / ".openclaw" / "workspace" / "skills" / "xiaohongshu-creator-finder" / "output"
        self.input_dir = finder_output if finder_output.exists() else self.workspace / "input"
        self.input_dir.mkdir(exist_ok=True)
        
        # 加载配置
        self.config = self.load_config()
        self.message_template = self.config.get("message_template", self.get_default_message())
        self.daily_limit = self.config.get("daily_limit", 5)
        self.min_delay = self.config.get("min_delay", 5)
        self.max_delay = self.config.get("max_delay", 15)
        self.chrome_path = self.config.get("chrome_path", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        
        self.records: List[OutreachRecord] = []
        self.today_sent = 0
        self.consecutive_failures = 0
        
    def load_config(self) -> dict:
        config_file = self.config_dir / "settings.json"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def get_default_message(self) -> str:
        return """hi，看到你的AI作品很有意思！

我在做AI短番创作者扶持，想邀请你了解一下：
- 流量扶持
- 变现机会  
- 创作工具

感兴趣可以回我，发你详细资料～"""
    
    def log(self, msg: str):
        safe_msg = msg.encode('ascii', 'replace').decode('ascii') if msg else ""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {safe_msg}", flush=True)
    
    def random_delay(self, min_sec=None, max_sec=None):
        min_sec = min_sec or self.min_delay
        max_sec = max_sec or self.max_delay
        return random.uniform(min_sec, max_sec)
    
    def find_input_file(self) -> Optional[Path]:
        excel_files = list(self.input_dir.glob("creators_*.xlsx"))
        if excel_files:
            return max(excel_files, key=lambda p: p.stat().st_mtime)
        return None
    
    def load_creators(self, excel_path: Path) -> List[Dict]:
        try:
            df = pd.read_excel(excel_path)
            creators = df.to_dict('records')
            self.log(f"[OK] 从 {excel_path.name} 加载 {len(creators)} 位创作者")
            return creators
        except Exception as e:
            self.log(f"[ERR] 读取Excel失败: {e}")
            return []
    
    def init_records(self, creators: List[Dict]):
        for creator in creators:
            record = OutreachRecord(
                creator_id=str(creator.get("创作者ID", "")),
                creator_name=str(creator.get("创作者名称", "")),
                home_url=str(creator.get("主页链接", "")),
                matched_keyword=str(creator.get("关键词", "")),
                message=self.message_template,
                status="待发送",
            )
            self.records.append(record)
    
    async def human_like_typing(self, page: Page, selector: str, text: str):
        for char in text:
            await page.type(selector, char, delay=random.randint(50, 200))
            await asyncio.sleep(random.uniform(0.01, 0.05))
    
    async def smart_click(self, page: Page, element):
        try:
            box = await element.bounding_box()
            if box:
                x = box['x'] + box['width'] / 2 + random.randint(-5, 5)
                y = box['y'] + box['height'] / 2 + random.randint(-5, 5)
                await page.mouse.move(x, y, steps=random.randint(3, 8))
                await asyncio.sleep(self.random_delay(0.3, 0.8))
        except:
            pass
        await element.click()
    
    async def find_and_click_message_btn(self, page: Page) -> bool:
        text_patterns = ["私信", "发消息", "聊天"]
        for text in text_patterns:
            try:
                btn = await page.wait_for_selector(f'text={text}', timeout=3000)
                if btn and await btn.is_visible():
                    self.log(f"[OK] 找到私信按钮（文字: {text}）")
                    await self.smart_click(page, btn)
                    return True
            except:
                continue
        
        css_selectors = [
            'button[class*="message"]',
            'button[class*="chat"]',
            'div[class*="message"]',
        ]
        for selector in css_selectors:
            try:
                btn = await page.query_selector(selector)
                if btn and await btn.is_visible():
                    self.log(f"[OK] 找到私信按钮（选择器）")
                    await self.smart_click(page, btn)
                    return True
            except:
                continue
        
        return False
    
    async def send_message(self, page: Page, record: OutreachRecord) -> bool:
        try:
            # 访问主页
            self.log("[STEP 1/5] 访问主页...")
            await page.goto(record.home_url, timeout=30000)
            await asyncio.sleep(self.random_delay(3, 5))
            
            page_text = await page.inner_text('body')
            if any(word in page_text for word in ["频繁", "限制", "违规", "异常"]):
                self.log("[WARN] 账号可能触发限制，暂停发送")
                return False
            
            # 点击私信按钮
            self.log("[STEP 2/5] 查找私信按钮...")
            if not await self.find_and_click_message_btn(page):
                self.log("[ERR] 未找到私信按钮，尝试备选方案...")
                # 备选：直接构造消息URL
                user_id = record.creator_id
                msg_url = f"https://www.xiaohongshu.com/user/profile/{user_id}"
                await page.goto(msg_url, timeout=30000)
                await asyncio.sleep(self.random_delay(4, 6))
                
                # 再次尝试找私信按钮
                if not await self.find_and_click_message_btn(page):
                    return False
            
            await asyncio.sleep(self.random_delay(4, 6))
            
            # 等待输入框
            self.log("[STEP 3/5] 等待聊天窗口...")
            input_box = None
            for _ in range(10):
                selectors = ['textarea', 'div[contenteditable="true"]', '[placeholder*="输入"]']
                for sel in selectors:
                    try:
                        box = await page.wait_for_selector(sel, timeout=1000)
                        if box and await box.is_visible():
                            input_box = box
                            break
                    except:
                        continue
                if input_box:
                    break
                await asyncio.sleep(1)
            
            if not input_box:
                self.log("[ERR] 未找到输入框")
                return False
            
            # 输入消息
            self.log("[STEP 4/5] 输入消息...")
            await input_box.fill("")
            await asyncio.sleep(0.5)
            
            # 逐字输入
            for char in record.message:
                await input_box.type(char, delay=random.randint(50, 150))
            
            await asyncio.sleep(self.random_delay(2, 4))
            
            # 发送
            self.log("[STEP 5/5] 发送消息...")
            await input_box.press('Enter')
            await asyncio.sleep(self.random_delay(3, 5))
            
            self.log("[OK] 消息发送完成")
            return True
            
        except Exception as e:
            self.log(f"[ERR] 发送异常: {str(e)[:50]}")
            return False
    
    def save_progress(self):
        try:
            progress_file = self.output_dir / "outreach_progress.json"
            data = {
                "records": [r.to_dict() for r in self.records],
                "today_sent": self.today_sent,
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log(f"[WARN] 保存进度失败: {e}")
    
    def export_results(self):
        if not self.records:
            return
        
        self.log(f"\n{'='*50}")
        self.log("[RESULT] 建联完成")
        
        status_count = {}
        for r in self.records:
            status_count[r.status] = status_count.get(r.status, 0) + 1
        
        for status, count in status_count.items():
            self.log(f"  {status}: {count}")
        
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = [r.to_dict() for r in self.records]
        
        excel = self.output_dir / f"outreach_{ts}.xlsx"
        pd.DataFrame(data).to_excel(excel, index=False, engine='openpyxl')
        self.log(f"\n[OK] Excel: {excel}")
    
    async def run(self):
        self.log("="*50)
        self.log("小红书创作者建联系统 - 自动化版")
        self.log("="*50)
        self.log(f"[CONFIG] 每日上限: {self.daily_limit}")
        self.log(f"[CONFIG] 延迟范围: {self.min_delay}-{self.max_delay}秒")
        
        input_file = self.find_input_file()
        if not input_file:
            self.log("[ERR] 未找到输入文件")
            return
        
        self.log(f"[INFO] 输入文件: {input_file.name}")
        
        creators = self.load_creators(input_file)
        if not creators:
            return
        
        self.init_records(creators)
        self.log(f"[INFO] 待发创作者: {len(self.records)}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                executable_path=self.chrome_path,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
            
            cookies_file = Path.home() / ".openclaw" / "workspace" / "skills" / "xiaohongshu-creator-finder" / "config" / "cookies.json"
            if cookies_file.exists():
                with open(cookies_file, 'r', encoding='utf-8') as f:
                    await context.add_cookies(json.load(f))
                self.log("[OK] Cookies loaded")
            
            page = await context.new_page()
            
            # 检查登录
            await page.goto("https://www.xiaohongshu.com", timeout=15000)
            await asyncio.sleep(2)
            
            if "/login" in page.url:
                self.log("[INFO] 请扫码登录...")
                await page.goto("https://www.xiaohongshu.com/login", timeout=30000)
                await asyncio.sleep(3)
                for i in range(60):
                    await asyncio.sleep(1)
                    if "/login" not in page.url:
                        self.log("[OK] 登录成功")
                        with open(self.config_dir / "cookies.json", 'w', encoding='utf-8') as f:
                            json.dump(await context.cookies(), f)
                        break
                else:
                    self.log("[ERR] 登录超时")
                    return
            
            # 逐个发送
            for i, record in enumerate(self.records):
                if self.today_sent >= self.daily_limit:
                    self.log(f"\n[INFO] 已达到每日发送上限 ({self.daily_limit})")
                    break
                
                if self.consecutive_failures >= 3:
                    self.log("[WARN] 连续失败3次，暂停发送以保护账号")
                    break
                
                self.log(f"\n{'='*50}")
                self.log(f"[{i+1}/{len(self.records)}] {record.creator_name}")
                
                if record.status == "已发送":
                    self.log(f"[SKIP] 已发送")
                    continue
                
                delay = self.random_delay()
                self.log(f"[WAIT] 等待 {delay:.1f} 秒...")
                await asyncio.sleep(delay)
                
                success = await self.send_message(page, record)
                
                if success:
                    self.today_sent += 1
                    self.consecutive_failures = 0
                    record.status = "已发送"
                    record.send_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.log(f"[OK] 发送成功 ({self.today_sent}/{self.daily_limit})")
                else:
                    self.consecutive_failures += 1
                    record.status = "发送失败"
                    self.log(f"[FAIL] 发送失败 (连续失败: {self.consecutive_failures})")
                
                self.save_progress()
            
            await browser.close()
        
        self.export_results()


if __name__ == "__main__":
    bot = OutreachBot()
    asyncio.run(bot.run())
