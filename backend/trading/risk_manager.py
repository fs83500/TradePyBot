"""
Risk Manager
"""

from typing import Dict, Any
from backend.config import settings


class RiskManager:
    """Manage trading risk"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.max_risk_percent = self.config.get("max_risk_percent", settings.trading.max_risk_percent)
        self.max_daily_loss = self.config.get("max_daily_loss", 100.0)
    
    def calculate_position_size(
        self, 
        balance: float, 
        risk_percent: float = None, 
        stop_loss_percent: float = 2.0
    ) -> float:
        """Calculate position size based on risk"""
        risk_percent = risk_percent or self.max_risk_percent
        
        risk_amount = balance * (risk_percent / 100)
        position_size = risk_amount / (balance * (stop_loss_percent / 100))
        
        return position_size
    
    def check_risk(
        self, 
        trade_params: Dict[str, Any], 
        current_balance: float
    ) -> Dict[str, Any]:
        """Check if trade meets risk criteria"""
        position_size = self.calculate_position_size(
            current_balance,
            trade_params.get("risk_percent"),
            trade_params.get("stop_loss_percent")
        )
        
        daily_loss = trade_params.get("potential_loss", 0)
        if daily_loss > self.max_daily_loss:
            return {
                "allowed": False,
                "reason": f"Daily loss {daily_loss} exceeds limit {self.max_daily_loss}",
                "adjusted_position": 0
            }
        
        return {
            "allowed": True,
            "reason": "Risk criteria met",
            "adjusted_position": position_size
        }
    
    def get_risk_score(self, symbol: str, volatility: float) -> float:
        """Calculate risk score for a symbol"""
        base_score = min(volatility / 100, 1.0)
        return min(base_score, 1.0)
