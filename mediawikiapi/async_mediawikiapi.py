from decimal import Decimal
from functools import partial
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from .async_requestsession import AsyncRequestSession
from .async_util import async_memorized
from .async_wikipediapage import AsyncWikipediaPage
from .config import Config
from .exceptions import HTTPTimeoutError, MediaWikiAPIException, PageError


class AsyncMediaWikiAPI:
    """Asynchronous interface for the MediaWiki API"""

    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialize with optional configuration"""
        self.config = Config()
        if config is not None:
            self.config = config
        self.session = AsyncRequestSession()

    async def close(self) -> None:
        """Close the session"""
        await self.session.close()

    async def __aenter__(self) -> "AsyncMediaWikiAPI":
        """Support for async context manager"""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Close the session when exiting context"""
        await self.close()

    @async_memorized
    async def search(
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
        search_params = {
            "list": "search",
            "srprop": "",
            "srlimit": results,
            "limit": results,
            "srsearch": query,
        }
        if suggestion:
            search_params["srinfo"] = "suggestion"

        raw_results = await self.session.request(search_params, self.config)

        if "error" in raw_results:
            if raw_results["error"]["info"] in (
                "HTTP request timed out.",
                "Pool queue is full",
            ):
                raise HTTPTimeoutError(query)
            else:
                raise MediaWikiAPIException(raw_results["error"]["info"])

        search_results = (d["title"] for d in raw_results["query"]["search"])

        if suggestion:
            if raw_results["query"].get("searchinfo"):
                return (
                    list(search_results),
                    raw_results["query"]["searchinfo"]["suggestion"],
                )
            else:
                return list(search_results), None

        return list(search_results)

    @async_memorized
    async def geosearch(
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
        search_params = {
            "list": "geosearch",
            "gsradius": radius,
            "gscoord": "{0}|{1}".format(latitude, longitude),
            "gslimit": results,
        }
        if title:
            search_params["titles"] = title

        raw_results = await self.session.request(search_params, self.config)

        if "error" in raw_results:
            if raw_results["error"]["info"] in (
                "HTTP request timed out.",
                "Pool queue is full",
            ):
                raise HTTPTimeoutError("{0}|{1}".format(latitude, longitude))
            else:
                raise MediaWikiAPIException(raw_results["error"]["info"])

        search_pages = raw_results["query"].get("pages", None)
        if search_pages:
            search_results = (v["title"] for k, v in search_pages.items() if k != "-1")
        else:
            search_results = (d["title"] for d in raw_results["query"]["geosearch"])

        return list(search_results)

    @async_memorized
    async def suggest(self, query: str) -> Any:
        """
        Get a Wikipedia search suggestion for `query`.
        Returns a string or None if no suggestion was found.
        """
        search_params = {
            "list": "search",
            "srinfo": "suggestion",
            "srprop": "",
        }
        search_params["srsearch"] = query
        raw_result = await self.session.request(search_params, self.config)
        if raw_result["query"].get("searchinfo"):
            return raw_result["query"]["searchinfo"]["suggestion"]
        return None

    async def random(self, pages: int = 1) -> Any:
        """
        Get a list of random Wikipedia article titles.

        .. note:: Random only gets articles from namespace 0, meaning no Category, User talk, or other meta-Wikipedia pages.

        Keyword arguments:

        * pages - the number of random pages returned (max of 10)
        """
        query_params = {
            "list": "random",
            "rnnamespace": 0,
            "rnlimit": pages,
        }
        request = await self.session.request(query_params, self.config)
        titles = [page["title"] for page in request["query"]["random"]]
        if len(titles) == 1:
            return titles[0]
        return titles

    @async_memorized
    async def summary(
        self,
        title: str,
        sentences: Optional[int] = 0,
        chars: Optional[int] = 0,
        auto_suggest: bool = False,
        redirect: bool = True,
    ) -> Any:
        """
        Plain text summary of the page.
        .. note:: This is a convenience wrapper - auto_suggest and redirect are enabled by default
        Keyword arguments:
        * sentences - if set, return the first `sentences` sentences (can be no greater than 10).
        * chars - if set, return only the first `chars` characters (actual text returned may be slightly longer).
        * auto_suggest - let Wikipedia find a valid page title for the query
        * redirect - allow redirection without raising RedirectError
        """
        # use auto_suggest and redirect to get the correct article
        page_info = await self.page(title, auto_suggest=auto_suggest, redirect=redirect)
        title = page_info.title
        pageid = page_info.pageid
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

        request = await self.session.request(query_params, self.config)
        summary = request["query"]["pages"][pageid]["extract"]
        return summary

    async def page(
        self,
        title: Optional[str] = None,
        pageid: Optional[int] = None,
        auto_suggest: bool = False,
        redirect: bool = True,
        preload: bool = False,
    ) -> AsyncWikipediaPage:
        """
        Get an AsyncWikipediaPage object for the page with title `title` or the pageid
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
        # Create a partial function for the request
        request_f = cast(Any, partial(self.session.request, config=self.config))

        if title is not None:
            # Always try exact title match first
            try:
                page = AsyncWikipediaPage(
                    request=request_f, title=title, redirect=False, preload=False
                )
                await page.load(redirect=redirect, preload=preload)
                return page
            except PageError:
                if not auto_suggest:
                    raise

            # If exact match fails and auto_suggest is True, try search
            results, suggestion = await self.search(title, results=1, suggestion=True)
            if suggestion:
                page = AsyncWikipediaPage(
                    request=request_f,
                    title=cast(str, suggestion),
                    pageid=pageid,
                    redirect=False,
                    preload=False,
                )
                await page.load(redirect=redirect, preload=preload)
                return page
            try:
                title = results[0]
            except IndexError:
                # if there are no suggestion or search results, the page doesn't exist
                raise PageError(title=title)
            page = AsyncWikipediaPage(
                request=request_f, title=title, redirect=False, preload=False
            )
            await page.load(redirect=redirect, preload=preload)
            return page
        elif pageid is not None:
            page = AsyncWikipediaPage(
                request=request_f, pageid=pageid, redirect=False, preload=False
            )
            await page.load(redirect=True, preload=preload)
            return page
        else:
            raise ValueError("Either a title or a pageid must be specified")

    async def languages(self) -> Dict[str, str]:
        """
        List all the currently supported language prefixes (usually ISO language code).

        Can be inputted to WikipediaPage.conf to change the Mediawiki that `wikipedia` requests
        results from.

        Returns: dict of <prefix>: <local_lang_name> pairs. To get just a list of prefixes,
        use `wikipedia.languages().keys()`.
        """
        response = await self.session.request(
            {"meta": "siteinfo", "siprop": "languages"}, self.config
        )
        languages = response["query"]["languages"]
        return {lang["code"]: lang["*"] for lang in languages}

    async def category_members(
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
        if title is not None and pageid is not None:
            raise ValueError(
                "Please specify only a category or only a pageid, only one param can be specified"
            )
        elif title is not None:
            query_params = {
                "list": "categorymembers",
                "cmtitle": "Category:{}".format(title),
                "cmlimit": str(cmlimit),
                "cmtype": cmtype,
            }
        elif pageid is not None:
            query_params = {
                "list": "categorymembers",
                "cmpageid": str(pageid),
                "cmlimit": str(cmlimit),
                "cmtype": cmtype,
            }
        else:
            raise ValueError("Either a category or a pageid must be specified")

        response = await self.session.request(query_params, self.config)
        if "error" in response:
            raise ValueError(response["error"].get("info"))
        return [member["title"] for member in response["query"]["categorymembers"]]

    def donate(self) -> None:
        """
        Open up the Wikimedia donate page in your favorite browser.
        """
        import webbrowser

        webbrowser.open(Config().donate_url(), new=2)

    async def custom_query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a custom query to the Wikipedia API with the given parameters.

        This method is useful for complex queries that aren't covered by the standard methods,
        especially those that may return large amounts of data requiring continuation tokens.

        Arguments:
        * query_params - A dictionary of query parameters to pass to the API

        Returns:
        * The raw API response as a dictionary

        Example:
        ```python
        # Query that uses geosearch with pageviews property
        params = {
            "action": "query",
            "generator": "geosearch",
            "ggsradius": 10000,
            "ggscoord": "40.7128|-74.0060",  # New York coordinates
            "ggslimit": 50,
            "prop": "pageviews",
        }
        result = await mediawikiapi.custom_query(params)
        ```
        """
        return await self.session.request(query_params, self.config)
