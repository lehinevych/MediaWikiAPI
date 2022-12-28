"""
Global wikipedia exception and warning classes.
"""

from typing import Optional

ODD_ERROR_MESSAGE = (
    "This shouldn't happen. Please report on GitHub: github.com/lehinevych/MediaWikiAPI"
)


class MediaWikiAPIException(Exception):
    """Base Wikipedia exception class."""

    def __init__(self, error: str):
        self.error = error

    def __unicode__(self) -> str:
        return 'An unknown error occured: "{0}". Please report it on GitHub!'.format(
            self.error
        )

    def __str__(self) -> str:
        return self.__unicode__()


class PageError(MediaWikiAPIException):
    """Exception raised when no Wikipedia matched a query."""

    def __init__(self, pageid: Optional[int] = None, title: Optional[str] = None):
        if pageid:
            self.pageid = pageid
        else:
            self.title = title

    def __unicode__(self) -> str:
        if hasattr(self, "title"):
            return '"{0}" does not match any pages. Try another query!'.format(
                self.title
            )
        else:
            return 'Page id "{0}" does not match any pages. Try another id!'.format(
                self.pageid
            )


class LanguageError(MediaWikiAPIException):
    """Exception raised when a language prefix is set which is not available"""

    def __init__(self, language: str):
        self.language = language

    def __unicode__(self) -> str:
        return (
            '"{0}" is not a language prefix available in Wikipedia. '
            "Run wikipedia.languages().keys() to get available prefixes.".format(
                self.language
            )
        )


class RedirectError(MediaWikiAPIException):
    """Exception raised when a page title unexpectedly resolves to a redirect."""

    def __init__(self, title: str):
        self.title = title

    def __unicode__(self) -> str:
        return '"{0}" resulted in a redirect. Set the redirect property to True to allow automatic redirects.'.format(
            self.title
        )


class HTTPTimeoutError(MediaWikiAPIException):
    """Exception raised when a request to the Mediawiki servers times out."""

    def __init__(self, query: str):
        self.query = query

    def __unicode__(self) -> str:
        return (
            'Searching for "{0}" resulted in a timeout. Try again in a few seconds, '
            "and make sure you have rate limiting set to True.".format(self.query)
        )
