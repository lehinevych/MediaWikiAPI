from __future__ import annotations
import sys
import re
import collections
import functools
from collections.abc import Callable
from typing import Dict, TypeVar, Any, Optional

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
    If called later with the same arguments,
    the cached value is returned (not reevaluated).
    """

    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func
        self.cache: Dict[str, Any] = {}
        functools.update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        is_uncacheable = [not isinstance(ar, collections.abc.Hashable) for ar in args]
        if any(is_uncacheable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args, **kwargs)
        key = str(args) + str(kwargs)
        if key in self.cache:
            return self.cache[key]
        else:
            value = self.func(*args, **kwargs)
            self.cache[key] = value
            return value

    def __repr__(self) -> Any:
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj: Optional[R], objtype: Optional[R]) -> Any:
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


# This decorator wrapper was added over class one for auto api document generation
def memorized(func: Callable[..., Any]) -> Callable[..., Any]:
    memoize = memoized_class(func)

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
