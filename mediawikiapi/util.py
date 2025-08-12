from __future__ import annotations

import collections
import functools
import re
import sys
import time
from collections.abc import Callable
from typing import Any, Dict, Optional, TypeVar, Union

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
    """

    def __init__(
        self, func: Optional[Callable[..., Any]] = None, *, ttl: Optional[float] = None
    ) -> None:
        self.func = func
        self.ttl = ttl
        self.cache: Dict[str, tuple[Any, float]] = {}  # (value, timestamp)

        # Handle both @memorized and @memorized(ttl=300) forms
        if func is not None:
            functools.update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        # Handle both @memorized and @memorized(ttl=300) forms
        if self.func is None:
            # Called as @memorized(ttl=300)
            func = args[0]
            wrapped = memoized_class(func=func, ttl=self.ttl)
            return wrapped

        is_uncacheable = [not isinstance(ar, collections.abc.Hashable) for ar in args]
        if any(is_uncacheable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args, **kwargs)

        # Get the language from the instance's config if available
        language = None
        if args and args[0] is not None:
            instance = args[0]
            if hasattr(instance, "config"):
                config = instance.config
                if hasattr(config, "language"):
                    language = config.language

        # Include language in the cache key if available
        key = f"{language}:{args!s}{kwargs!s}" if language else str(args) + str(kwargs)

        # Check if key exists in cache and if the cached value is not expired
        current_time = time.time()
        if key in self.cache:
            value, timestamp = self.cache[key]

            # If TTL is set and the cached value has expired, recompute
            if self.ttl is None or (current_time - timestamp) < self.ttl:
                return value

        # Compute new value and store with current timestamp
        value = self.func(*args, **kwargs)
        self.cache[key] = (value, current_time)
        return value

    def __repr__(self) -> Any:
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj: Optional[R], objtype: Optional[R]) -> Any:
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


# This decorator wrapper was added over class one for auto api document generation
def memorized(
    func: Optional[Callable[P, R]] = None, *, ttl: Optional[float] = None
) -> Union[Callable[P, R], Callable[[Callable[P, R]], Callable[P, R]]]:
    """Memorize function results to avoid repeated API calls.

    Args:
        func: The function to memoize
        ttl: Time to live in seconds. If specified, cached values will expire after this duration.
             Default is None (no expiration).
    """
    if func is None:
        # Called as @memorized(ttl=300)
        return functools.partial(memorized, ttl=ttl)

    # Called as @memorized
    memoize = memoized_class(func, ttl=ttl)

    @functools.wraps(func)
    def helper(*args: Any, **kwargs: Any) -> Any:
        return memoize(*args, **kwargs)

    return helper


def clean_infobox(text: str) -> str:
    text = re.sub(r"\[\d\]", "", text)
    text = re.sub(r"\n", " ", text)
    if sys.version_info[0] < 3:
        text = text.replace("\xa0", " ")
    else:
        text = text.replace("\xa0", " ")
    return text.strip()
