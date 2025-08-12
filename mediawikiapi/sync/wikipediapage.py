from __future__ import annotations

import re
from decimal import Decimal
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union

from bs4 import BeautifulSoup

from ..base.base_wikipediapage import BaseWikipediaPage
from ..exceptions import ODD_ERROR_MESSAGE, PageError, RedirectError
from ..language import Language
from .util import clean_infobox


class WikipediaPage(BaseWikipediaPage):
    """
    Contains data from a Wikipedia page.
    
    This class extends BaseWikipediaPage with synchronous HTTP requests and
    provides access to Wikipedia page content using standard Python data structures.
    Uses property methods to filter data from the raw HTML.
    """

    def __init__(
        self,
        request: Callable[
            [Dict[str, Any]],
            Dict[str, Any],
        ],
        title: Optional[str] = None,
        pageid: Optional[int] = None,
        redirect: bool = True,
        preload: bool = False,
        original_title: str = "",
    ) -> None:
        """
        Initialize a Wikipedia page.
        
        Args:
            request: Function to make API requests
            title: Title of the page (mutually exclusive with pageid)
            pageid: Page ID (mutually exclusive with title)
            original_title: Original title of the page if redirected
            redirect: Whether to follow redirects
            preload: Whether to preload page content
        """
        # Call the parent's init to set up basic properties
        super().__init__(request, title, pageid, original_title)
        
        # Load page data
        self.__load(redirect=redirect, preload=preload)
        
        # Preload properties if requested
        if preload:
            for prop in (
                "content",
                "summary",
                "images",
                "references",
                "links",
                "sections",
                "infobox",
            ):
                getattr(self, prop)

    def __repr__(self) -> str:
        """String representation of the page."""
        return f"<WikipediaPage {self.title}>"

    def __load(self, redirect: bool = True, preload: bool = False) -> None:
        """
        Load basic information from Wikipedia.
        Confirm that page exists and is not a disambiguation/redirect.

        Does not need to be called manually, should be called automatically during
        __init__.
        """
        query_params: Dict[str, Union[str, int]] = {
            "prop": "info|pageprops",
            "inprop": "url",
            "redirects": "",
        }
        if not getattr(self, "pageid", None):
            query_params["titles"] = self.title
        else:
            query_params["pageids"] = self.pageid

        request = self.request(query_params)

        query = request["query"]
        pageid = next(iter(query["pages"].keys()))
        page = query["pages"][pageid]

        # missing is present if the page is missing
        if "missing" in page:
            if hasattr(self, "title"):
                raise PageError(title=self.title)
            else:
                raise PageError(pageid=self.pageid)

        # same thing for redirect, except it shows up in query instead of page for
        # whatever silly reason
        elif "redirects" in query and page["title"] != query["redirects"][0]["to"]:
            if redirect:
                redirects = query["redirects"][0]
                if "normalized" in query:
                    normalized = query["normalized"][0]
                    assert normalized["from"] == self.title, ODD_ERROR_MESSAGE
                    from_title = normalized["to"]

                elif hasattr(self, "title"):
                    from_title = self.title
                else:
                    from_title = redirects["from"]

                assert redirects["from"] == from_title, ODD_ERROR_MESSAGE

                # change the title and reload the whole object
                new_page = WikipediaPage(
                    request=self.request,
                    title=redirects["to"],
                    redirect=redirect,
                    preload=preload,
                    original_title=from_title,
                )
                # Copy all attributes from the new page to self
                for attr, value in vars(new_page).items():
                    setattr(self, attr, value)

            else:
                raise RedirectError(getattr(self, "title", page["title"]))

        self.pageid = pageid
        self.title = page.get("title")
        self.url: str = page.get("fullurl")
        self.language: str = page.get("pagelanguage")
        self.pageprops: Dict[str, Any] = page.get("pageprops", {})
        self.disambiguate_pages: List[Any] = []

        # since we only asked for disambiguation in ppprop,
        # if a pageprop is returned,
        # then the page must be a disambiguation page
        if "pageprops" in page and "disambiguation" in page["pageprops"]:
            query_params = {
                "prop": "revisions",
                "rvprop": "content",
                "rvparse": "",
                "rvlimit": 1,
            }
            if hasattr(self, "pageid"):
                query_params["pageids"] = self.pageid
            else:
                query_params["titles"] = self.title
            request = self.request(query_params)
            html = request["query"]["pages"][pageid]["revisions"][0]["*"]
            lis = BeautifulSoup(html, "html.parser").find_all("li")
            filtered_lis = [
                li for li in lis if "tocsection" not in "".join(li.get("class", []))
            ]
            for lis_item in filtered_lis:
                items = lis_item.find_all("a")
                if items:
                    self.disambiguate_pages.append(items[0]["title"])

    def __continued_query(
        self, query_params: Dict[str, Any]
    ) -> Generator[Any, None, None]:
        """
        Execute a continued query for paging through results.
        Based on https://www.mediawiki.org/wiki/API:Query#Continuing_queries
        
        Args:
            query_params: Parameters for the API request
            
        Yields:
            Data from each page of results
        """
        query_params.update(self._title_query_param)

        last_continue: Dict[str, Any] = {}
        last_len_pages: int = 0
        prop = query_params.get("prop")
        while True:
            params = query_params.copy()
            params.update(last_continue)
            request = self.request(params)
            if "query" not in request:
                break

            if (
                "continue" in request
                and last_continue == request["continue"]
                and last_len_pages == len(request["query"]["pages"])
            ):
                break
            pages = request["query"]["pages"]
            if "generator" in query_params:
                yield from pages.values()
            else:
                if prop in pages[self.pageid]:
                    for datum in pages[self.pageid][prop]:
                        yield datum

            if "continue" not in request:
                break

            last_continue = request["continue"]
            last_len_pages = len(request["query"]["pages"])

    def html(self) -> str:
        """
        Get full page HTML.

        .. warning:: This can get pretty slow on long pages.
        """
        if not getattr(self, "_html", False):
            query_params = {
                "prop": "revisions",
                "rvprop": "content",
                "rvlimit": 1,
                "rvparse": "",
                "titles": self.title,
            }

            request = self.request(query_params)
            self._html = request["query"]["pages"][self.pageid]["revisions"][0]["*"]

        return self._html

    def section(self, section_title: str) -> Optional[str]:
        """
        Get the plain text content of a section from `self.sections`.
        Returns None if `section_title` isn't found, otherwise returns a whitespace
        stripped string.

        This is a convenience method that wraps self.content.

        Args:
            section_title: Title of the section to retrieve
        
        Returns:
            Content of the section or None if not found
        
        .. warning:: Calling `section` on a section that has subheadings will NOT return
               the full text of all of the subsections. It only gets the text between
               `section_title` and the next subheading, which is often empty.
        """
        # Use the helper method from the base class
        return self._extract_section_text(self.content, section_title)

    def lang_title(self, lang_code: str) -> Optional[str]:
        """
        Get the title of this page in a different language.
        
        Args:
            lang_code: Language code to get title for
            
        Returns:
            Title in the requested language or None if not available
            
        Raises:
            LanguageException: If language code is invalid
        """
        # Use the helper method from the base class to build parameters
        query_params = self._build_langlinks_params(Language(lang_code).language)
        
        request = self.request(query_params)
        pageid = next(iter(request["query"]["pages"]))
        title: Optional[str] = None
        
        import contextlib
        with contextlib.suppress(Exception):
            title = request["query"]["pages"][pageid]["langlinks"][0]["*"]
            
        return title
        
    @property
    def infobox(self) -> Dict[str, Any]:
        """
        Info box section of the page
        
        Supported only for MediaWiki version 1.34 or higher
        """
        if getattr(self, "_infobox", False):
            return self._infobox
        if not getattr(self, "_html", False):
            self.html()

        soup = BeautifulSoup(self._html, "html.parser")
        infobox = soup.find("table", {"class": "infobox"})
        results: Dict[str, Any] = {}

        if infobox:
            for row in infobox.find_all("tr"):
                title = row.find("th")
                text = row.find("td")
                if title and text:
                    title = clean_infobox(title.text)
                    results[title] = clean_infobox(text.text)
            self._infobox: Dict[str, Any] = results
        return self._infobox

    @property
    def content(self) -> str:
        """
        Plain text content of the page, excluding images, tables, and other data.
        
        Supported only for MediaWiki version 1.34 or higher
        """
        if not getattr(self, "_content", False):
            query_params: Dict[str, Union[str, int]] = {
                "prop": "extracts|revisions",
                "explaintext": "",
                "rvprop": "ids",
            }
            query_params.update(self._title_query_param)
            request = self.request(query_params)
            self._content: str = request["query"]["pages"][self.pageid]["extract"]
            self._revision_id: int = request["query"]["pages"][self.pageid][
                "revisions"
            ][0]["revid"]
            self._parent_id: int = request["query"]["pages"][self.pageid]["revisions"][
                0
            ]["parentid"]

        return self._content

    @property
    def revision_id(self) -> int:
        """
        Revision ID of the page.
        
        The revision ID is a number that uniquely identifies the current
        version of the page. It can be used to create the permalink or for
        other direct API calls. See `Help:Page history
        <http://en.wikipedia.org/wiki/Wikipedia:Revision>`_ for more
        information.
        
        Supported only for MediaWiki version 1.34 or higher
        """
        if not getattr(self, "_revision_id", False):
            # fetch the content (side effect is loading the revid)
            _ = self.content

        return self._revision_id

    @property
    def parent_id(self) -> int:
        """
        Revision ID of the parent version of the current revision of this
        page. See ``revision_id`` for more information.
        
        Supported only for MediaWiki version 1.34 or higher
        """
        if not getattr(self, "_parent_id", False):
            # fetch the content (side effect is loading the revid)
            _ = self.content
        return self._parent_id

    @property
    def summary(self) -> str:
        """
        Plain text summary of the page.
        
        Supported only for MediaWiki version 1.34 or higher
        """
        if not getattr(self, "_summary", False):
            query_params: Dict[str, Union[str, int]] = {
                "prop": "extracts",
                "explaintext": "",
                "exintro": "",
            }
            query_params.update(self._title_query_param)

            request = self.request(query_params)
            self._summary: str = request["query"]["pages"][self.pageid]["extract"]

        return self._summary

    @property
    def images(self) -> List[str]:
        """
        List of URLs of images on the page.
        """
        if not getattr(self, "_images", False):
            self._images = [
                page["imageinfo"][0]["url"]
                for page in self.__continued_query(
                    {
                        "generator": "images",
                        "gimlimit": "max",
                        "prop": "imageinfo",
                        "iiprop": "url",
                    }
                )
                if "imageinfo" in page and "url" in page["imageinfo"][0]
            ]

        return self._images

    @property
    def coordinates(self) -> Optional[Tuple[Decimal, Decimal]]:
        """
        Tuple of Decimals in the form of (lat, lon) or None
        """
        if not getattr(self, "_coordinates", False):
            query_params = self._build_coordinates_params("max")

            request = self.request(query_params)

            self._coordinates: Optional[Tuple[Decimal, Decimal]] = None
            try:
                coordinates = request["query"]["pages"][self.pageid]["coordinates"]
                self._coordinates = (
                    Decimal(coordinates[0]["lat"]),
                    Decimal(coordinates[0]["lon"]),
                )
            except KeyError:
                pass

        return self._coordinates

    @property
    def references(self) -> List[str]:
        """
        List of URLs of external links on a page.
        May include external links within page that aren't technically cited anywhere.
        """
        if not getattr(self, "_references", False):

            def add_protocol(url: str) -> str:
                return url if url.startswith("http") else "http:" + url

            self._references = [
                add_protocol(link["*"])
                for link in self.__continued_query(
                    self._build_references_params("max")
                )
            ]

        return self._references

    @property
    def links(self) -> List[str]:
        """
        List of titles of Wikipedia page links on a page.
        
        .. note:: Only includes articles from namespace 0, meaning no Category,
          User talk, or other meta-Wikipedia pages.
        """
        if not getattr(self, "_links", False):
            self._links = [
                link["title"]
                for link in self.__continued_query(
                    self._build_links_params(0, "max")
                )
            ]

        return self._links

    @property
    def backlinks(self) -> List[str]:
        """
        List of pages that link to a given page
        """
        if not getattr(self, "_backlinks", False):
            links = list(
                self.__continued_query(
                    {
                        "list": "backlinks",
                        "generator": "links",
                        "bltitle": self._title_query_param,
                        "blfilterredir": "redirects",
                    }
                )
            )
            self._backlinks = [link["title"] for link in links]
            self._backlinks_ids = [link["pageid"] for link in links if "pageid" in link]
        return self._backlinks

    @property
    def backlinks_ids(self) -> List[int]:
        """
        List of pages ids that link to a given page
        
        .. note:: It is not guaranteed that backlinks_ids list contains all backlinks.
            Sometimes the pageid is missing and only title is available, as a result
            len(backlinks_ids) <= len(backlinks).
        """
        if not getattr(self, "_backlinks_ids", False):
            _ = self.backlinks
        return self._backlinks_ids

    @property
    def categories(self) -> List[str]:
        """
        List of categories of a page.
        """
        if not getattr(self, "_categories", False):
            self._categories = [
                re.sub(r"^Category:", "", x)
                for x in [
                    link["title"]
                    for link in self.__continued_query(
                        self._build_categories_params("max")
                    )
                ]
            ]

        return self._categories

    @property
    def sections(self) -> List[str]:
        """
        List of section titles from the table of contents on the page.
        """
        if not getattr(self, "_sections", False):
            query_params: Dict[str, Union[str, int]] = self._build_parse_params()

            request = self.request(query_params)
            self._sections = [
                section["line"] for section in request["parse"]["sections"]
            ]

        return self._sections