"""
Continuation request handling utilities.

This module provides functions for handling continuation tokens in MediaWiki API responses.
These utilities are used by both synchronous and asynchronous implementations.
"""

from typing import Any, Dict, List, TypeVar, Union

from .type_definitions import WikiResponse

T = TypeVar("T")  # For generic result types


def should_continue(response: WikiResponse) -> bool:
    """
    Check if a response contains a continue token.

    Args:
        response: API response dictionary

    Returns:
        True if the response contains a continue token, False otherwise
    """
    return "continue" in response


def get_continue_params(
    response: WikiResponse, original_params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Get parameters for a continuation request.

    Args:
        response: API response containing continue token
        original_params: Original parameters used for the initial request

    Returns:
        Parameters for the continuation request
    """
    # Copy the original parameters and update with continue tokens
    continue_params = original_params.copy()
    continue_params.update(response["continue"])
    return continue_params


def merge_page_results(
    original_result: WikiResponse, continued_data: WikiResponse
) -> None:
    """
    Merge pages from a continuation response into the original result.

    This function modifies the original_result in place.

    Args:
        original_result: Original result dictionary to update
        continued_data: Continuation response data to merge
    """
    if "query" not in continued_data:
        return

    if "pages" in continued_data.get("query", {}) and "pages" in original_result.get(
        "query", {}
    ):
        for pageid, page_data in continued_data["query"]["pages"].items():
            if pageid in original_result["query"]["pages"]:
                # Page exists in the result, merge properties
                for prop, value in page_data.items():
                    if prop in original_result["query"]["pages"][pageid]:
                        # If the property is a list, extend it
                        if isinstance(value, list) and isinstance(
                            original_result["query"]["pages"][pageid][prop], list
                        ):
                            original_result["query"]["pages"][pageid][prop].extend(
                                value
                            )
                        else:
                            # Otherwise, replace it
                            original_result["query"]["pages"][pageid][prop] = value
                    else:
                        # Property doesn't exist in the result, add it
                        original_result["query"]["pages"][pageid][prop] = value
            else:
                # Page doesn't exist in the result, add it
                original_result["query"]["pages"][pageid] = page_data


def merge_query_results(
    original_result: WikiResponse, continued_data: WikiResponse
) -> None:
    """
    Merge query properties from a continuation response into the original result.

    This function modifies the original_result in place.

    Args:
        original_result: Original result dictionary to update
        continued_data: Continuation response data to merge
    """
    if "query" not in continued_data:
        return

    # Handle lists in the query (like search results, backlinks, etc.)
    for prop, value in continued_data["query"].items():
        if prop != "pages":  # Pages are handled by merge_page_results
            if prop not in original_result["query"]:
                original_result["query"][prop] = value
            elif isinstance(value, list) and isinstance(
                original_result["query"][prop], list
            ):
                # If the property is a list, extend it
                original_result["query"][prop].extend(value)


def update_continue_token(
    original_result: WikiResponse, continued_data: WikiResponse
) -> None:
    """
    Update the continue token in the original result.

    This function modifies the original_result in place.

    Args:
        original_result: Original result dictionary to update
        continued_data: Continuation response data with new token
    """
    if "continue" in continued_data:
        original_result["continue"] = continued_data["continue"]
    else:
        # No more continue tokens, remove it from the original result
        if "continue" in original_result:
            del original_result["continue"]


def merge_continue_results(
    original_result: WikiResponse, continued_data: WikiResponse
) -> None:
    """
    Merge all data from a continuation response into the original result.

    This function modifies the original_result in place.

    Args:
        original_result: Original result dictionary to update
        continued_data: Continuation response data to merge
    """
    # Merge pages
    merge_page_results(original_result, continued_data)

    # Merge other query properties
    merge_query_results(original_result, continued_data)

    # Update continue token
    update_continue_token(original_result, continued_data)
