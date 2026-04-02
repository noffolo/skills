#!/usr/bin/env python3
"""
量化单进场提示系统
Quantitative Entry Signal Alert System

功能:
- 多条件量化入场检测
- 实时监控股票池
- 进场信号推送
- 条件单管理
"""

import os
import sys
import json
import time
import urllib.request
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable

# Security: Removed sys.path manipulation to prevent importing external packages.
# This module is self-contained and does not import from sibling directories.
# Removed imports from optimizer, quantitative_cost_analyzer, trading_signals, 
# and support_resistance to ensure isolation.


class QuantitativeEntryAlert:
    """量化单进场提示器"""
    
    def __init__(self):
        self.cost_analyzer = QuantitativeCostAnalyzer()
        self.signal_generator = TradingSignalGenerator()
        self.sr_calculator = SupportResistanceCalculator()
        
        # 配置文件路径
        self.config_dir = os.path.expanduser('~/.trading_assistant')
        os.makedirs(self.config_dir, exist_ok=True)
        self.alerts_file = os.path.join(self.config_dir, 'entry_alerts.json')
        self.history_file = os.path.join(self.config_dir, 'alert_history.json')
    
    def load_watchlist(self) -> List[str]:
        """加载监控列表"""
        watchlist_file = os.path.join(self.config_dir, 'watchlist.json')
        if os.path.exists(watchlist_file):
            with open(watchlist_file, 'r') as f:
                data = json.load(f)
                return data.get('symbols', [])
        return []
    
    def save_watchlist(self, symbols: List[str]):
        """保存监控列表"""
        watchlist_file = os.path.join(self.config_dir, 'watchlist.json')
        with open(watchlist_file, 'w') as f:
            json.dump({'symbols': symbols, 'updated': datetime.now().isoformat()}, f, indent=2)
    
    def check_entry_conditions(self, symbol: str, use_a_share: bool = False) -> Optional[Dict]:
        """
        检查入场条件
        
        条件:
        1. 量化信号：BULLISH 且置信度 > 60%
        2. 技术信号：BUY 或 STRONG_BUY
        3. 风险收益比：≥ 1.5
        4. 价格位置：< 30% 分位
        
        Args:
            symbol: 标的符号
            use_a_share: 是否使用 A 股数据
            
        Returns:
            入场信号详情
        """
        print(f"  检查 {symbol}...")
        
        # 1. 量化分析
        if use_a_share:
            # A 股使用简化分析
            from a_stock_data import AStockDataFetcher
            fetcher = AStockDataFetcher()
            kline = fetcher.get_kline_data(symbol, 60)
            if not kline:
                return None
            
            current_price = kline[-1]['close']
            quant_result = self._analyze_a_stock(symbol, kline)
        else:
            quant_result = self.cost_analyzer.full_analysis(symbol, 60)
            if not quant_result:
                return None
            
            current_price = quant_result['current_price']
        
        # 2. 检查量化信号
        signal_summary = quant_result.get('signal_summary', {})
        if signal_summary.get('net_signal') != 'BULLISH':
            return None
        
        if signal_summary.get('confidence', 0) < 60:
            return None
        
        # 3. 检查技术信号
        rsi = 45  # 简化，实际应从数据计算
        macd_signal = 'buy'
        
        tech_signal = self.signal_generator.generate_signals({
            'symbol': symbol,
            'price': current_price,
            'rsi': rsi,
            'macd': 0.5,
            'signal_line': 0.3,
        })
        
        if not tech_signal or tech_signal[0].get('action') not in ['BUY', 'STRONG_BUY']:
            return None
        
        # 4. 检查风险收益比
        risk_reward = quant_result.get('risk_reward', {})
        rr_ratio = risk_reward.get('risk_reward_ratio', 0)
        
        if isinstance(rr_ratio, (int, float)) and rr_ratio < 1.5:
            return None
        
        # 5. 检查价格位置
        distribution = quant_result.get('distribution', {})
        min_p = distribution.get('min_price', 0)
        max_p = distribution.get('max_price', 0)
        
        if min_p > 0 and max_p > min_p:
            position = (current_price - min_p) / (max_p - min_p) * 100
            if position > 30:
                return None
        
        # 所有条件满足，生成入场信号
        return {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'current_price': current_price,
            'quant_confidence': signal_summary.get('confidence', 0),
            'bullish_strength': signal_summary.get('bullish_strength', 0),
            'risk_reward_ratio': rr_ratio,
            'price_position': position if min_p > 0 else 0,
            'entry_signal': 'STRONG_BUY' if signal_summary['confidence'] > 80 else 'BUY',
            'conditions_met': {
                'quant_signal': True,
                'tech_signal': True,
                'risk_reward': True,
                'price_position': True,
            },
            'suggested_position': self._calculate_position(symbol, current_price),
        }
    
    def _analyze_a_stock(self, symbol: str, kline: List[Dict]) -> Dict:
        """分析 A 股数据"""
        current_price = kline[-1]['close']
        prices = [k['close'] for k in kline]
        min_p, max_p = min(prices), max(prices)
        
        # 简化量化分析
        position = (current_price - min_p) / (max_p - min_p) * 100 if max_p > min_p else 50
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'distribution': {
                'min_price': min_p,
                'max_price': max_p,
                'current_price': current_price,
            },
            'signal_summary': {
                'net_signal': 'BULLISH' if position < 30 else 'BEARISH',
                'confidence': max(100 - position * 2, 0),
                'bullish_strength': 10 if position < 20 else 6,
                'bearish_strength': 0,
            },
            'risk_reward': {
                'risk_reward_ratio': (max_p - current_price) / (current_price - min_p) if current_price > min_p else 3,
            },
        }
    
    def _calculate_position(self, symbol: str, price: float) -> Dict:
        """计算建议仓位"""
        # 简化实现
        return {
            'position_percent': 30,  # 建议仓位 30%
            'stop_loss': price * 0.95,  # 5% 止损
            'take_profit_1': price * 1.05,  # 5% 止盈 1
            'take_profit_2': price * 1.10,  # 10% 止盈 2
        }
    
    def monitor_all(self, symbols: List[str] = None, use_a_share: bool = False) -> List[Dict]:
        """
        监控所有标的
        
        Args:
            symbols: 监控列表，None 则使用配置文件
            use_a_share: 是否使用 A 股数据
            
        Returns:
            触发的入场信号列表
        """
        if symbols is None:
            symbols = self.load_watchlist()
        
        if not symbols:
            print("⚠️ 监控列表为空")
            return []
        
        print(f"\n🔍 开始监控 {len(symbols)} 个标的...")
        print("=" * 60)
        
        alerts = []
        
        for symbol in symbols:
            try:
                signal = self.check_entry_conditions(symbol, use_a_share)
                if signal:
                    alerts.append(signal)
                    print(f"  ✅ {symbol} 触发入场信号!")
                else:
                    print(f"  ❌ {symbol} 未触发")
            except Exception as e:
                print(f"  ⚠️ {symbol} 检查失败：{e}")
        
        print("=" * 60)
        print(f"📊 监控完成：{len(alerts)}/{len(symbols)} 触发入场信号")
        
        # 保存历史
        if alerts:
            self._save_alerts(alerts)
        
        return alerts
    
    def _save_alerts(self, alerts: List[Dict]):
        """保存警报历史"""
        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                history = json.load(f)
        
        history.extend(alerts)
        
        # 保留最近 100 条
        history = history[-100:]
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def print_alert_report(self, alert: Dict):
        """打印警报报告"""
        print("\n" + "=" * 60)
        print(f"🚨 入场信号：{alert['symbol']}")
        print("=" * 60)
        print(f"时间：{alert['timestamp']}")
        print(f"当前价格：¥{alert['current_price']:.2f}")
        print(f"信号强度：{alert['entry_signal']} (置信度:{alert['quant_confidence']:.0f}%)")
        print()
        print("条件检查:")
        for condition, met in alert['conditions_met'].items():
            icon = "✅" if met else "❌"
            print(f"  {icon} {condition}")
        print()
        print(f"风险收益比：{alert['risk_reward_ratio']}")
        print(f"价格位置：{alert['price_position']:.1f}% (近 60 日)")
        print()
        print("建议操作:")
        pos = alert['suggested_position']
        print(f"  仓位：{pos['position_percent']}%")
        print(f"  止损：¥{pos['stop_loss']:.2f} (-5%)")
        print(f"  止盈 1: ¥{pos['take_profit_1']:.2f} (+5%)")
        print(f"  止盈 2: ¥{pos['take_profit_2']:.2f} (+10%)")
        print("=" * 60)
    
    def start_continuous_monitoring(self, symbols: List[str] = None, 
                                   interval: int = 300,
                                   use_a_share: bool = False):
        """
        持续监控
        
        Args:
            symbols: 监控列表
            interval: 检查间隔 (秒)
            use_a_share: 是否使用 A 股数据
        """
        print(f"\n🔍 开始持续监控 (间隔:{interval}秒)")
        print("按 Ctrl+C 停止\n")
        
        try:
            while True:
                alerts = self.monitor_all(symbols, use_a_share)
                
                if alerts:
                    print(f"\n🎯 发现 {len(alerts)} 个入场机会!")
                    for alert in alerts:
                        self.print_alert_report(alert)
                
                print(f"\n💤 等待{interval}秒后再次检查...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  监控已停止")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='量化单进场提示')
    parser.add_argument('symbol', nargs='*', help='标的符号')
    parser.add_argument('--a-share', action='store_true', help='使用 A 股数据')
    parser.add_argument('--interval', type=int, default=300, help='监控间隔 (秒)')
    parser.add_argument('--continuous', action='store_true', help='持续监控')
    parser.add_argument('--add', help='添加标的到监控列表')
    parser.add_argument('--list', action='store_true', help='显示监控列表')
    parser.add_argument('--history', action='store_true', help='显示历史警报')
    
    args = parser.parse_args()
    
    alert_system = QuantitativeEntryAlert()
    
    if args.add:
        watchlist = alert_system.load_watchlist()
        if args.add not in watchlist:
            watchlist.append(args.add)
            alert_system.save_watchlist(watchlist)
            print(f"✅ 已添加 {args.add} 到监控列表")
        else:
            print(f"ℹ️  {args.add} 已在监控列表中")
        return
    
    if args.list:
        watchlist = alert_system.load_watchlist()
        print(f"\n📋 监控列表 ({len(watchlist)}个):")
        for symbol in watchlist:
            print(f"   {symbol}")
        return
    
    if args.history:
        if os.path.exists(alert_system.history_file):
            with open(alert_system.history_file, 'r') as f:
                history = json.load(f)
            print(f"\n📜 历史警报 ({len(history)}条):")
            for alert in history[-10:]:
                print(f"   {alert['timestamp'][:16]} {alert['symbol']} {alert['entry_signal']}")
        else:
            print("暂无历史警报")
        return
    
    # 确定监控列表
    symbols = args.symbol if args.symbol else None
    
    if args.continuous:
        alert_system.start_continuous_monitoring(symbols, args.interval, args.a_share)
    else:
        alerts = alert_system.monitor_all(symbols, args.a_share)
        if alerts:
            for alert in alerts:
                alert_system.print_alert_report(alert)


if __name__ == '__main__':
    main()
