"""LinkedIn-specific scraper."""

from typing import Optional, Union, List
from ...models import ScrapeResult
from .base import BaseScraper


class LinkedInScraper(BaseScraper):
    """
    LinkedIn-specific scraping methods.
    
    Example:
        >>> client = BrightDataClient()
        >>> profile = await client.scrape.linkedin.profile(url="https://linkedin.com/in/...")
        >>> company = await client.scrape.linkedin.company(url="https://linkedin.com/company/...")
    """
    
    async def profile(
        self,
        url: Union[str, List[str]],
        zone: Optional[str] = None,
        country: str = "",
        timeout: Optional[int] = None,
    ) -> Union[ScrapeResult, List[ScrapeResult]]:
        """
        Scrape LinkedIn profile pages.
        
        Args:
            url: Single LinkedIn profile URL or list of URLs.
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
    
    async def company(
        self,
        url: Union[str, List[str]],
        zone: Optional[str] = None,
        country: str = "",
        timeout: Optional[int] = None,
    ) -> Union[ScrapeResult, List[ScrapeResult]]:
        """
        Scrape LinkedIn company pages.
        
        Args:
            url: Single LinkedIn company URL or list of URLs.
            zone: Bright Data zone identifier.
            country: Two-letter ISO country code for proxy location.
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
    
    async def job(
        self,
        url: Union[str, List[str]],
        zone: Optional[str] = None,
        country: str = "",
        timeout: Optional[int] = None,
    ) -> Union[ScrapeResult, List[ScrapeResult]]:
        """
        Scrape LinkedIn job postings.
        
        Args:
            url: Single LinkedIn job URL or list of URLs.
            zone: Bright Data zone identifier.
            country: Two-letter ISO country code for proxy location.
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

