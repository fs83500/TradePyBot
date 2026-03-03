"""
Configuration du TradePyBot
"""

from pydantic_settings import BaseSettings
from typing import Dict, Any, Optional


class AISettings(BaseSettings):
    """Configuration des providers IA"""
    gemini: Optional[Dict[str, Any]] = None
    claude: Optional[Dict[str, Any]] = None
    openai: Optional[Dict[str, Any]] = None
    groq: Optional[Dict[str, Any]] = None
    deepseek: Optional[Dict[str, Any]] = None
    mistral: Optional[Dict[str, Any]] = None
    ollama: Optional[Dict[str, Any]] = None


class DatabaseSettings(BaseSettings):
    """Configuration de la base de données"""
    dev_url: str = "sqlite+aiosqlite:///./trading.db"
    prod_url: str = "postgresql://user:pass@localhost/trading"
    echo: bool = False


class AuthSettings(BaseSettings):
    """Configuration de l'authentification"""
    secret_key: str = "TradePyBot-Secret-Key-2024"
    token_expiry_hours: int = 24
    algorithm: str = "HS256"


class TradingSettings(BaseSettings):
    """Configuration du trading"""
    default_amount: float = 100.0
    max_risk_percent: float = 2.0
    paper_mode: bool = True


class Settings(BaseSettings):
    """Configuration principale"""
    app_name: str = "TradePyBot"
    app_version: str = "1.0.0"
    debug: bool = False
    
    ai: AISettings = AISettings()
    database: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()
    trading: TradingSettings = TradingSettings()


settings = Settings()
