"""
Global MediaWiki API exception and warning classes.

This module defines a hierarchy of exceptions that can be raised during
interactions with the MediaWiki API. The exceptions provide specific
information about different types of errors that can occur.
"""

from typing import Optional, Dict, Any, List

ODD_ERROR_MESSAGE = (
    "This shouldn't happen. Please report on GitHub: github.com/lehinevych/MediaWikiAPI"
)


class MediaWikiAPIException(Exception):
    """Base exception class for all MediaWikiAPI errors."""

    def __init__(self, error: str, context: Optional[Dict[str, Any]] = None):
        self.error = error
        self.context = context or {}

    def __unicode__(self) -> str:
        msg = f'An error occurred: "{self.error}"'
        if self.context:
            msg += f'. Context: {self.context}'
        return msg

    def __str__(self) -> str:
        return self.__unicode__()


class PageError(MediaWikiAPIException):
    """Exception raised when no Wikipedia page matched a query."""

    def __init__(
        self, 
        pageid: Optional[int] = None, 
        title: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        self.context = context or {}
        if pageid:
            self.pageid = pageid
            self.context['pageid'] = pageid
        else:
            self.title = title
            if title:
                self.context['title'] = title

    def __unicode__(self) -> str:
        if hasattr(self, "title"):
            return f'"{self.title}" does not match any pages. Try another query!'
        else:
            return f'Page id "{self.pageid}" does not match any pages. Try another id!'


class LanguageError(MediaWikiAPIException):
    """Exception raised when a language prefix is set which is not available."""

    def __init__(self, language: str, available_languages: Optional[List[str]] = None):
        self.language = language
        context = {'language': language}
        if available_languages:
            context['available_languages'] = available_languages
        super().__init__(f'Language prefix "{language}" is not available', context)

    def __unicode__(self) -> str:
        return (
            f'"{self.language}" is not a language prefix available in Wikipedia. '
            "Run wikipedia.languages().keys() to get available prefixes."
        )


class RedirectError(MediaWikiAPIException):
    """Exception raised when a page title unexpectedly resolves to a redirect."""

    def __init__(self, title: str, redirect_target: Optional[str] = None):
        self.title = title
        context = {'title': title}
        if redirect_target:
            self.redirect_target = redirect_target
            context['redirect_target'] = redirect_target
        super().__init__(f'Page "{title}" is a redirect', context)

    def __unicode__(self) -> str:
        msg = f'"{self.title}" resulted in a redirect'
        if hasattr(self, 'redirect_target'):
            msg += f' to "{self.redirect_target}"'
        msg += ". Set the redirect property to True to allow automatic redirects."
        return msg


class HTTPTimeoutError(MediaWikiAPIException):
    """Exception raised when a request to the Mediawiki servers times out."""

    def __init__(self, query: str, timeout: Optional[int] = None):
        self.query = query
        context = {'query': query}
        if timeout:
            self.timeout = timeout
            context['timeout'] = timeout
        super().__init__('HTTP request timed out', context)

    def __unicode__(self) -> str:
        msg = f'Searching for "{self.query}" resulted in a timeout'
        if hasattr(self, 'timeout'):
            msg += f' (timeout: {self.timeout}s)'
        msg += ". Try again in a few seconds, and make sure you have rate limiting set to True."
        return msg


class RateLimitError(MediaWikiAPIException):
    """Exception raised when the API rate limit is exceeded."""
    
    def __init__(self, query: str, retry_after: Optional[int] = None):
        self.query = query
        context = {'query': query}
        if retry_after:
            self.retry_after = retry_after
            context['retry_after'] = retry_after
        super().__init__('Rate limit exceeded', context)
        
    def __unicode__(self) -> str:
        msg = f'Rate limit exceeded for query "{self.query}"'
        if hasattr(self, 'retry_after'):
            msg += f'. Try again after {self.retry_after} seconds'
        else:
            msg += '. Try again later'
        return msg


class AccessDeniedError(MediaWikiAPIException):
    """Exception raised when access to the API is denied."""
    
    def __init__(self, query: str, reason: Optional[str] = None):
        self.query = query
        context = {'query': query}
        if reason:
            self.reason = reason
            context['reason'] = reason
        super().__init__('Access denied', context)
        
    def __unicode__(self) -> str:
        msg = f'Access denied for query "{self.query}"'
        if hasattr(self, 'reason'):
            msg += f': {self.reason}'
        return msg


class InvalidParameterError(MediaWikiAPIException):
    """Exception raised when an invalid parameter is provided to the API."""
    
    def __init__(self, parameter: str, value: Any, details: Optional[str] = None):
        self.parameter = parameter
        self.value = value
        context = {'parameter': parameter, 'value': str(value)}
        if details:
            self.details = details
            context['details'] = details
        super().__init__(f'Invalid parameter: {parameter}', context)
        
    def __unicode__(self) -> str:
        msg = f'Invalid value "{self.value}" for parameter "{self.parameter}"'
        if hasattr(self, 'details'):
            msg += f': {self.details}'
        return msg


class ServerError(MediaWikiAPIException):
    """Exception raised when a server error occurs."""
    
    def __init__(self, error_code: str, message: Optional[str] = None):
        self.error_code = error_code
        context = {'error_code': error_code}
        if message:
            context['message'] = message
        super().__init__(f'Server error: {error_code}', context)
        
    def __unicode__(self) -> str:
        msg = f'MediaWiki server error (code: {self.error_code})'
        if hasattr(self, 'context') and 'message' in self.context:
            msg += f': {self.context["message"]}'
        return msg


class NetworkError(MediaWikiAPIException):
    """Exception raised when a network error occurs."""
    
    def __init__(self, error: str, original_exception: Optional[Exception] = None):
        context = {}
        if original_exception:
            self.original_exception = original_exception
            context['original_exception'] = str(original_exception)
        super().__init__(error, context)
        
    def __unicode__(self) -> str:
        return f'Network error: {self.error}'
