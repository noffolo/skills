#!/usr/bin/env python3
"""
Daily Report - 专业三级日报系统
独立版本，直接调用市场数据 API
Small: 简报 (10 秒) | Medium: 标准 (1 分钟) | Large: 深度 (5 分钟)
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests

# Security: Do not load .env files at runtime.
# API keys must be set via standard environment variables only.
# This prevents accidental exposure of unrelated secrets.

# Paths
PORTFOLIO_FILE = Path(__file__).parent / "portfolio" / "holdings.json"
WATCHLIST_FILE = Path(__file__).parent / "watchlist.txt"
REPORTS_DIR = Path(__file__).parent / "reports"
SENT_DIR = Path(__file__).parent / "sent"
FEISHU_CONFIG = Path(__file__).parent / "feishu_config.json"

REPORTS_DIR.mkdir(exist_ok=True)
SENT_DIR.mkdir(exist_ok=True)

def get_hk_time():
    """Get Hong Kong time."""
    try:
        return datetime.now(ZoneInfo("Asia/Shanghai"))
    except:
        return datetime.now()

def is_trading_day(date=None):
    if date is None:
        date = datetime.now()
    return date.weekday() < 5

def load_portfolio():
    if not PORTFOLIO_FILE.exists():
        return None
    with open(PORTFOLIO_FILE) as f:
        return json.load(f)

def load_watchlist():
    if not WATCHLIST_FILE.exists():
        return ["NVDA", "TSLA", "AAPL", "MSFT", "GOOGL"]
    symbols = []
    with open(WATCHLIST_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                symbol = line.split('|')[0].strip().upper()
                if symbol:
                    symbols.append(symbol)
    return symbols

def get_stock_data(symbol, days=30):
    """Get stock data from Twelve Data API directly.
    
    Security: No external package dependencies, direct API calls only.
    """
    api_key = os.environ.get("TWELVE_DATA_API_KEY")
    if not api_key:
        print(f"  ⚠️ {symbol}: Missing TWELVE_DATA_API_KEY")
        return None
    
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Direct API call to Twelve Data
        url = "https://api.twelvedata.com/time"
        params = {
            "symbol": symbol,
            "interval": "1day",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "apikey": api_key
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if "values" in result and result["values"]:
            data = [
                {
                    "date": v["datetime"],
                    "open": float(v["open"]),
                    "high": float(v["high"]),
                    "low": float(v["low"]),
                    "close": float(v["close"]),
                    "volume": int(v["volume"]) if "volume" in v else 0
                }
                for v in result["values"]
            ]
            
            latest = float(data[0].get("close", 0))
            
            if len(data) >= 5:
                price_5d = float(data[4].get("close", latest))
                change_5d = ((latest - price_5d) / price_5d) * 100
            else:
                change_5d = 0
            
            if len(data) >= 20:
                price_20d = float(data[19].get("close", latest))
                change_20d = ((latest - price_20d) / price_20d) * 100
            else:
                change_20d = 0
            
            high_30d = max(float(d.get("high", 0)) for d in data)
            low_30d = min(float(d.get("low", 0)) for d in data)
            
            return {
                "symbol": symbol,
                "price": latest,
                "change_5d": change_5d,
                "change_20d": change_20d,
                "high_30d": high_30d,
                "low_30d": low_30d,
                "data": data
            }
    except Exception as e:
        print(f"  ⚠️ {symbol}: {e}")
    
    return None

def get_external_sentiment(symbol):
    """Get external sentiment from news/social media."""
    try:
        sentiment_file = Path(__file__).parent / "sentiment_report.json"
        if sentiment_file.exists():
            with open(sentiment_file) as f:
                data = json.load(f)
                if symbol in data.get("sentiments", {}):
                    sent = data["sentiments"][symbol]
                    return {
                        "sentiment": sent.get("sentiment", "neutral"),
                        "score": sent.get("score", 0),
                        "confidence": sent.get("confidence", "low")
                    }
    except:
        pass
    
    # Default
    return {"sentiment": "neutral", "score": 0, "confidence": "low"}

def analyze_stock(symbol, portfolio_data=None):
    """Analyze stock with market data + external sentiment."""
    print(f"  📊 {symbol}...")
    
    data = get_stock_data(symbol)
    if not data:
        return None
    
    # Add external sentiment
    ext_sentiment = get_external_sentiment(symbol)
    data["news_sentiment"] = ext_sentiment["sentiment"]
    data["news_score"] = ext_sentiment["score"]
    data["sentiment_confidence"] = ext_sentiment["confidence"]
    
    # Add portfolio info
    if portfolio_data:
        for h in portfolio_data.get("holdings", []):
            if h["symbol"] == symbol:
                data["shares"] = h.get("shares", 0)
                data["avg_cost"] = h.get("avg_cost", 0)
                data["market_value"] = h.get("market_value", 0)
                data["unrealized_pnl"] = h.get("unrealized_pnl", 0)
                data["unrealized_pnl_pct"] = h.get("unrealized_pnl_pct", 0)
                data["weight"] = h.get("weight", 0)
                break
    
    # Determine rating (combine technical + sentiment)
    tech_score = data["change_5d"]
    sent_score = data.get("news_score", 0) * 10  # Weight sentiment
    
    combined_score = tech_score * 0.7 + sent_score * 0.3
    
    if combined_score > 5 or (tech_score > 3 and data.get("news_sentiment") == "bullish"):
        outlook = "Strong Bullish"
        outlook_cn = "强势看涨"
        rating = "BUY"
        confidence = "High"
    elif combined_score > 2 or (tech_score > 0 and data.get("news_sentiment") == "bullish"):
        outlook = "Bullish"
        outlook_cn = "看涨"
        rating = "OVERWEIGHT"
        confidence = "Medium"
    elif combined_score < -5 or (tech_score < -3 and data.get("news_sentiment") == "bearish"):
        outlook = "Strong Bearish"
        outlook_cn = "强势看跌"
        rating = "SELL"
        confidence = "High"
    elif combined_score < -2 or (tech_score < 0 and data.get("news_sentiment") == "bearish"):
        outlook = "Bearish"
        outlook_cn = "看跌"
        rating = "UNDERWEIGHT"
        confidence = "Medium"
    else:
        outlook = "Neutral"
        outlook_cn = "中性"
        rating = "HOLD"
        confidence = "Low"
    
    data["outlook"] = outlook
    data["outlook_cn"] = outlook_cn
    data["rating"] = rating
    data["confidence"] = confidence
    
    return data

def check_system_status():
    """Check system status."""
    status = {
        "api_twelve": "❌",
        "api_alpha": "❌",
        "portfolio": "❌",
        "watchlist": "❌",
        "feishu": "❌"
    }
    
    # Check Twelve Data
    if os.environ.get("TWELVE_DATA_API_KEY"):
        status["api_twelve"] = "✅"
    
    # Check Alpha Vantage
    if os.environ.get("ALPHA_VANTAGE_API_KEY"):
        status["api_alpha"] = "✅"
    
    # Check Portfolio
    if PORTFOLIO_FILE.exists():
        try:
            with open(PORTFOLIO_FILE) as f:
                data = json.load(f)
                holdings_count = len([h for h in data.get("holdings", []) if h.get("shares", 0) > 0])
                status["portfolio"] = f"✅ {holdings_count}只持仓"
        except:
            status["portfolio"] = "⚠️ 未初始化"
    
    # Check Watchlist
    if WATCHLIST_FILE.exists():
        with open(WATCHLIST_FILE) as f:
            count = sum(1 for line in f if line.strip() and not line.startswith('#'))
            status["watchlist"] = f"✅ {count}只股票"
    
    # Check Feishu
    if FEISHU_CONFIG.exists():
        status["feishu"] = "✅"
    
    return status

def get_feature_list():
    """Get feature list."""
    return [
        ("📊 支撑阻力", "support_resistance.py"),
        ("📈 交易信号", "trading_signals.py"),
        ("💰 持仓计算", "position_calculator.py"),
        ("⚠️ 止损预警", "stop_loss_alerts.py"),
        ("🔔 实时监控", "realtime_monitor.py"),
        ("📉 回测引擎", "backtest_engine_v2.py"),
        ("📋 持仓管理", "portfolio_manager.py"),
        ("📰 三级日报", "daily_report.py"),
    ]

def generate_small(analyses, portfolio, report_type, date):
    """Small - Brief (10 sec) + System Status."""
    hk_time = get_hk_time()
    report_date = date.strftime("%Y-%m-%d")
    weekday_map = {"Mon": "周一", "Tue": "周二", "Wed": "周三", "Thu": "周四", "Fri": "周五"}
    weekday = weekday_map.get(date.strftime("%a"), "")
    
    emoji = "🌅" if report_type == "morning" else "🌆"
    title = "市场早盘简报" if report_type == "morning" else "市场盘后简报"
    
    # System status
    sys_status = check_system_status()
    
    bullish = sum(1 for a in analyses if a and "Bullish" in a.get("outlook", ""))
    bearish = sum(1 for a in analyses if a and "Bearish" in a.get("outlook", ""))
    neutral = len(analyses) - bullish - bearish
    
    if bearish > bullish * 2:
        sentiment = "偏空 🐻"
    elif bullish > bearish * 2:
        sentiment = "偏多 🐂"
    else:
        sentiment = "震荡 ➡️"
    
    sorted_analyses = sorted([a for a in analyses if a], key=lambda x: abs(x.get("change_5d", 0)), reverse=True)
    top_gainers = [a for a in sorted_analyses if a.get("change_5d", 0) > 2][:2]
    top_losers = [a for a in sorted_analyses if a.get("change_5d", 0) < -2][:2]
    
    # Get accuracy stats
    stats, _ = get_accuracy_stats()
    accuracy_str = ""
    if stats and stats['total_predictions'] > 0:
        accuracy_str = f"  准确度：{stats['accuracy_rate']:.0f}%"
    
    report = f"{emoji} {title} | {report_date} {weekday} {hk_time.strftime('%H:%M')}\n\n"
    
    # Simplified status line (no technical details)
    report += f"情绪：{sentiment}  涨跌：{bullish}📈 {neutral}➡️ {bearish}📉{accuracy_str}\n"
    
    if top_gainers or top_losers:
        report += "关注："
        if top_gainers:
            report += "🔺" + ", ".join(f"{a['symbol']}({a['change_5d']:+.1f}%)" for a in top_gainers) + "  "
        if top_losers:
            report += "🔻" + ", ".join(f"{a['symbol']}({a['change_5d']:+.1f}%)" for a in top_losers)
        report += "\n\n"
    else:
        report += "\n"
    
    report += "股票    价格      5 日      观点\n"
    report += "────────────────────────────\n"
    
    for a in sorted_analyses:
        change_emoji = "📈" if a["change_5d"] > 2 else "📉" if a["change_5d"] < -2 else "➡️"
        outlook_emoji = "🐂" if "Bullish" in a["outlook"] else "🐻" if "Bearish" in a["outlook"] else "➡️"
        report += f"{a['symbol']:<6}  ${a['price']:>7.2f}  {change_emoji}{a['change_5d']:>+7.1f}%  {outlook_emoji}\n"
    
    # Portfolio summary if exists
    if portfolio and portfolio.get("total_market_value", 0) > 0:
        pnl = portfolio.get("total_unrealized_pnl", 0)
        pnl_pct = portfolio.get("total_unrealized_pnl_pct", 0)
        report += f"\n持仓盈亏：{pnl:+,.0f} ({pnl_pct:+.2f}%)"
    
    report += "\n⚠️ AI 生成，仅供参考 · 市场有风险，投资需谨慎"
    
    return report

def get_accuracy_stats():
    """Get accuracy statistics from tracker."""
    try:
        from accuracy_tracker import calculate_statistics, generate_report
        stats = calculate_statistics(7)  # 7-day stats
        return stats, generate_report(stats)
    except:
        return None, ""

def verify_predictions(analyses):
    """Verify today's predictions against actual data."""
    try:
        from accuracy_tracker import load_accuracy_log, update_accuracy
        
        # Load today's actual prices
        actual_data = {}
        today = datetime.now().strftime("%Y-%m-%d")
        
        for a in analyses:
            symbol = a["symbol"]
            if symbol not in actual_data:
                actual_data[symbol] = {}
            actual_data[symbol][today] = a["price"]
        
        # Update accuracy
        updated = update_accuracy(actual_data)
        return updated
    except Exception as e:
        print(f"  ⚠️ 验证失败：{e}")
        return 0

