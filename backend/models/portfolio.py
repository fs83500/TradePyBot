"""
Modèle Portfolio
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from backend.database.db import Base
from datetime import datetime
from enum import Enum as PyEnum


class PortfolioType(str, PyEnum):
    """Type de portfolio"""
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"


class Portfolio(Base):
    __tablename__ = "portfolio"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, default="default")
    type = Column(Enum(PortfolioType), default=PortfolioType.PAPER)
    
    # Balance information
    initial_balance = Column(Float, default=1000.0)
    current_balance = Column(Float, default=1000.0)
    free_balance = Column(Float, default=1000.0)
    used_balance = Column(Float, default=0.0)
    total_pnl = Column(Float, default=0.0)
    
    # Statistics
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    
    # Configuration
    max_risk_percent = Column(Float, default=2.0)
    max_daily_loss = Column(Float, default=100.0)
    
    is_active = Column(Integer, default=1)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<Portfolio {self.name} Balance: {self.current_balance}>"
