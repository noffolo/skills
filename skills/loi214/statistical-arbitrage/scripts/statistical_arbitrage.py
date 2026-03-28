#!/usr/bin/env python3
"""
Statistical Arbitrage (Pairs Trading) Strategy
Multi-market support: HK, US, CN stocks
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import yfinance as yf
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint
from datetime import datetime, timedelta
import warnings
import os
import sys
import json
import argparse
from pathlib import Path
import traceback
import re
warnings.filterwarnings('ignore')

# Font settings - Cross-platform compatible
try:
    # Try system fonts first (macOS/Linux)
    plt.rcParams['font.family'] = ['Arial Unicode MS', 'Heiti TC', 'PingFang HK', 'STHeiti', 'DejaVu Sans', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
except Exception as e:
    # Fallback to default sans-serif
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['axes.unicode_minus'] = False
BG, FG = '#1a1a2e', 'white'

# Language detection
def is_chinese(text):
    """Detect if text contains Chinese characters"""
    if not text:
        return False
    for char in str(text):
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

def detect_lang(stock1, stock2):
    """Detect language from stock codes"""
    # If any stock has Chinese market suffix (.HK, .SS, .SZ) or stock name has Chinese
    stock_str = str(stock1) + str(stock2)
    # Check if stock codes suggest HK/CN market
    if '.HK' in stock_str.upper() or '.SS' in stock_str.upper() or '.SZ' in stock_str.upper():
        return 'zh'
    # Default to English
    return 'en'

# Translation dictionary
T = {
    'zh': {
        'downloading': '下載數據...',
        'filter_zeros': '過濾 {n} 個假交易日',
        'success': '成功下載: {ticker} ({market}): {days} 個有效交易日',
        'download_fail': '下載失敗: {ticker}',
        'cointegration': '協整檢驗...',
        'pvalue': 'p值',
        'significant': '顯著',
        'not_significant': '不顯著',
        'hedge_ratio': '對沖比率',
        'r_squared': 'R²',
        'current_zscore': '當前 Z-Score',
        'entry_signal': '交易信號',
        'long_spread': '做多價差',
        'short_spread': '做空價差',
        'no_signal': '無交易信號',
        'running_backtest': '執行回測...',
        'backtest_summary': '回測績效摘要',
        'total_return': '總回報',
        'annual_return': '年化',
        'sharpe': '夏普比率',
        'max_drawdown': '最大回撤',
        'calmar': 'Calmar比率',
        'volatility': '波動率',
        'trades': '交易次數',
        'win_rate': '勝率',
        'profit_factor': '盈虧比',
        'generating_charts': '生成圖表...',
        'charts_generated': '{n}張圖表已生成到: {path}',
        'generating_report': '生成報告...',
        'report_generated': 'HTML報告已生成: {path}',
        'analysis_complete': '分析完成！',
        'final_capital': '最終資金',
        'stock_pair': '股票對',
        'time_range': '時間範圍',
        'common_days': '共同交易日',
        'cointegration_test': '協整檢驗',
        'exit_threshold': '出入場閾值',
        'stop_loss': '止損閾值',
        'initial_capital': '初始資金',
        'recommended': '強烈推薦',
        'good': '建議',
        'consider': '謹慎考慮',
    },
    'en': {
        'downloading': 'Downloading data...',
        'filter_zeros': 'Filtered {n} zero-volume days',
        'success': 'OK: {ticker} ({market}): {days} valid trading days',
        'download_fail': 'FAIL: {ticker}',
        'cointegration': 'Cointegration test...',
        'pvalue': 'p-value',
        'significant': 'Significant',
        'not_significant': 'Not significant',
        'hedge_ratio': 'Hedge Ratio (Beta)',
        'r_squared': 'R²',
        'current_zscore': 'Current Z-Score',
        'entry_signal': 'Entry Signal',
        'long_spread': 'Long spread',
        'short_spread': 'Short spread',
        'no_signal': 'No signal',
        'running_backtest': 'Running backtest...',
        'backtest_summary': 'Backtest Summary',
        'total_return': 'Total Return',
        'annual_return': 'Annual Return',
        'sharpe': 'Sharpe Ratio',
        'max_drawdown': 'Max Drawdown',
        'calmar': 'Calmar Ratio',
        'volatility': 'Volatility',
        'trades': 'Trades',
        'win_rate': 'Win Rate',
        'profit_factor': 'Profit Factor',
        'generating_charts': 'Generating charts...',
        'charts_generated': '{n} charts saved to: {path}',
        'generating_report': 'Generating report...',
        'report_generated': 'HTML report saved: {path}',
        'analysis_complete': 'Analysis complete!',
        'final_capital': 'Final Capital',
        'stock_pair': 'Stock Pair',
        'time_range': 'Time Range',
        'common_days': 'Common Trading Days',
        'cointegration_test': 'Cointegration Test',
        'exit_threshold': 'Entry/Exit Threshold',
        'stop_loss': 'Stop Loss',
        'initial_capital': 'Initial Capital',
        'recommended': 'Highly Recommended',
        'good': 'Good',
        'consider': 'Consider Carefully',
    }
}

def tr(key, lang='en', **kwargs):
    """Translate text"""
    text = T.get(lang, T['en']).get(key, T['en'].get(key, key))
    return text.format(**kwargs) if kwargs else text

class StatisticalArbitrage:
    """Statistical Arbitrage Strategy Engine"""
    
    def __init__(self, config, lang='en'):
        self.config = config
        self.lang = lang
        self.output_dir = Path(config.get('output_dir', './stat_arb_output')).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def detect_market(self, ticker):
        """檢測股票所屬市場"""
        ticker_upper = ticker.upper()
        if ticker_upper.endswith('.HK'):
            return 'HK', ticker_upper
        elif ticker_upper.endswith('.SS') or ticker_upper.endswith('.SZ'):
            return 'CN', ticker_upper
        elif ticker_upper.endswith('.TO') or ticker_upper.endswith('.V'):
            return 'CA', ticker_upper
        else:
            # 默認為美股
            return 'US', ticker_upper
    
    def download_clean(self, ticker, start, end):
        """Download and clean data, multi-market support"""
        market, clean_ticker = self.detect_market(ticker)
        lang = self.lang
        
        try:
            raw = yf.download(clean_ticker, start=start, end=end, progress=False)
            if raw.empty:
                raise ValueError(f"Data download failed: {clean_ticker}")
            
            # Handle MultiIndex
            if isinstance(raw.columns, pd.MultiIndex):
                df = raw.xs(clean_ticker, axis=1, level='Ticker').copy()
            else:
                df = raw.copy()
            
            # Filter zero-volume days (mainly for HK stocks)
            before = len(df)
            df = df[df['Volume'] > 0].copy()
            after = len(df)
            if before != after and market == 'HK':
                print(f"  {tr('filter_zeros', lang, n=before-after)}")
            
            # Print success message (bilingual)
            mkt_name = 'HK' if market == 'HK' else ('CN' if market == 'CN' else 'US')
            print(f"  OK: {clean_ticker} ({mkt_name}): {len(df)} {'days' if lang=='en' else '天'}")
            return df
        except Exception as e:
            print(f"  FAIL: {clean_ticker}")
            raise
    
    def calculate_metrics(self, equity, trades_df):
        """計算績效指標"""
        rets = equity.pct_change().dropna()
        total_ret = (equity.iloc[-1] / equity.iloc[0] - 1) * 100
        
        if len(equity) > 252:
            ann_ret = ((equity.iloc[-1] / equity.iloc[0]) ** (252 / len(equity)) - 1) * 100
        else:
            ann_ret = total_ret
        
        volatility = rets.std() * np.sqrt(252) * 100 if len(rets) > 0 else 0
        sharpe = (rets.mean() / rets.std() * np.sqrt(252)) if rets.std() > 0 else 0
        
        # 計算回撤
        cumulative = equity
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max * 100
        max_drawdown = drawdown.min()
        
        # Calmar比率
        calmar = ann_ret / abs(max_drawdown) if max_drawdown != 0 else 0
        
        # 交易統計
        exits = trades_df[trades_df['type'].str.startswith('EXIT')] if len(trades_df) > 0 else pd.DataFrame()
        win_rate = (exits['pnl'] > 0).mean() * 100 if len(exits) > 0 else 0
        avg_win = exits[exits['pnl'] > 0]['pnl'].mean() if len(exits[exits['pnl'] > 0]) > 0 else 0
        avg_loss = exits[exits['pnl'] < 0]['pnl'].mean() if len(exits[exits['pnl'] < 0]) > 0 else 0
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        
        return {
            'total_return': total_ret,
            'annual_return': ann_ret,
            'volatility': volatility,
            'sharpe': sharpe,
            'max_drawdown': max_drawdown,
            'calmar': calmar,
            'win_rate': win_rate,
            'total_trades': len(exits),
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor
        }
    
    def backtest(self, df, z_col, beta_ref):
        """執行回測"""
        capital = self.config['initial_capital']
        pos = 0  # 1=做多價差, -1=做空價差
        pv = self.config['position_size']
        cost_r = self.config['transaction_cost']
        trades = []
        equity = [capital]
        
        n1 = n2 = 0  # 持倉股數
        ep1 = ep2 = 0.0  # 入場價格
        
        for i in range(1, len(df)):
            dt = df.index[i]
            z = df[z_col].iloc[i]
            p1 = df['stock1'].iloc[i]
            p2 = df['stock2'].iloc[i]
            
            # 獲取當前beta
            if isinstance(beta_ref, pd.Series):
                beta = beta_ref.loc[dt] if dt in beta_ref.index else beta_ref.iloc[0]
            else:
                beta = beta_ref
            
            # 入場信號
            if pos == 0:
                alloc = capital * pv
                if z < -self.config['entry_threshold']:
                    pos = 1
                    n1 = alloc / 2 / p1
                    n2 = alloc / 2 * beta / p2
                    ep1, ep2 = p1, p2
                    capital -= alloc * cost_r
                    trades.append({'date': dt, 'type': 'ENTRY_LONG', 'z': z})
                
                elif z > self.config['entry_threshold']:
                    pos = -1
                    n1 = alloc / 2 / p1
                    n2 = alloc / 2 * beta / p2
                    ep1, ep2 = p1, p2
                    capital -= alloc * cost_r
                    trades.append({'date': dt, 'type': 'ENTRY_SHORT', 'z': z})
            
            # 出場（多頭）
            elif pos == 1:
                tp = z > -self.config['exit_threshold']
                sl = z < -self.config['stop_loss']
                if tp or sl:
                    pnl = n1 * (p1 - ep1) - n2 * (p2 - ep2) - (n1 * p1 + n2 * p2) * cost_r
                    capital += pnl
                    pos = 0
                    trades.append({'date': dt, 'type': 'EXIT_LONG', 'z': z,
                                   'pnl': pnl, 'reason': 'TP' if tp else 'SL'})
            
            # 出場（空頭）
            elif pos == -1:
                tp = z < self.config['exit_threshold']
                sl = z > self.config['stop_loss']
                if tp or sl:
                    pnl = -n1 * (p1 - ep1) + n2 * (p2 - ep2) - (n1 * p1 + n2 * p2) * cost_r
                    capital += pnl
                    pos = 0
                    trades.append({'date': dt, 'type': 'EXIT_SHORT', 'z': z,
                                   'pnl': pnl, 'reason': 'TP' if tp else 'SL'})
            
            equity.append(capital)
        
        # 強制平倉
        if pos != 0:
            p1f, p2f = df['stock1'].iloc[-1], df['stock2'].iloc[-1]
            if pos == 1:
                pnl = n1 * (p1f - ep1) - n2 * (p2f - ep2) - (n1 * p1f + n2 * p2f) * cost_r
            else:
                pnl = -n1 * (p1f - ep1) + n2 * (p2f - ep2) - (n1 * p1f + n2 * p2f) * cost_r
            capital += pnl
            trades.append({'date': df.index[-1], 'type': f'EXIT_{"LONG" if pos==1 else "SHORT"}',
                           'z': df[z_col].iloc[-1], 'pnl': pnl, 'reason': 'FINAL'})
            equity[-1] = capital
        
        return pd.DataFrame(trades), pd.Series(equity, index=df.index)
    
    def generate_charts(self, combined, train_data, test_data, trades_df, equity, beta_s, betas_dyn=None):
        """生成6張專業圖表"""
        
        def styled_ax(ax):
            ax.set_facecolor(BG)
            ax.tick_params(colors=FG, labelsize=9)
            ax.xaxis.label.set_color(FG)
            ax.yaxis.label.set_color(FG)
            ax.title.set_color(FG)
            for sp in ax.spines.values():
                sp.set_color('#4a4a6a')
            ax.grid(True, alpha=0.15, color='gray')
        
        # 圖1：價格走勢對比
        fig1, ax1 = plt.subplots(figsize=(14, 6))
        styled_ax(ax1)
        ax1.plot(combined['stock1'], label='Stock 1', linewidth=1.5, color='#3498db')
        ax1.plot(combined['stock2'], label='Stock 2', linewidth=1.5, color='#e67e22')
        ax1.axvline(train_data.index[-1], color='#e74c3c', linestyle='--', alpha=0.7, label='Train/Test')
        ax1.set_title('股票價格走勢對比', fontsize=13, fontweight='bold')
        ax1.set_ylabel('Price', fontsize=11)
        ax1.legend(facecolor='#2c3e50', labelcolor=FG, loc='upper left')
        plt.tight_layout()
        plt.savefig(self.output_dir / '1_Price_Comparison.png', dpi=150, bbox_inches='tight', facecolor=BG)
        plt.close()
        
        # 圖2：標準化價格
        fig2, ax2 = plt.subplots(figsize=(14, 6))
        styled_ax(ax2)
        norm1 = combined['stock1'] / combined['stock1'].iloc[0]
        norm2 = combined['stock2'] / combined['stock2'].iloc[0]
        ax2.plot(norm1, label='Stock 1 (Norm)', linewidth=1.5, color='#3498db')
        ax2.plot(norm2, label='Stock 2 (Norm)', linewidth=1.5, color='#e67e22')
        ax2.axvline(train_data.index[-1], color='#e74c3c', linestyle='--', alpha=0.7)
        ax2.set_title('標準化價格走勢', fontsize=13, fontweight='bold')
        ax2.set_ylabel('Norm Price', fontsize=11)
        ax2.legend(facecolor='#2c3e50', labelcolor=FG, loc='upper left')
        plt.tight_layout()
        plt.savefig(self.output_dir / '2_Normalized_Price.png', dpi=150, bbox_inches='tight', facecolor=BG)
        plt.close()
        
        # 圖3：Z-Score信號圖
        if 'z_score' in combined.columns:
            fig3, ax3 = plt.subplots(figsize=(14, 6))
            styled_ax(ax3)
            ax3.plot(combined.index, combined['z_score'], label='Z-Score', linewidth=1.2, color='#9b59b6')
            ax3.axhline(0, color='gray', linestyle='-', alpha=0.3)
            ax3.axhline(self.config['entry_threshold'], color='#e74c3c', linestyle='--', alpha=0.7, label=f'入場閾值 ±{self.config["entry_threshold"]}')
            ax3.axhline(-self.config['entry_threshold'], color='#e74c3c', linestyle='--', alpha=0.7)
            ax3.axhline(self.config['exit_threshold'], color='#2ecc71', linestyle='--', alpha=0.7, label=f'出場閾值 ±{self.config["exit_threshold"]}')
            ax3.axhline(-self.config['exit_threshold'], color='#2ecc71', linestyle='--', alpha=0.7)
            ax3.axvline(train_data.index[-1], color='#e74c3c', linestyle='--', alpha=0.7)
            
            # 標記交易點
            if len(trades_df) > 0:
                entry_trades = trades_df[trades_df['type'].str.contains('ENTRY')]
                exit_trades = trades_df[trades_df['type'].str.contains('EXIT')]
                
                if len(entry_trades) > 0:
                    ax3.scatter(entry_trades['date'], entry_trades['z'], 
                               color='yellow', s=50, zorder=5, label='Entry')
                if len(exit_trades) > 0:
                    ax3.scatter(exit_trades['date'], exit_trades['z'],
                               color='cyan', s=50, zorder=5, label='出場點')
            
            ax3.set_title('Z-Score 信號圖', fontsize=13, fontweight='bold')
            ax3.set_ylabel('Z-Score', fontsize=11)
            ax3.set_xlabel('Date', fontsize=11)
            ax3.legend(facecolor='#2c3e50', labelcolor=FG, loc='upper right')
            plt.tight_layout()
            plt.savefig(self.output_dir / '3_ZScore_Signals.png', dpi=150, bbox_inches='tight', facecolor=BG)
            plt.close()
        
        # 圖4：權益曲線與回撤
        fig4, (ax4a, ax4b) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
        styled_ax(ax4a); styled_ax(ax4b)
        
        # 權益曲線
        ax4a.plot(equity.index, equity, linewidth=2, color='#2ecc71')
        ax4a.axhline(self.config['initial_capital'], color='gray', linestyle='--', alpha=0.5)
        ax4a.set_title('Equity Curve', fontsize=12)
        ax4a.set_ylabel('Capital ($)', fontsize=10)
        
        # 回撤圖
        cumulative = equity
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max * 100
        ax4b.fill_between(drawdown.index, drawdown, 0, color='#e74c3c', alpha=0.3)
        ax4b.set_title('Drawdown', fontsize=12)
        ax4b.set_ylabel('Drawdown (%)', fontsize=10)
        ax4b.set_xlabel('Date', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '4_Equity_Drawdown.png', dpi=150, bbox_inches='tight', facecolor=BG)
        plt.close()
        
        # 圖5：月度損益熱力圖
        if len(trades_df) > 0:
            exits = trades_df[trades_df['type'].str.startswith('EXIT')].copy()
            if len(exits) > 0:
                exits['year'] = exits['date'].dt.year
                exits['month'] = exits['date'].dt.month
                monthly = exits.groupby(['year', 'month'])['pnl'].sum().unstack(fill_value=0)
                
                if not monthly.empty:
                    fig5, ax5 = plt.subplots(figsize=(12, 6))
                    styled_ax(ax5)
                    im = ax5.imshow(monthly.values, cmap='RdYlGn', aspect='auto')
                    ax5.set_xticks(range(len(monthly.columns)))
                    ax5.set_xticklabels([f'{m}' for m in monthly.columns], fontsize=9)
                    ax5.set_yticks(range(len(monthly.index)))
                    ax5.set_yticklabels([str(y) for y in monthly.index], fontsize=9)
                    ax5.set_title('Monthly P&L Heatmap', fontsize=12)
                    plt.colorbar(im, ax=ax5).ax.yaxis.set_tick_params(color=FG)
                    plt.tight_layout()
                    plt.savefig(self.output_dir / '5_Monthly_PnL.png', dpi=150, bbox_inches='tight', facecolor=BG)
                    plt.close()
        
        # 圖6：Beta分布圖
        fig6, ax6 = plt.subplots(figsize=(10, 6))
        styled_ax(ax6)
        
        if betas_dyn is not None and len(betas_dyn) > 0:
            ax6.hist(betas_dyn, bins=30, color='#3498db', alpha=0.7, density=True)
            ax6.axvline(beta_s, color='#e74c3c', linewidth=2, linestyle='--', label=f'Static β={beta_s:.4f}')
            ax6.axvline(betas_dyn.mean(), color='#f39c12', linewidth=2, linestyle='--', label=f'Dynamic β avg={betas_dyn.mean():.4f}')
            ax6.set_title('Dynamic Hedge Ratio', fontsize=12)
            ax6.set_xlabel('Beta', fontsize=10)
            ax6.set_ylabel('Freq', fontsize=10)
            ax6.legend(facecolor='#2c3e50', labelcolor=FG)
        else:
            ax6.text(0.5, 0.5, 'Static Beta Only', ha='center', va='center', 
                    transform=ax6.transAxes, color=FG, fontsize=12)
            ax6.set_title('Hedge Ratio', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / '6_Beta_Distribution.png', dpi=150, bbox_inches='tight', facecolor=BG)
        plt.close()
        
        print(f"  ✅ 6張圖表已生成到: {self.output_dir}")
    
    def generate_html_report(self, result, metrics, combined, trades_df):
        """生成HTML報告"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Statistical Arbitrage Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: white; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ text-align: center; margin-bottom: 40px; }}
                .section {{ background: #2c3e50; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
                .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; }}
                .metric-card {{ background: #34495e; padding: 15px; border-radius: 8px; text-align: center; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #2ecc71; }}
                .chart-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 20px; }}
                .chart-img {{ width: 100%; border-radius: 8px; }}
                .negative {{ color: #e74c3c !important; }}
                .positive {{ color: #2ecc71 !important; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 統計套利分析報告</h1>
                    <p>生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="section">
                    <h2>Analysis Overview</h2>
                    <p><strong>Stock Pair:</strong> {result['stock1']} vs {result['stock2']}</p>
                    <p><strong>Period:</strong> {result['start_date']} 至 {result['end_date']}</p>
                    <p><strong>Common Trading Days:</strong> {len(combined)} 天</p>
                    <p><strong>Cointegration p-value:</strong> {result['p_value']:.6f} 
                       <span class="{'positive' if result['p_value'] < 0.05 else 'negative'}">
                       ({'Significant' if result['p_value'] < 0.05 else 'Not significant'})
                       </span>
                    </p>
                    <p><strong>Hedge Ratio β:</strong> {result['beta']:.6f}</p>
                    <p><strong>Current Z-Score:</strong> {result['current_z']:.2f}
                       <span class="{'positive' if abs(result['current_z']) > result['entry_threshold'] else ''}">
                       ({'Signal detected' if abs(result['current_z']) > result['entry_threshold'] else 'No signal'})
                       </span>
                    </p>
                </div>
                
                <div class="section">
                    <h2>Performance Metrics</h2>
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div>Total Return</div>
                            <div class="metric-value {'positive' if metrics['total_return'] > 0 else 'negative'}">
                                {metrics['total_return']:+.2f}%
                            </div>
                        </div>
                        <div class="metric-card">
                            <div>Annual Return</div>
                            <div class="metric-value {'positive' if metrics['annual_return'] > 0 else 'negative'}">
                                {metrics['annual_return']:+.2f}%
                            </div>
                        </div>
                        <div class="metric-card">
                            <div>Sharpe Ratio</div>
                            <div class="metric-value">
                                {metrics['sharpe']:.3f}
                            </div>
                        </div>
                        <div class="metric-card">
                            <div>Max Drawdown</div>
                            <div class="metric-value negative">
                                {metrics['max_drawdown']:.2f}%
                            </div>
                        </div>
                        <div class="metric-card">
                            <div>Calmar Ratio</div>
                            <div class="metric-value">
                                {metrics['calmar']:.3f}
                            </div>
                        </div>
                        <div class="metric-card">
                            <div>Win Rate</div>
                            <div class="metric-value">
                                {metrics['win_rate']:.1f}%
                            </div>
                        </div>
                        <div class="metric-card">
                            <div>Trades</div>
                            <div class="metric-value">
                                {metrics['total_trades']}
                            </div>
                        </div>
                        <div class="metric-card">
                            <div>Profit Factor</div>
                            <div class="metric-value">
                                {metrics['profit_factor']:.2f}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Charts</h2>
                    <div class="chart-grid">
                        <div><img src="1_價格走勢對比.png" class="chart-img" alt="Price Comparison"></div>
                        <div><img src="2_標準化價格.png" class="chart-img" alt="Normalized Price"></div>
                        <div><img src="3_ZScore信號圖.png" class="chart-img" alt="Z-Score Signals"></div>
                        <div><img src="4_權益曲線與回撤.png" class="chart-img" alt="Equity Curve"></div>
                        <div><img src="5_月度損益熱力圖.png" class="chart-img" alt="Monthly P&L"></div>
                        <div><img src="6_Beta分布圖.png" class="chart-img" alt="Beta Distribution"></div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Parameters</h2>
                    <pre>{json.dumps(result['config'], indent=2, ensure_ascii=False)}</pre>
                </div>
                
                <div class="section">
                    <h2>Trade History (Last 10)</h2>
                    {trades_df.tail(10).to_html(index=False, classes='trades-table') if len(trades_df) > 0 else '<p>No trades</p>'}
                </div>
            </div>
        </body>
        </html>
        """
        
        report_path = self.output_dir / 'report.html'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  HTML report saved: {report_path}")
        return report_path
    
    def run_analysis(self, stock1, stock2, start_date, end_date):
        """Run complete analysis - bilingual"""
        lang = self.lang
        is_cn = (lang == 'zh')
        
        # Bilingual header
        if is_cn:
            print("\n" + "═" * 65)
            print("  統計套利分析系統")
            print(f"  {stock1} vs {stock2}")
            print(f"  時間範圍: {start_date} 至 {end_date}")
            print("═" * 65)
            print("\n下載數據...")
        else:
            print("\n" + "=" * 65)
            print("  Statistical Arbitrage Analysis")
            print(f"  {stock1} vs {stock2}")
            print(f"  Period: {start_date} to {end_date}")
            print("=" * 65)
            print("\nDownloading data...")
        
        d1 = self.download_clean(stock1, start_date, end_date)
        d2 = self.download_clean(stock2, start_date, end_date)
        
        combined = pd.DataFrame({
            'stock1': d1['Close'],
            'stock2': d2['Close'],
        }).dropna()
        
        print(f"  {'共同交易日' if is_cn else 'Common trading days'}: {len(combined)}")
        
        if len(combined) < 100:
            if is_cn:
                raise ValueError(f"數據不足（{len(combined)} 天），至少需要100天")
            else:
                raise ValueError(f"Insufficient data ({len(combined)} days), minimum 100 required")
        
        combined['log1'] = np.log(combined['stock1'])
        combined['log2'] = np.log(combined['stock2'])
        
        # 分割數據
        split_idx = int(len(combined) * self.config['train_ratio'])
        train_data = combined.iloc[:split_idx].copy()
        
        # 協整檢驗
        if is_cn:
            print("\n協整檢驗...")
        else:
            print("\nCointegration test...")
        
        _, p_coint, _ = coint(train_data['log1'], train_data['log2'], autolag='AIC')
        
        sig_text = "Significant" if p_coint < 0.05 else "Not significant"
        sig_emoji = "OK" if p_coint < 0.05 else "WARN"
        
        print(f"  p-value: {p_coint:.6f} [{sig_emoji}] {sig_text}")
        
        # 計算對沖比率
        X_tr = sm.add_constant(train_data['log2'])
        model = sm.OLS(train_data['log1'], X_tr).fit()
        beta_s = model.params.iloc[1]
        
        if is_cn:
            print(f"\n對沖比率 β={beta_s:.6f}  R²={model.rsquared:.4f}")
        else:
            print(f"\nHedge Ratio Beta={beta_s:.6f}  R²={model.rsquared:.4f}")
        
        # 計算Z-Score
        combined['spread'] = combined['log1'] - beta_s * combined['log2']
        sp_mean = combined['spread'].iloc[:split_idx].mean()
        sp_std = combined['spread'].iloc[:split_idx].std()
        combined['z_score'] = (combined['spread'] - sp_mean) / sp_std
        
        # 更新測試集
        test_data = combined.iloc[split_idx:].copy()
        
        # 動態對沖比率（可選）
        betas_dyn = None
        if self.config.get('dynamic_beta', True):
            W = self.config['window_size']
            betas_list, dates_list = [], []
            for i in range(W, len(combined)):
                w = combined.iloc[i-W:i]
                Xw = sm.add_constant(w['log2'])
                betas_list.append(sm.OLS(w['log1'], Xw).fit().params.iloc[1])
                dates_list.append(combined.index[i])
            betas_dyn = pd.Series(betas_list, index=dates_list)
            print(f"  動態β計算完成，範圍: [{betas_dyn.min():.4f}, {betas_dyn.max():.4f}]")
        
        # 當前信號
        current_z = combined['z_score'].iloc[-1]
        
        if is_cn:
            print(f"\n當前 Z-Score: {current_z:.2f}")
        else:
            print(f"\nCurrent Z-Score: {current_z:.2f}")
        
        if abs(current_z) > self.config['entry_threshold']:
            signal = "Long spread" if current_z < 0 else "Short spread"
            if is_cn:
                signal = '做多價差' if current_z < 0 else '做空價差'
            print(f"  SIGNAL: {signal} (Z beyond +- {self.config['entry_threshold']})")
        else:
            if is_cn:
                print(f"  無信號 (Z在±{self.config['entry_threshold']}內)")
            else:
                print(f"  No signal (Z within +- {self.config['entry_threshold']})")
        
        # 回測
        if is_cn:
            print("\n執行回測...")
        else:
            print("\nRunning backtest...")
        
        test_trades, test_equity = self.backtest(test_data, 'z_score', beta_s)
        
        # 計算績效
        metrics = self.calculate_metrics(test_equity, test_trades)
        
        # Bilingual metrics display
        print(f"\n{'-' * 55}")
        if is_cn:
            print("  回測績效摘要")
        else:
            print("  Backtest Summary")
        print(f"{'-' * 55}")
        
        if is_cn:
            print(f"  總回報: {metrics['total_return']:+.2f}%  |  年化: {metrics['annual_return']:+.2f}%")
            print(f"  夏普比率: {metrics['sharpe']:.3f}  |  最大回撤: {metrics['max_drawdown']:.2f}%")
            print(f"  Calmar比率: {metrics['calmar']:.3f}  |  波動率: {metrics['volatility']:.2f}%")
            print(f"  交易次數: {metrics['total_trades']}  |  勝率: {metrics['win_rate']:.1f}%")
            print(f"  盈虧比: {metrics['profit_factor']:.2f}")
        else:
            print(f"  Total Return: {metrics['total_return']:+.2f}%  |  Annual: {metrics['annual_return']:+.2f}%")
            print(f"  Sharpe: {metrics['sharpe']:.3f}  |  Max DD: {metrics['max_drawdown']:.2f}%")
            print(f"  Calmar: {metrics['calmar']:.3f}  |  Volatility: {metrics['volatility']:.2f}%")
            print(f"  Trades: {metrics['total_trades']}  |  Win Rate: {metrics['win_rate']:.1f}%")
            print(f"  Profit Factor: {metrics['profit_factor']:.2f}")
        
        # 生成圖表
        if is_cn:
            print("\n生成圖表...")
        else:
            print("\nGenerating charts...")
        
        self.generate_charts(combined, train_data, test_data, test_trades, test_equity, beta_s, betas_dyn)
        
        # 生成HTML報告
        if is_cn:
            print("\n生成報告...")
        else:
            print("\nGenerating report...")
        result = {
            'stock1': stock1,
            'stock2': stock2,
            'start_date': start_date,
            'end_date': end_date,
            'p_value': p_coint,
            'beta': beta_s,
            'current_z': current_z,
            'entry_threshold': self.config['entry_threshold'],
            'config': self.config
        }
        
        html_report = self.generate_html_report(result, metrics, combined, test_trades)
        
        # 保存原始數據
        combined.to_csv(self.output_dir / 'raw_data.csv')
        test_trades.to_csv(self.output_dir / 'trades.csv', index=False)
        pd.DataFrame([metrics]).to_csv(self.output_dir / 'metrics.csv', index=False)
        
        print(f"\n=== Analysis Complete ===")
        print(f"   Output: {self.output_dir}")
        print(f"   Report: {html_report}")
        print(f"   最終資金: ${test_equity.iloc[-1]:.2f}")
        
        return {
            'metrics': metrics,
            'result': result,
            'output_dir': str(self.output_dir),
            'html_report': str(html_report),
            'final_capital': test_equity.iloc[-1]
        }


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Statistical Arbitrage Analysis')
    parser.add_argument('--stock1', required=True, help='Stock 1 code (e.g., AAPL, 1398.HK)')
    parser.add_argument('--stock2', required=True, help='Stock 2 code (e.g., GOOGL, 0939.HK)')
    parser.add_argument('--start', default='2020-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', default=datetime.now().strftime('%Y-%m-%d'), help='End date (YYYY-MM-DD)')
    parser.add_argument('--entry', type=float, default=2.0, help='Entry threshold (Z-Score)')
    parser.add_argument('--exit', type=float, default=0.5, help='Exit threshold (Z-Score)')
    parser.add_argument('--stop', type=float, default=3.5, help='Stop loss threshold (Z-Score)')
    parser.add_argument('--capital', type=float, default=100000, help='Initial capital')
    parser.add_argument('--output', default='./stat_arb_output', help='Output directory')
    parser.add_argument('--dynamic', action='store_true', help='Use dynamic hedge ratio')
    parser.add_argument('--lang', default='auto', help='Language: en, zh, or auto')
    
    args = parser.parse_args()
    
    # Detect language
    if args.lang == 'auto':
        lang = detect_lang(args.stock1, args.stock2)
    else:
        lang = args.lang
    
    config = {
        'train_ratio': 0.7,
        'entry_threshold': args.entry,
        'exit_threshold': args.exit,
        'stop_loss': args.stop,
        'window_size': 60,
        'transaction_cost': 0.0015,
        'initial_capital': args.capital,
        'position_size': 0.5,
        'output_dir': args.output,
        'dynamic_beta': args.dynamic
    }
    
    try:
        engine = StatisticalArbitrage(config, lang=lang)
        result = engine.run_analysis(args.stock1, args.stock2, args.start, args.end)
        
        # Print summary
        is_cn = (lang == 'zh')
        if is_cn:
            print(f"\n=== 分析完成 ===")
        else:
            print(f"\n=== Analysis Complete ===")
        print(f"Stock Pair: {args.stock1} vs {args.stock2}")
        print(f"p-value: {result['result']['p_value']:.6f}")
        print(f"Current Z-Score: {result['result']['current_z']:.2f}")
        print(f"Annual Return: {result['metrics']['annual_return']:+.2f}%")
        print(f"Sharpe Ratio: {result['metrics']['sharpe']:.3f}")
        print(f"Output: {result['output_dir']}")
        
    except Exception as e:
        print(f"❌ 分析失敗: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()