def generate_medium(analyses, portfolio, report_type, date):
    """Medium - Standard (1 min) + System Status + Accuracy."""
    hk_time = get_hk_time()
    report_date = date.strftime("%Y-%m-%d")
    weekday = date.strftime("%A")
    
    emoji = "🌅" if report_type == "morning" else "🌆"
    title = "市场日报"
    subtitle = "Morning Market Brief" if report_type == "morning" else "Market Close Report"
    
    # Verify predictions (evening report)
    verified_count = 0
    if report_type == "evening":
        verified_count = verify_predictions(analyses)
    
    # System status
    sys_status = check_system_status()
    features = get_feature_list()
    
    port_summary = ""
    if portfolio and portfolio.get("total_market_value", 0) > 0:
        total_value = portfolio.get("total_market_value", 0)
        total_pnl = portfolio.get("total_unrealized_pnl", 0)
        total_pnl_pct = portfolio.get("total_unrealized_pnl_pct", 0)
        port_summary = f"\n**持仓盈亏**: ${total_value:,.0f} | {total_pnl:+,.0f} ({total_pnl_pct:+.2f}%)\n"
    
    bullish = sum(1 for a in analyses if a and "Bullish" in a.get("outlook", ""))
    bearish = sum(1 for a in analyses if a and "Bearish" in a.get("outlook", ""))
    neutral = len(analyses) - bullish - bearish
    
    # Accuracy stats
    stats, accuracy_report = get_accuracy_stats()
    accuracy_line = ""
    if stats:
        accuracy_line = f"  准确度：{stats['accuracy_rate']:.0f}% ({stats['accurate_predictions']}/{stats['total_predictions']})"
    
    report = f"""# {emoji} {title}

> 📅 **{report_date}** ({weekday}) · ⏰ **{hk_time.strftime("%H:%M")} HKT** · {subtitle}
{port_summary}
---

## 📊 市场情绪

| 看涨 🐂 | 中性 ➡️ | 看跌 🐻 |
|:------:|:------:|:------:|
| **{bullish}** | **{neutral}** | **{bearish}** |

---

## 🔍 个股分析

"""
    
    sorted_analyses = sorted([a for a in analyses if a], key=lambda x: abs(x.get("change_5d", 0)), reverse=True)
    
    for a in sorted_analyses:
        port_info = ""
        if "shares" in a and a.get("shares", 0) > 0:
            port_info = f"· 持仓：{a['shares']:,.0f}股 | 盈亏：{a['unrealized_pnl']:+,.0f} ({a['unrealized_pnl_pct']:+.2f}%)"
        
        report += f"""### {a['symbol']} - {a['rating']} {a['confidence']}

| 当前价格 | 5 日涨跌 | 20 日涨跌 | 30 日区间 |
|:--------:|:--------:|:---------:|:---------:|
| **${a['price']:.2f}** | {a['change_5d']:+.2f}% | {a['change_20d']:+.2f}% | ${a['low_30d']:.2f}-${a['high_30d']:.2f} |

**观点**: {a['outlook_cn']} {port_info}

---

"""
    
    report += """---
> ⚠️ 本报告由 AI 生成，仅供参考，不构成投资建议
> 数据来源：Twelve Data
"""
    
    return report

