"""
Modèle Agent IA
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from backend.database.db import Base


class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # heliox, syntax, prisme
    provider = Column(String)  # gemini, claude, openai, ollama, etc.
    model = Column(String)
    
    # Strategy
    strategy = Column(String, default="momentum")  # momentum, mean_reversion, sentiment
    
    # Configuration
    api_key_hash = Column(String, nullable=True)
    config = Column(JSON, nullable=True)
    
    # Risk settings (slider)
    risk_level = Column(String, default="medium")  # low, medium, high
    risk_slider_value = Column(Float, default=0.5)  # 0.0 - 1.0
    
    # Performance
    total_predictions = Column(Integer, default=0)
    accuracy = Column(Float, nullable=True)
    total_profit = Column(Float, default=0.0)
    
    # Status
    is_active = Column(Integer, default=1)
    last_active = Column(DateTime, nullable=True)
    
    # System
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<Agent {self.name} ({self.provider})>"
