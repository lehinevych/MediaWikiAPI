from __future__ import annotations

import collections
import functools
import heapq
import re
import sys
import time
from collections import OrderedDict
from collections.abc import Callable
from typing import Any, Dict, List, Optional, TypeVar, Tuple, Union

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


class memoized_class(object):
    """
    Decorator.
    Caches a function's return value each time it is called.
    If called later with the same arguments and language,
    the cached value is returned (not reevaluated).

    Optional parameters:
    - ttl: Time to live in seconds. If specified, cached values will expire after this duration.
    - max_size: Maximum number of entries to store in the cache. If specified, uses a
      least-recently-used (LRU) strategy to evict old entries when the cache is full.

    Cache invalidation methods:
    - invalidate_cache(*args, **kwargs): Invalidate cache for specific arguments
    - invalidate_all_cache(): Invalidate all cached values for this function
    """

    def __init__(
        self,
        func: Optional[Callable[..., Any]] = None,
        *,
        ttl: Optional[float] = None,
        max_size: Optional[int] = None,
    ) -> None:
        self.func = func
        self.ttl = ttl
        self.max_size = max_size

        # Initialize cache as a normal dict or OrderedDict based on max_size
        self.cache: Union[
            Dict[str, tuple[Any, float]], OrderedDict[str, tuple[Any, float]]
        ] = {}
        # We'll convert to OrderedDict later if needed when we know the instance config

        # Handle both @memorized and @memorized(...) forms
        if func is not None:
            functools.update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        # Handle both @memorized and @memorized(...) forms
        if self.func is None:
            # Called as @memorized(...)
            func = args[0]
            wrapped = memoized_class(func=func, ttl=self.ttl, max_size=self.max_size)
            return wrapped

        is_uncacheable = [not isinstance(ar, collections.abc.Hashable) for ar in args]
        if any(is_uncacheable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args, **kwargs)

            # Generate cache key
        key = self._get_cache_key(*args, **kwargs)

        # Check if key exists in cache and if the cached value is not expired
        current_time = time.time()
        if key in self.cache:
            value, timestamp = self.cache[key]

            # Check TTL from instance config or decorator parameter
            ttl = self.ttl
            if ttl is None and args and args[0] is not None:
                instance = args[0]
                if hasattr(instance, "config") and hasattr(
                    instance.config, "cache_ttl"
                ):
                    ttl = instance.config.cache_ttl

            # If TTL is set and the cached value has expired, recompute
            if ttl is None or (current_time - timestamp) < ttl:
                # Check if we need size limits based on instance config
                max_size = self.max_size
                if max_size is None and args and args[0] is not None:
                    instance = args[0]
                    if hasattr(instance, "config") and hasattr(
                        instance.config, "cache_max_size"
                    ):
                        max_size = instance.config.cache_max_size

                # For LRU cache, move accessed item to the end (most recently used)
                if max_size is not None:
                    # Convert to OrderedDict if needed
                    if not isinstance(self.cache, OrderedDict):
                        self.cache = OrderedDict(self.cache)
                    # Remove and reinsert to move to end of OrderedDict
                    del self.cache[key]
                    self.cache[key] = (value, timestamp)
                return value

        # Compute new value and store with current timestamp
        value = self.func(*args, **kwargs)

        # Check max_size from instance config or decorator parameter
        max_size = self.max_size
        if max_size is None and args and args[0] is not None:
            instance = args[0]
            if hasattr(instance, "config") and hasattr(
                instance.config, "cache_max_size"
            ):
                max_size = instance.config.cache_max_size

        # Convert cache to OrderedDict if we need size limits and haven't converted already
        if max_size is not None and not isinstance(self.cache, OrderedDict):
            # Convert to OrderedDict for LRU tracking
            self.cache = OrderedDict(self.cache)

        # Handle cache size limits
        if max_size is not None:
            # Move existing key to the end (most recently used position) by removing and reinserting
            if key in self.cache:
                del self.cache[key]

            # Remove oldest entry if at max size
            if len(self.cache) >= max_size:
                # OrderedDict remembers insertion order
                # popitem(last=False) removes the first-inserted (oldest) item
                self.cache.popitem(last=False)

            # Add the new entry at the end (most recently used position)
            self.cache[key] = (value, current_time)
        else:
            self.cache[key] = (value, current_time)

        return value

    def __repr__(self) -> Any:
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj: Optional[R], objtype: Optional[R]) -> Any:
        """Support instance methods."""
        return functools.partial(self.__call__, obj)

    def _get_cache_key(self, *args: Any, **kwargs: Any) -> str:
        """Generate a cache key for the given arguments."""
        # Get the language from the instance's config if available
        language = None
        if args and args[0] is not None:
            instance = args[0]
            if hasattr(instance, "config"):
                config = instance.config
                if hasattr(config, "language"):
                    language = config.language

        # Include language in the cache key if available
        return f"{language}:{args!s}{kwargs!s}" if language else str(args) + str(kwargs)

    def invalidate_cache(self, *args: Any, **kwargs: Any) -> bool:
        """Invalidate cache entry for specific arguments.

        Returns:
            bool: True if an entry was invalidated, False if no matching entry was found.
        """
        key = self._get_cache_key(*args, **kwargs)
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def invalidate_all_cache(self) -> int:
        """Invalidate all cached values for this function.

        Returns:
            int: Number of entries invalidated.
        """
        count = len(self.cache)
        self.cache.clear()
        return count


# This decorator wrapper was added over class one for auto api document generation
def memorized(
    func: Optional[Callable[P, R]] = None,
    *,
    ttl: Optional[float] = None,
    max_size: Optional[int] = None,
) -> Union[Callable[P, R], Callable[[Callable[P, R]], Callable[P, R]]]:
    """Memorize function results to avoid repeated API calls.

    Args:
        func: The function to memoize
        ttl: Time to live in seconds. If specified, cached values will expire after this duration.
             Default is None (no expiration).
        max_size: Maximum number of entries to store in the cache. If specified, uses a
             least-recently-used (LRU) strategy to evict old entries when the cache is full.
             Default is None (unlimited cache size).

    The decorated function will have the following methods added:
        invalidate_cache(*args, **kwargs): Invalidate cache for specific arguments
        invalidate_all_cache(): Invalidate all cached values for this function
    """
    if func is None:
        # Called as @memorized(ttl=300, max_size=1000)
        return functools.partial(memorized, ttl=ttl, max_size=max_size)

    # Called as @memorized
    memoize = memoized_class(func, ttl=ttl, max_size=max_size)

    @functools.wraps(func)
    def helper(*args: Any, **kwargs: Any) -> Any:
        return memoize(*args, **kwargs)

    # Add cache invalidation methods to the decorated function
    helper.invalidate_cache = memoize.invalidate_cache
    helper.invalidate_all_cache = memoize.invalidate_all_cache

    return helper


def clean_infobox(text: str) -> str:
    text = re.sub(r"\[\d\]", "", text)
    text = re.sub(r"\n", " ", text)
    if sys.version_info[0] < 3:
        text = text.replace("\xa0", " ")
    else:
        text = text.replace("\xa0", " ")
    return text.strip()
