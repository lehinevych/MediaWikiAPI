"""
MediaWikiAPI - A Python library for accessing and parsing data from Wikipedia.

This library provides both synchronous and asynchronous interfaces to the MediaWiki API,
making it easy to work with Wikipedia data in Python.
"""

# Configuration and common classes
from .config import Config
from .exceptions import (
    ODD_ERROR_MESSAGE,
    HTTPTimeoutError,
    LanguageError,
    MediaWikiAPIException,
    PageError,
    RedirectError,
)
from .language import Language

# Base classes
from .base import (
    BaseMediaWikiAPI,
    BaseWikipediaPage,
    BaseRequestSession
)

# Synchronous implementations
from .sync import (
    MediaWikiAPI,
    WikipediaPage,
    RequestSession,
    memorized,
    get_cache_statistics as sync_get_cache_statistics,
    invalidate_all_caches as sync_invalidate_all_caches
)

# Asynchronous implementations
from .async_api import (
    AsyncMediaWikiAPI,
    AsyncWikipediaPage,
    AsyncRequestSession,
    async_memorized,
    get_cache_statistics as async_get_cache_statistics,
    invalidate_all_caches as async_invalidate_all_caches
)

# Common utilities
from .common import (
    # Validation functions
    validate_title_or_pageid,
    validate_geosearch_params,
    validate_search_params,
    validate_limit,
    validate_category_params,
    validate_sentences_and_chars,
    
    # Error handling functions
    handle_api_error,
    handle_page_error,
    handle_redirect,
    handle_language_error,
    process_search_results,
    process_geosearch_results,
    process_random_results,
    process_category_members_results
)

# For backward compatibility
get_cache_statistics = sync_get_cache_statistics
invalidate_all_caches = sync_invalidate_all_caches

__all__ = [
    # Configuration and common classes
    "Config",
    "Language",
    "ODD_ERROR_MESSAGE",
    "HTTPTimeoutError",
    "LanguageError",
    "MediaWikiAPIException",
    "PageError",
    "RedirectError",
    
    # Base classes
    "BaseMediaWikiAPI",
    "BaseWikipediaPage",
    "BaseRequestSession",
    
    # Synchronous implementations
    "MediaWikiAPI",
    "WikipediaPage",
    "RequestSession",
    "memorized",
    "get_cache_statistics",
    "invalidate_all_caches",
    
    # Asynchronous implementations
    "AsyncMediaWikiAPI",
    "AsyncWikipediaPage",
    "AsyncRequestSession",
    "async_memorized",
    "async_get_cache_statistics",
    "async_invalidate_all_caches",
    
    # Common utilities
    "validate_title_or_pageid",
    "validate_geosearch_params",
    "validate_search_params",
    "validate_limit",
    "validate_category_params",
    "validate_sentences_and_chars",
    "handle_api_error",
    "handle_page_error",
    "handle_redirect",
    "handle_language_error",
    "process_search_results",
    "process_geosearch_results",
    "process_random_results",
    "process_category_members_results"
]