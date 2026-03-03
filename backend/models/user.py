"""
Modèle User (token)
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from backend.database.db import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, default="trader")
    
    # Token authentication (comme OpenClaw gateway)
    token_hash = Column(String)  # Stocke le hash, pas le token
    token_type = Column(String, default="bearer")
    token_expiry = Column(DateTime, nullable=True)
    
    # Permissions
    role = Column(String, default="user")  # user, admin
    permissions = Column(Text, nullable=True)
    
    # Configuration
    is_active = Column(Integer, default=1)
    last_login = Column(DateTime, nullable=True)
    
    # System
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<User {self.username} (token)>"
