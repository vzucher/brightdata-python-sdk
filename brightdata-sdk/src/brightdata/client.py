"""Main Bright Data SDK client - Enterprise-grade entry point."""

import os
from typing import Optional, Dict, Any, List
from pathlib import Path

from .core.engine import AsyncEngine
from .exceptions import ValidationError, AuthenticationError, APIError
from .services import ScrapeService, SearchService, CrawlerService


class BrightDataClient:
    """
    Main entry point for Bright Data SDK.
    
    Provides unified access to all Bright Data services with robust authentication
    and configuration management. Designed for enterprise use with fail-fast
    authentication and clear error messages.
    
    Example:
        >>> # Auto-load from environment
        >>> client = BrightDataClient()
        >>> 
        >>> # Explicit token
        >>> client = BrightDataClient(token="your_token")
        >>> 
        >>> # Service-specific tokens
        >>> client = BrightDataClient(
        ...     token="general_token",
        ...     scrape_token="scrape_specific_token",
        ...     search_token="search_specific_token"
        ... )
        >>> 
        >>> # Service access
        >>> result = await client.scrape.amazon.products(url="...")
        >>> results = await client.search.linkedin.jobs(query="...")
        >>> crawl_result = await client.crawler.discover(domain="...")
        >>> 
        >>> # Connection testing
        >>> is_valid = await client.test_connection()
        >>> account_info = await client.get_account_info()
    """
    
    ENV_TOKEN_NAMES = [
        "BRIGHTDATA_API_TOKEN",
        "BRIGHTDATA_TOKEN",
        "BRIGHT_DATA_API_TOKEN",
        "BRIGHT_DATA_TOKEN",
    ]
    
    DEFAULT_TIMEOUT = 30
    DEFAULT_ZONE = "sdk_unlocker"
    
    def __init__(
        self,
        token: Optional[str] = None,
        scrape_token: Optional[str] = None,
        search_token: Optional[str] = None,
        crawler_token: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        default_zone: str = DEFAULT_ZONE,
    ):
        """
        Initialize Bright Data client.
        
        Token resolution order:
        1. Explicit token parameter (general token)
        2. Service-specific tokens (scrape_token, search_token, crawler_token)
        3. Environment variables (BRIGHTDATA_API_TOKEN, etc.)
        4. .env file in current directory
        5. .env file in project root
        
        Args:
            token: General API token (used as fallback for all services).
            scrape_token: Token specific for scraping services (optional).
            search_token: Token specific for search services (optional).
            crawler_token: Token specific for crawler services (optional).
            timeout: Default timeout in seconds for API requests.
            default_zone: Default zone name for web unlocker operations.
        
        Raises:
            ValidationError: If token is not provided and cannot be loaded from environment.
        """
        self._token = self._resolve_token(token)
        self._scrape_token = scrape_token.strip() if scrape_token and isinstance(scrape_token, str) else None
        self._search_token = search_token.strip() if search_token and isinstance(search_token, str) else None
        self._crawler_token = crawler_token.strip() if crawler_token and isinstance(crawler_token, str) else None
        self._timeout = timeout
        self._default_zone = default_zone
        self._engine: Optional[AsyncEngine] = None
        self._scrape: Optional[ScrapeService] = None
        self._search: Optional[SearchService] = None
        self._crawler: Optional[CrawlerService] = None
    
    def _resolve_token(self, explicit_token: Optional[str]) -> str:
        """
        Resolve API token from multiple sources.
        
        Resolution order:
        1. Explicit token parameter
        2. Environment variables
        3. .env file
        
        Args:
            explicit_token: Token provided explicitly.
        
        Returns:
            Resolved API token.
        
        Raises:
            ValidationError: If token cannot be resolved.
        """
        if explicit_token:
            if not isinstance(explicit_token, str) or not explicit_token.strip():
                raise ValidationError("Token must be a non-empty string")
            return explicit_token.strip()
        
        for env_name in self.ENV_TOKEN_NAMES:
            token = os.getenv(env_name)
            if token and token.strip():
                return token.strip()
        
        token = self._load_token_from_env_file()
        if token:
            return token
        raise ValidationError(
            f"API token required. Provide token parameter or set one of these "
            f"environment variables: {', '.join(self.ENV_TOKEN_NAMES)}"
        )
    
    def _load_token_from_env_file(self) -> Optional[str]:
        """Load token from .env file if present."""
        try:
            from dotenv import load_dotenv
            
            env_path = Path(".env")
            if env_path.exists():
                load_dotenv(env_path)
                for env_name in self.ENV_TOKEN_NAMES:
                    token = os.getenv(env_name)
                    if token and token.strip():
                        return token.strip()
            
            for i in range(3):
                env_path = Path("../" * i + ".env")
                if env_path.exists():
                    load_dotenv(env_path)
                    for env_name in self.ENV_TOKEN_NAMES:
                        token = os.getenv(env_name)
                        if token and token.strip():
                            return token.strip()
        except ImportError:
            pass
        except Exception:
            pass
        
        return None
    
    @property
    def token(self) -> str:
        """Get the API token (masked for security)."""
        if len(self._token) > 8:
            return f"{self._token[:4]}...{self._token[-4:]}"
        return "***"
    
    @property
    def timeout(self) -> int:
        """Get default timeout in seconds."""
        return self._timeout
    
    @property
    def default_zone(self) -> str:
        """Get default zone name."""
        return self._default_zone
    
    def _get_engine(self, service_token: Optional[str] = None) -> AsyncEngine:
        """Get or create AsyncEngine instance with optional service-specific token."""
        if service_token:
            return AsyncEngine(service_token, timeout=self._timeout)
        if self._engine is None:
            self._engine = AsyncEngine(self._token, timeout=self._timeout)
        return self._engine
    
    @property
    def scrape(self) -> ScrapeService:
        """Access scraping services (Amazon, LinkedIn, ChatGPT, etc.)."""
        if self._scrape is None:
            engine = self._get_engine(self._scrape_token)
            self._scrape = ScrapeService(engine, self._default_zone)
        return self._scrape
    
    @property
    def search(self) -> SearchService:
        """Access search services (Google, Bing, Yandex, LinkedIn, etc.)."""
        if self._search is None:
            engine = self._get_engine(self._search_token)
            self._search = SearchService(engine)
        return self._search
    
    @property
    def crawler(self) -> CrawlerService:
        """Access web crawling services."""
        if self._crawler is None:
            engine = self._get_engine(self._crawler_token)
            self._crawler = CrawlerService(engine)
        return self._crawler
    
    async def test_connection(self) -> bool:
        """
        Test API connection and authentication.
        
        Makes a lightweight API call to verify credentials are valid.
        
        Returns:
            True if connection is valid, False otherwise.
        
        Example:
            >>> client = BrightDataClient()
            >>> async with client:
            ...     is_valid = await client.test_connection()
            ...     if not is_valid:
            ...         print("Invalid credentials")
        """
        try:
            zones = await self.list_zones()
            return True
        except (AuthenticationError, APIError):
            return False
        except Exception:
            return False
    
    async def list_zones(self) -> List[Dict[str, Any]]:
        """
        List all active zones in your Bright Data account.
        
        Returns:
            List of zone dictionaries with their configurations.
        
        Raises:
            AuthenticationError: If authentication fails.
            APIError: If API request fails.
        
        Example:
            >>> client = BrightDataClient()
            >>> async with client:
            ...     zones = await client.list_zones()
            ...     print(f"Found {len(zones)} zones")
        """
        engine = self._get_engine()
        response = await engine.get("/zone/get_active_zones")
        
        async with response:
            if response.status != 200:
                error_text = await response.text()
                raise APIError(
                    f"Failed to list zones: {response.status}",
                    status_code=response.status,
                    response_text=error_text,
                )
            
            try:
                data = await response.json()
                return data if isinstance(data, list) else []
            except Exception as e:
                raise APIError(f"Failed to parse zones response: {str(e)}")
    
    async def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information using zones list as a proxy.
        
        Since Bright Data API doesn't have a dedicated /account endpoint,
        this method uses the zones list to verify account access and returns
        zone information as account metadata.
        
        Returns:
            Dictionary with account information derived from zones:
            - zones: List of active zones
            - zone_count: Number of active zones
            - authenticated: True if credentials are valid
        
        Raises:
            AuthenticationError: If authentication fails.
            APIError: If API request fails.
        
        Example:
            >>> client = BrightDataClient()
            >>> info = await client.get_account_info()
            >>> print(f"Zones: {info['zone_count']}")
        """
        try:
            zones = await self.list_zones()
            return {
                "zones": zones,
                "zone_count": len(zones) if isinstance(zones, list) else 0,
                "authenticated": True,
            }
        except (AuthenticationError, APIError) as e:
            raise
    
    async def __aenter__(self):
        """Async context manager entry."""
        if self._engine is None:
            self._engine = AsyncEngine(self._token, timeout=self._timeout)
        await self._engine.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._engine:
            await self._engine.__aexit__(exc_type, exc_val, exc_tb)
    
    def __repr__(self) -> str:
        """String representation."""
        return f"<BrightDataClient token={self.token} timeout={self._timeout}s>"


BrightData = BrightDataClient
