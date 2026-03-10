#!/usr/bin/env python3
"""美团助手 - 支持外卖搜索、团购、红包"""

import argparse
import asyncio
import json
import os
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote, urlparse

try:
    from playwright.async_api import async_playwright, Page, Browser
except ImportError:
    print("请先安装依赖: pip install playwright && playwright install chromium")
    sys.exit(1)

# 配置
CONFIG_DIR = Path.home() / ".meituan"
COOKIES_FILE = CONFIG_DIR / "cookies.json"
DB_FILE = CONFIG_DIR / "meituan.db"
CONFIG_DIR.mkdir(exist_ok=True)

@dataclass
class FoodItem:
    """外卖商品数据类"""
    id: str
    name: str
    restaurant: str
    price: float
    original_price: Optional[float]
    rating: float
    sales: str
    delivery_time: str
    delivery_fee: str
    url: str
    image: str

@dataclass
class Deal:
    """团购优惠数据类"""
    id: str
    title: str
    category: str
    price: float
    original_price: float
    discount: str
    location: str
    sold: str
    url: str
    image: str

class MeituanClient:
    """美团客户端"""
    
    BASE_URL = "https://www.meituan.com"
    WAIMAI_URL = "https://waimai.meituan.com"
    TUAN_URL = "https://www.meituan.com/deal"
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.db = self._init_db()
    
    def _init_db(self) -> sqlite3.Connection:
        """初始化SQLite数据库"""
        conn = sqlite3.connect(DB_FILE)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS foods (
                id TEXT PRIMARY KEY,
                name TEXT,
                restaurant TEXT,
                price REAL,
                original_price REAL,
                rating REAL,
                sales TEXT,
                delivery_time TEXT,
                delivery_fee TEXT,
                url TEXT,
                image TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS deals (
                id TEXT PRIMARY KEY,
                title TEXT,
                category TEXT,
                price REAL,
                original_price REAL,
                discount TEXT,
                location TEXT,
                sold TEXT,
                url TEXT,
                image TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS redpackets (
                id TEXT PRIMARY KEY,
                name TEXT,
                value REAL,
                min_spend REAL,
                expiry TEXT,
                claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        return conn
    
    async def init_browser(self, headless: bool = True):
        """初始化浏览器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        # 加载cookies
        if COOKIES_FILE.exists():
            cookies = json.loads(COOKIES_FILE.read_text())
            await context.add_cookies(cookies)
        
        self.page = await context.new_page()
        
        # 注入反检测脚本
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
    
    async def login(self):
        """扫码登录"""
        await self.init_browser(headless=False)
        
        print("正在打开美团登录页面...")
        await self.page.goto("https://passport.meituan.com/account/unitivelogin")
        
        # 等待用户扫码登录
        print("请使用美团APP扫码登录...")
        try:
            await self.page.wait_for_selector(".user-info", timeout=120000)
            
            # 保存cookies
            cookies = await self.page.context.cookies()
            COOKIES_FILE.write_text(json.dumps(cookies))
            print(f"登录成功！Cookies已保存到 {COOKIES_FILE}")
        except Exception as e:
            print(f"登录超时或失败: {e}")
        
        await self.close()
    
    async def search_food(self, keyword: str, location: str = "北京") -> List[FoodItem]:
        """搜索外卖"""
        if not self.page:
            await self.init_browser()
        
        encoded_keyword = quote(keyword)
        url = f"{self.WAIMAI_URL}/home/{encoded_keyword}"
        
        print(f"正在搜索外卖: {keyword}")
        await self.page.goto(url, wait_until="networkidle")
        await asyncio.sleep(3)
        
        foods = []
        
        try:
            # 等待商家列表加载
            await self.page.wait_for_selector(".restaurant-item", timeout=10000)
            items = await self.page.query_selector_all(".restaurant-item")
            
            for item in items[:15]:
                try:
                    link_el = await item.query_selector("a")
                    url = await link_el.get_attribute("href") if link_el else ""
                    if url and not url.startswith("http"):
                        url = f"https:{url}"
                    
                    # 提取商家ID
                    restaurant_id = ""
                    if "/restaurant/" in url:
                        restaurant_id = url.split("/restaurant/")[-1].split("?")[0]
                    
                    name_el = await item.query_selector(".restaurant-name")
                    name = await name_el.inner_text() if name_el else ""
                    
                    rating_el = await item.query_selector(".rating")
                    rating_text = await rating_el.inner_text() if rating_el else "0"
                    rating = float(rating_text.strip() or 0)
                    
                    sales_el = await item.query_selector(".sales")
                    sales = await sales_el.inner_text() if sales_el else ""
                    
                    time_el = await item.query_selector(".delivery-time")
                    delivery_time = await time_el.inner_text() if time_el else ""
                    
                    fee_el = await item.query_selector(".delivery-fee")
                    delivery_fee = await fee_el.inner_text() if fee_el else ""
                    
                    img_el = await item.query_selector("img")
                    image = await img_el.get_attribute("src") if img_el else ""
                    
                    food = FoodItem(
                        id=restaurant_id,
                        name=name.strip(),
                        restaurant=name.strip(),
                        price=0,
                        original_price=None,
                        rating=rating,
                        sales=sales,
                        delivery_time=delivery_time,
                        delivery_fee=delivery_fee,
                        url=url,
                        image=image if image.startswith("http") else f"https:{image}"
                    )
                    foods.append(food)
                    self._save_food(food)
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"搜索外卖失败: {e}")
        
        return foods
    
    def _save_food(self, food: FoodItem):
        """保存外卖到数据库"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO foods 
            (id, name, restaurant, price, original_price, rating, sales, delivery_time, delivery_fee, url, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (food.id, food.name, food.restaurant, food.price, food.original_price,
              food.rating, food.sales, food.delivery_time, food.delivery_fee, food.url, food.image))
        self.db.commit()
    
    async def get_deals(self, category: str = "all") -> List[Deal]:
        """获取团购优惠"""
        if not self.page:
            await self.init_browser()
        
        print("正在获取团购优惠...")
        await self.page.goto(self.TUAN_URL, wait_until="networkidle")
        await asyncio.sleep(3)
        
        deals = []
        
        try:
            # 等待团购列表加载
            await self.page.wait_for_selector(".deal-item", timeout=10000)
            items = await self.page.query_selector_all(".deal-item")
            
            for item in items[:15]:
                try:
                    link_el = await item.query_selector("a")
                    url = await link_el.get_attribute("href") if link_el else ""
                    if url and not url.startswith("http"):
                        url = f"https:{url}"
                    
                    deal_id = ""
                    if "/deal/" in url:
                        deal_id = url.split("/deal/")[-1].split("?")[0]
                    
                    title_el = await item.query_selector(".deal-title")
                    title = await title_el.inner_text() if title_el else ""
                    
                    price_el = await item.query_selector(".deal-price")
                    price_text = await price_el.inner_text() if price_el else "0"
                    price = float(price_text.replace("¥", "").strip() or 0)
                    
                    original_el = await item.query_selector(".original-price")
                    original_text = await original_el.inner_text() if original_el else "0"
                    original_price = float(original_text.replace("¥", "").strip() or 0)
                    
                    discount_el = await item.query_selector(".discount")
                    discount = await discount_el.inner_text() if discount_el else ""
                    
                    location_el = await item.query_selector(".location")
                    location = await location_el.inner_text() if location_el else ""
                    
                    sold_el = await item.query_selector(".sold-count")
                    sold = await sold_el.inner_text() if sold_el else ""
                    
                    img_el = await item.query_selector("img")
                    image = await img_el.get_attribute("src") if img_el else ""
                    
                    deal = Deal(
                        id=deal_id,
                        title=title.strip(),
                        category=category,
                        price=price,
                        original_price=original_price,
                        discount=discount,
                        location=location,
                        sold=sold,
                        url=url,
                        image=image if image.startswith("http") else f"https:{image}"
                    )
                    deals.append(deal)
                    self._save_deal(deal)
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"获取团购失败: {e}")
        
        return deals
    
    def _save_deal(self, deal: Deal):
        """保存团购到数据库"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO deals 
            (id, title, category, price, original_price, discount, location, sold, url, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (deal.id, deal.title, deal.category, deal.price, deal.original_price,
              deal.discount, deal.location, deal.sold, deal.url, deal.image))
        self.db.commit()
    
    async def get_redpackets(self) -> List[dict]:
        """获取红包"""
        if not self.page:
            await self.init_browser()
        
        print("正在查询红包...")
        await self.page.goto("https://www.meituan.com/redpacket", wait_until="networkidle")
        await asyncio.sleep(2)
        
        redpackets = []
        try:
            items = await self.page.query_selector_all(".redpacket-item")
            for item in items[:10]:
                try:
                    name_el = await item.query_selector(".rp-name")
                    name = await name_el.inner_text() if name_el else ""
                    
                    value_el = await item.query_selector(".rp-value")
                    value = await value_el.inner_text() if value_el else ""
                    
                    limit_el = await item.query_selector(".rp-limit")
                    limit = await limit_el.inner_text() if limit_el else ""
                    
                    expiry_el = await item.query_selector(".rp-expiry")
                    expiry = await expiry_el.inner_text() if expiry_el else ""
                    
                    redpackets.append({
                        "name": name.strip(),
                        "value": value.strip(),
                        "limit": limit.strip(),
                        "expiry": expiry.strip()
                    })
                except:
                    continue
        except Exception as e:
            print(f"获取红包失败: {e}")
        
        return redpackets

def format_food(f: FoodItem, index: int) -> str:
    """格式化外卖输出"""
    rating_str = f"⭐{f.rating}" if f.rating else ""
    time_str = f" | {f.delivery_time}" if f.delivery_time else ""
    fee_str = f" | 配送{f.delivery_fee}" if f.delivery_fee else ""
    
    return f"""
[{index}] {f.name[:40]}{'...' if len(f.name) > 40 else ''}
    {rating_str} {f.sales}{time_str}{fee_str}
    链接: {f.url}
"""

def format_deal(d: Deal, index: int) -> str:
    """格式化团购输出"""
    discount_str = f" [{d.discount}]" if d.discount else ""
    sold_str = f" | 已售{d.sold}" if d.sold else ""
    location_str = f" | {d.location}" if d.location else ""
    
    return f"""
[{index}]{discount_str} {d.title[:40]}{'...' if len(d.title) > 40 else ''}
    价格: ¥{d.price:.2f} (原价¥{d.original_price:.2f}){sold_str}{location_str}
    链接: {d.url}
"""

async def main():
    parser = argparse.ArgumentParser(description="美团助手")
    parser.add_argument("command", choices=["food", "deal", "redpacket", "login"])
    parser.add_argument("arg", nargs="?", help="搜索关键词")
    parser.add_argument("--location", default="北京", help="城市位置")
    
    args = parser.parse_args()
    
    client = MeituanClient()
    
    try:
        if args.command == "login":
            await client.login()
        
        elif args.command == "food":
            if not args.arg:
                print("请提供搜索关键词")
                return
            foods = await client.search_food(args.arg, args.location)
            print(f"\n找到 {len(foods)} 家外卖:\n")
            for i, f in enumerate(foods, 1):
                print(format_food(f, i))
        
        elif args.command == "deal":
            deals = await client.get_deals()
            print(f"\n团购优惠 ({len(deals)} 个):\n")
            for i, d in enumerate(deals, 1):
                print(format_deal(d, i))
        
        elif args.command == "redpacket":
            redpackets = await client.get_redpackets()
            print(f"\n找到 {len(redpackets)} 个红包:\n")
            for i, r in enumerate(redpackets, 1):
                print(f"[{i}] {r['name']}")
                print(f"    金额: {r['value']}")
                print(f"    使用条件: {r['limit']}")
                print(f"    有效期: {r['expiry']}\n")
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
