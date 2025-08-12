from decimal import Decimal
from functools import partial
from typing import Any, Dict, List, Optional, Tuple, Union

from ..base.base_mediawikiapi import BaseMediaWikiAPI
from ..config import Config
from ..exceptions import HTTPTimeoutError, MediaWikiAPIException, PageError
from .requestsession import RequestSession
from .util import memorized
from .wikipediapage import WikipediaPage


class MediaWikiAPI(BaseMediaWikiAPI[WikipediaPage, Dict[str, Any]]):
    """
    Synchronous implementation of the MediaWiki API.
    
    This class extends BaseMediaWikiAPI with synchronous HTTP requests and 
    provides access to Wikipedia content using standard Python data structures.
    
    The MediaWikiAPI class can be used as a context manager to ensure
    proper resource cleanup:
    
    Example:
        ```python
        with MediaWikiAPI() as api:
            page = api.page("Python (programming language)")
        # Session is automatically closed after the with block
        ```
    """
    
    def __init__(self, config: Optional[Config] = None) -> None:
        """
        Initialize the MediaWiki API with optional configuration.
        
        Args:
            config: Optional configuration object. If not provided, default config is used.
        """
        super().__init__(config)
        self.session = RequestSession()
        
    def __enter__(self) -> 'MediaWikiAPI':
        """
        Enter the context manager.
        
        Returns:
            The MediaWikiAPI instance
        """
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the context manager and clean up resources.
        
        Args:
            exc_type: The exception type, if an exception was raised
            exc_val: The exception value, if an exception was raised
            exc_tb: The exception traceback, if an exception was raised
        """
        self.close()
        
    def close(self) -> None:
        """
        Close the session and release resources.
        
        This method should be called when you're done using the MediaWikiAPI
        instance to ensure proper resource cleanup.
        """
        self.session.close()
    
    def get_cache_statistics(self) -> Dict[str, int]:
        """
        Get cache statistics for all cached methods.
        
        Returns:
            Dictionary mapping method names to number of cache entries
        """
        from .cache_util import get_cache_statistics
        return get_cache_statistics(self)
    
    def invalidate_all_caches(self) -> Dict[str, int]:
        """
        Invalidate all caches for all methods.
        
        Returns:
            Dictionary mapping method names to number of entries invalidated
        """
        from .cache_util import invalidate_all_caches
        return invalidate_all_caches(self)
        
    def new_session(self) -> None:
        """
        Create a new request session, closing the existing one if necessary.
        
        This method can be used to refresh the connection or recover from connection issues.
        """
        self.session.close()
        self.session = RequestSession()
    
    @memorized
    def search(
        self,
        query: str,
        results: int = 10,
        suggestion: bool = False,
    ) -> Union[List[str], Tuple[List[str], Optional[str]]]:
        """
        Do a Wikipedia search for `query`.
        
        Keyword arguments:
        
        * results - the maxmimum number of results returned
        * suggestion - if True, return results and suggestion (if any) in a tuple
        """
        # Use helper method from the base class
        search_params = self._prepare_search_params(query, results, suggestion)
        
        # Make the request
        raw_results = self.session.request(search_params, self.config)
        
        # Handle errors
        self._handle_error_response(raw_results, query)
        
        # Process results
        return self._process_search_results(raw_results, suggestion)  # type: ignore
    
    @memorized
    def geosearch(
        self,
        latitude: Decimal,
        longitude: Decimal,
        title: Optional[str] = None,
        results: int = 10,
        radius: int = 1000,
    ) -> List[str]:
        """
        Do a wikipedia geo search for `latitude` and `longitude`
        using HTTP API described in http://www.mediawiki.org/wiki/Extension:GeoData
        
        Arguments:
        
        * latitude (float or decimal.Decimal)
        * longitude (float or decimal.Decimal)
        
        Keyword arguments:
        
        * title - The title of an article to search for
        * results - the maximum number of results returned
        * radius - Search radius in meters. The value must be between 10 and 10000
        """
        # Use helper method from the base class
        search_params = self._prepare_geosearch_params(latitude, longitude, title, results, radius)
        
        # Make the request
        raw_results = self.session.request(search_params, self.config)
        
        # Handle errors
        self._handle_error_response(raw_results, f"{latitude}|{longitude}")
        
        # Process results
        return self._process_geosearch_results(raw_results)
    
    @memorized
    def suggest(self, query: str) -> Optional[str]:
        """
        Get a Wikipedia search suggestion for `query`.
        Returns a string or None if no suggestion was found.
        """
        # Use helper method from the base class
        search_params = self._prepare_suggest_params(query)
        
        # Make the request
        raw_result = self.session.request(search_params, self.config)
        
        # Process results
        if raw_result["query"].get("searchinfo"):
            return raw_result["query"]["searchinfo"]["suggestion"]
        return None
    
    def random(self, pages: int = 1) -> Union[str, List[str]]:
        """
        Get a list of random Wikipedia article titles.
        
        .. note:: Random only gets articles from namespace 0, meaning no Category, User talk, or other meta-Wikipedia pages.
        
        Keyword arguments:
        
        * pages - the number of random pages returned (max of 10)
        """
        # Use helper method from the base class
        query_params = self._prepare_random_params(pages)
        
        # Make the request
        request = self.session.request(query_params, self.config)
        
        # Process results
        return self._process_random_results(request, pages)
    
    @memorized
    def summary(
        self,
        title: str,
        sentences: Optional[int] = 0,
        chars: Optional[int] = 0,
        auto_suggest: bool = False,
        redirect: bool = True,
    ) -> str:
        """
        Plain text summary of the page.
        
        .. note:: This is a convenience wrapper - auto_suggest and redirect are enabled by default
        
        Keyword arguments:
        * sentences - if set, return the first `sentences` sentences (can be no greater than 10).
        * chars - if set, return only the first `chars` characters (actual text returned may be slightly longer).
        * auto_suggest - let Wikipedia find a valid page title for the query
        * redirect - allow redirection without raising RedirectError
        """
        # Use auto_suggest and redirect to get the correct article
        page_info = self.page(title, auto_suggest=auto_suggest, redirect=redirect)
        title = page_info.title
        pageid = page_info.pageid
        
        # Use helper method from the base class
        query_params = self._prepare_summary_params(title, sentences, chars)
        
        # Make the request
        request = self.session.request(query_params, self.config)
        
        # Process results
        summary = request["query"]["pages"][pageid]["extract"]
        return summary
    
    def page(
        self,
        title: Optional[str] = None,
        pageid: Optional[int] = None,
        auto_suggest: bool = False,
        redirect: bool = True,
        preload: bool = False,
    ) -> WikipediaPage:
        """
        Get a WikipediaPage object for the page with title `title` or the pageid
        `pageid` (mutually exclusive).
        
        Keyword arguments:
        
        * title - the title of the page to load
        * pageid - the numeric pageid of the page to load
        * auto_suggest - let Wikipedia find a valid page title for the query
        * redirect - allow redirection without raising RedirectError
        * preload - load content, summary, images, references, and links during initialization
        
        The method first tries to load the page using the exact title provided.
        If that fails and auto_suggest is True, it will attempt to find a matching page
        using the search API.
        """
        request_f = partial(self.session.request, config=self.config)
        
        if title is not None:
            # Always try exact title match first
            try:
                return WikipediaPage(
                    request=request_f, title=title, redirect=redirect, preload=preload,
                    mediawiki_api=self
                )
            except PageError:
                if not auto_suggest:
                    raise
            
            # If exact match fails and auto_suggest is True, try search
            results, suggestion = self.search(title, results=1, suggestion=True)
            if suggestion:
                return WikipediaPage(
                    request=request_f,
                    title=suggestion,
                    pageid=pageid,
                    redirect=redirect,
                    preload=preload,
                    mediawiki_api=self
                )
            try:
                title = results[0]
            except IndexError:
                # if there are no suggestion or search results, the page doesn't exist
                raise PageError(title=title)
            return WikipediaPage(
                request=request_f, title=title, redirect=redirect, preload=preload,
                mediawiki_api=self
            )
        elif pageid is not None:
            return WikipediaPage(request=request_f, pageid=pageid, preload=preload, mediawiki_api=self)
        else:
            raise ValueError("Either a title or a pageid must be specified")
    
    def languages(self) -> Dict[str, str]:
        """
        List all the currently supported language prefixes (usually ISO language code).
        
        Can be inputted to WikipediaPage.conf to change the Mediawiki that `wikipedia` requests
        results from.
        
        Returns: dict of <prefix>: <local_lang_name> pairs. To get just a list of prefixes,
        use `wikipedia.languages().keys()`.
        """
        response = self.session.request(
            {"meta": "siteinfo", "siprop": "languages"}, self.config
        )
        languages = response["query"]["languages"]
        return {lang["code"]: lang["*"] for lang in languages}
    
    def category_members(
        self,
        title: Optional[str] = None,
        pageid: Optional[int] = None,
        cmlimit: int = 10,
        cmtype: str = "page",
    ) -> List[str]:
        """
        Get list of page titles belonging to a category.
        
        Keyword arguments:
        
        * title - category title. Cannot be used together with "pageid"
        * pageid - page id of category page. Cannot be used together with "title"
        * cmlimit - the maximum number of titles to return
        * cmtype - which type of page to include. ("page", "subcat", or "file")
        """
        # Use helper method from the base class
        query_params = self._prepare_category_members_params(title, pageid, cmlimit, cmtype)
        
        # Make the request
        response = self.session.request(query_params, self.config)
        
        # Process results
        return self._process_category_members_results(response)
    
    def custom_query(self, query_params: Dict[str, Union[str, int, bool, List[str]]]) -> Dict[str, Any]:
        """
        Make a custom query to the Wikipedia API with the given parameters.
        
        This method is useful for complex queries that aren't covered by the standard methods,
        especially those that may return large amounts of data requiring continuation tokens.
        
        Arguments:
        * query_params - A dictionary of query parameters to pass to the API
        
        Returns:
        * The raw API response as a dictionary
        """
        return self.session.request(query_params, self.config)