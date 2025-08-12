from datetime import timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Union

from .common.api_version import MediaWikiVersion, MEDIAWIKI_1_34
from .language import Language


class Config(object):
    """
    Contains global configuration
    """

    DEFAULT_TIMEOUT = 3.0
    DEFAULT_USER_AGENT = "mediawikiapi (https://github.com/lehinevych/MediaWikiAPI/)"
    DONATE_URL = (
        "https://donate.wikimedia.org/w/index.php?title=Special:FundraiserLandingPage"
    )
    API_URL = "https://{}.wikipedia.org/w/api.php"

    # Default retry settings
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_BACKOFF_FACTOR = 0.5  # seconds
    DEFAULT_RETRY_BACKOFF_MAX = 60  # seconds
    DEFAULT_RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
    
    # Default concurrency settings
    DEFAULT_CONNECTION_POOL_SIZE = 100
    DEFAULT_CONNECTIONS_PER_HOST = 10
    DEFAULT_MAX_CONCURRENT_REQUESTS = 10
    
    class RetryStrategy(Enum):
        """Enum defining retry strategies"""
        NONE = auto()           # No retries
        DEFAULT = auto()        # Default strategy using configured values
        AGGRESSIVE = auto()     # More aggressive strategy for important requests
        
    def __init__(
        self,
        language: Optional[str] = None,
        user_agent: Optional[str] = None,
        timeout: Optional[float] = None,
        rate_limit: Optional[Union[int, timedelta]] = None,
        mediawiki_url: Optional[str] = None,
        cache_ttl: Optional[float] = None,
        cache_max_size: Optional[int] = None,
        max_retries: Optional[int] = None,
        retry_backoff_factor: Optional[float] = None,
        retry_backoff_max: Optional[float] = None,
        retry_status_codes: Optional[Set[int]] = None,
        retry_strategy: RetryStrategy = RetryStrategy.DEFAULT,
        min_api_version: Optional[MediaWikiVersion] = None,
        feature_compatibility_mode: bool = True,
        connection_pool_size: Optional[int] = None,
        connections_per_host: Optional[int] = None,
        max_concurrent_requests: Optional[int] = None,
    ):
        if language is not None:
            self.__lang = Language(language)
        else:
            self.__lang = Language()
        if isinstance(rate_limit, int):
            rate_limit = timedelta(milliseconds=rate_limit)
        self.__rate_limit: Optional[timedelta] = rate_limit
        self.timeout: float = timeout or self.DEFAULT_TIMEOUT
        self.user_agent: str = user_agent or self.DEFAULT_USER_AGENT
        self.mediawiki_url: str = mediawiki_url or self.API_URL
        self.cache_ttl: Optional[float] = cache_ttl
        self.cache_max_size: Optional[int] = cache_max_size
        
        # API version handling
        self.min_api_version: MediaWikiVersion = min_api_version or MEDIAWIKI_1_34
        self.feature_compatibility_mode: bool = feature_compatibility_mode
        self.detected_api_versions: Dict[str, MediaWikiVersion] = {}
        
        # Initialize concurrency control settings
        self.connection_pool_size: int = connection_pool_size or self.DEFAULT_CONNECTION_POOL_SIZE
        self.connections_per_host: int = connections_per_host or self.DEFAULT_CONNECTIONS_PER_HOST
        self.max_concurrent_requests: int = max_concurrent_requests or self.DEFAULT_MAX_CONCURRENT_REQUESTS
        
        # Validate concurrency settings
        if self.connection_pool_size < 1:
            raise ValueError("Connection pool size must be at least 1")
        if self.connections_per_host < 1:
            raise ValueError("Connections per host must be at least 1")
        if self.max_concurrent_requests < 1:
            raise ValueError("Maximum concurrent requests must be at least 1")
        
        # Initialize retry settings
        self.retry_strategy = retry_strategy
        
        # Use provided values or defaults based on strategy
        if self.retry_strategy == self.RetryStrategy.NONE:
            self.max_retries = 0
            self.retry_backoff_factor = 0
            self.retry_backoff_max = 0
            self.retry_status_codes = set()
        elif self.retry_strategy == self.RetryStrategy.AGGRESSIVE:
            self.max_retries = max_retries or 5  # More retries
            self.retry_backoff_factor = retry_backoff_factor or 0.3  # Shorter initial backoff
            self.retry_backoff_max = retry_backoff_max or 120  # Longer max backoff
            self.retry_status_codes = retry_status_codes or {408, 429, 500, 502, 503, 504, 520, 521, 522, 524}
        else:  # DEFAULT strategy
            self.max_retries = max_retries or self.DEFAULT_MAX_RETRIES
            self.retry_backoff_factor = retry_backoff_factor or self.DEFAULT_RETRY_BACKOFF_FACTOR
            self.retry_backoff_max = retry_backoff_max or self.DEFAULT_RETRY_BACKOFF_MAX
            self.retry_status_codes = retry_status_codes or self.DEFAULT_RETRY_STATUS_CODES

    @classmethod
    def donate_url(cls) -> str:
        """Return media wiki donate url"""
        return cls.DONATE_URL

    @property
    def language(self) -> str:
        """Return current global language"""
        return self.__lang.language

    @language.setter
    def language(self, language: Union[str, Language]) -> None:
        """Set a new language
        Arguments:
        * language - (string or Language instance) specifying the language
        """
        if isinstance(language, Language):
            self.__lang = language
        else:
            self.__lang.language = language

    def get_api_url(self, language: Optional[Union[str, Language]] = None) -> str:
        """Return api for specified language
        Arguments:
        * language - (string or Language instance) specifying the language
        """
        if language is not None:
            if isinstance(language, Language):
                return self.mediawiki_url.format(language.language)
            else:
                # does the language verification
                lang = Language(language)
                return self.mediawiki_url.format(lang.language)
        return self.mediawiki_url.format(self.__lang.language)

    @property
    def rate_limit(self) -> Optional[timedelta]:
        return self.__rate_limit

    @rate_limit.setter
    def rate_limit(self, rate_limit: Optional[Union[int, timedelta]] = None) -> None:
        """
        Enable or disable rate limiting on requests to the Mediawiki servers.
        If rate limiting is not enabled, under some circumstances (depending on
        load on Wikipedia, the number of requests you and other `wikipedia` users
        are making, and other factors), Wikipedia may return an HTTP timeout error.

        Enabling rate limiting generally prevents that issue, but please note that
        HTTPTimeoutError still might be raised.

        Arguments:
        * min_wait - (integer or timedelta) describes the minimum time to wait in
               miliseconds before requests. Example timedelta(milliseconds=50).
               If None, rate_limit won't be used.

        """
        if rate_limit is None:
            self.__rate_limit = None
        elif isinstance(rate_limit, timedelta):
            self.__rate_limit = rate_limit
        else:
            self.__rate_limit = timedelta(milliseconds=rate_limit)
            
    def should_retry(self, attempt: int, status_code: Optional[int] = None) -> bool:
        """
        Determine if a request should be retried based on the current retry settings.
        
        Args:
            attempt: Current attempt number (0-based)
            status_code: HTTP status code of the failed request, if applicable
            
        Returns:
            True if request should be retried, False otherwise
        """
        # Check if we've reached max retries
        if attempt >= self.max_retries:
            return False
            
        # If no status code provided, retry based on attempt count only
        if status_code is None:
            return True
            
        # Otherwise, check if status code is in retry_status_codes
        return status_code in self.retry_status_codes
        
    def get_retry_backoff(self, attempt: int) -> float:
        """
        Calculate backoff time for a retry attempt using exponential backoff.
        
        Args:
            attempt: Current attempt number (0-based)
            
        Returns:
            Backoff time in seconds
        """
        # Calculate exponential backoff with jitter
        backoff = min(
            self.retry_backoff_max,
            self.retry_backoff_factor * (2 ** attempt)
        )
        return backoff
        
    def set_api_version(self, api_url: str, version: MediaWikiVersion) -> None:
        """
        Set the detected MediaWiki API version for a specific API URL.
        
        Args:
            api_url: The API URL
            version: The detected MediaWiki version
        """
        self.detected_api_versions[api_url] = version
        
    def get_api_version(self, api_url: str) -> Optional[MediaWikiVersion]:
        """
        Get the detected MediaWiki API version for a specific API URL.
        
        Args:
            api_url: The API URL
            
        Returns:
            MediaWikiVersion if detected, None otherwise
        """
        return self.detected_api_versions.get(api_url)
        
    def is_feature_available(self, feature: str, api_url: str) -> bool:
        """
        Check if a feature is available for the given API URL.
        
        Args:
            feature: Feature name
            api_url: The API URL
            
        Returns:
            True if the feature is available or compatibility mode is enabled,
            False otherwise
        """
        from .common.api_version import is_feature_available
        
        # If feature compatibility mode is enabled, assume all features are available
        if self.feature_compatibility_mode:
            return True
            
        # If we have detected the API version for this URL, check if the feature is available
        version = self.get_api_version(api_url)
        if version:
            return is_feature_available(feature, version)
            
        # If we haven't detected the API version yet, use the minimum required version
        return is_feature_available(feature, self.min_api_version)
