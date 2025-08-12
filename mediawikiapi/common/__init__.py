"""
Common module containing shared utilities and functionality.

This module provides shared utilities, validators, and error handlers
used by both synchronous and asynchronous implementations.
"""

from .validation import (
    validate_title_or_pageid,
    validate_geosearch_params,
    validate_search_params,
    validate_limit,
    validate_category_params,
    validate_sentences_and_chars
)
from .error_handling import (
    handle_api_error,
    handle_page_error,
    handle_redirect,
    handle_language_error,
    process_search_results,
    process_geosearch_results,
    process_random_results,
    process_category_members_results
)

__all__ = [
    # Validation functions
    "validate_title_or_pageid",
    "validate_geosearch_params",
    "validate_search_params",
    "validate_limit",
    "validate_category_params",
    "validate_sentences_and_chars",
    
    # Error handling functions
    "handle_api_error",
    "handle_page_error",
    "handle_redirect",
    "handle_language_error",
    "process_search_results",
    "process_geosearch_results",
    "process_random_results",
    "process_category_members_results"
]