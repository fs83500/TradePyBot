"""
Modèle Trade
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from backend.database.db import Base
from datetime import datetime
from enum import Enum as PyEnum


class TradeDirection(str, PyEnum):
    """Direction du trade"""
    LONG = "long"
    SHORT = "short"


class TradeStatus(str, PyEnum):
    """Statut du trade"""
    PENDING = "pending"
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    direction = Column(Enum(TradeDirection))
    entry_price = Column(Float)
    exit_price = Column(Float, nullable=True)
    amount = Column(Float)
    profit = Column(Float, nullable=True)
    status = Column(Enum(TradeStatus), default=TradeStatus.PENDING)
    
    agent_id = Column(Integer, nullable=True)
    agent_name = Column(String, nullable=True)  # heliox, syntax, prisme
    exchange = Column(String, default="paper")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    closed_at = Column(DateTime, nullable=True)
    
    # Additional info
    reason = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Trade {self.symbol} {self.direction} {self.status}>"
