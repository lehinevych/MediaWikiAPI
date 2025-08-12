"""
Utilities for managing AsyncMediaWikiAPI cache.
"""

from typing import Dict, Any, Optional

import inspect

from .async_mediawikiapi import AsyncMediaWikiAPI


def get_cached_methods(api_instance: AsyncMediaWikiAPI) -> Dict[str, Any]:
    """
    Get all cached methods in the AsyncMediaWikiAPI instance.

    Args:
        api_instance: Instance of AsyncMediaWikiAPI

    Returns:
        Dictionary mapping method names to method objects that have caching
    """
    cached_methods = {}

    # Get all methods from the instance
    for name, method in inspect.getmembers(api_instance):
        # Check if it's a method with cache invalidation capability
        if inspect.iscoroutinefunction(method) and hasattr(method, "invalidate_cache"):
            cached_methods[name] = method

    return cached_methods


def invalidate_all_caches(api_instance: AsyncMediaWikiAPI) -> Dict[str, int]:
    """
    Invalidate all caches for all methods in the AsyncMediaWikiAPI instance.

    Args:
        api_instance: Instance of AsyncMediaWikiAPI

    Returns:
        Dictionary mapping method names to number of cache entries invalidated
    """
    invalidation_counts = {}
    cached_methods = get_cached_methods(api_instance)

    for name, method in cached_methods.items():
        count = method.invalidate_all_cache()
        invalidation_counts[name] = count

    return invalidation_counts


def get_cache_statistics(api_instance: AsyncMediaWikiAPI) -> Dict[str, int]:
    """
    Get cache statistics for all methods in the AsyncMediaWikiAPI instance.

    Args:
        api_instance: Instance of AsyncMediaWikiAPI

    Returns:
        Dictionary mapping method names to number of cache entries
    """
    statistics = {}
    cached_methods = get_cached_methods(api_instance)

    # This works because the memoized methods have a reference to their decorator
    # and the decorator has a cache dictionary
    for name, method in cached_methods.items():
        # Find the memoize instance to get the cache size
        function = method.__func__
        if hasattr(function, "__closure__") and function.__closure__:
            for cell in function.__closure__:
                if hasattr(cell.cell_contents, "cache"):
                    statistics[name] = len(cell.cell_contents.cache)
                    break

    return statistics
