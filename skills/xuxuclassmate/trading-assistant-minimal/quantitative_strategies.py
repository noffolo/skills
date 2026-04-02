#!/usr/bin/env python3
"""
量化策略库
Quantitative Strategy Library

策略列表:
1. 多因子选股策略
2. 均值回归策略
3. 动量突破策略
4. 网格交易策略
"""

import os
import sys
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# Security: Removed sys.path manipulation to prevent importing external packages.
# This module is self-contained and does not import from sibling directories.


class MultiFactorStrategy:
    """
    多因子选股策略
    
    因子:
    1. 价值因子 (PE, PB)
    2. 成长因子 (营收增长，利润增长)
    3. 动量因子 (收益率)
    4. 质量因子 (ROE, 负债率)
    5. 技术因子 (RSI, MACD)
    """
    
    def __init__(self):
        self.factor_weights = {
            'value': 0.25,
            'growth': 0.25,
            'momentum': 0.20,
            'quality': 0.20,
            'technical': 0.10,
        }
    
    def calculate_factor_score(self, stock_data: Dict) -> Dict:
        """
        计算因子得分
        
        Args:
            stock_data: 股票数据
            
        Returns:
            各因子得分及总分
        """
        scores = {}
        
        # 1. 价值因子 (PE 越低分越高)
        pe = stock_data.get('pe_ratio', 50)
        scores['value'] = max(0, min(100, 100 - pe)) if pe > 0 else 50
        
        # 2. 成长因子 (营收增长率)
        revenue_growth = stock_data.get('revenue_growth', 0)
        scores['growth'] = min(100, max(0, 50 + revenue_growth * 2))
        
        # 3. 动量因子 (20 日收益率)
        return_20d = stock_data.get('return_20d', 0)
        scores['momentum'] = min(100, max(0, 50 + return_20d * 5))
        
        # 4. 质量因子 (ROE)
        roe = stock_data.get('roe', 0)
        scores['quality'] = min(100, max(0, roe * 5))
        
        # 5. 技术因子 (RSI)
        rsi = stock_data.get('rsi', 50)
        # RSI 在 30-70 之间最佳
        if 30 <= rsi <= 70:
            scores['technical'] = 70 + (1 - abs(rsi - 50) / 20) * 30
        elif rsi < 30:
            scores['technical'] = 80  # 超卖
        else:
            scores['technical'] = 20  # 超买
        
        # 计算加权总分
        total_score = sum(
            scores[factor] * weight 
            for factor, weight in self.factor_weights.items()
        )
        
        return {
            'scores': scores,
            'total_score': round(total_score, 2),
            'recommendation': self._get_recommendation(total_score)
        }
    
    def _get_recommendation(self, score: float) -> str:
        """根据得分给出建议"""
        if score >= 80:
            return 'STRONG_BUY'
        elif score >= 65:
            return 'BUY'
        elif score >= 50:
            return 'HOLD'
        elif score >= 35:
            return 'SELL'
        else:
            return 'STRONG_SELL'
    
    def rank_stocks(self, stocks: List[Dict]) -> List[Dict]:
        """
        对股票池排名
        
        Args:
            stocks: 股票数据列表
            
        Returns:
            排名结果
        """
        results = []
        
        for stock in stocks:
            factor_result = self.calculate_factor_score(stock)
            results.append({
                'symbol': stock.get('symbol', ''),
                'name': stock.get('name', ''),
                **factor_result
            })
        
        # 按总分排序
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        # 添加排名
        for i, result in enumerate(results):
            result['rank'] = i + 1
        
        return results


