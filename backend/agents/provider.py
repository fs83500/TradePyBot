"""
AI Providers Configuration
"""

from typing import Dict, Any, Optional
from enum import Enum


class ProviderType(str, Enum):
    """Type de provider IA"""
    API_KEY = "api_key"
    OAUTH = "oauth"
    LOCAL = "local"


class AIProviders:
    """Configuration des providers IA"""
    
    PROVIDERS: Dict[str, Dict[str, Any]] = {
        "gemini": {
            "type": ProviderType.OAUTH,
            "name": "Google Gemini",
            "models": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
            "oauth_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "api_url": "https://generativelanguage.googleapis.com"
        },
        "claude": {
            "type": ProviderType.API_KEY,
            "name": "Anthropic Claude",
            "models": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
            "api_url": "https://api.anthropic.com"
        },
        "openai": {
            "type": ProviderType.API_KEY,
            "name": "OpenAI",
            "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            "api_url": "https://api.openai.com"
        },
        "groq": {
            "type": ProviderType.API_KEY,
            "name": "Groq",
            "models": ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"],
            "api_url": "https://api.groq.com/openai/v1"
        },
        "deepseek": {
            "type": ProviderType.API_KEY,
            "name": "DeepSeek",
            "models": ["deepseek-chat", "deepseek-coder"],
            "api_url": "https://api.deepseek.com"
        },
        "mistral": {
            "type": ProviderType.API_KEY,
            "name": "Mistral",
            "models": ["mistral-large", "mistral-medium", "mistral-small"],
            "api_url": "https://api.mistral.ai"
        },
        "ollama": {
            "type": ProviderType.LOCAL,
            "name": "Ollama (Local)",
            "models": ["llama3", "llama3:7b", "llama3:8b", "mistral", "codellama"],
            "api_url": "http://localhost:11434"
        }
    }
    
    @classmethod
    def get_provider(cls, name: str) -> Optional[Dict[str, Any]]:
        """Get provider configuration"""
        return cls.PROVIDERS.get(name)
    
    @classmethod
    def get_provider_names(cls) -> list:
        """Get list of available provider names"""
        return list(cls.PROVIDERS.keys())
    
    @classmethod
    def get_models(cls, provider: str) -> list:
        """Get models for a provider"""
        if provider not in cls.PROVIDERS:
            return []
        return cls.PROVIDERS[provider].get("models", [])
    
    @classmethod
    def is_oauth(cls, provider: str) -> bool:
        """Check if provider uses OAuth"""
        if provider not in cls.PROVIDERS:
            return False
        return cls.PROVIDERS[provider]["type"] == ProviderType.OAUTH
    
    @classmethod
    def is_local(cls, provider: str) -> bool:
        """Check if provider is local"""
        if provider not in cls.PROVIDERS:
            return False
        return cls.PROVIDERS[provider]["type"] == ProviderType.LOCAL
