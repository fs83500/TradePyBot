"""
Heliox Agent - Momentum Strategy
"""

from backend.agents.base_agent import BaseAgent
from typing import Dict, Any, Optional
from datetime import datetime


class HelioxAgent(BaseAgent):
    """Heliox Agent - Momentum trading strategy"""
    
    def __init__(self):
        super().__init__("heliox", "openai", "gpt-4o")
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize Heliox agent"""
        self.config = config
        self._initialized = True
        return True
    
    async def analyze_market(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market using momentum strategy
        
        Returns:
            {
                "signal": "buy" | "sell" | "hold",
                "confidence": float,
                "reasoning": str,
                "momentum_score": float
            }
        """
        # Momentum analysis based on price trends
        current_price = market_data.get("close", 0)
        sma_20 = market_data.get("sma_20", current_price)
        sma_50 = market_data.get("sma_50", current_price)
        volume = market_data.get("volume", 0)
        
        # Calculate momentum score
        momentum_score = 0.0
        
        if current_price > sma_20 > sma_50:
            momentum_score = 0.8
            signal = "buy"
        elif current_price < sma_20 < sma_50:
            momentum_score = -0.8
            signal = "sell"
        else:
            momentum_score = 0.0
            signal = "hold"
        
        # Adjust for volume
        if volume > 1000:
            momentum_score *= 1.1
            momentum_score = min(momentum_score, 1.0)
        
        return {
            "signal": signal,
            "confidence": abs(momentum_score) * 0.8 + 0.2,
            "reasoning": f"Momentum score: {momentum_score:.2f}. Trend {'bullish' if signal == 'buy' else 'bearish' if signal == 'sell' else 'sideways'}.",
            "momentum_score": momentum_score
        }
    
    async def execute_trade(
        self, 
        symbol: str, 
        direction: str, 
        amount: float,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute trade with momentum strategy"""
        return {
            "success": True,
            "order_id": f"heliox_{datetime.now().timestamp()}",
            "symbol": symbol,
            "direction": direction,
            "amount": amount,
            "strategy": "momentum"
        }
