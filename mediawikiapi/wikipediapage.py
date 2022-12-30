from __future__ import annotations
import re
from typing import Dict, List, Any, Tuple, Optional, Generator, Callable, Union
from decimal import Decimal
from bs4 import BeautifulSoup
from .config import Config
from .exceptions import PageError, RedirectError, ODD_ERROR_MESSAGE
from .language import Language
from .util import clean_infobox


class WikipediaPage(object):
    """
    Contains data from a Wikipedia page.
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
        if title is not None:
            self.title: str = title
            self.original_title: str = original_title or title
        elif pageid is not None:
            self.pageid: int = pageid
        else:
            raise ValueError("Either a title or a pageid must be specified")

        self.request = request
        self.__load(redirect=redirect, preload=preload)
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
        return "<WikipediaPage {}>".format(self.title)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WikipediaPage):
            return NotImplemented
        try:
            return (
                self.pageid == other.pageid
                and self.title == other.title
                and self.url == other.url
            )
        except Exception:
            return False

    def __load(self, redirect: bool = True, preload: bool = False) -> None:
        """
        Load basic information from Wikipedia.
        Confirm that page exists and is not a disambiguation/redirect.

        Does not need to be called manually, should be called automatically during __init__.
        """
        query_params: Dict[str, str | int] = {
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
        pageid = list(query["pages"].keys())[0]
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
                # TODO this should be refactored
                self.__init__(  # type:ignore
                    redirects["to"],
                    redirect=redirect,
                    preload=preload,
                    request=self.request,
                )

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
        Based on https://www.mediawiki.org/wiki/API:Query#Continuing_queries
        """
        query_params.update(self.__title_query_param)

        last_continue: Dict[str, Any] = {}
        last_len_pages: int = 0
        prop = query_params.get("prop", None)
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

    @property
    def __title_query_param(self) -> Dict[str, str | int]:
        if getattr(self, "title", None) is not None:
            return {"titles": self.title}
        else:
            return {"pageids": self.pageid}

    def html(self) -> Any:
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

    @property
    def infobox(self) -> Dict[str, Any]:
        if getattr(self, "_infobox", False):
            return self._infobox
        if not getattr(self, "_html", False):
            self.html()

        soup = BeautifulSoup(self._html, "html.parser")
        infobox = soup.find("table", {"class": "infobox"})
        results: Dict[str, Any] = {}

        if infobox:
            for row in infobox.findAll("tr"):  # type: ignore
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
        """
        if not getattr(self, "_content", False):
            query_params: Dict[str, str | int] = {
                "prop": "extracts|revisions",
                "explaintext": "",
                "rvprop": "ids",
            }
            query_params.update(self.__title_query_param)
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
        """
        if not getattr(self, "_revid", False):
            # fetch the content (side effect is loading the revid)
            self.content

        return self._revision_id

    @property
    def parent_id(self) -> int:
        """
        Revision ID of the parent version of the current revision of this
        page. See ``revision_id`` for more information.
        """
        if not getattr(self, "_parentid", False):
            # fetch the content (side effect is loading the revid)
            self.content
        return self._parent_id

    @property
    def summary(self) -> str:
        """
        Plain text summary of the page.
        """
        if not getattr(self, "_summary", False):
            query_params: Dict[str, str | int] = {
                "prop": "extracts",
                "explaintext": "",
                "exintro": "",
            }
            query_params.update(self.__title_query_param)

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
            query_params = {
                "prop": "coordinates",
                "colimit": "max",
                "titles": self.title,
            }

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
                    {"prop": "extlinks", "ellimit": "max"}
                )
            ]

        return self._references

    @property
    def links(self) -> List[str]:
        """
        List of titles of Wikipedia page links on a page.

        .. note:: Only includes articles from namespace 0, meaning no Category, User talk, or other meta-Wikipedia pages.
        """
        if not getattr(self, "_links", False):
            self._links = [
                link["title"]
                for link in self.__continued_query(
                    {"prop": "links", "plnamespace": 0, "pllimit": "max"}
                )
            ]

        return self._links

    @property
    def backlinks(self) -> List[str]:
        """
        List of pages that link to a given page
        """
        if not getattr(self, "_backlinks", False):
            links = [
                link
                for link in self.__continued_query(
                    {
                        "list": "backlinks",
                        "generator": "links",
                        "bltitle": self.__title_query_param,
                        "blfilterredir": "redirects",
                    }
                )
            ]
            self._backlinks = [link["title"] for link in links]
            self._backlinks_ids = [link["pageid"] for link in links if "pageid" in link]
        return self._backlinks

    @property
    def backlinks_ids(self) -> List[int]:
        """
        List of pages ids that link to a given page

        .. note:: It is not garanted that backlinks_ids list contains all backlinks.
            Sometimes the pageid is missing and only title is available, as a result
            len(backlinks_ids) <= len(backlinks).
        """
        if not getattr(self, "_backlinks_ids", False):
            getattr(self, "backlinks")
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
                        {"prop": "categories", "cllimit": "max"}
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
            query_params: Dict[str, str | int] = {
                "action": "parse",
                "prop": "sections",
            }
            if getattr(self, "title", None) is not None:
                query_params.update({"page": self.title})
            else:
                query_params.update({"pageid": self.pageid})

            request = self.request(query_params)
            self._sections = [
                section["line"] for section in request["parse"]["sections"]
            ]

        return self._sections

    def section(self, section_title: str) -> Optional[str]:
        """
        Get the plain text content of a section from `self.sections`.
        Returns None if `section_title` isn't found, otherwise returns a whitespace stripped string.

        This is a convenience method that wraps self.content.

        .. warning:: Calling `section` on a section that has subheadings will NOT return
               the full text of all of the subsections. It only gets the text between
               `section_title` and the next subheading, which is often empty.
        """

        section = "== {} ==".format(section_title)
        try:
            index = self.content.index(section) + len(section)
        except ValueError:
            return None

        try:
            next_index = self.content.index("==", index)
        except ValueError:
            next_index = len(self.content)

        return self.content[index:next_index].lstrip("=").strip()

    def lang_title(self, lang_code: str) -> Optional[str]:
        """
        Get the title in specified language code
        Returns None if lang code or title isn't found, otherwise returns a string with title.
        Raise LanguageException if language doesn't exists
        """
        query_params = {
            "prop": "langlinks",
            "llurl": True,
        }
        query_params.update({"lllang": Language(lang_code).language})
        query_params.update(self.__title_query_param)
        request = self.request(query_params)
        pageid = list(request["query"]["pages"])[0]
        title: Optional[str] = None
        try:
            title = request["query"]["pages"][pageid]["langlinks"][0]["*"]
        except Exception:
            pass
        return title
