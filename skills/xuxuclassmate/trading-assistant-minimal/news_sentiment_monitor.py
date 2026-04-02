#!/usr/bin/env python3
"""
News & Social Media Sentiment Monitor
整合新闻、社交媒体情绪数据，提高预测准确度
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests

# Security: Do not load .env files at runtime.
# API keys must be set via standard environment variables only.
# This prevents accidental exposure of unrelated secrets.

def get_hk_time():
    """Get Hong Kong time."""
    try:
        return datetime.now(ZoneInfo("Asia/Shanghai"))
    except:
        return datetime.now()

def analyze_news_sentiment(symbols):
    """
    Analyze news sentiment for given symbols.
    Uses Alpha Vantage News API directly (no external dependencies).
    """
    print("📰 分析新闻情绪...")
    
    sentiments = {}
    
    # Use Alpha Vantage news API directly
    sentiments = analyze_news_alpha_vantage(symbols)
    
    return sentiments

def analyze_news_alpha_vantage(symbols):
    """Fallback: Use Alpha Vantage news sentiment API."""
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        return {symbol: {"sentiment": "neutral", "score": 0, "news_count": 0} for symbol in symbols}
    
    sentiments = {}
    for symbol in symbols:
        try:
            import urllib.request
            url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={api_key}"
            
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            if "feed" in data and len(data["feed"]) > 0:
                # Calculate average sentiment
                total_sentiment = 0
                for item in data["feed"][:5]:  # Last 5 news
                    if "overall_sentiment_score" in item:
                        total_sentiment += float(item["overall_sentiment_score"])
                
                avg_score = total_sentiment / min(5, len(data["feed"]))
                
                if avg_score > 0.15:
                    sentiment = "bullish"
                elif avg_score < -0.15:
                    sentiment = "bearish"
                else:
                    sentiment = "neutral"
                
                sentiments[symbol] = {
                    "sentiment": sentiment,
                    "score": avg_score,
                    "news_count": len(data["feed"]),
                    "headline": data["feed"][0].get("title", "")[:50]
                }
            else:
                sentiments[symbol] = {"sentiment": "neutral", "score": 0, "news_count": 0}
        except Exception as e:
            print(f"  ⚠️ {symbol}: {e}")
            sentiments[symbol] = {"sentiment": "neutral", "score": 0, "news_count": 0}
    
    return sentiments

def analyze_social_sentiment(symbols):
    """
    Analyze social media sentiment.
    Returns neutral sentiment (social media analysis requires external API).
    """
    print("📱 分析社交媒体情绪...")
    
    sentiments = {}
    
    # Social media analysis requires external API (not implemented in standalone mode)
    for symbol in symbols:
        sentiments[symbol] = {
            "sentiment": "neutral",
            "score": 0,
            "mentions": 0,
            "trending": False
        }
        print(f"  {symbol}: neutral (social API not configured)")
    
    return sentiments

def combine_sentiments(news_sent, social_sent):
    """Combine news and social sentiment into final score."""
    combined = {}
    
    for symbol in news_sent.keys():
        news_score = news_sent[symbol].get("score", 0)
        social_score = social_sent.get(symbol, {}).get("score", 0)
        
        # Weight: News 60%, Social 40%
        final_score = (news_score * 0.6) + (social_score * 0.4)
        
        if final_score > 0.1:
            sentiment = "bullish"
        elif final_score < -0.1:
            sentiment = "bearish"
        else:
            sentiment = "neutral"
        
        combined[symbol] = {
            "sentiment": sentiment,
            "score": final_score,
            "news_score": news_score,
            "social_score": social_score,
            "confidence": "high" if abs(final_score) > 0.3 else "medium" if abs(final_score) > 0.15 else "low"
        }
    
    return combined

def get_sentiment_emoji(sentiment):
    """Get emoji for sentiment."""
    if sentiment == "bullish":
        return "🐂"
    elif sentiment == "bearish":
        return "🐻"
    else:
        return "➡️"

def generate_sentiment_report(combined, symbols):
    """Generate sentiment report for daily report."""
    report = "\n## 📰 新闻 & 社交媒体情绪\n\n"
    report += "| 股票 | 综合情绪 | 分数 | 新闻 | 社交 | 置信度 |\n"
    report += "|------|---------|------|------|------|--------|\n"
    
    for symbol in symbols:
        if symbol in combined:
            data = combined[symbol]
            emoji = get_sentiment_emoji(data["sentiment"])
            report += f"| {symbol} | {emoji} {data['sentiment']} | {data['score']:+.2f} | {data['news_score']:+.2f} | {data['social_score']:+.2f} | {data['confidence']} |\n"
    
    # Count sentiment
    bullish = sum(1 for s in combined.values() if s["sentiment"] == "bullish")
    bearish = sum(1 for s in combined.values() if s["sentiment"] == "bearish")
    neutral = len(combined) - bullish - bearish
    
    report += f"\n**情绪分布**: {bullish}🐂 看涨 | {neutral}➡️ 中性 | {bearish}🐻 看跌\n"
    
    return report

def main():
    """Main function."""
    print("=" * 60)
    print("📰 新闻 & 社交媒体情绪监控")
    print("=" * 60)
    
    # Load watchlist
    watchlist_file = Path(__file__).parent / "watchlist.txt"
    if not watchlist_file.exists():
        print("❌ watchlist.txt 不存在")
        return
    
    symbols = []
    with open(watchlist_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                symbol = line.split('|')[0].strip().upper()
                if symbol:
                    symbols.append(symbol)
    
    print(f"\n分析 {len(symbols)} 只股票：{', '.join(symbols)}\n")
    
    # Analyze
    news_sent = analyze_news_sentiment(symbols)
    social_sent = analyze_social_sentiment(symbols)
    
    # Combine
    combined = combine_sentiments(news_sent, social_sent)
    
    # Generate report
    report = generate_sentiment_report(combined, symbols)
    print(report)
    
    # Save
    output_file = Path(__file__).parent / "sentiment_report.json"
    with open(output_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "symbols": symbols,
            "sentiments": combined
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 情绪报告已保存：{output_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