class MeanReversionStrategy:
    """
    均值回归策略
    
    原理:
    - 价格偏离均线过远时会回归
    - 使用 Z-Score 判断偏离程度
    """
    
    def __init__(self, lookback: int = 20, threshold: float = 2.0):
        self.lookback = lookback
        self.threshold = threshold
    
    def calculate_zscore(self, prices: List[float]) -> List[float]:
        """计算 Z-Score 序列"""
        if len(prices) < self.lookback:
            return []
        
        zscores = []
        
        for i in range(len(prices)):
            if i < self.lookback - 1:
                zscores.append(None)
                continue
            
            window = prices[i - self.lookback + 1:i + 1]
            mean = sum(window) / len(window)
            std = math.sqrt(sum((x - mean) ** 2 for x in window) / len(window))
            
            if std > 0:
                zscore = (prices[i] - mean) / std
            else:
                zscore = 0
            
            zscores.append(zscore)
        
        return zscores
    
    def generate_signals(self, prices: List[float], current_price: float) -> Dict:
        """
        生成交易信号
        
        Args:
            prices: 历史价格
            current_price: 当前价格
            
        Returns:
            交易信号
        """
        zscores = self.calculate_zscore(prices)
        
        if not zscores or zscores[-1] is None:
            return {'signal': 'HOLD', 'reason': '数据不足'}
        
        current_zscore = zscores[-1]
        
        if current_zscore < -self.threshold:
            return {
                'signal': 'STRONG_BUY',
                'reason': f'价格低于均值{abs(current_zscore):.2f}倍标准差',
                'confidence': min(abs(current_zscore) * 20, 100),
                'target': sum(prices[-self.lookback:]) / self.lookback,
            }
        elif current_zscore < -self.threshold * 0.8:
            return {
                'signal': 'BUY',
                'reason': f'价格低于均值{abs(current_zscore):.2f}倍标准差',
                'confidence': min(abs(current_zscore) * 20, 100),
                'target': sum(prices[-self.lookback:]) / self.lookback,
            }
        elif current_zscore > self.threshold:
            return {
                'signal': 'STRONG_SELL',
                'reason': f'价格高于均值{current_zscore:.2f}倍标准差',
                'confidence': min(current_zscore * 20, 100),
                'target': sum(prices[-self.lookback:]) / self.lookback,
            }
        elif current_zscore > self.threshold * 0.8:
            return {
                'signal': 'SELL',
                'reason': f'价格高于均值{current_zscore:.2f}倍标准差',
                'confidence': min(current_zscore * 20, 100),
                'target': sum(prices[-self.lookback:]) / self.lookback,
            }
        else:
            return {
                'signal': 'HOLD',
                'reason': '价格在均值附近',
                'confidence': 50,
            }


class MomentumBreakoutStrategy:
    """
    动量突破策略
    
    原理:
    - 价格突破 N 日高点时买入
    - 跌破 N 日低点时卖出
    """
    
    def __init__(self, lookback: int = 20):
        self.lookback = lookback
    
    def check_breakout(self, prices: List[float], volumes: List[float] = None) -> Dict:
        """
        检查突破信号
        
        Args:
            prices: 历史价格
            volumes: 历史成交量 (可选)
            
        Returns:
            突破信号
        """
        if len(prices) < self.lookback + 1:
            return {'signal': 'HOLD', 'reason': '数据不足'}
        
        current_price = prices[-1]
        prev_prices = prices[-self.lookback:-1]
        
        high_20d = max(prev_prices)
        low_20d = min(prev_prices)
        
        # 检查成交量放大
        volume_confirmed = False
        if volumes and len(volumes) >= self.lookback:
            avg_volume = sum(volumes[-self.lookback:-1]) / self.lookback
            current_volume = volumes[-1]
            volume_confirmed = current_volume > avg_volume * 1.5
        
        if current_price > high_20d:
            return {
                'signal': 'BUY',
                'type': 'BREAKOUT_HIGH',
                'reason': f'突破{self.lookback}日高点${high_20d:.2f}',
                'volume_confirmed': volume_confirmed,
                'confidence': 80 if volume_confirmed else 60,
                'target': high_20d * 1.1,
                'stop_loss': high_20d * 0.95,
            }
        elif current_price < low_20d:
            return {
                'signal': 'SELL',
                'type': 'BREAKOUT_LOW',
                'reason': f'跌破{self.lookback}日低点${low_20d:.2f}',
                'volume_confirmed': volume_confirmed,
                'confidence': 80 if volume_confirmed else 60,
                'target': low_20d * 0.9,
                'stop_loss': low_20d * 1.05,
            }
        else:
            return {
                'signal': 'HOLD',
                'reason': f'价格在{self.lookback}日区间内 (${low_20d:.2f} - ${high_20d:.2f})',
            }


