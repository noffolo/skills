#!/usr/bin/env python3
"""
持仓成本分析模块
Position Cost Basis Analysis

功能:
- 估算市场平均持仓成本
- 链上数据分析 (加密货币)
- 机构持仓分析 (美股)
- 成本支撑/阻力位计算
"""

import os
import sys
import json
import urllib.request
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Security: Removed sys.path manipulation to prevent importing external packages.
# This module is self-contained and does not import from sibling directories.
# Removed imports from config and optimizer to ensure isolation.


class PositionCostAnalyzer:
    """持仓成本分析器"""
    
    def __init__(self):
        self.api_key = get_api_key('TWELVE_DATA')
    
    def get_crypto_onchain_data(self, symbol: str) -> Optional[dict]:
        """
        获取加密货币链上数据
        
        数据来源:
        - Glassnode (付费)
        - CryptoQuant (部分免费)
        - Dune Analytics (社区)
        
        Args:
            symbol: 加密货币符号 (BTC, ETH)
            
        Returns:
            链上数据字典
        """
        # 免费替代方案：使用 CoinGecko 基础数据
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{symbol.lower()}"
            req = urllib.request.Request(url)
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                
                return {
                    'symbol': symbol.upper(),
                    'current_price': data.get('market_data', {}).get('current_price', {}).get('usd'),
                    'market_cap': data.get('market_data', {}).get('market_cap', {}).get('usd'),
                    'total_volume': data.get('market_data', {}).get('total_volume', {}).get('usd'),
                    'circulating_supply': data.get('market_data', {}).get('circulating_supply'),
                    # 估算数据
                    'estimated_avg_cost': self._estimate_crypto_avg_cost(data),
                    'realized_cap': data.get('market_data', {}).get('market_cap', {}).get('usd'),  # 简化
                }
        except Exception as e:
            print(f"⚠️ 获取链上数据失败：{e}")
            return None
    
    def _estimate_crypto_avg_cost(self, data: dict) -> Optional[float]:
        """
        估算加密货币平均持仓成本
        
        方法:
        1. 使用已实现市值 / 流通供应量
        2. 简化模型：假设平均成本为当前价格的 80-90%
        """
        current_price = data.get('market_data', {}).get('current_price', {}).get('usd')
        
        if not current_price:
            return None
        
        # 简化估算：平均成本约为当前价格的 85%
        # 实际应该使用链上数据 (UTXO 年龄分布、已实现价格等)
        estimated_avg = current_price * 0.85
        
        return round(estimated_avg, 2)
    
    def get_stock_institutional_holdings(self, symbol: str) -> Optional[dict]:
        """
        获取美股机构持仓数据
        
        数据来源:
        - SEC 13F  filings (免费但延迟)
        - Alpha Vantage (部分免费)
        - Yahoo Finance (非官方)
        
        Args:
            symbol: 股票代码
            
        Returns:
            机构持仓数据
        """
        # 使用 Alpha Vantage
        av_key = get_api_key('ALPHA_VANTAGE')
        
        if not av_key:
            print("⚠️ 未配置 Alpha Vantage API Key")
            return None
        
        try:
            url = f"https://www.alphavantage.co/query?function=INSTITUTIONAL_HOLDINGS&symbol={symbol}&apikey={av_key}"
            req = urllib.request.Request(url)
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                
                holdings = data.get('holdings', [])
                
                if not holdings:
                    return None
                
                # 计算机构持仓统计
                total_shares = sum(int(h.get('shares', 0)) for h in holdings[:10])  # 前 10 大
                total_value = sum(float(h.get('value', 0)) for h in holdings[:10])
                
                return {
                    'symbol': symbol,
                    'num_institutions': len(holdings),
                    'top_10_shares': total_shares,
                    'top_10_value': total_value,
                    'avg_cost_estimate': self._estimate_stock_avg_cost(holdings),
                    'last_updated': data.get('updated', ''),
                }
        except Exception as e:
            print(f"⚠️ 获取机构持仓失败：{e}")
            return None
    
    def _estimate_stock_avg_cost(self, holdings: list) -> Optional[float]:
        """
        估算股票平均持仓成本
        
        方法:
        1. 使用加权平均价格
        2. 基于 SEC 13F 报告的持仓变化
        """
        if not holdings:
            return None
        
        total_shares = 0
        total_value = 0
        
        for h in holdings[:10]:  # 前 10 大机构
            shares = int(h.get('shares', 0))
            value = float(h.get('value', 0))
            
            total_shares += shares
            total_value += value
        
        if total_shares == 0:
            return None
        
        return round(total_value / total_shares, 2)
    
    def calculate_cost_support_resistance(self, symbol: str, asset_type: str = 'crypto') -> Optional[dict]:
        """
        计算基于持仓成本的支撑/阻力位
        
        Args:
            symbol: 标的符号
            asset_type: 资产类型 (crypto/stock)
            
        Returns:
            成本支撑/阻力位数据
        """
        if asset_type == 'crypto':
            data = self.get_crypto_onchain_data(symbol)
        else:
            data = self.get_stock_institutional_holdings(symbol)
        
        if not data or not data.get('estimated_avg_cost'):
            return None
        
        avg_cost = data['estimated_avg_cost']
        current_price = data.get('current_price')
        
        if not current_price:
            return None
        
        # 计算成本支撑/阻力位
        return {
            'symbol': symbol,
            'current_price': current_price,
            'average_cost': avg_cost,
            'profit_ratio': ((current_price - avg_cost) / avg_cost) * 100,
            'support_levels': [
                avg_cost * 0.9,  # -10%
                avg_cost * 0.8,  # -20%
                avg_cost * 0.7,  # -30%
            ],
            'resistance_levels': [
                avg_cost * 1.1,  # +10%
                avg_cost * 1.2,  # +20%
                avg_cost * 1.3,  # +30%
            ],
            'signal': self._generate_cost_signal(current_price, avg_cost),
        }
    
    def _generate_cost_signal(self, current_price: float, avg_cost: float) -> dict:
        """
        基于持仓成本生成交易信号
        
        Args:
            current_price: 当前价格
            avg_cost: 平均持仓成本
            
        Returns:
            交易信号
        """
        ratio = (current_price - avg_cost) / avg_cost
        
        if ratio < -0.2:
            # 低于平均成本 20% 以上 - 可能超卖
            signal = 'STRONG_BUY'
            reason = f"价格低于平均持仓成本{abs(ratio)*100:.1f}%"
        elif ratio < -0.1:
            signal = 'BUY'
            reason = f"价格低于平均持仓成本{abs(ratio)*100:.1f}%"
        elif ratio < 0.1:
            signal = 'HOLD'
            reason = "价格在平均持仓成本附近"
        elif ratio < 0.3:
            signal = 'SELL'
            reason = f"价格高于平均持仓成本{ratio*100:.1f}%"
        else:
            signal = 'STRONG_SELL'
            reason = f"价格远高于平均持仓成本{ratio*100:.1f}%"
        
        return {
            'action': signal,
            'reason': reason,
            'confidence': min(abs(ratio) * 200, 100),  # 偏离越大，置信度越高
        }
    
    def get_whale_alerts(self, symbol: str) -> List[dict]:
        """
        获取大户持仓变动警报
        
        Args:
            symbol: 标的符号
            
        Returns:
            大户警报列表
        """
        # 简化实现：返回模拟数据
        # 实际应该接入 Whale Alert API 或链上数据
        return [
            {
                'timestamp': datetime.now().isoformat(),
                'type': 'accumulation',
                'description': f"大户正在积累 {symbol}",
                'confidence': 'medium'
            }
        ]


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='持仓成本分析')
    parser.add_argument('symbol', help='标的符号 (BTC, ETH, AAPL, TSLA)')
    parser.add_argument('--type', choices=['crypto', 'stock'], default='crypto',
                       help='资产类型')
    parser.add_argument('--support-resistance', action='store_true',
                       help='计算成本支撑/阻力位')
    
    args = parser.parse_args()
    
    analyzer = PositionCostAnalyzer()
    
    if args.support_resistance:
        result = analyzer.calculate_cost_support_resistance(args.symbol, args.type)
        
        if result:
            print(f"\n📊 {result['symbol']} 持仓成本分析")
            print("=" * 50)
            print(f"当前价格：${result['current_price']:,.2f}")
            print(f"平均持仓成本：${result['average_cost']:,.2f}")
            print(f"盈亏比例：{result['profit_ratio']:+.1f}%")
            print()
            print(f"支撑位:")
            for i, level in enumerate(result['support_levels'], 1):
                print(f"  S{i}: ${level:,.2f}")
            print(f"\n阻力位:")
            for i, level in enumerate(result['resistance_levels'], 1):
                print(f"  R{i}: ${level:,.2f}")
            print()
            print(f"🎯 信号：{result['signal']['action']}")
            print(f"   原因：{result['signal']['reason']}")
            print(f"   置信度：{result['signal']['confidence']:.0f}%")
            print("=" * 50)
        else:
            print("❌ 无法获取数据")
    else:
        if args.type == 'crypto':
            data = analyzer.get_crypto_onchain_data(args.symbol)
        else:
            data = analyzer.get_stock_institutional_holdings(args.symbol)
        
        if data:
            print(f"\n📊 {args.symbol} 持仓数据")
            print("=" * 50)
            for key, value in data.items():
                if isinstance(value, float):
                    print(f"{key}: ${value:,.2f}")
                else:
                    print(f"{key}: {value}")
            print("=" * 50)
        else:
            print("❌ 无法获取数据")


if __name__ == '__main__':
    main()
