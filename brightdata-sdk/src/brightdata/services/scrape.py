"""Scraping service with platform-specific scrapers."""

from typing import Optional, Union, List, Any, Dict
from ..core.engine import AsyncEngine
from ..models import ScrapeResult
from ..api.web_unlocker import WebUnlockerService
from .scrapers.amazon import AmazonScraper
from .scrapers.linkedin import LinkedInScraper
from .scrapers.chatgpt import ChatGPTScraper


class ScrapeService:
    """
    Main scraping service providing access to platform-specific scrapers.
    
    Example:
        >>> client = BrightDataClient()
        >>> # Amazon scraping
        >>> result = await client.scrape.amazon.products(url="...")
        >>> # LinkedIn scraping
        >>> profile = await client.scrape.linkedin.profile(url="...")
        >>> # Generic scraping
        >>> result = await client.scrape.url("https://example.com")
    """
    
    def __init__(self, engine: AsyncEngine, default_zone: str = "sdk_unlocker"):
        """
        Initialize scraping service.
        
        Args:
            engine: AsyncEngine instance.
            default_zone: Default zone name for web unlocker.
        """
        self._engine = engine
        self._default_zone = default_zone
        self._web_unlocker: Optional[WebUnlockerService] = None
        self._amazon: Optional[AmazonScraper] = None
        self._linkedin: Optional[LinkedInScraper] = None
        self._chatgpt: Optional[ChatGPTScraper] = None
    
    @property
    def amazon(self) -> "AmazonScraper":
        """Access Amazon-specific scraping methods."""
        if self._amazon is None:
            self._amazon = AmazonScraper(self._engine, self._default_zone)
        return self._amazon
    
    @property
    def linkedin(self) -> "LinkedInScraper":
        """Access LinkedIn-specific scraping methods."""
        if self._linkedin is None:
            self._linkedin = LinkedInScraper(self._engine, self._default_zone)
        return self._linkedin
    
    @property
    def chatgpt(self) -> "ChatGPTScraper":
        """Access ChatGPT-specific scraping methods."""
        if self._chatgpt is None:
            self._chatgpt = ChatGPTScraper(self._engine, self._default_zone)
        return self._chatgpt
    
    async def url(
        self,
        url: Union[str, List[str]],
        zone: Optional[str] = None,
        country: str = "",
        response_format: str = "raw",
        method: str = "GET",
        timeout: Optional[int] = None,
    ) -> Union[ScrapeResult, List[ScrapeResult]]:
        """
        Scrape URL(s) using Web Unlocker API (generic scraping).
        
        This is the fastest, most cost-effective option for basic HTML extraction
        without JavaScript rendering.
        
        Args:
            url: Single URL string or list of URLs to scrape.
            zone: Bright Data zone identifier (defaults to service default).
            country: Two-letter ISO country code for proxy location (optional).
            response_format: Response format - "json" for structured data, "raw" for HTML string.
            method: HTTP method for the request (default: "GET").
            timeout: Request timeout in seconds (uses engine default if not provided).
        
        Returns:
            ScrapeResult for single URL, or List[ScrapeResult] for multiple URLs.
        
        Example:
            >>> client = BrightDataClient()
            >>> result = await client.scrape.url("https://example.com")
            >>> print(result.data)
        """
        if self._web_unlocker is None:
            self._web_unlocker = WebUnlockerService(self._engine)
        
        zone = zone or self._default_zone
        return await self._web_unlocker.scrape_async(
            url=url,
            zone=zone,
            country=country,
            response_format=response_format,
            method=method,
            timeout=timeout,
        )

