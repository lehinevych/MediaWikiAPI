"""
Utilities for managing MediaWikiAPI cache.
"""

from typing import Dict, List, Set, Any, Optional, Type
import inspect

from .mediawikiapi import MediaWikiAPI


def get_cached_methods(api_instance: MediaWikiAPI) -> Dict[str, Any]:
    """
    Get all cached methods in the MediaWikiAPI instance.

    Args:
        api_instance: Instance of MediaWikiAPI

    Returns:
        Dictionary mapping method names to method objects that have caching
    """
    cached_methods = {}

    # Get all methods from the instance
    for name, method in inspect.getmembers(api_instance):
        # Check if it's a method with cache invalidation capability
        if inspect.ismethod(method) and hasattr(method, "invalidate_cache"):
            cached_methods[name] = method

    return cached_methods


def invalidate_all_caches(api_instance: MediaWikiAPI) -> Dict[str, int]:
    """
    Invalidate all caches for all methods in the MediaWikiAPI instance.

    Args:
        api_instance: Instance of MediaWikiAPI

    Returns:
        Dictionary mapping method names to number of cache entries invalidated
    """
    invalidation_counts = {}
    cached_methods = get_cached_methods(api_instance)

    for name, method in cached_methods.items():
        count = method.invalidate_all_cache()
        invalidation_counts[name] = count

    return invalidation_counts


def get_cache_statistics(api_instance: MediaWikiAPI) -> Dict[str, int]:
    """
    Get cache statistics for all methods in the MediaWikiAPI instance.

    Args:
        api_instance: Instance of MediaWikiAPI

    Returns:
        Dictionary mapping method names to number of cache entries
    """
    statistics = {}
    cached_methods = get_cached_methods(api_instance)

    # This works because the memoized methods have a reference to their decorator
    # and the decorator has a cache dictionary
    for name, method in cached_methods.items():
        # Find the memoize instance to get the cache size
        # This is method.__self__.__class__.__dict__[method.__name__].__closure__[0].cell_contents
        # but we'll use a simpler approach by using the __func__ attribute
        function = method.__func__
        if hasattr(function, "__closure__") and function.__closure__:
            for cell in function.__closure__:
                if hasattr(cell.cell_contents, "cache"):
                    statistics[name] = len(cell.cell_contents.cache)
                    break

    return statistics
