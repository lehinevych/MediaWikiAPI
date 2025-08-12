"""
Base class for MediaWiki API implementations.

This module provides the abstract base class that both synchronous and
asynchronous MediaWiki API implementations extend.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union, TypeVar, Generic

from ..config import Config
from ..exceptions import HTTPTimeoutError, MediaWikiAPIException, PageError

# Type variables for generic specialization
T = TypeVar('T')  # For return type from request methods
P = TypeVar('P')  # For page type


class BaseMediaWikiAPI(ABC, Generic[P, T]):
    """
    Abstract base class for MediaWiki API implementations.
    
    This class contains shared functionality between synchronous and asynchronous
    implementations of the MediaWiki API. It defines the interface and common
    operations, leaving I/O-specific operations to derived classes.
    
    Type Parameters:
        P: Type of the page object returned (WikipediaPage or AsyncWikipediaPage)
        T: Return type of request methods (Dict[str, Any] or Coroutine)
    """
    
    def __init__(self, config: Optional[Config] = None) -> None:
        """
        Initialize the MediaWiki API with optional configuration.
        
        Args:
            config: Optional configuration object. If not provided, default config is used.
        """
        self.config = Config() if config is None else config
    
    # Cache invalidation methods (identical in both implementations)
    def invalidate_cache(self, method_name: str, *args: Any, **kwargs: Any) -> bool:
        """
        Invalidate cache for a specific method with specific arguments.
        
        Args:
            method_name: Name of the method whose cache to invalidate
            *args, **kwargs: Arguments for which to invalidate the cache
            
        Returns:
            bool: True if an entry was invalidated, False otherwise
            
        Raises:
            AttributeError: If the method doesn't exist or isn't cached
        """
        method = getattr(self, method_name)
        if hasattr(method, "invalidate_cache"):
            return method.invalidate_cache(self, *args, **kwargs)
        raise AttributeError(
            f"Method {method_name} doesn't have a cache or doesn't exist"
        )
    
    def invalidate_all_method_cache(self, method_name: str) -> int:
        """
        Invalidate all cache entries for a specific method.
        
        Args:
            method_name: Name of the method whose cache to invalidate
            
        Returns:
            int: Number of cache entries invalidated
            
        Raises:
            AttributeError: If the method doesn't exist or isn't cached
        """
        method = getattr(self, method_name)
        if hasattr(method, "invalidate_all_cache"):
            return method.invalidate_all_cache()
        raise AttributeError(
            f"Method {method_name} doesn't have a cache or doesn't exist"
        )
    
    @abstractmethod
    def get_cache_statistics(self) -> Dict[str, int]:
        """
        Get cache statistics for all cached methods.
        
        Returns:
            Dictionary mapping method names to number of cache entries
        """
        pass
    
    @abstractmethod
    def invalidate_all_caches(self) -> Dict[str, int]:
        """
        Invalidate all caches for all methods.
        
        Returns:
            Dictionary mapping method names to number of entries invalidated
        """
        pass
    
    @abstractmethod
    def search(
        self,
        query: str,
        results: int = 10,
        suggestion: bool = False,
    ) -> Union[List[str], Tuple[List[Any], Optional[List[str]]]]:
        """
        Do a Wikipedia search for `query`.
        
        Keyword arguments:
        * results - the maxmimum number of results returned
        * suggestion - if True, return results and suggestion (if any) in a tuple
        """
        pass
    
    @abstractmethod
    def geosearch(
        self,
        latitude: Any,  # Use Decimal in implementations
        longitude: Any, # Use Decimal in implementations
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
        pass
    
    @abstractmethod
    def suggest(self, query: str) -> Any:
        """
        Get a Wikipedia search suggestion for `query`.
        Returns a string or None if no suggestion was found.
        """
        pass
    
    @abstractmethod
    def random(self, pages: int = 1) -> Any:
        """
        Get a list of random Wikipedia article titles.
        
        Keyword arguments:
        * pages - the number of random pages returned (max of 10)
        """
        pass
    
    @abstractmethod
    def summary(
        self,
        title: str,
        sentences: Optional[int] = 0,
        chars: Optional[int] = 0,
        auto_suggest: bool = False,
        redirect: bool = True,
    ) -> Any:
        """
        Plain text summary of the page.
        
        Keyword arguments:
        * sentences - if set, return the first `sentences` sentences
        * chars - if set, return only the first `chars` characters
        * auto_suggest - let Wikipedia find a valid page title for the query
        * redirect - allow redirection without raising RedirectError
        """
        pass
    
    @abstractmethod
    def page(
        self,
        title: Optional[str] = None,
        pageid: Optional[int] = None,
        auto_suggest: bool = False,
        redirect: bool = True,
        preload: bool = False,
    ) -> P:
        """
        Get a WikipediaPage object for the page with title `title` or the pageid
        `pageid` (mutually exclusive).
        
        Keyword arguments:
        * title - the title of the page to load
        * pageid - the numeric pageid of the page to load
        * auto_suggest - let Wikipedia find a valid page title for the query
        * redirect - allow redirection without raising RedirectError
        * preload - load content, summary, images, references, and links during initialization
        """
        pass
    
    @abstractmethod
    def languages(self) -> Dict[str, str]:
        """
        List all the currently supported language prefixes (usually ISO language code).
        
        Returns: dict of <prefix>: <local_lang_name> pairs.
        """
        pass
    
    @abstractmethod
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
        pass
    
    # Donate is identical in both implementations so implemented here
    def donate(self) -> None:
        """
        Open up the Wikimedia donate page in your favorite browser.
        """
        import webbrowser
        
        webbrowser.open(self.config.donate_url(), new=2)
    
    @abstractmethod
    def custom_query(self, query_params: Dict[str, Any]) -> T:
        """
        Make a custom query to the Wikipedia API with the given parameters.
        
        Arguments:
        * query_params - A dictionary of query parameters to pass to the API
        
        Returns:
        * The raw API response as a dictionary
        """
        pass
    
    # Helper methods for parameter preparation
    def _prepare_search_params(self, query: str, results: int, suggestion: bool) -> Dict[str, Any]:
        """
        Helper method to prepare search parameters.
        
        Args:
            query: The search query
            results: Maximum number of results to return
            suggestion: Whether to return a suggestion
            
        Returns:
            Dictionary of search parameters for the API request
        """
        search_params = {
            "list": "search",
            "srprop": "",
            "srlimit": results,
            "limit": results,
            "srsearch": query,
        }
        if suggestion:
            search_params["srinfo"] = "suggestion"
        return search_params
    
    def _prepare_geosearch_params(
        self, latitude: Any, longitude: Any, title: Optional[str], results: int, radius: int
    ) -> Dict[str, Any]:
        """
        Helper method to prepare geosearch parameters.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            title: Optional title to search for
            results: Maximum number of results to return
            radius: Search radius in meters
            
        Returns:
            Dictionary of geosearch parameters for the API request
        """
        search_params = {
            "list": "geosearch",
            "gsradius": radius,
            "gscoord": f"{latitude}|{longitude}",
            "gslimit": results,
        }
        if title:
            search_params["titles"] = title
        return search_params
    
    def _prepare_suggest_params(self, query: str) -> Dict[str, Any]:
        """
        Helper method to prepare suggest parameters.
        
        Args:
            query: The search query
            
        Returns:
            Dictionary of suggest parameters for the API request
        """
        return {
            "list": "search",
            "srinfo": "suggestion",
            "srprop": "",
            "srsearch": query,
        }
    
    def _prepare_random_params(self, pages: int) -> Dict[str, Any]:
        """
        Helper method to prepare random article parameters.
        
        Args:
            pages: Number of random pages to return
            
        Returns:
            Dictionary of random parameters for the API request
        """
        return {
            "list": "random",
            "rnnamespace": 0,
            "rnlimit": pages,
        }
    
    def _prepare_summary_params(
        self, title: str, sentences: Optional[int], chars: Optional[int]
    ) -> Dict[str, Union[str, int]]:
        """
        Helper method to prepare summary parameters.
        
        Args:
            title: Title of the page
            sentences: Optional number of sentences to return
            chars: Optional number of characters to return
            
        Returns:
            Dictionary of summary parameters for the API request
        """
        query_params: Dict[str, Union[str, int]] = {
            "prop": "extracts",
            "explaintext": "",
            "titles": title,
        }
        if sentences:
            query_params["exsentences"] = sentences
        elif chars:
            query_params["exchars"] = chars
        else:
            query_params["exintro"] = ""
        return query_params
        
    def _prepare_category_members_params(
        self, title: Optional[str], pageid: Optional[int], cmlimit: int, cmtype: str
    ) -> Dict[str, Any]:
        """
        Helper method to prepare category members parameters.
        
        Args:
            title: Title of the category (exclusive with pageid)
            pageid: Page ID of the category (exclusive with title)
            cmlimit: Maximum number of members to return
            cmtype: Type of members to include (page, subcat, or file)
            
        Returns:
            Dictionary of category members parameters for the API request
        """
        if title is not None and pageid is not None:
            raise ValueError(
                "Please specify only a category or only a pageid, only one param can be specified"
            )
        
        if title is not None:
            return {
                "list": "categorymembers",
                "cmtitle": f"Category:{title}",
                "cmlimit": str(cmlimit),
                "cmtype": cmtype,
            }
        elif pageid is not None:
            return {
                "list": "categorymembers",
                "cmpageid": str(pageid),
                "cmlimit": str(cmlimit),
                "cmtype": cmtype,
            }
        else:
            raise ValueError("Either a category or a pageid must be specified")
            
    # Helper methods for error handling
    def _handle_error_response(self, response: Dict[str, Any], query_identifier: str) -> None:
        """
        Helper method to handle error responses from the MediaWiki API.
        
        Args:
            response: API response dictionary
            query_identifier: Identifier for the query (used in error messages)
            
        Raises:
            HTTPTimeoutError: If the API request timed out
            MediaWikiAPIException: For other API errors
        """
        if "error" in response:
            if response["error"]["info"] in (
                "HTTP request timed out.",
                "Pool queue is full",
            ):
                raise HTTPTimeoutError(query_identifier)
            else:
                raise MediaWikiAPIException(response["error"]["info"])
    
    # Helper methods for result processing
    def _process_search_results(
        self, response: Dict[str, Any], suggestion: bool
    ) -> Union[List[str], Tuple[List[Any], Optional[List[str]]]]:
        """
        Helper method to process search results from the API.
        
        Args:
            response: API response dictionary
            suggestion: Whether to return suggestion with results
            
        Returns:
            List of search results, or tuple of (results, suggestion) if suggestion=True
        """
        search_results = (d["title"] for d in response["query"]["search"])
        
        if suggestion:
            if response["query"].get("searchinfo"):
                return (
                    list(search_results),
                    response["query"]["searchinfo"]["suggestion"],
                )
            else:
                return list(search_results), None
        
        return list(search_results)
    
    def _process_geosearch_results(self, response: Dict[str, Any]) -> List[str]:
        """
        Helper method to process geosearch results from the API.
        
        Args:
            response: API response dictionary
            
        Returns:
            List of page titles from the geosearch
        """
        search_pages = response["query"].get("pages", None)
        if search_pages:
            search_results = (v["title"] for k, v in search_pages.items() if k != "-1")
        else:
            search_results = (d["title"] for d in response["query"]["geosearch"])
        
        return list(search_results)
    
    def _process_random_results(self, response: Dict[str, Any], pages: int) -> Union[str, List[str]]:
        """
        Helper method to process random page results from the API.
        
        Args:
            response: API response dictionary
            pages: Number of pages requested
            
        Returns:
            Single title as string if pages=1, otherwise list of titles
        """
        titles = [page["title"] for page in response["query"]["random"]]
        if len(titles) == 1:
            return titles[0]
        return titles
    
    def _process_category_members_results(
        self, response: Dict[str, Any]
    ) -> List[str]:
        """
        Helper method to process category members results from the API.
        
        Args:
            response: API response dictionary
            
        Returns:
            List of page titles in the category
        """
        if "error" in response:
            raise ValueError(response["error"].get("info"))
        return [member["title"] for member in response["query"]["categorymembers"]]