#!/usr/bin/env python3
"""
实时监控预警系统
Real-time Market Monitor & Alert System

功能:
- 价格监控：监控股票/加密货币价格
- 波动预警：大波动实时通知
- 支撑阻力突破：关键位置突破提醒
- 信号监控：买卖信号实时生成
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import urllib.request
import urllib.error

# Security: Removed sys.path manipulation to prevent importing external packages.
# This module is self-contained and does not import from sibling directories.
# Removed imports from config and i18n to ensure isolation.

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
ALERT_LOG_FILE = os.path.join(DATA_DIR, 'alert_log.json')
MONITOR_CONFIG_FILE = os.path.join(DATA_DIR, 'monitor_config.json')

class PriceAlert:
    """价格预警配置"""
    
    def __init__(self, symbol: str, alert_type: str, price: float, condition: str = 'above'):
        self.symbol = symbol.upper()
        self.alert_type = alert_type  # 'price', 'change', 'breakout'
        self.target_price = price
        self.condition = condition  # 'above', 'below', 'cross_above', 'cross_below'
        self.active = True
        self.created_at = datetime.now().isoformat()
        self.triggered_at = None
    
    def check(self, current_price: float) -> bool:
        """检查是否触发预警"""
        if not self.active:
            return False
        
        triggered = False
        
        if self.alert_type == 'price':
            if self.condition == 'above' and current_price >= self.target_price:
                triggered = True
            elif self.condition == 'below' and current_price <= self.target_price:
                triggered = True
        
        if triggered:
            self.active = False
            self.triggered_at = datetime.now().isoformat()
        
        return triggered
    
    def to_dict(self) -> dict:
        return {
            'symbol': self.symbol,
            'alert_type': self.alert_type,
            'target_price': self.target_price,
            'condition': self.condition,
            'active': self.active,
            'created_at': self.created_at,
            'triggered_at': self.triggered_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PriceAlert':
        alert = cls(
            data['symbol'],
            data['alert_type'],
            data['target_price'],
            data.get('condition', 'above')
        )
        alert.active = data.get('active', True)
        alert.created_at = data.get('created_at', datetime.now().isoformat())
        alert.triggered_at = data.get('triggered_at')
        return alert


class MarketMonitor:
    """市场监控器"""
    
    def __init__(self):
        self.watchlist = []
        self.alerts: List[PriceAlert] = []
        self.last_prices: Dict[str, float] = {}
        self.api_key = get_api_key('TWELVE_DATA')
        
        # 确保数据目录存在
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # 加载配置
        self.load_config()
    
    def load_config(self):
        """加载监控配置"""
        if os.path.exists(MONITOR_CONFIG_FILE):
            try:
                with open(MONITOR_CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.watchlist = config.get('watchlist', [])
                    self.alerts = [PriceAlert.from_dict(a) for a in config.get('alerts', [])]
            except Exception as e:
                print(f"⚠️ 加载配置失败：{e}")
    
    def save_config(self):
        """保存监控配置"""
        config = {
            'watchlist': self.watchlist,
            'alerts': [a.to_dict() for a in self.alerts],
            'last_updated': datetime.now().isoformat()
        }
        with open(MONITOR_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_price(self, symbol: str) -> Optional[float]:
        """获取实时价格"""
        try:
            # 尝试 Twelve Data
            if self.api_key:
                url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={self.api_key}"
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode())
                    if 'price' in data:
                        return float(data['price'])
            
            # 备选：Alpha Vantage
            av_key = get_api_key('ALPHA_VANTAGE')
            if av_key:
                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={av_key}"
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode())
                    quote = data.get('Global Quote', {})
                    price = quote.get('05. price')
                    if price:
                        return float(price)
            
            return None
        except Exception as e:
            print(f"⚠️ 获取 {symbol} 价格失败：{e}")
            return None
    
    def check_alerts(self, symbol: str, current_price: float) -> List[str]:
        """检查是否有预警触发"""
        triggered = []
        
        for alert in self.alerts:
            if alert.symbol == symbol and alert.check(current_price):
                msg = f"🚨 {symbol} 预警触发！"
                if alert.alert_type == 'price':
                    if alert.condition == 'above':
                        msg += f" 价格突破 ${alert.target_price} (当前：${current_price:.2f})"
                    else:
                        msg += f" 价格跌破 ${alert.target_price} (当前：${current_price:.2f})"
                triggered.append(msg)
        
        return triggered
    
    def check_volatility(self, symbol: str, current_price: float, threshold: float = 5.0) -> Optional[str]:
        """检查波动预警"""
        if symbol not in self.last_prices:
            self.last_prices[symbol] = current_price
            return None
        
        last_price = self.last_prices[symbol]
        change_pct = ((current_price - last_price) / last_price) * 100
        
        if abs(change_pct) >= threshold:
            direction = "📈" if change_pct > 0 else "📉"
            return f"{direction} {symbol} 大波动！{change_pct:+.2f}% (${last_price:.2f} → ${current_price:.2f})"
        
        self.last_prices[symbol] = current_price
        return None
    
    def add_alert(self, symbol: str, alert_type: str, price: float, condition: str = 'above'):
        """添加预警"""
        alert = PriceAlert(symbol, alert_type, price, condition)
        self.alerts.append(alert)
        self.save_config()
        print(f"✅ 已添加预警：{symbol} {condition} ${price}")
    
    def remove_alert(self, index: int):
        """移除预警"""
        if 0 <= index < len(self.alerts):
            removed = self.alerts.pop(index)
            self.save_config()
            print(f"✅ 已移除预警：{removed.symbol}")
    
    def list_alerts(self):
        """列出所有预警"""
        if not self.alerts:
            print("📭 暂无预警")
            return
        
        print("\n🔔 活跃预警:")
        for i, alert in enumerate(self.alerts):
            if alert.active:
                status = "⏳" if alert.active else "✅"
                print(f"  {i}. {status} {alert.symbol} {alert.condition} ${alert.target_price:.2f}")
        
        print("\n✅ 已触发预警:")
        for i, alert in enumerate(self.alerts):
            if not alert.active:
                print(f"  {i}. {alert.symbol} @ ${alert.target_price:.2f} ({alert.triggered_at})")
    
    def run_monitor(self, interval: int = 60):
        """运行监控循环"""
        print(f"🔍 开始监控 {len(self.watchlist)} 个标的，间隔 {interval} 秒...")
        print("按 Ctrl+C 停止\n")
        
        try:
            while True:
                for symbol in self.watchlist:
                    price = self.get_price(symbol)
                    if price:
                        # 检查预警
                        alerts = self.check_alerts(symbol, price)
                        for msg in alerts:
                            print(f"\n{msg}")
                            self.log_alert(msg)
                        
                        # 检查波动
                        vol_alert = self.check_volatility(symbol, price)
                        if vol_alert:
                            print(f"\n{vol_alert}")
                            self.log_alert(vol_alert)
                        
                        print(f"{symbol}: ${price:.2f}", end="  ")
                
                print()
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n⏹️  监控已停止")
            self.save_config()
    
    def log_alert(self, message: str):
        """记录预警到日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'message': message
        }
        
        logs = []
        if os.path.exists(ALERT_LOG_FILE):
            try:
                with open(ALERT_LOG_FILE, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(log_entry)
        
        # 保留最近 100 条
        logs = logs[-100:]
        
        with open(ALERT_LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='实时监控预警系统')
    parser.add_argument('--add', '-a', nargs=3, metavar=('SYMBOL', 'CONDITION', 'PRICE'),
                       help='添加预警 (例：AAPL above 150)')
    parser.add_argument('--list', '-l', action='store_true', help='列出预警')
    parser.add_argument('--remove', '-r', type=int, help='移除预警索引')
    parser.add_argument('--watchlist', '-w', nargs='+', help='设置监控列表')
    parser.add_argument('--interval', '-i', type=int, default=60, help='监控间隔 (秒)')
    parser.add_argument('--run', action='store_true', help='启动监控')
    
    args = parser.parse_args()
    
    monitor = MarketMonitor()
    
    if args.add:
        symbol, condition, price = args.add
        monitor.add_alert(symbol, 'price', float(price), condition)
    
    elif args.list:
        monitor.list_alerts()
    
    elif args.remove is not None:
        monitor.remove_alert(args.remove)
    
    elif args.watchlist:
        monitor.watchlist = [s.upper() for s in args.watchlist]
        monitor.save_config()
        print(f"✅ 监控列表：{monitor.watchlist}")
    
    elif args.run:
        if not monitor.watchlist:
            print("❌ 请先设置监控列表：--watchlist AAPL GOOGL TSLA")
            sys.exit(1)
        monitor.run_monitor(args.interval)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
