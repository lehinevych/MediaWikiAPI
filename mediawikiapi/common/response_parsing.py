"""
Response parsing utilities.

This module provides functions for parsing MediaWiki API responses
in a consistent way across synchronous and asynchronous implementations.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional, Set, Tuple, TypeVar, Union, cast

from .type_definitions import SearchResults, SearchResultsWithSuggestion, WikiResponse


def extract_search_results(response: WikiResponse) -> SearchResults:
    """
    Extract search results from a MediaWiki API search response.

    Args:
        response: API response containing search results

    Returns:
        List of page titles
    """
    if "query" not in response or "search" not in response["query"]:
        return []

    return [d["title"] for d in response["query"]["search"]]


def extract_search_suggestion(response: WikiResponse) -> Optional[str]:
    """
    Extract search suggestion from a MediaWiki API search response.

    Args:
        response: API response containing search suggestion

    Returns:
        Suggestion string or None if no suggestion is available
    """
    if (
        "query" in response
        and "searchinfo" in response["query"]
        and "suggestion" in response["query"]["searchinfo"]
    ):
        return response["query"]["searchinfo"]["suggestion"]
    return None


def process_search_results(
    response: WikiResponse, suggestion: bool
) -> Union[SearchResults, SearchResultsWithSuggestion]:
    """
    Process search results from a MediaWiki API response.

    Args:
        response: API response containing search results
        suggestion: Whether to include suggestion in the result

    Returns:
        List of search results, or tuple of (results, suggestion) if suggestion=True
    """
    results = extract_search_results(response)

    if suggestion:
        sugg = extract_search_suggestion(response)
        return results, sugg

    return results


def extract_geosearch_results(response: WikiResponse) -> SearchResults:
    """
    Extract geosearch results from a MediaWiki API geosearch response.

    Args:
        response: API response containing geosearch results

    Returns:
        List of page titles
    """
    if "query" not in response or "geosearch" not in response["query"]:
        return []

    return [item["title"] for item in response["query"]["geosearch"]]


def extract_random_page_titles(response: WikiResponse) -> SearchResults:
    """
    Extract random page titles from a MediaWiki API random response.

    Args:
        response: API response containing random page titles

    Returns:
        List of page titles
    """
    if "query" not in response or "random" not in response["query"]:
        return []

    return [page["title"] for page in response["query"]["random"]]


def process_random_results(
    response: WikiResponse, pages: int
) -> Union[str, SearchResults]:
    """
    Process random results from a MediaWiki API response.

    Args:
        response: API response containing random page titles
        pages: Number of pages requested

    Returns:
        Single page title string if pages=1, otherwise list of page titles
    """
    results = extract_random_page_titles(response)

    if not results:
        return []

    # Return a single string if only one page was requested
    if pages == 1:
        return results[0]

    return results


def extract_category_members(response: WikiResponse) -> SearchResults:
    """
    Extract category members from a MediaWiki API categorymembers response.

    Args:
        response: API response containing category members

    Returns:
        List of page titles
    """
    if "query" not in response or "categorymembers" not in response["query"]:
        return []

    return [cm["title"] for cm in response["query"]["categorymembers"]]


def extract_coordinates(
    response: WikiResponse, pageid: str
) -> Optional[Tuple[Decimal, Decimal]]:
    """
    Extract coordinates from a MediaWiki API response.

    Args:
        response: API response containing coordinates
        pageid: Page ID to extract coordinates for

    Returns:
        Tuple of (latitude, longitude) as Decimals, or None if not available
    """
    try:
        coordinates = response["query"]["pages"][pageid]["coordinates"]
        return (Decimal(coordinates[0]["lat"]), Decimal(coordinates[0]["lon"]))
    except (KeyError, IndexError, ValueError):
        return None


def extract_page_properties(
    response: WikiResponse, property_name: str
) -> Dict[str, Any]:
    """
    Extract page properties from a MediaWiki API response.

    Args:
        response: API response containing page properties
        property_name: Name of the property to extract

    Returns:
        Dictionary mapping page IDs to property values
    """
    result = {}

    if "query" not in response or "pages" not in response["query"]:
        return result

    for pageid, page_data in response["query"]["pages"].items():
        if property_name in page_data:
            result[pageid] = page_data[property_name]

    return result


def extract_page_titles(response: WikiResponse) -> Dict[str, str]:
    """
    Extract page titles from a MediaWiki API response.

    Args:
        response: API response containing pages

    Returns:
        Dictionary mapping page IDs to titles
    """
    result = {}

    if "query" not in response or "pages" not in response["query"]:
        return result

    for pageid, page_data in response["query"]["pages"].items():
        if "title" in page_data:
            result[pageid] = page_data["title"]

    return result
