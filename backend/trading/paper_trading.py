"""
Paper Trading Mode (Simulation)
"""

from typing import Dict, Any, List
from datetime import datetime


class PaperTrading:
    """Paper trading mode (simulation without real money)"""
    
    def __init__(self, initial_balance: float = 10000.0):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions: List[Dict[str, Any]] = []
        self.trades: List[Dict[str, Any]] = []
        self._initialized = True
    
    def is_initialized(self) -> bool:
        return self._initialized
    
    async def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        """Simulate ticker fetch"""
        return {
            "symbol": symbol,
            "last": 100.0,
            "bid": 99.9,
            "ask": 100.1,
            "volume": 1000,
            "high": 102,
            "low": 98
        }
    
    async def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> List[Dict[str, Any]]:
        """Simulate OHLCV fetch"""
        return [{
            "timestamp": i * 3600000,
            "open": 100 + i * 0.5,
            "high": 100 + i * 0.5 + 2,
            "low": 100 + i * 0.5 - 2,
            "close": 100 + i * 0.5 + 1,
            "volume": 1000 + i
        } for i in range(limit)]
    
    async def create_order(
        self, symbol: str, type: str, side: str, amount: float, price: float = None
    ) -> Dict[str, Any]:
        """Simulate order creation"""
        current_price = price or 100
        
        if side == "buy":
            cost = amount * current_price
            if cost > self.balance:
                return {"success": False, "error": "Insufficient balance"}
            
            self.balance -= cost
            self.positions.append({
                "symbol": symbol,
                "side": "long",
                "amount": amount,
                "entry_price": current_price,
                "created_at": datetime.now().isoformat()
            })
        else:
            if self.positions:
                position = self.positions.pop(0)
                revenue = amount * current_price
                pnl = revenue - (amount * position["entry_price"])
                self.balance += revenue
                
                self.trades.append({
                    "symbol": symbol,
                    "side": "sell",
                    "amount": amount,
                    "price": current_price,
                    "pnl": pnl,
                    "timestamp": datetime.now().isoformat()
                })
        
        return {
            "success": True,
            "order_id": f"paper_{len(self.trades)}",
            "status": "filled",
            "symbol": symbol,
            "side": side,
            "amount": amount,
            "price": current_price
        }
    
    async def fetch_balance(self) -> Dict[str, Any]:
        """Fetch simulated balance"""
        return {
            "total": {"USDT": self.balance},
            "free": {"USDT": self.balance},
            "used": {"USDT": 0}
        }
    
    def get_performance(self) -> Dict[str, Any]:
        """Get trading performance"""
        total_trades = len(self.trades)
        winning_trades = sum(1 for t in self.trades if t.get("pnl", 0) > 0)
        
        total_pnl = sum(t.get("pnl", 0) for t in self.trades)
        
        return {
            "initial_balance": self.initial_balance,
            "current_balance": self.balance,
            "total_pnl": total_pnl,
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "win_rate": winning_trades / total_trades * 100 if total_trades > 0 else 0
        }
