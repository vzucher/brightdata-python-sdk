"""Search service for SERP and platform-specific search."""

from typing import Optional, Dict, Any, List
from ..core.engine import AsyncEngine
from ..models import SearchResult
from .search_engines.google import GoogleSearch
from .search_engines.bing import BingSearch
from .search_engines.linkedin import LinkedInSearch


class SearchService:
    """
    Main search service providing access to search engines and platform-specific search.
    
    Example:
        >>> client = BrightDataClient()
        >>> # Google search
        >>> results = await client.search.google.query("python sdk")
        >>> # LinkedIn job search
        >>> jobs = await client.search.linkedin.jobs(query="software engineer")
    """
    
    def __init__(self, engine: AsyncEngine):
        """
        Initialize search service.
        
        Args:
            engine: AsyncEngine instance.
        """
        self._engine = engine
        self._google: Optional[GoogleSearch] = None
        self._bing: Optional[BingSearch] = None
        self._linkedin: Optional[LinkedInSearch] = None
    
    @property
    def google(self) -> "GoogleSearch":
        """Access Google search methods."""
        if self._google is None:
            self._google = GoogleSearch(self._engine)
        return self._google
    
    @property
    def bing(self) -> "BingSearch":
        """Access Bing search methods."""
        if self._bing is None:
            self._bing = BingSearch(self._engine)
        return self._bing
    
    @property
    def linkedin(self) -> "LinkedInSearch":
        """Access LinkedIn search methods."""
        if self._linkedin is None:
            self._linkedin = LinkedInSearch(self._engine)
        return self._linkedin