class GridTradingStrategy:
    """
    网格交易策略
    
    原理:
    - 在价格区间内设置多个买卖点
    - 低买高卖赚取差价
    """
    
    def __init__(self, lower_bound: float, upper_bound: float, grid_num: int = 10):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.grid_num = grid_num
        self.grid_levels = self._calculate_grids()
    
    def _calculate_grids(self) -> List[Dict]:
        """计算网格位"""
        grid_size = (self.upper_bound - self.lower_bound) / self.grid_num
        
        grids = []
        for i in range(self.grid_num + 1):
            price = self.lower_bound + i * grid_size
            grids.append({
                'level': i,
                'price': round(price, 2),
                'action': 'SELL' if i > self.grid_num / 2 else 'BUY',
            })
        
        return grids
    
    def get_grid_signal(self, current_price: float, position: float = 0) -> Dict:
        """
        获取网格交易信号
        
        Args:
            current_price: 当前价格
            position: 当前持仓比例 (0-1)
            
        Returns:
            交易信号
        """
        if current_price <= self.lower_bound:
            return {
                'signal': 'STRONG_BUY',
                'reason': '价格触及网格底部',
                'suggested_action': '买入至 80% 仓位',
                'confidence': 90,
            }
        elif current_price >= self.upper_bound:
            return {
                'signal': 'STRONG_SELL',
                'reason': '价格触及网格顶部',
                'suggested_action': '卖出至 20% 仓位',
                'confidence': 90,
            }
        
        # 找到最近的网格位
        nearest_grid = min(self.grid_levels, 
                          key=lambda x: abs(x['price'] - current_price))
        
        distance = abs(current_price - nearest_grid['price'])
        grid_size = (self.upper_bound - self.lower_bound) / self.grid_num
        
        if distance < grid_size * 0.1:
            # 接近网格位
            if nearest_grid['action'] == 'BUY':
                return {
                    'signal': 'BUY',
                    'reason': f'接近网格买入位 ${nearest_grid["price"]:.2f}',
                    'suggested_action': '买入 10% 仓位',
                    'confidence': 70,
                }
            else:
                return {
                    'signal': 'SELL',
                    'reason': f'接近网格卖出位 ${nearest_grid["price"]:.2f}',
                    'suggested_action': '卖出 10% 仓位',
                    'confidence': 70,
                }
        
        return {
            'signal': 'HOLD',
            'reason': f'价格在网格中间 (最近网格位：${nearest_grid["price"]:.2f})',
        }


def demo_strategies():
    """演示各策略"""
    print("\n" + "=" * 60)
    print("量化策略演示")
    print("=" * 60)
    
    # 1. 多因子选股
    print("\n📊 1. 多因子选股策略")
    stocks = [
        {'symbol': 'AAPL', 'pe_ratio': 25, 'revenue_growth': 0.08, 'return_20d': 0.05, 'roe': 0.25, 'rsi': 55},
        {'symbol': 'GOOGL', 'pe_ratio': 20, 'revenue_growth': 0.12, 'return_20d': 0.03, 'roe': 0.20, 'rsi': 45},
        {'symbol': 'TSLA', 'pe_ratio': 60, 'revenue_growth': 0.30, 'return_20d': 0.15, 'roe': 0.15, 'rsi': 70},
    ]
    
    mf = MultiFactorStrategy()
    results = mf.rank_stocks(stocks)
    
    for r in results:
        print(f"   #{r['rank']} {r['symbol']}: {r['total_score']}分 -> {r['recommendation']}")
    
    # 2. 均值回归
    print("\n📈 2. 均值回归策略")
    prices = [100, 102, 98, 101, 99, 103, 97, 100, 102, 98, 95, 93, 90, 92, 94]
    mr = MeanReversionStrategy(lookback=10, threshold=1.5)
    signal = mr.generate_signals(prices, prices[-1])
    print(f"   信号：{signal['signal']}")
    print(f"   原因：{signal['reason']}")
    
    # 3. 动量突破
    print("\n🚀 3. 动量突破策略")
    prices = [100, 102, 101, 103, 102, 104, 103, 105, 104, 106, 105, 107, 108, 110, 112]
    mo = MomentumBreakoutStrategy(lookback=10)
    signal = mo.check_breakout(prices)
    print(f"   信号：{signal['signal']}")
    print(f"   原因：{signal['reason']}")
    
    # 4. 网格交易
    print("\n🕸️  4. 网格交易策略")
    grid = GridTradingStrategy(lower_bound=90, upper_bound=110, grid_num=10)
    signal = grid.get_grid_signal(current_price=95)
    print(f"   信号：{signal['signal']}")
    print(f"   原因：{signal['reason']}")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    demo_strategies()
