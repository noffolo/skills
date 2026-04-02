#!/usr/bin/env python3
"""
量化持仓成本分析
Quantitative Position Cost Analysis

融合量化交易策略的持仓成本分析系统
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


class QuantitativeCostAnalyzer:
    """量化持仓成本分析器"""
    
    def __init__(self):
        self.config = Config()
    
    def get_price_history(self, symbol: str, days: int = 60) -> Optional[List[dict]]:
        """获取历史价格数据"""
        cached = api_cache.get('history', {'symbol': symbol, 'days': days})
        if cached:
            return cached
        
        try:
            api_key = self.config.api_keys.get('TWELVE_DATA', '')
            if not api_key:
                return None
            
            url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize={days}&apikey={api_key}"
            req = urllib.request.Request(url)
            
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
                
                if 'values' not in data:
                    return None
                
                history = []
                for item in data['values'][:days]:
                    history.append({
                        'datetime': item.get('datetime', ''),
                        'open': float(item.get('open', 0)),
                        'high': float(item.get('high', 0)),
                        'low': float(item.get('low', 0)),
                        'close': float(item.get('close', 0)),
                        'volume': int(item.get('volume', 0))
                    })
                
                api_cache.set('history', {'symbol': symbol, 'days': days}, history)
                return history
                
        except Exception as e:
            print(f"⚠️ 获取历史数据失败：{e}")
            return None
    
    def calculate_cost_distribution(self, history: List[dict]) -> Dict:
        """计算成本分布（筹码分布）"""
        if not history:
            return {}
        
        prices = [h['close'] for h in history]
        min_price, max_price = min(prices), max(prices)
        price_range = max_price - min_price
        
        if price_range == 0:
            return {}
        
        num_bins = 20
        bin_size = price_range / num_bins
        chip_distribution = {}
        total_volume = sum(h['volume'] for h in history)
        
        for bar in history:
            typical_price = (bar['high'] + bar['low'] + bar['close']) / 3
            bin_index = int((typical_price - min_price) / bin_size)
            bin_index = min(bin_index, num_bins - 1)
            bin_price = round(min_price + bin_index * bin_size, 2)
            
            chip_distribution[bin_price] = chip_distribution.get(bin_price, 0) + bar['volume']
        
        sorted_chips = sorted(chip_distribution.items(), key=lambda x: x[1], reverse=True)
        sorted_by_price = sorted(chip_distribution.items(), key=lambda x: float(x[0]))
        
        cumulative = 0
        concentration_low = concentration_high = None
        
        for price, volume in sorted_by_price:
            cumulative += volume
            if concentration_low is None and cumulative >= total_volume * 0.15:
                concentration_low = float(price)
            if concentration_high is None and cumulative >= total_volume * 0.85:
                concentration_high = float(price)
                break
        
        peak_price, peak_volume = sorted_chips[0] if sorted_chips else (0, 0)
        peak_ratio = (peak_volume / total_volume * 100) if total_volume > 0 else 0
        
        return {
            'distribution': chip_distribution,
            'min_price': min_price,
            'max_price': max_price,
            'current_price': history[-1]['close'] if history else 0,
            'concentration_range': [concentration_low, concentration_high],
            'peak_price': float(peak_price),
            'peak_ratio': round(peak_ratio, 2),
            'total_volume': total_volume,
        }
    
    def estimate_main_force_cost(self, history: List[dict]) -> Optional[Dict]:
        """估算主力成本"""
        if len(history) < 20:
            return None
        
        volumes = [h['volume'] for h in history]
        avg_volume = sum(volumes) / len(volumes)
        
        high_volume_days = []
        for bar in history:
            if bar['volume'] > avg_volume * 2:
                typical_price = (bar['high'] + bar['low'] + bar['close']) / 3
                high_volume_days.append({'price': typical_price, 'volume': bar['volume']})
        
        if not high_volume_days:
            avg_cost = sum(h['close'] for h in history) / len(history)
            return {'estimated_cost': round(avg_cost, 2), 'method': 'average', 'confidence': 'medium'}
        
        total_pv = sum(d['price'] * d['volume'] for d in high_volume_days)
        total_volume = sum(d['volume'] for d in high_volume_days)
        main_cost = total_pv / total_volume if total_volume > 0 else 0
        
        return {
            'estimated_cost': round(main_cost, 2),
            'high_volume_days': len(high_volume_days),
            'main_volume_ratio': round(total_volume / sum(volumes) * 100, 2),
            'method': 'high_volume_weighted',
            'confidence': 'high' if len(high_volume_days) >= 3 else 'medium'
        }
    
    def calculate_profit_ratio(self, current_price: float, distribution: Dict) -> Dict:
        """计算获利盘比例"""
        chip_dist = distribution.get('distribution', {})
        if not chip_dist:
            return {}
        
        total_chips = sum(chip_dist.values())
        if total_chips == 0:
            return {}
        
        profit_chips = sum(vol for price, vol in chip_dist.items() if float(price) < current_price)
        loss_chips = total_chips - profit_chips
        
        return {
            'profit_ratio': round(profit_chips / total_chips * 100, 2),
            'loss_ratio': round(loss_chips / total_chips * 100, 2),
        }
    
    def generate_quantitative_signals(self, result: Dict) -> List[Dict]:
        """生成量化交易信号"""
        signals = []
        current_price = result.get('current_price', 0)
        distribution = result.get('distribution', {})
        main_cost_data = result.get('main_force_cost', {})
        profit_data = result.get('profit_ratio', {})
        
        # 筹码集中度信号
        peak_ratio = distribution.get('peak_ratio', 0)
        if peak_ratio > 15:
            signals.append({'type': 'chip_concentration', 'signal': 'BULLISH',
                          'reason': f'筹码高度集中 (峰值占比{peak_ratio}%)', 'strength': min(peak_ratio / 5, 10)})
        
        # 获利盘信号
        profit_ratio = profit_data.get('profit_ratio', 0)
        if profit_ratio < 10:
            signals.append({'type': 'oversold', 'signal': 'BULLISH',
                          'reason': f'获利盘仅{profit_ratio}%，市场超卖', 'strength': 8})
        elif profit_ratio > 90:
            signals.append({'type': 'overbought', 'signal': 'BEARISH',
                          'reason': f'获利盘{profit_ratio}%，市场超买', 'strength': 8})
        
        # 主力成本信号
        if main_cost_data:
            main_cost = main_cost_data.get('estimated_cost', 0)
            if main_cost > 0:
                price_vs_main = ((current_price - main_cost) / main_cost) * 100
                if price_vs_main < -15:
                    signals.append({'type': 'main_discount', 'signal': 'STRONG_BULLISH',
                                  'reason': f'价格低于主力成本{abs(price_vs_main):.1f}%', 'strength': 9})
                elif price_vs_main < -5:
                    signals.append({'type': 'main_slight_discount', 'signal': 'BULLISH',
                                  'reason': f'价格低于主力成本{abs(price_vs_main):.1f}%', 'strength': 6})
                elif price_vs_main > 30:
                    signals.append({'type': 'main_premium', 'signal': 'BEARISH',
                                  'reason': f'价格高于主力成本{price_vs_main:.1f}%', 'strength': 7})
        
        # 价格位置信号
        min_p, max_p = distribution.get('min_price', 0), distribution.get('max_price', 0)
        if min_p > 0 and max_p > min_p:
            position = (current_price - min_p) / (max_p - min_p) * 100
            if position < 20:
                signals.append({'type': 'low_position', 'signal': 'BULLISH',
                              'reason': f'价格处于{position:.1f}%分位（近 60 日低位）', 'strength': 7})
            elif position > 80:
                signals.append({'type': 'high_position', 'signal': 'BEARISH',
                              'reason': f'价格处于{position:.1f}%分位（近 60 日高位）', 'strength': 7})
        
        # 综合信号
        if signals:
            bullish = [s for s in signals if 'BULLISH' in s['signal']]
            bearish = [s for s in signals if 'BEARISH' in s['signal']]
            result['signal_summary'] = {
                'bullish_count': len(bullish),
                'bearish_count': len(bearish),
                'bullish_strength': sum(s.get('strength', 0) for s in bullish),
                'bearish_strength': sum(s.get('strength', 0) for s in bearish),
                'net_signal': 'BULLISH' if sum(s.get('strength', 0) for s in bullish) > sum(s.get('strength', 0) for s in bearish) else 'BEARISH',
                'confidence': min(abs(sum(s.get('strength', 0) for s in bullish) - sum(s.get('strength', 0) for s in bearish)) * 10, 100)
            }
        
        return signals
    
    def calculate_risk_reward(self, current_price: float, distribution: Dict) -> Dict:
        """计算风险收益比"""
        chip_dist = distribution.get('distribution', {})
        sorted_prices = sorted([float(p) for p in chip_dist.keys()])
        
        support = next((p for p in reversed(sorted_prices) if p < current_price), None)
        resistance = next((p for p in sorted_prices if p > current_price), None)
        
        if not support or not resistance:
            return {}
        
        risk = current_price - support
        reward = resistance - current_price
        rr_ratio = reward / risk if risk > 0 else float('inf')
        
        return {
            'support': support,
            'resistance': resistance,
            'risk': round(risk, 2),
            'reward': round(reward, 2),
            'risk_reward_ratio': round(rr_ratio, 2) if rr_ratio != float('inf') else '∞',
            'recommendation': 'GOOD' if rr_ratio >= 2 else 'FAIR' if rr_ratio >= 1 else 'POOR'
        }
    
    def full_analysis(self, symbol: str, days: int = 60) -> Optional[Dict]:
        """完整量化分析"""
        print(f"\n🔬 正在分析 {symbol}...")
        
        history = self.get_price_history(symbol, days)
        if not history:
            return None
        
        distribution = self.calculate_cost_distribution(history)
        main_cost = self.estimate_main_force_cost(history)
        profit_ratio = self.calculate_profit_ratio(distribution['current_price'], distribution)
        risk_reward = self.calculate_risk_reward(distribution['current_price'], distribution)
        
        result = {
            'symbol': symbol,
            'current_price': distribution['current_price'],
            'analysis_period': days,
            'distribution': distribution,
            'main_force_cost': main_cost,
            'profit_ratio': profit_ratio,
            'risk_reward': risk_reward,
        }
        
        result['signals'] = self.generate_quantitative_signals(result)
        return result


def print_report(result: Dict):
    """打印分析报告"""
    if not result:
        return
    
    print("\n" + "=" * 60)
    print(f"📊 {result['symbol']} 量化持仓成本分析报告")
    print("=" * 60)
    print(f"\n当前价格：${result['current_price']:.2f}")
    print(f"分析周期：{result['analysis_period']} 天")
    
    dist = result['distribution']
    print(f"\n💰 成本分布:")
    print(f"   价格区间：${dist['min_price']:.2f} - ${dist['max_price']:.2f}")
    print(f"   筹码峰值：${dist['peak_price']:.2f} (占比{dist['peak_ratio']}%)")
    if dist['concentration_range'][0]:
        print(f"   70% 筹码集中区：${dist['concentration_range'][0]:.2f} - ${dist['concentration_range'][1]:.2f}")
    
    main = result['main_force_cost']
    if main:
        print(f"\n🎯 主力成本:")
        print(f"   估算成本：${main['estimated_cost']:.2f}")
        print(f"   方法：{main['method']}")
        print(f"   置信度：{main['confidence']}")
    
    profit = result['profit_ratio']
    print(f"\n📈 获利盘:")
    print(f"   获利盘：{profit['profit_ratio']}%")
    print(f"   套牢盘：{profit['loss_ratio']}%")
    
    rr = result['risk_reward']
    if rr:
        print(f"\n⚖️  风险收益比:")
        print(f"   支撑位：${rr['support']:.2f}")
        print(f"   阻力位：${rr['resistance']:.2f}")
        print(f"   风险收益比：{rr['risk_reward_ratio']}")
        print(f"   建议：{rr['recommendation']}")
    
    signals = result.get('signals', [])
    if signals:
        print(f"\n🎯 量化信号 ({len(signals)} 个):")
        for sig in signals:
            emoji = "🟢" if "BULLISH" in sig['signal'] else "🔴"
            print(f"   {emoji} {sig['signal']}: {sig['reason']}")
        
        summary = result.get('signal_summary', {})
        if summary:
            print(f"\n📊 综合信号:")
            print(f"   多头信号：{summary['bullish_count']} (强度:{summary['bullish_strength']})")
            print(f"   空头信号：{summary['bearish_count']} (强度:{summary['bearish_strength']})")
            print(f"   净信号：{summary['net_signal']} (置信度:{summary['confidence']:.0f}%)")
    
    print("\n" + "=" * 60)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='量化持仓成本分析')
    parser.add_argument('symbol', help='标的符号')
    parser.add_argument('--days', type=int, default=60, help='分析天数')
    
    args = parser.parse_args()
    
    analyzer = QuantitativeCostAnalyzer()
    result = analyzer.full_analysis(args.symbol, args.days)
    
    if result:
        print_report(result)
    else:
        print("❌ 分析失败")


if __name__ == '__main__':
    main()
