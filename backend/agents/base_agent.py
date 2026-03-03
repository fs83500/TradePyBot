"""
Base class for AI Agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, name: str, provider: str, model: str):
        self.name = name
        self.provider = provider
        self.model = model
        self.config: Dict[str, Any] = {}
        self._initialized = False
    
    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the agent with configuration"""
        pass
    
    @abstractmethod
    async def analyze_market(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market data and return prediction
        
        Args:
            market_data: OHLCV data and indicators
            
        Returns:
            {
                "signal": "buy" | "sell" | "hold",
                "confidence": float,
                "target_price": float,
                "stop_loss": float,
                "take_profit": float,
                "reasoning": str
            }
        """
        pass
    
    @abstractmethod
    async def execute_trade(
        self, 
        symbol: str, 
        direction: str, 
        amount: float,
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a trade
        
        Args:
            symbol: Trading pair (e.g., "BTC/USDT")
            direction: "long" or "short"
            amount: Amount to trade
            config: Exchange-specific config
            
        Returns:
            {
                "success": bool,
                "order_id": str,
                "executed_price": float,
                "executed_amount": float
            }
        """
        pass
    
    async def learn(self, feedback: Dict[str, Any]) -> None:
        """Learn from feedback"""
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            "name": self.name,
            "provider": self.provider,
            "model": self.model,
            "initialized": self._initialized
        }
