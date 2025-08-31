"""
Common type definitions for MediaWikiAPI.

This module provides type aliases used across both synchronous and asynchronous
implementations to ensure consistent typing.
"""

from decimal import Decimal
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    Union,
)

from ..config import Config


# Basic type aliases
JSONValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JSONDict = Dict[str, JSONValue]
JSONList = List[JSONValue]
SearchResults = List[str]
SearchResultsWithSuggestion = Tuple[List[str], Optional[str]]
SearchResult = Union[SearchResults, SearchResultsWithSuggestion]
CoordinateValue = Union[float, Decimal]
WikiQuery = Dict[str, Union[str, int, bool, List[str]]]
WikiResponse = Dict[str, Any]


# Type variables for generic specialization
T = TypeVar("T")  # Generic type
P = TypeVar("P")  # For page type


# Protocol for request functions
class SyncRequestCallable(Protocol):
    """Protocol for synchronous request functions."""

    def __call__(self, params: WikiQuery, config: Config) -> WikiResponse: ...


class AsyncRequestCallable(Protocol):
    """Protocol for asynchronous request functions."""

    def __call__(
        self, params: WikiQuery, config: Config
    ) -> Awaitable[WikiResponse]: ...


# Generic request callable
RequestCallable = Union[SyncRequestCallable, AsyncRequestCallable]


# Return type from API methods
APIMethodReturn = Union[
    # Sync types
    str,
    SearchResults,
    SearchResultsWithSuggestion,
    # Async types
    Awaitable[str],
    Awaitable[SearchResults],
    Awaitable[SearchResultsWithSuggestion],
]
