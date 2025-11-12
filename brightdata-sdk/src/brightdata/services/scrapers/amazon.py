"""Amazon-specific scraper."""

from typing import Optional, Union, List
from ...models import ScrapeResult
from .base import BaseScraper


class AmazonScraper(BaseScraper):
    """
    Amazon-specific scraping methods.
    
    Example:
        >>> client = BrightDataClient()
        >>> result = await client.scrape.amazon.products(url="https://amazon.com/product/...")
        >>> print(result.data)
    """
    
    async def products(
        self,
        url: Union[str, List[str]],
        zone: Optional[str] = None,
        country: str = "",
        timeout: Optional[int] = None,
    ) -> Union[ScrapeResult, List[ScrapeResult]]:
        """
        Scrape Amazon product pages.
        
        Args:
            url: Single Amazon product URL or list of URLs.
            zone: Bright Data zone identifier (defaults to service default).
            country: Two-letter ISO country code for proxy location (optional).
            timeout: Request timeout in seconds.
        
        Returns:
            ScrapeResult for single URL, or List[ScrapeResult] for multiple URLs.
        """
        zone = zone or self._default_zone
        return await self._unlocker.scrape_async(
            url=url,
            zone=zone,
            country=country,
            response_format="json",
            method="GET",
            timeout=timeout,
        )
    
    async def search(
        self,
        query: str,
        zone: Optional[str] = None,
        country: str = "",
        timeout: Optional[int] = None,
    ) -> ScrapeResult:
        """
        Scrape Amazon search results.
        
        Args:
            query: Search query string.
            zone: Bright Data zone identifier.
            country: Two-letter ISO country code for proxy location.
            timeout: Request timeout in seconds.
        
        Returns:
            ScrapeResult with search results.
        """
        search_url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
        
        zone = zone or self._default_zone
        result = await self._unlocker.scrape_async(
            url=search_url,
            zone=zone,
            country=country,
            response_format="json",
            method="GET",
            timeout=timeout,
        )
        
        if isinstance(result, list):
            return result[0]
        return result

