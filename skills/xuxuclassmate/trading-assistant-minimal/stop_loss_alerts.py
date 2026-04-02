#!/usr/bin/env python3
"""
Stop Loss & Take Profit Alerts / 止盈止损提醒

功能:
- 设置止盈止损位
- 监控价格触达
- 发送推送通知
- 记录触发历史

Features:
- Set take-profit and stop-loss levels
- Monitor price triggers
- Send push notifications
- Log trigger history
"""

from datetime import datetime
from pathlib import Path
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

from config import DATA_DIR, LOG_DIR
from i18n import t

# 数据目录
ALERTS_DIR = DATA_DIR / "alerts"
ALERTS_DIR.mkdir(exist_ok=True)


@dataclass
class AlertConfig:
    """止盈止损配置"""
    symbol: str
    entry_price: float
    stop_loss_price: float
    take_profit_price: float
    shares: int = 0
    status: str = "active"  # active, triggered, cancelled
    created_at: str = ""
    triggered_at: str = ""
    triggered_type: str = ""  # stop_loss, take_profit
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    @property
    def risk_reward_ratio(self) -> float:
        """风险收益比"""
        risk = abs(self.entry_price - self.stop_loss_price)
        reward = abs(self.take_profit_price - self.entry_price)
        if risk == 0:
            return 0
        return reward / risk
    
    @property
    def potential_profit(self) -> float:
        """潜在盈利"""
        return (self.take_profit_price - self.entry_price) * self.shares
    
    @property
    def potential_loss(self) -> float:
        """潜在亏损"""
        return (self.entry_price - self.stop_loss_price) * self.shares


class StopLossAlert:
    """止盈止损提醒系统"""
    
    def __init__(self, symbol: str, current_price: float):
        self.symbol = symbol
        self.current_price = current_price
        self.alerts_file = ALERTS_DIR / f"{symbol}_alerts.json"
        self.logs_file = LOG_DIR / f"{symbol}_alerts.log"
        self.alerts = self._load_alerts()
    
    def _load_alerts(self) -> List[AlertConfig]:
        """加载配置"""
        if self.alerts_file.exists():
            with open(self.alerts_file, 'r') as f:
                data = json.load(f)
                return [AlertConfig(**item) for item in data]
        return []
    
    def _save_alerts(self):
        """保存配置"""
        with open(self.alerts_file, 'w') as f:
            json.dump([asdict(a) for a in self.alerts], f, indent=2)
    
    def _log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.logs_file, 'a') as f:
            f.write(log_entry)
        
        print(log_entry.strip())
    
    def create_alert(
        self,
        entry_price: float,
        stop_loss_price: float,
        take_profit_price: float,
        shares: int = 0
    ) -> AlertConfig:
        """
        创建止盈止损提醒
        
        Args:
            entry_price: 入场价
            stop_loss_price: 止损价
            take_profit_price: 止盈价
            shares: 股数
        
        Returns:
            AlertConfig 配置对象
        """
        alert = AlertConfig(
            symbol=self.symbol,
            entry_price=entry_price,
            stop_loss_price=stop_loss_price,
            take_profit_price=take_profit_price,
            shares=shares
        )
        
        self.alerts.append(alert)
        self._save_alerts()
        
        self._log(f"Created alert: Entry=${entry_price}, SL=${stop_loss_price}, TP=${take_profit_price}, Shares={shares}")
        self._log(f"Risk/Reward Ratio: {alert.risk_reward_ratio:.2f}")
        self._log(f"Potential Profit: ${alert.potential_profit:.2f}")
        self._log(f"Potential Loss: ${alert.potential_loss:.2f}")
        
        return alert
    
    def check_triggers(self, current_price: Optional[float] = None) -> List[AlertConfig]:
        """
        检查是否触发止盈止损
        
        Args:
            current_price: 当前价格（默认使用实例价格）
        
        Returns:
            触发的提醒列表
        """
        if current_price is None:
            current_price = self.current_price
        
        triggered = []
        
        for alert in self.alerts:
            if alert.status != "active":
                continue
            
            # 检查止损
            if current_price <= alert.stop_loss_price:
                alert.status = "triggered"
                alert.triggered_at = datetime.now().isoformat()
                alert.triggered_type = "stop_loss"
                triggered.append(alert)
                
                self._log(f"🔴 STOP LOSS TRIGGERED! Price=${current_price} <= SL=${alert.stop_loss_price}")
                self._log(f"   Symbol: {alert.symbol}")
                self._log(f"   Entry: ${alert.entry_price} → Loss: ${alert.potential_loss:.2f}")
            
            # 检查止盈
            elif current_price >= alert.take_profit_price:
                alert.status = "triggered"
                alert.triggered_at = datetime.now().isoformat()
                alert.triggered_type = "take_profit"
                triggered.append(alert)
                
                self._log(f"🟢 TAKE PROFIT TRIGGERED! Price=${current_price} >= TP=${alert.take_profit_price}")
                self._log(f"   Symbol: {alert.symbol}")
                self._log(f"   Entry: ${alert.entry_price} → Profit: ${alert.potential_profit:.2f}")
        
        if triggered:
            self._save_alerts()
        
        return triggered
    
    def get_active_alerts(self) -> List[AlertConfig]:
        """获取所有活跃的提醒"""
        return [a for a in self.alerts if a.status == "active"]
    
    def get_triggered_alerts(self) -> List[AlertConfig]:
        """获取已触发的提醒"""
        return [a for a in self.alerts if a.status == "triggered"]
    
    def cancel_alert(self, index: int) -> bool:
        """取消提醒"""
        if 0 <= index < len(self.alerts):
            self.alerts[index].status = "cancelled"
            self._save_alerts()
            self._log(f"Cancelled alert #{index}")
            return True
        return False
    
    def get_summary(self) -> Dict:
        """获取摘要信息"""
        active = self.get_active_alerts()
        triggered = self.get_triggered_alerts()
        
        return {
            "symbol": self.symbol,
            "current_price": self.current_price,
            "total_alerts": len(self.alerts),
            "active": len(active),
            "triggered": len(triggered),
            "cancelled": len(self.alerts) - len(active) - len(triggered),
        }


