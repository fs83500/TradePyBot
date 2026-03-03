"""
Syntax Agent - Mean Reversion Strategy
"""

from backend.agents.base_agent import BaseAgent
from typing import Dict, Any, Optional
from datetime import datetime


class SyntaxAgent(BaseAgent):
    """Syntax Agent - Mean reversion trading strategy"""
    
    def __init__(self):
        super().__init__("syntax", "claude", "claude-3-sonnet")
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize Syntax agent"""
        self.config = config
        self._initialized = True
        return True
    
    async def analyze_market(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market using mean reversion strategy
        
        Returns:
            {
                "signal": "buy" | "sell" | "hold",
                "confidence": float,
                "reasoning": str,
                "bb_position": float  # Position in Bollinger Bands (0-1)
            }
        """
        current_price = market_data.get("close", 0)
        upper_band = market_data.get("upper_band", current_price)
        lower_band = market_data.get("lower_band", current_price)
        middle_band = market_data.get("middle_band", current_price)
        
        # Calculate BB position (0 = lower, 0.5 = middle, 1 = upper)
        bb_position = (current_price - lower_band) / (upper_band - lower_band) if upper_band != lower_band else 0.5
        
        # Mean reversion signal
        if bb_position < 0.2:
            signal = "buy"
            confidence = 0.7 + (0.2 - bb_position) * 2
            confidence = min(confidence, 0.95)
        elif bb_position > 0.8:
            signal = "sell"
            confidence = 0.7 + (bb_position - 0.8) * 2
            confidence = min(confidence, 0.95)
        else:
            signal = "hold"
            confidence = 0.4
        
        return {
            "signal": signal,
            "confidence": confidence,
            "reasoning": f"BB position: {bb_position:.2f}. {'Mean reversion buy opportunity' if signal == 'buy' else 'Mean reversion sell opportunity' if signal == 'sell' else 'Neutral zone'}",
            "bb_position": bb_position
        }
    
    async def execute_trade(
        self, 
        symbol: str, 
        direction: str, 
        amount: float,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute trade with mean reversion strategy"""
        return {
            "success": True,
            "order_id": f"syntax_{datetime.now().timestamp()}",
            "symbol": symbol,
            "direction": direction,
            "amount": amount,
            "strategy": "mean_reversion"
        }