def generate_large(analyses, portfolio, report_type, date):
    """Large - Deep Dive (5 min) + Full System Report."""
    hk_time = get_hk_time()
    report_date = date.strftime("%Y-%m-%d")
    weekday = date.strftime("%A")
    
    emoji = "🌅" if report_type == "morning" else "🌆"
    title = "深度分析报告"
    subtitle = "System & Market Analysis"
    
    # System status
    sys_status = check_system_status()
    features = get_feature_list()
    
    bullish = sum(1 for a in analyses if a and ("Strong Bullish" in a.get("outlook", "") or "Bullish" in a.get("outlook", "")))
    bearish = sum(1 for a in analyses if a and ("Strong Bearish" in a.get("outlook", "") or "Bearish" in a.get("outlook", "")))
    
    if bullish > len(analyses) * 0.6:
        market_view = "整体偏多"
        action = "建议增持"
    elif bearish > len(analyses) * 0.6:
        market_view = "整体偏空"
        action = "建议减持"
    else:
        market_view = "震荡整理"
        action = "保持观望"
    
    port_section = ""
    if portfolio and portfolio.get("total_market_value", 0) > 0:
        port_section = f"""
## 💼 持仓分析

| 指标 | 数值 |
|------|------|
| 总市值 | ${portfolio.get('total_market_value', 0):,.2f} |
| 总成本 | ${portfolio.get('total_cost_basis', 0):,.2f} |
| 浮盈浮亏 | {portfolio.get('total_unrealized_pnl', 0):+,.2f} ({portfolio.get('total_unrealized_pnl_pct', 0):+.2f}%) |
| 持仓数量 | {len([h for h in portfolio.get('holdings', []) if h.get('shares', 0) > 0])} 只 |

### 持仓明细

| 股票 | 数量 | 成本 | 现价 | 市值 | 盈亏 | 占比 |
|------|------|------|------|------|------|------|
"""
        for h in portfolio.get("holdings", []):
            if h.get("shares", 0) > 0:
                # Use avg_cost for cost, current_price from data or fallback
                cost = h.get('avg_cost', 0)
                price = h.get('current_price', 0)
                if price == 0 and cost > 0:
                    # Fallback: estimate from market_value
                    price = h.get('market_value', 0) / h.get('shares', 1)
                port_section += f"| {h['symbol']} | {h['shares']:,.0f} | ${cost:.2f} | ${price:.2f} | ${h.get('market_value', 0):,.2f} | {h.get('unrealized_pnl', 0):+,.2f} | {h.get('weight', 0):.1f}% |\n"
    
    report = f"""# {emoji} {title}

> 📅 **{report_date}** ({weekday}) · ⏰ **{hk_time.strftime("%H:%M")} HKT** · {subtitle}

---

## 🖥️ 系统状态

### 核心组件

| 组件 | 状态 | 说明 |
|------|------|------|
| Twelve Data API | {sys_status['api_twelve']} | 主力数据源 (800 次/天) |
| Alpha Vantage API | {sys_status['api_alpha']} | 备用数据源 (25 次/天) |
| 持仓管理 | {sys_status['portfolio']} | 持仓数据跟踪 |
| 自选列表 | {sys_status['watchlist']} | 监控股票池 |
| 飞书推送 | {sys_status['feishu']} | 报告自动推送 |

### 功能模块

| 功能 | 文件 | 状态 |
|------|------|------|
"""
    
    for name, file in features:
        file_path = Path(__file__).parent / file
        status = "✅" if file_path.exists() else "❌"
        report += f"| {name} | `{file}` | {status} |\n"
    
    report += f"""
### API 使用统计

| API | 限额 | 已用 | 剩余 |
|-----|------|------|------|
| Twelve Data | 800/天 | ~{len(analyses)*2} | {800-len(analyses)*2} |
| Alpha Vantage | 25/天 | ~{len(analyses)} | {25-len(analyses)} |

---

## 📋 执行摘要

**市场观点**: {market_view}  
**操作建议**: {action}  
**置信度**: {'高' if abs(bullish - bearish) > len(analyses) * 0.5 else '中' if abs(bullish - bearish) > len(analyses) * 0.3 else '低'}

---
{port_section}
## 📊 市场情绪指标

| 指标 | 数值 | 解读 |
|------|------|------|
| 看涨比例 | {bullish/len(analyses)*100:.1f}% | {'多头主导' if bullish > bearish * 2 else '多空平衡' if abs(bullish - bearish) < 2 else '空头主导'} |
| 看跌比例 | {bearish/len(analyses)*100:.1f}% | - |

---

## 🔍 个股深度分析

"""
    
    sorted_analyses = sorted([a for a in analyses if a], key=lambda x: abs(x.get("change_5d", 0)), reverse=True)
    
    for a in sorted_analyses:
        port_info = ""
        if "shares" in a and a.get("shares", 0) > 0:
            port_info = f"""
**持仓信息**:
- 持仓数量：{a['shares']:,.0f} 股
- 平均成本：${a['avg_cost']:.2f}
- 当前盈亏：{a['unrealized_pnl']:+,.2f} ({a['unrealized_pnl_pct']:+.2f}%)
- 仓位占比：{a['weight']:.1f}%
"""
        
        report += f"""### {a['symbol']} | {a['rating']} | {a['confidence']}

**价格分析**:
- 当前价格：**${a['price']:.2f}**
- 5 日涨跌幅：{a['change_5d']:+.2f}%
- 20 日涨跌幅：{a['change_20d']:+.2f}%
- 30 日区间：${a['low_30d']:.2f} - ${a['high_30d']:.2f}

**技术观点**: {a['outlook_cn']}

**操作建议**: 
- 短线：{'买入' if 'Bullish' in a['outlook'] else '卖出' if 'Bearish' in a['outlook'] else '持有'}
- 中线：{'增持' if a['change_20d'] > 0 else '减持' if a['change_20d'] < 0 else '观望'}
- 支撑位：${a['low_30d']:.2f}
- 阻力位：${a['high_30d']:.2f}
{port_info}
---

"""
    
    report += f"""## 📈 后市展望

**关注重点**:
1. 美联储政策动向
2. 科技股财报季表现
3. 宏观经济数据发布

**风险提示**:
- 地缘政治风险
- 通胀数据超预期
- 利率政策变化

---

> 📌 **免责声明**: 本报告由 AI 生成，仅供参考，不构成投资建议  
> 📌 市场有风险，投资需谨慎  
> 📌 数据来源：Twelve Data · 生成时间：{hk_time.strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    return report

def save_report(report, report_type, size, date):
    """Save report to file."""
    report_date = date.strftime("%Y-%m-%d")
    filename = f"{report_date}_{report_type}_{size}.md"
    filepath = REPORTS_DIR / filename
    
    with open(filepath, "w") as f:
        f.write(report)
    
    print(f"📄 报告已保存：{filepath}")
    return filepath

def send_to_feishu(report, report_type, size):
    """Send report to Feishu (with duplicate prevention)."""
    if not FEISHU_CONFIG.exists():
        print("⚠️ 飞书配置不存在")
        return False
    
    with open(FEISHU_CONFIG) as f:
        config = json.load(f)
    
    chat_id = config.get("chat_id")
    if not chat_id:
        print("⚠️ chat_id 未配置")
        return False
    
    # Check if already sent today (prevent duplicates)
    sent_marker = SENT_DIR / f"{datetime.now().strftime('%Y-%m-%d')}_{report_type}_{size}.sent"
    if sent_marker.exists():
        print(f"⚠️ 今日{report_type} {size}报告已发送，跳过推送")
        return True
    
    # Use local Feishu config for push
    if FEISHU_CONFIG.exists():
        try:
            with open(FEISHU_CONFIG) as f:
                feishu_cfg = json.load(f)
            
            import urllib.request
            webhook_url = feishu_cfg.get("webhook_url")
            if webhook_url:
                data = json.dumps({
                    "msg_type": "text",
                    "content": {"text": report[:2000]}
                }).encode('utf-8')
                
                req = urllib.request.Request(
                    webhook_url,
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    if response.status == 200:
                        sent_marker.touch()
                        print("✅ 已推送到飞书")
                        return True
        except Exception as e:
            print(f"❌ 推送失败：{e}")
    
    return False

def main():
    if len(sys.argv) < 3:
        print("用法：python3 daily_report.py <morning|evening> <small|medium|large>")
        print("\n尺寸说明:")
        print("  small  - 简报 (10 秒阅读) - 适合快速推送")
        print("  medium - 标准 (1 分钟阅读) - 日常使用")
        print("  large  - 深度 (5 分钟阅读) - 周末/月度总结")
        sys.exit(1)
    
    report_type = sys.argv[1].lower()
    size = sys.argv[2].lower()
    
    if report_type not in ["morning", "evening"]:
        print("❌ 无效类型，使用 morning 或 evening")
        sys.exit(1)
    
    if size not in ["small", "medium", "large"]:
        print("❌ 无效尺寸，使用 small/medium/large")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"市场日报 | {report_type} {size}")
    print(f"{'='*60}\n")
    
    hk_time = get_hk_time()
    if not is_trading_day(hk_time):
        print("⚠️ 非交易日，跳过")
        sys.exit(0)
    
    # Load data
    portfolio = load_portfolio()
    watchlist = load_watchlist()
    
    print(f"📋 分析 {len(watchlist)} 只股票\n")
    
    # Analyze
    analyses = []
    for symbol in watchlist:
        result = analyze_stock(symbol, portfolio)
        if result:
            analyses.append(result)
    
    # Generate report
    print(f"\n📝 生成 {size} 报告...")
    
    if size == "small":
        report = generate_small(analyses, portfolio, report_type, hk_time)
    elif size == "medium":
        report = generate_medium(analyses, portfolio, report_type, hk_time)
    else:
        report = generate_large(analyses, portfolio, report_type, hk_time)
    
    # Save
    report_path = save_report(report, report_type, size, hk_time)
    
    # Send
    print(f"\n📤 推送报告...")
    send_to_feishu(report, report_type, size)
    
    print(f"\n{'='*60}")
    print("✅ 完成")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()