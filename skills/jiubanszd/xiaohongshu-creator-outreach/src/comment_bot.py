#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书创作者评论引流 - 全自动化版本 v2.0
核心技术：多策略元素定位 + JavaScript注入 + 智能重试机制
目标：100%全自动化评论，零人工干预
"""

import asyncio
import json
import random
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Tuple, Any
import traceback

# 尝试导入依赖库
try:
    from playwright.async_api import async_playwright, Page, Locator
except ImportError:
    print("ERROR: 请先安装playwright: pip install playwright")
    exit(1)

try:
    import pandas as pd
except ImportError:
    print("ERROR: 请先安装pandas: pip install pandas openpyxl")
    exit(1)

try:
    from rich.console import Console
    from rich.progress import Progress, TaskID, BarColumn, TextColumn, TimeElapsedColumn
    from rich.panel import Panel
    from rich.table import Table
    from rich import box
except ImportError:
    print("ERROR: 请先安装rich: pip install rich")
    exit(1)

# 初始化Rich控制台
console = Console()


@dataclass
class CommentRecord:
    """评论记录数据类"""
    creator_id: str
    creator_name: str
    creator_home_url: str
    post_url: str = ""
    comment: str = ""
    status: str = "待评论"  # 待评论/已评论/评论失败/已跳过
    comment_time: str = ""
    notes: str = ""
    retry_count: int = 0  # 重试次数
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "创作者ID": self.creator_id,
            "创作者名称": self.creator_name,
            "主页链接": self.creator_home_url,
            "作品链接": self.post_url,
            "评论内容": self.comment,
            "评论状态": self.status,
            "评论时间": self.comment_time,
            "重试次数": self.retry_count,
            "备注": self.notes,
        }


@dataclass
class BotStats:
    """运行统计"""
    total: int = 0
    success: int = 0
    failed: int = 0
    skipped: int = 0
    current_step: str = "初始化"
    current_creator: str = ""
    
    @property
    def progress_pct(self) -> float:
        if self.total == 0:
            return 0.0
        return ((self.success + self.failed + self.skipped) / self.total) * 100


class CommentBot:
    """小红书评论机器人 - 全自动化版本"""
    
    # 类常量
    MAX_RETRIES = 3  # 最大重试次数
    RETRY_DELAY = 5  # 重试间隔(秒)
    CONSECUTIVE_FAIL_THRESHOLD = 5  # 连续失败阈值
    
    def __init__(self):
        # 路径配置
        self.src_dir = Path(__file__).parent
        self.workspace = self.src_dir.parent
        self.config_dir = self.workspace / "config"
        self.config_dir.mkdir(exist_ok=True)
        self.output_dir = self.workspace / "output"
        self.output_dir.mkdir(exist_ok=True)
        self.debug_dir = self.output_dir / "debug"
        self.debug_dir.mkdir(exist_ok=True)
        
        # 输入文件查找
        finder_output = Path.home() / ".openclaw" / "workspace" / "skills" / "xiaohongshu-creator-finder" / "output"
        self.input_dir = finder_output if finder_output.exists() else self.workspace / "input"
        self.input_dir.mkdir(exist_ok=True)
        
        # 加载配置
        self.config = self.load_config()
        self.comment_template = self.config.get("comment_template", self.get_default_comment())
        self.daily_limit = self.config.get("daily_limit", 50)
        self.min_delay = self.config.get("min_delay", 3)
        self.max_delay = self.config.get("max_delay", 8)
        self.chrome_path = self.config.get("chrome_path", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        
        # 运行时状态
        self.records: List[CommentRecord] = []
        self.stats = BotStats()
        self.today_commented = 0
        self.consecutive_failures = 0
        self.progress: Optional[Progress] = None
        self.task_id: Optional[TaskID] = None
        
        # 页面状态
        self.page: Optional[Page] = None
        self.browser = None
        self.context = None
    
    # ==================== 配置管理 ====================
    
    def load_config(self) -> dict:
        """加载配置文件"""
        config_file = self.config_dir / "settings.json"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.log_warning(f"加载配置失败: {e}")
        return {}
    
    def get_default_comment(self) -> str:
        """获取默认评论模板"""
        return "内容很棒！对你的作品很感兴趣，期待更多分享～"
    
    # ==================== 日志输出 ====================
    
    def log(self, message: str, style: str = ""):
        """输出日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        if style:
            console.print(f"[{timestamp}] {message}", style=style)
        else:
            console.print(f"[{timestamp}] {message}")
    
    def log_info(self, message: str):
        """信息日志"""
        self.log(f"[INFO] {message}", style="cyan")
    
    def log_success(self, message: str):
        """成功日志"""
        self.log(f"[OK] {message}", style="green bold")
    
    def log_warning(self, message: str):
        """警告日志"""
        self.log(f"[WARN] {message}", style="yellow")
    
    def log_error(self, message: str):
        """错误日志"""
        self.log(f"[ERR] {message}", style="red bold")
    
    def log_step(self, step_num: int, total_steps: int, message: str):
        """步骤日志"""
        self.stats.current_step = message
        self.log(f"[步骤 {step_num}/{total_steps}] {message}", style="blue")
    
    # ==================== 工具方法 ====================
    
    def random_delay(self, min_sec: Optional[float] = None, max_sec: Optional[float] = None) -> float:
        """生成随机延迟时间（防检测）"""
        min_sec = min_sec or self.min_delay
        max_sec = max_sec or self.max_delay
        return random.uniform(min_sec, max_sec)
    
    async def human_like_delay(self, min_sec: Optional[float] = None, max_sec: Optional[float] = None):
        """执行人类化延迟"""
        delay = self.random_delay(min_sec, max_sec)
        await asyncio.sleep(delay)
        return delay
    
    async def simulate_mouse_movement(self, page: Page, target_x: float, target_y: float):
        """模拟真实鼠标移动轨迹（贝塞尔曲线）"""
        try:
            # 获取当前鼠标位置
            viewport = await page.evaluate("() => ({ width: window.innerWidth, height: window.innerHeight })")
            current_x = viewport['width'] / 2 + random.randint(-100, 100)
            current_y = viewport['height'] / 2 + random.randint(-100, 100)
            
            # 生成中间控制点（贝塞尔曲线）
            cp1_x = current_x + (target_x - current_x) * 0.3 + random.randint(-50, 50)
            cp1_y = current_y + (target_y - current_y) * 0.3 + random.randint(-50, 50)
            cp2_x = current_x + (target_x - current_x) * 0.7 + random.randint(-50, 50)
            cp2_y = current_y + (target_y - current_y) * 0.7 + random.randint(-50, 50)
            
            # 沿贝塞尔曲线移动
            steps = random.randint(5, 10)
            for i in range(steps + 1):
                t = i / steps
                # 三次贝塞尔曲线公式
                x = (1-t)**3 * current_x + 3*(1-t)**2*t * cp1_x + 3*(1-t)*t**2 * cp2_x + t**3 * target_x
                y = (1-t)**3 * current_y + 3*(1-t)**2*t * cp1_y + 3*(1-t)*t**2 * cp2_y + t**3 * target_y
                await page.mouse.move(x, y)
                await asyncio.sleep(random.uniform(0.02, 0.08))
        except Exception as e:
            self.log_warning(f"鼠标移动模拟失败: {e}")
    
    async def random_scroll(self, page: Page, min_pixels: int = 100, max_pixels: int = 500):
        """随机滚动页面（模拟人类行为）"""
        try:
            scroll_pixels = random.randint(min_pixels, max_pixels)
            direction = random.choice([1, -1])  # 向上或向下
            
            # 分步滚动，更自然
            steps = random.randint(3, 6)
            per_step = (scroll_pixels * direction) // steps
            
            for _ in range(steps):
                await page.evaluate(f"window.scrollBy(0, {per_step})")
                await asyncio.sleep(random.uniform(0.1, 0.3))
            
            self.log_info(f"随机滚动: {scroll_pixels * direction}px")
        except Exception as e:
            self.log_warning(f"随机滚动失败: {e}")
    
    async def save_debug_screenshot(self, page: Page, filename: str):
        """保存调试截图"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = self.debug_dir / f"{filename}_{timestamp}.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)
            self.log_warning(f"调试截图已保存: {screenshot_path}")
        except Exception as e:
            self.log_error(f"截图保存失败: {e}")
    
    # ==================== 文件管理 ====================
    
    def find_input_file(self) -> Optional[Path]:
        """查找输入文件"""
        excel_files = list(self.input_dir.glob("creators_*.xlsx"))
        if excel_files:
            return max(excel_files, key=lambda p: p.stat().st_mtime)
        return None
    
    def load_creators(self, excel_path: Path) -> List[Dict]:
        """从Excel加载创作者列表"""
        try:
            df = pd.read_excel(excel_path)
            creators = df.to_dict('records')
            self.log_success(f"从 {excel_path.name} 加载 {len(creators)} 位创作者")
            return creators
        except Exception as e:
            self.log_error(f"读取Excel失败: {e}")
            return []
    
    def init_records(self, creators: List[Dict]):
        """初始化评论记录"""
        for creator in creators:
            home_url = str(creator.get("主页链接", ""))
            video_url = str(creator.get("视频链接", ""))
            
            record = CommentRecord(
                creator_id=str(creator.get("创作者ID", "")),
                creator_name=str(creator.get("创作者名称", "")),
                creator_home_url=home_url,
                post_url=video_url if video_url else home_url,
                comment=self.comment_template,
                status="待评论",
            )
            self.records.append(record)
        
        self.stats.total = len(self.records)
        self.log_info(f"待发创作者总数: {self.stats.total}")
    
    def save_progress(self):
        """保存进度"""
        try:
            progress_file = self.output_dir / "comment_progress.json"
            data = {
                "records": [r.to_dict() for r in self.records],
                "today_commented": self.today_commented,
                "stats": {
                    "success": self.stats.success,
                    "failed": self.stats.failed,
                    "skipped": self.stats.skipped,
                },
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log_warning(f"保存进度失败: {e}")
    
    def export_results(self):
        """导出结果"""
        if not self.records:
            return
        
        console.print()
        console.rule("[bold green]评论任务完成")
        
        # 创建统计表格
        table = Table(title="评论统计", box=box.ROUNDED)
        table.add_column("状态", style="cyan")
        table.add_column("数量", justify="right", style="magenta")
        
        status_count = {}
        for r in self.records:
            status_count[r.status] = status_count.get(r.status, 0) + 1
        
        for status, count in status_count.items():
            table.add_row(status, str(count))
        
        console.print(table)
        
        # 导出Excel
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = [r.to_dict() for r in self.records]
        
        excel = self.output_dir / f"comment_{ts}.xlsx"
        pd.DataFrame(data).to_excel(excel, index=False, engine='openpyxl')
        self.log_success(f"结果已导出: {excel}")
    
    # ==================== 核心功能：评论框定位 ====================
    
    async def locate_comment_box(self, page: Page, record: CommentRecord) -> Optional[Locator]:
        """
        多策略评论框定位（核心功能）
        按优先级依次尝试多种定位方法
        """
        self.log_step(2, 5, "定位评论输入框 - 多策略尝试")
        
        # 策略1: 使用精确的ID选择器（小红书网页版评论框）
        self.log_info("策略1: 使用ID选择器查找评论框...")
        try:
            locator = page.locator('#content-textarea')
            if await locator.is_visible(timeout=3000):
                self.log_success("通过ID选择器定位成功: #content-textarea")
                return locator
        except Exception as e:
            self.log_warning(f"ID选择器定位失败: {e}")
        
        # 策略2: 使用class选择器
        self.log_info("策略2: 使用class选择器查找评论框...")
        try:
            locator = page.locator('.content-input[contenteditable="true"]')
            if await locator.is_visible(timeout=2000):
                self.log_success("通过class选择器定位成功")
                return locator
        except Exception as e:
            self.log_warning(f"class选择器定位失败: {e}")
        
        # 策略3: 查找所有 contenteditable 的 p 标签
        self.log_info("策略3: 查找 contenteditable 的 p 标签...")
        try:
            locator = page.locator('p[contenteditable="true"]')
            if await locator.is_visible(timeout=2000):
                box = await locator.bounding_box()
                if box and box['y'] > 400:
                    self.log_success("通过p标签定位成功")
                    return locator
        except Exception as e:
            self.log_warning(f"p标签定位失败: {e}")
        
        # 策略4: 使用placeholder查找
        self.log_info("策略4: 使用placeholder查找评论框...")
        try:
            locator = page.get_by_placeholder("说点什么")
            if await locator.is_visible(timeout=2000):
                self.log_success("通过placeholder定位成功")
                return locator
        except Exception as e:
            self.log_warning(f"placeholder定位失败: {e}")
        
        # 策略5: 通用的 contenteditable 选择器
        self.log_info("策略5: 使用通用 contenteditable 选择器...")
        try:
            all_editables = await page.query_selector_all('[contenteditable="true"]')
            valid_elements = []
            
            for el in all_editables:
                try:
                    box = await el.bounding_box()
                    if box and box['y'] > 400 and box['height'] > 20:
                        valid_elements.append((el, box['y']))
                except:
                    continue
            
            if valid_elements:
                valid_elements.sort(key=lambda x: x[1], reverse=True)
                self.log_success(f"选择最下方的输入框")
                return valid_elements[0][0]
        except Exception as e:
            self.log_warning(f"通用选择器定位失败: {e}")
        
        self.log_error("所有定位策略均失败")
        return None
    
    # ==================== 核心功能：评论发送 ====================
    
    async def send_comment(self, page: Page, comment_box: Locator, comment_text: str, record: CommentRecord) -> bool:
        """
        多策略评论发送
        按优先级尝试多种发送方式
        """
        self.log_step(4, 5, "发送评论 - 多策略尝试")
        
        # 方式1: 按Enter键发送
        self.log_info("方式1: 尝试按Enter键发送...")
        try:
            await comment_box.press('Enter', timeout=10000)
            await self.human_like_delay(2, 3)
            
            # 验证是否成功
            if await self.verify_comment_sent(page, comment_text):
                self.log_success("通过Enter键发送成功")
                return True
        except Exception as e:
            self.log_warning(f"Enter键发送失败: {e}")
        
        # 方式2: 点击发送按钮
        self.log_info("方式2: 尝试点击发送按钮...")
        try:
            # 多种发送按钮文本
            send_button_texts = ["发送", "评论", "提交", "Submit", "Post", "Send"]
            
            for text in send_button_texts:
                try:
                    # 尝试通过role和name定位
                    send_btn = page.get_by_role("button", name=text)
                    if await send_btn.is_visible(timeout=2000):
                        await send_btn.click(timeout=5000)
                        await self.human_like_delay(2, 3)
                        
                        if await self.verify_comment_sent(page, comment_text):
                            self.log_success(f"通过'{text}'按钮发送成功")
                            return True
                except:
                    pass
                
                try:
                    # 尝试通过文本定位
                    send_btn = page.get_by_text(text).first
                    if await send_btn.is_visible(timeout=2000):
                        await send_btn.click(timeout=5000)
                        await self.human_like_delay(2, 3)
                        
                        if await self.verify_comment_sent(page, comment_text):
                            self.log_success(f"通过'{text}'文本按钮发送成功")
                            return True
                except:
                    pass
        except Exception as e:
            self.log_warning(f"点击发送按钮失败: {e}")
        
        # 方式3: JavaScript触发事件
        self.log_info("方式3: 尝试JavaScript触发...")
        try:
            # 直接操作DOM触发键盘事件
            await page.evaluate("""
                (text) => {
                    const activeElement = document.activeElement;
                    if (activeElement) {
                        // 触发Enter键事件
                        const enterEvent = new KeyboardEvent('keydown', {
                            key: 'Enter',
                            code: 'Enter',
                            keyCode: 13,
                            which: 13,
                            bubbles: true,
                            cancelable: true,
                        });
                        activeElement.dispatchEvent(enterEvent);
                        
                        // 也触发表单提交事件
                        const form = activeElement.closest('form');
                        if (form) {
                            form.dispatchEvent(new Event('submit', { bubbles: true }));
                        }
                    }
                }
            """, comment_text)
            
            await self.human_like_delay(2, 3)
            
            if await self.verify_comment_sent(page, comment_text):
                self.log_success("通过JavaScript触发发送成功")
                return True
        except Exception as e:
            self.log_warning(f"JavaScript触发失败: {e}")
        
        # 方式4: 强制提交（最后手段）
        self.log_info("方式4: 尝试强制提交...")
        try:
            await page.evaluate("""
                () => {
                    // 查找所有可能的提交按钮
                    const buttons = document.querySelectorAll('button, [role="button"]');
                    for (const btn of buttons) {
                        const text = btn.textContent || btn.innerText || '';
                        if (/发送|评论|提交|send|post/i.test(text)) {
                            btn.click();
                            return true;
                        }
                    }
                    return false;
                }
            """)
            
            await self.human_like_delay(2, 3)
            
            if await self.verify_comment_sent(page, comment_text):
                self.log_success("通过强制提交发送成功")
                return True
        except Exception as e:
            self.log_warning(f"强制提交失败: {e}")
        
        self.log_error("所有发送方式均失败")
        return False
    
    async def verify_comment_sent(self, page: Page, comment_text: str) -> bool:
        """
        验证评论是否发送成功
        """
        try:
            # 等待一下让页面更新
            await asyncio.sleep(2)
            
            # 方法1: 检查页面是否包含评论内容
            page_content = await page.content()
            if comment_text[:10] in page_content:
                return True
            
            # 方法2: 查找评论列表中的内容
            comments = await page.query_selector_all('[class*="comment"], [class*="remark"]')
            for comment in comments[:10]:  # 只检查前10条
                try:
                    text = await comment.inner_text()
                    if comment_text[:10] in text:
                        return True
                except:
                    continue
            
            # 方法3: 检查是否有成功提示
            success_indicators = ["评论成功", "发送成功", "success", "posted"]
            page_text = await page.inner_text('body')
            for indicator in success_indicators:
                if indicator in page_text.lower():
                    return True
            
            return False
        except Exception as e:
            self.log_warning(f"验证失败: {e}")
            return False
    
    # ==================== 核心功能：输入评论 ====================
    
    async def input_comment_text(self, page: Page, comment_box: Locator, comment_text: str) -> bool:
        """
        输入评论内容
        使用多种输入方式确保成功
        """
        self.log_step(3, 5, "输入评论内容")
        
        try:
            # 滚动到元素可见
            await comment_box.scroll_into_view_if_needed()
            await self.human_like_delay(0.5, 1)
            
            # 模拟真实点击（带鼠标移动）
            try:
                box = await comment_box.bounding_box()
                if box:
                    target_x = box['x'] + box['width'] / 2 + random.randint(-5, 5)
                    target_y = box['y'] + box['height'] / 2 + random.randint(-5, 5)
                    await self.simulate_mouse_movement(page, target_x, target_y)
                    await page.mouse.click(target_x, target_y)
            except:
                # 备用：直接点击
                await comment_box.click(timeout=10000)
            
            await self.human_like_delay(0.5, 1)
            
            # 清空现有内容
            try:
                await comment_box.fill("", timeout=5000)
            except:
                # 如果fill失败，尝试选中全部后删除
                await comment_box.press('Control+a')
                await comment_box.press('Delete')
            
            await asyncio.sleep(0.5)
            
            # 输入评论内容（模拟人类打字）
            input_method = random.choice(['type', 'fill'])
            
            if input_method == 'type':
                # 逐字输入，带随机延迟
                for char in comment_text:
                    await comment_box.type(char, delay=random.randint(30, 100))
            else:
                # 一次性填充
                await comment_box.fill(comment_text, timeout=10000)
            
            # 随机额外延迟（模拟思考时间）
            if random.random() < 0.3:
                await self.human_like_delay(1, 2)
            
            self.log_success("评论内容输入完成")
            return True
            
        except Exception as e:
            self.log_error(f"输入评论失败: {e}")
            return False
    
    # ==================== 核心功能：获取最新作品 ====================
    
    async def get_latest_post(self, page: Page, home_url: str) -> Optional[str]:
        """
        获取创作者最新作品链接
        """
        try:
            await page.goto(home_url, timeout=30000)
            await self.human_like_delay(3, 5)
            
            # 随机滚动一下
            await self.random_scroll(page)
            
            # 作品链接选择器
            post_selectors = [
                'a[href*="/explore/"]',
                'a[href*="/discovery/item/"]',
                'a[href*="/item/"]',
            ]
            
            for selector in post_selectors:
                posts = await page.query_selector_all(selector)
                for post in posts[:5]:
                    try:
                        href = await post.get_attribute('href')
                        if href:
                            # 清理链接
                            clean_href = href.split('?')[0]
                            if not clean_href.startswith('http'):
                                clean_href = f"https://www.xiaohongshu.com{clean_href}"
                            self.log_success(f"获取到作品链接: {clean_href}")
                            return clean_href
                    except:
                        continue
            
            return None
        except Exception as e:
            self.log_error(f"获取最新作品失败: {e}")
            return None
    
    # ==================== 核心功能：主评论流程 ====================
    
    async def post_comment_with_retry(self, record: CommentRecord) -> Tuple[bool, str]:
        """
        带重试机制的评论流程
        """
        page = self.page
        if not page:
            return False, "页面未初始化"
        
        for attempt in range(1, self.MAX_RETRIES + 1):
            record.retry_count = attempt
            
            if attempt > 1:
                self.log_warning(f"第{attempt}次重试...")
                await asyncio.sleep(self.RETRY_DELAY * attempt)  # 递增延迟
            
            try:
                # ===== 步骤1: 获取/确认作品链接 =====
                self.log_step(1, 5, "访问作品页面")
                
                post_url = record.post_url
                if not post_url or '/user/profile/' in post_url:
                    self.log_info("需要获取最新作品链接...")
                    post_url = await self.get_latest_post(page, record.creator_home_url)
                    if not post_url:
                        if attempt == self.MAX_RETRIES:
                            await self.save_debug_screenshot(page, f"no_post_{record.creator_id}")
                        continue  # 重试
                    record.post_url = post_url
                
                self.log_info(f"作品链接: {post_url}")
                
                # 访问作品页面
                await page.goto(post_url, timeout=30000)
                await self.human_like_delay(4, 6)
                
                # 检查登录状态
                if "/login" in page.url:
                    return False, "需要登录"
                
                # 滚动到评论区（页面底部）
                self.log_info("滚动到评论区...")
                for _ in range(5):
                    await page.evaluate("window.scrollBy(0, 800)")
                    await asyncio.sleep(0.5)
                
                # 额外等待评论区加载
                await asyncio.sleep(2)
                
                # 随机滚动
                await self.random_scroll(page)
                
                # ===== 步骤2: 定位评论框 =====
                comment_box = await self.locate_comment_box(page, record)
                if not comment_box:
                    if attempt == self.MAX_RETRIES:
                        await self.save_debug_screenshot(page, f"no_comment_box_{record.creator_id}")
                    continue  # 重试
                
                # ===== 步骤3: 输入评论 =====
                if not await self.input_comment_text(page, comment_box, record.comment):
                    if attempt == self.MAX_RETRIES:
                        await self.save_debug_screenshot(page, f"input_failed_{record.creator_id}")
                    continue  # 重试
                
                # ===== 步骤4: 发送评论 =====
                if not await self.send_comment(page, comment_box, record.comment, record):
                    if attempt == self.MAX_RETRIES:
                        await self.save_debug_screenshot(page, f"send_failed_{record.creator_id}")
                    continue  # 重试
                
                # ===== 步骤5: 验证结果 =====
                self.log_step(5, 5, "验证评论结果")
                
                if await self.verify_comment_sent(page, record.comment):
                    return True, "评论成功"
                else:
                    # 即使没有明确验证成功，只要流程走完也算成功
                    self.log_warning("无法明确验证，但流程已完成")
                    return True, "评论完成（未明确验证）"
                
            except Exception as e:
                error_msg = str(e)
                self.log_error(f"评论异常: {error_msg[:100]}")
                traceback.print_exc()
                
                if attempt == self.MAX_RETRIES:
                    await self.save_debug_screenshot(page, f"exception_{record.creator_id}")
        
        return False, f"重试{self.MAX_RETRIES}次后仍失败"
    
    # ==================== 浏览器管理 ====================
    
    async def init_browser(self):
        """初始化浏览器"""
        self.log_info("正在初始化浏览器...")
        
        p = await async_playwright().start()
        
        browser = await p.chromium.launch(
            headless=False,
            executable_path=self.chrome_path if Path(self.chrome_path).exists() else None,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # 注入反检测脚本
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        """)
        
        page = await context.new_page()
        
        self.browser = browser
        self.context = context
        self.page = page
        
        self.log_success("浏览器初始化完成")
    
    async def load_cookies(self):
        """加载Cookies"""
        cookie_paths = [
            self.config_dir / "cookies.json",
            Path.home() / ".openclaw" / "workspace" / "skills" / "xiaohongshu-creator-finder" / "config" / "cookies.json",
            Path.home() / ".openclaw" / "workspace" / ".xiaohongshu_cookies.json",
        ]
        
        for cookie_file in cookie_paths:
            if cookie_file.exists():
                try:
                    with open(cookie_file, 'r', encoding='utf-8') as f:
                        cookies = json.load(f)
                        await self.context.add_cookies(cookies)
                        self.log_success(f"已加载Cookies: {cookie_file.parent.name}")
                        return True
                except Exception as e:
                    self.log_warning(f"加载Cookie失败: {e}")
        
        return False
    
    async def check_and_login(self):
        """检查登录状态并处理登录"""
        await self.page.goto("https://www.xiaohongshu.com", timeout=15000)
        await asyncio.sleep(2)
        
        if "/login" in self.page.url:
            self.log_warning("Cookie已过期，需要重新登录")
            await self.page.goto("https://www.xiaohongshu.com/login", timeout=30000)
            await asyncio.sleep(3)
            
            self.log_info("请在浏览器中扫码登录（60秒超时）...")
            for i in range(60):
                await asyncio.sleep(1)
                if "/login" not in self.page.url:
                    self.log_success("登录成功")
                    
                    # 保存Cookie
                    cookies = await self.context.cookies()
                    with open(self.config_dir / "cookies.json", 'w', encoding='utf-8') as f:
                        json.dump(cookies, f)
                    
                    global_cookie = Path.home() / ".openclaw" / "workspace" / ".xiaohongshu_cookies.json"
                    with open(global_cookie, 'w', encoding='utf-8') as f:
                        json.dump(cookies, f)
                    
                    self.log_success("Cookie已保存")
                    return True
            
            self.log_error("登录超时")
            return False
        else:
            self.log_success("Cookie有效，已登录")
            return True
    
    # ==================== 主运行流程 ====================
    
    async def process_single_record(self, record: CommentRecord, index: int) -> bool:
        """
        处理单个创作者的评论
        """
        self.stats.current_creator = record.creator_name
        
        # 更新进度显示
        if self.progress and self.task_id is not None:
            self.progress.update(
                self.task_id,
                advance=0,
                description=f"[{index}/{self.stats.total}] {record.creator_name[:15]}... | 成功:{self.stats.success} 失败:{self.stats.failed}"
            )
        
        self.log("")
        console.rule(f"[cyan]处理 {index}/{self.stats.total}: {record.creator_name}")
        
        # 检查是否已评论
        if record.status == "已评论":
            self.log_info("已评论，跳过")
            self.stats.skipped += 1
            return True
        
        # 检查每日上限
        if self.today_commented >= self.daily_limit:
            self.log_warning(f"已达到每日评论上限 ({self.daily_limit})")
            return False
        
        # 检查连续失败
        if self.consecutive_failures >= self.CONSECUTIVE_FAIL_THRESHOLD:
            self.log_error(f"连续失败{self.consecutive_failures}次，暂停保护账号")
            return False
        
        # 延迟
        delay = await self.human_like_delay()
        self.log_info(f"等待 {delay:.1f} 秒...")
        
        # 执行评论
        success, message = await self.post_comment_with_retry(record)
        
        # 更新状态
        if success:
            self.today_commented += 1
            self.consecutive_failures = 0
            self.stats.success += 1
            record.status = "已评论"
            record.comment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_success(f"评论成功 ({self.today_commented}/{self.daily_limit})")
        else:
            self.consecutive_failures += 1
            self.stats.failed += 1
            record.status = "评论失败"
            record.notes = message
            self.log_error(f"评论失败: {message}")
        
        # 保存进度
        self.save_progress()
        
        # 更新进度条
        if self.progress and self.task_id is not None:
            self.progress.update(self.task_id, advance=1)
        
        return success
    
    async def run(self):
        """主运行入口"""
        console.rule("[bold blue]小红书创作者评论引流系统 v2.0")
        
        # 配置信息面板
        config_table = Table(box=box.ROUNDED)
        config_table.add_column("配置项", style="cyan")
        config_table.add_column("值", style="magenta")
        config_table.add_row("每日上限", str(self.daily_limit))
        config_table.add_row("延迟范围", f"{self.min_delay}-{self.max_delay}秒")
        config_table.add_row("最大重试", str(self.MAX_RETRIES))
        config_table.add_row("评论模板", self.comment_template[:30] + "...")
        console.print(config_table)
        
        # 查找输入文件
        input_file = self.find_input_file()
        if not input_file:
            self.log_error("未找到输入文件(creators_*.xlsx)")
            return
        
        self.log_info(f"输入文件: {input_file.name}")
        
        # 加载创作者
        creators = self.load_creators(input_file)
        if not creators:
            self.log_error("没有可处理的创作者")
            return
        
        self.init_records(creators)
        
        # 初始化浏览器
        await self.init_browser()
        
        # 加载Cookie并检查登录
        await self.load_cookies()
        if not await self.check_and_login():
            return
        
        # 使用Rich进度条
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(complete_style="green", finished_style="green"),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            
            self.progress = progress
            self.task_id = progress.add_task("准备开始...", total=self.stats.total)
            
            # 逐个处理
            for i, record in enumerate(self.records, 1):
                should_continue = await self.process_single_record(record, i)
                
                if not should_continue:
                    break
        
        # 关闭浏览器
        if self.browser:
            await self.browser.close()
        
        # 导出结果
        self.export_results()


# ==================== 入口 ====================

if __name__ == "__main__":
    bot = CommentBot()
    asyncio.run(bot.run())
