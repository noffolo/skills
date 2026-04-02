---
name: trading-assistant
description: Trading analysis system with technical indicators, signals, and position management. Read-only market data, no trade execution.
version: 3.0.0
author: XuXuClassMate
license: MIT
category: Finance
tags:
  - trading
  - finance
  - technical-analysis
  - stock-market
  - openclaw
metadata:
  openclaw:
    requires:
      env:
        - TWELVE_DATA_API_KEY
        - ALPHA_VANTAGE_API_KEY
      bins:
        - python3
        - pip
    primaryEnv: TWELVE_DATA_API_KEY
    emoji: 📊
    homepage: https://github.com/XuXuClassMate/trading-assistant
    safety:
      level: safe
      audit: manual
      notes: Pure Python modules only. No subprocess, no shell execution. API keys from environment variables only. Read-only market data access.
---

# 📊 Trading Assistant

**Version**: v2.0.0 (Security Hardened) | **License**: MIT

Advanced trading analysis system providing technical indicators, trading signals, and position management for stock and crypto investors.

**Security Improvements in v2.0.0:**
- ✅ Removed TradingAgents and other heavy external dependencies
- ✅ No reading of sibling/parent `.env` files
- ✅ Direct API calls to Twelve Data and Alpha Vantage only
- ✅ All API keys loaded from environment variables only (not from `.env` files at runtime)
- ✅ No access to files outside the project directory
- ✅ Removed all `sys.path.insert()` calls to prevent sibling directory imports
- ✅ Removed runtime `.env` file loading (daily_report.py, news_sentiment_monitor.py)
- ✅ Removed `load_dotenv()` from config.py to prevent automatic `.env` scanning

**Dependencies:**
- `requests` - HTTP client for API calls (installed via requirements.txt)
- Standard Python libraries: `json`, `os`, `datetime`, `argparse`, etc.

---

## ✨ Features

- **Technical Indicators**: RSI, MACD, Bollinger Bands, KDJ, CCI, ADX, ATR, OBV, VWAP
- **Trading Signals**: Auto-generated BUY/SELL/HOLD signals with confidence scores
- **Position Sizing**: Smart position calculator based on risk profile and stop-loss
- **Support/Resistance**: Automatic calculation of key price levels
- **Multi-Market**: Support for A-shares, US stocks, and cryptocurrencies
- **Daily Reports**: Small (10s), Medium (1min), Large (5min) report formats
- **News Sentiment**: Alpha Vantage news sentiment analysis
- **Portfolio Management**: Track holdings and P&L

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

**Important**: This version does NOT load `.env` files at runtime. You must set environment variables directly:

**Option A: Export in shell (recommended)**
```bash
export TWELVE_DATA_API_KEY=your_twelve_data_key
export ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
```

**Option B: Set in shell profile (~/.bashrc or ~/.zshrc)**
```bash
echo 'export TWELVE_DATA_API_KEY=your_key' >> ~/.bashrc
echo 'export ALPHA_VANTAGE_API_KEY=your_key' >> ~/.bashrc
source ~/.bashrc
```

**Option C: Use with command**
```bash
TWELVE_DATA_API_KEY=your_key ALPHA_VANTAGE_API_KEY=your_key python3 trading_signals.py
```

Get free API keys:
- **Twelve Data**: https://twelvedata.com (800 calls/day, free tier)
- **Alpha Vantage**: https://www.alphavantage.co (25 calls/day, free tier)

### 3. Test Installation

```bash
python3 support_resistance.py
python3 trading_signals.py
python3 position_calculator.py
```

---

## 📖 Basic Usage

### Generate Trading Signal

```python
from trading_signals import generate_trading_signal
result = generate_trading_signal("AAPL")
print(result)
```

### Calculate Position Size

```python
from position_calculator import calculate_position_size
result = calculate_position_size(
    total_capital=100000,
    entry_price=175.64,
    stop_loss_price=165.00,
    risk_profile="moderate"
)
```

