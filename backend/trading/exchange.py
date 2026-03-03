"""
Exchange API (CCXT)
"""

from typing import Dict, Any, List
import ccxt.async_support as ccxt


class ExchangeAPI:
    """Wrapper around CCXT for exchange operations"""
    
    def __init__(self, exchange_id: str = "binance", api_key: str = None, secret: str = None):
        self.exchange_id = exchange_id
        self.api_key = api_key
        self.secret = secret
        self.exchange = None
        self._initialized = False
    
    async def initialize(self) -> bool:
        """Initialize exchange connection"""
        try:
            exchange_class = getattr(ccxt, self.exchange_id)
            self.exchange = exchange_class({
                'apiKey': self.api_key,
                'secret': self.secret,
                'enableRateLimit': True
            })
            await self.exchange.load_markets()
            self._initialized = True
            return True
        except Exception as e:
            print(f"Error initializing exchange: {e}")
            return False
    
    async def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        """Fetch ticker data"""
        if not self._initialized:
            return {"symbol": symbol, "last": 0}
        
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            return {
                "symbol": ticker["symbol"],
                "last": ticker["last"],
                "bid": ticker["bid"],
                "ask": ticker["ask"],
                "volume": ticker["baseVolume"],
                "high": ticker["high"],
                "low": ticker["low"]
            }
        except Exception:
            return {"symbol": symbol, "last": 0}
    
    async def fetch_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch OHLCV data"""
        if not self._initialized:
            return []
        
        try:
            ohlcv = await self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return [{
                "timestamp": c[0],
                "open": c[1],
                "high": c[2],
                "low": c[3],
                "close": c[4],
                "volume": c[5]
            } for c in ohlcv]
        except Exception:
            return []
    
    async def create_order(
        self, symbol: str, type: str, side: str, amount: float, price: float = None
    ) -> Dict[str, Any]:
        """Create a trade order"""
        if not self._initialized:
            return {"success": False, "error": "Exchange not initialized"}
        
        try:
            params = {}
            if type == "limit" and price:
                params["price"] = price
            
            order = await self.exchange.create_order(
                symbol=symbol, type=type, side=side, amount=amount, params=params
            )
            
            return {
                "success": True,
                "order_id": order["id"],
                "status": order["status"],
                "symbol": order["symbol"],
                "side": order["side"],
                "amount": order["amount"],
                "price": order["price"]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def fetch_balance(self) -> Dict[str, Any]:
        """Fetch account balance"""
        if not self._initialized:
            return {"total": {}, "free": {}, "used": {}}
        
        try:
            balance = await self.exchange.fetch_balance()
            return {
                "total": balance.get("total", {}),
                "free": balance.get("free", {}),
                "used": balance.get("used", {})
            }
        except Exception:
            return {"total": {}, "free": {}, "used": {}}
    
    async def close(self):
        """Close exchange connection"""
        if self.exchange:
            await self.exchange.close()
            self._initialized = False


class PaperTrading:
    """Paper trading mode (simulation)"""
    
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
            "volume": 1000
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
