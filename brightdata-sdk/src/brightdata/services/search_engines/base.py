"""Base class for search engines."""

from abc import ABC
from typing import Optional, Dict, Any
from ...core.engine import AsyncEngine


class BaseSearchEngine(ABC):
    """Base class for all search engine implementations."""
    
    def __init__(self, engine: AsyncEngine):
        """
        Initialize base search engine.
        
        Args:
            engine: AsyncEngine instance.
        """
        self._engine = engine