### Calculate Support/Resistance

```python
from support_resistance import calculate_support_resistance
result = calculate_support_resistance("NVDA")
```

---

## 📁 Directory Structure

```
trading-assistant/
├── SKILL.md                 # This file
├── README.md                # Full documentation (Chinese)
├── README_en.md             # Full documentation (English)
├── requirements.txt         # Dependencies
├── .env.example             # Config template
├── config.py                # Configuration (v2.0: no external .env access)
├── support_resistance.py    # Support/resistance module
├── trading_signals.py       # Signal generator
├── position_calculator.py   # Position sizing
├── daily_report.py          # Daily report generator
├── portfolio_manager.py     # Portfolio tracking
└── news_sentiment_monitor.py # News sentiment analysis
```

---

## 🔒 Security Model

**此技能是安全的：**
- ✅ 仅读取标准环境变量获取 API 密钥
- ✅ 仅连接 Twelve Data 和 Alpha Vantage 官方 API
- ✅ 仅在自身目录内读写文件
- ✅ 只读市场数据，不执行交易
- ✅ 无需经纪商或交易所凭证

**此技能不做：**
- ❌ 不读取 .env 文件
- ❌ 不访问父目录或兄弟目录
- ❌ 不执行后台任务或自主操作
- ❌ 不发送数据到未授权端点

---

## 📚 Documentation

For detailed usage including daily reports, learning system, and automation setup, see:

- **Chinese**: `README.md`
- **English**: `README_en.md`
- **GitHub**: https://github.com/XuXuClassMate/trading-assistant

---

## ⚠️ Disclaimer

**For educational and research purposes only. Not financial advice.**

- Market investments carry risks
- Past performance does not guarantee future results
- Users are responsible for their own investment decisions
- This tool does not execute trades or provide brokerage services

---

## 🔗 Links

- **GitHub**: https://github.com/XuXuClassMate/trading-assistant
- **Issues**: https://github.com/XuXuClassMate/trading-assistant/issues
- **OpenClaw**: https://openclaw.ai
- **ClawHub**: https://clawhub.com

---

## 📝 Changelog / 版本历史

### v2.0.0 (2026-04-01) - Security Hardened / 安全加固

**Security Fixes / 安全修复**:
- ✅ Removed all `sys.path.insert()` calls (9 files) / 移除所有 sys.path.insert() 调用
- ✅ Removed runtime `.env` file loading (4 files) / 移除运行时 .env 文件加载
- ✅ Removed `load_dotenv()` from `config.py` / 从 config.py 移除 load_dotenv()
- ✅ Removed sibling module imports / 移除兄弟模块导入
- ✅ Updated SKILL.md security model / 更新 SKILL.md 安全模型

**Breaking Changes / 重大变更**:
- ⚠️ API keys must be set via environment variables (no `.env` file loading)
- ⚠️ API 密钥必须通过环境变量设置 (不再加载 .env 文件)
- ⚠️ Removed `python-dotenv` dependency / 移除 python-dotenv 依赖

**Release Channels / 发布渠道**:
- ✅ PyPI: `trading-assistant==2.0.0`
- ✅ npm: `@xuxuclassmate/trading-assistant@2.0.0`
- ✅ Docker Hub: `xuxuclassmate/trading-assistant:v2.0.0`
- ✅ GHCR: `ghcr.io/xuxuclassmate/trading-assistant:v2.0.0`
- ✅ GitHub Release: v2.0.0
- ✅ ClawHub: trading-assistant@2.0.0

### v1.3.1 (2026-03-28)
- Bug fixes and improvements / 错误修复和改进

### v1.1.0 (2026-03-24)
- Take Profit / Stop Loss Alerts / 止盈止损提醒

---

**Last Updated**: 2026-04-01
**Security Audit**: v2.0.0 - Removed external dependencies, hardened API key handling
