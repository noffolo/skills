#!/usr/bin/env python3
"""
Interactive Holdings Setup - 交互式持仓设置
"""

import json
from pathlib import Path

PORTFOLIO_FILE = Path(__file__).parent / "portfolio" / "holdings.json"
WATCHLIST_FILE = Path(__file__).parent / "watchlist.txt"

def load_watchlist():
    if not WATCHLIST_FILE.exists():
        return []
    
    holdings = []
    with open(WATCHLIST_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('|')
                symbol = parts[0].strip()
                name = parts[1].strip() if len(parts) > 1 else symbol
                holdings.append({"symbol": symbol, "name": name})
    return holdings

def setup():
    print("=" * 60)
    print("📊 持仓设置")
    print("=" * 60)
    print("\n请输入每只股票的持仓信息 (直接回车跳过)\n")
    
    holdings = load_watchlist()
    portfolio = {
        "holdings": [],
        "total_market_value": 0,
        "total_cost_basis": 0,
        "total_unrealized_pnl": 0,
        "total_unrealized_pnl_pct": 0,
        "cash": 0,
        "last_updated": None
    }
    
    for stock in holdings:
        print(f"\n--- {stock['symbol']} - {stock['name']} ---")
        
        shares_input = input(f"持仓数量 (股): ").strip()
        shares = float(shares_input) if shares_input else 0
        
        if shares == 0:
            print("⊘ 跳过 (无持仓)")
            portfolio["holdings"].append({
                "symbol": stock["symbol"],
                "name": stock["name"],
                "shares": 0,
                "avg_cost": 0,
                "current_price": 0,
                "market_value": 0,
                "cost_basis": 0,
                "unrealized_pnl": 0,
                "unrealized_pnl_pct": 0,
                "weight": 0,
                "notes": ""
            })
            continue
        
        cost_input = input(f"平均成本 (USD): ").strip()
        avg_cost = float(cost_input) if cost_input else 0
        
        notes = input(f"备注 (可选): ").strip()
        
        portfolio["holdings"].append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": shares,
            "avg_cost": avg_cost,
            "current_price": 0,
            "market_value": 0,
            "cost_basis": shares * avg_cost,
            "unrealized_pnl": 0,
            "unrealized_pnl_pct": 0,
            "weight": 0,
            "notes": notes
        })
        
        print(f"✅ 已添加：{shares:,.0f} 股 @ ${avg_cost:.2f}")
    
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("✅ 持仓设置完成！")
    print("=" * 60)
    print(f"\n保存位置：{PORTFOLIO_FILE}")
    print("\n下一步:")
    print("1. python3 portfolio_manager.py update - 更新实时价格")
    print("2. python3 daily_report.py morning small - 生成简报")
    print("3. python3 daily_report.py evening large - 生成深度报告")
    print("\n")

if __name__ == "__main__":
    setup()
