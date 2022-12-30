from functools import partial
from typing import Dict, List, Union, Optional, Any, Tuple
from decimal import Decimal
from .exceptions import PageError, HTTPTimeoutError, MediaWikiAPIException
from .config import Config
from .util import memorized
from .wikipediapage import WikipediaPage
from .requestsession import RequestSession


class MediaWikiAPI(object):
    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = Config()
        if config is not None:
            self.config = config
        self.session = RequestSession()

    @memorized
    def search(
        self, query: str, results: int = 10, suggestion: bool = False
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

        raw_results = self.session.request(search_params, self.config)

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
        search_params = {
            "list": "geosearch",
            "gsradius": radius,
            "gscoord": "{0}|{1}".format(latitude, longitude),
            "gslimit": results,
        }
        if title:
            search_params["titles"] = title

        raw_results = self.session.request(search_params, self.config)

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

    @memorized
    def suggest(self, query: str) -> Any:
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
        raw_result = self.session.request(search_params, self.config)
        if raw_result["query"].get("searchinfo"):
            return raw_result["query"]["searchinfo"]["suggestion"]
        return None

    def random(self, pages: int = 1) -> Any:
        """
        Get a list of random Wikipedia article titles.

        .. note:: Random only gets articles from namespace 0, meaning no Category, User talk, or other meta-Wikipedia pages.

        Keyword arguments:

        * pages - the number of random pages returned (max of 10)
        """
        # http://en.wikipedia.org/w/api.php?action=query&list=random&rnlimit=5000&format=jsonfm
        query_params = {
            "list": "random",
            "rnnamespace": 0,
            "rnlimit": pages,
        }
        request = self.session.request(query_params, self.config)
        titles = [page["title"] for page in request["query"]["random"]]
        if len(titles) == 1:
            return titles[0]
        return titles

    @memorized
    def summary(
        self,
        title: str,
        sentences: Optional[int] = 0,
        chars: Optional[int] = 0,
        auto_suggest: bool = True,
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
        page_info = self.page(title, auto_suggest=auto_suggest, redirect=redirect)
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

        request = self.session.request(query_params, self.config)
        summary = request["query"]["pages"][pageid]["extract"]
        return summary

    def page(
        self,
        title: Optional[str] = None,
        pageid: Optional[int] = None,
        auto_suggest: bool = True,
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

        Attention!

        The usage of auto_suggest may provide you with different page than you searched.

        For example:

        `page("The Squires (disambiguation)", auto_suggest=True)` returns page with title `Squires (disambiguation)`

        `page("The Squires (disambiguation)", auto_suggest=False)` returns page with title `The Squires (disambiguation)`
        """
        request_f = partial(self.session.request, config=self.config)
        if title is not None:
            if auto_suggest:
                results, suggestion = self.search(title, results=1, suggestion=True)
                if suggestion:
                    return WikipediaPage(
                        request=request_f,
                        title=suggestion,
                        pageid=pageid,
                        redirect=redirect,
                        preload=preload,
                    )
                try:
                    title = results[0]
                except IndexError:
                    # if there are no suggestion or search results, the page doesn't exist
                    raise PageError(title=title)
            return WikipediaPage(
                request=request_f, title=title, redirect=redirect, preload=preload
            )
        elif pageid is not None:
            return WikipediaPage(request=request_f, pageid=pageid, preload=preload)
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

        response = self.session.request(query_params, self.config)
        if "error" in response:
            raise ValueError(response["error"].get("info"))
        return [member["title"] for member in response["query"]["categorymembers"]]

    def donate(self) -> None:
        """
        Open up the Wikimedia donate page in your favorite browser.
        """
        import webbrowser

        webbrowser.open(Config().donate_url(), new=2)
