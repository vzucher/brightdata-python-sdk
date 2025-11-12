"""ChatGPT-specific scraper."""

from typing import Optional, Union, List
from ...models import ScrapeResult
from .base import BaseScraper


class ChatGPTScraper(BaseScraper):
    """
    ChatGPT-specific scraping methods.
    
    Example:
        >>> client = BrightDataClient()
        >>> result = await client.scrape.chatgpt.conversation(url="https://chat.openai.com/...")
    """
    
    async def conversation(
        self,
        url: Union[str, List[str]],
        zone: Optional[str] = None,
        country: str = "",
        timeout: Optional[int] = None,
    ) -> Union[ScrapeResult, List[ScrapeResult]]:
        """
        Scrape ChatGPT conversation pages.
        
        Args:
            url: Single ChatGPT conversation URL or list of URLs.
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

