from __future__ import annotations

import collections
import functools
import sys
from collections.abc import Callable, Coroutine
from typing import Any, Dict, Optional, TypeVar, cast

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


class async_memoized_class:
    """
    Decorator.
    Caches an async function's return value each time it is called.
    If called later with the same arguments and language,
    the cached value is returned (not reevaluated).
    """

    def __init__(self, func: Callable[..., Coroutine[Any, Any, R]]) -> None:
        self.func = func
        self.cache: Dict[str, R] = {}
        functools.update_wrapper(self, func)

    async def __call__(self, *args: Any, **kwargs: Any) -> R:
        is_uncacheable = [not isinstance(ar, collections.abc.Hashable) for ar in args]
        if any(is_uncacheable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return await self.func(*args, **kwargs)

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

        if key in self.cache:
            return self.cache[key]
        else:
            value = await self.func(*args, **kwargs)
            self.cache[key] = value
            return value

    def __repr__(self) -> str:
        """Return the function's docstring."""
        return self.func.__doc__ or ""

    def __get__(
        self, obj: Optional[Any], objtype: Optional[Any]
    ) -> Callable[..., Coroutine[Any, Any, R]]:
        """Support instance methods."""
        return cast(
            Callable[..., Coroutine[Any, Any, R]],
            functools.partial(self.__call__, obj),
        )


# This decorator wrapper is added over class one for auto api document generation
def async_memorized(
    func: Callable[..., Coroutine[Any, Any, R]],
) -> Callable[..., Coroutine[Any, Any, R]]:
    """
    Decorator for memoizing async functions.
    Caches the function's return value each time it is called.
    """
    memoize = async_memoized_class(func)

    @functools.wraps(func)
    async def helper(*args: Any, **kwargs: Any) -> R:
        return await memoize(*args, **kwargs)

    return helper


# Reuse the clean_infobox function from the original util module
from .util import clean_infobox
