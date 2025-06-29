"""Configuration settings for Options Flow Analyzer."""

import os
from typing import Optional
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    # Look for .env file in the project root
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, skip loading .env file
    pass


class Config:
    """Configuration class for API keys and settings."""

    # API Configuration
    TRADIER_API_KEY: Optional[str] = os.getenv("TRADIER_API_KEY")
    TRADIER_BASE_URL: str = "https://api.tradier.com/v1"

    # Polygon.io API Configuration
    POLYGON_API_KEY: Optional[str] = os.getenv("POLYGON_API_KEY")
    POLYGON_BASE_URL: str = "https://api.polygon.io"

    # Default settings
    DEFAULT_MIN_VOLUME: int = 10
    DEFAULT_EXPIRATION_DAYS: int = 30

    # Display settings
    MAX_STRIKES_DISPLAY: int = 20
    DECIMAL_PLACES: int = 2

    @classmethod
    def validate_api_keys(cls) -> bool:
        """Validate that required API keys are available."""
        # For MVP, we'll primarily use yfinance which doesn't require API key
        # Tradier API key is optional for enhanced features
        return True

    @classmethod
    def get_tradier_headers(cls) -> dict:
        """Get headers for Tradier API requests."""
        if cls.TRADIER_API_KEY:
            return {
                "Authorization": f"Bearer {cls.TRADIER_API_KEY}",
                "Accept": "application/json",
            }
        return {}
