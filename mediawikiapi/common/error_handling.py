"""
Error handling utilities for the MediaWikiAPI package.

This module provides common error handling functions used across
both synchronous and asynchronous implementations.
"""

from typing import Any, Dict, Optional, Union, List

from ..exceptions import (
    HTTPTimeoutError, 
    MediaWikiAPIException, 
    PageError, 
    RedirectError,
    LanguageError
)


def handle_api_error(response: Dict[str, Any], query_identifier: str) -> None:
    """
    Handle errors in API responses.
    
    Args:
        response: The API response dictionary
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


def handle_page_error(response: Dict[str, Any], title: Optional[str] = None, pageid: Optional[int] = None) -> None:
    """
    Handle page-not-found errors.
    
    Args:
        response: The API response dictionary
        title: Title of the page being requested (if applicable)
        pageid: Page ID being requested (if applicable)
        
    Raises:
        PageError: If the page doesn't exist
    """
    if "missing" in response.get("query", {}).get("pages", {}).get("-1", {}):
        raise PageError(pageid=pageid, title=title)


def handle_redirect(response: Dict[str, Any], title: str, allow_redirect: bool) -> Dict[str, Any]:
    """
    Handle page redirects.
    
    Args:
        response: The API response dictionary
        title: Title of the page being requested
        allow_redirect: Whether to allow redirects
        
    Returns:
        The response dictionary, potentially updated to follow the redirect
        
    Raises:
        RedirectError: If redirect is not allowed but page is a redirect
    """
    if response.get("query", {}).get("redirects"):
        if not allow_redirect:
            raise RedirectError(title)
    return response


def handle_language_error(language: str, available_languages: List[str]) -> None:
    """
    Validate that a language is available.
    
    Args:
        language: Language code to check
        available_languages: List of available language codes
        
    Raises:
        LanguageError: If the language is not available
    """
    if language not in available_languages:
        raise LanguageError(language)


def process_search_results(response: Dict[str, Any], suggestion: bool) -> Union[List[str], tuple]:
    """
    Process search results from the API.
    
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


def process_geosearch_results(response: Dict[str, Any]) -> List[str]:
    """
    Process geosearch results from the API.
    
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


def process_random_results(response: Dict[str, Any], pages: int) -> Union[str, List[str]]:
    """
    Process random page results from the API.
    
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


def process_category_members_results(response: Dict[str, Any]) -> List[str]:
    """
    Process category members results from the API.
    
    Args:
        response: API response dictionary
        
    Returns:
        List of page titles in the category
    """
    if "error" in response:
        raise ValueError(response["error"].get("info"))
    return [member["title"] for member in response["query"]["categorymembers"]]
