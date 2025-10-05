"""
Configuration management using environment variables
"""
import os
from typing import List


class Settings:
    """Application settings from environment variables"""

    # API Security
    API_KEY: str = os.getenv("API_KEY", "change-me-in-production")

    # Allowed domains for screenshots (security)
    ALLOWED_DOMAINS: List[str] = os.getenv("ALLOWED_DOMAINS", "easydis.io,www.easydis.io").split(
        ","
    )

    # Screenshot limits
    MAX_WAIT_TIME: int = int(os.getenv("MAX_WAIT_TIME", "60000"))  # 60 seconds max
    MAX_WIDTH: int = int(os.getenv("MAX_WIDTH", "3840"))  # 4K max
    MAX_HEIGHT: int = int(os.getenv("MAX_HEIGHT", "2160"))  # 4K max

    # Browser settings
    BROWSER_TYPE: str = os.getenv("BROWSER_TYPE", "chromium")  # chromium, firefox, webkit
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"

    # Service
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def is_domain_allowed(cls, url: str) -> bool:
        """Check if URL domain is in allowed list"""
        for domain in cls.ALLOWED_DOMAINS:
            if domain in url:
                return True
        return False


settings = Settings()
