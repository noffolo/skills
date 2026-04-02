#!/usr/bin/env python3
"""
实盘交易接口
Live Trading Interface

免注册/低门槛 API:
1. Binance (加密货币) - 无需注册可读取公开数据
2. CoinGecko (加密货币) - 完全免费，无需 API Key
3. 新浪财经 (A 股/港股/美股) - 完全免费，无需 API Key
4. Alpha Vantage (美股) - 免费层 25 次/天
5. Twelve Data (全球) - 免费层 800 次/天
"""

import os
import sys
import json
import hashlib
import hmac
import time
import urllib.request
import urllib.parse
import re
from datetime import datetime
from typing import Dict, List, Optional

# Security: Removed sys.path manipulation to prevent importing external packages.
# This module is self-contained and does not import from sibling directories.


class LiveTradingInterface:
    """实盘交易接口"""
    
    def __init__(self):
        self.config_dir = os.path.expanduser('~/.trading_assistant')
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_file = os.path.join(self.config_dir, 'trading_config.json')
    
    def load_config(self) -> Dict:
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_config(self, config: Dict):
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get_binance_ticker(self, symbol: str) -> Optional[Dict]:
        """Binance 实时行情 (无需 API Key)"""
        try:
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol.upper()}"
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                return {
                    'symbol': data.get('symbol', ''),
                    'price': float(data.get('lastPrice', 0)),
                    'change_percent': float(data.get('priceChangePercent', 0)),
                    'high_24h': float(data.get('highPrice', 0)),
                    'low_24h': float(data.get('lowPrice', 0)),
                    'volume_24h': float(data.get('volume', 0)),
                }
        except Exception as e:
            return None
    
    def get_binance_kline(self, symbol: str, interval: str = '1d', limit: int = 60) -> Optional[List[Dict]]:
        """Binance K 线 (无需 API Key)"""
        try:
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol.upper()}&interval={interval}&limit={limit}"
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                return [{
                    'timestamp': datetime.fromtimestamp(item[0] / 1000).isoformat(),
                    'open': float(item[1]),
                    'high': float(item[2]),
                    'low': float(item[3]),
                    'close': float(item[4]),
                    'volume': float(item[5]),
                } for item in data]
        except:
            return None
    
    def get_coingecko_price(self, coin_id: str) -> Optional[Dict]:
        """CoinGecko 价格 (完全免费)"""
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                if coin_id in data:
                    return {
                        'symbol': coin_id,
                        'price': data[coin_id].get('usd', 0),
                        'change_24h': data[coin_id].get('usd_24h_change', 0),
                    }
        except:
            return None
    
    def get_sina_quote(self, symbol: str) -> Optional[Dict]:
        """新浪财经 (A 股/港股/美股，完全免费)"""
        try:
            url = f"http://hq.sinajs.cn/list={symbol}"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode('gbk')
                match = re.search(r'= "([^"]+)"', content)
                if match:
                    data_str = match.group(1).split(',')
                    if len(data_str) >= 4:
                        return {
                            'symbol': symbol,
                            'name': data_str[0],
                            'current': float(data_str[3]) if data_str[3] else 0,
                            'change_percent': ((float(data_str[3]) / float(data_str[2]) - 1) * 100) if data_str[2] else 0,
                        }
        except:
            return None
    
    def place_simulated_order(self, symbol: str, side: str, amount: float, price: float = None) -> Dict:
        """模拟下单"""
        order = {
            'order_id': f"SIM_{int(time.time() * 1000)}",
            'symbol': symbol,
            'side': side,
            'type': 'MARKET' if price is None else 'LIMIT',
            'amount': amount,
            'status': 'FILLED',
        }
        print(f"📝 模拟订单：{side} {amount} {symbol}")
        return order
    
    def show_api_info(self):
        """显示 API 信息"""
        print("\n" + "=" * 60)
        print("📡 实盘接口信息")
        print("=" * 60)
        print("\n✅ 免注册接口 (立即使用):")
        print("   • Binance - 加密货币行情/K 线")
        print("   • CoinGecko - 加密货币价格")
        print("   • 新浪财经 - A 股/港股/美股行情")
        print("\n⚠️  需要 API Key (可选):")
        print("   • Alpha Vantage - 美股 (25 次/天)")
        print("   • Twelve Data - 全球市场 (800 次/天)")
        print("   • Binance - 加密货币实盘交易")
        print("=" * 60)


def main():
    interface = LiveTradingInterface()
    interface.show_api_info()
    
    # 测试免注册接口
    print("\n🧪 测试接口...")
    
    print("\n1. Binance BTC 行情:")
    ticker = interface.get_binance_ticker('BTCUSDT')
    if ticker:
        print(f"   价格：${ticker['price']:,.2f}")
        print(f"   24h: {ticker['change_percent']:+.2f}%")
    
    print("\n2. CoinGecko BTC 价格:")
    price = interface.get_coingecko_price('bitcoin')
    if price:
        print(f"   价格：${price['price']:,.2f}")
        print(f"   24h: {price['change_24h']:+.2f}%")
    
    print("\n3. 新浪财经 贵州茅台:")
    quote = interface.get_sina_quote('sh600519')
    if quote:
        print(f"   {quote['name']}: ¥{quote['current']:.2f}")
        print(f"   涨跌：{quote['change_percent']:+.2f}%")
    
    print("\n✅ 测试完成")


if __name__ == '__main__':
    main()
