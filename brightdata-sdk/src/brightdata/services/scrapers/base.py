"""Base class for platform-specific scrapers."""

from abc import ABC
from typing import Optional
from ...core.engine import AsyncEngine
from ...api.web_unlocker import WebUnlockerService


class BaseScraper(ABC):
    """Base class for all platform-specific scrapers."""
    
    def __init__(self, engine: AsyncEngine, default_zone: str = "sdk_unlocker"):
        """
        Initialize base scraper.
        
        Args:
            engine: AsyncEngine instance.
            default_zone: Default zone name for web unlocker.
        """
        self._engine = engine
        self._default_zone = default_zone
        self._web_unlocker: Optional[WebUnlockerService] = None
    
    @property
    def _unlocker(self) -> WebUnlockerService:
        """Get or create WebUnlockerService instance."""
        if self._web_unlocker is None:
            self._web_unlocker = WebUnlockerService(self._engine)
        return self._web_unlocker

