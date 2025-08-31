"""
Error handling utilities for the MediaWikiAPI package.

This module provides common error handling functions used across
both synchronous and asynchronous implementations.
"""

from typing import Any, Dict, Optional, Union, List

from ..exceptions import (
    AccessDeniedError,
    HTTPTimeoutError,
    InvalidParameterError,
    LanguageError,
    MediaWikiAPIException,
    NetworkError,
    PageError,
    RateLimitError,
    RedirectError,
    ServerError,
)


def handle_api_error(response: Dict[str, Any], query_identifier: str) -> None:
    """
    Handle errors in API responses with more specific exception types.

    Args:
        response: The API response dictionary
        query_identifier: Identifier for the query (used in error messages)

    Raises:
        HTTPTimeoutError: If the API request timed out
        RateLimitError: If the rate limit was exceeded
        AccessDeniedError: If access was denied
        InvalidParameterError: If an invalid parameter was provided
        ServerError: For server errors
        MediaWikiAPIException: For other API errors
    """
    if "error" in response:
        error_info = response["error"]
        error_code = error_info.get("code", "")
        error_message = error_info.get("info", "")

        # Create context dictionary with available error information
        context = {
            "query": query_identifier,
            "error_code": error_code,
            "error_info": error_message,
        }

        # Handle specific error types
        if error_message in ("HTTP request timed out.", "Pool queue is full"):
            raise HTTPTimeoutError(query_identifier)

        elif error_code == "ratelimited" or "rate limit" in error_message.lower():
            retry_after = None
            if "retry-after" in response.get("headers", {}):
                try:
                    retry_after = int(response["headers"]["retry-after"])
                except (ValueError, TypeError):
                    pass
            raise RateLimitError(query_identifier, retry_after)

        elif error_code in (
            "permissiondenied",
            "blocked",
            "autoblocked",
            "noedit",
            "cantcreate",
        ):
            raise AccessDeniedError(query_identifier, reason=error_message)

        elif error_code in ("badtoken", "missingparam", "invalidparameter", "badvalue"):
            # Try to extract the parameter name from the error message
            param_name = "unknown"
            if "parameter" in error_message:
                parts = error_message.split("parameter")
                if len(parts) > 1 and parts[1].strip().startswith("'"):
                    param_name = parts[1].strip().split("'")[1]

            raise InvalidParameterError(
                param_name, "invalid value", details=error_message
            )

        elif error_code.startswith(("internal", "server")):
            raise ServerError(error_code, message=error_message)

        else:
            # Fall back to generic MediaWikiAPIException for unhandled error types
            raise MediaWikiAPIException(error_message, context=context)


def handle_page_error(
    response: Dict[str, Any], title: Optional[str] = None, pageid: Optional[int] = None
) -> None:
    """
    Handle page-not-found errors with additional context.

    Args:
        response: The API response dictionary
        title: Title of the page being requested (if applicable)
        pageid: Page ID being requested (if applicable)

    Raises:
        PageError: If the page doesn't exist
    """
    if "missing" in response.get("query", {}).get("pages", {}).get("-1", {}):
        # Create context dictionary with available information
        context = {
            "response_data": response.get("query", {}).get("pages", {}).get("-1", {}),
            "api_response_keys": list(response.keys()),
        }

        raise PageError(pageid=pageid, title=title, context=context)


def handle_redirect(
    response: Dict[str, Any], title: str, allow_redirect: bool
) -> Dict[str, Any]:
    """
    Handle page redirects with target information.

    Args:
        response: The API response dictionary
        title: Title of the page being requested
        allow_redirect: Whether to allow redirects

    Returns:
        The response dictionary, potentially updated to follow the redirect

    Raises:
        RedirectError: If redirect is not allowed but page is a redirect
    """
    if redirects := response.get("query", {}).get("redirects"):
        if not allow_redirect:
            # Get the redirect target if available
            redirect_target = None
            if redirects and len(redirects) > 0 and "to" in redirects[0]:
                redirect_target = redirects[0]["to"]
            raise RedirectError(title, redirect_target=redirect_target)
    return response


def handle_language_error(language: str, available_languages: List[str]) -> None:
    """
    Validate that a language is available with available options.

    Args:
        language: Language code to check
        available_languages: List of available language codes

    Raises:
        LanguageError: If the language is not available, including available languages
    """
    if language not in available_languages:
        # Pass available languages to provide more context in the exception
        raise LanguageError(language, available_languages=available_languages)


def process_search_results(
    response: Dict[str, Any], suggestion: bool
) -> Union[List[str], tuple]:
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


def process_random_results(
    response: Dict[str, Any], pages: int
) -> Union[str, List[str]]:
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