def calculate_stop_loss_levels(
    entry_price: float,
    stop_loss_percent: float = 5.0,
    take_profit_percent: float = 10.0
) -> Dict[str, float]:
    """
    计算止盈止损位
    
    Args:
        entry_price: 入场价
        stop_loss_percent: 止损百分比（默认 5%）
        take_profit_percent: 止盈百分比（默认 10%）
    
    Returns:
        包含止损价和止盈价的字典
    """
    stop_loss_price = entry_price * (1 - stop_loss_percent / 100)
    take_profit_price = entry_price * (1 + take_profit_percent / 100)
    
    return {
        "entry_price": entry_price,
        "stop_loss_price": round(stop_loss_price, 2),
        "take_profit_price": round(take_profit_price, 2),
        "stop_loss_percent": stop_loss_percent,
        "take_profit_percent": take_profit_percent,
        "risk_reward_ratio": round(take_profit_percent / stop_loss_percent, 2)
    }


# 示例用法
if __name__ == "__main__":
    print("=" * 60)
    print("Stop Loss & Take Profit Alerts / 止盈止损提醒")
    print("=" * 60)
    print()
    
    # 示例：NVDA
    symbol = "NVDA"
    current_price = 175.64
    
    print(f"Symbol: {symbol}")
    print(f"Current Price: ${current_price}")
    print()
    
    # 计算止盈止损位
    levels = calculate_stop_loss_levels(current_price, stop_loss_percent=5, take_profit_percent=10)
    print("Calculated Levels / 计算的价格位:")
    print(f"  Entry Price: ${levels['entry_price']}")
    print(f"  Stop Loss: ${levels['stop_loss_price']} (-{levels['stop_loss_percent']}%)")
    print(f"  Take Profit: ${levels['take_profit_price']} (+{levels['take_profit_percent']}%)")
    print(f"  Risk/Reward Ratio: {levels['risk_reward_ratio']}")
    print()
    
    # 创建提醒
    alert_system = StopLossAlert(symbol, current_price)
    
    alert = alert_system.create_alert(
        entry_price=current_price,
        stop_loss_price=levels['stop_loss_price'],
        take_profit_price=levels['take_profit_price'],
        shares=100
    )
    
    print(f"Alert Created / 提醒已创建:")
    print(f"  Entry: ${alert.entry_price}")
    print(f"  Stop Loss: ${alert.stop_loss_price}")
    print(f"  Take Profit: ${alert.take_profit_price}")
    print(f"  Shares: {alert.shares}")
    print(f"  Risk/Reward: {alert.risk_reward_ratio:.2f}")
    print(f"  Potential Profit: ${alert.potential_profit:.2f}")
    print(f"  Potential Loss: ${alert.potential_loss:.2f}")
    print()
    
    # 获取摘要
    summary = alert_system.get_summary()
    print(f"Summary / 摘要:")
    print(f"  Total Alerts: {summary['total_alerts']}")
    print(f"  Active: {summary['active']}")
    print(f"  Triggered: {summary['triggered']}")
    print()
    
    # 模拟价格触达止损
    print("Simulating price drop to stop loss...")
    test_price = levels['stop_loss_price'] - 1.0
    triggered = alert_system.check_triggers(test_price)
    
    if triggered:
        print(f"Triggered alerts: {len(triggered)}")
        for t in triggered:
            print(f"  - {t.triggered_type.upper()} at ${test_price}")
    print()
    
    print("=" * 60)
    print("Test completed! Check logs/ and data/alerts/ for details.")
    print("=" * 60)
