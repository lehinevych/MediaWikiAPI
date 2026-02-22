from datetime import timedelta
from typing import Union, Optional, Dict
from .language import Language


class Config(object):
    """
    Contains global configuration for MediaWiki API requests.
    """

    DEFAULT_TIMEOUT = 3.0
    DEFAULT_USER_AGENT = "mediawikiapi (https://github.com/lehinevych/MediaWikiAPI/)"
    DONATE_URL = (
        "https://donate.wikimedia.org/w/index.php?title=Special:FundraiserLandingPage"
    )
    API_URL = "https://{}.wikipedia.org/w/api.php"

    def __init__(
        self,
        language: Optional[str] = None,
        user_agent: Optional[str] = None,
        timeout: Optional[float] = None,
        rate_limit: Optional[Union[int, timedelta]] = None,
        mediawiki_url: Optional[str] = None,
        access_token: Optional[str] = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize MediaWiki API configuration.

        Args:
            language: Language code for Wikipedia (e.g., 'en', 'fr'). Defaults to 'en'.
            user_agent: Custom User-Agent string for requests. Defaults to library identifier.
            timeout: Request timeout in seconds. Defaults to 3.0.
            rate_limit: Minimum time between requests (int as milliseconds or timedelta).
            mediawiki_url: Custom MediaWiki API URL. Defaults to Wikipedia URL pattern.
            access_token: Personal Access Token for Wikimedia API authentication.
                         See https://api.wikimedia.org/wiki/Authentication
            custom_headers: Additional HTTP headers to include in all requests.
                           Can override default headers including User-Agent.
        """
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
        self.access_token: Optional[str] = access_token
        self.custom_headers: Dict[str, str] = custom_headers or {}

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
        * min_wait - (integer or timedelta) describes the minimum time to wait in miliseconds before requests.
               Example timedelta(milliseconds=50). If None, rate_limit won't be used.

        """
        if rate_limit is None:
            self.__rate_limit = None
        elif isinstance(rate_limit, timedelta):
            self.__rate_limit = rate_limit
        else:
            self.__rate_limit = timedelta(milliseconds=rate_limit)

    def get_headers(self) -> Dict[str, str]:
        """
        Get HTTP headers for API requests including authentication.

        Returns:
            Dictionary of HTTP headers including User-Agent, Authorization (if access_token is set),
            and any custom headers.
        """
        headers = {"User-Agent": self.user_agent}

        # Add Personal Access Token authentication if provided
        # https://api.wikimedia.org/wiki/Authentication
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        # Merge custom headers (custom headers can override defaults)
        headers.update(self.custom_headers)

        return headers
